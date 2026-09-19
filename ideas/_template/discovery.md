# Discovery

## Discovery goal and stopping condition

この調査で変えたい判断と、何が分かれば追加調査を止められるかを書く。調査量ではなく verdict を変える不確実性で範囲を決める。

## Problem frame

### Situation and trigger

誰が、どの状況で、何をきっかけに行動を始めるか。

### Desired progress

利用者が機能ではなく状況をどう変えたいか。

### Current journey

現在の開始から結果までを、具体的な道具、待ち、判断、手戻りを含めて示す。

### Friction and cost

時間、金銭、認知負荷、エラー、諦め、機会損失を、根拠のある単位で示す。

### Boundary and counterexamples

問題が起きない人・状況、別問題として扱う境界を書く。

## Evidence ledger

| id | claim | level | evidence and source | observed | scope and counterevidence | recheck trigger |
| --- | --- | --- | --- | --- | --- | --- |
| E-001 |  | E0 |  | {{DATE}} |  |  |

levelは `docs/methods.md` の E0〜E4 を使う。事実を引用する場合は直接のsource URLまたはrepository path、観測日、適用範囲を記す。推論はsourceと同じセルに紛れ込ませない。

## Existing alternatives and competitors

同カテゴリの製品だけでなく、何もしない、手作業、設定、複数サービス、人への依頼を含める。

| alternative | outcome fit | setup / switching | ongoing cost | control | failure cost | evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Do nothing |  |  |  |  |  |  |

## Segments and selection

年齢・肩書だけでなく、問題の引き金、現在行動、頻度、制約が異なる実在のgroupを分ける。最初の対象を選び、選ばないgroupがなぜ同じ初期体験へ入らないかを書く。

## Problem prevalence and reachable scale

対象状況がどの程度起き、最初の提供経路でどの範囲へ届きうるかを、点推定より上下限と根拠で示す。自分専用なら利用頻度と一回あたりの費用で代替する。数字を取得できない場合、架空のTAMを作らず、verdictを変える仮説として残す。

## Reframed problem

調査後の問題を、対象状況、望む進歩、現在の障害、解く価値、根拠強度を含む一段落で記す。

## Unknowns that can change the verdict

未知を列挙するのではなく、答えが変わるとbuild / non-buildまたはsolution shapeが変わるものだけを置く。取得方法と停止条件を添える。

## Discovery gate result

Gate 1の各条件がどの記述と根拠で満たされたか、または満たされず `validate-first | park | stop` へ進む理由を書く。
