# book-catalog

Obsidian vault「Helloworld / 01_Inbox / BookSummary」にある書籍分析ノート283件を、検索・分類フィルタ・ブログ化進捗トラッキングができる1枚のHTMLカタログにまとめたもの。GitHub Pagesで公開し、進捗（ブログ化チェック・作成日）はGitHubリポジトリ内のJSONファイルに保存されるため、どの端末・ブラウザからアクセスしても同じ進捗が見える。

## 構成

```
book-catalog/
├── build.py              # data/*.json から docs/index.html を生成するビルドスクリプト
├── data/
│   ├── books.json        # 書籍データ（title / author / date / category / summary / id）— ほぼ固定
│   ├── progress.json     # ブログ化進捗（id ごとの done / date）— アプリから直接更新される
│   └── book_catalog_source.md   # 生成元のMarkdown一覧表（参考用）
└── docs/
    └── index.html         # 生成された成果物。GitHub Pagesの公開対象
```

## セットアップ（GitHub Pagesで公開する）

1. このリポジトリをGitHub上に作成し、push する。
   ```bash
   git remote add origin https://github.com/bamboomeat/book-catalog.git
   git push -u origin main
   ```
2. GitHubのリポジトリ画面で **Settings → Pages** を開き、Source を「Deploy from a branch」、Branch を「main」「/docs」に設定する。
3. しばらくすると `https://bamboomeat.github.io/book-catalog/` でカタログが閲覧できるようになる（URLを知っている人なら誰でも閲覧可能。検索エンジンには積極的にインデックスされない）。

閲覧だけならここまでで完了。書籍データや概要はページを開くだけで見える。

## 進捗を更新できるようにする（どの端末からでも）

進捗（作成済みチェック・作成日）の更新は、ページから直接 GitHub の `data/progress.json` にコミットする形で反映される。更新するには書き込み権限を持つトークンが必要。

1. GitHubで **Settings → Developer settings → Personal access tokens → Fine-grained tokens** から新規トークンを作成する。
   - Repository access: `book-catalog` のみに限定
   - Permissions: **Contents = Read and write**
2. カタログ画面右上の「⚙ GitHub連携設定」からトークンを貼り付けて保存する。
   - トークンはそのブラウザの `localStorage` にのみ保存され、GitHub以外には送信されない。
   - 別の端末・別のブラウザで更新したい場合は、その端末でも同じ手順でトークンを設定する（トークン自体は自動同期されない）。
3. 設定後はチェックボックス・作成日入力がその場でGitHubにコミットされ、他の端末でページを開き直すと最新の進捗が反映される。

トークン未設定のブラウザではチェックボックス等は読み取り専用（無効化）になる。

## データを編集する

`data/books.json` を編集して `python3 build.py` を再実行し、`docs/index.html` の再生成後にコミット・pushすれば、カタログに反映される。各レコードの `id` はブログ進捗（`data/progress.json`）のキーとして使われるため、既存レコードの `id` は変更しないこと。新規追加時は連番の続きなど、既存と重複しない値を振ること。

## バックアップ

ページ内の「進捗をエクスポート」「進捗をインポート」ボタンで、`data/progress.json` とは別にローカルJSONファイルとしての書き出し・復元もできる（GitHub連携とは独立した保険用）。

## 由来

- Claude Code のセッションで、Obsidian vault内の書籍分析ノートを並列サブエージェントで解析し、タイトル/著者/発行日/分類/概要を抽出して生成した。
- もともとは単一HTML + ブラウザの `localStorage` で進捗管理していたが、端末をまたいだ同期ができなかったため、GitHub Pages + GitHubリポジトリへの直接コミット方式に移行した。
