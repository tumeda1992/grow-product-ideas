# 導入設計

自作設計ではなく、確認済み製品機能、人の操作、未確認挙動を分ける。

## 構成・設定

| 手順 | 確認済み機能 | 人の操作 | 未確認/gate |
| --- | --- | --- | --- |
| hosting | PikaPodsがGrocy podを2 USD/月から提供し構成・DB・更新を管理 | checkout総額≤1,000円だけ購入 | 実円・税、provision結果 |
| 非公開 | Grocy production modeに認証、user管理あり | 既定admin passwordを最初に変更。二人目だけ追加。他userを作らない | ログアウト/未知userで在庫が見えないこと |
| 最小master | location、quantity unit、productがある | 「冷蔵庫」「個」、product最大50。Never Expires | 不要入力を実画面で省略できるか |
| 日常 | Stock overview、purchase、consume、inventory | 買ったらpurchase +数量、使ったらconsume +数量、誤数はinventory | 二ブラウザ更新、同時/通信失敗 |
| 可搬性 | PikaPodsはSFTP data取得を案内 | pod停止前にdata全体を取得 | 同版の空podへrestoreできるか |

不要featureは設定で可能なものだけ非表示化する。設定名を未確認のまま断定せず、Tasks/Chores/Batteries/Equipment等は公式configのfeature flagを使う。賞味期限関連はproductでNever Expiresを選び、表示が残っても使わない。shopping list、recipe、price、barcodeは使わない。

## 具体場面

- 初期：ownerがproduction modeとHTTPSを確認→既定admin password変更→ログアウト/再ログイン→二人目user作成→「冷蔵庫」「個」→牛乳、初期2をinventoryで設定。
- 使用：AがStock overviewで牛乳をconsume 1。成功表示後、Bが再読込して1を確認。
- 購入：Bがpurchase 1、Aが再読込して2を確認。
- 訂正：表示が3だが実物2ならinventoryで2へ合わせ、直後に両者が2を確認。
- 失敗：通信失敗/結果不明なら同じ操作を盲目的に再送せず、まずStock overviewとstock logを再読込して、対象品目・利用者・操作・数量・基準後の履歴から反映済みと特定できるか確認する。値が変わらないだけでは遅延中の処理を排除できない。成否を特定できなければ二人ともその品目の更新を止め、実物と以後の増減を私的なメモへ退避して相談する。未反映と推測して再送・inventory訂正しない。Grocyの全操作idempotencyは保証せず、この停止が日常的に必要なら採用を見直す。

## データ・履歴・離脱

Grocy自身のproduct、stock entry、stock log、user DBを正本とし、独自CSV schemaや安定ID再構成を約束しない。podを停止して取得した全persistent fileと、外部DBが表示される場合の全DB dumpを一組のbackup/restore単位とする。環境変数は別途設定値一覧を秘密値なしで記録し、秘密値はpassword managerで保持する。stock logは在庫transaction確認に使うが、商品改名前後名の回復は今回約束しない。一週間中はproductの改名・削除を原則行わず、誤名は試用終了後に修正する。どうしても直す場合は変更前名を二人の私的メモへ残すが、これは在庫復旧の正本ではない。

利用停止：最終backup取得→ローカルでfile/dumpの存在と非ゼロsize確認→別の空podへ公式手順でrestoreリハーサル。新podのGrocy版が異なる、環境変数が復元不能、起動logにmigration errorがある場合は元podを削除せず停止する。解約・削除は別途ユーザー許可後だけ。二人目離脱はGrocyのuser削除後、旧資格情報でlogin不可を確認する。

## 合格・停止

合格：二人だけがloginでき、逐次操作、[X1の競合・応答消失](validation/X1-procedure.md)、inventory訂正、50品目以下、backup/restoreが通る。X1は制御した到達済み操作の応答消失を確認するもので、任意の障害で成否が必ず分かるという保証ではない。停止：未認証閲覧、checkout>1,000円/月、期限入力を回避不能、競合後の算術/transaction不一致、結果を特定不能、restore不能。停止時は実データを増やさず自作再検討へ戻す。

## 今回提供しない契約

独自mutation/request_id、原子的RPC、RLS、archive復元、改名前後名履歴、CSVによる世帯/user ID再作成、初回password変更強制UIは存在しない。I1/I2はこれにより「曖昧なまま実装者へ渡す」のではなく、採用範囲から除去した。
