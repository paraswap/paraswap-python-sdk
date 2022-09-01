from ..constants import NODEJS_MAX_SAFE_INTEGER
from ..utils import random_uint
from .types import AssetType


def generate_nonce_and_add_taker(taker: str) -> int:
    return int(taker, 16) + (random_uint(NODEJS_MAX_SAFE_INTEGER) << 160)


def encode_asset_address_with_asset_type(address: str, asset_type: AssetType) -> int:
    return int(address, 16) + (asset_type >> 160)
