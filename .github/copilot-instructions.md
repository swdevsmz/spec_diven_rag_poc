# Copilot 指示書

## プロジェクト概要

このリポジトリは、仕様駆動開発（Specification-Driven Development）と RAG（Retrieval-Augmented Generation）を学ぶための PoC（Proof of Concept）プロジェクトです。主な目的は、RAG を用いた AI チャットボットを構築し、プレーンテキスト直接入力とベクトルDB（ChromaDB）を用いた取得強化の違いを明確に示すことです。

キーワード: 仕様駆動開発、RAG、ChromaDB、AI チャットボット PoC

## 中核方針

このプロジェクトの最優先事項は「仕様駆動」と「RAG を利用した学習／検証」です。作業は常にこの目的に沿って行い、範囲や目的があいまいな場合は作業を進める前に必ず確認してください。

## 開発環境（DevContainer）

このリポジトリは DevContainer を用いることを前提としています。主な構成要素:

- Python 3.11+（ベースイメージ: `mcr.microsoft.com/devcontainers/python:3.11-bullseye`）
- uv（パッケージマネージャー）
- Specify CLI（GitHub Spec Kit）
- Node.js 24（spec-kit 用）
- GitHub CLI (`gh`) と Copilot 拡張
- Ruff（Python 用リンタ/フォーマッタ）

### 環境確認コマンド

```bash
# 環境の基本チェック
specify check

# 必要に応じてプロジェクト初期化
specify init

# Specify のヘルプ表示
specify --help
```

### 主要ツールの配置（例）

- `specify`: `/home/vscode/.local/bin/specify`
- `uv`: `/home/vscode/.local/bin/uv`
- `python3`: `/usr/local/bin/python3`

## GitHub Spec Kit ワークフロー（概要）

このプロジェクトでは Specify CLI を想定した仕様駆動開発を行います。代表的なコマンド:

- `specify init` - テンプレートからプロジェクトを初期化
- `specify check` - 必要なツールのインストール状況を検証
- `specify version` - バージョン情報や環境情報を表示
- `specify extension` - Spec Kit の拡張管理

注: スラッシュコマンド等の具体的な仕様はまだ確立されていないため、未定義のワークフローについては推測で実装しないでください。

## アーキテクチャ（現状）

現在は初期構成段階です。想定する主要コンポーネント:

- RAG システム: ChromaDB を想定したベクトルストレージ
- AI チャットボット: 直接テキスト入力とベクター検索を比較検証する
- 仕様駆動開発: GitHub Spec Kit に基づくワークフロー

### 想定ディレクトリ構成（抜粋）

```
/workspaces/spec_diven_rag_poc/
├── .devcontainer/          # DevContainer 設定
│   ├── devcontainer.json
│   └── post-create.sh      # 自動セットアップスクリプト
├── wsl_setup_scripts/      # WSL2 / Docker 用スクリプト
├── .gitignore              # キャッシュや環境ファイルの除外設定
└── README.md               # 日本語のプロジェクト説明
```

## キーとなる慣習

- ドキュメントは主に日本語で記述されています（README 等）。
- Python パッケージ管理は可能な限り `uv` を使用することを想定します。
- Ruff によるフォーマット（保存時自動整形）が設定されています。
- 仕様駆動開発のため、仕様が不明瞭な場合は実装前に明確化してください。

## GitHub Copilot CLI について

- `gh` CLI の Copilot 拡張を利用できます。
- 初回実行時に Copilot CLI が `/home/vscode/.local/share/gh/copilot` にダウンロードされます。
- 認証が必要です: `gh auth login`
- 使い方例: `gh copilot -p "<prompt>"`

## やってはいけないこと

- 学習目的や PoC の範囲を超えて不要な機能を追加しないこと
- ドキュメントに記載のないスラッシュコマンド等のワークフローを仮定して実装しないこと
- 過度な最適化よりもまず PoC の検証を優先すること

