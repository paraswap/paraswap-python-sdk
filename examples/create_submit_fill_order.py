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
    # get api url from .env
    # our prod is http://api.paraswap.io
    api_url = environ.get("PARASWAP_URL")
    if api_url is None:
        print("missing api url")
        sys.exit(1)

    # init private key 1
    pk1 = environ.get("PK1")
    # init private key 2
    pk2 = environ.get("PK2")

    # use network polygon for example
    network = Network.Polygon
    # do a map of rpc providers
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
    # initialize http rpc provider
    provider = HTTPProvider(http_providers[network])

    # initialize web3
    web3 = Web3(provider)

    # create web3 account with pk1
    account1 = web3.eth.account.from_key(pk1)

    # create web3 account with pk2
    account2 = web3.eth.account.from_key(pk2)

    # hack to make PoA work (for example polygon)
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # create order helper object, TODO: maybe rename it to augustusRFQ helper
    # orderHelper is an helper for the augustusRFQ contract
    orderHelper = OrderHelper(
        network,
        web3,
    )

    # get ftApi object instance
    # fungible api is a wrapper to our limit orders api
    ftApi = create_fungible_api(network, api_url)

    # create_managed_order is used to createa a limit order that our backend track fillability
    # and also using for pricing inside paraswap protocol
    order = create_managed_order(
        expiry=0,  # 0 means the order never expire
        maker=account1.address,  # account1 is the maker of the order
        maker_asset=MAKER_ASSET,  # account1 is selling maker_asset
        taker_asset=TAKER_ASSET,  # account1 is buying taker_asset
        maker_amount=1000000000000,  # amount of maker_asset that account1 is selling
        taker_amount=845718000000,  # amount of taker_asset that account1 is buying
    )

    # The created order needs to be sign with an account to be valid
    orderWithSignature = orderHelper.sign_order(account1, order)

    # send this signed order to our centralised api.
    # It means that the order will be use in pricing
    res = ftApi.create_order(orderWithSignature)
    print("Order created", res)
    print("-----")

    # get orders create by account1
    ordersResponse = ftApi.get_orders_by_maker(account1.address)

    # get the array of orders
    orders = ordersResponse["orders"]

    # get the first created order from the list probably the one jus tcreated
    orderFromApi = orders[0]

    # check if it's the same as the one just created
    if orderWithSignature.signature != orderFromApi["signature"]:
        print("Did not find the order kill process")
        sys.exit(1)

    print("Get my orders found the created order", orderFromApi)
    print("-----")

    # get the whole order book first page
    orderbook = ftApi.get_orderbook()
    orders = orderbook["orders"]

    # find the created order in the orderbook
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

    # erc20 helper is an ERC20 contract wrapper
    daiHelper = Erc20Helper(web3, TAKER_ASSET)

    # check allowance of takerAsset token for account2 and augustus_rfq_address
    allowance = daiHelper.allowance(account2.address, orderHelper.augustus_rfq_address)

    print("Current allowance to augustus rfq", allowance)

    # get the nonce of the wallet:
    nonce = web3.eth.get_transaction_count(account2.address)
    print(f"account2 nonce {nonce}")

    tx_params: TxParams = {
        "from": account2.address,
        "nonce": nonce,
        "gasPrice": web3.toWei(GAS_PRICE, "gwei"),
    }
    # check if the allowance is lower that the order swappable_balance
    if allowance < found_order.swappable_balance:
        # account2 approve taker_asset to augustus for swappable_balance amount
        tx = daiHelper.approve(
            orderHelper.augustus_rfq_address,
            found_order.swappable_balance,
            tx_params=tx_params,
        )
        # account2 sign tx
        signed = account2.sign_transaction(tx)
        # send the tx to rpc node
        tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction).hex()

        print(f"Approve asset {TAKER_ASSET} hash is {tx_hash}")
        sys.exit(1)

    # tx = orderHelper.cancel_order(found_order.hash, tx_params)
    # account2 create tx to fill order
    tx = orderHelper.fill_order(found_order.order_with_signature, tx_params)

    # sign the tx
    signed = account2.sign_transaction(tx)

    # send the tx to rpc node
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction).hex()

    print(f"Filled order hash is {tx_hash}")


if __name__ == "__main__":
    main()
