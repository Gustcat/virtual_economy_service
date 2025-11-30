from celery import Celery
from celery.schedules import crontab
from celery.signals import after_setup_logger
from app.core.config import settings


app = Celery(
    "worker",
    broker=settings.redis_url,
    backend=settings.redis_celery_url,
    imports=["app.services.celery_worker"],
)
app.autodiscover_tasks()

app.conf.update(
    timezone="UTC",
    enable_utc=True,
    worker_hijack_root_logger=False,
)


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    """Configure Celery logger to use the same configuration as the main application."""
    from logging.config import dictConfig
    from pathlib import Path
    from app.log_config import LOGGING_CONFIG

    Path("logs").mkdir(parents=True, exist_ok=True)
    dictConfig(LOGGING_CONFIG)


app.conf.beat_schedule = {
    "clear-cache-every-day": {
        "task": "app.services.celery_worker.clear_cache",
        "schedule": crontab(hour="0", minute="0"),
    },
}
