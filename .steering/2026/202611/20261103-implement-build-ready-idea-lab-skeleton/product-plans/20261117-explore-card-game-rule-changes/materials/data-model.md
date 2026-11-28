# data-model

## 依頼と粒度

| 依頼した層と決めるもの | 何のため | 求めた粒度 | この材料で満たしたか |
| --- | --- | --- | --- |
| [設計](../how-to-build/README.md) | W1/W3/W5の同一性と追跡を支える | 読書きと制約を使える具体の構造 | snapshot案との比較、実例、検証と修正を返す |

## 中身

### 必要な読取り・変更から情報を導く

開始で規則と順を固定、手の後で結果を再生、比較で二つの経過と理由を並べ、再開で保存済みの対象を選ぶ。見込みは操作時の任意入力だけが出どころ。初期入力に無い過去の理由を埋める列を作らない。時刻は補助で、同一性・先後の根拠はroot/node/親。

snapshot配列だけの案は楽だが、結果だけの修正で根拠が割れる。rootと親を持つ行いの木は枝の分かれ目を指せ、六手なら再生負担も小さい。後者を設計の候補として返す。

### 保存するJSONの型と制約

一つのdocument: schema=1（整数）、revision（0以上の整数）、roots（配列）、nodes（配列）、annotations（配列）。IDは各種類のprefixとUUID、文書内で一意。ID同一は同じ記録、名前が似ていても同一としない。

- root: id、ruleがV0又はV1、deckが12個の札ID全てを各一回含む配列、originRootがnull又は比較元rootのID。初期蓄え3・手札3・上限6・六手はschema1の規則へ固定。rootは作成後変更不可。
- node: id、rootId、parentId（rootの初期nodeならnull）、action（初期ならnull、それ以外は{kind:rest}又は{kind:play,card:札ID}）、expectation（文字列又はnull）。初期nodeはrootごとに一つ。parentは同じrootの既存node、循環無し、深さは6まで。各行いが中核規則で成立することを検証する。ノードは追記だけで変更・削除不可。
- annotation: id、nodeId、kindがevaluation又はcorrection、text（空でない文字列）。後からの評価・誤記訂正はここへ追記する。元のexpectationを消さず表示に両方を置く。評価を当時の見込みへ昇格させない。
- 派生値: 手札、山札位置、蓄え、得点、手数、終了は保存値を正とせずrootとnode経路から毎回再生する。

### 一件の保存・分岐と読取り

例の短いIDは説明用であり本実装のID生成仕様ではない。

```json
{"schema":1,"revision":3,"roots":[{"id":"r0","rule":"V0","deck":["A2","B5","A3","B2","A6","B1","A4","B3","A1","B6","A5","B4"],"originRoot":null}],"nodes":[{"id":"n0","rootId":"r0","parentId":null,"action":null,"expectation":null},{"id":"n1","rootId":"r0","parentId":"n0","action":{"kind":"play","card":"A3"},"expectation":"小さい札を残したい"},{"id":"b1","rootId":"r0","parentId":"n0","action":{"kind":"play","card":"A2"},"expectation":null}],"annotations":[]}
```

r0/n0からn1を再生すると蓄え0、得点3、[A2,B5,B2]。b1なら蓄え1、得点2、[B5,A3,B2]。二つを比較すると共通の親n0と異なる初手を示せる。b1の理由は未記録で、n1の文字を流用しない。b1へ「次はA3を試したい」とevaluationを追記しても当時の見込みにはならない。n1の誤記はcorrectionで元と訂正を両表示する。誤った手そのものは親から別の枝にする。

V1のr1はr0のdeckを複製しoriginRoot=r0、初期node m0を作る。r0のn1をr1の親へ付ける更新は拒否。originRootの一致だけでは規則一致とは言わず、compareはrule/deck/行いを実際に照合する。

### 検証と破損の扱い

load時にschema、型、全ID重複、参照、rootごとの初期node、親の同根と循環、札集合、各経路の合法性を検査する。未知schema、欠けた親、7手、非法な行い、壊れたJSONなら全体を読取りエラーとし、自動上書きしない。UUIDの衝突は作成を中止し別IDを取り直す。
固定lockを取得してから最新revisionを読む。追加後にrevision+1の全量を切替。比較・表示は変更しない。外の手編集・同期待ちは支援せず、書換え発見後は止める。移行が必要な将来schemaは別設計へ戻す。

### 必要な保証

木をJSONへ置くだけで安全にはならない。最新読取り→全制約確認→追加→同filesystem切替の一回を排他で行う必要がある。比較の表示へはrootの規則・順、親の経路、expectation/annotationを分けて渡す。これは[構成](implementation-structure.md)と[表示](experience-sketch.md)への問いとして依頼元へ返す。

## 確かめた方法と限界

design-data-modelを、読書き→意味・出どころ・同一性→snapshotと木の差→型と制約→具体JSONの再生・別rootと誤記→必要な保証の順に適用。保存例は設計用で実利用データではない。全量データが大規模でも速い等の性能保証はしていない。
