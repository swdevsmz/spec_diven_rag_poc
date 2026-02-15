from __future__ import annotations

from pydantic import BaseModel


class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    embedding: list[float]
