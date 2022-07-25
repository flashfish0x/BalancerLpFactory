# README

## BalancerGlobal.sol

https://github.com/flashfish0x/BalancerLpFactory/blob/ffe140fde292fc69d2a4c7b4ba89d49c568ebba2/contracts/BalancerGlobal.sol

This is our factory for creating yVaults for Balancer pool tokens, with one strategy to farm via Aura.
There are lots of setters that we can use to make changes to future vaults/strategies created by the factory.
The createNewVaultsAndStrategies function allows any user to create a yVault for a BPT by entering a gauge (provided one doesn't already exist).
The gauge is used to identify the lpToken and the Aura pid.
Then we create the new automated vault and the Aura strategy.
Finally we add the strategy to the vault.

## StrategyConvexFactoryClonable.sol

https://github.com/flashfish0x/BalancerLpFactory/blob/ffe140fde292fc69d2a4c7b4ba89d49c568ebba2/contracts/StrategyConvexFactoryClonable.sol

This is our Aura strategy that is created by BalancerGlobal and automatically added to each vault it creates.
It's a simple auto-compounder for Aura.
It deposits Balancer pool tokens into Aura and then periodically claims BAL and AURA rewards, swaps them for the vault's Balancer pool tokens, and deposits those back into Aura to earn more rewards.

## KeeperWrapper.sol

https://github.com/flashfish0x/BalancerLpFactory/blob/ffe140fde292fc69d2a4c7b4ba89d49c568ebba2/contracts/KeeperWrapper.sol

If set as the keeper of the strategy, this contract will make keeper functions (like harvest) public.

## BalancerZapper.sol

https://github.com/flashfish0x/BalancerLpFactory/blob/ffe140fde292fc69d2a4c7b4ba89d49c568ebba2/contracts/BalancerZapper.sol

This contract can be ignored. It's something related to a yswaps limitation.