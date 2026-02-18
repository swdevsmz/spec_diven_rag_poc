# Implementation Plan: RAGチャットボット

**Branch**: `001-rag-chat` | **Date**: 2026-02-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-rag-chat/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

日本語ドキュメント群を基に質問応答を行う RAG チャットボットを実装します。GitHub Models（埋め込みモデルと生成モデル）と ChromaDB を使用し、ドキュメント検索を活用した回答生成と、検索なしの Non-RAG モードとの比較評価を可能にします。REST API（FastAPI）を通じて、ドキュメント登録、ベクトル化、質問応答、実験ログ記録の機能を提供し、再現性と教育目的の検証を重視します。

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI, ChromaDB, GitHub Models SDK, uvicorn, pydantic  
**Storage**: ChromaDB (ベクトルストレージ)、ファイルシステム（ドキュメント保存、実験ログ保存）  
**Testing**: pytest, pytest-asyncio  
**Target Platform**: Linux サーバー（DevContainer 環境）  
**Project Type**: Web アプリケーション（バックエンド API + 将来的にフロントエンド）  
**Performance Goals**: 質問応答レスポンス時間 10秒以内（SC-001）  
**Constraints**: シークレットは環境変数管理、日本語ドキュメント対応必須、MVP 優先でスケーラビリティは対象外  
**Scale/Scope**: 評価用質問セット 10問、小〜中規模ドキュメント（数十〜数百ファイル想定）

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ 再現性と可視化 (Reproducibility & Visibility)
- [x] すべての実験ログを `experiments/` に構造化形式で保存（FR-010）
- [x] 実行パラメータ、使用モデル、取得ドキュメント ID を記録（FR-008）
- [x] quickstart.md で再現手順を文書化（Phase 1 で生成）

### ✅ 評価 (Evaluation)
- [x] RAG vs Non-RAG の定量比較機能を実装（FR-009）
- [x] 正答率とファクト一致率の測定（SC-002, SC-003）
- [x] 人間による手動評価プロセスを定義（Assumptions で明記）

### ✅ セキュリティ (Security)
- [x] GITHUB_TOKEN を環境変数から読み込み（FR-012）
- [x] シークレットをコードに埋め込まない（FR-012）
- [x] 起動時に環境変数の存在を検証（Edge Cases で明記）

### ✅ スコープ (Scope)
- [x] MVP 優先、スケーラビリティは対象外（Out of Scope）
- [x] 教育・検証目的に焦点（Purpose）
- [x] 評価用質問セット 10問で妥当性検証（SC-002, SC-003）

### ✅ 制約 (Constraints)
- [x] 主要ドキュメント（README、spec、plan等）を日本語で記述（FR-013）
- [x] エラーメッセージも日本語（FR-014）

**結論**: すべての憲章要件を満たしています。Phase 0 研究に進行可能です。

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-chat/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   └── api-spec.yaml    # OpenAPI 仕様
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI アプリケーションエントリーポイント
│   ├── config.py               # 環境変数・設定管理
│   ├── models/                 # データモデル（Pydantic）
│   │   ├── __init__.py
│   │   ├── document.py
│   │   ├── query.py
│   │   └── experiment.py
│   ├── services/               # ビジネスロジック
│   │   ├── __init__.py
│   │   ├── embedding.py        # GitHub Models 埋め込み生成
│   │   ├── vectordb.py         # ChromaDB 操作
│   │   ├── generation.py       # GitHub Models 生成
│   │   └── experiment_logger.py # 実験ログ記録
│   ├── api/                    # REST API エンドポイント
│   │   ├── __init__.py
│   │   ├── documents.py        # ドキュメント登録・ベクトル化
│   │   ├── queries.py          # 質問応答
│   │   └── evaluation.py       # 評価実行
│   └── utils/                  # ユーティリティ
│       ├── __init__.py
│       └── file_handlers.py    # ファイル処理
├── tests/
│   ├── contract/               # API 契約テスト
│   ├── integration/            # 統合テスト
│   └── unit/                   # 単体テスト
├── requirements.txt
└── README.md

data/
├── documents/                  # 登録ドキュメント保存先
├── chromadb/                   # ChromaDB データ保存先
└── evaluation/                 # 評価用質問セット

experiments/                    # 実験ログ保存先
└── README.md                   # 再現手順

