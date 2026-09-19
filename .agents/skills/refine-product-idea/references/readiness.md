# Readiness phase

## Outcome

大きな手戻りが実装後に発覚する可能性を、実装前に攻撃して下げる。文書品質のレビューではなく、決定と構造の反証レビューである。

## Traceability first

次を左から右、右から左にたどる。

```text
evidence → problem → outcome → requirement → experience → touchpoint → data/module → acceptance
```

孤立した要素を見つけたら、単にlinkを足さない。必要なら上流のproblem、requirement、solution boundaryを修正する。

## Attack set

### Premortem

リリース後に「使われない」「既存手段へ戻る」「維持不能」「重大事故」のいずれかが起きたと仮定する。最もらしい原因を最低一つずつ考えるが、非該当なら理由を示す。現在の設計が原因を予防・検知・回復できるか確認する。

### Strongest alternative

最有力のnon-build案へ新しい知見を反映し、build案と再比較する。build案を選んだ後に比較条件を固定しない。

### Change stress tests

アイデアに関連する三つ以上を具体値で変える。

- 利用量またはdata volumeが10倍になる
- 最初のsegmentと異なる隣接segmentが入る
- 外部serviceの価格・仕様・可用性が変わる
- privacyまたはretention要求が厳しくなる
- manual seamの頻度が想定を超える
- source of truthを移行する

すべてを無傷で吸収する必要はない。どこが意図的なmilestone boundaryで、どこが大手戻りになるかを区別する。

### Failure and recovery

該当するtimeout、duplicate、partial write、stale data、permission loss、user interruptionを具体recordで通す。system state、user-visible state、retry、manual recovery、observabilityがつながるか確認する。

### Implementer simulation

元の会話を知らない初見の実装者として、正本だけを読む。次の問いへの答えが一意でない箇所をfindingにする。

- 何を作ればacceptanceを満たすか。
- どのdataが正で、いつ変わるか。
- 各actionはどのmoduleが引き受けるか。
- 失敗時に何を保存し、何を見せ、どう回復するか。
- scope外へどこから先は踏み込まないか。

## Severity and loop

P0は価値、対象、安全、法令、核心的実現性を崩す。P1は主要体験、touchpoint、data、moduleを大幅に作り直す。P2は局所修正、P3は誤読を生む表現改善である。

P0/P1は最上流のroot artifactを修正し、影響するgateを再実行する。修正後に新しいroundを追加する。新しいP0/P1がゼロになるまで `build-ready` にしない。

P2/P3をゼロにすることを完璧主義の目標にしない。first milestone後に安く直せるものはowner、signal、triggerを付けてresidual riskへ移せる。
