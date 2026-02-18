from __future__ import annotations
from app.utils.file_handlers import chunk_text, read_text_file
from app.services.vectordb import get_vectordb_service
from app.services.embedding import get_embedding

import asyncio
from pathlib import Path
import sys
from uuid import uuid4

PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def _collect_documents(documents_dir: Path) -> list[Path]:
    return [path for path in documents_dir.glob("*.txt") if path.is_file()]


async def _ingest_document(document_path: Path) -> None:
    document_id = str(uuid4())
    text = read_text_file(str(document_path))
    chunks = chunk_text(text)

    vectordb = get_vectordb_service()
    collection = vectordb.get_collection()

    for index, chunk in enumerate(chunks):
        embedding = await get_embedding(chunk, task_type="RETRIEVAL_DOCUMENT")
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
    documents_dir = PROJECT_ROOT / "application" / "data" / "documents"
    if not documents_dir.exists():
        raise RuntimeError("application/data/documents が存在しません。")

    documents = _collect_documents(documents_dir)
    if not documents:
        raise RuntimeError("application/data/documents に .txt ドキュメントがありません。")

    for document_path in documents:
        await _ingest_document(document_path)


if __name__ == "__main__":
    asyncio.run(main())
