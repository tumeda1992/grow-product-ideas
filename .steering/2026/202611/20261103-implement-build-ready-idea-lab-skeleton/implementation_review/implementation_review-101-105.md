# 議論記録（論点101〜105）

## 論点101: 現在の差分を、成立する仕事と取り消す効果に沿ってコミットへ分ける

**ステータス:** 決定

**種別:** コミット計画

### イテレーション0（論点101）: 実差分から保存する仕事と順番を決める

#### 提案0（論点101）

**現在の差分を、以下の17本で保存する計画にする。** 比較元はfeature-16の`6246ecdb9d3c0f9a7e1cf728a8a1ba421239a99d`。初期50fileと、この計画の新記録2fileを対象にする。stage済みは空であり、この論点で決めるのは分割・順序・メッセージと実行時の確認までである。

新しい専門は本文・呼出元・局所確認を一緒にする。同じfile内でも、条件の十分性、部分案の育成、費用の再見積もり等は、取り消す効果が独立しているため分ける。前回のpush完了、保留する改善、Bの区切り、未採用のC案もそれぞれ何を保存したかを明示する。

##### 作るコミットの順番

| 順 | コミットメッセージ |
| --- | --- |
| 01 | `docs: 前回のコミットとpushの完了を記録` |
| 02 | `docs: 各層の発散と収束を結ぶ全体構造の合意を記録` |
| 03 | `feat: 停止と変更の後も続けられる実装構成を設計できるようにする` |
| 04 | `docs: Codexの曖昧な設計の進め方を改善対象として保留する` |
| 05 | `feat: 選定を左右する技術の性質を検証へ依頼して比較へ戻せるようにする` |
| 06 | `docs: 達成条件と版の選定と実現設計の責務を揃える` |
| 07 | `feat: 案件の原事例を既存の保守へ渡して改善を吟味できるようにする` |
| 08 | `docs: 案件内で判断を読み切り公開資料の出典を辿れるようにする` |
| 09 | `feat: 必要な他者の体験を取得し各層の判断へ返せるようにする` |
| 10 | `fix: 反例が浮かばないことだけで条件を十分としない` |
| 11 | `feat: 一巡の改善と残る損失を比べられる部分案を育てる` |
| 12 | `fix: 機能構成を選定前の候補比較にも使えるようにする` |
| 13 | `feat: 比較期間を揃え必要な部分だけ費用を再見積もりできるようにする` |
| 14 | `fix: 材料の変更を閉じた判断と再開後にも受け渡せるようにする` |
| 15 | `docs: 方法整備Bを現行の実行版としていったん閉じる` |
| 16 | `docs: Cの一式試運転の未採用案と検討を保存` |
| 17 | `docs: 現在の差分のコミット分割と検証の計画を記録` |

##### 各コミットへ入れる実物と、戻す時の境界

以下の`W/`は、この作業の`.steering/2026/202611/20261103-implement-build-ready-idea-lab-skeleton/`を表す。それ以外はrepository rootからの相対pathである。同じpathが複数回出る場合はfile全体を繰り返し収録せず、指定した節・文の中間版へ分ける。

###### 01. docs: 前回のコミットとpushの完了を記録

前回計画の作成記録に、6246ecdまでの作成・pushが終わった結果を加える。今回の新しい仕事や新たなpush結果と区別する。

対象file:

- `W/internal-records/implementation_review.md.topic-89.md`

入れる範囲: 末尾の前回実行結果7行。既存のcommitを作り直さない。

取り消す効果: 前回の完了追記だけが消える。Git上の既存commitとリモートへ保存済みの履歴は残る。

依存・制約: 既存HEADのみ。

###### 02. docs: 各層の発散と収束を結ぶ全体構造の合意を記録

Aの内実／Bの表層として、各層の探索・比較・専門材料・受け口と戻りを、有機的な全体として採用した根拠を保存する。Bの詳細とCの成立を済ませたとは扱わない。

対象file:

- `W/design.md`
- `W/implementation_review/implementation_review-81-85.md`
- `W/internal-records/implementation_review.md.topic-83.md`
- `W/implementation_review/implementation_review.md`

