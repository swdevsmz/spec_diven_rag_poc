from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Gemini APIキー（必須）
    gemini_api_key: str = ""

    # ChromaDB（ローカル永続）の設定
    chroma_host: str = "localhost"
    chroma_port: int = 8001
    chroma_persist_directory: str = "data/chromadb"

    # 使用モデル
    generation_model: str = "gemini-2.0-flash"
    embedding_model: str = "gemini-embedding-001"

    # アプリログ設定
    log_level: str = "INFO"

    # ルートの .env を読み込む
    model_config = SettingsConfigDict(
        env_prefix="",
        env_file=Path(__file__).resolve().parents[2] / ".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    # 設定オブジェクトをキャッシュして毎回の再生成を防ぐ
    return Settings()
