from typing import Type, Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppError
from app.db.base import Base

UNIQUENESS_VIOLATION_PGCODE = "23505"


async def safe_add(
    session: AsyncSession,
    obj: Base,
    error_cls: Type[AppError] | None = None,
    **kwargs: Any,
) -> None:
    session.add(obj)
    try:
        await session.flush()
    except IntegrityError as e:
        await session.rollback()
        if error_cls and getattr(e.orig, "pgcode", None) == UNIQUENESS_VIOLATION_PGCODE:
            raise error_cls(**kwargs)
        raise