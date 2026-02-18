# Research: RAGチャットボット技術選定

**Date**: 2026-02-15 (更新)  
**Purpose**: Technical Context の技術選定を行い、GitHub Copilot Pro 契約下での実装方針を明確化する

## 1. 埋め込みモデル (Embedding Model)

### Decision
**GitHub Models の text-embedding-3-small** を採用

### Rationale
- **日本語対応**: OpenAI 互換のモデルで、多言語対応と日本語の品質が高い
- **次元数**: 1536 次元（標準）でコストと精度のバランスが良い
- **認証**: GitHub トークン（GITHUB_TOKEN）のみで利用可能、OpenAI API キー不要
- **契約適合**: GitHub Copilot Pro 契約で追加コストなく利用可能
- **ChromaDB 互換性**: OpenAI 形式の埋め込みは ChromaDB で標準的にサポートされている
- **MVP 適合**: API ベースで素早く実装可能、教育・検証目的に最適

### Alternatives Considered

| 代替案 | メリット | デメリット | 却下理由 |
|--------|---------|-----------|---------|
| **OpenAI API 直接** | 公式、豊富なドキュメント | API キー別途契約必要、追加コスト | GitHub Copilot Pro のみ契約のため利用不可 |
| **multilingual-e5-large** | ローカル実行可能、コスト不要 | GPU 必要、DevContainer での動作検証が必要 | MVP フェーズではセットアップ複雑性が高い |
| **sentence-transformers (日本語)** | オープンソース、柔軟性高い | 日本語モデルの選定・評価が必要 | 選定に時間がかかり MVP に不適 |

### Parameters
- **Model**: `text-embedding-3-small`
- **Dimensions**: 1536 (デフォルト)
- **API Endpoint**: `https://models.inference.ai.azure.com/embeddings`
- **認証**: 環境変数 `GITHUB_TOKEN` で管理

### Implementation Pattern
```python
import httpx
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
EMBEDDING_ENDPOINT = "https://models.inference.ai.azure.com/embeddings"

async def get_embedding(text: str) -> list[float]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            EMBEDDING_ENDPOINT,
            headers={
                "Authorization": f"Bearer {GITHUB_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "input": text,
                "model": "text-embedding-3-small"
            }
        )
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]
```

---

## 2. 生成モデル (LLM)

### Decision
**GitHub Models の GPT-4o** を採用

### Rationale
- **日本語品質**: GPT-4 シリーズは日本語の生成品質が高く、教育検証に適している
- **コンテキスト長**: 128k tokens で、複数ドキュメントを含むプロンプトに対応可能
- **認証統一**: 埋め込みモデルと同じ GITHUB_TOKEN で利用可能
- **契約適合**: GitHub Copilot Pro 契約で追加コストなく利用可能
- **Non-RAG 比較**: 同じモデルで RAG/Non-RAG を比較することで、検索の効果を純粋に測定できる
- **API 安定性**: 高い可用性と安定したレスポンス時間

### Alternatives Considered

| 代替案 | メリット | デメリット | 却下理由 |
|--------|---------|-----------|---------|
| **OpenAI API 直接** | 公式、豊富なドキュメント | API キー別途契約必要、追加コスト | GitHub Copilot Pro のみ契約のため利用不可 |
| **Claude 3.7 Sonnet (GitHub Models)** | 日本語品質高い、長文対応 | GPT-4o と比較して評価データ少ない | GPT-4o で十分、将来的に切り替え可能 |
| **ローカル LLM (Ollama + Llama 3等)** | コスト不要 | GPU 必要、日本語品質不明 | DevContainer 環境でのセットアップが複雑 |

### Parameters
- **Model**: `gpt-4o`
- **Temperature**: 0.3 (ファクト重視、一貫性優先)
- **MaxTokens**: 1000 (回答の長さ制限)
- **API Endpoint**: `https://models.inference.ai.azure.com/chat/completions`
- **認証**: 環境変数 `GITHUB_TOKEN` で管理

### Implementation Pattern
```python
async def generate_answer(question: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks)
    prompt = f"""以下のドキュメントに基づいて質問に答えてください。

【ドキュメント】
{context}

【質問】
{question}

【回答】"""
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://models.inference.ai.azure.com/chat/completions",
            headers={
                "Authorization": f"Bearer {GITHUB_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 1000
            }
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
```

---

## 3. フロントエンドビルドツール

### Decision
**Vite + React** を採用（Phase 2 以降で実装）

