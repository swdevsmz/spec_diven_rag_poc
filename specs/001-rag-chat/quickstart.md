# RAGチャットボット クイックスタートガイド

**対象者**: 開発者、評価者  
**所要時間**: 約20分  
**前提条件**: Docker、Python 3.11+、Git がインストール済み

---

## 📋 概要

このガイドでは、RAGチャットボットをローカル環境で起動し、最初の質問応答を実行するまでの手順を説明します。

### 構成要素
- **バックエンド**: FastAPI（Python）
- **ベクトルDB**: ChromaDB
- **埋め込みモデル**: GitHub Models text-embedding-3-small (1536次元)
- **生成モデル**: GitHub Models GPT-4o
- **フロントエンド**: React（将来実装）
- **認証**: GitHub Token（GitHub Copilot Pro 契約で利用可能）

---

## 🚀 セットアップ手順

### Step 1: リポジトリのクローン

```bash
git clone https://github.com/swdevsmz/spec_diven_rag_poc.git
cd spec_diven_rag_poc
```

### Step 2: 環境変数の設定

プロジェクトルートに `.env` ファイルを作成し、以下を設定します：

```bash
# .env ファイル
GITHUB_TOKEN=ghp_your_github_token_here

# ChromaDB 設定（ローカル実行時はデフォルト値で OK）
CHROMA_HOST=localhost
CHROMA_PORT=8001

# 生成モデル設定
GENERATION_MODEL=gpt-4o
EMBEDDING_MODEL=text-embedding-3-small

# ログ設定
LOG_LEVEL=INFO
```

**⚠️ 重要**: 
- `.env` ファイルは `.gitignore` に含まれています。絶対にリポジトリにコミットしないでください。
- GitHub Token は GitHub Settings > Developer settings > Personal access tokens から生成できます（GitHub Copilot Pro 契約があれば GitHub Models にアクセス可能）

### Step 3: 依存関係のインストール

#### Python 環境（uv を使用）

```bash
# DevContainer 内で実行する場合は uv が既にインストール済み
# 仮想環境は作成せず、システム環境に依存関係をインストール
uv pip install --system -r requirements.txt
```

#### 必要なパッケージ（requirements.txt）

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
chromadb==0.4.22
openai==1.12.0
python-dotenv==1.0.1
pydantic==2.6.0
pydantic-settings==2.1.0
langchain==0.1.6
langchain-openai==0.0.5
pypdf==4.0.0
```

### Step 4: ChromaDB の起動

ChromaDB をローカルで起動します（Docker を使用）：

```bash
docker run -d \
  --name chromadb \
  -p 8001:8000 \
  -v $(pwd)/data/chromadb:/chroma/chroma \
  chromadb/chroma:latest
```

**確認**:
```bash
curl http://localhost:8001/api/v1/heartbeat
# 正常な場合: {"nanosecond heartbeat": 1234567890}
```

### Step 5: FastAPI サーバーの起動

```bash
cd backend
uv run --with-requirements requirements.txt uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**確認**:
- ブラウザで http://localhost:8000/docs にアクセス
- Swagger UI が表示されればOK

---

## 📝 最初の質問応答を実行

### Step 1: ドキュメントの準備

サンプルドキュメントを作成します：

```bash
mkdir -p data/documents
cat > data/documents/sample.txt << 'EOF'
# FastAPI ガイド

FastAPI は、Python 3.7+ で API を構築するための、モダンで高速な Web フレームワークです。

## 主な特徴
- 高速: NodeJS や Go に匹敵する非常に高いパフォーマンス
- 高速なコーディング: 開発速度を約 200% ~ 300% 向上
- 少ないバグ: 人為的なエラーを約 40% 削減
- 直感的: 優れたエディタのサポート
- 簡単: 簡単に使用でき、ドキュメントの読み込み時間を削減
- 堅牢: 本番環境対応のコードを取得

## インストール方法
```bash
uv pip install --system fastapi "uvicorn[standard]"
```

## 簡単な例
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

このコードを save.py として保存し、以下で実行します:
```bash
uv run --with fastapi --with "uvicorn[standard]" uvicorn main:app --reload
```
EOF
```

### Step 2: ドキュメントのアップロード

```bash
curl -X POST "http://localhost:8000/api/v1/documents" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/documents/sample.txt"
```

**レスポンス例**:
```json
{
  "document_id": "123e4567-e89b-12d3-a456-426614174000",
  "filename": "sample.txt",
  "file_type": "txt",
  "status": "pending",
  "created_at": "2026-02-14T10:00:00Z"
}
```

### Step 3: ドキュメントのベクトル化

上記で取得した `document_id` を使用します：

```bash
curl -X POST "http://localhost:8000/api/v1/documents/123e4567-e89b-12d3-a456-426614174000/vectorize" \
  -H "Content-Type: application/json" \
  -d '{
    "chunk_size": 500,
    "chunk_overlap": 50
  }'
```

**レスポンス例**:
```json
{
  "document_id": "123e4567-e89b-12d3-a456-426614174000",
  "chunks_created": 5,
  "status": "processed",
  "embedding_model": "text-embedding-3-small",
  "embedding_dimension": 1536
}
```

