from pydantic import BaseModel, ConfigDict

from app.db.models import ProductType


class ProductShortSchema(BaseModel):
    id: int
    name: str
    type: ProductType

    model_config = ConfigDict(from_attributes=True)
