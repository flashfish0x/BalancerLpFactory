import brownie
from brownie import ZERO_ADDRESS, Contract

def test_keepers(
    gov,
    accounts,
    keeper_contract,
    token,
    booster,
    interface,
    new_trade_factory,
    pid,
    strategist,
    vault,
    BalancerGlobal,
    whale,
    badgerweth_gauge,
    strategy,
    chain,
    balancer_global,
    amount,
):
    assert balancer_global.numVaults() == 1

    assert vault == balancer_global.deployedVaults(0)

    with brownie.reverts("Vault already exists"):
        balancer_global.createNewVaultsAndStrategies(badgerweth_gauge, {"from": strategist})

def test_can_create(balancer_global, strategy, strategist, new_registry, accounts):
    registry_owner = accounts.at(new_registry.owner(), force=True)
    new_registry.setApprovedVaultsOwner(balancer_global, True, {"from": registry_owner})
    new_registry.setRole(balancer_global, False, True, {"from": registry_owner})

    # New registry `0xFFFAB17b48914d2bAe231Bb380FAf8C05fE8E2fF`
    # Example LP Token `0x178E029173417b1F9C8bC16DCeC6f697bC323746`
    # Example Gauge: `0xDD4Db3ff8A37FE418dB6FF34fC316655528B6bbC`
    # Example Vault: `0xA9412Ffd7E0866755ae0dda3318470A61F62abe8`

    example_gauges = [
        '0x34f33CDaED8ba0E1CEECE80e5f4a73bcf234cfac',
        '0x605eA53472A496c3d483869Fe8F355c12E861e19',
        '0x79eF6103A513951a3b25743DB509E267685726B7',
        '0xDD4Db3ff8A37FE418dB6FF34fC316655528B6bbC', # Already created, should fail
    ]

    gauge_controller = Contract("0xC128468b7Ce63eA702C1f104D55A2566b13D3ABD")
    registry = Contract("0x78f73705105A63e06B932611643E0b210fAE93E9")
    for g in example_gauges:
        token = Contract(g).lp_token()
        print(f'can create (from factory): {balancer_global.canCreateVaultPermissionlessly(g)}')
        print(f'token: {token}')
        print(f'is registered: {registry.isRegistered(token)}')
        print(f'DEFAULT type vault for token: {registry.latestVault(token)}')
        print(f'AUTOMATED type vault for token: {registry.latestVault(token, 1)}\n')
        should_succeed = registry.latestVault(token) == ZERO_ADDRESS and registry.latestVault(token, 1) == ZERO_ADDRESS
        assert should_succeed == balancer_global.canCreateVaultPermissionlessly(g)
        if not should_succeed:
            with brownie.reverts("Vault already exists"):
                balancer_global.createNewVaultsAndStrategies(g, {"from": strategist})
        else:
            tx = balancer_global.createNewVaultsAndStrategies(g, {"from": strategist})


def test_keeps(
    gov,
    accounts,
    keeper_contract,
    token,
    booster,
    interface,
    new_trade_factory,
    pid,
    strategist,
    vault,
    BalancerGlobal,
    whale,
    other_gauge,
    strategy,
    StrategyConvexFactoryClonable,
    chain,
    balancer_global,
    amount,
):
    assert balancer_global.numVaults() == 1

    new_keep_crv = 4_000
    new_keep_cvx = 6_000
    voter_crv = whale
    voter_cvx = strategy

    balancer_global.setKeepCRV(new_keep_crv, voter_crv, {"from": gov})
    balancer_global.setKeepCVX(new_keep_cvx, voter_cvx, {"from": gov})

    t1 = balancer_global.createNewVaultsAndStrategies(
        other_gauge, {"from": gov}
    )

    new_strategy = StrategyConvexFactoryClonable.at(t1.events['NewAutomatedVault']['strategy'])

    assert new_strategy.localKeepCRV() == new_keep_crv
    assert new_strategy.localKeepCVX() == new_keep_cvx
    assert new_strategy.curveVoter() == voter_crv
    assert new_strategy.convexVoter() == voter_cvx

    