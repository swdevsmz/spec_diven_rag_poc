# Spec Kit 次セッション引き継ぎガイド

このドキュメントは、次のセッションで GitHub Spec Kit を使い始める際の「最初の一歩」をサポートするガイドです。

## 現在の状態

✅ **準備完了**: 
- Spec Kit v0.0.95 が初期化済み
- テンプレートとスクリプトが `.specify/` に配置済み
- AI アシスタント: GitHub Copilot（copilot-sh）

❌ **未実施**:
- `/speckit.constitution` によるプロジェクト原則の確立
- `/speckit.specify` による仕様定義

## 次セッション開始ステップ（5分で完了）

### Step 1: 環境確認
DevContainer 内で以下を実行して環境が整っていることを確認：

```bash
specify check
```

### Step 2: VS Code で Copilot Chat を開く
1. VS Code のコマンドパレット（Ctrl+Shift+P）を開く
2. `Copilot: Focus on Chat View` を実行
3. チャットパネルが右側に開く

### Step 3: `/speckit.constitution` を実行
Copilot Chat に以下を貼り付けて実行：

```
/speckit.constitution

このプロジェクトは仕様駆動開発と RAG（Retrieval-Augmented Generation）を学ぶための PoC です。

開発原則:
- Python 3.11+、uv でパッケージ管理
- RAG システム: ChromaDB を使用したベクターストレージ
- AI チャットボット: FastAPI バックエンド、シンプルなフロント
- テスト重視: pytest による自動テスト必須
- シンプルさ優先: オーバーエンジニアリング回避、YAGNI 原則
- ドキュメント: 仕様駆動開発による明確な要件定義
```

Copilot が対話的に質問をしてくるため、曖昧な点は回答してください。

### Step 4: 結果確認
実行完了後、以下が自動生成されます：

```
.specify/memory/constitution.md  ← 更新される（プロジェクト原則が記載）
.specify/features/              ← 新規作成される可能性
```

## 次の Phase へ進むには

### Phase 2: Specify（要件定義）
Constitution が完成したら、以下を実行：

```
/speckit.specify

RAG を使った AI チャットボット PoC。ユーザーが質問すると、
事前に学習させたドキュメント（ベクターDB に保存）から関連情報を検索し、
その情報に基づいて AI が回答を生成する機能。

対比実装: テキスト直投入版も並行して実装し、
ベクターDB 活用による精度向上を検証する。
```

### Phase 3～5: Plan → Tasks → Implement
以降のフェーズは Phase 2 の完了後に README の「仕様駆動開発のワークフロー」を参照してください。

## 参考資料

### このリポジトリ内
- `README.md` - 全体概要と環境構築手順
- `README.md` セクション「仕様駆動開発のワークフロー」 - Spec Kit フロー説明
- `.github/copilot-instructions.md` - Copilot 向け指示書

### 公式資料
- [GitHub Spec Kit](https://github.com/github/spec-kit) - 公式リポジトリ
- [ClassMethod 実例記事](https://dev.classmethod.jp/articles/spec-driven-development-with-github-spec-kit/) - 実践例

## トラブルシューティング

### Q: `/speckit.constitution` が認識されない
**A**: 
- Copilot Chat が最新の状態か確認（拡張機能の更新）
- DevContainer 内で実行していることを確認
- `specify check` で環境が整っていることを確認

### Q: テンプレートがうまく埋まらない
**A**:
- Copilot Chat での対話に応じて詳しく説明してください
- ClassMethod 記事の例を参考に、より具体的な指示を与えてください

### Q: `.specify/` フォルダ内のファイルを編集してもいい？
**A**: 
- `constitution.md`: 編集可（Copilot との対話で更新）
- テンプレートファイル: 手動編集不要（Spec Kit が管理）
- スクリプトファイル: 変更不可（Spec Kit 依存）

## 進捗追跡

次セッション開始時に以下をチェックしてください：

- [ ] `specify check` で環境確認
- [ ] Copilot Chat を開く
- [ ] `/speckit.constitution` を実行
- [ ] `.specify/memory/constitution.md` が更新されたか確認
- [ ] 完了後、このドキュメントを更新（日付・進捗記録）

**最終更新**: 2026-02-14  
**準備状態**: ✅ 初期化済み、Phase 1 開始待ち
