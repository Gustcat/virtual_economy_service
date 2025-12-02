from app.cache.utils import (
    set_cache_with_idempotency,
    get_cache_with_idempotency,
)
from app.core.config import settings
from app.schemas.user import AddFundsResponse, AddFundsRequest


def get_balance_cache_key(idempotency_key: str) -> str:
    return f"balance:{idempotency_key}"


async def set_balance_cache(
    idempotency_key: str,
    add_funds_request: AddFundsRequest,
    add_funds_response: AddFundsResponse,
):
    key = get_balance_cache_key(idempotency_key)

    await set_cache_with_idempotency(
        key, add_funds_request, add_funds_response, settings.balance_ttl
    )


async def get_balance_cache(
    idempotency_key: str, add_funds_request: AddFundsRequest
) -> AddFundsResponse | None:
    key = get_balance_cache_key(idempotency_key)

    return await get_cache_with_idempotency(key, add_funds_request, AddFundsResponse)
