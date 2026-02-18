from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .api import documents, queries


def create_app() -> FastAPI:
    # FastAPIアプリ本体を生成
    app = FastAPI(title="RAG Chatbot API")

    # ローカル検証を優先し、CORSは広めに許可
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def validate_environment() -> None:
        # 必須環境変数が未設定のまま起動しないようにチェック
        settings = get_settings()
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY が設定されていません。.env を確認してください。")

        # 起動時にログレベルを反映
        logging.basicConfig(level=settings.log_level)

    # APIルーターを登録
    app.include_router(queries.router)
    app.include_router(documents.router)

    return app


app = create_app()
