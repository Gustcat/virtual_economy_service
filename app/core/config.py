from pathlib import Path
from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR.parent.parent / ".env"


class Settings(BaseSettings):
    db_user: Annotated[str, Field(alias="POSTGRES_USER")] = "user"
    db_pass: Annotated[str, Field(alias="POSTGRES_PASSWORD")] = "password"
    db_port: Annotated[str, Field(alias="POSTGRES_PORT")] = "5432"
    db_name: Annotated[str, Field(alias="POSTGRES_DB")] = "virtual_shop"
    db_echo: Annotated[bool, Field(alias="DB_ECHO")] = False
    db_host: Annotated[str, Field(alias="POSTGRES_HOST")] = "localhost"

    http_host: Annotated[str, Field(alias="HTTP_HOST")] = "localhost"
    http_port: Annotated[int, Field(alias="HTTP_PORT")] = 8080

    redis_host: Annotated[str, Field(alias="REDIS_HOST")] = "localhost"
    redis_port: Annotated[str, Field(alias="REDIS_PORT")] = "6379"
    redis_user: Annotated[str, Field(alias="REDIS_USER")] = "default"
    redis_password: Annotated[str, Field(alias="REDIS_PASSWORD")] = ""
    redis_cache_db: Annotated[int, Field(alias="REDIS_CACHE_DB")] = 0
    redis_celery_db: Annotated[int, Field(alias="REDIS_CELERY_DB")] = 1

    inventory_ttl: Annotated[int, Field(alias="INVENTORY_TTL")] = 300
    product_top_ttl: Annotated[int, Field(alias="PRODUCT_TTL")] = 86400
    balance_ttl: Annotated[int, Field(alias="BALANCE_TTL")] = 3600
    transaction_ttl: Annotated[int, Field(alias="TRANSACTION_TTL")] = 3600

    days_for_product_top: Annotated[int, Field(alias="DAYS_FOR_PRODUCT_TOP")] = 7
    amount_products_top: Annotated[int, Field(alias="AMOUNT_PRODUCTS_TOP")] = 5

    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def real_database_url(self):
        return f"postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

    @property
    def redis_url(self):
        return (
            f"redis://{settings.redis_user}:{settings.redis_password}@{settings.redis_host}:"
            f"{settings.redis_port}"
        )

    @property
    def redis_celery_url(self):
        return settings.redis_url + f"/{settings.redis_celery_db}"


settings = Settings()
