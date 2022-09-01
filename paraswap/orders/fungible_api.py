import requests

from ..types import Network
from ..utils import handle_requests_errors
from .types import OrderApiCreationResponse, OrdersApiResponse, OrderWithSignature


class FungibleApi:

    url: str
    network: Network

    prefix: str

    def __init__(self, network: Network, url: str) -> None:
        self.url = url
        self.network = network

        self.prefix = f"{self.url}/ft/orders/{self.network}"

    def get_orders_by_address(self, maker_or_taker: str, address: str):
        res = requests.get(f"{self.prefix}/{maker_or_taker}/{address}")
        handle_requests_errors(res)

        return res.json()

    def get_orders_by_maker(self, maker: str) -> OrdersApiResponse:
        return self.get_orders_by_address("maker", maker)

    def create_order(self, order: OrderWithSignature) -> OrderApiCreationResponse:
        res = requests.post(f"{self.prefix}/", json=order.cast_to_dict())
        handle_requests_errors(res)

        return res.json()
