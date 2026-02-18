# Copilot Instructions

## Language / 言語

**GitHub Copilot の回答内容および途中のプロセス表示はすべて日本語で行うこと。**

## Project Overview / プロジェクト概要

このプロジェクトは、**仕様駆動開発（Spec-Driven Development）** と **RAG（Retrieval-Augmented Generation）** を組み合わせた、教育・検証目的の PoC です。

- **目的**: 仕様駆動開発と RAG の理解を深め、RAG と非 RAG の差分を教育的に検証する
- **最優先**: 再現性と可視化（何をしたか／なぜ行ったかを後から説明できること）
- **スコープ**: MVP を短期間で反復し、教育・検証を優先

## Architecture / アーキテクチャ

### 仕様駆動開発のワークフロー（GitHub Spec Kit）

このプロジェクトは **GitHub Spec Kit** を使用した 5 フェーズの開発プロセスに従います：

```
Constitution → Specify → Plan → Tasks → Implement
```

1. **Constitution（憲章）**: プロジェクトの開発規約と方針を `.specify/memory/constitution.md` に定義
2. **Specify（要件）**: 機能の WHAT を `.specify/features/[name]/spec.md` に記述
3. **Plan（実装計画）**: 技術的な HOW を `.specify/features/[name]/plan.md` に定義
4. **Tasks（タスク分割）**: 実装可能なタスクに分割し `.specify/features/[name]/tasks.md` に記載
5. **Implement（実装）**: タスクに基づき実装を実行

### スラッシュコマンド（Custom Agents）

以下の `/speckit.*` スラッシュコマンドが利用可能です：

- `/speckit.constitution` - プロジェクト憲章の作成・更新
- `/speckit.specify` - 機能仕様の作成
- `/speckit.plan` - 実装計画の作成
- `/speckit.tasks` - タスク分割
- `/speckit.implement` - 実装実行
- `/speckit.clarify` - 仕様の曖昧性を特定し質問を生成
- `/speckit.analyze` - 仕様・計画・タスクの一貫性分析
- `/speckit.checklist` - 機能別チェックリスト生成
- `/speckit.taskstoissues` - タスクを GitHub Issues に変換

エージェント定義: `.github/agents/speckit.*.agent.md`  
プロンプト: `.github/prompts/speckit.*.prompt.md`

### ディレクトリ構造

```
.
├── .devcontainer/           # DevContainer 設定（Python 3.11, uv, Node.js 24）
├── .github/
│   ├── agents/              # Copilot カスタムエージェント定義
│   └── prompts/             # エージェント用プロンプトテンプレート
├── .specify/
│   ├── memory/
│   │   └── constitution.md  # プロジェクト憲章
│   ├── scripts/             # 補助スクリプト
│   └── templates/           # ドキュメントテンプレート
├── specs/                   # 機能仕様の永続化先（将来的に実装予定）
│   └── 001-rag-chat/        # 現在進行中の機能
└── wsl_setup_scripts/       # WSL + Docker セットアップスクリプト
```

## Development Setup / 開発環境

### 環境構成

- **ホスト**: Windows 11
- **WSL2**: Debian
- **コンテナ**: DevContainer (Python 3.11-bullseye)
- **パッケージマネージャー**: uv
- **必須ツール**: Git, GitHub CLI, Node.js 24, Specify CLI

### セットアップコマンド

DevContainer は `.devcontainer/post-create.sh` で自動セットアップされます：

```bash
# uv のインストール
curl -LsSf https://astral.sh/uv/install.sh | sh

# Specify CLI のインストール
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# インストール確認
specify check
```

### 主要コマンド

```bash
# Specify CLI のバージョン確認
specify version

# 環境診断
specify check

# 新しい機能の初期化（将来的に実装予定）
# specify init --here --ai copilot
```

## Key Conventions / 重要な規約

### 憲章の遵守

すべての実装は `.specify/memory/constitution.md` に定義された原則に従う必要があります：

- **再現性**: 実験・実装の手順と結果を記録・可視化すること
- **評価**: RAG と非 RAG を定量・定性の両面で比較すること
- **セキュリティ**: シークレットは環境変数で管理し、リポジトリに埋め込まない
- **ドキュメント**: 主要ドキュメントは日本語で記述すること
- **スコープ**: MVP 優先で、段階的に拡張すること

### ワークフロー遵守

- 新機能の追加時は必ず Constitution → Specify → Plan → Tasks → Implement の順序で実施
- 各フェーズの成果物（spec, plan, tasks）をリポジトリに保存
- すべての PR は対応する `spec` または `plan` へのリンクを含めること

### 命名規則

- 機能ディレクトリ: `specs/NNN-feature-name/` 形式（例: `001-rag-chat`）
- ドキュメントファイル: `spec.md`, `plan.md`, `tasks.md`

### コードスタイル

- Python: Ruff を使用（フォーマット・リント）
- VS Code: 保存時に自動フォーマット有効

## Working with Features / 機能開発の進め方

### 新機能を追加する場合

1. `/speckit.constitution` で憲章を確認・更新（必要に応じて）
2. `/speckit.specify` で機能仕様を作成
3. `/speckit.plan` で実装計画を策定
4. `/speckit.tasks` でタスクに分割
5. `/speckit.implement` で実装を実行

### 既存機能を修正する場合

1. 対応する `spec.md` と `plan.md` を確認
2. 憲章との整合性をチェック
3. 必要に応じて `tasks.md` を更新
4. 実装を進める

## Important Notes / 重要事項

### シークレット管理

- API キーや認証情報は **絶対に** リポジトリにコミットしない
- 環境変数または安全なシークレット管理ツールを使用
- 設定手順は README または `docs/` に記載

### 実験データ

- 実験データは `experiments/` に整理
- 再現手順とメタデータを `experiments/README.md` に記録

### ドキュメント言語

- 主要ドキュメントは日本語で記述
- 英訳が必要な場合は別ファイルとして作成し、理由を明記
