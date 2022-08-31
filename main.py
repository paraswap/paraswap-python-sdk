from src.types import Config, Network
from src.sdk import Sdk

from os import environ
from dotenv import load_dotenv

from src.types import Network

load_dotenv()

http_providers = {
    Network.Ethereum: environ.get('RPC_HTTP_1'),
    Network.Optimism: environ.get('RPC_HTTP_10'),
    Network.Bsc: environ.get('RPC_HTTP_56'),
    Network.Polygon: environ.get('RPC_HTTP_137'),
    Network.Fantom: environ.get('RPC_HTTP_250'),
    Network.Arbiturm: environ.get('RPC_HTTP_42161'),
    Network.Avalanche: environ.get('RPC_HTTP_43114'),
}

# config = Config(enabled_networks=[Network.Optimism], http_providers= { Network.Optimism: 'test'})
config = Config(enabled_networks=[Network.Optimism], http_providers=http_providers)


sdk = Sdk(config)