### Step 4: 質問を投げる

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "FastAPIの主な特徴を教えてください",
    "top_k": 5,
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

**レスポンス例**:
```json
{
  "query_id": "456e7890-e89b-12d3-a456-426614174001",
  "question": "FastAPIの主な特徴を教えてください",
  "answer": "FastAPIの主な特徴は以下の通りです：\n1. 高速: NodeJSやGoに匹敵する非常に高いパフォーマンス\n2. 高速なコーディング: 開発速度を約200%~300%向上\n3. 少ないバグ: 人為的なエラーを約40%削減\n4. 直感的: 優れたエディタのサポート\n5. 簡単: 簡単に使用でき、ドキュメントの読み込み時間を削減\n6. 堅牢: 本番環境対応のコードを取得",
  "retrieved_chunks": [
    {
      "chunk_id": "789e0123-e89b-12d3-a456-426614174002",
      "document_id": "123e4567-e89b-12d3-a456-426614174000",
      "content": "## 主な特徴\n- 高速: NodeJS や Go に匹敵する非常に高いパフォーマンス\n- 高速なコーディング: 開発速度を約 200% ~ 300% 向上...",
      "similarity_score": 0.92
    }
  ],
  "model": "gpt-4",
  "parameters": {
    "temperature": 0.7,
    "max_tokens": 500,
    "top_k": 5
  },
  "timestamp": "2026-02-14T10:05:00Z"
}
```

---

## 🔬 RAG vs Non-RAG 比較

RAG モードと Non-RAG モードの違いを確認します：

```bash
curl -X POST "http://localhost:8000/api/v1/query/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "FastAPIの主な特徴を教えてください",
    "top_k": 5,
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

**レスポンス例**:
```json
{
  "question": "FastAPIの主な特徴を教えてください",
  "rag_response": {
    "answer": "FastAPIの主な特徴は...(ドキュメントに基づく詳細な回答)",
    "retrieved_chunks": [...]
  },
  "non_rag_response": {
    "answer": "FastAPIは...(一般的な知識のみに基づく回答)",
    "model": "gpt-4",
    "parameters": {...}
  },
  "timestamp": "2026-02-14T10:10:00Z"
}
```

---

## 📊 実験ログの確認

実行された質問応答のログを確認します：

```bash
curl "http://localhost:8000/api/v1/experiments?limit=10"
```

ログは `experiments/` ディレクトリにも JSON 形式で保存されます：

```bash
ls experiments/
# 2026-02-14_experiment_001.json
# 2026-02-14_experiment_002.json
```

---

## 🧪 評価の実行

評価用質問セット（10問）を使用してシステムを評価します：

### Step 1: 評価用質問セットの準備

```bash
cat > data/evaluation/default_set.json << 'EOF'
{
  "evaluation_set_id": "default",
  "questions": [
    {
      "question": "FastAPIの主な特徴を教えてください",
      "expected_answer": "高速、高速なコーディング、少ないバグ、直感的、簡単、堅牢",
      "category": "features"
    },
    {
      "question": "FastAPIをインストールする方法は？",
      "expected_answer": "uv pip install --system fastapi \"uvicorn[standard]\"",
      "category": "installation"
    }
    // ... 残り8問
  ]
}
EOF
```

### Step 2: 評価の実行

```bash
curl -X POST "http://localhost:8000/api/v1/evaluation" \
  -H "Content-Type: application/json" \
  -d '{
    "evaluation_set_id": "default",
    "mode": "both"
  }'
```

**レスポンス例**:
```json
{
  "evaluation_id": "eval-001",
  "mode": "both",
  "results": {
    "rag": {
      "accuracy": 0.9,
      "fact_match_rate": 0.85,
      "average_response_time": 1.2,
      "question_results": [...]
    },
    "non_rag": {
      "accuracy": 0.6,
      "fact_match_rate": 0.55,
      "average_response_time": 0.8,
      "question_results": [...]
    }
  }
}
```

---

## 🛠️ トラブルシューティング

### ChromaDB に接続できない

```bash
# ChromaDB コンテナの状態を確認
docker ps | grep chromadb

# ログを確認
docker logs chromadb

# 再起動
docker restart chromadb
```

### GitHub Token エラー

```bash
# GitHub Token が正しく設定されているか確認
echo $GITHUB_TOKEN

# .env ファイルを再読み込み
source .env

# GitHub Models へのアクセス確認
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://models.inference.ai.azure.com/models
```

### ベクトル化が失敗する

- ドキュメントファイルが破損していないか確認
- サポートされているファイル形式（txt, pdf, md）か確認
- ログを確認: `tail -f logs/app.log`

---

## 📚 次のステップ

1. **フロントエンド開発**: React フロントエンドの実装
2. **カスタムドキュメント追加**: 独自のドキュメントを登録
3. **評価セット拡充**: より多様な質問で評価
4. **パラメータチューニング**: chunk_size, top_k, temperature の最適化

---

## 🔗 関連ドキュメント

- [API 仕様](./contracts/api-spec.yaml)
- [データモデル](./data-model.md)
- [技術調査結果](./research.md)
- [機能仕様](./spec.md)
- [実装計画](./plan.md)
