# CR-015　商品同定と店舗同定を一括の復活条件にすると、先に調べられる候補まで止まる

- 優先度　P2
- 対象スナップショット　`4b8dc31c0e8242bcda6fd2a2746b25e997b23243`。[内容ハッシュ](../evidence/snapshot.json)
- 対象　[what-defines-a-product/how-to-solve.md L46–53・88–97・210–226](../../../../../../what-defines-a-product/how-to-solve.md)、[.agents/skills/propose-alternatives/SKILL.md L38–57・123–146](../../../../../../.agents/skills/propose-alternatives/SKILL.md)、[.steering/2026/202611/20261103-implement-build-ready-idea-lab-skeleton/product-plans/20261117-find-compatible-pen-refills/materials/alternatives.md L15–21・36–45](../../../../../../.steering/2026/202611/20261103-implement-build-ready-idea-lab-skeleton/product-plans/20261117-find-compatible-pen-refills/materials/alternatives.md)、[.steering/2026/202611/20261103-implement-build-ready-idea-lab-skeleton/product-plans/20261117-find-compatible-pen-refills/README.md L61–71](../../../../../../.steering/2026/202611/20261103-implement-build-ready-idea-lab-skeleton/product-plans/20261117-find-compatible-pen-refills/README.md)
- 観点　取得の責任、候補ごとの依存関係
- 由来　全体レビュー。指定C3の停止と再開を分けて、現行の出どころ確認の受渡しを検査した。
- 採否　採用（2026年11月21日の全件適用指示）
- 対応状況　適用・検証済み
- 適用枠　挙動変更が必要
- 依存する指摘　なし

## 問題と根拠

指定C3の時点では商品と実店の両方が未提供で、集約や店舗在庫を検証しない判断には根拠がある。一方、その正本は品番等と実店・通販の正式名称またはURLがいずれも提供されることを復活条件にした。候補一覧には包装で確かめる部分案、通販を含むE、K1/K2の実店への直接確認Dがある。仮に後日、本人が品番・メーカーの対応資料だけを提供したら、商品の同定、許された範囲でのその品の公開情報の調査は進む。K1/K2の特定はD系の比較で依然必要で、通販の到着には他の条件も要る。一律に両方を待つと、本人が持つ店情報が不要な部分まで取得できない。

現行は『取得可能で比較を変える事実は取りに戻る』とも指示する。一方50行は出どころの事実が他のどの選択肢より先に要るとし、どの不足がどの候補にだけ効くかを、停止・復活の条件へ写す責任が明確でない。受け手が初めから枝分けできたなら全候補停止は不要であり、C3で実際に選べる通販や価格が存在したという主張ではない。

## 改善案

不足を『本人しか出せない識別子』『その識別子でこちらが調べられる公開事実』『特定の候補だけに要る条件』に分ける。保留は案件全体に表示しても、再開条件には最初に進められる依頼・行為をそれぞれ書く。取得後に答えが変わる候補だけ比較を更新する。

## 振る舞いへの影響

本人に全ての店名・資料の発見を一括で返さずに済む。禁止された電話・購入を行わず、実店舗の検査や入手の見込みが未確認であることも保持できる。

## 検証方法・証拠

静的な復活条件の検査。初期設定のまま、品番と互換根拠だけ追加、実店だけ追加、両方追加を比較する。最初の状態は保留、商品だけなら同定および許される探索が進み、実店舗だけでは対象商品の在庫は確定しないこと。外部の検索や再ドライランは実施していない。

## 合意・適用記録

[全件適用の委任](../bulk-application.md)により採用し、本線へ適用した。
設計・具体例での照合・機械検査と限界は[適用記録](../application.md#cr-015)と[検証記録](../evidence/CR-015-application.md)を参照する。
