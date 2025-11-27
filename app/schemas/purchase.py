from annotated_types import Gt
from pydantic import BaseModel, ConfigDict
from typing_extensions import Annotated

from app.schemas.inventory import InventorySchema
from app.schemas.transaction import TransactionShortSchema


class PurchaseRequest(BaseModel):
    user_id: Annotated[int, Gt(0)]
    amount: Annotated[int, Gt(0)] = 1

    model_config = ConfigDict(extra="forbid")


class PurchaseResponse(BaseModel):
    transaction: TransactionShortSchema
    balance: int
    inventory_item: InventorySchema
