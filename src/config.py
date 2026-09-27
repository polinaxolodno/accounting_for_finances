from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any
from pydantic import PostgresDsn, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging.config


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra='ignore',
        env_file='.env'
    )
    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'master'
    POSTGRES_DB: str = "postgres"

    POSTGRES_DB_ECHO: bool = False

    SQLALCHEMY_DATABASE_URI: str | None = None
    SQLALCHEMY_DATABASE_URI_ASYNC: str | None = None

    @field_validator('SQLALCHEMY_DATABASE_URI', mode='before')
    @classmethod
    def assemble_db_connection(cls, v: str | None, info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        return str(PostgresDsn.build(
            scheme='postgresql+psycopg',
            username=info.data.get('POSTGRES_USER'),
            password=info.data.get('POSTGRES_PASSWORD'),
            host=info.data.get('POSTGRES_SERVER'),
            port=info.data.get('POSTGRES_PORT'),
            path=info.data.get('POSTGRES_DB') or '',
        ))

    @field_validator('SQLALCHEMY_DATABASE_URI_ASYNC', mode='before')
    @classmethod
    def assemble_async_db_connection(cls, v: str | None, info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        return info.data.get('SQLALCHEMY_DATABASE_URI')


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file =".env"
    )
    BASE_ROUTE_PATH: str = "/api/v1"
    DB: DBSettings = DBSettings()

    SECRET_KEY: str = 'iseuybcdfgvloiszdflujabw'

    LOG_LEVEL: str = "DEBUG"

settings = Settings()



LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {"default": {"format": "%(asctime)s [%(process)s] %(levelname)s: %(message)s"}},
    "handlers": {
        "console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": settings.LOG_LEVEL,
        }
    },
    "root": {"handlers": ["console"], "level": settings.LOG_LEVEL},
    "loggers": {
        "gunicorn": {"propagate": True},
        "gunicorn.access": {"propagate": True},
        "gunicorn.error": {"propagate": True},
        "uvicorn": {"propagate": True},
        "uvicorn.access": {"propagate": True},
        "uvicorn.error": {"propagate": True},
    },
}

logging.config.dictConfig(LOG_CONFIG)