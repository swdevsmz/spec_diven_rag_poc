from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    embedding: list[float]


class Document(BaseModel):
    document_id: str
    filename: str
    file_type: Literal["txt", "pdf", "md"]
    status: Literal["pending", "processed", "error"]
    created_at: datetime
    original_text: str | None = None
