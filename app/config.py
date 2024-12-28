from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # app config
    title: str = "International Delivery Service"
    app_version: str = "0.1.0"
    api_version: int = Field(default=1)
    debug: bool = Field(default=True)

    mongodb_url: str = "mongodb://mongodb:27017"
    rabbitmq_url: str = "amqp://guest:guest@rabbitmq:5672/"
    db_host: str = "db"
    mysql_database: str = "delivery"
    mysql_user: str = "user"
    mysql_password: str = "password"
    # redis
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    secret_key: str = "your-secret-key"
    https_only: bool = False

    workers: int = 1
    model_config = SettingsConfigDict(
        env_file="../config/.env",
        case_sensitive=False,
    )


@lru_cache()
def get_settings():
    return Settings()
