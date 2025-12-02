import json

from app.cache.utils import set_cache, get_cache, delete_cache
from app.core.config import settings
from app.schemas.inventory import InventorySchema


def get_inventory_cache_key(user_id: int) -> str:
    return f"user:{user_id}:inventory"


async def set_inventory_cache(user_id: int, inventories: list[InventorySchema]):
    key = get_inventory_cache_key(user_id)

    inventories_data = [json.loads(i.model_dump_json()) for i in inventories]

    await set_cache(key, inventories_data, settings.inventory_ttl)


async def get_inventory_cache(user_id: int) -> list[InventorySchema] | None:
    key = get_inventory_cache_key(user_id)

    inventories_data = await get_cache(key)
    if not inventories_data:
        return None

    return [InventorySchema(**i) for i in inventories_data]


async def invalidate_inventory_cache(user_id: int):
    key = get_inventory_cache_key(user_id)

    await delete_cache(key)
