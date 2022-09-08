import requests

from ..types import Network
from ..utils import handle_requests_errors
from .order import ManagedOrder
from .types import (
    OrderApiCreationResponse,
    OrderbookApiResponse,
    OrdersApiResponse,
    OrderWithSignature,
    Pair,
    PairsApiResponse,
)


class Api:

    url: str
    network: Network

    prefix: str
    prefix_p2p: str

    def __init__(self, network: Network, url: str, type: str) -> None:
        self.url = url
        self.network = network

        self.prefix = f"{self.url}/{type}/orders/{network}"
        self.prefix_p2p = f"{self.url}/{type}/p2p/{network}"

    def get_orders_by_address(
        self, prefix: str, maker_or_taker: str, address: str
    ) -> OrdersApiResponse:
        res = requests.get(f"{prefix}/{maker_or_taker}/{address}")
        handle_requests_errors(res)

        return res.json()

    def get_orders_by_maker(self, maker: str) -> OrdersApiResponse:
        return self.get_orders_by_address(self.prefix, "maker", maker)

    def get_p2p_orders_by_maker(self, maker: str) -> OrdersApiResponse:
        return self.get_orders_by_address(self.prefix_p2p, "maker", maker)

    def create_order_generic(
        self, prefix: str, order: OrderWithSignature
    ) -> OrderApiCreationResponse:
        res = requests.post(prefix, json=order.cast_to_dict())
        handle_requests_errors(res)

        return res.json()

    def create_order(self, order: OrderWithSignature) -> OrderApiCreationResponse:
        return self.create_order_generic(self.prefix, order)

    def create_p2p_order(self, order: OrderWithSignature) -> OrderApiCreationResponse:
        return self.create_order_generic(self.prefix_p2p, order)

    def get_orderbook_pairs(self) -> list[Pair]:
        res = requests.get(f"{self.prefix}/pairs")
        handle_requests_errors(res)

        casted: PairsApiResponse = res.json()
        return casted["pairs"]

    def get_orderbook(self, maker_asset: str, taker_asset: str) -> list[ManagedOrder]:
        res = requests.get(
            f"{self.prefix}/orderbook/maker/{maker_asset}/taker/{taker_asset}"
        )
        handle_requests_errors(res)

        casted: OrderbookApiResponse = res.json()
        return [ManagedOrder(order) for order in casted["orders"]]


def create_fungible_api(network: Network, url: str) -> Api:
    return Api(network, url, "ft")


def create_non_fungible_api(network: Network, url: str) -> Api:
    return Api(network, url, "nft")
