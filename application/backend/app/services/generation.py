from __future__ import annotations

import httpx
from urllib.parse import urlencode

from ..config import get_settings

# Gemini API のモデルエンドポイントベースURL
GEMINI_BASE_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models"


def build_rag_prompt(question: str, context_chunks: list[str]) -> str:
    # 取得チャンクをまとめて、回答用の日本語プロンプトを組み立てる
    context = "\n\n".join(context_chunks)
    return (
        "以下のドキュメントに基づいて質問に答えてください。\n\n"
        "【ドキュメント】\n"
        f"{context}\n\n"
        "【質問】\n"
        f"{question}\n\n"
        "【回答】"
    )


async def generate_answer(
    question: str,
    context_chunks: list[str],
    temperature: float = 0.3,
    max_tokens: int = 1000,
) -> str:
    # 設定とプロンプトを準備
    settings = get_settings()
    prompt = build_rag_prompt(question, context_chunks)
    endpoint = f"{GEMINI_BASE_ENDPOINT}/{settings.generation_model}:generateContent"
    query = urlencode({"key": settings.gemini_api_key})

    # Gemini generateContent の入力形式
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
        },
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        # REST API で回答生成
        response = await client.post(
            f"{endpoint}?{query}",
            headers={"Content-Type": "application/json"},
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    # 候補がない場合は上位でエラーとして扱う
    candidates = data.get("candidates", [])
    if not candidates:
        raise RuntimeError("Gemini から回答候補が返されませんでした。")

    # 先頭候補のテキストパートを連結して返却
    parts = candidates[0].get("content", {}).get("parts", [])
    texts = [part.get("text", "") for part in parts if part.get("text")]
    if not texts:
        raise RuntimeError("Gemini からテキスト回答が取得できませんでした。")

    return "\n".join(texts)
