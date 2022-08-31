from web3 import HTTPProvider, Web3
from .types import Config, MapToNetwork
from .exceptions import RpcHttpMissing

class Sdk():

    http_web3_providers: MapToNetwork[HTTPProvider] = {}
    _config: Config

    def __init__(self, config: Config) -> None:
        self._config = config

        for network in config.enabled_networks:
            if network not in config.http_providers:
                raise RpcHttpMissing('missing http provider for network', network)
            url = config.http_providers[network]
            self.http_web3_providers[network] = HTTPProvider(url)
