from typing import TypedDict

from web3 import Web3

from ..config import AUGUSTUS
from ..constants import MAX_UINT256_VALUE, NULL_ADDRESS
from ..types import Network
from .types import (
    Order,
    OrderApiResponse,
    OrderNFT,
    OrderState,
    OrderType,
    OrderWithSignature,
)
from .utils import (
    AssetType,
    encode_asset_address_with_asset_type,
    generate_nonce_and_add_taker,
    random_uint,
)


def create_order(
    expiry: int,
    maker: str,
    taker: str,
    maker_asset: str,
    taker_asset: str,
    maker_amount: int,
    taker_amount: int,
    nonce_and_meta: int = -1,
) -> Order:
    if nonce_and_meta == -1:
        nonce_and_meta = random_uint(MAX_UINT256_VALUE)

    return Order(
        nonceAndMeta=nonce_and_meta,
        expiry=expiry,
        maker=Web3.toChecksumAddress(maker),
        taker=Web3.toChecksumAddress(taker),
        makerAsset=Web3.toChecksumAddress(maker_asset),
        takerAsset=Web3.toChecksumAddress(taker_asset),
        makerAmount=maker_amount,
        takerAmount=taker_amount,
    )


def create_managed_p2p_order(
    network: Network,
    expiry: int,
    maker: str,
    maker_asset: str,
    taker_asset: str,
    maker_amount: int,
    taker_amount: int,
    actual_taker: str,
    taker: str = "",
):
    # encode taker address inside the nonce and meta and generate a random nonce
    nonce_and_meta = generate_nonce_and_add_taker(actual_taker)
    return create_order(
        expiry=expiry,
        maker=maker,
        taker=AUGUSTUS[network]
        if taker == ""
        else taker,  # ParaSwap managed orders ALWAYS go through AUGUSTUS
        maker_asset=maker_asset,
        taker_asset=taker_asset,
        maker_amount=maker_amount,
        taker_amount=taker_amount,
        nonce_and_meta=nonce_and_meta,
    )


def create_managed_order(
    expiry: int,
    maker: str,
    maker_asset: str,
    taker_asset: str,
    maker_amount: int,
    taker_amount: int,
    taker: str = "",
):
    nonce_and_meta = generate_nonce_and_add_taker(NULL_ADDRESS)
    return create_order(
        expiry=expiry,
        maker=maker,
        taker=NULL_ADDRESS
        if taker == ""
        else taker,  # ParaSwap managed orders ALWAYS go through AUGUSTUS
        maker_asset=maker_asset,
        taker_asset=taker_asset,
        maker_amount=maker_amount,
        taker_amount=taker_amount,
        nonce_and_meta=nonce_and_meta,
    )


def create_order_nft(
    maker: str,
    taker: str,
    maker_asset: str,
    maker_asset_type: AssetType,
    taker_asset: str,
    taker_asset_type: AssetType,
    maker_amount: int,
    taker_amount: int,
    maker_asset_id: int = 0,
    taker_asset_id: int = 0,
    nonce_and_meta: int = -1,
) -> OrderNFT:
    if nonce_and_meta == -1:
        nonce_and_meta = random_uint(MAX_UINT256_VALUE)

    return OrderNFT(
        nonceAndMeta=nonce_and_meta,
        maker=Web3.toChecksumAddress(maker),
        taker=Web3.toChecksumAddress(taker),
        makerAsset=encode_asset_address_with_asset_type(maker_asset, maker_asset_type),
        makerAssetId=maker_asset_id,
        takerAsset=encode_asset_address_with_asset_type(taker_asset, taker_asset_type),
        takerAssetId=taker_asset_id,
        makerAmount=maker_amount,
        takerAmount=taker_amount,
    )


def create_managed_order_nft(
    maker: str,
    taker: str,
    maker_asset: str,
    maker_asset_type: AssetType,
    taker_asset: str,
    taker_asset_type: AssetType,
    maker_amount: int,
    taker_amount: int,
    actual_taker: str,
    maker_asset_id: int = 0,
    taker_asset_id: int = 0,
) -> OrderNFT:
    # encode taker address inside the nonce and meta and generate a random nonce
    nonce_and_meta = generate_nonce_and_add_taker(actual_taker)
    return create_order_nft(
        maker=maker,
        taker=taker,
        maker_asset=maker_asset,
        maker_asset_type=maker_asset_type,
        taker_asset=taker_asset,
        taker_asset_type=taker_asset_type,
        maker_amount=maker_amount,
        taker_amount=taker_amount,
        maker_asset_id=maker_asset_id,
        taker_asset_id=taker_asset_id,
        nonce_and_meta=nonce_and_meta,
    )


class ManagedOrder:
    order_with_signature: OrderWithSignature
    fillable_balance: int
    swappable_balance: int
    maker_balance: int
    is_fill_or_kill: bool
    type: OrderType
    state: OrderState

    def __init__(self, order: OrderApiResponse) -> None:
        orderSolidity = create_order(
            expiry=order["expiry"],
            maker=order["maker"],
            taker=order["taker"],
            maker_asset=order["makerAsset"],
            taker_asset=order["takerAsset"],
            maker_amount=int(order["makerAmount"], 10),
            taker_amount=int(order["takerAmount"], 10),
            nonce_and_meta=int(order["nonceAndMeta"], 10),
        )

        self.order_with_signature = OrderWithSignature(
            order=orderSolidity,
            signature=order["signature"],
            hash=order["orderHash"],
        )

        self.fillable_balance = int(order["fillableBalance"], 10)
        self.swappable_balance = int(order["swappableBalance"], 10)
        self.maker_balance = int(order["makerBalance"], 10)
        self.is_fill_or_kill = order["isFillOrKill"]
        self.type = order["type"]
        self.state = order["state"]

    @property
    def maker_asset(self):
        return self.order_with_signature.order.makerAsset

    @property
    def taker_asset(self):
        return self.order_with_signature.order.makerAsset

    @property
    def signature(self):
        return self.order_with_signature.signature

    @property
    def hash(self):
        return self.order_with_signature.hash


class OrdersApiWithParsedOrders(TypedDict):
    limit: int
    offset: int
    orders: list[ManagedOrder]
    total: int
    hasMore: bool
