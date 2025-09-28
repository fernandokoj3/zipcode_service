from __future__ import annotations

from enum import Enum
from typing import Final, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_URL = ""
VERSION_1: Final[str] = f"{BASE_URL}/v1"
VERSION_2: Final[str] = f"{BASE_URL}/v2"

DEFAULT_ISSUER: Final[str] = "dock"
# DEFAULT_VIACEP_BASE_URL: Final[str] = "https://viacep.com.br"
DEFAULT_VIACEP_BASE_URL: Final[str] = "http://local"


class Environment(Enum):
    DEVELOPMENT = "DEVELOPMENT"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"
    TEST = "TEST"


class RedisConfig(BaseModel):
    host: str
    port: int
    db: int
    password: str


class _Settings(BaseSettings):
    version: str
    base_url_v1: str = Field(VERSION_1)
    base_url_v2: str = Field(VERSION_2)
    redis: Optional[RedisConfig] = Field(None)

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )

    def is_env_test(self) -> bool:
        return self.env == Environment.TEST


load_dotenv()
settings = _Settings()
