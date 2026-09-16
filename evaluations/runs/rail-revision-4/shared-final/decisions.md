# 判断履歴

## D1（置換済み）専用Web自作

2026-09-13自律確定。差分RPCを採用したが、全mutation再送契約I1と改名前後名履歴I2が不足し、managed Grocyを比較していなかったためD2で置換。

## D2 条件付きmanaged Grocy

2026-09-14自律確定。cloudを既製/自作に対称適用すると、PikaPods Grocyは2 USD/月からで管理済み、purchase/consume/inventoryを持ち、一週間開始が早い。X1合格時だけ採用確定。不合格/確認不能は自作へ戻る。

## D3 最小運用

production/HTTPS、既定admin passwordを最初に変更して再login、二人目だけ追加、location「冷蔵庫」、unit「個」、Never Expires。改名/削除回復を提供せず試用中は行わない。独自CSVでIDを再構成せず、停止中の全persistent file＋必要時全DB dump＋環境設定をbackup単位とする。

## D4 X1応答消失

2026-09-14自律確定。手動の機内mode/offline切替はrequest未送信と到達後response lossを区別できないため採用しない。desktopのPlaywright routeで対象mutationを捕捉し、`route.fetch()` がupstream HTTP responseを得た後にpageへfulfillせず `route.abort()` する。upstream到達とpage応答消失を分離して記録する。最大3試行または20分。再現不能は合格でなく確認不能。