入れる範囲: designの全体の育成・判断と受渡し、進め方・境界の83採用部分。83のイテレーション7、決定と反映、内部logの追加51行。既存の却下・未採用の履歴は保持する。後の99のB完了文は含めない。

取り消す効果: 全体構造の今回の採用記録が消える。既存の84〜88の役割の構想・過去の議論は残る。後続の本文整備がこの構造に依るため、基盤だけを単独で取り消す運用はしない。

依存・制約: 既存81〜88の記録。後続の本文整備の基盤。

###### 03. feat: 停止と変更の後も続けられる実装構成を設計できるようにする

構想だけだった実装構成設計を、必要な保証から実行・保存・接続と回復の責任を配置し、案の差・根拠・不足を返せる専門にする。呼べる入口と局所の証拠まで含める。

対象file:

- `.agents/skills/implementation-structure-design/SKILL.md`
- `README.md`
- `what-defines-a-product/README.md`
- `what-defines-a-product/how-to-build.md`
- `.agents/skills/propose-alternatives/SKILL.md`
- `W/design.md`
- `W/implementation_review/implementation_review-86-90.md`
- `W/internal-records/implementation_review.md.topic-90.md`
- `W/implementation_review/implementation_review-91-95.md`
- `W/internal-records/implementation_review.md.topic-92.md`
- `W/implementation_review/implementation_review.md`
- `W/implementation-structure-check/README.md`
- `W/implementation-structure-check/consumer-results.md`
- `W/implementation-structure-check/implementation-structure.md`
- `W/implementation-structure-check/local-regeneration.md`
- `W/implementation-structure-check/probe.py`
- `W/implementation-structure-check/probe-results.json`

入れる範囲: 新SKILL本文全体と局所確認6file。root／共通一覧のimplementation-structure行、how-to-buildの問い・依頼と受領・使用可能一覧の追加、alternativesの作る部分の形の出所、designの当該専門の採用・接続済みの説明。費用期間の後の拡張は13へ分ける。90・92の提案・採用・局所検証と索引。

取り消す効果: 実装構成を作る専門・呼出しと模型の証拠がまとまって消える。既存の機能・情報・技術検証は残る。後で費用や現行版の案内がこの専門を参照するため、それらの依存箇所も戻す必要がある。

依存・制約: 02。外部API・実host・本番費用の実証は含まない。SQLiteの7観測は指定条件の局所確認である。

###### 04. docs: Codexの曖昧な設計の進め方を改善対象として保留する

進め方自体の論点化、階層別の進め方、新iterationでの軌道修正、小ブロックの局所検証という利用者の指摘を、後で扱う改善として保存する。

対象file:

- `W/pending-escalations/007-codex-design-process-and-local-validation.md`
- `W/implementation_review/implementation_review-91-95.md`
- `W/internal-records/implementation_review.md.topic-91.md`
- `W/implementation_review/implementation_review.md`

入れる範囲: 007全文、91の原文・保留報告と内部log、索引の91。ロードマップは候補という所感にとどめる。

取り消す効果: この改善の保留控えと追跡が消える。専門本文と既存のtask-designは変わらない。

依存・制約: 03の90の出来事を根拠にする。shared pluginへの引渡し・改稿・暫定適用は未実施のまま。

###### 05. feat: 選定を左右する技術の性質を検証へ依頼して比較へ戻せるようにする

動かさないと分からない事実を未整備の依頼先として扱っていた選定から、既存の技術検証へ具体の問いを渡し、対象・条件が合う事実と不足を比較へ戻せるようにする。

対象file:

- `what-defines-a-product/how-to-solve.md`
- `.agents/skills/propose-alternatives/SKILL.md`
- `W/implementation_review/implementation_review-91-95.md`
- `W/internal-records/implementation_review.md.topic-93.md`
- `W/implementation_review/implementation_review.md`

入れる範囲: 選定の1の技術の行・依頼条件・受領・費用更新と未知／実験版の境界・揃えば満たした。alternativesの候補の事実の技術への問いと許可範囲・出典の扱いも対応させる。他者の経験の行は09。

