from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .api import documents, queries


_TAGS_METADATA = [
    {
        "name": "query",
        "description": "RAG（検索拡張生成）を使った質問応答エンドポイント。"
        "ドキュメントを検索して根拠に基づく回答を生成します。",
    },
    {
        "name": "documents",
        "description": "ドキュメントのアップロード・ベクトル化・一覧取得などを行うエンドポイント。",
    },
]

_DESCRIPTION = """
## RAG Chatbot API

**仕様駆動開発 × RAG (Retrieval-Augmented Generation)** の PoC バックエンドです。

### 主な機能

- **ドキュメント管理**: テキストファイルをアップロード・ベクトル化して知識ベースを構築
- **RAG 質問応答**: 知識ベースを検索し、Gemini で根拠付き回答を生成
- **非 RAG 比較**: RAG あり／なしの回答品質を比較・評価

### 利用フロー

1. `POST /api/v1/documents` でテキストファイルをアップロード
2. `POST /api/v1/documents/{document_id}/vectorize` でベクトル化
3. `POST /api/v1/query` で質問を送信
"""


def create_app() -> FastAPI:
    # FastAPIアプリ本体を生成
    app = FastAPI(
        title="RAG Chatbot API",
        description=_DESCRIPTION,
        version="0.1.0",
        openapi_tags=_TAGS_METADATA,
        contact={
            "name": "spec_driven_rag_poc",
            "url": "https://github.com/swdevsmz/spec_diven_rag_poc",
        },
        docs_url="/docs",
        redoc_url="/redoc",
    )

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
