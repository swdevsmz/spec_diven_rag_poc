from __future__ import annotations

from pathlib import Path


def read_text_file(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")


def extract_text_from_file(file_path: str, file_type: str) -> str:
    if file_type == "txt":
        return read_text_file(file_path)

    raise ValueError(f"未対応のファイル形式です: {file_type}")


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size は正の整数である必要があります。")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap は 0 以上かつ chunk_size 未満である必要があります。")

    chunks: list[str] = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        if end == text_length:
            break
        start = end - overlap

    return chunks
