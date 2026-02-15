from __future__ import annotations

import httpx

from ..config import get_settings

CHAT_ENDPOINT = "https://models.inference.ai.azure.com/chat/completions"


def build_rag_prompt(question: str, context_chunks: list[str]) -> str:
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
    settings = get_settings()
    prompt = build_rag_prompt(question, context_chunks)
    headers = {
        "Authorization": f"Bearer {settings.github_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.generation_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(CHAT_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    return data["choices"][0]["message"]["content"]
