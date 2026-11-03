# 内部検討記録: 論点18 — 複数のskillが共通で使うfileの置き場所

**discussion:** [task-design-discussion.md](../task-design-discussion/task-design-discussion.md)

**論点:** 論点18

## 開始context

論点17の委託で、層skill4種の共通手順`answering.md`と材料skill8種の共通の約束`making-material.md`を、`.agents/skills/grow-product-idea/references/`に置いた。利用者から「referencesの場所について厳しく自己レビューして。共通で使われるものが1つのskillの中にあるってどう思う？」と問われた。

<a id="iteration-0"></a>

## イテレーション0: 自己レビュー

<a id="iteration-0-record-1"></a>

### 診断: 置き場所を決めた時の判断

#### 何を基準に置いたか

「全体制御skillはレールの入口で、テンプレートも持っている」という理由で、共有物の置き場所として流用した。誰が持ち主か、誰が誰に依存するかを確かめていない。置ける場所に置いた判断である。

#### 問題

- 持ち主と場所が一致しない。`answering.md`は層skillの手順、`making-material.md`は材料skillの約束であり、`grow-product-idea`はどちらも使わない。pathを見た人は`grow-product-idea`の持ち物だと読む。`grow-product-idea`を直す人が、層skillや材料skillの振る舞いを変えてしまう。
- 依存の向きが逆になる。`grow-product-idea`は層skillを起動する側であり、層skillは起動される側である。起動される側が起動する側の中身に依存すると、両方向の依存になる。
- 名前の仮置きと噛み合わない。skill名は暫定であり（論点8）、`grow-product-idea`の名前を変えると、12種のskillの参照が全て切れる。
- 中身の一部が既存の正本と重複している。`making-material.md`の「育て方」は、`what-defines-a-product/README.md`の「粒度と再利用」と同じ内容を持つ。置き場所を決める時に、既に書いた正本を確かめていない。

#### 同じ問題を持つもの

材料skillは`grow-product-idea/templates/material.md`の雛形と`layout.md`を使う。テンプレートを全体制御skillに置くことは論点9・10で決めたが、その時は「全体制御skillがdirectoryを作る」ことを理由にしており、材料skillも使うことを確かめていなかった。同じ依存の問題を持つ。

<a id="iteration-0-record-2"></a>

### 判断: 置き直し方

案:

1. どのskillにも属さない共有の置き場所を作り、`answering.md`、`making-material.md`、`layout.md`と雛形を移す。各skillはそこを参照する。持ち主が「レール全体」であることと場所が一致し、依存は全てのskillから共有の場所への一方向になる。
2. 共有をやめ、各skillへ書き写す。持ち主と場所は一致するが、層skill4か所・材料skill8か所の同期が要る。
3. 層skill4種を一つのskillへまとめ、層ごとの順序と落とし穴を層fileへ移す。共通手順の共有が不要になるが、前回designのskill一覧（層4）を変える大きな変更になり、この指摘の範囲を越える。

推奨は1。置き場所の名前は、中身を表す名前にする。`shared`や`common`は何でも入る名前になり、何も言わない（naming/core.md）。中身は「`product-plans/<slug>/`を作り、問いに答え、材料を作る時の、skillをまたぐ約束」であり、候補は`.agents/product-plan-conventions/`。

skillのloaderが`.agents/skills/`の下のskillでないdirectoryをどう扱うかは確かめていないため、`.agents/skills/`の外に置く。

重複は、`making-material.md`から「育て方」の内容を除き、`what-defines-a-product/README.md`の「粒度と再利用」を参照する形にする。

<a id="iteration-1"></a>

## イテレーション1: fileごとに約束かskillかを判断する

入口は利用者の応答「それぞれ個別で考えてほしい。conventionなのか、これ自体独自スキルなのか」。

<a id="iteration-1-record-1"></a>

### 判断: 約束かskillかの基準と、fileごとの結果

基準: 手順を持たず形と置き方を定めるものは約束。入力を受けて手順を実行し結果を返すものはskill（前回designの「無いとagentが参照先・手順を毎回自分で決めるか」）。

- `layout.md`: 約束。`product-plans/README.md`へ。dataの隣に置き、利用者も読む。
- `canonical.md`、`material.md`: 約束。`product-plans/templates/`へ。
- `making-material.md`: 約束だが、置き方（`layout.md`）、育て方（README「粒度と再利用」）、限界の書き方（`material.md`）と重複。残る「層skillが材料skillへ渡すもの」はREADMEの「材料」節へ。fileを無くす。
- `answering.md`: skill。層skill4種との関係が変わるため論点20へ。

提案0の`.agents/product-plan-conventions/`はagentだけが読む場所に見えるが、この約束は利用者も読むため、`product-plans/`に置く。

<a id="iteration-2"></a>

## イテレーション2: templatesの三つを、誰が使うかで分ける

入口は利用者の問い「元々templatesにあったものは、grow-product-idea/templatesのままでよいのでは。このskillでしか使わないのでは」。

<a id="iteration-2-record-1"></a>

### 調査: 各fileを参照しているskill

`.agents/skills/`の下で`grep -rln`を各file名で実行した。`material.md`は`making-material.md`の部分一致を除いて読んだ。

- `layout.md`: `grow-product-idea/SKILL.md`、`grow-product-idea/references/answering.md`、`grow-product-idea/references/making-material.md`、`refine-what-defines-a-product/SKILL.md`
- `canonical.md`: `grow-product-idea/SKILL.md`、`grow-product-idea/templates/layout.md`
- `material.md`: `grow-product-idea/references/making-material.md`（材料skill8種はこれを通して使う）、`grow-product-idea/templates/layout.md`

### 判断

`canonical.md`は`grow-product-idea`だけが使うため残す。`layout.md`は全skillが使うため`product-plans/README.md`へ。`material.md`は材料skillが使い、`making-material.md`を無くすため、`product-plans/README.md`の中に材料の入口の形として書く。提案1は使う担当を確かめずに三つをまとめていた。
