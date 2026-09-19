# Handoff and readiness audit

## Applicability

Applicability: pending

verdictが`build`なら`required`へ変える。その他のverdictでは、`not-applicable — <readiness auditが不要な理由と次の行動の正本>`へ変え、以降の節を埋めない。

## Handoff summary

初見の実装者が、誰のどの問題を、どのマイルストーンで、どの体験として解くかを5文以内で把握できる要約を書く。

## Traceability

| evidence | problem / outcome | requirement | experience step | touchpoint | data / module | acceptance |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

表を左から右、右から左へ確認する。根拠のない要件、実装先のない要件、要件に結びつかない構造、受入条件のない重要挙動を残さない。

## Acceptance scenarios

王道、重要分岐、失敗と復旧、権限・privacy、運用観測を Given / When / Then または同等の具体形式で示す。実装方式ではなく外から観測できる結果を書く。

## Decisions delegated to implementation design

後続の `task-design` 等が決めてよい技術判断を列挙する。選択によって体験、データ意味、public contract、運用費が変わるものは委譲しない。

## Readiness audit rounds

### Round 1

#### Premortem

使われなかった、維持できなかった、事故を起こしたと仮定し、原因と現在の防止策を結ぶ。

#### Strongest non-build alternative

選んだ案が、最有力の既存手段またはassemble案より本当に優れるかを再判定する。

#### Change stress tests

関連する三つ以上の変化を具体値で通し、壊れる仕様と吸収できる仕様を示す。

#### Failure and recovery walkthrough

具体データで重要な失敗を通し、状態、利用者表示、retry、manual recovery、観測を確認する。

#### Implementer simulation

仕様だけを読んだ初見の実装者として、追加判断が必要な箇所を列挙する。

| id | severity | finding | root artifact | correction | rechecked gates | status |
| --- | --- | --- | --- | --- | --- | --- |
| A-001 | P0 / P1 / P2 / P3 |  |  |  |  | open |

P0/P1は根本の正本を修正し、影響gateを再実行してから `resolved` にする。新しい重大指摘がなくなるまでRound 2以降を追加する。

## Residual risks

build後の運用で解決すると意図的に判断した不確実性だけを置く。owner、観測方法、発火条件、対応を含める。

## Final readiness decision

- Verdict:
- Status:
- P0 open count:
- P1 open count:
- Owner decisions remaining:
- Why implementation can start:

`build-ready` を記録できるのは verdict が `build`、P0/P1がゼロ、owner decisionがゼロ、全gateがpassedまたは理由付きnot-applicableの場合だけである。

## Implementation handoff

後続エージェントへ渡す入力を、参照path、実装scope、非scope、受入条件、残留risk、推奨validationの順で記す。ここへ仕様全体を複製せず、正本を参照する。

後続の `steering` / `task-design` は、`source.md`、`product.md`、`specification.md`、この`handoff.md`を上位制約として読む。技術調査で前提矛盾が見つかった場合の戻り先も記す。
