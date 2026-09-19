# Definition phase

## Outcome

`specification.md`だけを読んだ実装設計者が、プロダクトの挙動、情報、責務について新しい判断をせず、技術設計へ進める状態にする。

## Design from scenarios

最初にgolden pathを具体的なactorとdataで最後まで通す。その経路からtouchpoint、data、moduleを導く。各成果物を別々に作って後から対応づけない。

次に、結果または永続状態を変えるmeaningful branchを通す。最後に、関連するfailureとrecoveryを通す。全errorを網羅するのではなく、大幅な画面、table、moduleの手戻りを起こすcaseを優先する。

## Touchpoints

各画面または接点について、entry、表示・出力、action、input source、状態、遷移を確定する。UIならempty、loading、error、successを必要な範囲で示す。CLI/APIならcommandまたはendpoint、input、output、error、idempotencyを示す。

screen countやcomponent countは目的ではない。同じ判断を異なる画面で重複させない。逆に、異なる利用目的を一画面へ詰めて複雑さを隠さない。

UIがある場合は、navigation map、王道を担う主要画面の低忠実度構成、複数画面へ効くinteraction・visual rulesを作る。個別画面を先に完成させず、情報の優先順位、共通layout、feedback、responsive、accessibilityを横断して決める。

## Core rules

利用者が得る結果を決めるロジックを、rule id、input、precondition、outputまたはstate change、boundary、failure、具体例で定義する。代表例から抽出した規則を、別の境界例と反例へ当ててから確定する。

実行しなければ決められない閾値やmodel品質は架空に確定しない。product decisionの技術spikeで先に潰すか、first milestoneで観測する初期fallbackと変更条件を決める。

## Data

schemaより先に、golden、boundary、failureを表す具体recordを作る。その後にidentity、関係、invariant、lifecycle、source of truth、retention/deletionを導く。

derived valueを保存する場合は、再計算元、更新契機、不整合時の扱いを決める。履歴が必要な場合は、現在値だけで失われる判断を具体caseで示す。

## Modules

一緒に変わる理由が同じ責務をまとめる。moduleごとにpublic boundary、dependency、failure policy、observabilityを定める。画面単位またはtable単位で機械的にmoduleを作らない。

外部integrationではtimeout、retryの安全性、重複、rate limit、credential owner、停止中の挙動を必要な範囲で確定する。

他のmodule、client、automationが利用するpublic contractは、callerと目的、具体的なrequest / response、error、idempotency、互換性を定義する。公開名と値の意味を後続の実装判断へ残さない。

## Cross-cutting requirements

一般論を列挙しない。milestoneの具体scenarioに作用するsecurity、privacy、accessibility、performance、reliability、operationだけを `required | not-applicable(reason) | deferred-after-milestone(reason)` にする。

## Adversarial checks

- golden pathの各stepを担うtouchpointがあり、各inputの供給元を追えるか。
- 主要画面を並べたとき、navigation、情報優先度、共通action、feedbackが一つの体験として整合するか。
- 核心ruleを代表例、境界例、反例へ当て、同じinputから一意な結果を得られるか。
- concrete dataをschemaで表し、invariantを破る例を拒否または回復できるか。
- state transitionと画面表示が矛盾しないか。
- module境界を跨ぐ一つの変更が循環依存や二重責務を生まないか。
- public contractのcallerが、追加調査なしに正しいrequestを作り、errorから回復できるか。
- external failureで利用者が永久待機、重複処理、状態不明にならないか。
- deferred項目が、実はmilestoneの価値または安全性に必要ではないか。
- Requirement indexのMUSTを一つずつ削ったとき、何が壊れるか具体的に言えるか。
