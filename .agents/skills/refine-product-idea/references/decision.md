# Decision phase

## Outcome

`product.md`だけを読んだ人が、最有力の非build案を含む選択肢を比較し、なぜそのverdictと最初のマイルストーンになったかを再現できる状態にする。

## Procedure

1. 同じreframed problemから、narrow、adjacent、broaderを作る。各案は機能リストでなく、開始から成果までの一つのscenarioにする。
2. `do nothing / process change`、既存製品、assembleまたはautomation、buildを候補にする。実在しない候補を枠埋めに作らない。
3. 比較期間と単位を先に固定し、成果、初期費、継続費、切替費、制御性、失敗費を比較する。
4. 各案が成立するための仮説を desirability、feasibility、viability に分ける。
5. 誤りなら案全体が崩れる仮説を、高影響・低根拠の順にする。
6. buildより安く判別できる重要仮説には、反証可能なexperimentを作る。
7. `build | validate-first | use-existing | park | stop` を一つ選び、最有力の反対案を退ける理由を書く。
8. `build`の場合、actor、trigger、completed outcomeを持つ縦の一切れとしてfirst milestoneを決める。
9. 高影響のfeasibility仮説が文書調査で決まらない場合は、最小の技術spikeを `ideas/<slug>/spikes/<hypothesis>/` に置いて実測する。spikeは事実取得用であり、意図的に採用を決めない限り本実装の土台にしない。実測結果をCritical assumptionsへ戻す。

## Decision rules

- 作ること自体が目的のpersonal projectは許容する。ただし「楽しさ・学習」と「既存手段より経済合理的」を別の便益として書く。
- 高影響・低根拠でも、first milestone自体が最小の検証になり、捨てられる費用が許容範囲ならbuildを選べる。どの学習で継続判断するかを明示する。
- 外部公開、支払い、利用者への連絡が必要なexperimentは、計画作成と実行権限を分ける。権限なしに実行しない。
- broader案は将来性で選ばない。narrowでは価値が完結しない、または共通資産で追加価値の限界費用が低い場合だけ選ぶ。
- 他者向けに提供する案は、到達経路、価値交換、価格または継続理由、support・更新費を確認する。自分専用の案へ架空の収益modelを強制しない。

## Adversarial checks

- non-build案を不便に描いてbuildを勝たせていないか。
- narrow案は単なる機能削減でなく、特定状況の価値を完結させているか。
- broader案は複数segmentの異なる要求を一つへ押し込んでいないか。
- priceだけを比較し、移行、手運用、保守、停止時損失を落としていないか。
- experimentの成功基準が、どんな結果でも「有望」と読める形になっていないか。
- first milestoneが水平な基盤や画面一覧で終わり、利用者が価値を得られない形になっていないか。
