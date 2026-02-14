# Spec-Driven RAG PoC

## 概要

仕様駆動開発（Specification-Driven Development）と GitHub Copilot を活用した RAG（Retrieval-Augmented Generation）の PoC プロジェクト。

## 特徴

- **仕様駆動**: 曖昧さを排除し、AI による無駄なアウトプットを削減
- **GitHub Spec Kit**: 仕様から実装までの段階的な流れをサポート
- **GitHub Copilot 統合**: スラッシュコマンドによる構造化ワークフロー
- **DevContainer**: Windows + Podman + WSL2 でチーム全体が同じ環境を共有

## 環境構成

```text
Windows 11
├─ Podman Desktop
└─ WSL2 (Debian)
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
└─ Podman Desktop

VS Code 拡張機能（DevContainer内で自動インストール）
├─ GitHub Copilot（GitHub.copilot）
├─ GitHub Copilot Chat（GitHub.copilot-chat）
├─ Python（ms-python.python）
├─ Pylance（ms-python.vscode-pylance）
├─ Makefile Tools（ms-vscode.makefile-tools）
└─ Ruff（charliermarsh.ruff）
```

## 環境構築

### Step 1: DevContainer セットアップスクリプト
- [.devcontainer/post-create.sh](.devcontainer/post-create.sh) - uv と Specify CLI の自動インストール

### Step 2: DevContainer 設定
- [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json) - Python 3.11 ベースイメージ、Spec Kit 関連拡張機能の有効化

### Step 3: VsCodeでDevContainerの起動

## 仕様駆動開発の実施

### Step 1: Spec Kit ガバナンス
- [.speckit/constitution.md](.speckit/constitution.md) - プロジェクト原則と開発方針
- [.speckit/config.yaml](.speckit/config.yaml) - Spec Kit メタデータ設定

1. DevContainer 起動確認
   ```bash
   specify check
   ```

2. GitHub Copilot Chat で仕様定義開始

VS Code 内で Ctrl+Shift+i で Copilot Chat を起動
/speckit.constitution で憲法を確認
/speckit.specify で実装要件の定義を開始
仕様・計画ドキュメントを specs/ に保存

プロジェクト構成

```text
.
├── .devcontainer/
│   ├── devcontainer.json              # DevContainer 設定
│   ├── post-create.sh                 # セットアップスクリプト
│   └── [README.md](http://_vscodecontentref_/0)                      # DevContainer ガイド
│
├── .speckit/
│   ├── constitution.md                # プロジェクト原則
│   └── config.yaml                    # Spec Kit 設定
│
├── specs/                             # 仕様・計画ドキュメント
│   └── [Step 5で作成]
│
└── [README.md](http://_vscodecontentref_/1)                          # このファイル
```