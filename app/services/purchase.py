import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    InsufficientBalanceError,
    ProductInactiveError,
    InventoryAlreadyExistsError,
    PermanentProductQuantityError,
    ProductNotFoundError,
    UserNotFoundError,
    AppError,
)
from app.db.models import ProductType, Status
from app.repositories.inventory import InventoryRepository
from app.repositories.product import ProductRepository
from app.repositories.transaction import TransactionRepository
from app.repositories.user import UserRepository
from app.schemas.inventory import InventorySchema
from app.schemas.transaction import TransactionShortSchema


logger = logging.getLogger(__name__)


class PurchaseService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)
        self.transaction_repo = TransactionRepository(session)
        self.inventory_repo = InventoryRepository(session)
        self.product_repo = ProductRepository(session)
        self.session = session

    async def purchase_product(
        self, product_id: int, user_id: int, amount: int
    ) -> tuple[TransactionShortSchema, int, InventorySchema]:
        transaction_dict = {
            "user_id": user_id,
            "product_id": product_id,
            "amount": amount,
            "status": Status.PENDING,
        }

        async with self.session.begin():
            product = await self.product_repo.get_product(product_id)
            if product is None:
                raise ProductNotFoundError(product_id)
            if not product.is_active:
                raise ProductInactiveError(product_id)
            product_type = product.type
            if product_type == ProductType.PERMANENT and amount > 1:
                raise PermanentProductQuantityError

            user = await self.user_repo.get_user(user_id, for_update=True)
            if user is None:
                raise UserNotFoundError(user_id)

            transaction = await self.transaction_repo.create_transaction(
                transaction_dict
            )
            await self.session.flush()

            try:
                total_cost = product.price * amount
                if user.balance - total_cost < 0:
                    raise InsufficientBalanceError(user.balance, total_cost)

                inventory = await self.inventory_repo.get_inventory(
                    user_id, product_id, for_update=True
                )
                if inventory:
                    if product_type == ProductType.PERMANENT:
                        raise InventoryAlreadyExistsError(product_id)
                    inventory = await self.inventory_repo.update_quantity_inventory(
                        inventory, inventory.quantity + amount
                    )
                else:
                    inventory = await self.inventory_repo.create_inventory(
                        {
                            "user_id": user_id,
                            "product_id": product_id,
                            "quantity": amount,
                        }
                    )

                user = await self.user_repo.change_balance(
                    user, user.balance - total_cost
                )

                transaction = await self.transaction_repo.update_status(
                    transaction, Status.COMPLETED
                )
            except Exception as e:
                if not isinstance(e, AppError):
                    logger.error(
                        f"Unexpected error during purchase transaction {transaction.id}: {e}"
                    )
                await self.transaction_repo.update_status(transaction, Status.FAILED)
                await self.session.commit()
                raise

        return (
            TransactionShortSchema.model_validate(transaction),
            user.balance,
            InventorySchema.model_validate(inventory),
        )