取り消す効果: 選定から技術の事実を取得して戻す経路が消える。既存の技術検証本文と、how-to-buildでの利用は残る。

依存・制約: 03の構成材料を問いの具体化へ使える。verify-technical-feasibility自体は既存commitにあり、今回の新規本文には数えない。

###### 06. docs: 達成条件と版の選定と実現設計の責務を揃える

whatは全体の達成条件、how-to-solveは今回届ける版と得失の選定、how-to-buildはその版の実現設計として、呼び名・受け渡す内容・差し戻す判断を一致させる。人と既存道具の行いも版に含める。

対象file:

- `README.md`
- `what-defines-a-product/README.md`
- `what-defines-a-product/why-to-build.md`
- `what-defines-a-product/what-must-hold.md`
- `what-defines-a-product/how-to-solve.md`
- `what-defines-a-product/how-to-build.md`
- `product-plans/README.md`
- `.agents/skills/grow-product-idea/templates/canonical.md`
- `.agents/skills/grow-product-idea/templates/layer-record.md`
- `.agents/skills/sketch-experience/SKILL.md`
- `W/design.md`
- `W/implementation_review/implementation_review-91-95.md`
- `W/internal-records/implementation_review.md.topic-94.md`
- `W/implementation_review/implementation_review-96-100.md`
- `W/internal-records/implementation_review.md.topic-98.md`
- `W/implementation_review/implementation_review.md`

入れる範囲: 94の8fileの責務・戻り先・版全体の引継ぎに、98の残ったhow表記とsketchの「選んだ版」、root／共通のsketchの説明を加える。canonicalの選んだ版の分担・得失と再判断、layer-recordの「物差しと前提」、plansの4層と版の説明。98の一括提案・採否の記録は最も早い対応commitとしてここへ保存し、後続08〜14はcommit本文で98の該当変更を指す。designはこの責務と、sketchの現行の仕事の説明だけ。

取り消す効果: 版を選ぶ判断と設計する判断の整理・呼び名と雛形が戻る。他者の経験の取得、独立した改善の候補、費用を具体化する別の方法までは消さない。

依存・制約: 02・03・05の整備を前提に現在の担当を案内する。独立how-farを追加しない。98の議論の反映済みは当時の作業状態であり、このcommitで98全体の本文まで収録したという意味にはしない。

###### 07. feat: 案件の原事例を既存の保守へ渡して改善を吟味できるようにする

専用の還元skill待ちだった案内を、growから既存のsteering／task-designへ、原事例・未処理の差と当時の方法を渡し、具体の直しと共通化を吟味する循環へする。

対象file:

- `README.md`
- `.agents/skills/grow-product-idea/SKILL.md`
- `W/design.md`
- `W/implementation_review/implementation_review-91-95.md`
- `W/internal-records/implementation_review.md.topic-95.md`
- `W/implementation_review/implementation_review.md`

入れる範囲: rootの「レールを育てる」全文と還元を退避中とする案内、growの責務／やらないこと／参照／全体flow／出口後の引渡し。designの還元の担当・状態とリスク行の「還元skill」から既存保守への補足修正。resumeと公開出典は別の仕事へ分ける。

取り消す効果: 案件から保守へ渡す方法が消える。既存の専門と案件の出口・差し戻し自体は残る。

依存・制約: 02。shared pluginの変更や新しい専用skill・第二の台帳は作らない。

###### 08. docs: 案件内で判断を読み切り公開資料の出典を辿れるようにする

「外へのlinkを全て禁止」と読める規則を、外のrepository内fileへ依存せず判断を内側で読み切り、要点・対象と時点・限界を残した公開資料の出典URLは辿れる規則へする。

対象file:

- `.agents/skills/grow-product-idea/SKILL.md`
- `.agents/skills/grow-product-idea/templates/canonical.md`
- `product-plans/README.md`
- `W/design.md`

