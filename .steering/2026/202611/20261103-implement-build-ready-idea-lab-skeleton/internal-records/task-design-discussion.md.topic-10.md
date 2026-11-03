# 内部検討記録: 論点10 — 材料の識別と`materials/`の中の置き方

**discussion:** [task-design-discussion.md](../task-design-discussion/task-design-discussion.md)

**論点:** 論点10

## 開始context

前回designは、各問いがそれを閉じるために必要な材料を定義し、水準の一段目で「問いに定義された必要材料が`materials/`に存在するか」を機械的に判定するとしている。論点7で、一段目は全体制御skillが見ると決めた。

一段目を機械的に判定するには、次の三者が同じ識別子で材料を指す必要がある。

- 問い（`what-defines-a-product/`の層file）: 必要な材料を挙げる
- 材料skill: 材料を作り、`materials/`へ置く
- 全体制御skill: 問いが挙げた材料が`materials/`にあるかを見る

この識別子は複数fileにまたがる契約であり、各fileの中身を作る前に決める必要がある。

前回designの関連記述:

- 材料は層を跨いで再利用され、一度作れば要求した全ての問いへ供給される
- 材料の粒度は要求元の問いが決め、材料は一度作って完成ではなく要求元が求める粒度まで作る
- ラフ画、技術検証のように、md以外のfile（画像、code）を伴う材料がある

論点9で、正本の配置は全体制御skillのテンプレート一箇所で定め、仮置きにした。

<a id="iteration-0"></a>

## イテレーション0: 材料の識別子と置き方

<a id="iteration-0-record-1"></a>

### 判断: 材料の種類と材料skillを一対一にするか

材料skillは8種あり、それぞれが一種類の材料を作る（前回designのskill一覧）。材料の種類を材料skillと一対一にすれば、問いが挙げた材料から作るskillが一意に決まり、層skillが起動するskillを迷わない。

識別子は材料skill名の目的語を名詞形にしたものとする。

| 材料skill | 材料の識別子 |
| --- | --- |
| `find-existing-alternatives` | `existing-alternatives` |
| `compare-build-and-alternative-costs` | `cost-comparison` |
| `gather-target-user-voices` | `target-user-voices` |
| `sketch-experience` | `experience-sketch` |
| `design-core-logic` | `core-logic` |
| `design-tables` | `tables` |
| `design-modules` | `modules` |
| `verify-technical-feasibility` | `technical-feasibility` |

<a id="iteration-0-record-2"></a>

### 判断: `materials/`の中の置き方

- 一つの材料は一つの入口file `materials/<識別子>.md`を持つ。一段目はこのfileがあるかを見る。
- 画像、code等を伴う材料は、付随fileを`materials/<識別子>/`に置き、入口fileから参照する。
- 材料は要求元の問いが求める粒度まで同じ入口fileを育てる。粒度ごとに別fileを作らない。前回designの「一度作れば要求した全ての問いへ供給される」と合う。

材料の識別子の一覧の正本は、問いを定義する`what-defines-a-product/README.md`に置く。層fileの問いはこの識別子で必要な材料を挙げ、材料skillは自分の識別子を名乗る。

<a id="iteration-1"></a>

## イテレーション1: 材料をdirectory単位にし、結論・材料・決定過程の置き場所を分ける

入口は利用者の応答である。材料が1fileになるかは不明。議論や決定過程はどこに置くか。

<a id="iteration-1-record-1"></a>

### 調査: 決定過程の置き場所について前回designと既存skillが決めていること

#### 確認先と結果

- 前回designのプロダクト1件のディレクトリ: `discussion.md`は「議論の変遷」。正本は問いごとに答え、水準を満たしたか、根拠の材料への参照を持つ。
- 前回designの既存plugin接続: 再利用するものに`facilitate-discussion`（議論の記録）がある。
- `facilitate-discussion`の`SKILL.md`: ユーザーへ提示する前に提案を保存し、決定には具体案と明示合意の証拠を要する。実論点が10件を超えると範囲fileへ分割する（`split-discussion.md`）。
- 論点7: ユーザー確認gateは層の閉じと出口判定に置く。

#### 解釈

決定過程の置き場所は前回designで`discussion.md`と決まっているが、何をそこへ書き、正本とどう分けるかは決まっていない。`facilitate-discussion`の合意モデルは、層の閉じのgateと噛み合う。

<a id="iteration-1-record-2"></a>

### 判断: 置き場所の分け方

- 結論: 正本（論点7で状態の唯一の置き場所）
- 材料: `materials/<識別子>/`。生成系の複数案は材料そのもの
- 決定過程: `discussion.md`。問いごとに論点を立て、層skillが提案として保存し、層の閉じのgateで利用者が応答して決定になる
- 材料もdirectory単位にし、入口`README.md`を仮置きにする（論点9と同じ扱い）

代償: 層skillが答えるたびに`facilitate-discussion`の手順を通るため重い。前回designが再利用を決めていること、還元時に過程を辿れる必要があることから受け入れる。

<a id="iteration-1-record-3"></a>

### 記録: 議論記録の分割

論点10の決定後、次の論点の追加で実論点が10件を超えるため、`facilitate-discussion`の分割手順で`task-design-discussion.md`を`task-design-discussion/`（索引`task-design-discussion.md`、範囲`task-design-discussion-1-5.md`、`task-design-discussion-6-10.md`）へ移した。

- 分割前のsnapshotを取り、`check-candidate`で件数・番号・順序・所属・親子・索引と、href以外の原文一致を確認した。problemsは0件。
- href差は18件で、すべて`internal-records/`→`../internal-records/`、`pending-escalations/`→`../pending-escalations/`の移動に必要な変更である。
- 分割前の原文fileが保存した控えと一致することを確認してから除去した。
- 外部からの参照は、内部logの`**discussion:**`行を同名索引へ、保留メモの論点7への参照を`task-design-discussion-6-10.md`へ追随させた。
- 除去後、`resolve`がsplitを返し、`check`のproblemsが0件、steering directory内のmd相対linkに切れがないことを確認した。