### Rationale
- **高速**: Vite は開発サーバーの起動とホットリロードが非常に高速
- **シンプル**: 設定が最小限で、MVP の素早い構築に適している
- **モダン**: ES Modules ベースで、最新の JavaScript 標準に対応
- **TypeScript サポート**: 標準で TypeScript に対応 (オプション)
- **React 公式推奨**: React の公式ドキュメントでも Vite が推奨されている

**注意**: 初期 MVP（Phase 1）では REST API のみを実装し、フロントエンドは将来的な拡張として扱います。

### Alternatives Considered

| 代替案 | メリット | デメリット | 却下理由 |
|--------|---------|-----------|---------|
| **Next.js** | SSR/SSG、フルスタック | MVP では過剰機能、学習コスト高い | 単純な SPA で十分 |
| **Create React App** | 公式、安定 | 開発速度が Vite より遅い、メンテナンス停滞 | Vite の方が開発体験が良い |

### Setup
- **Template**: `npm create vite@latest frontend -- --template react`
- **Dev Server**: `npm run dev` (port 5173)
- **Build**: `npm run build` で production ビルド

---

## 4. デプロイ環境

### Decision
**Docker Compose (ローカル開発・検証環境)** を採用

### Rationale
- **教育目的**: ローカルで完結し、チーム全員が同じ環境で実行可能
- **再現性**: Docker Compose で backend, frontend, ChromaDB を統合管理
- **DevContainer 互換**: 既存の DevContainer 環境との親和性が高い
- **MVP 適合**: 本番デプロイは範囲外、検証と学習にフォーカス
- **シンプル**: Kubernetes 等のオーケストレーションは不要

### Alternatives Considered

| 代替案 | メリット | デメリット | 却下理由 |
|--------|---------|-----------|---------|
| **Kubernetes** | スケーラブル、本番対応 | セットアップ複雑、MVP に過剰 | スコープ外（constitution でスケーリング除外） |
| **ローカル直接実行** | シンプル | 環境依存、再現性低い | 再現性が constitution の最優先事項 |
| **クラウドデプロイ** | 本番想定 | コスト、管理負担 | MVP 段階では不要 |

### Setup
- **docker-compose.yml**: backend (FastAPI), frontend (Vite dev server), ChromaDB を定義
- **Volumes**: ChromaDB データ永続化、experiments/ ログ保存
- **Networks**: 内部ネットワークで backend ↔ ChromaDB 通信

---

## 5. 追加の技術選定

### ドキュメント処理
- **アプローチ**: シンプルなテキスト分割アルゴリズムを自前実装
  - **Decision**: **固定サイズ + オーバーラップ方式**を採用（LangChain は使用しない）
  - **Rationale**: MVP では依存関係を最小化し、シンプルな実装で十分
  - **Chunk Size**: 500 文字（日本語テキストの場合）
  - **Chunk Overlap**: 50 文字（コンテキスト保持）
  
```python
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks
```

### テストフレームワーク
- **Backend**: `pytest` + `pytest-asyncio` (FastAPI の非同期テスト)
- **Frontend**: `Vitest` + `@testing-library/react` (Vite 推奨)
- **Contract Test**: `pytest` + `requests` で API エンドポイントを検証

### ロギング
- **Backend**: Python 標準 `logging` + JSON 形式で experiments/ に出力
- **Frontend**: `console.log` (開発時のみ)

---

## Summary

すべての技術選定が完了しました。以下の技術スタックで Phase 1 (Design & Contracts) に進みます：

| カテゴリ | 選定技術 | 理由 |
|---------|---------|------|
| **埋め込みモデル** | GitHub Models text-embedding-3-small | 日本語品質、GitHub トークンのみ、追加コスト不要 |
| **生成モデル** | GitHub Models GPT-4o | 日本語品質、GitHub トークンのみ、統合容易 |
| **バックエンド** | FastAPI + ChromaDB | 非同期対応、型安全、軽量ベクトルDB |
| **フロントエンド** | Vite + React (Phase 2以降) | 高速、シンプル、モダン |
| **デプロイ** | Docker Compose | 再現性、教育目的、MVP 適合 |
| **ドキュメント処理** | 自前実装（固定サイズ分割） | 依存関係最小化、シンプル |
| **テスト** | pytest, Vitest | 標準的、フレームワーク親和性高い |
| **認証** | GitHub Token (GITHUB_TOKEN 環境変数) | 統一された認証、追加契約不要 |

この選定は constitution の principles (再現性、MVP 優先、教育目的、シークレット管理) に準拠しています。特に、GitHub Copilot Pro 契約のみで完結し、追加の API キー契約が不要な点が重要な特徴です。
