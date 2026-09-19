# Product specification

## Applicability

Applicability: pending

verdictが`build`なら`required`へ変える。その他のverdictでは、`not-applicable — <この仕様を作らず、どの成果物が次の行動を担うか>`へ変え、以降の節を埋めない。

## Scope of this specification

`product.md` の最初のマイルストーンのうち、この仕様が確定する範囲を書く。将来構想と現在の約束を混ぜない。

## Experience

### Golden path

開始から価値獲得までを番号付きで示す。各stepに、actor action、system response、visible result、次へ進む条件を含める。

### Meaningful branches

王道と異なるプロダクト挙動になる分岐だけを、条件と合流先を含めて示す。

### Failure and recovery

関連する不完全入力、中断、重複、権限不足、外部停止、競合更新を具体例で通す。利用者が次に何をすれば回復できるかを書く。

## Touchpoints

画面、CLI command、API、通知、手動運用など、体験を担う接点を使う順に並べる。

| id | touchpoint | entry | information / actions | input source | outcomes and next |
| --- | --- | --- | --- | --- | --- |
| T-01 |  |  |  |  |  |

UIがある場合は、画面ごとに状態、主要component、入力の供給元、action後の遷移、empty/loading/error/successを具体化する。UIがない場合は `not-applicable` の理由と、同じ判断を担う接点仕様を示す。

### Navigation and screen map

UIがある場合、どの画面からどの条件で移動できるかを図示する。王道と主要分岐が一枚で読めなければ、王道と例外を分ける。

### Low-fidelity screen composition

王道を担う各画面について、情報の優先順位、主要領域、主要action、戻る・中断する経路が分かるwireframeまたは同等の構成を置く。装飾の完成ではなく、実装後に画面を継ぎ足して体験が崩れることを防ぐ。

### Shared interaction and visual rules

navigation、layout、form、feedback、empty/loading/error、responsive、accessibilityのうち、このmilestoneで複数画面へ効く規則をまとめる。画面ごとに別の規則を作らない。既存design systemがある場合は複製せず参照し、今回追加する差分だけを定める。

## Core product rules

推薦、分類、優先順位、価格、権限、スケジュールなど、結果を決める核心ロジックを記す。

| rule id | inputs and preconditions | output / state change | boundary and failure | concrete examples |
| --- | --- | --- | --- | --- |
| RULE-001 |  |  |  |  |

代表例だけでなく、境界例と「適用しない」反例を通す。実測でしか決まらない閾値は架空に固定せず、spikeまたは運用計測で決める範囲と初期fallbackを書く。

## Data and state

### Concrete examples

王道、境界、失敗を表す実データ相当の例を置き、schemaだけで済ませない。

### Entities and ownership

| entity / record | identity | owner / source of truth | required fields | invariants | retention / deletion |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### Relationships and lifecycle

関係、生成、更新、状態遷移、削除、履歴を示す。永続化が不要なら `not-applicable` の理由と、状態をどこが持つかを書く。

## Backend modules and integrations

| module | responsibility | public boundary | depends on | failure policy | observability |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

フレームワーク名ではなく、変更理由が同じ責務をまとめる。外部サービスはtimeout、retry可否、idempotency、rate limit、degraded behavior、資格情報のownerを必要な範囲で確定する。

## Public contracts

他の画面、module、client、automationから利用される境界を、callerを主語にして定義する。

| contract id | caller and purpose | request / input example | response / output example | errors and compatibility |
| --- | --- | --- | --- | --- |
| C-001 |  |  |  |  |

内部実装だけで閉じる場合は `not-applicable` と理由を書く。API、CLI、event、shared libraryでは、命名、必須値、error、idempotency、versioningまたはmigrationを実装者へ残さない。

## Cross-cutting requirements

このマイルストーンでプロダクト挙動を変えるものだけを書く。

- Security and authorization
- Privacy and data handling
- Accessibility
- Performance and capacity
- Reliability, backup, and recovery
- Logging, metrics, and support
- Compatibility and migration

各項目は `required | not-applicable(reason) | deferred-after-milestone(reason)` を明示する。規格名を置くだけでなく、対象シナリオと受入可能な境界を書く。

## Product measurement

| signal | event / source | baseline | target or decision rule | review timing |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

計測のための収集が利用者の信頼や実装費に見合うかも判断する。

## Requirement index

| id | requirement | priority | evidence / decision | experience | touchpoint | data / module |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 |  | MUST / SHOULD / MAY |  |  |  |  |

MUSTは満たさなければ最初のマイルストーンの価値または安全性が崩れるものに限る。

## Specification gate result

Gate 5について、該当する四骨格がつながり、実装者へ残るプロダクト判断がない根拠を書く。
