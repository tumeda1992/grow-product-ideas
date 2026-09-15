# 根拠と検証

確認日はすべて2026-09-14。価格・機能は購入直前に再確認する。

## E1 原文

proposal.mdの引用。二人、ブラウザ、品名/個数、最大50、手入力許容、非公開、自宅サーバーなし、月1,000円、不要機能、登録/課金禁止を確認。頻度・操作時間・アカウントは不明。

## E2 Sheets

[Google公式の比較](https://support.google.com/docs/answer/9331278?hl=en) と [変更履歴](https://support.google.com/docs/answer/190843?hl=en-10)。リアルタイム共同編集、自動保存、版/セル履歴は確認。差分在庫transactionや1タップconsumeは記載なし。次善案の範囲を限定する。

## E3 Grocy機能・導入条件

- [Grocy公式リポジトリ](https://github.com/grocy/grocy)：self-hosted Web/PWA、最近のFirefox/Chrome/Edge、既定admin/passwordの即時変更、feature flags、更新時のdata backupを確認。
- [公式ドキュメント food](https://github.com/grocy/grocy-docs/blob/master/tutorials/food.md)：初期にlocationとquantity unitが必要。purchaseは量を在庫へ加え、consumeは量を減らし、inventoryは棚卸しで増減する。期限はNever Expiresを選べる。product name/default location等の必要入力がある。
- [公式 setup](https://github.com/grocy/grocy-docs/blob/master/tutorials/setup.md)：user追加、全userがadministrator権限であることを確認。二人以外を作らない条件では許容するが、将来第三者を招くなら不適合。
- [Grocy stock service](https://github.com/grocy/grocy/blob/master/services/StockService.php)：consumeがcurrent stock超過を拒否し、transaction IDとuser IDをstock logへ保存する実装を確認。ただし同時操作・応答消失時のidempotencyを実行確認していないため保証しない。

## E4 管理Grocyの実用構成と費用

[PikaPods Apps](https://www.pikapods.com/apps/) はGrocyを2.0 USD/月から掲示。[PikaPods公式](https://www.pikapods.com/) は構成・DB・更新を管理、隔離container、暗号化接続、SFTPでdata取得可能と説明。表示価格はUSD・税別で、実請求円は未確認。自宅サーバーなしでも既製Grocyを使えるため比較へ採用。

[PikaPods Backup](https://docs.pikapods.com/manage/backup) は、一回backupについてpod停止後にSFTPで全fileをコピーし、外部DBがあれば全DBもexportする手順を示す。新podへのrestoreは、空podを停止し、DB全tableを除去してdumpをimport、SFTPでfileを戻し、起動後logを確認する。環境変数はbackupに含まれず再設定が必要な場合がある。この公式手順を復旧契約とし、Grocy固有の実データ配置・version互換は実restore gateで確認する。

代替のmanaged GrocyとしてDINAO 9.90 EUR/月税別、grocy.ch 5 CHF/月、selfhost.tools 15.99 USD/月も確認したが、月1,000円上限への余裕と初回試用でPikaPodsに劣る。価格以外の品質比較はしていない。

## E5 Supabase/Cloudflare（不採用自作案の成立根拠）

[Supabase pricing](https://supabase.com/pricing)、[RLS](https://supabase.com/docs/guides/database/postgres/row-level-security)、[Cloudflare Pages pricing](https://developers.cloudflare.com/pages/functions/pricing/) を確認。自作経路は存在するが、無料DB休止、手動backup、実装時間があり、まず既製品を試す判断へ変更。

## V1 実行済みと適用範囲

旧自作案の `shared/validation/atomic-counter.mjs` を2026-09-14に実行し8/8合格した事実は [独立レビュー](../shared-receiver-review.md) で確認済み。ただし逐次インメモリの `adjust`、再送、負数、非member、逐次50/51だけを示す。Grocy、実DB、RLS、同名、改名、archive、CSVを示さず、現採用案の合格証拠には使わない。

## 未実行

PikaPods/Grocyの登録・課金・実instance、production認証、二人user、二ブラウザpurchase/consume、同時操作、通信応答消失、50品目、backup取得/復元、本人の一週間利用。禁止された外部行為または導入後でしか確認できないため、handoffのgateへ移した。未決仕様ではない。

## 調査終了

「クラウド上の既製Grocy」という推奨を変える候補を確認できた。表示価格と既存機能は一週間試用に足りる。残る未知は購入画面と実instanceでしか解けず、失敗時は購入しない/停止して自作へ戻る条件があるため終了する。
