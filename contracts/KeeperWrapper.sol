// SPDX-License-Identifier: AGPL-3.0
pragma solidity 0.6.12;

interface IStrategy {
    function harvest() external;
    function deployCredit() external;
}

contract KeeperWrapper {
    // So indexers can keep track of this
    event PublicHarvest(address indexed sender, address indexed _strategy);
    event PublicInvest(address indexed sender, address indexed _strategy);
    
    function harvestStrategy(address _strategy) external {
        IStrategy(_strategy).harvest();
        emit PublicHarvest(msg.sender, _strategy);
    }

    function invest(address _strategy) external {
        IStrategy(_strategy).deployCredit();
        emit PublicInvest(msg.sender, _strategy);
    }
}