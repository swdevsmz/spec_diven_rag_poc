from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """質問応答リクエスト"""

    question: str = Field(..., min_length=1, description="ユーザーの質問文")
    top_k: int = Field(5, ge=1, le=20, description="ベクトル検索で取得する上位チャンク数 (1〜20)")
    temperature: float = Field(
        0.7, ge=0.0, le=2.0, description="生成時のランダム性 (0.0=決定的, 2.0=最大)"
    )
    max_tokens: int = Field(500, ge=1, description="生成する最大トークン数")


class GenerationParameters(BaseModel):
    """実行時に使用した生成パラメータ"""

    temperature: float = Field(..., description="生成時のランダム性")
    max_tokens: int = Field(..., description="最大生成トークン数")
    top_k: int = Field(..., description="検索上位チャンク数")


class RetrievedChunk(BaseModel):
    """回答生成に利用した検索チャンク"""

    chunk_id: str = Field(..., description="チャンクの一意ID")
    document_id: str | None = Field(None, description="所属ドキュメントのID")
    content: str = Field(..., description="チャンクのテキスト内容")
    similarity_score: float = Field(..., description="質問との類似スコア (0.0〜1.0)")


class QueryResponse(BaseModel):
    """質問応答APIのレスポンス"""

    query_id: str = Field(..., description="リクエストの一意ID")
    question: str = Field(..., description="入力された質問文")
    answer: str = Field(..., description="RAGが生成した回答")
    retrieved_chunks: list[RetrievedChunk] = Field(
        ..., description="回答根拠として使用したチャンク一覧"
    )
    model: str = Field(..., description="使用した生成モデル名")
    parameters: GenerationParameters = Field(..., description="実行時パラメータ")
    timestamp: datetime = Field(..., description="レスポンス生成日時 (UTC)")
