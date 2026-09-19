---
name: refine-product-idea
description: Rough product ideas are researched, challenged, narrowed or expanded, and turned into a build-ready specification or an explicit validate/use-existing/park/stop decision. Use for new ideas and for continuing work in ideas/; do not use for implementation of an already build-ready product.
---

# Refine Product Idea

粗いアイデアを「作るだけ」の状態へ育てる。ただし、根拠が支持しない場合は `validate-first | use-existing | park | stop` を、`build` と同じく正しい出口として扱う。

## Start

1. `AGENTS.md`、`docs/operating-model.md`、`docs/methods.md`を完全に読む。
2. 新規アイデアなら `scripts/new-idea.sh <slug> "<title>" "<raw idea>"` を使い、元のユーザー発言を `source.md` の `Raw idea` へ逐語で保存する。既存アイデアなら、そのディレクトリの全正本を読み、価格、競合仕様、法令、外部APIなど時間で変わる根拠のうち、現在のverdictまたは仕様を変えうるものだけを再確認する。
3. `README.md` のstatusを現在のphaseへ更新する。statusは作業量ではなく `docs/operating-model.md` の到達条件で進める。
4. アイデア種別を判定し、`docs/methods.md` の重点を調整する。画面、database、市場調査などを非該当の対象へ機械的に要求しない。

## Operating contract

- エージェントが取得できる外部情報、比較、推論、可逆な判断、成果物作成、自己レビューは自走する。
- ユーザーにしかない情報が欠けても、独立して進められるphase・section・調査・監査を先に完了する。
- ユーザーにしか決められない高影響事項は `README.md` のOwner decisionsへ集約し、推奨案、理由、答えで変わる範囲を添えて最後に一度だけ問う。
- 可逆で安全な暫定案を置けるなら、仮定と反証条件を明示して先へ進む。ユーザーの動機、費用・リスク許容、倫理、権限を推測で確定しない。
- 事実、引用、推論、仮説、決定を区別する。Web情報には直接sourceと観測日を残す。調査で需要を検証済みと表現しない。
- 文書を埋めるための架空の数字、persona、競合、代案、例外を作らない。不明な値は比較可能な代理尺度かunknownにする。
- 各phaseで結論が変われば、下流へ注記を足すのではなく、影響を受ける正本を新しい前提で再構築する。

## Phase loop

### 1. Discover the problem

`references/discovery.md`を完全に読み、`discovery.md`を完成させる。

元の解決策をいったん問題へ戻す。利用状況、望む進歩、現在の経路、摩擦、既存手段、問題が起きない境界を、利用可能な根拠で具体化する。対象者は属性ラベルではなく状況と行動で選ぶ。

Gate 1を満たせない場合、足りない証拠がverdictを変えるか判定する。変えるなら後続を止めず、実行可能な検証計画まで作って `validate-first` にする。変えない低影響の不確実性は、適用範囲を限定して進む。

### 2. Decide whether and what to build

`references/decision.md`を完全に読み、`product.md`を完成させる。

元の案、narrow、adjacent、broader、何もしない、既存製品、assembleを同じ利用成果に対する選択肢として比較する。最有力の非build案を弱く描かない。望ましさ、実現可能性、継続可能性の仮説を影響と証拠で並べ、verdictを一つ選ぶ。

`validate-first | use-existing | park | stop` なら、実行可能な次の一手または再開条件を作り、順に `experiment-ready | adopt-ready | parked | stopped` へ進める。この場合、`specification.md`と`handoff.md`のApplicabilityを理由付き`not-applicable`にし、残る節を埋めない。`build`なら両fileを`required`にし、開始から価値獲得まで完結する最初のマイルストーンを定義する。

### 3. Define the first milestone

verdictが `build` の場合だけ `references/definition.md`を完全に読み、`specification.md`を完成させる。

体験、画面やその他の接点、データ、バックエンドモジュールを別々の一覧として作らず、同じシナリオを通して接続する。王道だけでなく、重要分岐、失敗、復旧を具体データで通す。後から安く変えられる実装詳細を決めすぎず、プロダクト挙動を変える判断は残さない。

### 4. Audit readiness

verdictが `build` の場合だけ `references/readiness.md`を完全に読み、`handoff.md`を完成させる。

最初にtraceabilityを両方向で確認し、その後pre-mortem、最有力の非build案、変更stress test、失敗復旧、初見実装者simulationで攻撃する。P0/P1が見つかったら、`handoff.md`へ指摘を残すだけでなく、原因が生じた最上流の成果物へ戻して修正し、影響gateを再実行する。

新しいP0/P1がなくなるまで監査roundを繰り返す。P0/P1、Owner decisions、未通過gateがゼロになった場合だけ `build-ready` にする。

### 5. Improve the lab

出口に関わらず `retrospective.md`を完成させる。共有の型を変える候補は、異なる二件以上で再発した摩擦、一件でもP0/P1を生んだ欠落、または品質を落とさず手順を減らした改善に限る。

候補があるだけで共有fileを自動変更しない。現在の作業がラボ自体の改善もscopeに含む場合は、起点ケースと異なる二ケース以上へ適用してから変更する。アイデアを育てる依頼だけなら候補を記録し、変更提案として返す。

## Finish

終了前に `scripts/check-lab.sh ideas/<slug>` を実行する。`build-ready` の場合は次をすべて確認する。

- verdictが`build`
- 全gateが`passed`または具体理由付き`not-applicable`
- P0/P1 open countが0
- Owner decisionsが0
- `handoff.md`から正本path、scope、受入条件、残留riskを後続実装へ渡せる

最終報告は、verdictと理由、最初のマイルストーンまたは次の検証、重大レビューで直した点、残る低影響risk、ユーザーにしか決められない事項を示す。作業履歴の列挙ではなく、現在の完成形を先に伝える。
