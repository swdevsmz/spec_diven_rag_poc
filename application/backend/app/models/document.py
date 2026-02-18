from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class DocumentChunk(BaseModel):
    # ベクトル検索の最小単位（ドキュメント分割後のチャンク）
    chunk_id: str
    document_id: str
    content: str
    embedding: list[float]


class Document(BaseModel):
    # ドキュメント管理APIで扱うメタ情報
    document_id: str
    filename: str
    file_type: Literal["txt", "pdf", "md"]
    status: Literal["pending", "processed", "error"]
    created_at: datetime
    original_text: str | None = None
