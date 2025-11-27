from app.core.exceptions import InventoryAlreadyExistsError
from app.db.models import Transaction, Status
from app.repositories.utils import safe_add


class TransactionRepository:
    def __init__(self, session):
        self.session = session

    async def create_transaction(self, transaction_data: dict) -> Transaction:
        new_transaction = Transaction(**transaction_data)
        await safe_add(
            self.session,
            new_transaction,
            InventoryAlreadyExistsError,
            product_id=new_transaction.product_id)
        return new_transaction

    async def update_status(self, transaction: Transaction, new_status: Status) -> Transaction:
        transaction.status = new_status
        self.session.add(transaction)
        await self.session.flush()
        return transaction