入れる範囲: growのbuild-ready前の確認、canonicalの冒頭のlink規則、plansの「directoryの中だけで読み切れるようにする」、designの同じ受入れ条件の出典URLの但し書き。98の該当部分。

取り消す効果: 公開資料の出典URLと案件内の要約の両立を明確にした規則が戻る。後続09の公開投稿を含む材料はこの契約へ依るので、影響を受ける出典の扱いも併せて戻す必要がある。

依存・制約: 06の98の採用記録。repo内の外部参照を新しく許す変更ではない。

###### 09. feat: 必要な他者の体験を取得し各層の判断へ返せるようにする

退避中だった体験取得を、必要な経験と異なる見方を探索・整理し、語りの根拠・着想・支持と反証・不足を返す専門として使えるようにする。予定・勧め・一回を完了や継続に補完しない方法と呼出元まで閉じる。

対象file:

- `.agents/skills/gather-target-user-voices/SKILL.md`
- `README.md`
- `what-defines-a-product/README.md`
- `what-defines-a-product/why-to-build.md`
- `what-defines-a-product/what-must-hold.md`
- `what-defines-a-product/how-to-solve.md`
- `what-defines-a-product/how-to-build.md`
- `.agents/skills/propose-alternatives/SKILL.md`
- `W/design.md`
- `W/implementation_review/implementation_review-76-80.md`
- `W/internal-records/implementation_review.md.topic-78.md`
- `W/implementation_review/implementation_review-96-100.md`
- `W/internal-records/implementation_review.md.topic-96.md`
- `W/implementation_review/implementation_review.md`
- `W/target-user-voices-check/README.md`
- `W/target-user-voices-check/inputs.md`
- `W/target-user-voices-check/provided-experience.md`
- `W/target-user-voices-check/consumer-results.md`
- `W/target-user-voices-check/existing-source-audit.md`
- `W/target-user-voices-check/public-experience.md`
- `W/target-user-voices-check/public-source-observations.json`

入れる範囲: 新SKILL本文と7file。78の新しい採用回・内部log（旧未採用案は維持）、96の各層の依頼と受領。root／共通一覧と退避案内、whyの体験の広げ方、whatの場面への利用、選定の経験の行、設計の認識・引受けへの照合、alternativesの経験・着想の入力と利用。designの当該専門の採用と受渡し。

取り消す効果: 体験を取得する専門と各層の呼出し・局所証拠が消える。本人との対話、原資料による事実確認、他の専門は残る。

依存・制約: 06・08。公開投稿の実際の取得範囲を保持する。架空の提供記録は実在の調査に数えず、現行機能や実際の家族の継続を保証しない。

###### 10. fix: 反例が浮かばないことだけで条件を十分としない

崩れる日を作れなければ十分という判定を、導出・当てた場面と前提・探索範囲・違う手段の判定を合わせて吟味する方法へする。必要な事実の取得先も本人だけに固定しない。

対象file:

- `what-defines-a-product/what-must-hold.md`

入れる範囲: 条件の導出2の十分性の文、4の事実の取得先と揃えば満たした、止める時の答えと根拠。09の他者の経験の依頼文とは分ける。98の該当部分。

取り消す効果: 十分性の過大な保証を抑える変更と事実の取得先の訂正だけが戻る。他者の体験を得る専門と条件の元の導出手順は残る。

依存・制約: 06の98の記録。09を取り消しても、この仕事自体は原資料・既存記録で成立する。

###### 11. feat: 一巡の改善と残る損失を比べられる部分案を育てる

全体案の道具の組合せだけを並べる方法から、対象・期間・担い手・分担を動かし、独立した改善のある部分案も、強い非開発案・現状維持と比較できるようにする。情報が見えるだけで対応が終わるとしない。

対象file:

- `.agents/skills/propose-alternatives/SKILL.md`
- `what-defines-a-product/how-to-solve.md`
- `.agents/skills/grow-product-idea/templates/canonical.md`
- `README.md`
- `what-defines-a-product/README.md`
- `W/design.md`
- `W/implementation_review/implementation_review-96-100.md`
- `W/internal-records/implementation_review.md.topic-97.md`
- `W/implementation_review/implementation_review.md`

