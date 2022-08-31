from eip712_structs import Address, EIP712Struct, Uint
from typing import TypeVar
from enum import Enum, IntEnum

class Network(Enum):
    Ethereum = 1
    Optimism = 10
    Bsc = 56
    Polygon = 137
    Fantom = 250
    Arbiturm = 42161
    Avalanche = 43114

T = TypeVar('T')

MapToNetwork = dict[Network, T]

class Config():
    enabled_networks: list[Network]
    http_providers: MapToNetwork[str] = {}

    def __init__(self, enabled_networks: list[Network], http_providers: MapToNetwork[str]) ->  None:
        self.enabled_networks = enabled_networks
        self.http_providers = http_providers

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
    maker: Address
    taker: Address
    makerAsset = Uint(256)
    takerAsset = Uint(256)
    makerAmount = Uint(256)
    takerAmount = Uint(256)

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
    maker: Address
    taker: Address
    makerAsset = Uint(256)
    makerAssetId = Uint(256)
    takerAsset = Uint(256)
    takerAssetId = Uint(256)
    makerAmount = Uint(256)
    takerAmount = Uint(256)
