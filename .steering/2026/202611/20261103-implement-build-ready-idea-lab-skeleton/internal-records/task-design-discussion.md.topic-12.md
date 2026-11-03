# 内部検討記録: 論点12 — build-readyの`product-plans/<slug>/`を、後続のリポジトリで読み切れる状態にする方法

**discussion:** [task-design-discussion.md](../task-design-discussion/task-design-discussion.md)

**論点:** 論点12

## 開始context

論点1の再開で、終了状態に「build-readyなら`product-plans/<slug>/`を新しいリポジトリへ持っていき、そのまま初回構築を始められる」を加えた。後続のリポジトリには`what-defines-a-product/`もこのリポジトリのskillも無いため、directoryの中だけで読み切れ、後続の`steering`／`task-design`がdirectoryの外へ問い合わせずに初回構築へ着手できる必要がある。満たし方を別論点にしていた。

関連する既決事項:

- 論点7: 層skillは水準を作る時の目標にし、書いた後に同じ水準で漏れを確認する。品質は作る段階で担保し、確認は漏れを拾う。出口判定は全体制御skill。
- 論点9・10: 正本の名前と構成、材料の入口は仮置きで、全体制御skillのテンプレート一箇所で定める。決定過程は`discussion.md`。
- 前回designの四層: なぜ作るか、何を作るか（スコープの内と外）、どこまで作るか（最初に作る分の区切り、AIへ自走させる範囲）、どう作るか（体験、画面構成、テーブル構成、モジュール構成）。

<a id="iteration-0"></a>

## イテレーション0: 読み切れる状態をいつ、誰が作るか

<a id="iteration-0-record-1"></a>

### 調査: directoryの外へ依存しうるもの

`product-plans/<slug>/`の中身が、directoryの外へ依存しうる箇所を、論点7・9・10の決定から列挙した。

- 正本の問い: 問いの文面を`what-defines-a-product/`への参照だけで書くと、後続では読めない。
- 正本・`discussion.md`・材料のlink: directoryの外（`what-defines-a-product/`、skill、他のproduct-plans）へのlinkは後続で切れる。
- 定石や水準への言及: 「定石Aを採った」とだけ書くと、定石の中身が`what-defines-a-product/`にしか無い。
- 材料の付随file: `materials/<識別子>/`の中に閉じていれば問題ない。

<a id="iteration-0-record-2"></a>

### 判断: 作る時から読み切れるように書くか、build-ready時に整える工程を足すか

- 作る時から書く: 論点7の「品質は作る段階で担保し、確認は漏れを拾う」と同じ形になる。層skillが答えを書く時点で、問いの文面と、採った選択肢の中身を正本・`discussion.md`に書き、directoryの外へlinkしない。出口判定でbuild-readyとする時に、全体制御skillが外へのlinkが無いことを確認して漏れを拾う。
- build-ready時に整える工程を足す: 作る時は参照で済ませ、build-ready時に全体制御skillが外への参照を展開して写しを作る。作る段階を緩めて後で補う形であり、論点7で退けた形になる。また、出口が作らない・保留のdirectoryは整えられず、判断記録として読みにくくなる。

推奨は前者。出口に関わらず、どの`product-plans/<slug>/`も単独で読める判断記録になる。

後続が初回構築へ着手できるかについては、四層の答え（スコープの内と外、最初に作る分の区切り、体験・画面・テーブル・モジュール）がそのまま初回構築の入力になる。別の要約documentを足すかは、自演で着手しにくさが見えた時に判断する。
