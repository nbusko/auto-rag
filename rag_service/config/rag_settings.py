from pydantic import Field, AnyUrl
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    OPENAI_BASE_URL: Optional[AnyUrl] = Field(
        default="https://api.proxyapi.ru/openai/v1", env="OPENAI_BASE_URL"
    )
    EMBEDDER_MODEL: Optional[str] = Field(
        default="sergeyzh/rubert-mini-frida", env="EMBEDDER_MODEL"
    )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="allow"
    )
