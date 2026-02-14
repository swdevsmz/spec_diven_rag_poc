<!--
Sync Impact Report

- Version change: template -> 0.1.0
- Modified principles:
	- [template placeholders] -> 目的, 最優先, 評価, セキュリティ, スコープ, 制約
- Added sections: 追加制約 (Section 2), 開発ワークフロー (Section 3)
- Removed sections: none
- Templates inspected: ✅ .specify/templates/plan-template.md (inspected)
											✅ .specify/templates/spec-template.md (inspected)
											✅ .specify/templates/tasks-template.md (inspected)
											✅ .github/prompts/speckit.constitution.prompt.md (present)
											✅ .github/agents/speckit.constitution.agent.md (present)
- Follow-up TODOs: none
-->

# プロジェクト憲章

## Core Principles

### 目的 (Purpose)
仕様駆動で RAG を使ったチャットボットを構築し、仕様駆動開発と RAG の理解を深める。RAG と非RAG の差分は教育的に比較・検証し、知見をドキュメント化することを目的とする。

### 最優先: 再現性と可視化 (Top priority: Reproducibility & Visibility)
すべての実験・実装は再現可能であることを最優先とする。実施した手順、入力データ、環境、得られた結果、その解釈を後から説明できるように記録・可視化しなければならない。

### 評価 (Evaluation)
RAG と Non-RAG の比較は必ず定量的指標と定性的評価の両面で実施する。仕様駆動プロセスの理解度とドキュメントの網羅性を検証基準として定義し、測定可能な成功基準を明記すること。

### セキュリティ (Security)
シークレットや機密情報をリポジトリに埋め込んではならない。秘密情報は環境変数や安全なシークレット管理ツールで管理し、設定手順を `README` または `docs/` に記載すること。

### スコープ (Scope)
教育・検証を最優先とし、MVP を短期間で反復することを優先する。商用品質や運用耐久性は段階的に導入するが、最初のフェーズでは学習と検証にフォーカスする。

### 制約 (Constraints)
作成するドキュメントは原則として日本語で記述する。例外がある場合は明示的に理由を記載し、レビューで承認を受けること。

## 追加制約
- 成果物の README と主要ドキュメントは日本語で書き、英訳が必要な場合は別ファイルにする。
- 実験データや環境は `experiments/` または `data/` に整理し、再現手順を `experiments/README.md` に残す。

## 開発ワークフロー
- `specify` → `plan` → `tasks` → `implement` の 5 フェーズを順守すること。各フェーズでの成果物（spec, plan, tasks, implementation）をリポジトリに保存すること。
- すべてのプルリクエストは対応する `spec` または `plan` へのリンクを含め、憲章の `Constitution Check` を満たしていることを示す必要がある。

## Governance
- この憲章はプロジェクトの最上位方針とする。憲章の変更は以下の手順を MUST とする:
	1. 変更案を含む PR を作成し、変更理由と Sync Impact Report を PR 説明に含めること。
	2. 少なくともプロジェクトのメンテナ（1 名以上）によるレビューとマージ承認を得ること。
	3. マージ時に `Last Amended` を更新し、バージョン規則に従って `CONSTITUTION_VERSION` をインクリメントすること。
- バージョン規則:
	- MAJOR: 既存の原則（非互換）を削除または再定義する場合
	- MINOR: 新しい原則や主要セクションを追加する場合
	- PATCH: 文言の明確化、誤字訂正、小さな整備のみ
- コンプライアンスレビュー: 重要な設計変更やセキュリティ影響がある変更は、関連する `plan` と `tasks` テンプレートの `Constitution Check` を通じて検証を受けること。

**Version**: 0.1.0 | **Ratified**: 2026-02-14 | **Last Amended**: 2026-02-14
