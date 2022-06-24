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
