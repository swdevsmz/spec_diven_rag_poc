# Spec-Driven RAG PoC

## 概要

- 仕様駆動開発（Specification-Driven Development）と GitHub Copilot を活用した RAG（Retrieval-Augmented Generation）を活用したAIチャットボットの PoC プロジェクト。
- 仕様駆動開発とRAGを学ぶにあたりRAGを活用したAIチャットボットの構築をPoCで行います。
- RAGにはベクターDBのChromaDBを使います。単純にノウハウをテキストデータでAIにInputするのとベクターDBを利用する場合との違いを明確化します。

## 特徴

- **仕様駆動**: 曖昧さを排除し、AI による無駄なアウトプットを削減
- **GitHub Spec Kit**: 仕様から実装までの段階的な流れをサポート
- **GitHub Copilot 統合**: スラッシュコマンドによる構造化ワークフロー
- **DevContainer**: Windows + Docker + WSL2 でチーム全体が同じ環境を共有

## 環境構成

```text
Windows 11
└─ WSL2 (Debian)
    ├─ Docker
└─ DevContainer
    ├─ Python 3.11+
    ├─ uv（パッケージマネージャー）
    ├─ GitHub Spec Kit (specify-cli)
    ├─ GitHub Copilot
    └─ Development Tools
          ├─ git
          ├─ github-cli
          └─ vscode

VS Code と拡張機能（ホスト側）
├─ VS Code
├─ Dev Containers 拡張機能

VS Code 拡張機能（DevContainer内で自動インストール）
├─ GitHub Copilot（GitHub.copilot）
├─ GitHub Copilot Chat（GitHub.copilot-chat）
├─ Python（ms-python.python）
├─ Pylance（ms-python.vscode-pylance）
├─ Makefile Tools（ms-vscode.makefile-tools）
└─ Ruff（charliermarsh.ruff）

### GitHub Copilot CLI (`gh copilot`)
- 説明: この DevContainer では `gh` に `copilot` コマンドが組み込まれており、初回実行時に Copilot CLI がダウンロードされます（保存先: `/home/vscode/.local/share/gh/copilot`）。
- 認証: 事前にコンテナ内で `gh auth login` を実行してください。
- 基本コマンド例:
  - `gh copilot`                 # 最初のダウンロード + 実行
  - `gh copilot --remove`        # ダウンロード済み CLI を削除
  - `gh copilot -p "<prompt>"`  # 例: `gh copilot -p "Summarize README.md"`
- 備考: `.devcontainer/post-create.sh` は `gh-copilot` 拡張のインストールを試みますが、`gh` が既に `copilot` コマンドを提供している場合は拡張の追加インストールは不要です。
```

## 環境構築

### Step 1: WSL2（Debian）のインストール
- Windows 11 上で WSL2 を有効化
- Debian ディストリビューションをインストール
  ```bash
  wsl --install --distribution Debian
  ```

### Step 2: VS Code と拡張機能のインストール
- VS Code をインストール
- 以下の拡張機能をインストール：
  - Dev Containers（ms-vscode-remote.remote-containers）

### Step 3: リポジトリのクローンと DevContainer 起動

- WSL2（Debian）上にこのリポジトリをクローン
- VS Code でプロジェクトを開く
- コマンドパレット（Ctrl+Shift+P）から Dev Containers: Reopen in Container を選択
- DevContainer が起動し、post-create.sh が自動実行される
- 起動確認
  - DevContainer内で以下を実行してセットアップを確認：
    ```bash
    specify check
    ```

## 仕様駆動開発の実施
TODO