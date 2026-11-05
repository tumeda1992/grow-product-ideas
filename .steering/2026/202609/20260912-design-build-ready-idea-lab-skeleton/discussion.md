# 議論記録（steering固有）

## 論点1: Ready result後の必須gateの結果

**ステータス:** 決定

**種別:** レビュー指摘

### イテレーション0: 三つのgateを通した結果を記録する

#### 提案0

`task-design` が `planless_complete` を返したため、steeringの必須gate（doc-enricher提案mode、discussionを元にした再発防止review、steering skill自身の確認）を実行した。

##### 4-1. doc-enricher（提案mode）

提案なし。既存docs（`docs/README.md` の5群、`think_standards/README.md` の場面一覧、`development_standards/`）を確認したうえで、候補をすべて落とした。

落とした理由の内訳は次のとおり。

- レビューを一言コメントにしない、レビュー結果から方向性を帰納する、評価基準を到達可能な水準へ合わせる、名前空間の中で評価する: Gate G（`task-design-discussion.md` の論点13と重複）
- 層は工程ではなく依存方向であり、答えと材料の供給は逆方向: Gate G（論点4と重複）
- `entity_modeling/core.md` への失敗例追記: この基準は最初から正しく適用でき、誤った前提を持たなかったため不要
- `grow-product-ideas` の README: 実体作成は次段階であり対象外
- 品質担保を材料の有無で行う: `grow-product-ideas` 固有の設計であり `design.md` に記載済み。一般原則へ上げると既存群のどれにも該当せず、新規docs作成は禁止

escalate時の判断材料として、論点13の内容のうち「レビューの詳細度」「方向性の帰納」「評価基準を到達可能な水準へ合わせる」は `think_standards/` の場面に該当する可能性が高い。命名に固有なのは逆翻訳と宣言性の理論である。

##### 4-2. discussionを元にした再発防止review

`task-design-discussion.md` の19論点を見直した。論点2・論点4・論点13でカバーされない失敗が一つ残った。

**facilitate-discussion の契約を繰り返し守れなかった**

chat先・file後の順で提案を出し、論点12のイテレーション4〜8を記録せず6往復分を事後再構成した。ユーザーから2回指摘を受けた。

三問を当てた結果は次のとおり。

1. 共有されていなかった前提は「記録の遅延は複利で効く」ことである。1回遅らせると次も遅らせやすくなり、6往復分が溜まって事後再構成が必要になる
2. `facilitate-discussion` の `SKILL.md` には契約も理由も書かれている。記述の不足ではなく、逸脱を検知する仕組みがないというprocessの不足に見える
3. 書く場所が確定しなかった

ユーザーの判断により escalate しない。

> facilitate-discussion の契約を繰り返し守れなかった
> の件については再発防止できる具体がわかってればエスカレーションしたいけど、頑張る、間違えないようにする、くらいしか候補がなさそうだから、スルーせざるを得ない

再発防止策が「頑張る」「間違えないようにする」の水準にとどまるなら、書いても機能しない。具体的な検知手段が見つかった時点で改めて扱う。

他の失敗は既存論点でカバーされる。論点のscope肥大は論点4（タスクを進めたい衝動が構造の選択を歪める）と根が同じ。検算依頼と同じ質問の繰り返しは論点13。`design.md` の用語が議論に追随していなかった点（ラボ、観点カタログ、標準、アイデア1件）は、`task-design` Step 4 のStage 2（目視通読）で検出できたためskillの不足はない。

##### 4-3. steering skill自身の確認

変更不要。

steeringは初回task-design起動前の境界を守り、必須gateも機能した。doc-enricherの候補がすべて「escalate論点と重複」で落ちたのは、「同じoriginating decisionについてreview済みなら重複提案しない」という契約どおりの動作である。

#### 提案0へのフィードバック

**結果:** 4-2で残った一件について、再発防止の具体がないためescalateしないことを確認。

> facilitate-discussion の契約を繰り返し守れなかった
> の件については再発防止できる具体がわかってればエスカレーションしたいけど、頑張る、間違えないようにする、くらいしか候補がなさそうだから、スルーせざるを得ない

### 決定

必須gate三つを完了した。

- doc-enricher: 提案なし。候補はすべて既存のescalate論点と重複、または対象外
- 再発防止review: 新たな再発防止先は立てない。`facilitate-discussion` の契約違反は、再発防止策が「頑張る」水準にとどまるため見送る
- steering skill: 変更不要

`tumeda-dev` pluginへのescalateは、`task-design-discussion.md` の論点2・論点4・論点13が持つ。escalate先（`naming/` か `think_standards/` か）の判定は、escalate起動時に行う。
