# 根拠

確認日は2026-09-14。価格・機能は導入直前に再確認する。

- E1 原文：proposal.md引用。二人、browser、品名/個数、50、手入力、非公開、月1,000円、不要機能、外部行為禁止。
- E2 [Google公式比較](https://support.google.com/docs/answer/9331278?hl=en)・[変更履歴](https://support.google.com/docs/answer/190843?hl=en-10)：共同編集、自動保存、履歴を確認。差分在庫transactionは未記載。
- E3 [Grocy公式repository](https://github.com/grocy/grocy)・[food tutorial](https://github.com/grocy/grocy-docs/blob/master/tutorials/food.md)・[setup](https://github.com/grocy/grocy-docs/blob/master/tutorials/setup.md)：Web/PWA、既定admin変更、user追加（全user admin）、location/unit、purchase/consume/inventory、Never Expiresを確認。[StockService](https://github.com/grocy/grocy/blob/master/services/StockService.php) はconsume上限、transaction/user logを示す。ただし同時実行・応答消失・idempotencyは保証しない。
- E4 [PikaPods Apps](https://www.pikapods.com/apps/)：Grocy 2 USD/月から。[公式概要](https://www.pikapods.com/)：managed構成、更新、SFTP。[backup手順](https://docs.pikapods.com/manage/backup)：pod停止、全persistent file、必要時全DB export、新pod停止・DB/file復元・log確認、環境変数はbackup外を確認。実円・税・Grocy固有restoreは未確認。
- E5 自作案：[Supabase pricing](https://supabase.com/pricing)、[RLS](https://supabase.com/docs/guides/database/postgres/row-level-security)、[Cloudflare Pages](https://developers.cloudflare.com/pages/functions/pricing/) で経路は成立するが、実装負担のため次善。
- V1 旧自作モデル：旧 `shared/validation/atomic-counter.mjs` の8/8合格は逐次インメモリadjust、再送、負数、非member、逐次50/51だけを示す。Grocy/X1/RLS/同名/restoreの証拠にしない。

## 未実行と調査終了

X1を含む実Grocy/PikaPods、checkout、登録、認証、二browser、backup/restore、本人利用は未実施。外部禁止または実環境でしか確認できない。X1の入力・方法・証拠・上限・判定が完成し、公開調査で採用をさらに確定できる残作業はないため調査を終了する。
