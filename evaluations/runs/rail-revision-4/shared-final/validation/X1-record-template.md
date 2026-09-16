# X1実施記録

- 実施日・timezone：
- Grocy/PikaPods版・region：
- 実施者：仮名のみ
- 証拠保管先名・SHA-256：資格情報を含まない識別子のみ

## X1-A 競合

| 項目 | 記録 |
| --- | --- |
| product / 開始count | `X1-concurrent-...` / 2 |
| A/B browser context | |
| 基準log末尾・該当件数 | |
| A操作 / B操作 / 確定時刻 | consume 1 / purchase 1 / |
| 再取得count | |
| 基準後log（user/type/amount/件数） | |
| 判定 | 合格 / 不合格 |

## X1-B 応答消失

全体上限：最大3試行か20分の早い方。productを試行ごとに新規作成する。

| 項目 | 試行1 | 試行2 | 試行3 |
| --- | --- | --- | --- |
| 日時 / browser context | | | |
| product / 開始count | `X1-loss-1-...` / 2 | | |
| 基準log末尾 / A consume件数 | / 0 | | |
| route URL pattern / method（hostやtokenは伏せる） | | | |
| `route.fetch` status / 完了時刻 | | | |
| `route.abort`時刻 / page表示 | | | |
| 再取得count | | | |
| 追加log user/type/amount/件数 | | | |
| 観測時刻（直後 / 60秒後 / 後発） | | | |
| upstream未完了時に再送・訂正・削除しなかったか | | | |
| 到達分類 | 2xx後response loss / 到達不明 / 送信前失敗 | | |
| 組の分類 | `(1,1)` / `(2,0)` / 不整合 | | |
| 判定 | 合格 / 不合格 / 有效試行外 | | |

## 総合判定

- X1-A：合格 / 不合格
- X1-B：合格 / 不合格 / 確認不能
- X1：両方合格の時だけ合格。それ以外は不合格または確認不能。
- 次の処置：実在庫へ進む / 確認待ち維持 / 自作再検討
- 限界・異常：

password、email、URL全文、cookie、token、request body、実在庫名は記録しない。screenshot/traceは暗号化私的保管とし、この文書には証拠名とSHA-256だけを残す。

`route.fetch` の2xx完了がない試行では、どの観測時点の `(2,0)` も未反映確定にしない。遅延commitの可能性が残るため、そのproductを変更せず、X1-Bは確認不能のままとする。
