from fastapi import APIRouter, BackgroundTasks

from app.cache.inventory_cache import get_inventory_cache, set_inventory_cache
from app.db.session import SessionDep
from app.schemas.inventory import InventorySchema
from app.schemas.user import AddFundsResponse, AddFundsRequest
from app.services.inventory import InventoryService
from app.services.user import UserService

user_router = APIRouter()


@user_router.post("/{user_id}/add-funds/", response_model=AddFundsResponse)
async def add_funds(user_id: int, funds: AddFundsRequest, session: SessionDep):
    user_service = UserService(session)
    new_balance = await user_service.add_funds(user_id, funds.amount)
    return AddFundsResponse(balance=new_balance)


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
