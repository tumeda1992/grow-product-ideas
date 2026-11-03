# Design: build-readyなアイデアラボの骨格を実体化する

## 元の依頼内容

.steering/2026/202609/20260912-design-build-ready-idea-lab-skeleton で考えたものを形にしたい

---

## TL;DR

前回の骨格design（[前提とする既存仕様](#付録前提とする既存仕様)）は、各skillの`SKILL.md`本文、問いのセットの項目、`product-plans/`のテンプレート本文を「実際にアイデアを1件通して初めて確定する」として次段階へ送った。今回はその次段階にあたる。

今回の終了時には、アイデアを出口まで運べ、build-readyなら`product-plans/<slug>/`を新しいリポジトリへ持っていって初回構築を始められるレールが、このリポジトリに存在する。レールは前回designの構成要素（README、`what-defines-a-product/`、`product-plans/`の構造と雛形、skill）を備え、各要素の中身はレールとして機能するかで判定して作る。前回designは保持対象ではなく、機能させるための仮説として扱う。

---

## このdesignの対象範囲

今回のdesignは、アイデアを出口まで運べ、出口がbuild-readyの時は`product-plans/<slug>/`を新しいリポジトリへ持っていってそのまま初回構築を始められる状態になる、レールを作るところまでを対象とする。これを、assistantが用意した出来合いのアイデア3件ほどを、assistant自身がユーザー役も演じて通すことで確かめる（[受け入れ基準](#受け入れ基準)）。

対象外は、利用者の実際のアイデアを通すこと、新しいリポジトリの作成、`initial_product_plan`等への名前の変更、初回構築である。これらはこのsteeringの後の作業である。

build-readyの後、`product-plans/<slug>/`の写しは`initial_product_plan`のような名前で新しいリポジトリの最初の存在になり、それを元に初回構築が行われる。後続のリポジトリには`what-defines-a-product/`もこのリポジトリのskillも無い。そのため、build-readyの`product-plans/<slug>/`は、directoryの中だけで読み切れ、後続の`steering`／`task-design`がdirectoryの外へ問い合わせずに初回構築へ着手できる必要がある。満たし方は[後続のリポジトリへの受け渡し](#後続のリポジトリへの受け渡し)で定める。

`product-plans/`はこのリポジトリにとって判断記録の堆積である。自演で作った`product-plans/<slug>/`も残し、後続へ渡す時もこのリポジトリの`product-plans/<slug>/`は残して写しを持っていく。

自演で見つかった摩擦は、このsteeringの中で該当fileを直して解消する。利用者の実際のアイデアで得る摩擦は、このsteeringの後に還元skillで`what-defines-a-product/`へ戻す。利用者の実際のアイデアを範囲外に残すのは、レールの利用と改善を同じ作業単位に混ぜると、利用で見つかった摩擦をその場で改善へ戻すことになり、実装中に新しい設計判断が生まれるためである。自演はレールの検証として扱い、アイデアをassistantが用意するため、終了状態がアイデアの着地先に依存しない。

前回designのリスクと対策は「次段階のスコープを実体作成で止めず、実体作成と最初の1件を通すことまでとする」としており、その意図（構造を作ること自体が目的化し、1件も通らない状態を防ぐ）は、自演で出口まで通すことで保つ。

### このdesignが持つものと、実fileが持つもの

各要素の中身は子designへ分けず、このdesign一つで扱う。

- このdesign.mdが持つもの: 要素間の接合面（file一覧・配置・名前、要素間の参照関係、受け入れ基準）、各fileの役割、中身の判定基準、前回designからの変更
- 実fileが持つもの: 各層の問い・水準・定石、各`SKILL.md`の本文、`product-plans/README.md`と正本の雛形の本文。中身の正本は実fileであり、design.mdへ複製しない

作成は、接合面の合意の後、依存順（問いの中身を先、それを使うskillを後）に、fileまたはfile群ごとに「見出し構成と各見出しの内容を合意 → 実fileを作成 → 実fileをreview」を繰り返して進める。作る順は次のとおりとする。

1. `what-defines-a-product/README.md`の約束の部分（問いの書き方、材料の識別子）。他の見出しは前回designの内容で仮に書く
2. `what-defines-a-product/`の四層ファイル（問い、必要な材料、水準、定石）
3. `product-plans/README.md`（配置と材料の入口の形）、`grow-product-idea`と正本の雛形
4. `settle-question`
5. 材料skill8種
6. `refine-what-defines-a-product`
7. リポジトリの`README.md`と、`.claude/skills`のsymbolic link。あわせて`what-defines-a-product/README.md`の仮に書いた見出し（冒頭の説明、四つの層、問いの選び方、粒度と再利用、問いを足す・削る基準）を、実際の層file・skillと照らして直し確定させる

層fileの問いは層の閉じ条件から導き、skillに依存しない。逆に、問いに答えるskillは層fileの問い・材料の並び・水準を読んで動くため、1・2を先にする。水準と定石の本文が機能するかは自演で確かめて直す。全体制御skillは`settle-question`を起動する側であり、配置の約束とあわせて先にする。リポジトリの`README.md`はレール全体の使い方を書くため最後にする。`what-defines-a-product/README.md`を二回に分けるのは、層fileとskillが従う約束は後から決めると書き直しが要り、全体を取りまとめる部分は層file・skillが出来るまで合っているかを確かめられないためである。前回designが次段階へ送った中身には判断が残るため、その判断は各fileの見出し構成の合意として扱う。

子designへ分けないのは、中身の正本を実fileに置けばdesign.mdの分量は問題にならず、分けた場合との差がsteeringの必須gateとroadmapの状態管理の重複だけになるためである。依存順は、扱うfileの順番として保つ。

fable・astraに関する作業は別issueとして存在し、このdesignの範囲に含めない。

### 中身の判定基準

各要素の中身は、レールとして機能するかで判定する。機能とは、前回designが解こうとした痛みから取り出した次の働きを果たすことである。

| 働き | 対応する痛み | 主に担う要素 |
| --- | --- | --- |
| 毎回同じ問いが出てきて、何を考えるかをゼロから決めずに済む | 毎回紆余曲折する | 層ファイルの問い、全体制御skill |
| 答えが閉じたかを判定でき、浅い答えで先へ進まない | 各工程を一定以上の水準にする | 水準、全体制御skill |
| 思いつきを対案と比べてから選べる | プロセスが我流 | 定石、`settle-question`・材料skill |
| 体験・画面・テーブル・モジュールを全体で揃えて決められる | パッチワーク | 生成系の材料skill |
| 作らない・保留も含めて出口を判定できる | 作るべきかを問う場面がない | 全体制御skill、`why-to-build.md` |
| 1件通した結果で問い・水準・定石を育てられる | プロセス自体を資産にする | 還元skill、正本の「このアイデアでの問い」 |

深さに上限は置かない。足すか削るかは、その中身がなければ上の働きが果たせないか、あると働きを妨げるかで決める。前回designの「網羅しない」は、問いが増えすぎると紆余曲折そのものが増えて一つ目の働きを妨げる、という機能上の理由として使う。

前回designは保持対象ではなく、機能させるための仮説として扱う。fileを作る中で直した方が機能すると分かった箇所は、そのfileの見出し構成の合意の中で直す箇所と理由を示して合意し、[前回designからの変更](#付録前回designからの変更)へ記録する。直す余地がなければそのまま適用する。

---

## 完成後の姿

### skillの役割と能力境界

skill11種の役割と能力境界を、前回designのskill一覧と[アイデアを通すworkflow](#アイデアを通すworkflow)から定める。skill間の起動関係と担当の詳細はworkflowが正本であり、ここでは各skillが持つものと持たないものを示す。各`SKILL.md`の本文は実fileを正本とする。

| 分類 | skill | 持つもの | 持たないもの |
| --- | --- | --- | --- |
| 全体制御 | `grow-product-idea` | 受け入れ、`product-plans/<slug>/`の作成と正本の雛形、次の問いの選択、`settle-question`の起動、水準の一段目と確認の記録の有無の確認、層の閉じと出口判定のユーザー確認gate、出口判定、還元skillの起動の促し | 層ごとの中身（問いごとの水準）。問いの立て直し、答えを作ること、水準に照らす確認 |
| 問い | `settle-question` | 問い一つについて、このアイデアの問いへの立て直し、詰める深さの決定、材料skillの起動と粒度の指定、定石からの対案、`facilitate-discussion`での決定過程の記録、正本への記入、立て直した基準での漏れの確認 | 次の問いの選択、出口判定。層ごとの分岐（層ごとの内容は層fileが持つ）。着想・動機・体験の質感を要する時以外のユーザーへの問い |
| 材料（調査系） | `find-existing-alternatives`、`compare-build-and-alternative-costs`、`gather-target-user-voices` | 前回designのskill一覧の「持つもの」（探す先、同じ尺度へ揃える手順、個人版の代替であることと落ちる精度の記録等）、要求された粒度で材料を作る・育てること | 問いへの答え。材料から結論を出すのは`settle-question` |
| 材料（生成系） | `sketch-experience`、`design-core-logic`、`design-tables`、`design-modules` | 前回designのskill一覧の「持つもの」（全体を一度に並べる手順、複数案を作る手順、定石の参照先、作り込みすぎない粒度等）、要求された粒度で材料を作る・育てること | 複数案からの選択。選ぶのは`settle-question` |
| 材料 | `verify-technical-feasibility` | `task-design`の`spike/`の考え方で、実行して初めて分かる技術的な事実を材料に残すこと | 本実装 |
| 還元 | `refine-what-defines-a-product` | 出口到達後に、問いの過不足、水準の妥当性、定石の有効性、skillの手順、正本・材料の名前と構成の金属疲労を判定し、変更案を出すこと。正本の「このアイデアでの問い」を主な根拠に読む。ユーザーの承認後に、このリポジトリの作業の進め方に従ってレールを直し、記録を`.steering/`に残すこと | ユーザーの承認なしにレール自体を変えること。`product-plans/<slug>/`の中身を変えること |

全体制御を進行に、`settle-question`を問いの中身に、材料skillを材料づくりに分けるのは、全体制御へ層ごとの知識が集まって太ることを防ぐためである。

前回designは層ごとに4種のskillを置いていた。その理由は、起動条件・参照先・落とし穴が層ごとに違い、一つのskillへ畳むと層による分岐をskill内に持つことになるためだった。今回は、起動条件（上位層が閉じているか）を全体制御が判定し、参照先は問いのidentifierから層fileが決まり、落とし穴は層fileの水準と材料の並びへ移したため、`settle-question`は層ごとの分岐を持たない。層skill4種は共通の答える手順を除くと層fileの内容をほぼ繰り返しており、前回designの「参照先も手順も既に確定していてskillが何も足さないなら立てない」に当たるため、一つにまとめた。

`settle-question`は、答える前に一般の問いをこのアイデアの問いへ立て直す。一般の問いと一般の満たさない例ではアイデアに特有の浅さを捕まえられず、前回designが検査機構で防ごうとした浅い通過が残るためである。立て直しを独立したskillにしないのは、同じ層の後の問いの立て直しが前の問いの答えに依存し、まとめて先に立て直すと早すぎ、問いごとに分けると受け渡しが増えるだけになるためである。詰める深さは、答えが変わった時の出口・下位の問いへの影響と今の材料での確信度で問いごとに配分する。前回designの「過剰な深掘りを排除する」と[中身の判定基準](#中身の判定基準)の「上限を固定せず機能で判定する」を両立させるためである。

### 知識体系（`what-defines-a-product/`）

`what-defines-a-product/`は前回designの構成のまま、`README.md`と四層ファイルを持つ。各ファイルの中身は実fileを正本とし、[中身の判定基準](#中身の判定基準)で判定する。

```text
what-defines-a-product/
├── README.md             # 問いのセットの引き方、層の関係（答えの依存方向と材料の供給方向）、問いを選ぶ基準、粒度の判定基準、材料の識別子の一覧
├── why-to-build.md       # なぜ作るか。作る根拠と、作ることのリスク
├── what-to-build.md      # 何を作るか。解く範囲
├── how-far-to-build.md   # どこまで作るか。最初に作る分の区切り
└── how-to-build.md       # どう作るか。体験・画面構成・テーブル構成・モジュール構成
```

- 層fileの各問いは、前回designの形（問い、必要な材料、水準、定石）を持つ。必要な材料は[材料の識別子](#file成果物)で挙げ、要求する粒度を添える。
- 水準は、`settle-question`が答えを作る時の目標と、書いた後の確認の基準を兼ねる一つの正本である。`settle-question`は一般の満たさない例を外さず、このアイデアで起きやすい例を足して問いを立て直す。満たさない答えの例を、作る側が狙え、確認する側が判定を一つに決められる具体性で書く（[答えの作り方と、書いた後の確認](#答えの作り方と書いた後の確認)）。
- 材料の識別子の一覧の正本は`README.md`に置く。材料を要求するのは問いであり、問いの引き方を持つのが`README.md`だからである。

### アイデアを通すworkflow

前回designの「問いに答えるまでの流れ」「出口は三つ」「ユーザー確認のgate」を、skill間の起動関係・状態・gateへ具体化する。skill名は[file成果物](#file成果物)で定める。

#### 登場するもの

- ユーザー
- 全体制御skill: アイデア1件を出口まで運ぶ
- `settle-question`: 問い一つを、このアイデアの問いへ立て直して答え、漏れを確認して閉じる
- 材料skill（8種）: 要求された粒度で材料を作る。どの層にも属さない
- 還元skill: 出口到達後、レール自体を育てる
- 正本（`product-plans/<slug>/`の正本ファイル）: アイデア1件の状態の唯一の置き場所

#### 流れ

```text
ユーザー ──(アイデア、作りたい動機、既にある着想)──→ 全体制御
                                                    │ product-plans/<slug>/ と正本を作る
                                                    ▼
                         ┌────────── 全体制御: 次の問いを選ぶ ←───────────────┐
                         │   （未回答の問いのうち下位を最も多く規定するもの）    │
                         ▼                                                      │
                 その問いについてsettle-questionを起動                           │
                         │ このアイデアの問いへ立て直し、詰める深さを決める      │
                         │ 立て直した基準を目標に、必要なら材料skillを起動       │
                         │ 定石から対案を出し、自分の案と並べて選ぶ              │
                         │ 答えを正本へ書く                                      │
                         │ 立て直した基準で漏れを確認し、正本へ「閉じた」と記録  │
                         ▼                                                      │
                 全体制御: 一段目と確認の記録を見る                              │
                         │                                                      │
                         ├─ 層の全問いが閉じた → ユーザー確認gate ───────────────┤
                         │      （なぜ作るか層が閉じた時は、ここで出口判定も行う）│
                         └─ 層はまだ閉じない ────────────────────────────────────┘

全問いが閉じた、または途中で「作らない」「保留」と判定した
  → 出口判定のユーザー確認gate → 正本へ出口を記録
  → 全体制御がユーザーへ還元skillの起動を促す
  → 還元skill: 問い・水準・定石の変更案を出し、ユーザーの承認後に what-defines-a-product/ とskillを直す
```

#### 担当

| 担当すること | 担当 |
| --- | --- |
| アイデアの受け入れ、`product-plans/<slug>/`と正本の作成 | 全体制御 |
| 次の問いの選択 | 全体制御 |
| 問いの立て直しと深さの決定、答えを作る（立て直した基準を目標に、材料集め、対案との比較、正本への記入） | `settle-question` |
| 材料skillの起動と粒度の指定 | `settle-question`。材料が別の層のもの（なぜ作るか層の問いがラフ画を要求する等）でも直接起動する |
| 書いた後の漏れの確認と「閉じた」の記録 | 答えを書いた`settle-question` |
| 水準の一段目（材料が揃っているか、生成系は複数案と全体の揃い）と、確認の記録があることの確認 | 全体制御 |
| 状態（問いごとの答え・確認結果・材料参照、出口） | 正本だけに置く |
| 出口判定 | 全体制御。全問いが閉じた時に加え、なぜ作るか層が閉じた時点でも行う |
| ユーザーへの問い | 受け入れ時（アイデア、動機、既にある着想）、層の閉じ、出口判定は全体制御。問いが着想・動機・体験の質感を必要とした時だけ`settle-question`。これ以外ではユーザーへ問わない |
| 還元 | 出口記録の直後に全体制御が起動を促し、還元skillが変更案を出す。レール自体の変更はユーザーの承認後 |

全体制御は進行（次の問いの選択、`settle-question`の起動、gate、出口判定）だけを持ち、層ごとの中身（問いごとの水準）を持たない。水準に照らす確認を全体制御へ置くと四層分の水準の知識が全体制御へ集まるため、確認は`settle-question`に置く。

#### 答えの作り方と、書いた後の確認

品質は答えを作る段階で担保し、書いた後の確認はそれでも漏れたものを拾うためにある。確認があるから作る段階を緩くしてよい、という形は取らない。`tumeda-dev`の`task-design`が設計時から`document-review`の観点を見込み、`document-review`がemit前に漏れを拾うのと同じ関係である。

- 答えを作る時: `settle-question`は、立て直した問いの基準（一般の満たさない例とこのアイデアの例、調査系は必要な材料、生成系は複数案と全体の揃い）を目標として使い、水準を満たす答えを作ろうとして材料を集め、対案を並べ、答えを書く。
- 書いた後の確認: 正本に書いた立て直しの基準に照らして漏れを確認する。確認は正本を後で読む人（出口判定のユーザー、build-ready後の`steering`／`task-design`）の立場で、正本に書かれた答えと`materials/`の材料だけを見て行い、答えを考えた時の推論で補わない。

| 漏れ | 戻り先 |
| --- | --- |
| 言い回し、参照の欠け等の局所的な漏れ | その場で直し、確認をやり直す |
| 材料が足りない、対案を比べていない、答えが材料から導かれていない等、答えの骨子の漏れ | 材料集めか答えを作る段階へ戻って作り直す。一文を足して満たしたことにしない |

水準は、作る時の目標と確認の基準を兼ねる一つの正本である。`what-defines-a-product/`の各層fileでは、満たさない答えの例を、作る側が狙いを定められ、確認する側が照合して判定を一つに決められる具体性で書く。

#### 出口判定の時期

出口判定は、全問いが閉じた時に加え、なぜ作るか層が閉じた時点でも行う。全問いが閉じるまで待つと、なぜ作るか層で作らないと分かった後も下位層の問いに答え続けることになり、紆余曲折を減らすというレールの目的を妨げる。

#### 後続のリポジトリへの受け渡し

build-readyの`product-plans/<slug>/`の写しは、`initial_product_plan`のような名前で新しいリポジトリの最初の存在になり、それを元に初回構築が行われる。後続のリポジトリには`what-defines-a-product/`もこのリポジトリのskillも無いため、`product-plans/<slug>/`は出口に関わらず、作る時からdirectoryの中だけで読み切れるように書く。

- `settle-question`・材料skillは、正本の各問いに問いの文面とこのアイデアでの問いを書き、定石から選んだ時は選んだ選択肢と比べた選択肢の中身を`discussion.md`に書き、linkをdirectoryの中（正本、`discussion.md`、`materials/`）だけに張る。
- 全体制御skillは、出口判定でbuild-readyとする時に、directoryの外へのlinkや外を見ないと分からない参照が無いかを確認し、見つかればその問いについて`settle-question`へ戻して直させる。
- このリポジトリの`README.md`に、build-readyの`product-plans/<slug>/`の写しを新しいリポジトリへ持っていき、初回構築の入力にする流れを書く。写しの作成、名前の変更、リポジトリの作成は利用者が行う。このリポジトリの`product-plans/<slug>/`は判断記録として残す。

build-ready時に外への参照を展開して整える工程は置かない。作る段階を緩めて後で補う形になり、作らない・保留のdirectoryが判断記録として読みにくく残るためである。初回構築向けの要約documentは置かない。四層の答え（スコープの内と外、最初に作る分の区切り、体験・画面・テーブル・モジュール）がそのまま初回構築の入力になるためであり、自演で後続が着手しにくいと分かった時に見直す。

### file成果物

今回の終了時には、前回designのリポジトリ構成とskill一覧にある構成要素がすべて存在する。各要素の中身は[中身の判定基準](#中身の判定基準)で判定する。

構成要素の数を減らさないのは、skill一覧が前回designでskillを立てる基準を通して合意済みであり、skillを欠いたまま1件目を通すと、得られる摩擦の多くが「手順を示すskillが無い」ことになるためである。それでは還元で拾うべき問い・水準・定石の過不足が覆い隠される。各skillの中身が1件通すまで検証されない仮のものになることは、問いのセットが仮であることと同じ性質の代償として受け入れる。

- `AGENTS.md`と`CLAUDE.md`: プロジェクト指示の正本は`AGENTS.md`であり、`CLAUDE.md`は`AGENTS.md`へのsymbolic linkである。Claude CodeとCodexの両方へ同じ指示を一つの正本から渡す。
- `README.md`: このリポジトリの使い方。プロダクトのアイデアを入れる人が最初に読む（前回designのまま）。
- `what-defines-a-product/`配下: [知識体系](#知識体系what-defines-a-product)のとおり。
- `product-plans/README.md`: `product-plans/<slug>/`の配置と名前、directoryの中だけで読み切れるようにする規則、材料の入口の形を定める唯一の場所。全てのskillが読むため、どのskillにも属さない`product-plans/`に置く。
- 正本の雛形: `grow-product-idea`だけが使うため、`.agents/skills/grow-product-idea/templates/canonical.md`に置く。
- `product-plans/<slug>/`: slugは`name-work-directory`で決める。正本の配置と構成は`product-plans/README.md`の一箇所だけで定め、全体制御skill（`grow-product-idea`）はそれと正本の雛形から`product-plans/<slug>/`を作る。他のskillは正本をfile名ではなく「正本」という役割で参照する。

  正本は仮置きとして名前を`README.md`、構成を1枚とする。正本の分量はアイデアを実際に通して初めて分かるため、今は確定させない。最初の1件を通す中で正本が読み書きしにくい分量になった時に、名前と構成を見直し、還元の対象として扱う。仮置きの影響を`product-plans/README.md`と正本の雛形に閉じるため、各skillは役割で参照する。

  ```text
  product-plans/<slug>/
  ├── README.md       # 正本（仮置き）。受け入れ時の入力、現在の状態、問いごとの答え・確認結果・材料参照、出口の記録
  ├── discussion.md   # 決定過程。facilitate-discussionで記録する
  └── materials/
      └── <材料の識別子>/
          ├── README.md   # 材料の入口（仮置き）
          └── ...         # 中の分け方は材料skillが分量に応じて決める
  ```

  材料の種類は材料skillと一対一にし、識別子で問い・材料skill・全体制御skillをつなぐ。識別子の一覧の正本は`what-defines-a-product/README.md`に置く。

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

  一段目は`materials/<識別子>/README.md`の有無を見る。材料の分量も実際に通すまで分からないため、入口だけを定めて中の分け方は材料skillに任せ、入口の名前は正本と同じく仮置きにする。要求元の問いが細かい粒度を求めた時は同じdirectoryの中を育て、粒度ごとに別の材料を作らない。

  記録するものは置き場所で分ける。

  | 記録するもの | 置き場所 | 中身 |
  | --- | --- | --- |
  | 結論 | 正本 | 問いごとの答え、確認結果、材料と決定過程への参照、出口 |
  | 材料 | `materials/<識別子>/` | 調査系は集めた事実と出典。生成系は作った複数案そのもの |
  | 決定過程 | `discussion.md` | 問いごとに一つの論点。定石の対案と自分の案の比較、選んだ理由、ユーザーの指摘と合意 |

  `settle-question`は答えを作る時に、立て直した問い、比較と選んだ理由を`facilitate-discussion`で該当論点へ提案として保存し、正本の答えから論点へ参照する。層の閉じのユーザー確認gateで、ユーザーがその層の論点群へ応答し、合意した時点で決定になる。正本に過程まで持たせると膨らみ、決定過程を残さないと還元時に答えの理由を辿れないため、この三つに分ける。
- skill11種（全体制御1、問い1、材料8、還元1）: 正本を`.agents/skills/<skill名>/SKILL.md`に置き、`.claude/skills`を`../.agents/skills`へのsymbolic linkにする。skillの追加・変更は`.agents/skills/`配下だけで行う。skill名は次のとおりとする。名前は暫定であり、レールを育てる中で名前と実態がずれた時点で見直す。

  | 役割 | 名前 |
  | --- | --- |
  | 全体制御 | `grow-product-idea` |
  | 問い一つに決着をつける | `settle-question` |
  | 競合とあり物の組み合わせを調べる | `find-existing-alternatives` |
  | 構築コストと代案のランニングコストを見積もる | `compare-build-and-alternative-costs` |
  | ペルソナを想定し、ウェブ上の声を集める | `gather-target-user-voices` |
  | 体験とラフ画を作る | `sketch-experience` |
  | 心臓部ロジックを検討する | `design-core-logic` |
  | テーブル構成を決める | `design-tables` |
  | モジュール構成を決める | `design-modules` |
  | 技術検証する | `verify-technical-feasibility` |
  | `what-defines-a-product/`へ還元する | `refine-what-defines-a-product` |

  `settle-question`は、問いを立て直して答え、確認して閉じる担当であるため、答えるだけでなく決着がついた状態を名指す。`close`は単独で「終える」と読まれるため採らない。全体制御はリポジトリ名`grow-product-ideas`の単数形とし、アイデア1件の入口であることを表す。

  ```text
  grow-product-ideas/
  ├── .agents/
  │   └── skills/                       # skill11種の正本
  │       └── <skill名>/SKILL.md
  └── .claude/
      └── skills -> ../.agents/skills   # Claude Code用の入口。実体を持たない
  ```

  レールはClaude Codeに加えてCodexでも動かす可能性があり、配置先が動かすagentから読めなければレールは機能しない。利用者は`tumeda-dev` pluginのrepositoryでこの形を使い、両agentからskillを使っている。

---

## 要件（Requirements）

### MUST（必達）

- 前回designの構成要素（`README.md`、`what-defines-a-product/`の`README.md`と四層ファイル、`product-plans/`の配置の約束と正本の雛形、skill11種）がすべて存在し、各要素の中身が[中身の判定基準](#中身の判定基準)の働きを果たす
- skillの正本が`.agents/skills/`にあり、`.claude/skills`から辿れ、プロジェクト指示の正本が`AGENTS.md`にある
- skill11種が[アイデアを通すworkflow](#アイデアを通すworkflow)の担当どおりに起動し合い、状態を正本だけに置く
- 正本と材料の入口の配置を`product-plans/README.md`一箇所だけで定め、各skillは役割で参照する
- 材料の識別子で、問い・材料skill・全体制御skillがつながる
- `product-plans/<slug>/`が、作る時からdirectoryの中だけで読み切れるように書かれる
- 前回designから変えた箇所が、理由とともに[前回designからの変更](#付録前回designからの変更)に記録されている

### SHOULD（できれば）

- レールを育てる中で名前・構成の金属疲労が起きた時に、還元skillの対象として見直せる

### MAY（あれば嬉しい）

なし

### 非目標

- 利用者の実際のアイデアを通すこと。このsteeringの後に行うレールの利用であり、そこで得た摩擦は還元skillで戻す
- 新しいリポジトリの作成、`initial_product_plan`等への名前の変更、初回構築。build-ready後の後続の作業である
- fable・astraに関する作業。別issueとして存在する
- reviewの位置づけについてのpluginへのescalate。利用者の指示で保留しており、保留メモ（`pending-escalations/001-review-as-leak-catch.md`）が利用者の解除指示を再開条件として持つ
- 初回構築向けの要約documentを`product-plans/<slug>/`に置くこと。四層の答えがそのまま初回構築の入力になるため今は置かず、自演で後続が着手しにくいと分かった時に見直す
- 正本・材料の入口の名前と構成の確定。分量はアイデアを通して初めて分かるため仮置きとし、正本が読み書きしにくい分量になった時に還元skillで見直す

### 受け入れ基準

全fileを作り終えた後、次の四つを確かめる。個々のfileは作成時に実fileをreviewする。

- 接合面が実fileで一致している。skill11種が[決めた名前](#file成果物)で`.agents/skills/<skill名>/SKILL.md`として存在し、`.claude/skills`から辿れる。`what-defines-a-product/README.md`の材料の識別子と材料skill8種の識別子が一対一で一致する。層fileの問いが挙げる材料がすべてその識別子のどれかである。正本と材料の入口の配置を定めるのが`product-plans/README.md`だけであり、各skillは役割で参照している。
- assistantが用意した出来合いのアイデア3件ほど（出口が分かれそうなもの）を、出口まで自演で通せる。assistantは全体制御skillから各skillの手順どおりに進め、ユーザー確認gateと着想・動機・体験の質感を問われた場面ではユーザー役を演じ、ユーザー役の回答であることを`discussion.md`に区別して残す。各件の出口と、止まった・迷った箇所を記録し、原因が担当skillの中身か接合面かを分けて該当fileを直し、影響範囲を通し直す。自演で作った`product-plans/<slug>/`は残す。
- 新しいsessionで、Codexが`.agents/skills/`のskillと`AGENTS.md`を、Claude Codeが`.claude/skills`経由でskillを読み込む。
- 自演でbuild-readyになった`product-plans/<slug>/`が、directoryの外へのlinkを持たず、正本の各問いに文面があり、定石を名前だけで参照していない。

自演の前に利用者がsessionを閉じてresumeで再開し、新しいskillが読み込まれた状態で自演を行う。自演の直前にassistantが再開を依頼する。ユーザー役の回答を区別して残すのは、`product-plans/`を判断記録として残すため、後から読む人が実際の利用者の判断と取り違えないようにするためである。

---

## リスクと対策

| リスク | 対策 |
| --- | --- |
| skillを書いたassistant自身が自演するため、書いた時の前提で手順の穴を補ってしまい、穴が見つからない | 自演前にsessionを再開し、読み込まれたskillとして起動する。止まった・迷った箇所を、補えた場合も含めて記録する |
| 自演のアイデアの出口が偏り、作らない・保留の経路が確かめられない | 出口が分かれそうなアイデアを選ぶ。全件が同じ出口に着いた場合は、その事実を記録し、別の出口に着きそうなアイデアを追加するかを利用者へ確認する |
| 問いが増えすぎ、紆余曲折を減らすはずが増やす | [中身の判定基準](#中身の判定基準)で、働きを妨げる問いは置かない |
| 正本や材料が膨大になり読み書きしにくくなる | 名前と構成を仮置きにし、配置を`product-plans/README.md`一箇所に閉じ、還元skillで見直せるようにしている |
| 問いを立て直す側と答える側が同じため、答えやすいように基準を下げる | 一般の満たさない例を外さず足すだけにし、立て直した問いと基準を正本に書いて層の閉じで利用者が見る。確認は書かれた基準で行う |

---

## テスト方針

成果物はdocsとskillであり、自動テストはない。

- 各fileは、見出し構成の合意の後に作成し、作成した実fileを`tumeda-dev`の`document-review`の観点と[中身の判定基準](#中身の判定基準)でreviewする
- 全fileを作り終えた後、[受け入れ基準](#受け入れ基準)の四つを確かめる

---

## （付録）前提とする既存仕様

- 骨格design: `.steering/2026/202609/20260912-design-build-ready-idea-lab-skeleton/design.md`（`planless_complete`で完了済み）。リポジトリの役割（詰めれば決まるものを引き受け、着想だけを利用者に残す）、中核を問いのセットとすること、問いの三属性（問い・水準・定石）、四層（なぜ作るか・何を作るか・どこまで作るか・どう作るか）、水準の二段判定、調査系と生成系の区別、出口三種（build-ready・作らない・保留）、skill一覧と厚さ、リポジトリ構成、プロダクト1件のディレクトリ、リポジトリ名`grow-product-ideas`を確定している。各skillの`SKILL.md`本文、問いのセットの全項目、`product-plans/`配下のテンプレート本文、ファイル名とskill名は次段階へ送っている。
- 対象リポジトリの現状（このsteering開始時）: `README.md`（見出し1行のみ）、`CLAUDE.md`、`.steering/`だけが存在する。`what-defines-a-product/`、`product-plans/`、skill配置ディレクトリは未作成。
- `tumeda-dev` plugin: `/Users/takahiroumeda/src/github.com/tumeda1992/ai_agent_dev_skill_plugin/plugins/tumeda-dev/`。骨格designが再利用先とした`facilitate-discussion`、`name-work-directory`、`think-through`、`document-review`と、build-ready後の受け手である`steering`／`task-design`を持つ。

---

## （付録）前回designからの変更

前回designを機能させるための仮説として扱い、直した方が機能すると合意した箇所を記録する。

| 前回designの記述 | 変更後 | 理由 | 参照するdesign section |
| --- | --- | --- | --- |
| リポジトリ構成: リポジトリ直下に`CLAUDE.md`（tumeda-dev pluginとgenshijinの適用方針）を置く | 正本を`AGENTS.md`にし、`CLAUDE.md`は`AGENTS.md`へのsymbolic linkにする | Codexは`CLAUDE.md`を読まず、レールをCodexでも動かす場合にプロジェクト指示が渡らない | [file成果物](#file成果物) |
| 問いに答えるまでの流れ: 全問いが閉じたら出口を判定する | 全問いが閉じた時に加え、なぜ作るか層が閉じた時点でも出口を判定する | 作らないと分かった後も下位層の問いに答え続けることを防ぐ | [出口判定の時期](#出口判定の時期) |
| プロダクト1件のディレクトリ: 正本`idea.md`（仮称） | 正本の配置と構成を`product-plans/README.md`一箇所で定め、仮置きとして`README.md`の1枚とする | 正本の分量は実際に通すまで分からず、仮置きの影響を一箇所に閉じるため | [file成果物](#file成果物) |
| skill一覧: 層ごとに4種の層skill（なぜ作るか層を閉じる等）を置く | 一つの`settle-question`にまとめ、層ごとの内容は層fileへ移す。skillは14種から11種になる | 起動条件は全体制御が判定し、参照先は問いのidentifierで決まり、落とし穴は層fileへ移したため、層ごとの分岐が要らない。層skillは共通手順を除くと層fileの繰り返しだった | [skillの役割と能力境界](#skillの役割と能力境界) |
| 問いに答える流れ: 層の問いに答える | 答える前に、一般の問いをこのアイデアの問いへ立て直し、詰める深さを問いごとに配分する | 一般の問いと一般の満たさない例では、アイデアに特有の浅い通過が残る | [skillの役割と能力境界](#skillの役割と能力境界) |
| リポジトリ構成: 運用skillを`.claude/skills/`に置く | 正本を`.agents/skills/`に置き、`.claude/skills`はそこへのsymbolic linkにする | レールをCodexでも動かす可能性があり、Claude Codeだけが読む場所では機能しない | [file成果物](#file成果物) |

---

## （付録）変更の実行区分

### task-design内で対象成果物へ適用済み

| 対象 | 反映内容 | validation結果 | 参照するdesign section |
| --- | --- | --- | --- |
| `what-defines-a-product/README.md`（1回目） | 論点13の見出し構成で作成。約束の部分（問いの書き方、identifier、系統、水準、定石、粒度、材料の識別子）を固め、他の見出しは前回designの内容で仮に書いた | 作成時観点（内容の濃さ、記法、命名、指示対象、機密性、暫定性）でreviewし、問いの選び方の判定方法と定石の具体例を補った。利用者が実fileをreviewし「ok」 | [知識体系](#知識体系what-defines-a-product) |
| `.agents/skills/`配下のskill11種、`.agents/skills/grow-product-idea/templates/canonical.md`、`product-plans/README.md`、`.claude/skills`、リポジトリの`README.md` | 論点17の委託で一度skill14種と共有fileを作り、論点18〜22で作り直した。層skill4種を`settle-question`にまとめ（論点20〜22）、層skillの内容のうち層fileと重ならない材料の順序の理由・要求の優先度・`core-logic`を先に揃えることを層fileへ移した。`grow-product-idea/references/`と`templates/layout.md`・`material.md`を無くし、配置と材料の入口の形を`product-plans/README.md`へ、材料skillへ渡すものと材料skillが答えないことを`what-defines-a-product/README.md`の「材料」節へ移した（論点18）。自演への言及を恒久のfileから削った（論点19） | 受け入れ基準の一つ目を作り直し後に確認した。skill11種が名前どおり存在しfrontmatterの`name`が一致し`.claude/skills`経由で読めること、材料の識別子8種が表と材料skillの宣言で一致し層fileの要求とも一致すること、配置のfile名を書くのが`product-plans/README.md`と正本の雛形だけであること、参照される問いのidentifierが全て定義されていること、リポジトリ内のmdの相対linkに切れが無いこと | [file成果物](#file成果物)、[アイデアを通すworkflow](#アイデアを通すworkflow) |
| `what-defines-a-product/README.md`（2回目） | 作る順の7番目として、仮に書いた見出しをskillと照らした。「問いの選び方」を、上位層が閉じていない間は下位層の問いを選ばず、下位層の材料は問いに答えるskillが直接取りに行く形へ直した（workflowとの整合） | 冒頭の案内表の引き先が、各skillが実際に引く見出しと一致することを確認 | [知識体系](#知識体系what-defines-a-product) |
| `what-defines-a-product/how-far-to-build.md`、`what-defines-a-product/how-to-build.md` | 論点17により問いの一覧の合意を省いて作成。`how-far-to-build.md`は3問（最初に作る分、運用で都度解決するもの、AIが聞かずに進めてよい範囲）、`how-to-build.md`は5問（体験、画面、テーブル、モジュール、後から返済する負債） | 作成時観点でreview。四層file全体で、相対linkの切れが無いこと、参照される問いのidentifierが全て定義されていること、材料の識別子8種が全てどこかの問いから要求されていることを確認した。利用者への報告済み、矛盾が見つかれば作り直す | [知識体系](#知識体系what-defines-a-product) |
| `what-defines-a-product/what-to-build.md` | 論点16の3問を作成。各問いに必要な材料、水準、定石を書いた | 作成時観点でreview。一段目の記述位置を水準の節へ揃え、`why-to-build.md`も同じ位置へ直した。利用者は論点17で、問いの多くが前回designから導かれたものとして受け入れた | [知識体系](#知識体系what-defines-a-product) |
| `what-defines-a-product/why-to-build.md` | 論点15の5問を、READMEの問いの書き方に従って作成。各問いに必要な材料、水準（満たさない答えの例と一段目）、定石（選択肢、判断軸、個人版への翻訳と落ちる精度）を書いた | 作成時観点でreview。他の問いの答えを材料にする書き方がREADMEに無かったため、READMEの約束（必要な材料、一段目）へ追記した。利用者が実fileをreviewし「ok」 | [知識体系](#知識体系what-defines-a-product) |
| `AGENTS.md`（利用者が適用） | 冒頭の「設計の正本は`.steering/2026/202609/20260912-design-build-ready-idea-lab-skeleton/design.md`」を削除。使い方と構成はリポジトリの`README.md`、設計の記録は`.steering/`が持つため | 利用者が直接編集。`git show HEAD:CLAUDE.md`との差分が、この削除と論点6の2行だけであることを確認 | [file成果物](#file成果物) |
| `AGENTS.md`、`CLAUDE.md` | 旧`CLAUDE.md`の本文を`AGENTS.md`へ移し、自己参照の2行を`AGENTS.md`へ変更。`CLAUDE.md`を`AGENTS.md`へのsymbolic linkにした | `git show HEAD:CLAUDE.md`と`AGENTS.md`のdiffが35行目・37行目の2行だけであること、`CLAUDE.md -> AGENTS.md`のlinkが成立していることを確認 | [file成果物](#file成果物) |

### task-design内の対象成果物反映待ち

| 対象 | 待つ理由 | 依存decision | 参照するdesign section |
| --- | --- | --- | --- |
| 作成した全file | 受け入れ基準の二〜四つ目（自演、新しいsessionでの読込み、build-readyの読み切れ）を確かめ、摩擦があれば直す。自演の前に利用者がsessionを再開する | 自演の結果 | [受け入れ基準](#受け入れ基準) |

### execution plan対象

なし
