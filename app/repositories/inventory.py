from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.core.exceptions import InventoryAlreadyExistsError
from app.db.models import Inventory
from app.repositories.utils import safe_add


class InventoryRepository:
    def __init__(self, session):
        self.session = session

    async def get_inventory(self, user_id: int, product_id: int, for_update: bool = False) -> Inventory | None:
        stmt = select(Inventory).where(
            Inventory.user_id == user_id,
            Inventory.product_id == product_id
        )
        if for_update:
            stmt = stmt.with_for_update()
        inventory = (await self.session.execute(stmt)).scalar_one_or_none()
        return inventory

    async def create_inventory(self, inventory_dict: dict) -> Inventory:
        inventory = Inventory(**inventory_dict)
        await safe_add(
            self.session,
            inventory,
            InventoryAlreadyExistsError,
            product_id=inventory.product_id)
        return inventory

    async def list_user_inventories(self, user_id: int) -> list[Inventory]:
        stmt = select(Inventory).where(Inventory.user_id == user_id).options(joinedload(Inventory.product))
        result = await self.session.execute(stmt)
        inventories = result.scalars().all()
        return list(inventories)

    async def delete_inventory(self, inventory: Inventory):
        await self.session.delete(inventory)
        await self.session.flush()

    async def update_quantity_inventory(self, inventory: Inventory, new_quantity: int) -> Inventory:
        inventory.quantity = new_quantity
        self.session.add(inventory)
        await self.session.flush()
        return inventory
