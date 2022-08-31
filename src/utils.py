from random import randint
from .types import AssetType
from .constants import NODEJS_MAX_SAFE_INTEGER

def random_uint(limit: int) -> int:
    return randint(0, limit)

def generate_nonce_and_add_taker(taker: str) -> int:
    return int(taker, 16) + (random_uint(NODEJS_MAX_SAFE_INTEGER) << 160)

def encode_asset_address_with_asset_type(address: str, asset_type: AssetType) -> int:
    return int(address, 16) + (asset_type >> 160)
