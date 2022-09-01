from os import environ
from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware
from paraswap.orders.order import createOrder
from paraswap.types import Network
from paraswap.orders.order_helper import OrderHelper, OrderWithSignature
from paraswap.orders.fungible_api import FungibleApi
from paraswap.types import Network

from dotenv import load_dotenv

load_dotenv()

api_url = 'http://api.paraswap.io'
order_hash = '0x6f1719be180c3b0987bbeaf63673b05577a0a98aa60c5704532a7e9c5783912c'
pk = environ.get('PK')
http_providers = {
    Network.Ethereum: environ.get('RPC_HTTP_1'),
    Network.Ropsten: environ.get('RPC_HTTP_3'),
    Network.Optimism: environ.get('RPC_HTTP_10'),
    Network.Bsc: environ.get('RPC_HTTP_56'),
    Network.Polygon: environ.get('RPC_HTTP_137'),
    Network.Fantom: environ.get('RPC_HTTP_250'),
    Network.Arbiturm: environ.get('RPC_HTTP_42161'),
    Network.Avalanche: environ.get('RPC_HTTP_43114'),
}
provider = HTTPProvider(http_providers[Network.Polygon])
web3 = Web3(provider)
account = web3.eth.account.from_key(pk)
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
onChainHelper = OrderHelper(
    Network.Polygon,
    web3,
)

ftApi = FungibleApi(Network.Polygon, api_url)
bo = ftApi.get_orders_by_maker(account.address)

nonce = web3.eth.get_transaction_count(account.address)

# res = onChainHelper.cancel_order(order_hash, {
#     'nonce': nonce,
#     'gasPrice': web3.toWei('35', 'gwei'),
# })

order = createOrder(
    nonce_and_meta=3490796090708800604682573566392112679433383115782363129776701440,
    expiry=0,
    maker='0x05182e579fdfcf69e4390c3411d8fea1fb6467cf',
    taker='0xdef171fe48cf0115b1d80b88dc8eab59176fee57',
    maker_asset='0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270',
    taker_asset='0x8f3cf7ad23cd3cadbd9735aff958023239c6a063',
    maker_amount=100000000000000,
    taker_amount=84571800000000
)

# orderWithSignature = OrderWithSignature(order, '0x24d374f78eeaa0fd0d12163c4ef582027c00685b0a6b4d08ad1405267301aec82a6730e586b801bc12be5c0fb1f88ae75e448e5980b3d38710d2156c933fe5de1c')

res = onChainHelper.sign_order(account, order)

print(res.signature, res.hash)

# res = ftApi.create_order(orderWithSignature)
# print(res)

# res = onChainHelper.fill_order(orderWithSignature, {
#     'nonce': nonce,
#     'gasPrice': web3.toWei('35', 'gwei')
# })

# signed = account.sign_transaction(res)
#
# tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
# print(tx_hash.hex())
