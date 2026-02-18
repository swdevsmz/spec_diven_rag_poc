from __future__ import annotations

import httpx
from urllib.parse import urlencode

from ..config import get_settings

# Gemini API のモデルエンドポイントベースURL
GEMINI_BASE_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models"


async def get_embedding(text: str, task_type: str | None = None) -> list[float]:
    # 設定からモデル名とAPIキーを取得
    settings = get_settings()
    endpoint = f"{GEMINI_BASE_ENDPOINT}/{settings.embedding_model}:embedContent"
    query = urlencode({"key": settings.gemini_api_key})

    # Gemini embedContent の入力フォーマット
    payload: dict = {
        "content": {"parts": [{"text": text}]},
    }
    # 検索用途に合わせて埋め込み最適化を切り替え（例: RETRIEVAL_QUERY / RETRIEVAL_DOCUMENT）
    if task_type:
        payload["taskType"] = task_type

    async with httpx.AsyncClient(timeout=30.0) as client:
        # REST API で埋め込みを取得
        response = await client.post(
            f"{endpoint}?{query}",
            headers={"Content-Type": "application/json"},
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    # 返却形式: {"embedding": {"values": [...]}}
    return data["embedding"]["values"]
