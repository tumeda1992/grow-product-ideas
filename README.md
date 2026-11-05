# grow-product-ideas

プロダクトのアイデアを、作り始める前に決めるべきことが全部決まった状態（build-ready、あと作れば終わり）まで詰めるリポジトリ。

詰めれば決まるもの（代案の比較、スコープ、テーブル構成、モジュール構成）はこのリポジトリのレールが引き受け、利用者の頭は、寝かせないと出てこないもの（着想、作りたい動機、体験の質感）だけに使う。
決めるべきことは問いの形で持っていて、答えが揃うまでbuild-readyにしない。

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
- 層の閉じ: なぜ作るか・何を作るか・どこまで作るか・どう作るかの各層の答えを受け入れるか
- 出口判定: build-ready・作らない・保留のどれにするか
- 着想・動機・体験の質感が無いと答えられない問いに当たった時

### 出口

| 出口 | 状態 | 残るもの |
| --- | --- | --- |
| build-ready | 全ての問いが水準を満たした | 問いと答えの全体。初回構築の入力になる |
| 作らない | 作らないと判断した | 作らないと決めた理由 |
| 保留 | 今は作らない | 復活する条件 |

出口がどれでも、`product-plans/<slug>/`はこのリポジトリの判断記録として残る。

### build-readyの後

1. `product-plans/<slug>/`の写しを、`initial_product_plan`のような名前で新しいリポジトリへ置く。
2. 新しいリポジトリで、その写しの`README.md`（プロダクトの説明）を入力に`tumeda-dev`の`steering`／`task-design`で初回構築を始める。最初に作るものは「最初に作る分」の節に、AIが利用者に聞かずに進めてよい範囲は「AIに任せる範囲」の節にある。なぜそう決めたかは、層ごとのdirectoryの決定過程にある。

`product-plans/<slug>/`は、作る時からdirectoryの中だけで読み切れるように書かれている。新しいリポジトリに`what-defines-a-product/`やこのリポジトリのskillが無くても読める。
写しの作成、名前の変更、新しいリポジトリの作成は、利用者が行う。

## 構成

```text
grow-product-ideas/
├── README.md                 # このfile
├── AGENTS.md                 # プロジェクト指示の正本
├── CLAUDE.md -> AGENTS.md
├── what-defines-a-product/   # 問いのセット。READMEと四層file
├── product-plans/            # 1アイデア1directory。レールを通した判断記録。READMEが中の配置を定める
├── .agents/skills/           # レールのskillの正本
├── .claude/skills -> ../.agents/skills
└── .steering/                # このリポジトリ自体を改善する作業の記録
```

| 置き場所 | 役割 |
| --- | --- |
| [`what-defines-a-product/`](what-defines-a-product/README.md) | プロダクトをbuild-readyにするために答える問いのセット。層ごとに、問い、水準（満たさない答えの例）、定石（選択肢と判断軸）を持つ |
| [`product-plans/`](product-plans/README.md) | アイデア1件ごとに、プロダクトの説明（正本）、層ごとの問いの決着の記録と決定過程、材料。中の配置と名前は`product-plans/README.md`が定める |
| `.agents/skills/` | レールのskill。Claude Code は`.claude/skills`から、Codex は`.agents/skills`から読む |

### skill

| 分類 | skill | 役割 |
| --- | --- | --- |
| 全体制御 | `grow-product-idea` | アイデアを受け取り、次の問いを選び、`settle-question`を起動し、出口まで運ぶ。入口はこれ |
| 問い | `settle-question` | 問い一つを、このアイデアの問いへ立て直し、詰める深さを決め、材料を揃えて対案と比べて答え、漏れを確認して閉じる |
| 材料（対案） | `propose-alternatives` | 要求の状態を、やり方を変える・あり物・組み合わせ・作る道で覆う対案を、候補の事実と費用を添えて挙げる |
| 材料（調査） | `gather-target-user-voices` | 利用者の声と、同じ痛みを持つ人のしのぎ方を集める |
| 材料（生成） | `sketch-experience`、`design-core-logic`、`design-tables`、`design-modules` | 体験とラフ画、心臓部のロジック、テーブル構成、モジュール構成の複数案を作る |
| 材料（検証） | `verify-technical-feasibility` | 動かさないと分からないことを、最小限のcodeで確かめる |
| 還元 | `refine-what-defines-a-product` | 出口へ着いた1件から、問い・水準・定石とskillの過不足を判定し、レールを育てる |

## 前提

- `tumeda-dev` plugin: `facilitate-discussion`（決定過程の記録）、`name-work-directory`（slugの決定）、`steering`／`task-design`（レールの改善、build-ready後の初回構築）を使う。

## レールを育てる

アイデアが出口へ着いたら、`refine-what-defines-a-product`で、その1件で分かった過不足をレールへ戻す。
問いは網羅を目指さない。毎回悩むところを先回りして、答えの出し方ごと用意するために置く。

レールの設計の記録は`.steering/`にある。

- 骨格の設計: `.steering/2026/202609/20260912-design-build-ready-idea-lab-skeleton/design.md`
- 実体化の設計: `.steering/2026/202611/20261103-implement-build-ready-idea-lab-skeleton/design.md`
