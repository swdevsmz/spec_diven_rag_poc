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
└─ VS Code + Dev Containers 拡張機能
    └─ WSL2 (Debian)
        └─ Docker
            └─ DevContainer
                ├─ Python 3.11+
                ├─ uv（パッケージマネージャー）
                ├─ GitHub Spec Kit (specify-cli)
                ├─ GitHub Copilot
                └─ Development Tools
                      ├─ git
                      ├─ github-cli (gh)
                      └─ Node.js 24

VS Code 拡張機能（ホスト側 Windows）
├─ Dev Containers（ms-vscode-remote.remote-containers）

VS Code 拡張機能（DevContainer 内で自動インストール）
├─ GitHub Copilot（GitHub.copilot）
├─ GitHub Copilot Chat（GitHub.copilot-chat）
├─ Python（ms-python.python）
├─ Pylance（ms-python.vscode-pylance）
├─ Makefile Tools（ms-vscode.makefile-tools）
└─ Ruff（charliermarsh.ruff）
```

### GitHub Copilot CLI (`gh copilot`)
- 説明: この DevContainer では `gh` に `copilot` コマンドが組み込まれており、初回実行時に Copilot CLI がダウンロードされます（保存先: `/home/vscode/.local/share/gh/copilot`）。
- 認証: 事前にコンテナ内で `gh auth login` を実行してください。
- 基本コマンド例:
  - `gh copilot`                 # 最初のダウンロード + 実行
  - `gh copilot --remove`        # ダウンロード済み CLI を削除
  - `gh copilot -p "<prompt>"`  # 例: `gh copilot -p "Summarize README.md"`
- 備考: `.devcontainer/post-create.sh` は `gh-copilot` 拡張のインストールを試みますが、`gh` が既に `copilot` コマンドを提供している場合は拡張の追加インストールは不要です。

## 環境構築

### Step 1: VS Code と拡張機能のインストール
- Windows 11 に VS Code をインストール
- 以下の拡張機能をインストール：
  - **Dev Containers**（ms-vscode-remote.remote-containers）

### Step 2: WSL2（Debian）のインストール
- `wsl_setup_scripts/wsl_debian_install.ps1` をローカル PC にダウンロード
- PowerShell（管理者権限）でスクリプトを実行
  ```powershell
  .\wsl_debian_install.ps1
  ```
- スクリプトが Debian をインストールし、初回起動時にユーザー名とパスワードの設定を求めます。

### Step 3: リポジトリのクローン（WSL 内）
- WSL（Debian）内でこのリポジトリをクローン
  ```bash
  cd ~
  git clone https://github.com/swdevsmz/spec_diven_rag_poc.git
  cd spec_diven_rag_poc
  ```

### Step 4: Docker のインストール（WSL 内）
- WSL（Debian）内で `wsl_docker_install.sh` を実行
  ```bash
  bash wsl_setup_scripts/wsl_docker_install.sh
  ```
- スクリプト完了後、一度 WSL から `exit` で抜けて、PowerShell で `wsl --shutdown` を実行してください。

### Step 5: DevContainer の起動
- VS Code で WSL 内のリポジトリを開く
  - VS Code のコマンドパレット（Ctrl+Shift+P）から **WSL: Connect to WSL** を選択
  - WSL 接続後、`~/spec_diven_rag_poc` フォルダを開く
- コマンドパレット（Ctrl+Shift+P）から **Dev Containers: Reopen in Container** を選択
- DevContainer が起動し、`.devcontainer/post-create.sh` が自動実行されます。
- 起動確認
  - DevContainer 内で以下を実行してセットアップを確認：
    ```bash
    specify check
    ```

## 仕様駆動開発の実施

以下はこのリポジトリでの仕様駆動（Spec-Driven Development）を実践するための手順です。短期的なワークフロー、主要コマンド、および PR 作成時のチェックリストを含みます。

1. 前提確認（DevContainer 内）
- DevContainer 内で以下を実行してツールが利用可能か確認します:
  - specify check
  - gh --version
  - gh auth login  # 必要に応じて認証を行ってください

2. 仕様（Spec）の作成
- `specs/` ディレクトリを作成し、各機能について Markdown 形式で Spec を追加します（例: `specs/feature-x.spec.md`）。
- 各 Spec に含める項目:
  - 目的
  - ユーザーストーリー
  - 受け入れ基準（Acceptance Criteria）
  - 検証方法（対応するテストや手順）

3. Issue の作成（gh）
- Spec を書いたら対応する Issue を作成し、Spec へのリンクを含めます:
  - gh issue create --title "Spec: feature-x" --body "See specs/feature-x.spec.md" --label spec

4. ブランチ作成と実装
- ブランチ命名例: `spec/feature-x` または `feat/spec-feature-x`
  - git checkout -b spec/feature-x
- 実装は Spec の受け入れ基準に従って行います。

5. ローカル検証
- 仕様に記載した検証方法に従いテスト・検証を行います。例:
  - specify check
  - pytest tests/test_feature_x.py

6. PR 作成（必須: Spec へのリンク）
- PR を作成する際、本文に Spec へのリンクと受け入れ基準を必ず含めてください:
  - gh pr create --title "Implement feature-x (spec)" --body "Spec: specs/feature-x.spec.md\nAcceptance: ..." --base main
- `.github/PULL_REQUEST_TEMPLATE.md` を利用して Spec のリンクを必須化しています。

7. レビューとマージ
- レビューでは以下を必ずチェックしてください:
  - 仕様の各受け入れ基準が満たされていること
  - テストが通っていること
  - Spec へのリンクが正しいこと
- マージ例:
  - gh pr merge <pr-number> --merge --delete-branch

8. 仕様の更新ルール
- 既存の Spec を変更する場合は Spec ファイルを更新し、変更点を Issue と PR に明記してください。
- 大きな仕様変更は新しいバージョンの Spec ファイルとして管理してください（例: `feature-x.v2.spec.md`）。

短いチェックリスト（PR 作成前）
- [ ] Spec ファイルが `specs/` に存在する
- [ ] Issue が作成されている/紐付いている
- [ ] ブランチ名が規約に従っている
- [ ] テストが通る（または必要なテストが追加されている）
- [ ] PR 本文に Spec へのリンクと受け入れ基準が含まれている

自動化の推奨
- GitHub Actions に `specify check` を組み込み、PR ごとに環境チェックを実行することを推奨します（既に `.github/workflows/specify-check.yml` を追加済み）。

