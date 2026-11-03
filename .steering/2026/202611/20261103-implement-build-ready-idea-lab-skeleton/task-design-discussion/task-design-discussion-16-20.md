# 議論記録（論点16〜20）

## 論点16: `what-to-build.md`の問い

**ステータス:** 決定

**種別:** TBDヒアリング

### イテレーション0（論点16）: 問いの一覧

#### 提案0（論点16）

`what-to-build.md`に、次の3問をこの順で置く。各問いの水準と定石の本文は、合意後に実fileへ書く。

| 順 | identifier | 文面 | 系統 | 必要な材料（粒度） |
| --- | --- | --- | --- | --- |
| 1 | `what-to-build/requirements` | 何を満たせば、痛みが解けたと言えるか | 調査系 | `why-to-build/pain-to-solve`の答え、`why-to-build/existing-alternatives-fall-short`の答え |
| 2 | `what-to-build/solution-shape` | どんな形の道具で解くか | 生成系 | 1の答え、`experience-sketch`（解き方の案ごとに、主要な操作の流れが分かる程度） |
| 3 | `what-to-build/scope-in-and-out` | スコープの内と外はどこか | 生成系 | 1・2の答え、`cost-comparison`（スコープの案ごとに作る時間を比べられる程度） |

##### この層と「どこまで作るか」層の境界

この層は、そのプロダクトが扱う範囲（内と外）を決める。「どこまで作るか」層は、その範囲の中で、最初に作る分と運用で済ませる分の線を決める。

##### 置かない問い

- 最初に作る分の区切り: 「どこまで作るか」層が持つ。
- 性能や可用性などの非機能の細部: 痛みに直結するもの（例: 毎朝7時に必ず届く）は1の要求に含め、それ以外は「どう作るか」層で扱う。

#### 検討記録（論点16・イテレーション0）

閉じ条件「スコープの内側と外側が言える」には、内と外を分ける基準（要求）、内に何が入るかを決める解き方の形、そして線そのものが要る。この三つを問いにした。

- 要求（1）は、`why-to-build`層で確定した痛みと、代案で残る痛みから導くため、材料が揃えば決まる調査系とした。
- 解き方の形（2）は、同じ要求でも通知で解くか、記録画面で解くか、自動化で解くかで内に入るものが変わり、材料が揃っても一つに決まらないため生成系とした。案ごとの操作の流れを比べるため、粗い`experience-sketch`を使う。
- 内と外の線（3）は、前回designが弱い領域として挙げた「スコープの伸縮」にあたり、狭く取る・広く取る等の複数案から選ぶため生成系とした。案ごとの作る時間を比べるため`cost-comparison`を使う。

順は、要求が変われば解き方とスコープが変わり、解き方が変わればスコープが変わるため、1 → 2 → 3とした。

「どこまで作るか」層との境界を、扱う範囲（この層）と、その範囲の中で最初に作る分の線（どこまで作るか層）で分けた。前回designの各層の「問うこと」から導いた。

