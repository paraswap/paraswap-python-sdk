import sys
from os import environ

from dotenv import load_dotenv
from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware
from web3.types import TxParams

from paraswap.orders.fungible_api import create_fungible_api
from paraswap.orders.order import create_managed_order
from paraswap.orders.order_helper import OrderHelper
from paraswap.types import Network
from paraswap.utils import Erc20Helper

load_dotenv()

MAKER_ASSET = "0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270"
TAKER_ASSET = "0x8f3cf7ad23cd3cadbd9735aff958023239c6a063"
GAS_PRICE = "50"


def main():
    api_url = environ.get("PARASWAP_URL")
    if api_url is None:
        print("missing api url")
        sys.exit(1)

    pk1 = environ.get("PK1")
    pk2 = environ.get("PK2")

    http_providers = {
        Network.Ethereum: environ.get("RPC_HTTP_1"),
        Network.Ropsten: environ.get("RPC_HTTP_3"),
        Network.Optimism: environ.get("RPC_HTTP_10"),
        Network.Bsc: environ.get("RPC_HTTP_56"),
        Network.Polygon: environ.get("RPC_HTTP_137"),
        Network.Fantom: environ.get("RPC_HTTP_250"),
        Network.Arbiturm: environ.get("RPC_HTTP_42161"),
        Network.Avalanche: environ.get("RPC_HTTP_43114"),
    }
    provider = HTTPProvider(http_providers[Network.Polygon])
    web3 = Web3(provider)

    account1 = web3.eth.account.from_key(pk1)
    account2 = web3.eth.account.from_key(pk2)

    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    orderHelper = OrderHelper(
        Network.Polygon,
        web3,
    )

    network = Network.Polygon
    ftApi = create_fungible_api(network, api_url)

    order = create_managed_order(
        expiry=0,
        maker="0x05182e579fdfcf69e4390c3411d8fea1fb6467cf",
        maker_asset=MAKER_ASSET,
        taker_asset=TAKER_ASSET,
        maker_amount=1000000000000,
        taker_amount=845718000000,
    )

    orderWithSignature = orderHelper.sign_order(account1, order)

    res = ftApi.create_order(orderWithSignature)
    print("Order created", res)
    print("-----")

    ordersResponse = ftApi.get_orders_by_maker(account1.address)
    orders = ordersResponse["orders"]
    orderFromApi = orders[0]

    if orderWithSignature.signature != orderFromApi["signature"]:
        print("Did not find the order kill process")
        sys.exit(1)

    print("Get my orders found the created order", orderFromApi)
    print("-----")

    orderbook = ftApi.get_orderbook()
    orders = orderbook["orders"]

    found_order = None
    for _order in orders:
        if _order.signature == orderWithSignature.signature:
            found_order = _order
            break

    if found_order is None:
        print("order created not found in the orderbook")
        sys.exit(1)

    print("signature", found_order.signature)
    print("orderHash", found_order.hash)

    daiHelper = Erc20Helper(web3, TAKER_ASSET)

    allowance = daiHelper.allowance(account2.address, orderHelper.augustus_rfq_address)

    print("Current allowance to augustus rfq", allowance)

    nonce = web3.eth.get_transaction_count(account2.address)
    print(f"account2 nonce {nonce}")

    tx_params: TxParams = {
        "from": account2.address,
        "nonce": nonce,
        "gasPrice": web3.toWei(GAS_PRICE, "gwei"),
    }
    if allowance < found_order.swappable_balance:
        tx = daiHelper.approve(
            orderHelper.augustus_rfq_address,
            found_order.swappable_balance,
            tx_params=tx_params,
        )
        signed = account2.sign_transaction(tx)
        tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction).hex()

        print(f"Approve asset {TAKER_ASSET} hash is {tx_hash}")
        sys.exit(1)

    # tx = orderHelper.cancel_order(found_order.hash, tx_params)
    tx = orderHelper.fill_order(found_order.order_with_signature, tx_params)
    signed = account2.sign_transaction(tx)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction).hex()

    print(f"Filled order hash is {tx_hash}")


if __name__ == "__main__":
    main()

# res = onChainHelper.fill_order(orderWithSignature, {
#     'nonce': nonce,
#     'gasPrice': web3.toWei('35', 'gwei')
# })

# signed = account.sign_transaction(res)
#
# tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
# print(tx_hash.hex())
