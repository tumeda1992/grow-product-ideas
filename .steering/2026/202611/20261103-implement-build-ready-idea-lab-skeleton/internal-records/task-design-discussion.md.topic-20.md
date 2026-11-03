# 内部検討記録: 論点20 — 問いに答える手順をskillにし、層skill4種との関係をどうするか

**discussion:** [task-design-discussion.md](../task-design-discussion/task-design-discussion.md)

**論点:** 論点20

## 開始context

論点18で`answering.md`はskillだと判断した。共通手順を共有する層skill4種が何を足しているかを確かめる。

<a id="iteration-0"></a>

## イテレーション0: 層skillが共通手順に何を足しているか

<a id="iteration-0-record-1"></a>

### 調査: 層skill4種の中身と層fileの重複

作成した`answer-*/SKILL.md`4種を読み、共通手順への参照を除いた中身を、層fileと照合した。

- 「材料を取りに行く順序」の表: 各問いの「必要な材料」の並びとほぼ同じ。足しているのは理由の一行（例: 声から痛みを作らない、ラフ画は粗くてよい）。
- 「落とし穴」: 多くが層fileの水準の満たさない例と重複。例: `answer-why-to-build`の「『競合はいない』『リスクはない』で終える」は`why-to-build.md`の満たさない例。`answer-how-to-build`の「テーブルを画面ごとに作る」は`how-to-build.md`のテーブルの満たさない例。
- 重複しないものの例: `answer-why-to-build`の「作りたい動機や楽しみを費用の比較に混ぜる」（`why-to-build.md`の定石の判断軸に近い記述はある）、`answer-how-to-build`の「心臓部のロジックをテーブルやモジュールの後に考える」（`how-to-build.md`の材料の並びで表現できる）。

### 判断

前回designの歯止め「参照先も手順も既に確定していてskillが何も足さないなら立てない」に照らすと、層skill4種は共通手順を除けば層fileの繰り返しに近い。

- a: 共通skillを作り層skillが起動する。skill一覧を保つが、層skillは渡すだけになり、重複も残る。
- b: 一つにまとめ、層ごとの内容を層fileへ移す。重複が無くなり起動の段も減る。前回designのskill一覧と論点2・7・8を変える。

推奨はb。論点4で前回designは仮説として扱うと決めている。
