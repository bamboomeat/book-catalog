# book-catalog

Obsidian vault「Helloworld / 01_Inbox / BookSummary」にある書籍分析ノート283件を、検索・分類フィルタ・ブログ化進捗トラッキングができる1枚のHTMLカタログにまとめたもの。

## 構成

```
book-catalog/
├── build.py              # data/books.json から dist/book_catalog.html を生成するビルドスクリプト
├── data/
│   ├── books.json        # 書籍データ（title / author / date / category / summary / id）
│   └── book_catalog_source.md   # 生成元のMarkdown一覧表（参考用）
└── dist/
    └── book_catalog.html # 生成された成果物。ブラウザで直接開けば動く
```

## 使い方

```bash
python3 build.py
```

`dist/book_catalog.html` が再生成される。ブラウザで直接開けば動作する（外部依存なし、単一HTMLファイル）。

## データを編集する

`data/books.json` を編集して `python3 build.py` を再実行すれば、カタログに反映される。各レコードの `id` はブログ進捗（後述）のキーとして使われるため、既存レコードの `id` は変更しないこと。新規追加時は連番の続きなど、既存と重複しない値を振ること。

## ブログ化進捗トラッキング

`dist/book_catalog.html` には「作成済」チェックボックスと「作成日」欄があり、チェックすると自動で当日の日付が入る。

- 進捗はブラウザの `localStorage`（キー: `bookCatalogProgress_v1`）に保存される。**ブラウザ・端末をまたいで同期はされない。**
- ページ内の「進捗をエクスポート」「進捗をインポート」ボタンでJSONバックアップの書き出し・復元ができる。
- Claude.ai の Artifact 版（`window.claude.use("downloads")` 経由）ではダウンロード確認ダイアログが出るが、ローカルでブラウザから直接開いた場合はブラウザ標準のダウンロードとして保存される。

## 由来

- Claude Code のセッションで、Obsidian vault内の書籍分析ノートを並列サブエージェントで解析し、タイトル/著者/発行日/分類/概要を抽出して生成した。
- Claude.ai の Artifact としても公開済み（同じ `dist/book_catalog.html` の内容）。
