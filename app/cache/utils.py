import hashlib
import json
import logging
from typing import Any

from pydantic import BaseModel
from redis import asyncio as aio_redis

from app.core.config import settings
from app.core.exceptions import IdempotencyKeyConflictError

logger = logging.getLogger(__name__)

redis = aio_redis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)


async def set_cache(key: str, value: Any, ttl: int):
    logging.debug(f"Set cache: {key} = {value}")
    value = json.dumps(value)
    await redis.set(key, value, ex=ttl)


async def get_cache(key: str) -> Any | None:
    value = await redis.get(key)
    if value:
        logging.debug(f"Get cache: {key} = {value}")
        return json.loads(value)
    return None


async def delete_cache(key: str):
    logging.info(f"Invalidate cache for {key}")
    await redis.delete(key)


async def get_hash_from_base_model(request: BaseModel) -> str:
    data = request.model_dump(mode="json")

    model_json = json.dumps(data, sort_keys=True)
    return hashlib.sha256(model_json.encode()).hexdigest()


async def set_cache_with_idempotency(key: str, request, response: BaseModel, ttl: int):
    request_hash = await get_hash_from_base_model(request)

    value = {
        "request_hash": request_hash,
        "response": json.loads(response.model_dump_json()),
    }

    await set_cache(key, value, ttl)


async def get_cache_with_idempotency(
    key: str, request: BaseModel, response_model: type[BaseModel]
) -> BaseModel | None:
    cached_data = await get_cache(key)
    if not cached_data:
        return None

    cached_hash = cached_data["request_hash"]
    current_hash = await get_hash_from_base_model(request)
    if cached_hash != current_hash:
        raise IdempotencyKeyConflictError

    value = cached_data["response"]
    logging.debug(f"Get cache: {key} = {value}")

    return response_model(**value)
