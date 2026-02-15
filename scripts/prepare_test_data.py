from __future__ import annotations

import asyncio
from pathlib import Path
from uuid import uuid4

from backend.app.services.embedding import get_embedding
from backend.app.services.vectordb import get_vectordb_service
from backend.app.utils.file_handlers import chunk_text, read_text_file


def _collect_documents(documents_dir: Path) -> list[Path]:
    return [path for path in documents_dir.glob("*.txt") if path.is_file()]


async def _ingest_document(document_path: Path) -> None:
    document_id = str(uuid4())
    text = read_text_file(str(document_path))
    chunks = chunk_text(text)

    vectordb = get_vectordb_service()
    collection = vectordb.get_collection()

    for index, chunk in enumerate(chunks):
        embedding = await get_embedding(chunk)
        chunk_id = str(uuid4())
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[chunk_id],
            metadatas=[
                {
                    "document_id": document_id,
                    "document_filename": document_path.name,
                    "chunk_index": index,
                }
            ],
        )


async def main() -> None:
    documents_dir = Path("data/documents")
    if not documents_dir.exists():
        raise RuntimeError("data/documents が存在しません。")

    documents = _collect_documents(documents_dir)
    if not documents:
        raise RuntimeError("data/documents に .txt ドキュメントがありません。")

    for document_path in documents:
        await _ingest_document(document_path)


if __name__ == "__main__":
    asyncio.run(main())