入れる範囲: alternativesの目的・入力のmustの意味と比較範囲・候補の探索と止め方・候補×状態の未確認・対案の構成と一巡・品質。how-to-solveの基準の人の判断と対応・選択肢と受渡し・崩れ方と未確認・止め方、canonicalの基準。root／共通のalternativesの部分案の説明、designの当該方法。97と98の該当部分。費用だけの依頼と期間の計算は13。

取り消す効果: 独立した改善を持つ部分案を育てて比べる方法が戻る。既存の未達と損失を合意して選べる規則、全体の条件、他者の体験の取得は残る。

依存・制約: 06・09の現行の入口に接続する。形式のために弱い非開発案や部分案を作らない。

###### 12. fix: 機能構成を選定前の候補比較にも使えるようにする

入力を選んだ版へ狭めていた機能構成を、候補の比較にも使える記述へ揃える。仮の範囲を採用済みへ読み替えない。

対象file:

- `.agents/skills/functional-structure-design/SKILL.md`
- `what-defines-a-product/README.md`

入れる範囲: functionalのdescription・支える判断の冒頭・入力の3箇所、共通一覧のfunctional-structureの行。98の該当部分。

取り消す効果: 選定前にも機能構成の材料を依頼できる明示が消える。既存の選んだ版の機能構成設計と他の専門は残る。

依存・制約: 06の判断と材料を分ける契約。DDDやclass分割を増やす変更ではない。

###### 13. feat: 比較期間を揃え必要な部分だけ費用を再見積もりできるようにする

全段の候補探索と年の回数を前提にする見積もりから、依頼目的に応じて既存の案と根拠を再利用し、同じ対象・期間で増えた部品と人の行いだけ再見積もりできるようにする。

対象file:

- `.agents/skills/propose-alternatives/SKILL.md`
- `what-defines-a-product/how-to-solve.md`
- `what-defines-a-product/how-to-build.md`
- `what-defines-a-product/README.md`

入れる範囲: alternativesの目的別の実施範囲・既存材料の入力と必要な利用者の事実・手順の選択・6の費用の期間／頻度と差・品質の費用の部分。how-to-solveの八軸の手間と続ける時間、how-to-buildの構成から費用へ渡す文の対象場面・比較期間・既存値と増減・外挿の制限、共通依頼の比較期間とalternatives行の再見積もりの説明。98の該当部分。

取り消す効果: 目的に応じた費用だけの依頼と期間の揃え方が戻る。部分案を育てる方法と構成の専門は残る。

依存・制約: 03の構成材料、05の事実の更新、06の版全体、11の比較材料。費用の三点や実測値を今回完成したとはしない。

###### 14. fix: 材料の変更を閉じた判断と再開後にも受け渡せるようにする

閉じた層には知らせない、再開時に受け入れからやり直す、材料は常に表と複数案という説明を直す。依頼・受領・依った値と不足、変更の影響・未処理の差・履歴を保ち、必要な判断だけ更新できるようにする。

対象file:

- `.agents/skills/grow-product-idea/SKILL.md`
- `what-defines-a-product/README.md`
- `product-plans/README.md`
- `.agents/skills/grow-product-idea/templates/layer-record.md`

入れる範囲: growの再開手順と変更時の差し戻し、共通の依頼の語彙・受領の値と根拠・前の依頼の値の変更、plansの材料のfile→directoryの移行・記録形式・依頼と受領・中断中の変更・専門に適した中身、layer-recordの図表本文と依頼／受領欄。06の版全体の前提と08の公開出典は保持する。98の該当部分。

取り消す効果: 閉じた層と再開時への変更受領、入口の移行と履歴の扱いが戻る。個別の専門、期間を揃える見積もり、版の責務は残る。

依存・制約: 06・09・11・13で育てた材料の共通の受領に適用する。外部への連絡や過去の採否の無断変更は含まない。

###### 15. docs: 方法整備Bを現行の実行版としていったん閉じる

