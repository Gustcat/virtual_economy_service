from contextlib import asynccontextmanager

from fastapi import FastAPI
from typing import AsyncGenerator

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from app.core.config import settings
from app.db.session import engine

import logging
from logging.config import dictConfig
from pathlib import Path
from app.log_config import LOGGING_CONFIG


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    Path("logs").mkdir(parents=True, exist_ok=True)
    dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    logger.info("Launch application...")

    redis = aioredis.from_url(
        settings.redis_url, encoding="utf-8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

    logger.info("Stop application...")
    await engine.dispose()
