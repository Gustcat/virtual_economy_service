from app.cache.utils import (
    set_cache_with_idempotency,
    get_cache_with_idempotency,
)
from app.core.config import settings
from app.schemas.purchase import PurchaseRequest, PurchaseResponse


def get_purchase_cache_key(idempotency_key: str) -> str:
    return f"transaction:{idempotency_key}"


async def set_purchase_cache(
    idempotency_key: str,
    purchase_request: PurchaseRequest,
    purchase_response: PurchaseResponse,
):
    key = get_purchase_cache_key(idempotency_key)

    await set_cache_with_idempotency(
        key, purchase_request, purchase_response, settings.transaction_ttl
    )


async def get_purchase_cache(
    idempotency_key: str, purchase_request: PurchaseRequest
) -> PurchaseResponse | None:
    key = get_purchase_cache_key(idempotency_key)

    return await get_cache_with_idempotency(key, purchase_request, PurchaseResponse)
