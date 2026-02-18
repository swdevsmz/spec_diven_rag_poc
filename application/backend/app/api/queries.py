from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from ..config import get_settings
from ..models.query import (
    GenerationParameters,
    QueryRequest,
    QueryResponse,
    RetrievedChunk,
)
from ..services.embedding import get_embedding
from ..services.generation import generate_answer
from ..services.vectordb import get_vectordb_service

router = APIRouter(prefix="/api/v1", tags=["query"])


@router.post("/query", response_model=QueryResponse)
async def query_rag(payload: QueryRequest) -> QueryResponse:
    # 1リクエストごとに一意IDを付与
    settings = get_settings()
    query_id = str(uuid4())

    try:
        # 1) 質問を埋め込み化して 2) 類似チャンク検索
        query_embedding = await get_embedding(payload.question, task_type="RETRIEVAL_QUERY")
        vectordb = get_vectordb_service()
        chunks = vectordb.query_similar_chunks(query_embedding, payload.top_k)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="ベクトル検索に失敗しました。") from exc

    parameters = GenerationParameters(
        temperature=payload.temperature,
        max_tokens=payload.max_tokens,
        top_k=payload.top_k,
    )

    if not chunks:
        # ヒットなし時は明示メッセージで返却
        return QueryResponse(
            query_id=query_id,
            question=payload.question,
            answer="関連ドキュメントが見つかりませんでした。",
            retrieved_chunks=[],
            model=settings.generation_model,
            parameters=parameters,
            timestamp=datetime.now(timezone.utc),
        )

    try:
        # 検索結果を根拠に回答生成
        answer = await generate_answer(
            payload.question,
            [chunk["content"] for chunk in chunks],
            payload.temperature,
            payload.max_tokens,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail="回答生成に失敗しました。") from exc

    # APIレスポンス形式へ整形
    retrieved_chunks = [
        RetrievedChunk(
            chunk_id=chunk["chunk_id"],
            document_id=chunk.get("document_id"),
            content=chunk["content"],
            similarity_score=chunk["score"],
        )
        for chunk in chunks
    ]

    return QueryResponse(
        query_id=query_id,
        question=payload.question,
        answer=answer,
        retrieved_chunks=retrieved_chunks,
        model=settings.generation_model,
        parameters=parameters,
        timestamp=datetime.now(timezone.utc),
    )
