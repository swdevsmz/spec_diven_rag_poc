from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    github_token: str
    chroma_host: str = "localhost"
    chroma_port: int = 8001
    generation_model: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-small"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_prefix="",
        env_file=Path(__file__).resolve().parents[2] / ".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
