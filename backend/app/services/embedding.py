from __future__ import annotations

import httpx

from ..config import get_settings

EMBEDDING_ENDPOINT = "https://models.inference.ai.azure.com/embeddings"


async def get_embedding(text: str) -> list[float]:
    settings = get_settings()
    headers = {
        "Authorization": f"Bearer {settings.github_token}",
        "Content-Type": "application/json",
    }
    payload = {"input": text, "model": settings.embedding_model}

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(EMBEDDING_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    return data["data"][0]["embedding"]
