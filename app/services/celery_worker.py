from app.core.celery_app import app
from app.core.config import settings
import logging

from redis import Redis

logger = logging.getLogger(__name__)


@app.task(name="app.services.celery_worker.clear_cache")
def clear_cache():
    logger.info("Clearing Redis cache...")
    r = Redis.from_url(
        f"redis://{settings.redis_user}:{settings.redis_password}@redis:{settings.redis_port}/0",
        decode_responses=True,
    )
    r.flushdb()
