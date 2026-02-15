from __future__ import annotations

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


def get_vectordb_service() -> VectorDBService:
    settings = get_settings()
    return VectorDBService(settings.chroma_host, settings.chroma_port)
