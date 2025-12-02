from typing import Annotated

from fastapi import Header, Depends

from app.core.types import IdempotencyKey


async def get_idempotency_key(
    idempotency_key: IdempotencyKey = Header(..., alias="Idempotency-Key")
):
    return idempotency_key


IdempotencyKeyDep = Annotated[IdempotencyKey, Depends(get_idempotency_key)]
