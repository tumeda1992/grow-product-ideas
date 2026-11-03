# 内部検討記録: 論点21 — 層skill4種をまとめたskillの名前

**discussion:** [task-design-discussion.md](../task-design-discussion/task-design-discussion.md)

**論点:** 論点21

## 開始context

論点20で、層skill4種（`answer-why-to-build`等）を一つの「問いに答えるskill」にまとめると決め、名前を別に決めることにした。担当は、`what-defines-a-product/`の問い一つについて、材料を揃え、対案を比べ、決定過程と正本に書き、漏れを確認して「閉じた」と記録することである。

<a id="iteration-0"></a>

## イテレーション0: 名前

<a id="iteration-0-record-1"></a>

### 判断: 候補の逆翻訳

`.agents/skills/`の中で、`grow-product-idea`、`find-existing-alternatives`等と並べて読む。

| 候補 | 初見の人が予想する中身 | 実態との差 |
| --- | --- | --- |
| `answer-question` | 問いに答えるskill | どの問いかは名前に無いが、このリポジトリで問いは`what-defines-a-product/`の問いだけであり、並ぶskill群と読めば方向は同じ。論点8の`answer-`の型を保つ |
| `answer-product-question` | プロダクトについての問いに答える | 差は小さいが、`product`は並ぶskill群から既に読める情報で冗長 |
| `close-question` | 問いを閉じる | `close`は単独で「終える」と読まれ、論点8で退けた理由と同じ |

推奨は`answer-question`。
