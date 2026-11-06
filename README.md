# grow-product-ideas

プロダクトのアイデアを、作り始める前に決めるべきことが全部決まった状態（build-ready、あと作れば終わり）まで詰めるリポジトリ。

詰めれば決まるもの（代案の比較、スコープ、テーブル構成、モジュール構成）はこのリポジトリのレールが引き受け、利用者の頭は、寝かせないと出てこないもの（着想、作りたい動機、体験の質感）だけに使う。
決めるべきことは、層ごとの決めるものと決め方として持っていて、全ての層が閉じるまでbuild-readyにしない。

## 使い方

このリポジトリのrootで Claude Code か Codex を開き、アイデアを渡して`grow-product-idea`を使うよう頼む。

```text
grow-product-idea で、このアイデアを詰めたい。
アイデア: 毎月のサブスクの更新日を忘れて、使っていないサービスに払い続けている。
作りたい動機: 自分の家計の無駄を減らしたい。
既にある着想: 更新日の3日前に通知が来れば十分な気がする。
```

途中で止めたアイデアは、`product-plans/<slug>/`を指定して再開できる。

### 利用者に問われる場面

レールが利用者へ問うのは、次の時だけである。

- 受け入れ時: アイデア、作りたい動機、既にある着想
- 層を決める中で立った論点: 利用者の採否が要る判断、利用者しか持たない事実、発案者の視野の外の点
- 層の閉じ: その層で決めたものを受け入れるか
- 出口判定: build-ready・作らない・保留のどれにするか

### 出口

| 出口 | 状態 | 残るもの |
| --- | --- | --- |
| build-ready | 全ての層が閉じた | 正本と、層ごとの記録と決定過程、材料。初回構築の入力になる |
| 作らない | 作らないと判断した | 作らないと決めた理由 |
| 保留 | 今は作らない | 復活する条件 |

出口がどれでも、`product-plans/<slug>/`はこのリポジトリの判断記録として残る。

### build-readyの後

1. `product-plans/<slug>/`の写しを、`initial_product_plan`のような名前で新しいリポジトリへ置く。
2. 新しいリポジトリで、その写しの`README.md`（正本）を入力に`tumeda-dev`の`steering`／`task-design`で初回構築を始める。なぜそう決めたかは、層ごとのdirectoryの記録と決定過程にある。

今は、どこまで作るか層とどう作るか層を、まだ今の形で書いていない。そのため、アイデアは、なぜ作るか層、何が成り立てばよいか層、どう解くか層を閉じた所で、検討中のまま止まり、build-readyにはならない。

`product-plans/<slug>/`は、作る時からdirectoryの中だけで読み切れるように書かれている。新しいリポジトリに`what-defines-a-product/`やこのリポジトリのskillが無くても読める。
写しの作成、名前の変更、新しいリポジトリの作成は、利用者が行う。

## 構成

```text
grow-product-ideas/
├── README.md                 # このfile
├── AGENTS.md                 # プロジェクト指示の正本
├── CLAUDE.md -> AGENTS.md
├── what-defines-a-product/   # 層。READMEと層file
├── product-plans/            # 1アイデア1directory。レールを通した判断記録。READMEが中の配置を定める
├── .agents/skills/           # レールのskillの正本
├── .claude/skills -> ../.agents/skills
└── .steering/                # このリポジトリ自体を改善する作業の記録
```

| 置き場所 | 役割 |
| --- | --- |
| [`what-defines-a-product/`](what-defines-a-product/README.md) | プロダクトをbuild-readyにするための層。層fileは、層ごとの決めるもの、決め方、止める時を持つ。READMEは、層の順、層の閉じ、差し戻し、skillへの頼み方を持つ |
| [`product-plans/`](product-plans/README.md) | アイデア1件ごとに、正本（プロダクトの説明）、層ごとの記録と決定過程、材料とその決定過程。中の配置と名前、記録の役割は`product-plans/README.md`が定める |
| `.agents/skills/` | レールのskill。Claude Code は`.claude/skills`から、Codex は`.agents/skills`から読む |

### skill

| skill | 役割 |
| --- | --- |
| `grow-product-idea` | アイデアを受け取り、層を順に決めて閉じ、出口まで運ぶ。入口はこれ |
| `propose-alternatives` | 層から頼まれ、覆いたい状態を、やり方を変える・あり物・組み合わせ・作る道で覆う対案を、候補の事実と費用を添えて挙げる。選ばない |
| `sketch-experience` | 層から頼まれ、体験の流れと、全画面を一度に並べたラフ画の複数案を、頼まれた粒度で作る。選ばない |

ほかのskill（利用者の声、心臓部のロジック、テーブル構成、モジュール構成、技術検証、レールの還元）は、今の形に直すまで、`.steering/2026/202611/20261103-implement-build-ready-idea-lab-skeleton/archive/`に退避している。

## 前提

- `tumeda-dev` plugin: `facilitate-discussion`（決定過程の記録）、`name-work-directory`（slugの決定）、`steering`／`task-design`（レールの改善、build-ready後の初回構築）を使う。

## レールを育てる

アイデアを通して分かった過不足は、`.steering/`の作業でレールへ戻す（還元のskillは、今の形に直すまで退避している）。
層の決め方は網羅を目指さない。毎回悩むところを先回りして、答えの出し方ごと用意するために置く。

レールの設計の記録は`.steering/`にある。

- 骨格の設計: `.steering/2026/202609/20260912-design-build-ready-idea-lab-skeleton/design.md`
- 実体化の設計: `.steering/2026/202611/20261103-implement-build-ready-idea-lab-skeleton/design.md`
