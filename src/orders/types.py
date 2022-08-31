from eip712_structs import EIP712Struct, Uint, Address
from enum import IntEnum

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
    maker = Address()
    taker = Address()
    makerAsset = Uint(256)
    takerAsset = Uint(256)
    makerAmount = Uint(256)
    takerAmount = Uint(256)

class OrderWithSignature():
    order: Order
    signature: str

    def __init__(self, order: Order, signature: str) -> None:
        self.order = order
        self.signature = signature

class AssetType(IntEnum):
    ERC20 = 0,
    ERC1155 = 1,
    ERC712 = 2,

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
