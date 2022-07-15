import brownie
from brownie import Contract

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

def test_can_create(BalancerGlobal):
    example_gauges = [
        '0xE867AD0a48e8f815DC0cda2CDb275e0F163A480b',
        '0xf01541837CF3A64BC957F53678b0AB113e92911b',
        '0xc3bB46B8196C3F188c6A373a6C4Fde792CA78653'
    ]

    gauge_controller = Contract("0xC128468b7Ce63eA702C1f104D55A2566b13D3ABD")
    registry = Contract("0x78f73705105A63e06B932611643E0b210fAE93E9")
    for g in example_gauges:
        token = Contract(g).lp_token()
        print(f'can create (from factory): {BalancerGlobal.canCreateVaultPermissionlessly(g)}')
        print(f'token: {token}')
        print(f'is registered: {registry.isRegistered(token)}')
        print(f'DEFAULT type vault for token: {registry.latestVault(token)}')
        print(f'AUTOMATED type vault for token: {registry.latestVault(token, 1)}\n')




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

    