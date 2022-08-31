from .constants import MAX_UINT256_VALUE
from .utils import AssetType, encode_asset_address_with_asset_type, generate_nonce_and_add_taker, random_uint
from .types import Order, OrderNFT

def createOrder(
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
        maker=maker,
        taker=taker,
        makerAsset=maker_asset,
        takerAsset=taker_asset,
        makerAmount=maker_amount,
        takerAmount=taker_amount,
    )

def createManagedOrder(
    maker: str,
    taker: str,
    maker_asset: str,
    taker_asset: str,
    maker_amount: int,
    taker_amount: int,
    actual_taker: str,
):
    # encode taker address inside the nonce and meta and generate a random nonce
    nonce_and_meta = generate_nonce_and_add_taker(actual_taker)
    return createOrder(
        maker=maker,
        taker=taker,
        maker_asset=maker_asset,
        taker_asset=taker_asset,
        maker_amount=maker_amount,
        taker_amount=taker_amount,
        nonce_and_meta=nonce_and_meta,
    )

def createOrderNFT(
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
        maker=maker,
        taker=taker,
        makerAsset=encode_asset_address_with_asset_type(maker_asset, maker_asset_type),
        makerAssetId=maker_asset_id,
        takerAsset=encode_asset_address_with_asset_type(taker_asset, taker_asset_type),
        takerAssetId=taker_asset_id,
        makerAmount=maker_amount,
        takerAmount=taker_amount,
    )

def createManagedOrderNFT(
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
    return createOrderNFT(
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
