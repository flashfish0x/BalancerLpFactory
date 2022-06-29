import brownie
def test_zap(
    BalancerZapper,
    accounts,
    interface,
    chain,
    Contract,
):
    whale = accounts.at('0xE78388b4CE79068e89Bf8aA7f218eF6b9AB0e9d0', force=True)
    weth = interface.ERC20('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', owner=whale)
    bvault= Contract('0xBA12222222228d8Ba445958a75a0704d566BF2C8', owner=whale)
    bpt = Contract('0x32296969Ef14EB0c6d29669C550D4a0449130230', owner=whale)

    actionId = '0xf741bc2f246e8cf02dc2f04d1c5136b613d963812e6b85d2e7e7a601a826c56b'


    
    # weth.approve(bvault, 2**256-1)
    bzap = whale.deploy(BalancerZapper)
    weth.approve(bzap, 2**256-1)

    # bvault.setRelayerApproval(whale, bzap, True)
    # authoriser = Contract(bvault.getAuthorizer(), owner=whale)
    # authoriser.grantRole(actionId, whale)


    
    pool_id = bpt.getPoolId() #'0x32296969ef14eb0c6d29669c550d4a0449130230000200000000000000000080'
    amountIn = 10*1e18
    max_amounts_in = [0, amountIn]
    bzap.joinPool(weth, amountIn, pool_id, whale, max_amounts_in, 0)

    print(bpt.balanceOf(whale))
    