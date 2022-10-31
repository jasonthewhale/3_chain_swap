from sympy import poly
from web3 import Web3, HTTPProvider
from chain_constants import*

web3_poly = Web3(HTTPProvider(POLYGON_rpc))
web3_avax = Web3(HTTPProvider(AVALANCHE_rpc))
web3_moon = Web3(HTTPProvider(MOONRIVER_rpc))

poly_swap_contract = web3_poly.eth.contract(address=QUICKSWAP_address, abi=QUICKSWAP_abi)
poly_weth_contract = web3_poly.eth.contract(address=POLYGON_weth_address, abi=POLYGON_weth_abi)

avax_swap_contract = web3_avax.eth.contract(address=PANGOLIN_address, abi=PANGOLIN_abi)
wavax_contract = web3_avax.eth.contract(address=WAVAX_address, abi=WAVAX_abi)

moon_swap_contract = web3_moon.eth.contract(address=SOLARBEAM_address, abi=SOLARBEAM_abi)
wmovr_contract = web3_moon.eth.contract(address=WMOVR_address, abi=WMOVR_abi)

poly_pool = "0x5F819F510CA9B1469e6a3Ffe4ecD7F0C1126f8F5"
avax_pool = "0xA34862a7de51a0E1aEE6d3912c3767594390586d"
moonriver_pool = "0x6ed3bc66DFCc5AC05daeC840A75836da935faC97"

def check_pool_eth(chain):
    if chain == "poly":
        print(web3_poly.fromWei(poly_weth_contract.functions.balanceOf(poly_pool).call(), "ether"))
        return poly_weth_contract.functions.balanceOf(poly_pool).call()
    elif chain == "avax":
        print(web3_avax.fromWei(wavax_contract.functions.balanceOf(avax_pool).call(), "ether"))
        return wavax_contract.functions.balanceOf(avax_pool).call()
    else:
        print(web3_moon.fromWei(wmovr_contract.functions.balanceOf(moonriver_pool).call(), "ether"))
        return wmovr_contract.functions.balanceOf(moonriver_pool).call()

def poly_swap(percentage):
    amount = int(check_pool_eth("poly")*percentage/100)
    path = [POLYGON_weth_address, '0x60bB3D364B765C497C8cE50AE0Ae3f0882c5bD05']
    expected_amount_out = poly_swap_contract.functions.getAmountsOut(amount, path).call()[-1]
    amount_out_min = int(expected_amount_out * (1-0.01))
    swap = poly_swap_contract.functions.swapExactTokensForTokens(amount, amount_out_min, path, WALLET, 1766964953)
    nonce = web3_poly.eth.getTransactionCount(WALLET)
    params = {
    'chainId': POLYGON_id,
    "value": web3_poly.toWei(0, 'ether'),
    'gasPrice': web3_poly.toWei(88, 'gwei'),
    "gas": 981250,
    "nonce": nonce,
    }
    try:
        tx = swap.buildTransaction(params)
        signed_tx = web3_poly.eth.account.sign_transaction(tx, PK)
        tx_hash = web3_poly.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Transaction Success! Transaction hash：{tx_hash.hex()}")
    except Exception as e:
        print(f"{WALLET}Transaction Failed!：", e)


def avax_swap(percentage):
    amount = int(check_pool_eth("avax")*percentage/100)
    path = [WAVAX_address, '0xeA6887e4a9CdA1B77E70129E5Fba830CdB5cdDef']
    expected_amount_out = avax_swap_contract.functions.getAmountsOut(amount, path).call()[-1]
    amount_out_min = int(expected_amount_out * (1-0.01))
    swap = avax_swap_contract.functions.swapExactTokensForTokens(amount,amount_out_min, path, WALLET, 1766964953)
    nonce = web3_avax.eth.getTransactionCount(WALLET)
    params = {
    'chainId': AVALANCHE_id,
    "value": web3_avax.toWei(0, 'ether'),
    'gasPrice': web3_avax.toWei(30, 'gwei'),
    "gas": 236609,
    "nonce": nonce,
    }
    try:
        tx = swap.buildTransaction(params)
        signed_tx = web3_avax.eth.account.sign_transaction(tx, PK)
        tx_hash = web3_avax.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Transaction Success! Transaction hash：{tx_hash.hex()}")
    except Exception as e:
        print(f"{WALLET}Transaction Failed!：", e)

def moon_swap(percentage):
    amount = int(check_pool_eth("moonriver")*percentage/100)
    path = [WMOVR_address, '0x900f1Ec5819FA087d368877cD03B265Bf1802667']
    expected_amount_out = moon_swap_contract.functions.getAmountsOut(amount, path, 0).call()[-1]
    amount_out_min = int(expected_amount_out * (1-0.01))
    swap = moon_swap_contract.functions.swapExactTokensForTokens(amount,amount_out_min, path, WALLET, 1766964953)
    nonce = web3_moon.eth.getTransactionCount(WALLET)
    params = {
    'chainId': MOONRIVER_id,
    "value": web3_moon.toWei(0, 'ether'),
    'gasPrice': web3_moon.toWei(2.5, 'gwei'),
    "gas": 246018,
    "nonce": nonce,
    }
    try:
        tx = swap.buildTransaction(params)
        signed_tx = web3_moon.eth.account.sign_transaction(tx, PK)
        tx_hash = web3_moon.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Transaction Success! Transaction hash：{tx_hash.hex()}")
    except Exception as e:
        print(f"{WALLET}Transaction Failed!：", e)

def swap_all(percentage):
    poly_swap(percentage)
    avax_swap(percentage)
    moon_swap(percentage)


def moon_swap_amount(amount, nonce):
    amountin = web3_moon.toWei(amount, 'ether')
    path = [WMOVR_address, '0x900f1Ec5819FA087d368877cD03B265Bf1802667']
    expected_amount_out = moon_swap_contract.functions.getAmountsOut(amountin, path, 0).call()[-1]
    amount_out_min = int(expected_amount_out * (1-0.01))
    swap = moon_swap_contract.functions.swapExactTokensForTokens(amountin, amount_out_min, path, WALLET, 1766964953)
    params = {
    'chainId': MOONRIVER_id,
    "value": web3_moon.toWei(0, 'ether'),
    'gasPrice': web3_moon.toWei(5, 'gwei'),
    "gas": 176018,
    "nonce": nonce,
    }
    try:
        tx = swap.buildTransaction(params)
        signed_tx = web3_moon.eth.account.sign_transaction(tx, PK)
        tx_hash = web3_moon.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Transaction Success! Transaction hash：{tx_hash.hex()}")
    except Exception as e:
        print(f"{WALLET}Transaction Failed!：", e)

def improved_moon(amount):
    nonce = web3_moon.eth.getTransactionCount(WALLET)
    moon_swap_amount(amount/5, nonce)
    moon_swap_amount(amount, nonce+1)
