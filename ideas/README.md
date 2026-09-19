# Ideas

一つのアイデアにつき `ideas/<kebab-case-slug>/` を一つ使う。`_template/` は雛形であり、検討対象には含めない。

新規作成:

```bash
./scripts/new-idea.sh <slug> "<title>" "<raw idea>"
```

第3引数を省略した場合はtitleをraw ideaとして保存する。各ディレクトリの `README.md` が現在地の入口であり、詳細の正本は同階層の `source.md`、`discovery.md`、`product.md`、`specification.md`、`handoff.md`、`retrospective.md` である。

アイデア間の優先順位は、各アイデアの判断が揃ってから比較する。粗いアイデアと build-ready なアイデアを同じ点数表へ入れて、見かけの精度を作らない。
