from fastapi import APIRouter, BackgroundTasks

from app.api.deps import IdempotencyKeyDep
from app.cache.balance_cache import get_balance_cache, set_balance_cache
from app.cache.inventory_cache import get_inventory_cache, set_inventory_cache
from app.db.session import SessionDep
from app.schemas.inventory import InventorySchema
from app.schemas.user import AddFundsResponse, AddFundsRequest
from app.services.inventory import InventoryService
from app.services.user import UserService

user_router = APIRouter()


@user_router.post("/{user_id}/add-funds/", response_model=AddFundsResponse)
async def add_funds(
    user_id: int,
    funds: AddFundsRequest,
    session: SessionDep,
    bg_tasks: BackgroundTasks,
    idempotency_key: IdempotencyKeyDep,
):
    balance_cache = await get_balance_cache(idempotency_key, funds)
    if balance_cache:
        return balance_cache

    user_service = UserService(session)
    new_balance = await user_service.add_funds(user_id, funds.amount)

    response = AddFundsResponse(balance=new_balance)
    bg_tasks.add_task(set_balance_cache, idempotency_key, funds, response)

    return response


@user_router.get("/{user_id}/inventory/", response_model=list[InventorySchema])
async def list_user_inventories(
    user_id: int, session: SessionDep, bg_tasks: BackgroundTasks
):
    inventories = await get_inventory_cache(user_id)
    if inventories:
        return inventories

    inventory_service = InventoryService(session)
    inventories = await inventory_service.list_user_inventories(user_id)

    bg_tasks.add_task(set_inventory_cache, user_id, inventories)

    return inventories
