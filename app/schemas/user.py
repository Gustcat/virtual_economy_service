from typing import Annotated

from annotated_types import Gt, Le
from pydantic import BaseModel, ConfigDict


class AddFundsRequest(BaseModel):
    amount: Annotated[int, Gt(0), Le(1_000_000)]

    model_config = ConfigDict(extra="forbid")


class AddFundsResponse(BaseModel):
    balance: int