[内部検討記録: 論点16・イテレーション0](../internal-records/task-design-discussion.md.topic-16.md#iteration-0)

#### 提案0へのフィードバック（論点16）

**結果:** 合意

> ok

### 決定（論点16）

`what-to-build.md`に次の3問を、この順で置く。

| 順 | identifier | 文面 | 系統 | 必要な材料（粒度） |
| --- | --- | --- | --- | --- |
| 1 | `what-to-build/requirements` | 何を満たせば、痛みが解けたと言えるか | 調査系 | `why-to-build/pain-to-solve`の答え、`why-to-build/existing-alternatives-fall-short`の答え |
| 2 | `what-to-build/solution-shape` | どんな形の道具で解くか | 生成系 | 1の答え、`experience-sketch`（解き方の案ごとに、主要な操作の流れが分かる程度） |
| 3 | `what-to-build/scope-in-and-out` | スコープの内と外はどこか | 生成系 | 1・2の答え、`cost-comparison`（スコープの案ごとに作る時間を比べられる程度） |

- この層はプロダクトが扱う範囲（内と外）を決め、「どこまで作るか」層はその範囲の中で最初に作る分と運用で済ませる分の線を決める。
- 最初に作る分の区切りは「どこまで作るか」層が持つ。非機能は、痛みに直結するものだけを1の要求に含め、それ以外は「どう作るか」層で扱う。

## 論点17: 残りの層fileの作り方

**ステータス:** 決定

**親論点:** 論点3

**種別:** TBDヒアリング

### イテレーション0（論点17）: 問いの一覧の合意を省いて作るか

#### 提案0（論点17）

この論点は、利用者からの進め方の指示を受けて開いた。assistantの提案は無く、利用者の指示を受領して決定とした。

#### 検討記録（論点17・イテレーション0）

論点3で、各fileは「見出し構成の合意 → 作成 → 実fileのreview」で作ると決め、層fileでは問いの一覧を見出し構成として合意してきた（論点15、16）。`what-to-build.md`の作成後、利用者から次の指示があった。

利用者の観察は、問いの一覧の多くが前回designの決定から導かれており、合意の場面が判断の場面になっていない、というものである。合意の手間に対して、確かめられることが少ない。実fileと自演の方が、矛盾や摩擦を見つけやすい。

#### 提案0へのフィードバック（論点17）

**結果:** 進め方の指示を受領

> もう基本的に前steeringで決議したやつばっかだから、okって思考停止で言ってる。ここらへん一帯は１回作っちゃっていいよ。後で矛盾起きたら作り直す勢いで

### イテレーション1（論点17）: skill群も同じ進め方にするか

#### 認識合わせ1（論点17）

層fileの作成後、「ここらへん一帯」にskill群（全体制御、層、材料、還元）を含むかを確認した。含むなら14種を一度に作ってまとめて報告し、含まないなら`grow-product-idea`の見出し構成から一つずつ合意する、と示した。

#### 検討記録（論点17・イテレーション1）

決定（論点17）の時点で、指示がskill群まで含むかを読み取れなかったため確認した。skillは層fileより手順の判断が多い。

#### 認識合わせ1への回答（論点17）

**結果:** 回答あり（層fileは合意、skillも作ってよい）

> できたファイルについてはok。skillも既に前steeringで合意済みなら一旦作ってみちゃっていいよ。運用に耐えられなさそうなら相談してもらって

### 決定（論点17）

残りの層file、skill群、テンプレート、リポジトリの`README.md`は、見出し構成や問いの一覧の合意を挟まずに、assistantが一度に作る。

- 根拠にするのは、前回designとこれまでの論点で合意済みの内容である。層fileの問いは、層の閉じ条件と問うことから導き、`what-defines-a-product/README.md`の問いの書き方に従う。
- 作成後、assistantが作成時観点でreviewし、作ったものと判断を利用者へ報告する。後で矛盾が見つかれば作り直す。
- 合意済みの内容から一意に決まらず、運用に耐えられるか疑わしい判断に当たった場合は、作成後に利用者へ相談する。
- 作成済みの`how-far-to-build.md`と`how-to-build.md`は利用者が受け入れた。

## 論点18: 複数のskillが共通で使うfileの置き場所

**ステータス:** 分解済み

**種別:** レビュー指摘

### イテレーション0（論点18）: 自己レビューと置き直し方

#### 提案0（論点18）

層skillの共通手順`answering.md`、材料skillの共通の約束`making-material.md`、`product-plans/<slug>/`の配置`layout.md`と雛形を、どのskillにも属さない共有の場所へ移す。

```text
.agents/
├── product-plan-conventions/       # skillをまたぐ約束。どのskillにも属さない
│   ├── layout.md                   # product-plans/<slug>/ の配置と名前（論点9・10）
│   ├── answering.md                # 層skill共通の答える手順
│   ├── making-material.md          # 材料skill共通の約束
│   └── templates/
│       ├── canonical.md            # 正本の雛形
│       └── material.md             # 材料の入口の雛形
└── skills/
    └── grow-product-idea/
        └── SKILL.md                # references/ と templates/ を持たなくなる
```

- 各skillは`.agents/product-plan-conventions/`を参照する。依存は、全てのskillから共有の場所への一方向になる。
- `.agents/skills/`の外に置くのは、skillのloaderがskillでないdirectoryをどう扱うかを確かめていないためである。
- `making-material.md`の「育て方」は、`what-defines-a-product/README.md`の「粒度と再利用」と重複しているため、そちらを参照する形にする。
- 論点9・10の「配置は全体制御skillのテンプレート一箇所で定める」は、「`.agents/product-plan-conventions/layout.md`の一箇所で定める」に変わる。一箇所で定めることは変えない。

#### 検討記録（論点18・イテレーション0）

自己レビューの結果、置き場所は「全体制御skillはレールの入口でテンプレートも持っているから」という理由で、置ける場所に置いた判断だった。誰が持ち主で、誰が誰に依存するかを確かめていない。

問題は四つある。

- 持ち主と場所が一致しない。`answering.md`は層skillの手順、`making-material.md`は材料skillの約束であり、`grow-product-idea`はどちらも使わない。pathを見た人は`grow-product-idea`の持ち物だと読み、`grow-product-idea`を直す人が層skillや材料skillの振る舞いを変えてしまう。
- 依存の向きが両方向になる。`grow-product-idea`は層skillを起動する側であり、起動される側の層skillが起動する側の中身に依存している。
- skill名は暫定であり（論点8）、`grow-product-idea`の名前を変えると12種のskillの参照が全て切れる。
- `making-material.md`の「育て方」は、既に書いた`what-defines-a-product/README.md`の「粒度と再利用」と重複している。

テンプレートと`layout.md`も同じ問題を持つ。論点9・10では「全体制御skillがdirectoryを作る」ことを理由に全体制御skillへ置いたが、材料skillも雛形を使い、全てのskillが配置を引くことを確かめていなかった。

置き直し方として、共有の場所へ移す案、各skillへ書き写す案、層skill4種を一つにまとめて共通手順の共有自体を無くす案を比べた。書き写す案は12か所の同期が要る。まとめる案は前回designのskill一覧を変える大きな変更であり、この指摘の範囲を越える。共有の場所へ移す案なら、持ち主（レール全体）と場所が一致し、依存は一方向になる。

場所の名前は、`shared`や`common`のような何でも入る名前を避け、中身（`product-plans/<slug>/`を作り、問いに答え、材料を作る時の、skillをまたぐ約束）を表す`product-plan-conventions`にした。

[内部検討記録: 論点18・イテレーション0](../internal-records/task-design-discussion.md.topic-18.md#iteration-0)

#### 提案0へのフィードバック（論点18）

**結果:** 修正要求（fileごとに、約束かskillかを判断する）

> 18についてはそれぞれ個別で考えてほしいんだけど、conventionなのか、これ自体独自スキルなのか

提案0は、四種類のfileをまとめて「skillをまたぐ約束」として一つの場所へ移す案だった。fileごとに、約束（形や置き方を定め、複数の担当が読むもの）なのか、それ自体が独立したskill（入力を受けて手順を実行し、結果を返すもの）なのかを判断し直す。

### イテレーション1（論点18）: fileごとに約束かskillかを判断する

#### 提案1（論点18）

| file | 判断 | 理由 | 行き先 |
| --- | --- | --- | --- |
| `layout.md` | 約束 | 手順を持たず、`product-plans/<slug>/`の形と名前、directoryの中だけで読み切れるようにする規則を定める。全てのskillが読む | `product-plans/README.md`。約束が治めるdataの隣に置き、`product-plans/`を開いた人がまず読む |
| `canonical.md`（正本の雛形） | 約束 | 正本の形を定める。全体制御skillが作り、層skillが書き、還元skillが読む | `product-plans/templates/canonical.md` |
| `material.md`（材料の入口の雛形） | 約束 | 材料の入口の形を定める。材料skillが作り、層skillと全体制御skillが読む | `product-plans/templates/material.md` |
| `making-material.md` | 約束。ただし独立したfileにしない | 中身は、受け取るもの、置き方、育て方、書き方、持たないもの。置き方は`layout.md`、育て方は`what-defines-a-product/README.md`の「粒度と再利用」、限界の書き方は`material.md`の雛形と重複している。重複を除くと、残るのは「層skillが材料skillへ渡すもの」だけになる | fileを無くす。重複は既存の正本へ寄せ、渡すものは`what-defines-a-product/README.md`の「材料」節へ足す |
| `answering.md` | skill | 入力（`product-plans/<slug>/`と問いのidentifier）を受け、材料を揃え、対案を比べ、記録し、漏れを確認して「閉じた」を返す、一つの手順である | 論点20で扱う。skillにすると、層skill4種との関係が変わるため |

- `product-plans/templates/`は、slug（`YYYYMMDD-`で始まる）と名前で区別できる。
- 論点9・10の「配置は一箇所で定める」は変えず、その一箇所を`product-plans/README.md`にする。
- 変更後、各skillは`product-plans/README.md`と`product-plans/templates/`を参照する。依存は、全てのskillから`product-plans/`の約束への一方向になる。

#### 検討記録（論点18・イテレーション1）

利用者の問いは、fileごとに「約束なのか、それ自体が独自のskillなのか」である。分ける基準を、手順を持つかに置いた。

- 約束は、形と置き方を定め、手順を持たない。複数の担当が読む。
- skillは、入力を受けて手順を実行し、結果を返す。前回designのskillを立てる基準「そのskillが無いと、agentが参照先または手順を毎回自分で決めることになるか」に当たる。

`layout.md`と雛形二つは手順を持たず、`product-plans/<slug>/`の形を定める約束である。約束が治めるdataの隣、`product-plans/`に置けば、持ち主（`product-plans/`という置き場所の約束）と場所が一致し、`product-plans/`を開いた人がまず読める。提案0の`.agents/product-plan-conventions/`は、agentだけが読む場所に見えるが、この約束は利用者も読む。

`making-material.md`を見直すと、中身のほとんどが既存の正本と重複していた。置き方は`layout.md`、育て方は`what-defines-a-product/README.md`の「粒度と再利用」、限界の書き方は`material.md`の雛形にある。独立したfileとして残すと、同じ内容の正本が二つになる。重複を除いて残る「層skillが材料skillへ渡すもの」は、材料の識別子と同じく層skillと材料skillの間の約束なので、`what-defines-a-product/README.md`の「材料」節へ足す。

`answering.md`は、入力を受け、手順を実行し、「閉じた」を返す。手順そのものであり、skillである。skillにすると、同じ手順を共有している層skill4種がそれぞれ何を足しているのかが問われるため、別の論点20で扱う。

[内部検討記録: 論点18・イテレーション1](../internal-records/task-design-discussion.md.topic-18.md#iteration-1)

#### 提案1へのフィードバック（論点18）

**結果:** 部分合意（`making-material.md`と`answering.md`の行き先は合意。雛形の行き先に問い）

> 1の元々templatesにあったものって、grow-product-idea/templatesのままじゃだめなの？このスキルでしか使わないんじゃない？ referencesの行き先については合意。論点20はbで

`answering.md`と`making-material.md`の行き先（提案1の表の該当行）は合意。`grow-product-idea/templates/`にあった三つのfileは、`grow-product-idea`だけが使うならそのままでよいのではないか、という問いがあった。

### イテレーション2（論点18）: templatesの三つを、誰が使うかで分ける

#### 提案2（論点18）

`grow-product-idea/templates/`の三つを、実際に誰が使うかで分ける。

| file | 使う担当 | 行き先 |
| --- | --- | --- |
| `canonical.md`（正本の雛形） | `grow-product-idea`だけ。受け入れ時に正本を作る。他のskillは作られた正本を読み書きし、雛形は読まない | `grow-product-idea/templates/`のまま |
| `layout.md`（配置と名前、外を参照しない規則） | 全てのskill。問いに答えるskillは正本と材料の入口の場所を、材料skillは入口の場所を、還元skillは読む場所を引く | `product-plans/README.md` |
| `material.md`（材料の入口の雛形） | 材料skill8種。`grow-product-idea`は使わない | `product-plans/README.md`の中に、材料の入口の形として書く。`making-material.md`を無くすため、雛形を単独のfileで持つ理由も無くなる |

`grow-product-idea`は、正本の場所と形を`product-plans/README.md`で引き、正本の雛形だけを自分で持つ。

#### 検討記録（論点18・イテレーション2）

提案1は、三つをまとめて`product-plans/`へ移す案だった。利用者の問いを受けて、各fileを実際に参照しているskillを`grep`で確かめた。

- `canonical.md`を参照しているのは`grow-product-idea/SKILL.md`と`layout.md`だけである。他のskillは、作られた正本を読み書きするが、雛形は読まない。`grow-product-idea`だけが使うため、そのままでよい。提案1は、置き場所を一つの約束にまとめることを優先し、使う担当を確かめていなかった。
- `layout.md`は、`grow-product-idea/SKILL.md`、`answering.md`、`making-material.md`、`refine-what-defines-a-product/SKILL.md`が参照している。問いに答える手順も材料を作る約束も使うため、`grow-product-idea`だけのものではない。
- `material.md`は、材料skill8種が`making-material.md`を通して使い、`grow-product-idea`は使わない。

[内部検討記録: 論点18・イテレーション2](../internal-records/task-design-discussion.md.topic-18.md#iteration-2)

#### 提案2へのフィードバック（論点18）

**結果:** 合意（論点22の合意と一緒に受けた）

> ok

論点22の提示の最後に、assistantは「OKなら、論点18（提案2）・19・20・22の内容でまとめて作り直す」と添えた。

### 決定（論点18）

複数のskillが使うfileを、fileごとに約束かskillかで判断して置き直す。

- `layout.md`（`product-plans/<slug>/`の配置と名前、directoryの中だけで読み切れるようにする規則）は約束であり、`product-plans/README.md`へ移す。論点9・10の「配置は一箇所で定める」の一箇所はここになる。
- 正本の雛形`canonical.md`は`grow-product-idea`だけが使うため、`grow-product-idea/templates/`に残す。
- 材料の入口の雛形`material.md`は材料skillが使うため、`product-plans/README.md`の中に材料の入口の形として書く。
- `making-material.md`は約束だが、置き方・育て方・限界の書き方が既存の正本と重複するためfileを無くす。残る「材料skillへ渡すもの」と「材料skillは問いへ答えない」は`what-defines-a-product/README.md`の「材料」節へ足す。
- `answering.md`はskillであり、論点20・22のとおり`settle-question`の本文になる。
- 理由は、持ち主と場所を一致させ、依存を一方向にするためである。全体制御skillの中に共有物を置くと、起動される側が起動する側の中身に依存し、`grow-product-idea`の改名で全skillの参照が切れる。

## 論点19: 自演の扱いを恒久のskillから外す

**ステータス:** 反映済み

**種別:** レビュー指摘

### イテレーション0（論点19）: 診断と直し方

#### 提案0（論点19）

- 正本の雛形`canonical.md`から「自演」欄を、`grow-product-idea/SKILL.md`から「## 自演」節を削る。
- ユーザー役の回答を区別して残すことは、design.mdの受け入れ基準に従い、自演の時にこのsteeringの手順として行う。自演で作った正本には、その1件の記録として、自演であることを本文に書く。

#### 検討記録（論点19・イテレーション0）

自演は、論点11で決めた、このsteeringの受け入れ基準を確かめる一回の検証である。ユーザー役の回答を区別して残す必要は、その検証の手順に属し、design.mdの受け入れ基準に既に書いてある。

これを恒久のskillと雛形へ書くと、レールを使う全ての後続のアイデアに、一回の検証の都合が残る。一時的な作業の都合と恒久の成果物の機能を分けずに、必要が生じた場所（自演で作る正本）に近い恒久のfileへ書いた。

[内部検討記録: 論点19・イテレーション0](../internal-records/task-design-discussion.md.topic-19.md#iteration-0)

#### 提案0へのフィードバック（論点19）

**結果:** 合意

> 19はok。

### 決定（論点19）

自演は、このsteeringの受け入れ基準を確かめる一回の検証であり、恒久のskillと雛形に書かない。

- 正本の雛形`canonical.md`の「自演」欄、`grow-product-idea/SKILL.md`の「## 自演」節、`refine-what-defines-a-product/SKILL.md`の自演への言及を削る。
- ユーザー役の回答を区別して残すことは、design.mdの受け入れ基準に従い、自演の時にこのsteeringの手順として行う。自演で作った正本には、その1件の記録として本文に書く。

### 現在の変更（論点19）

決定直後に適用済み。上の3fileから自演への言及を削り、`grep -rn "自演" .agents/`で残りが無いことを確認した。

## 論点20: 問いに答える手順をskillにし、層skill4種との関係をどうするか

**ステータス:** 決定

**親論点:** 論点18

**種別:** レビュー指摘

### イテレーション0（論点20）: 層skillが共通手順に何を足しているか

#### 提案0（論点20）

**推奨:** b。

##### a. 共通手順を一つのskillにし、層skill4種はそれを起動する

`answer-question`のような共通のskillを作る。層skill4種は残し、それぞれが自分の層の材料の順序と落とし穴を添えて共通のskillを起動する。

```text
grow-product-idea → answer-why-to-build → answer-question → 材料skill
```

前回designのskill一覧（層4）は変わらない。起動が一段深くなり、層skillは「順序と落とし穴を渡すだけ」のskillになる。

##### b. 層skill4種を一つのskillにまとめ、層ごとの内容は層fileへ移す

層skill4種を一つの「問いに答えるskill」にまとめる。層skillが持っていた内容は、層fileの問いへ移す。

- 材料を取りに行く順序: 各問いの「必要な材料」の並び順を取りに行く順とし、理由が要るものは問いの中に一行添える
- 落とし穴: 各問いの水準の「満たさない例」と重なるものは除き、残るものを水準へ足す

```text
grow-product-idea → （問いに答えるskill） → 材料skill
```

前回designのskill一覧は、層4が1になり、14種が11種になる。skill名は別に決める。

#### 検討記録（論点20・イテレーション0）

論点18で、`answering.md`は入力を受けて手順を実行し結果を返す、それ自体がskillだと判断した。そうすると、同じ手順を共有する層skill4種が、それぞれ何を足しているのかが問われる。

作成した層skill4種を見直すと、足しているのは二つだけだった。

- 材料を取りに行く順序: 各問いの「必要な材料」の並びとほぼ同じであり、理由の一行を足しているだけである。
- 落とし穴: 多くが層fileの水準の「満たさない例」と重複している。例えば`answer-why-to-build`の「『競合はいない』『リスクはない』で終える」は、`why-to-build.md`の満たさない例そのものである。

前回designのskillを立てる基準には、歯止めとして「参照先も手順も既に確定していてskillが何も足さないなら立てない」がある。層skill4種は、共通手順を除くと、層fileの内容をほぼ繰り返している。

aは前回designのskill一覧を保つが、層skillは順序と落とし穴を渡すだけのskillになり、層fileとの重複も残る。bは重複を無くし、起動の段も減る。代償は、前回designのskill一覧（論点2で全て作ると決めた）と、論点7・8の決定を変えることである。論点4で、前回designは機能させるための仮説として扱い、直した方が機能するなら直すと決めている。

[内部検討記録: 論点20・イテレーション0](../internal-records/task-design-discussion.md.topic-20.md#iteration-0)

#### 提案0へのフィードバック（論点20）

**結果:** 合意（b）

> 論点20はbで

### 決定（論点20）

層skill4種を一つの「問いに答えるskill」にまとめ、層ごとの内容は層fileへ移す。

- 共通の答える手順（`answering.md`の中身）を、このskillの本文にする。
- 材料を取りに行く順序は、各問いの「必要な材料」の並び順で表し、理由が要るものは問いの中に一行添える。
- 層skillの落とし穴のうち、水準の満たさない例と重なるものは除き、重ならないものを水準へ足す。
- skillは14種から11種になる。まとめたskillの名前は別の論点で決める。
- 理由は、層skill4種が共通手順を除くと層fileの内容をほぼ繰り返しており、前回designの「参照先も手順も既に確定していてskillが何も足さないなら立てない」に当たるためである。前回designのskill一覧（論点2）と、論点7の担当、論点8の名前を変える。論点4で、前回designは機能させるための仮説として扱うと決めている。
