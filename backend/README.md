# Backend

## セットアップ

```bash
cd backend
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## 環境変数

プロジェクトルートに `.env` を作成し、以下を設定します。

```bash
GITHUB_TOKEN=your_token
CHROMA_HOST=localhost
CHROMA_PORT=8001
GENERATION_MODEL=gpt-4o
EMBEDDING_MODEL=text-embedding-3-small
LOG_LEVEL=INFO
```

## 起動

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
