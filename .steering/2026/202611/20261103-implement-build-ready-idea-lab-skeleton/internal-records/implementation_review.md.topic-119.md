# 内部検討記録: 論点119 — 111〜116の本線改稿と合意の保存

**discussion:** [implementation_review.md](../implementation_review/implementation_review.md)

**論点:** 論点119

## 開始context

利用者の「一旦コミット計画立てて、コミットしてpushして」により、計画とその実行を同じ依頼として受領した。111〜116の採用/反映/局所検査は完了。本線8fileと関連記録12fileが未コミットで、HEAD/実remoteはb30f0ed8f922f96a1e417eb3ac4370a9623bf525、branchはfeature-16、indexは空。既存ケースやsharedの編集、追加のドライランはこの保存の範囲に入れない。

<a id="iteration-0"></a>

## イテレーション0: 論点ごとの本線改稿と根拠を、参照を保って保存する

<a id="iteration-0-record-1"></a>

### 計画: 六つの採用差分を順に保存し、計画と実行結果もGitへ入れる

#### 実差分と保存単位の選択

Gitの実差分は20file、うち本線8fileと記録12file。8fileは六つの採用候補を順に合成した最後のafterと全文一致し、原product-plansとstageは不変だった。recordの場所だけで最後へまとめず、複数論点を含む公開議論と、その固定anchorのある内部記録を第1の111の改稿と一緒に保存する。後続commitの本文は採用の論点/提案番号を指す。
各本線改稿は独立の問いであり、111/112/113/114/115/116の六本へ分ける。同じgrowやhow-to-solve等は採用当時のbefore/afterをindexへ順に載せ、作業treeは最終内容を保つ。第7でこの119/索引/内部記録を、第8で第7までのpushの実結果を保存し、その結果記録もpushする。原文/採否/却下と検証の限界を保持する。

#### 実行前に確かめるもの

隔離copyの各段でpatch/参照/構造と期待treeを検査し、第7の累積を21fileの現物へ一致させる。実行直前に保持したHEAD/index/現物hashを照合する。commit後は対象のblob、tree、parent、messageを確認し、実remote/upstream/HEADを比較してpushの成功を判断する。第8の結果記録は自身のhashを本文へ足す循環を作らず、最後のtool結果で保存/remote/cleanを確認する。

#### 権限と未実施の境界

計画とそのcommit/pushは利用者の一つの明示依頼に含まれるため、追加の採否待ちは作らない。既存commitのamend/rebase、強制push、PR/merge、製品実装やshared改稿はしない。計画を記録した時点ではcommit/pushの成功を記録せず、実行後のtool結果から更新する。


<a id="iteration-0-record-2"></a>

### 検査と第1〜6の作成: 採用差分の順序と、実際のtree/parentを照合する

#### 保存前の中間版の検査

第1〜7の保存内容を隔離copyへ順に構成し、各段の参照/議論構造/期待treeを検査した。第1〜6は118論点、第7は119論点で構造問題無し。保存対象の参照は190/193/197/197/197/197/200件で不成立無し。累積は21fileの実物とbyte一致し、indexは空のままだった。引用diffの文脈の空白一文字だけを保持し、他の空白問題は無かった。

#### 第1〜6で得られた実結果

利用者の明示委託に従い第1〜6を作成した。各commitの対象/staged blob/tree/parent/messageを検査した中間版と照合し、実行前に保持した現物hashが変わっていないこと、各commit後にindexが空であることを確認した。

- 第1: `ce82397a754eca981b6677fd7b8cd61c1f240ef2` — fix: 検査の操作制限と製品の目標範囲を区別する
- 第2: `d740468b55d237dbb18ee48ec3937010a00d5650` — fix: 原状と基準を保って候補の増分を比較する
- 第3: `c15ee9160041310ceb81dddb3614736fd7a5983a` — fix: 検査例の成立する経過と期待値の根拠を渡す
- 第4: `802ea5e3c4b47ddb7d29e4012dd82fd652cd6a0c` — fix: 費用の数値の対象と限界を選定まで保つ
- 第5: `c264114edfece9f31b24ca43935f709f88c9f4e8` — fix: 成果の現在表示と根拠を受渡し時に照合する
- 第6: `661b5cd0067438dbff678f6337c811255945c71a` — fix: 決定反映後の結果返却と文書reviewを接続する

#### 第7とpushの境界

現時点で第7の作成/pushは未実施。この実結果の追記で変わる第7の保存内容を更新して照合し、第7までの通常pushへ進む。新しい通しドライランや元ケースの変更を実施したとはしない。


<a id="iteration-0-record-3"></a>

### 第7までのpush完了: 実remoteと、作成したcommitの最終内容を照合する

#### 観測した結果

第7は`4cb2449afcd50f877ab201acdc3bb53882d7dcc1`。第1〜7を通常のpushでorigin/feature-16へ保存し、実remote/upstream/HEADがこの値へ一致した。保存対象21fileの最終blob/実物と、七つのcommitのparent/tree/message/対象を確認した。第7のpush後に作業treeはcleanだった。詳細は/tmp/grow119-commit-plan/pushed-seven.jsonに保持した。
この観測から119の反映済みと親110の現在の保存状態を同期し、計画済みの第8として結果記録自身をcommit/pushする。第8の成功は未来の結果として書かず、実行後のtool結果で確認する。自身のhashを自身へ書き足す循環は作らない。

#### 文書reviewとorigin119のdoc-enricher一回

文書reviewで、計画と実施済み/未実施を区別し、委託原文から保存単位、実際のcommit/remote/cleanの証拠へ辿れることを確認した。以前の118のpushを今回の保存へ流用せず、原ケースとsharedの未変更、通しドライランの未実施も保持した。
origin119のdoc-enricherを提案modeで一回実施した。steeringのcommit順序/共有議論の扱いと既存のbranchの規範を今回の計画へ照合した。共有記録を先の関連commitへ揃える知識は既存規範にあり、今回のhash/段数/ファイル一覧はこの作業の検証記録に属するため、README/docsへ追加する候補は無い。共有cacheは変更しない。
