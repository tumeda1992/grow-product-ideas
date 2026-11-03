# 内部検討記録: 論点14 — 作る順（`what-defines-a-product/README.md`をいつ確定させるか）

**discussion:** [task-design-discussion.md](../task-design-discussion/task-design-discussion.md)

**論点:** 論点14

## 開始context

design.mdの作る順は、assistantが決定済みの事項（論点3の「問いの中身を先、それを使うskillを後」）から導いて書き、1番目を`what-defines-a-product/README.md`にしていた。論点13の見出し構成に合意した利用者から、「ここから決まるのか、skillが決まった後に取りまとめる輪郭が決まるのか。今ほぼ内容無い」という問いがあった。

<a id="iteration-0"></a>

## イテレーション0: 取りまとめる輪郭は、先に決まるか後で決まるか

<a id="iteration-0-record-1"></a>

### 判断: このfileの中で、先に要るものと後で決まるものを分ける

論点13の見出しを、層file・skillとの依存で分けた。

| 見出し | 層file・skillとの関係 | 決まる時期 |
| --- | --- | --- |
| 問いの書き方（一つの問いが持つもの、identifier、水準、定石、粒度） | 層fileが従う形式 | 先に要る |
| 材料の識別子 | 層fileの問いと材料skillが使う | 先に要る |
| 冒頭の説明、四つの層、問いの選び方、粒度と再利用、問いを足す・削る基準 | 前回designの記述と、層file・skillを読む人のための案内 | 層file・skillが出来て合っているかを確かめられる |

先に要るものを後回しにすると、層fileとskillを書き直すことになる。後で決まるものを先に確定させても、実物と合っているかを確かめられない。前者を最初に書き、後者は前回designの内容で仮に書いて、最後の段で見直して確定させる。
