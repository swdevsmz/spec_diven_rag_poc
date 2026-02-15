# Research: RAGチャットボット技術選定

**Date**: 2026-02-14  
**Purpose**: Technical Context の NEEDS CLARIFICATION 項目を解決し、実装に必要な技術選定を行う

## 1. 埋め込みモデル (Embedding Model)

### Decision
**OpenAI text-embedding-3-small** を採用

### Rationale
- **日本語対応**: OpenAI の埋め込みモデルは多言語対応で日本語の品質が高い
- **次元数**: 512/1536 次元を選択可能。コストと精度のバランスが良い text-embedding-3-small (1536次元) を選択
- **API ベース**: ローカル環境不要で、DevContainer から直接利用可能
- **コスト**: text-embedding-3-small は ada-002 より安価 ($0.02/1M tokens)
- **ChromaDB 互換性**: OpenAI の埋め込みは ChromaDB で標準的にサポートされている
- **MVP 適合**: 教育・検証目的であり、API ベースで素早く実装できる

### Alternatives Considered

| 代替案 | メリット | デメリット | 却下理由 |
|--------|---------|-----------|---------|
| **multilingual-e5-large** | ローカル実行可能、コスト不要 | GPU 必要、DevContainer での動作検証が必要 | MVP フェーズではセットアップ複雑性が高い |
| **intfloat/multilingual-e5-base** | 軽量、ローカル実行 | 精度が large より低い | OpenAI の品質と比較して教育的価値が低い |
| **sentence-transformers (日本語)** | オープンソース、柔軟性高い | 日本語モデルの選定・評価が必要 | 選定に時間がかかり MVP に不適 |

### Parameters
- **Model**: `text-embedding-3-small`
- **Dimensions**: 1536 (デフォルト)
- **API Key**: 環境変数 `OPENAI_API_KEY` で管理

---

## 2. 生成モデル (LLM)

### Decision
**OpenAI GPT-4o-mini** を採用

### Rationale
- **日本語品質**: GPT-4 シリーズは日本語の生成品質が高く、教育検証に適している
- **コスト効率**: GPT-4o-mini は GPT-4 より大幅に安価 ($0.15/1M input, $0.60/1M output) でMVPに適合
- **コンテキスト長**: 128k tokens で、複数ドキュメントを含むプロンプトに対応可能
- **API 安定性**: 高い可用性と安定したレスポンス時間
- **Non-RAG 比較**: 同じモデルで RAG/Non-RAG を比較することで、検索の効果を純粋に測定できる

### Alternatives Considered

| 代替案 | メリット | デメリット | 却下理由 |
|--------|---------|-----------|---------|
| **GPT-4 (full)** | 最高品質 | コストが高い ($10/1M input) | MVP では過剰、教育目的で不要 |
| **GPT-3.5-turbo** | 最安価 | 日本語品質が GPT-4 系より劣る | 教育的価値を高めるため GPT-4 系を優先 |
| **Claude 3.5 Sonnet** | 日本語品質高い、長文対応 | API キー別途必要、コスト比較必要 | OpenAI との統合が容易（埋め込みと同一） |
| **ローカル LLM (Llama 3等)** | コスト不要 | GPU 必要、日本語品質不明 | DevContainer 環境でのセットアップが複雑 |

### Parameters
- **Model**: `gpt-4o-mini`
- **Temperature**: 0.3 (ファクト重視、一貫性優先)
- **MaxTokens**: 1000 (回答の長さ制限)
- **API Key**: 環境変数 `OPENAI_API_KEY` で管理

---

## 3. フロントエンドビルドツール

### Decision
**Vite + React** を採用

### Rationale
- **高速**: Vite は開発サーバーの起動とホットリロードが非常に高速
- **シンプル**: 設定が最小限で、MVP の素早い構築に適している
- **モダン**: ES Modules ベースで、最新の JavaScript 標準に対応
- **TypeScript サポート**: 標準で TypeScript に対応 (オプション)
- **React 公式推奨**: React の公式ドキュメントでも Vite が推奨されている

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
- **ライブラリ**: `langchain` または `llama-index` のドキュメントローダー
  - **Decision**: **LangChain** を採用
  - **Rationale**: ドキュメント分割 (TextSplitter)、埋め込み、ChromaDB 統合が充実
  - **Chunk Size**: 500 tokens (日本語は約 250 文字相当)
  - **Chunk Overlap**: 50 tokens (コンテキスト保持)

### テストフレームワーク
- **Backend**: `pytest` + `pytest-asyncio` (FastAPI の非同期テスト)
- **Frontend**: `Vitest` + `@testing-library/react` (Vite 推奨)
- **Contract Test**: `pytest` + `requests` で API エンドポイントを検証

### ロギング
- **Backend**: Python 標準 `logging` + JSON 形式で experiments/ に出力
- **Frontend**: `console.log` (開発時のみ)

---

## Summary

すべての NEEDS CLARIFICATION が解決されました。以下の技術スタックで Phase 1 (Design & Contracts) に進みます：

| カテゴリ | 選定技術 | 理由 |
|---------|---------|------|
| **埋め込みモデル** | OpenAI text-embedding-3-small | 日本語品質、コスト、API 利用可 |
| **生成モデル** | OpenAI GPT-4o-mini | 日本語品質、コスト効率、統合容易 |
| **フロントエンド** | Vite + React | 高速、シンプル、モダン |
| **デプロイ** | Docker Compose | 再現性、教育目的、MVP 適合 |
| **ドキュメント処理** | LangChain | ChromaDB 統合、充実した機能 |
| **テスト** | pytest, Vitest | 標準的、フレームワーク親和性高い |

この選定は constitution の principles (再現性、MVP 優先、教育目的) に準拠しています。
