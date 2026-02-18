from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from ..config import get_settings
from ..models.document import Document
from ..services.embedding import get_embedding
from ..services.vectordb import get_vectordb_service
from ..utils.file_handlers import chunk_text, extract_text_from_file

router = APIRouter(prefix="/api/v1", tags=["documents"])

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"
INDEX_PATH = DOCUMENTS_DIR / "documents_index.json"
SUPPORTED_EXTENSIONS: dict[str, str] = {
    ".txt": "txt",
}


def _ensure_storage() -> None:
    # ドキュメント保存先とインデックスファイルを初期化
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    if not INDEX_PATH.exists():
        INDEX_PATH.write_text("{}", encoding="utf-8")


def _load_index() -> dict[str, dict]:
    # ドキュメント管理用インデックスを読み込む
    _ensure_storage()
    raw = INDEX_PATH.read_text(encoding="utf-8")
    if not raw.strip():
        return {}
    return json.loads(raw)


def _save_index(index_data: dict[str, dict]) -> None:
    # 見やすさ優先でJSONを整形保存
    INDEX_PATH.write_text(
        json.dumps(index_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _build_document_response(index_entry: dict) -> Document:
    # 内部インデックス形式をAPIレスポンス型へ変換
    return Document(
        document_id=index_entry["document_id"],
        filename=index_entry["filename"],
        file_type=index_entry["file_type"],
        status=index_entry["status"],
        created_at=index_entry["created_at"],
        original_text=index_entry.get("original_text"),
    )


@router.post(
    "/documents",
    response_model=Document,
    status_code=201,
    summary="ドキュメントをアップロード",
    description="テキストファイル (.txt) をアップロードして知識ベースに登録します。"
    "アップロード直後はステータスが `pending` となり、別途ベクトル化が必要です。",
    response_description="登録されたドキュメントのメタ情報",
)
async def upload_document(file: UploadFile = File(..., description="アップロードするテキストファイル (.txt)")) -> Document:
    # アップロードファイル名のバリデーション
    filename = Path(file.filename or "").name
    if not filename:
        raise HTTPException(status_code=400, detail="ファイル名が不正です。")

    # 受け付ける拡張子を制限
    ext = Path(filename).suffix.lower()
    file_type = SUPPORTED_EXTENSIONS.get(ext)
    if file_type is None:
        raise HTTPException(
            status_code=400,
            detail="未対応のファイル形式です。現在は .txt のみ対応しています。",
        )

    # テキストファイルをUTF-8として読み込む
    try:
        content = await file.read()
        text = content.decode("utf-8")
    except Exception as exc:
        raise HTTPException(
            status_code=400, detail="ファイルの読み込みに失敗しました。") from exc

    # 保存時は重複回避のため document_id をファイル名に利用
    document_id = str(uuid4())
    stored_filename = f"{document_id}{ext}"
    stored_path = DOCUMENTS_DIR / stored_filename

    try:
        # 本文保存 + インデックス更新
        _ensure_storage()
        stored_path.write_text(text, encoding="utf-8")

        index_data = _load_index()
        created_at = datetime.now(timezone.utc).isoformat()
        index_data[document_id] = {
            "document_id": document_id,
            "filename": filename,
            "file_type": file_type,
            "status": "pending",
            "created_at": created_at,
            "original_text": text,
            "stored_path": str(stored_path),
        }
        _save_index(index_data)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail="ドキュメントの保存に失敗しました。") from exc

    return _build_document_response(index_data[document_id])


@router.post(
    "/documents/{document_id}/vectorize",
    summary="ドキュメントをベクトル化",
    description="指定したドキュメントをチャンクに分割し、埋め込みモデルでベクトル化して"
    " ChromaDB に保存します。完了後はステータスが `processed` になります。",
    response_description="ベクトル化結果（チャンク数・モデル情報など）",
)
async def vectorize_document(
    document_id: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> dict:
    # チャンク設定の妥当性チェック
    if chunk_size <= 0 or chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise HTTPException(
            status_code=400, detail="chunk_size / chunk_overlap の指定が不正です。")

    # 対象ドキュメント存在確認
    index_data = _load_index()
    entry = index_data.get(document_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="指定されたドキュメントが見つかりません。")

    try:
        # 1) 抽出 2) 分割 3) 埋め込み 4) ベクトルDB保存
        text = extract_text_from_file(entry["stored_path"], entry["file_type"])
        chunks = chunk_text(text, chunk_size=chunk_size, overlap=chunk_overlap)

        embeddings: list[list[float]] = []
        for chunk in chunks:
            embeddings.append(await get_embedding(chunk, task_type="RETRIEVAL_DOCUMENT"))

        vectordb = get_vectordb_service()
        vectordb.add_document_chunks(document_id, chunks, embeddings)

        # 正常完了時はステータスを processed へ更新
        entry["status"] = "processed"
        entry["original_text"] = text
        index_data[document_id] = entry
        _save_index(index_data)
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        # 失敗時はステータスを error にして再試行可能にする
        entry["status"] = "error"
        index_data[document_id] = entry
        _save_index(index_data)
        raise HTTPException(
            status_code=500, detail="ドキュメントのベクトル化に失敗しました。") from exc

    embedding_dimension = len(embeddings[0]) if embeddings else 0
    settings = get_settings()

    return {
        "document_id": document_id,
        "chunks_created": len(chunks),
        "status": "processed",
        "embedding_model": settings.embedding_model,
        "embedding_dimension": embedding_dimension,
    }


@router.get(
    "/documents",
    summary="ドキュメント一覧を取得",
    description="登録済みドキュメントの一覧を返します。`status` でフィルタリング、`limit`/`offset` でページングができます。",
    response_description="ドキュメント一覧・件数・ページング情報",
)
async def list_documents(
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict:
    # ページング引数のバリデーション
    if limit < 1 or offset < 0:
        raise HTTPException(status_code=400, detail="limit / offset の指定が不正です。")

    # インデックスをレスポンス形式へ変換
    index_data = _load_index()
    documents = [
        _build_document_response(entry).model_dump(mode="json")
        for entry in index_data.values()
    ]

    if status is not None:
        # 必要に応じてステータスで絞り込み
        documents = [doc for doc in documents if doc["status"] == status]

    try:
        # VectorDB上の実チャンク数を付与
        vectordb = get_vectordb_service()
        vectordb_documents = vectordb.list_documents()
        chunk_counts = {
            item["document_id"]: item["chunk_count"]
            for item in vectordb_documents
            if item.get("document_id")
        }

        for doc in documents:
            doc["chunk_count"] = chunk_counts.get(doc["document_id"], 0)
    except Exception:
        # 集計失敗時は一覧取得を優先し chunk_count=0 を返す
        for doc in documents:
            doc["chunk_count"] = 0

    total = len(documents)
    paginated = documents[offset: offset + limit]

    return {
        "documents": paginated,
        "total": total,
        "limit": limit,
        "offset": offset,
    }
