# 内部検討記録: 論点19 — 自演の扱いを恒久のskillから外す

**discussion:** [task-design-discussion.md](../task-design-discussion/task-design-discussion.md)

**論点:** 論点19

## 開始context

論点17の委託で、正本の雛形`canonical.md`の状態の節に「自演」欄を、`grow-product-idea/SKILL.md`に「## 自演」節を足した。利用者から「自演って今回のsteeringについてdryrunするだけの話なのに、なんで継続的に使われるskillに書かれるの？」と問われた。

<a id="iteration-0"></a>

## イテレーション0: 診断と直し方

<a id="iteration-0-record-1"></a>

### 診断

自演は、論点11で決めた、このsteeringの受け入れ基準を確かめる一回の検証である。ユーザー役の回答を区別して残す必要は、その検証の手順に属する。
これを恒久のskillと雛形へ書くと、レールを使う全ての後続のアイデアに、一回の検証の都合が残る。

一時的な作業の都合と、恒久の成果物の機能を分けずに、必要が生じた場所（自演で作る正本）に近い恒久のfileへ書いた。

### 直し方

- `canonical.md`から「自演」欄を、`grow-product-idea/SKILL.md`から「## 自演」節を削る。
- ユーザー役の回答を区別して残すことは、design.mdの受け入れ基準（既に書いてある）に従い、自演の時にこのsteeringの手順として行う。自演で作った正本には、その正本の中に自演であることを書く（雛形の欄ではなく、その1件の記録として）。
