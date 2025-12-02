from fastapi import APIRouter, BackgroundTasks

from app.api.deps import IdempotencyKeyDep
from app.cache.inventory_cache import invalidate_inventory_cache
from app.cache.purchase_cache import get_purchase_cache, set_purchase_cache
from app.db.session import SessionDep
from app.schemas.inventory import UseProductResponse, UseProductRequest
from app.schemas.purchase import PurchaseResponse, PurchaseRequest
from app.services.inventory import InventoryService
from app.services.purchase import PurchaseService

product_router = APIRouter()


@product_router.post("/{product_id}/purchase/", response_model=PurchaseResponse)
async def purchase_product(
    product_id: int,
    purchase_details: PurchaseRequest,
    session: SessionDep,
    bg_tasks: BackgroundTasks,
    idempotency_key: IdempotencyKeyDep,
):
    purchase_cache = await get_purchase_cache(idempotency_key, purchase_details)
    if purchase_cache:
        return purchase_cache

    user_id = purchase_details.user_id
    purchase_service = PurchaseService(session)
    transaction, balance, inventory = await purchase_service.purchase_product(
        product_id, user_id, purchase_details.amount
    )

    bg_tasks.add_task(invalidate_inventory_cache, user_id)

    response = PurchaseResponse(
        transaction=transaction, balance=balance, inventory_item=inventory
    )

    bg_tasks.add_task(set_purchase_cache, idempotency_key, purchase_details, response)

    return response


@product_router.post("/{product_id}/use/", response_model=UseProductResponse)
async def use_product(
    product_id: int,
    inventory_data: UseProductRequest,
    session: SessionDep,
    bg_tasks: BackgroundTasks,
):
    user_id = inventory_data.user_id

    inventory_service = InventoryService(session)
    quantity = await inventory_service.use_product(
        product_id, user_id, inventory_data.amount
    )

    bg_tasks.add_task(invalidate_inventory_cache, user_id)

    return UseProductResponse(remaining_quantity=quantity)