frontend/                       # 将来的に実装（Phase 2以降）
└── [React アプリケーション]
```

**Structure Decision**: Web アプリケーション構成を採用。バックエンド（FastAPI）を `backend/` に配置し、将来的なフロントエンド（React）拡張を考慮して `frontend/` ディレクトリを予約。データと実験ログはリポジトリルートに配置し、明確に分離します。

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

該当なし。すべての憲章要件を満たしており、複雑性の正当化は不要です。

---

## Phase 0: Research ✅

**Status**: 完了  
**Output**: [research.md](./research.md)

### 完了内容
- GitHub Models（埋め込み・生成）の使用方法調査
- ChromaDB 統合パターンの決定
- FastAPI ベストプラクティスの適用
- ドキュメントチャンク分割戦略の決定
- 実験ログの構造化形式の設計
- エラーハンドリングとテスト戦略の策定

### 主要な決定事項
- GitHub Models を HTTP API 経由で使用（`httpx` ライブラリ）
- ChromaDB をローカル永続化モード + Docker で運用
- 固定サイズ（500文字）+ オーバーラップ（50文字）でチャンク分割
- JSON Lines 形式で実験ログを記録

---

## Phase 1: Design & Contracts ✅

**Status**: 完了  
**Outputs**: 
- [data-model.md](./data-model.md)
- [contracts/api-spec.yaml](./contracts/api-spec.yaml)
- [quickstart.md](./quickstart.md)

### 完了内容
- データモデル（6エンティティ）の詳細設計
- Pydantic モデルの定義
- REST API 仕様（OpenAPI 3.0）の作成
- クイックスタートガイドの作成
- エージェントコンテキストの更新

### エンティティ
1. Document（ドキュメント）
2. DocumentChunk（ドキュメントチャンク）
3. Query（質問）
4. Answer（回答）
5. RetrievedChunk（取得されたチャンク）
6. ExperimentLog（実験記録）

### API エンドポイント
- `POST /api/v1/documents` - ドキュメント登録
- `POST /api/v1/documents/{document_id}/vectorize` - ベクトル化実行
- `POST /api/v1/query` - 質問応答（RAGモード）
- `POST /api/v1/query/compare` - RAG vs Non-RAG 比較
- `POST /api/v1/evaluation` - 評価実行
- `GET /api/v1/experiments` - 実験ログ取得

---

## Constitution Check (再確認) ✅

Phase 1 完了後の再チェック:

### ✅ 再現性と可視化
- 実験ログ形式が定義済み（JSON Lines）
- quickstart.md で再現手順を文書化完了
- データモデルに再現に必要な全情報を含む

### ✅ 評価
- API 仕様に評価エンドポイントを定義
- 比較モードのエンドポイント実装計画完了
- 評価質問セットの管理方法を決定

### ✅ セキュリティ
- 環境変数（GITHUB_TOKEN）による認証を設計
- quickstart.md でトークン管理方法を文書化
- .env ファイルの .gitignore 除外を明記

### ✅ スコープ
- バックエンド API に焦点、フロントエンドは将来対応
- Docker Compose でローカル完結
- 評価は10問で実施

### ✅ 制約
- 全ドキュメントが日本語で作成済み
- API エラーメッセージも日本語対応

**結論**: すべての憲章要件を引き続き満たしています。Phase 2 (Tasks) に進行可能です。

---

## Next Steps

1. **Phase 2: Tasks（タスク分割）** - `/speckit.tasks` コマンドを実行
   - `tasks.md` の生成
   - 実装タスクの優先順位付けと依存関係の整理
   
2. **Phase 3: Implementation（実装）** - `/speckit.implement` コマンドを実行
   - タスクに基づいた実装の開始
   - テスト駆動開発の実施
   - 段階的なデプロイと検証

---

## Summary

RAGチャットボットの実装計画が完了しました。

### 主要な成果物
- ✅ Technical Context の定義
- ✅ Constitution Check の完了
- ✅ Project Structure の設計
- ✅ Phase 0: Research（技術調査）
- ✅ Phase 1: Design & Contracts（設計・契約）

### 技術スタック
- **言語**: Python 3.11+
- **バックエンド**: FastAPI + ChromaDB
- **AI Models**: GitHub Models (text-embedding-3-small, GPT-4o)
- **認証**: GitHub Token (GITHUB_TOKEN 環境変数)
- **テスト**: pytest, pytest-asyncio
- **デプロイ**: Docker Compose

次のコマンドで実装タスクの分割に進んでください:
```
/speckit.tasks
```
