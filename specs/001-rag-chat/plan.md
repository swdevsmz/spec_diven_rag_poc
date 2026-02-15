# Implementation Plan: RAGチャットボット

**Branch**: `001-rag-chat` | **Date**: 2026-02-14 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-rag-chat/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

日本語ドキュメント群を対象としたRAGチャットボットを構築します。ユーザーは質問を入力し、システムはベクトル検索で関連ドキュメントを取得して生成モデルで回答します。バックエンドは FastAPI + ChromaDB、フロントエンドは React で実装します。RAG と Non-RAG の比較評価を行い、教育・検証目的で再現性を重視します。

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: FastAPI (バックエンドAPI), ChromaDB (ベクトルDB), React (フロントエンド) → **フロントエンドフレームワーク詳細は NEEDS CLARIFICATION (Vite/Next.js/CRA)**  
**Storage**: ChromaDB (ベクトルストア), ファイルシステム (実験ログ、ドキュメント保存)  
**Testing**: pytest (バックエンド), Jest/Vitest (フロントエンド) → **フロントテストツール詳細は NEEDS CLARIFICATION**  
**Target Platform**: Web application (Linux server backend + browser frontend)  
**Project Type**: Web (backend + frontend)  
**Performance Goals**: 質問応答レスポンス < 10秒  
**Constraints**: シークレット管理は環境変数必須, ドキュメントは日本語, MVPフォーカス (スケーリング除外)  
**Scale/Scope**: 評価用質問10問, 小〜中規模ドキュメント (数百〜数千件), 同時ユーザー考慮不要  
**未確定技術選択 (Phase 0 Research で決定)**: 
- **埋め込みモデル**: NEEDS CLARIFICATION (候補: OpenAI text-embedding-3-small, multilingual-e5-large, intfloat/multilingual-e5-base など。日本語対応、次元数、コスト、ローカル実行可否を考慮)
- **生成モデル**: NEEDS CLARIFICATION (候補: OpenAI GPT-4/GPT-3.5, Claude, ローカルLLM など。日本語品質、コスト、API vs ローカルを考慮)
- **フロントエンドビルドツール**: NEEDS CLARIFICATION (候補: Vite, Next.js, Create React App)
- **デプロイ環境**: NEEDS CLARIFICATION (候補: Docker Compose, Kubernetes, ローカル開発のみ)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| 原則 | 状態 | 準拠状況 |
|-----|------|---------|
| **再現性と可視化** | ✅ PASS | 実験ログを experiments/ に保存、再現手順を明記する設計 |
| **RAG vs Non-RAG 比較** | ✅ PASS | FR-009 で Non-RAG モード実装、評価指標で定量比較を明記 |
| **定性評価** | ✅ PASS | SC-006 でユーザビリティ評価（5点満点）を含む |
| **シークレット管理** | ✅ PASS | FR-012 で環境変数管理を必須化、コード埋め込み禁止 |
| **MVP & 教育優先** | ✅ PASS | スケーリング除外、評価用10問で検証、段階的改善 |
| **日本語ドキュメント** | ✅ PASS | FR-013 で主要ドキュメントの日本語記載を必須化 |
| **5フェーズワークフロー** | ✅ PASS | spec → plan (本文書) → tasks → implement の流れを遵守 |

**判定**: すべての原則に準拠しており、Phase 0 Research に進行可能です。

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/           # データモデル (Document, Query, Answer, ExperimentLog)
│   ├── services/         # ビジネスロジック (embedding, retrieval, generation)
│   ├── api/              # FastAPI エンドポイント
│   ├── storage/          # ChromaDB 接続、ファイルIO
│   └── config/           # 設定、環境変数読み込み
├── tests/
│   ├── unit/             # 単体テスト
│   ├── integration/      # 統合テスト (API, DB)
│   └── fixtures/         # テストデータ
└── scripts/              # ドキュメント登録、評価実行スクリプト

frontend/
├── src/
│   ├── components/       # UI コンポーネント (QuestionForm, AnswerDisplay)
│   ├── pages/            # ページ (Home, Evaluation)
│   ├── services/         # API クライアント
│   └── utils/            # ヘルパー関数
├── tests/
│   └── components/       # コンポーネントテスト
└── public/               # 静的ファイル

data/                     # サンプルドキュメント、評価質問セット
experiments/              # 実験ログ、再現手順
└── README.md             # 実験の再現方法
```

**Structure Decision**: Web application として backend (FastAPI) と frontend (React) を分離。backend は API 提供、frontend は UI を担当します。実験ログと再現手順は experiments/ に集約します。

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | - | - |

## Phase 0: Research Completed ✅

**成果物**: [`research.md`](research.md)

Phase 0 で未確定だった技術選択を決定しました：
- **埋め込みモデル**: OpenAI text-embedding-3-small (1536次元)
- **生成モデル**: OpenAI GPT-4 / GPT-3.5-turbo
- **フロントエンドビルドツール**: Vite
- **デプロイ環境**: Docker Compose

詳細は [`research.md`](research.md) を参照してください。

## Phase 1: Design Completed ✅

**成果物**:
- [`data-model.md`](data-model.md) - データモデルとエンティティ関係
- [`contracts/api-spec.yaml`](contracts/api-spec.yaml) - REST API 仕様（OpenAPI 3.0）
- [`quickstart.md`](quickstart.md) - クイックスタートガイド
- `.github/agents/copilot-instructions.md` - GitHub Copilot コンテキスト（更新済み）

### Constitution Check (Phase 1 完了後)

*Re-check after Phase 1 design as required by the plan template.*

| 原則 | 状態 | Phase 1 成果物での準拠状況 |
|-----|------|---------------------------|
| **再現性と可視化** | ✅ PASS | quickstart.md で詳細な環境構築手順と実験再現手順を提供。api-spec.yaml で実験ログエンドポイント（GET /experiments）を定義。 |
| **RAG vs Non-RAG 比較** | ✅ PASS | api-spec.yaml で /query/compare エンドポイントを定義し、両モードの比較を実装可能に。 |
| **定性評価** | ✅ PASS | api-spec.yaml で /evaluation エンドポイントを定義し、評価セット（10問）による評価を実装可能に。 |
| **シークレット管理** | ✅ PASS | quickstart.md で .env ファイルを使用した環境変数管理を明記。OPENAI_API_KEY 等の設定例を提供。 |
| **MVP & 教育優先** | ✅ PASS | data-model.md と api-spec.yaml で必須機能のみを定義。スケーリングや高度な機能は除外。 |
| **日本語ドキュメント** | ✅ PASS | すべての成果物（research.md, data-model.md, quickstart.md, api-spec.yaml の description）が日本語で記述。 |
| **5フェーズワークフロー** | ✅ PASS | spec → plan (本文書) → research (Phase 0) → design (Phase 1) の流れを完了。次は tasks フェーズ。 |

**Phase 1 判定**: すべての原則に準拠しています。Phase 2（Tasks 分割）に進行可能です。

## Next Steps

1. **Phase 2: Tasks 分割** - `/speckit.tasks` コマンドを実行して、実装タスクに分割
2. **Phase 3: Implement** - `/speckit.implement` コマンドで実装を実行
3. **継続的な憲章準拠確認** - 各実装タスクで憲章の原則を再確認

---

**Plan Status**: Phase 1 完了 ✅ | **Last Updated**: 2026-02-14
