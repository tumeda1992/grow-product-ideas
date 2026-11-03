# 内部検討記録: 論点13 — `what-defines-a-product/README.md`の見出し構成

**discussion:** [task-design-discussion.md](../task-design-discussion/task-design-discussion.md)

**論点:** 論点13

## 開始context

接合面の論点（論点1〜12）が決まり、design.mdの作る順の1番目が`what-defines-a-product/README.md`である。論点3で、各fileは見出し構成と各見出しの内容を合意してから作り、作った実fileをreviewすると決めた。

design.mdの知識体系の節が定めるこのfileの役割:

- 問いのセットの引き方
- 層の関係（答えの依存方向と材料の供給方向）
- 問いを選ぶ基準
- 粒度の判定基準
- 材料の識別子の一覧（論点10）

<a id="iteration-0"></a>

## イテレーション0: 見出し構成

<a id="iteration-0-record-1"></a>

### 判断: このfileに置くものと置かないもの

読む人は、層skill（答えを作る・確認する時に問いの形式と水準の扱いを知る）、全体制御skill（次の問いを選ぶ、一段目を確かめる）、還元skill（問いを足す・削る）、利用者である。

前回designとこれまでの論点から、四層file全てに共通し、どの層fileにも属さない内容をここへ置く。

- 層と閉じ条件、答えの依存と材料の供給（前回designの「問いは四つの層を持つ」「答えの依存と材料の供給は方向が逆である」）
- 問いの選び方（前回designのworkflow手順3）
- 層fileの共通形式: 一つの問いが持つもの、水準（論点7: 作る時の目標と確認の基準を兼ねる）、定石（前回designの「選択肢と判断軸の形」「個人開発へ翻訳してから載せる」）、粒度（三属性を持てる単位）
- 材料: 識別子の一覧（論点10）、粒度と再利用（前回design）
- 問いを足す・削る基準（前回designの「載せる・載せない」「網羅しない」、論点4の働き）。還元skillが使う

置かないもの:

- 各層の問いの中身（層fileが正本）
- 答えを作る・確かめる手順（層skill、全体制御skillが正本）
- `product-plans/<slug>/`の配置（全体制御skillのテンプレートが正本、論点9）

<a id="iteration-0-record-2"></a>

### 判断: 問いのidentifierの形

論点12で、正本の各問いに「問いのidentifierだけでなく問いの文面」を書くと決めた。identifierの形はまだ決まっていない。正本、`discussion.md`の論点、還元skillが問いを指すために要る。

- 形: `<層file名>/<問いのslug>`（例: `why-to-build/cheaper-alternative-exists`）。層をまたいで一意になり、どの層fileにあるかが読める。
- 層fileの中では、各問いの見出しにidentifierを添える。
- identifierは問いの文面を言い換えても変えない。還元で問いを統合・分割した時は新しいidentifierにする。過去の`product-plans/<slug>/`が古いidentifierを指していても、正本に文面があるため読める（論点12）。
