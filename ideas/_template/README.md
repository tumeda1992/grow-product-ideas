---
status: captured
verdict: undecided
last_updated: "{{DATE}}"
---

# {{TITLE}}

## Current position

- Status: `captured`
- Verdict: `undecided`
- Confidence: 根拠未評価
- Next action: `source.md` の元アイデアを保ったまま discovery を開始する

## One-minute summary

検討後に、対象者、問題、選んだ解決、最初のマイルストーン、verdictの理由を5文以内で記す。

## Gates

| gate | status | evidence |
| --- | --- | --- |
| Problem is real enough | pending | `discovery.md` |
| Alternatives were compared | pending | `product.md` |
| Verdict matches evidence | pending | `product.md` |
| First milestone is bounded | pending | `product.md` |
| Experience, touchpoints, data, and modules connect | pending | `specification.md` |
| Readiness audit has no P0/P1 | pending | `handoff.md` |

Gate statusは `pending | passed | failed | not-applicable` のいずれかにする。`not-applicable` には、このアイデアで同じ実装判断を何が担うかを evidence 欄へ書く。

## Owner decisions

エージェントが自走できず、verdictまたは重大な設計を変える事項だけを置く。各項目に推奨案、理由、答えで変わる範囲を書く。無ければ「なし」。

## Artifact map

- [Source](./source.md)
- [Discovery](./discovery.md)
- [Product decision](./product.md)
- [Specification](./specification.md)
- [Handoff and audit](./handoff.md)
- [Process retrospective](./retrospective.md)
