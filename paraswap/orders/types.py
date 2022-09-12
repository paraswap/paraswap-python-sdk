from enum import Enum, IntEnum
from typing import Optional, TypedDict

from eip712_structs import Address, EIP712Struct, Uint
from typing_extensions import NotRequired

# struct Order {
#     uint256 nonceAndMeta; // Nonce and taker specific metadata
#     uint128 expiry;
#     address makerAsset;
#     address takerAsset;
#     address maker;
#     address taker;  // zero address on orders executable by anyone
#     uint256 makerAmount;
#     uint256 takerAmount;
# }


class Order(EIP712Struct):
    nonceAndMeta = Uint(256)
    expiry = Uint(128)
    makerAsset = Address()
    takerAsset = Address()
    maker = Address()
    taker = Address()
    makerAmount = Uint(256)
    takerAmount = Uint(256)


class OrderWithSignature:
    order: Order
    signature: str
    hash: str

    def __init__(self, order: Order, signature: str, hash: str) -> None:
        self.order = order
        self.signature = signature
        self.hash = hash

    def cast_to_dict(self):
        order = self.order.data_dict()
        return {
            "nonceAndMeta": str(order["nonceAndMeta"]),
            "expiry": str(order["expiry"]),
            "maker": str(order["maker"]),
            "taker": str(order["taker"]),
            "makerAsset": str(order["makerAsset"]),
            "takerAsset": str(order["takerAsset"]),
            "makerAmount": str(order["makerAmount"]),
            "takerAmount": str(order["takerAmount"]),
            "signature": self.signature,
        }


class AssetType(IntEnum):
    ERC20 = (0,)
    ERC1155 = (1,)
    ERC712 = (2,)


# struct OrderNFT {
#     uint256 nonceAndMeta; // Nonce and taker specific metadata
#     uint128 expiry;
#     uint256 makerAsset;
#     uint256 makerAssetId; // simply ignored in case of ERC20s
#     uint256 takerAsset;
#     uint256 takerAssetId; // simply ignored in case of ERC20s
#     address maker;
#     address taker;  // zero address on orders executable by anyone
#     uint256 makerAmount;
#     uint256 takerAmount;
# }


class OrderNFT(EIP712Struct):
    nonceAndMeta = Uint(256)
    expiry = Uint(128)
    maker = Address()
    taker = Address()
    makerAsset = Uint(256)
    makerAssetId = Uint(256)
    takerAsset = Uint(256)
    takerAssetId = Uint(256)
    makerAmount = Uint(256)
    takerAmount = Uint(256)


class OrderType(Enum):
    LIMIT = "LIMIT"
    P2P = "P2P"


class OrderState(Enum):
    PENDING = "PENDING"
    FULFILLED = "FULFILLED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class OrderApiResponse(TypedDict):
    expiry: int
    createdAt: int
    transactionHash: NotRequired[str]
    chainId: int
    nonceAndMeta: str
    maker: str
    taker: str
    takerFromMeta: str
    makerAsset: str
    takerAsset: str
    makerAmount: str
    fillableBalance: str
    swappableBalance: str
    makerBalance: str
    isFillOrKill: bool
    takerAmount: str
    signature: str
    orderHash: str
    permitMakerAsset: Optional[str]
    type: OrderType
    state: OrderState


class OrderApiCreationResponse(TypedDict):
    order: OrderApiResponse


class OrdersApiResponse(TypedDict):
    limit: int
    offset: int
    orders: list[OrderApiResponse]
    total: int
    hasMore: bool


class OrderbookApiResponse(TypedDict):
    orders: list[OrderApiResponse]


class Pair(TypedDict):
    makerAsset: str
    takerAsset: str


class PairsApiResponse(TypedDict):
    sucess: bool
    pairs: list[Pair]
