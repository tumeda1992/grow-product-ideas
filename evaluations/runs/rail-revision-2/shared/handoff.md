# 引き継ぎ

状態は README.md を参照。本書は実装仕様であり、外部登録・公開の許可ではない。

## 読む順序

README.md → proposal.md → design.md → review.md。判断理由は decisions.md、外部条件と検証は evidence.md。ディレクトリごと実装先へ渡す。

## 実現するもの

proposal.md「到達点」の今回引き渡す線と R1〜R8、design.md の画面・データ・RPC・権限表を実現する。非目標を追加しない。U1は配備時入力、U2は運用観測で、ローカル実装を止めない。

## 着手順と確認箇所

1. **ローカルの縦の一場面**：入力は牛乳2と二人相当のuser ID。DB migration（表、制約、非再帰の membership helper、RLS、grants、RPC）と最小一覧を作り、A `-1` → B read=1 を統合試験する。未認証/非memberが読書きできる、または membership policy が再帰エラーになったら停止。
2. **最も危険な更新契約**：同じ初期値から相反するRPCを実際のPostgresで並行実行し最終2・event2件、同じrequest_id再送でevent1件、0未満拒否を確認。片方だけ成功、絶対値上書き、event不整合ならUIへ進まない。
3. **境界と回復**：50/51件、同名、archive後の同名、STALE_VERSION、通信失敗表示、逆操作、履歴を自動試験する。
4. **UI完成**：login、一覧、追加、訂正、改名、archive、history、空/読込/エラー/未同期を実装。390px幅で主要操作が横スクロールなし、通常増減が一覧から1タップであることを目視確認。
5. **外部登録許可後だけ配備**：料金を公式ページで再確認。Supabase/Cloudflareアカウント作成、migration適用、公開signup無効、U1の二人だけ作成、Cloudflare Pagesへdirect upload。有料機能は選ばない。
6. **配備後受入**：通常/シークレット等の独立2ブラウザで同時更新、focus再取得、第三者、ログアウト後、直URL/API、再送、CSV export/復元リハーサルを実施。RLS試験が全て通るまで二人の実データを入れない。
7. **一週間試用**：U2/H1/H2を記録。古い値への巻き戻し1件でもあれば不合格でログとeventを保全し更新処理を修正。入力率80%未満なら機能拡張せず問題設定を見直す。

## 実装先との接続

実装先は未指定。新規 repository に移送可能で既存コード依存なし。Node LTS、TypeScript、Vite、Supabase CLI を推奨するが、design.md の公開契約を守ればframework変更は可。外部アカウント、project ID、メールはコードへ固定しない。

最低成果物：frontend source、SQL migrations、seed（架空データのみ）、単体/統合/RLSテスト、`.env.example`、local/deploy/backup/restore README。秘密鍵・実メール・実在庫はcommitしない。

## 裁量・相談・運用後の確認

裁量と相談条件は design.md 最終節。U2 の観測者は二人、集計者はowner。7日後、(1)古い値への巻戻し、(2)更新予定/実記録、(3)±1以外の訂正回数、(4)通信失敗、(5)第三者アクセス兆候を確認する。巻戻し>0または漏洩兆候>0は直ちに停止、CSV保全、原因修正。記録率<80%なら買い物リスト化/対象品目削減を比較する。

## 受取確認

- 確認者：育成担当による受取視点の自己確認（独立実装者・実装ではない）。
- 対象：最初の縦の一場面と、最も危険な並行更新/RLS。
- 既に記載：schema、所有、RPC入出力、idempotency、競合、エラー、権限、UI応答、合格値、配備順、復旧。
- 安く変えられる裁量：framework内部分割、見た目、Realtime有無。
- 重要な未決：なし。実メールは配備入力でアーキテクチャを変えず、実配備試験は実装工程の合格gate。
- 対応結果：実装者が追加の商品判断なしにDB migrationと最初の統合試験を書ける。SQL/RLSの実行結果が仕様と違う場合は design.md の契約を薄めず停止して相談する。
