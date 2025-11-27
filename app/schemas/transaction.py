from pydantic import BaseModel, ConfigDict

from app.db.models import Status


class TransactionShortSchema(BaseModel):
    id: int
    status: Status

    model_config = ConfigDict(from_attributes=True)
