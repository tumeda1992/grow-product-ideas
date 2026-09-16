# 判断履歴

## D1（置換済み）専用Web自作

2026-09-13、担当エージェントが自律確定。共有メモの絶対値上書きを差分RPCで解くため自作を選んだ。独立受取レビューでI1/I2が判明し、さらにmanaged Grocyを比較せずself-hostedだけで棄却していたためD2で置換。

## D2 管理Grocyを先に試す

- 日付・判断者：2026-09-14、担当エージェント。
- 状態：自律確定。
- 結論：PikaPods上のGrocyを最小設定し一週間試す。
- 理由：クラウドを既製/自作へ対称に許すと、2 USD/月から、管理済み、purchase/consume/inventory、Web/PWA、複数userを既製品で得られる。自作16〜30hより一週間試用へ早い（E3/E4）。
- 逆転条件：checkout>月1,000円、非公開不成立、期限入力を省けない、操作過剰、または実挙動で在庫更新を失う。
- 影響：自作DB/API/UI/handoffを現在案から除去。I1/I2は自作へ戻る場合に先に解消する条件として保持し、現導入の未決仕様にはしない。

## D3 最小Grocy運用

- 状態：自律確定。
- 結論：production mode、既定admin資格情報即時変更、二人だけのuser、location「冷蔵庫」、quantity unit「個」、Never Expires、価格0/任意、不要feature無効。日常はstock overviewからpurchase/consume、訂正はinventory。
- 理由：E3で確認できた製品機能だけでR1〜R6を満たす。改名/削除/復元は一週間の必須場面でなく提供を約束しない。

## D4 資格情報とバックアップ

- 状態：自律確定。
- 結論：PikaPods/Grocyのowner資格情報は本人がpassword managerで生成・保管。初回変更をアプリに強制させるとは約束せず、導入者が既定adminを最初に変更して再ログイン確認後に品目登録する。backupはPikaPodsのpod data全体を取得し、その同じGrocy版の空podへ戻すリハーサルを合格gateにする。
- 理由：初回変更フラグやCSVだけのID再構成を独自仕様にしない。製品のdata一式を可搬単位とする。
