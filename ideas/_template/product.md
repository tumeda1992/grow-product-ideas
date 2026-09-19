# Product decision

## Decision question

このアイデアで今決めるべきことを、解決策名ではなく利用者の成果を主語にして書く。

## Solution shapes

元の案を narrow、adjacent、broader に変形し、それぞれ一つの具体シナリオで価値獲得まで通す。

### Narrow

一人、一状況、一成果へ研ぎ澄ませた案。

### Adjacent

同じデータまたは行動連鎖で自然に完結させる案。

### Broader

対象者、ジョブ、チャネルを広げた案。広げる限界費用が低い根拠がなければ採らない。

## Build / buy / assemble comparison

| option | user outcome | initial cost | ongoing cost | switching cost | control | failure / lock-in | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Do nothing / process change |  |  |  |  |  |  |  |
| Existing product |  |  |  |  |  |  |  |
| Assemble / automate |  |  |  |  |  |  |  |
| Build narrow |  |  |  |  |  |  |  |

比較期間、費用の単位、推定の根拠を表の前後に書く。金額を推測で作らない。

## Critical assumptions

| id | assumption | type | impact if false | evidence level | cheapest discriminating test | decision threshold |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H-001 |  | desirability / feasibility / viability |  | E0 |  |  |

## Verdict

`build | validate-first | use-existing | park | stop` の一つを選ぶ。

### Rationale

最有力の反対案と比較し、なぜこのverdictなのかを説明する。作りたい動機と経済合理性は別々に書く。

### Validation plan

`validate-first` の場合だけ、仮説、成功・失敗基準、対象、刺激物、観測行動、期間または件数、結果別の次の判断を記す。外部公開、連絡、支出は実行直前に権限を確認する。

### Non-build next step

- `use-existing`: 採用する手段、初期設定、移行するデータ、日常の運用、撤退条件を、実行できる順序で記す。
- `park`: 再開を判断する観測可能な条件と、条件を確認する時機を記す。
- `stop`: 同じ案を根拠なしに再開しないため、停止理由と覆すために必要な新しい証拠を記す。

`build`または`validate-first`では `not-applicable` と理由を書く。

## First milestone

`build` の場合だけ記す。

### Actor, trigger, and completed outcome

誰が、どの引き金で開始し、何を得たら一連の体験が完了するか。

### In scope

開始から価値獲得までに保証するシナリオ。

### Out of scope

魅力的だがこのマイルストーンへ入れないものと、入れなくても王道が完結する理由。

### Manual seams

手動運用で補う箇所、担当、頻度、失敗時の対処。

### Operate-after line

どの状態から先は、運用で観測しながら都度解決してよいか。その線より前に確定すべき不可逆な判断を書く。

### Success and stop signals

継続、変更、中止を判断する観測可能な信号。

## Delivery and sustainability

他者向けに提供する場合、次を最初のマイルストーンに必要な深さで確定する。自分専用なら `not-applicable` と、その判断が後で変わる条件を書く。

- 到達経路: 対象者がどこで知り、なぜ試し、どう初回価値へ到達するか。
- 価値交換: 無料、有料、業務時間削減、学習など、継続する理由と提供側が負う費用。
- 価格・収益: 誰が何に対して支払うか。未検証なら仮説と最小の検証を置く。
- 運用: 問い合わせ、障害、content・data更新、外部service変更を誰がどの頻度で扱うか。
- 法令・規約: verdictまたはmilestoneを変える可能性のある制約。

## Product decision gate result

Gate 2〜4について、満たした根拠、残る低影響の不確実性、受け入れたリスクを書く。
