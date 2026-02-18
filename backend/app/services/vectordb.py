from __future__ import annotations

from collections import defaultdict
from uuid import uuid4

import chromadb

from ..config import get_settings

COLLECTION_NAME = "rag_documents"


class VectorDBService:
    def __init__(self, host: str, port: int, collection_name: str = COLLECTION_NAME) -> None:
        self._client = chromadb.HttpClient(host=host, port=port)
        self._collection_name = collection_name

    def get_collection(self):
        return self._client.get_or_create_collection(name=self._collection_name)

    def query_similar_chunks(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        collection = self.get_collection()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances", "ids"],
        )

        if not results.get("ids"):
            return []

        items: list[dict] = []
        ids = results["ids"][0]
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for index, chunk_id in enumerate(ids):
            metadata = metadatas[index] if index < len(metadatas) else {}
            distance = distances[index] if index < len(distances) else None
            score = 1.0 - distance if distance is not None else 0.0
            items.append(
                {
                    "chunk_id": chunk_id,
                    "document_id": metadata.get("document_id") if metadata else None,
                    "content": documents[index] if index < len(documents) else "",
                    "score": score,
                }
            )

        return items

    def add_document_chunks(
        self,
        document_id: str,
        chunks: list[str],
        embeddings: list[list[float]],
    ) -> list[str]:
        if len(chunks) != len(embeddings):
            raise ValueError("chunks と embeddings の件数が一致しません。")
        if not chunks:
            return []

        collection = self.get_collection()
        chunk_ids = [str(uuid4()) for _ in chunks]
        metadatas = [
            {
                "document_id": document_id,
                "chunk_index": index,
            }
            for index in range(len(chunks))
        ]

        collection.add(
            ids=chunk_ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        return chunk_ids

    def list_documents(self) -> list[dict]:
        collection = self.get_collection()
        results = collection.get(include=["metadatas"])
        metadatas = results.get("metadatas", [])

        grouped: dict[str, dict] = defaultdict(
            lambda: {"document_id": "", "chunk_count": 0})
        for metadata in metadatas:
            if not metadata:
                continue
            document_id = metadata.get("document_id")
            if not document_id:
                continue

            if not grouped[document_id]["document_id"]:
                grouped[document_id]["document_id"] = document_id
            grouped[document_id]["chunk_count"] += 1

        return list(grouped.values())


def get_vectordb_service() -> VectorDBService:
    settings = get_settings()
    return VectorDBService(settings.chroma_host, settings.chroma_port)