本文・接続と局所例の吟味を経たBを、現行の方法としていったん閉じた採否と現在位置を残す。Cの一式適用や実利用は未確認のままにする。

対象file:

- `W/design.md`
- `W/implementation_review/implementation_review-96-100.md`
- `W/internal-records/implementation_review.md.topic-99.md`
- `W/implementation_review/implementation_review.md`

入れる範囲: 99の決定と反映の記録、designの現在位置とBの閉じの2hunk。未特定の家のPC／実APIの77の宿題、80・91の保留を保つ。

取り消す効果: Bをいったん閉じた状態表示と根拠が戻る。整備した専門と方法の本文は残る。

依存・制約: 02〜14の方法と保存済みの局所検証。全体が実際に回ったという保証は増やさない。

###### 16. docs: Cの一式試運転の未採用案と検討を保存

新しい3案件、固定する入力、層と専門の返りごとの検査、設計・引継ぎと出口の判定を、利用者への未採用の具体案として保存する。

対象file:

- `W/implementation_review/implementation_review-96-100.md`
- `W/internal-records/implementation_review.md.topic-100.md`
- `W/implementation_review/implementation_review.md`

入れる範囲: 100の提案0・検討記録・空のフィードバック欄と内部log。designへのC計画の適用とintegration-check／新案件の作成は含めない。

取り消す効果: 未採用のC計画と検討だけが消える。Bの区切りと、Cで一式適用が必要という既存の受入れ条件は残る。

依存・制約: 15の後の提案。応答待ちを保持し、Cの採用・実行済みにはしない。

###### 17. docs: 現在の差分のコミット分割と検証の計画を記録

今回の保存範囲・分割・順番・取り消す効果と未実施の検証を、レビューできる具体の計画として保存する。

対象file:

- `W/implementation_review/implementation_review-101-105.md`
- `W/internal-records/implementation_review.md.topic-101.md`
- `W/implementation_review/implementation_review.md`

入れる範囲: 論点101の計画・内部検討と索引。実行結果は、実際に実行を依頼された後に得た事実だけを別の追記として扱う。

取り消す効果: 今回のコミット計画の記録だけが消える。製品レール・専門と他の論点の採否は残る。

依存・制約: 01〜16の差分の割当てを説明する。計画への合意はstage・commit・pushの許可に替えない。

##### 共有するfileと過去の記録をどう分けるか

README・共通一覧・how-to-buildの使用可能一覧は、03で構成、09で体験取得を加える中間版にする。alternativesの同じ入力表は、03の構成の出所、09の経験の根拠、11の部分案、13の費用だけの依頼に分ける。how-to-solveの技術の問い05、責務06、経験の行09、一巡を比較する11、費用期間13も、実際の採用案のbefore/afterと最終本文から切り出す。一つのhunkに入っていることだけで不可分にはしない。

designの全体構造02、専門の接続03・09、責務06、保守07、出典08、部分案11、Bの完了15を一括で最後へ寄せない。新規の専門を案内する断片は本文と同じcommitに入れる。共有索引には、そのcommitで保存する論点の入口を入れる。
public記録の範囲fileは対応する論点単位で追加する。78・83は今回追加された回と現在状態だけを扱い、過去の却下案や当時の未採用理由を変えない。98は一度に採用・反映した実際の議論であり、複数の架空の合意へ分解しない。steeringの指示に従い最初の対応commit06へ記録を置き、後続のcommit本文から98の該当部分を指す。記録中の「反映済み」は当時の作業状態であって、06だけで98の本文全体を収録したという意味ではない。

01〜17は意味のある仕事又は保存目的で分けた案である。分けられないという理由で、無関係な変更を手順単位へまとめた箇所は現時点では無い。ただし、これは17中間treeを実際に組んで検証済みという報告ではない。

##### 実行を依頼された後の確認と、今回の到達点

