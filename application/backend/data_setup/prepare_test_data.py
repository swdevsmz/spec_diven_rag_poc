from __future__ import annotations

import asyncio
from pathlib import Path
import sys
from uuid import uuid4

PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.utils.file_handlers import chunk_text, read_text_file
from app.services.vectordb import get_vectordb_service
from app.services.embedding import get_embedding


def _collect_documents(documents_dir: Path) -> list[Path]:
    return [path for path in documents_dir.glob("*.txt") if path.is_file()]


def _ensure_test_documents(documents_dir: Path) -> list[Path]:
    documents_dir.mkdir(parents=True, exist_ok=True)
    documents = _collect_documents(documents_dir)
    if documents:
        return documents

    seed_documents: dict[str, str] = {
        "sample_devcontainer.txt": (
            "DevContainer は開発環境をコードとして管理し、チーム全員の実行環境を揃えます。\n"
            "本プロジェクトでは Python と uv を利用して依存関係を管理します。"
        ),
        "sample_rag.txt": (
            "RAG は検索で取得した文脈を生成モデルへ渡すことで、回答の根拠を強化します。\n"
            "ベクター検索には ChromaDB を使用し、ローカル永続化します。"
        ),
    }

    for filename, content in seed_documents.items():
        (documents_dir / filename).write_text(content, encoding="utf-8")

    return _collect_documents(documents_dir)


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
    documents_dir = PROJECT_ROOT / "data" / "documents"
    documents = _ensure_test_documents(documents_dir)
    if not documents:
        raise RuntimeError("data/documents にテスト用 .txt ドキュメントを準備できませんでした。")

    for document_path in documents:
        await _ingest_document(document_path)


if __name__ == "__main__":
    asyncio.run(main())
