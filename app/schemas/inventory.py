from datetime import datetime
from typing import Annotated

from annotated_types import Gt
from pydantic import BaseModel, ConfigDict

from app.schemas.product import ProductShortSchema


class InventorySchema(BaseModel):
    product: ProductShortSchema
    quantity: int
    purchased_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UseProductRequest(BaseModel):
    user_id: Annotated[int, Gt(0)]
    amount: Annotated[int, Gt(0)] = 1

    model_config = ConfigDict(extra="forbid")


class UseProductResponse(BaseModel):
    remaining_quantity: int
