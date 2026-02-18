from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .api import documents, queries


def create_app() -> FastAPI:
    app = FastAPI(title="RAG Chatbot API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def validate_environment() -> None:
        settings = get_settings()
        if not settings.github_token:
            raise RuntimeError("GITHUB_TOKEN が設定されていません。.env を確認してください。")

        logging.basicConfig(level=settings.log_level)

    app.include_router(queries.router)
    app.include_router(documents.router)

    return app


app = create_app()
