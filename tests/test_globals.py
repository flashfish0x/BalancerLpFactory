import brownie
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

    