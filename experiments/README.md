# Experiments

このディレクトリは実験ログの保存と再現性確保のために使用します。

## 使い方

- 実験ログは JSON Lines 形式で `experiments/` 配下に保存します。
- 実験の再現手順は以下の形式で記録します。

## 再現手順テンプレート

```text
1. 実行日時: YYYY-MM-DD HH:MM
2. 実行コマンド:
3. 使用モデル: 生成モデル / 埋め込みモデル
4. 主要パラメータ: temperature, max_tokens, top_k, chunk_size, chunk_overlap
5. 入力データ: ドキュメント一覧 / 評価セット
6. 出力ファイル: logs/ のパス
7. 結果の要約:
```
