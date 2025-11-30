import json
import logging

from datetime import datetime

from redis import asyncio as aioredis

from app.core.config import settings
from app.schemas.inventory import InventorySchema

logger = logging.getLogger(__name__)

redis = aioredis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)


async def set_inventory_cache(
    user_id: int, inventories: list[InventorySchema], ttl: int = settings.inventory_ttl
):
    key = f"user:{user_id}:inventory"

    inventories_data = [i.model_dump() for i in inventories]

    for i in inventories_data:
        i["purchased_at"] = i["purchased_at"].strftime("%Y-%m-%d %H:%M:%S")

    logging.debug(f"Set cache: {inventories_data}")
    value = json.dumps(inventories_data)
    await redis.set(key, value, ex=ttl)


async def get_inventory_cache(user_id: int) -> list[InventorySchema] | None:
    key = f"user:{user_id}:inventory"
    value = await redis.get(key)
    if value:
        inventories_data = json.loads(value)

        for i in inventories_data:
            i["purchased_at"] = datetime.strptime(
                i["purchased_at"], "%Y-%m-%d %H:%M:%S"
            )

        logging.debug(f"Get cache: {inventories_data}")
        return [InventorySchema(**i) for i in inventories_data]
    return None


async def invalidate_inventory_cache(user_id: int):
    key = f"user:{user_id}:inventory"
    logging.info(f"Invalidate cache for {key}")
    await redis.delete(key)
