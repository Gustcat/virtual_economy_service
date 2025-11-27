from asyncio import current_task
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, async_scoped_session

from app.core.config import settings

engine = create_async_engine(settings.real_database_url, echo=settings.db_echo)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
)


def get_scoped_session():
    session = async_scoped_session(
        session_factory=async_session,
        scopefunc=current_task,
    )
    return session


async def get_async_session() -> AsyncSession:
    scoped_session = get_scoped_session()

    async with scoped_session() as session:
        yield session

    await scoped_session.remove()


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
