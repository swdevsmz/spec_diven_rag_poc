from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    # ユーザーからの質問入力
    question: str = Field(..., min_length=1)

    # 検索・生成パラメータ
    top_k: int = Field(5, ge=1, le=20)
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(500, ge=1)


class GenerationParameters(BaseModel):
    # 実行時に使用した生成パラメータ
    temperature: float
    max_tokens: int
    top_k: int


class RetrievedChunk(BaseModel):
    # 回答に利用した検索チャンク
    chunk_id: str
    document_id: str | None
    content: str
    similarity_score: float


class QueryResponse(BaseModel):
    # 質問応答APIの返却形式
    query_id: str
    question: str
    answer: str
    retrieved_chunks: list[RetrievedChunk]
    model: str
    parameters: GenerationParameters
    timestamp: datetime
