import brownie
from brownie import Contract
from brownie import config
import math


def test_claim_rewards(
    gov,
    token,
    vault,
    strategist,
    whale,
    strategy,
    chain,
    strategist_ms,
    interface,
    gauge,
    booster,
    rewardsContract,
    amount,
):
    ## deposit to the vault after approving
    startingWhale = token.balanceOf(whale)
    token.approve(vault, 2**256 - 1, {"from": whale})
    vault.deposit(amount, {"from": whale})
    newWhale = token.balanceOf(whale)
    booster.earmarkRewards(strategy.pid(), {"from": strategist})

    # this is part of our check into the staking contract balance
    stakingBeforeHarvest = rewardsContract.balanceOf(strategy)

    # harvest, store asset amount
    chain.sleep(1)
    strategy.harvest({"from": gov})
    chain.sleep(1)
    old_assets = vault.totalAssets()
    assert old_assets > 0
    assert token.balanceOf(strategy) == 0
    assert strategy.estimatedTotalAssets() > 0
    print("\nStarting Assets: ", old_assets / 1e18)

    # try and include custom logic here to check that funds are in the staking contract (if needed)
    assert rewardsContract.balanceOf(strategy) > stakingBeforeHarvest

    # simulate 6 hours of earnings so we don't outrun our convex earmark
    chain.sleep(21600)
    chain.mine(1)

    # harvest, store new asset amount
    chain.sleep(1)
    pending_rewards = strategy.claimableProfitInUsdt()
    assert strategy.stakedBalance() > 0
    assert token.balanceOf(strategy) == 0
    claimable_crv = strategy.claimableBalance()
    assert claimable_crv > 0
    print("\nPending claimable in USDT after 1 day: ", pending_rewards / 1e6)
    strategy._claimRewards({"from": whale}) 

    crv = interface.ERC20(strategy.crv())
    cvx = interface.ERC20(strategy.convexToken())

    assert crv.balanceOf(strategy) > 0
    assert cvx.balanceOf(strategy) > 0
    assert strategy.claimableProfitInUsdt() == 0
    chain.sleep(1)

    # withdraw and confirm that there's no more money, since rewards haven't been sold
    vault.withdraw({"from": whale})
    assert token.balanceOf(whale) == startingWhale
