from pydantic import BaseModel

from app.db.models import ProductType


class PopularProductSchema(BaseModel):
    id: int
    name: str
    description: str | None = None
    type: ProductType
    purchase_count: int
