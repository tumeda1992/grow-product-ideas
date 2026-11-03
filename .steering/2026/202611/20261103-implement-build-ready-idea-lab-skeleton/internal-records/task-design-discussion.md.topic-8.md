# 内部検討記録: 論点8 — skill14種の名前

**discussion:** [task-design-discussion.md](../task-design-discussion/task-design-discussion.md)

**論点:** 論点8

## 開始context

論点5でskillの正本を`.agents/skills/<skill名>/SKILL.md`に置くと決め、論点7でworkflowと各skillの担当を決めた。前回designはskill名を仮称（「なぜ作るか層を閉じる」等の日本語の役割名）で置き、確定を次段階へ送っている。

skill名はdirectory名であり、Claude CodeとCodexでの呼び出し名になる。各`SKILL.md`を書く前に決める必要がある。

判断基準は`tumeda-dev`の`development_standards/naming/`（core、file、reverse_translation、review）である。

- 初見で自明、宣言的（outcomeを名指す）、具体性、名前空間の中で評価する
- 同列の要素と表面・抽象度を揃える（file.md）。周囲の慣習は、skillはkebab-case、`tumeda-dev`のskillは動詞+目的語（`facilitate-discussion`、`name-work-directory`等）
- 評価は「意味する方向が同じか」で行う（review.md）

<a id="iteration-0"></a>

## イテレーション0: 命名の型と14種の名前

<a id="iteration-0-record-1"></a>

### 判断: 層skillを層fileの名前と対にするか

層fileは`why-to-build.md`、`what-to-build.md`、`how-far-to-build.md`、`how-to-build.md`である。層skillの担当は「担当層の問いに答える」（論点7）。

- `answer-why-to-build`等: 層fileの名前をそのまま目的語にするため、どの層fileを扱うskillかが名前から一意に分かる。outcome（その層の問いに答えが出ている）を名指す。
- 前回designの仮称「なぜ作るか層を閉じる」から`close-why-to-build`も考えたが、`close`は単独では「終える・やめる」と読まれ、閉じ条件というこのリポジトリ内の概念を知らない人には方向が違う誤解になる。`answer`は方向が同じ。

<a id="iteration-0-record-2"></a>

### 判断: 各skillの名前と逆翻訳

| 役割（前回designの仮称） | 名前 | 初見の人が予想する中身 | 実態との差 |
| --- | --- | --- | --- |
| 全体制御 | `grow-product-idea` | プロダクトのアイデアを育てるskill。入口だと予想する | 「アイデアを広げるブレスト」と読まれる余地がある。リポジトリ名`grow-product-ideas`と同じ誤解であり、前回designで方向が同じとして受け入れている。単数形にすることで、アイデア1件を扱う入口であることが読める |
| なぜ作るか層を閉じる | `answer-why-to-build` | why-to-buildに答える | 差なし。層fileと対になる |
| 何を作るか層を閉じる | `answer-what-to-build` | 同上 | 同上 |
| どこまで作るか層を閉じる | `answer-how-far-to-build` | 同上 | 同上 |
| どう作るか層を閉じる | `answer-how-to-build` | 同上 | 同上 |
| 競合とあり物の組み合わせを調べる | `find-existing-alternatives` | 既にある代替手段を探す | 「あり物の組み合わせ」は名前から読めないが、組み合わせも代替手段の一つであり方向は同じ |
| 構築コストと代案のランニングコストを見積もる | `compare-build-and-alternative-costs` | 作る費用と代案の費用を比べる | 差なし。前回designの「二つを同じ尺度へ揃える」が`compare`に表れる |
| ペルソナを想定し、ウェブ上の声を集める | `gather-target-user-voices` | 対象利用者の声を集める | ペルソナの想定が名前に出ないが、声を集める対象を定める前段であり方向は同じ。`persona`を入れると「ペルソナになりきって演じる」と読まれる余地がある |
| 体験とラフ画を作る | `sketch-experience` | 体験をラフに描く | 差なし。ラフ画（sketch）と体験の両方を拾う |
| 心臓部ロジックを検討する | `design-core-logic` | 中核のロジックを設計する | 差なし |
| テーブル構成を決める | `design-tables` | テーブルを設計する | 差なし |
| モジュール構成を決める | `design-modules` | モジュールを設計する | 差なし |
| 技術検証する | `verify-technical-feasibility` | 技術的に実現できるかを確かめる | 前回designは`task-design`の`spike/`を包むとしている。`spike`を名前に入れるとAgile用語を知らない人に読めないため、outcome（実現できるかが分かる）を名指した |
| `what-defines-a-product/`へ還元する | `refine-what-defines-a-product` | what-defines-a-productを改良する | 差なし。還元の対象を名前で示す |

同列の揃い:

- 全てkebab-case、動詞+目的語
- 層skillは`answer-`で揃い、材料skillは調査系（`find`、`compare`、`gather`）と生成系（`sketch`、`design`）で動詞が分かれ、系統の違いが読める