実行時は隔離した中間版で、各commitの本文・呼出元・現行案内・参照がその段階で揃うことを確認する。新しい専門の03・09では既存のvalidatorと局所確認の根拠を対応させ、03のSQLite模型を実行する場合は7観測の期待と結果を照合する。本文を変えない記録だけのcommitへ無関係な試験は増やさない。
最後に、計画で切り出した本文の累積が承認時の作業treeと一致し、対象の漏れ・余計なfileが無く、diff・discussionの検査が通ることを確かめる。実行結果の追記だけは、実際に得た結果として区別する。分割のために本文の意味を変える必要が出る場合は、実物の重なりを示して境界を改める。
今確認したのはGitの比較元と実差分、fileと節・文の割当て、依存と保存範囲までである。各中間treeの組立て、各commitのrevertとその後の実行は未実施であり、任意の順のrevertを保証しない。後続が参照する基盤を戻す場合は、その依存箇所も戻す。

論点100のC案は応答待ちのままにする。007は適用保留のまま保存する。今回の計画への合意から、Cの採用・実行やstage・commit・pushを始めない。

#### 検討記録（論点101・イテレーション0）

利用者の「その前にコミット計画立てて」を受け、Cの提案への応答より先に、現在の差分の保存単位を検討する。論点100の提案0は応答待ちのままとし、計画への合意からCの採用、stage・commit・pushの許可を補わない。
比較元はfeature-16のHEAD `6246ecdb9d3c0f9a7e1cf728a8a1ba421239a99d`。計画の記録前は変更50file、stage済みは空である。新しい専門の本文だけでなく、呼出元・雛形・局所確認と、合意・未合意の記録を照合して分ける。

[内部検討記録: 論点101・イテレーション0](../internal-records/implementation_review.md.topic-101.md#iteration-0)

差分の50fileを割り当てると、今回の新記録を含め52fileになった。旧試運転や変更のない専門、Cの未適用のdesign案を混ぜず、保存する効果から17本を取り出した。共有fileの中間版の組立ては実行時に残るため、計画上の境界の照合と、各commitの動作・revertの検証を区別している。

#### 提案0へのフィードバック（論点101）

**結果:** 17本の分割を採用し、commit・pushを先に実行する

> 待った。コミットプッシュしてなかったか。先にそっちだな

この指示を、直前に提示済みの論点101のコミット計画を実際に実行してpushする許可として受領した。直前の「じゃあ論点100でC試して」でC計画が採用されたため、16本目の保存状態は未採用から採用済み・実行待ちに変わる。メッセージは`docs: Cの一式試運転の計画と実行待ちを保存`とし、100の実際の応答と順序指定を加える。Cの仕様や試運転の成果を新しく混ぜるものではない。他の分割と対象52fileは保つ。

### 決定（論点101）

提案0の17本を、上記16本目の状態とメッセージだけを実際の応答に合わせて実行し、feature-16へpushする。既存commitを書き換えない。共有fileの中間版を隔離して検査し、累積を承認された作業treeと照合する。Cの準備・実行はpush後へ回す。

### 実行結果（論点101・第17コミット作成前）

計画の第1〜16コミットを作成した。第1は`09bea03c82`、第16は`31d6a94714`。各commitのparent・対象path・treeは、隔離して検査した中間版と一致し、既存の6246ecd以前の履歴は変更していない。
17段階の議論の番号・親子、各段の現行本文の相対link74〜75件と内部証拠への参照を確認した。新しい専門と変更した専門のvalidator、SQLite模型の7観測は通過した。累積は52fileの保存対象と一致する。各中間版の空白検査では、議論に引用されたunified diffの文脈を表す空白1文字だけを識別して保持し、それ以外の問題を認めていない。任意順のrevertや一式試運転Cの成立は検証していない。
対象欄に漏れていた公開側89の前回完了追記は第1へ、技術の接続・条件の吟味・材料の接続に対応するdesignの反映はそれぞれ第5・10・14へ含めた。いずれも記載した仕事に必要な反映で、独立した変更の混入や本数の変更は無い。
この計画・採用と実行許可・現在までの検査結果を第17へ保存し、その後origin/feature-16へ通常のpushを行う。この欄の保存時点では、第17の作成とpushの成功を先取りしない。Cは採用済みだが準備・反映・実行待ちである。
