from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    """ベクトル検索の最小単位（ドキュメント分割後のチャンク）"""

    chunk_id: str = Field(..., description="チャンクの一意ID")
    document_id: str = Field(..., description="所属ドキュメントのID")
    content: str = Field(..., description="チャンクのテキスト内容")
    embedding: list[float] = Field(..., description="テキストの埋め込みベクトル")


class Document(BaseModel):
    """ドキュメント管理APIで扱うメタ情報"""

    document_id: str = Field(..., description="ドキュメントの一意ID")
    filename: str = Field(..., description="元のファイル名")
    file_type: Literal["txt", "pdf", "md"] = Field(..., description="ファイル種別")
    status: Literal["pending", "processed", "error"] = Field(
        ..., description="処理状態: pending=未処理, processed=ベクトル化済, error=エラー"
    )
    created_at: datetime = Field(..., description="アップロード日時 (UTC)")
    original_text: str | None = Field(None, description="ドキュメントの原文テキスト")
