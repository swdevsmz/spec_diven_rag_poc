from __future__ import annotations

import httpx

from ..config import get_settings

# Gemini API のモデルエンドポイントベースURL
GEMINI_BASE_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models"


async def get_embedding(text: str, task_type: str | None = None) -> list[float]:
    # 設定からモデル名とAPIキーを取得
    settings = get_settings()
    endpoint = f"{GEMINI_BASE_ENDPOINT}/{settings.embedding_model}:embedContent"

    # Gemini embedContent の入力フォーマット
    payload: dict = {
        "content": {"parts": [{"text": text}]},
    }
    # 検索用途に合わせて埋め込み最適化を切り替え（例: RETRIEVAL_QUERY / RETRIEVAL_DOCUMENT）
    if task_type:
        payload["taskType"] = task_type

    async with httpx.AsyncClient(timeout=30.0) as client:
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": settings.gemini_api_key,
        }
        response = await client.post(endpoint, headers=headers, json=payload)

        # taskType 非対応モデル向けフォールバック
        if response.status_code == 400 and task_type:
            fallback_payload = {
                "content": {"parts": [{"text": text}]},
            }
            response = await client.post(endpoint, headers=headers, json=fallback_payload)

        if response.status_code >= 400:
            raise RuntimeError(f"Embedding API error: status={response.status_code}, body={response.text}")

        data = response.json()

    # 返却形式: {"embedding": {"values": [...]}}
    return data["embedding"]["values"]
