import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.inventory_cache import (
    invalidate_inventory_cache,
)
from app.core.exceptions import (
    PermanentProductUseError,
    ProductNotFoundError,
    UserNotFoundError,
    InsufficientProductQuantityError,
)
from app.db.models import ProductType
from app.repositories.inventory import InventoryRepository
from app.repositories.product import ProductRepository
from app.repositories.user import UserRepository
from app.schemas.inventory import InventorySchema

logger = logging.getLogger(__name__)


class InventoryService:
    def __init__(self, session: AsyncSession):
        self.inventory_repo = InventoryRepository(session)
        self.product_repo = ProductRepository(session)
        self.user_repo = UserRepository(session)
        self.session = session

    async def list_user_inventories(self, user_id: int) -> list[InventorySchema]:
        inventories = await self.inventory_repo.list_user_inventories(user_id)
        await self.session.commit()

        return [InventorySchema.model_validate(inventory) for inventory in inventories]

    async def use_product(self, product_id, user_id, amount: int) -> int:
        async with self.session.begin():
            user = await self.user_repo.get_user(user_id)
            if user is None:
                raise UserNotFoundError(user_id)

            product = await self.product_repo.get_product(product_id)
            if product is None:
                raise ProductNotFoundError(product_id)

            if product.type != ProductType.CONSUMABLE:
                raise PermanentProductUseError

            inventory = await self.inventory_repo.get_inventory(
                user_id, product_id, for_update=True
            )

            quantity = inventory.quantity
            logger.debug(f"{quantity=} vs {amount=}")
            if quantity < amount:
                raise InsufficientProductQuantityError(quantity, amount)
            elif quantity == amount:
                await self.inventory_repo.delete_inventory(inventory)
                return 0
            else:
                inventory = await self.inventory_repo.update_quantity_inventory(
                    inventory, inventory.quantity - amount
                )
            return inventory.quantity
