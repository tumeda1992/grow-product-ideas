# 導入設計

## 最小構成

PikaPods Grocy 1 pod、production/HTTPS、二人だけのuser、location「冷蔵庫」、quantity unit「個」、Never Expires。日常はStock overview、purchase、consume、訂正はinventory。不要featureは公式flagで確認できたものだけ隠し、期限・price・recipe等は使わない。

既定admin passwordは品目投入前にpassword manager生成値へ変更し、logout/new password loginを確認する。初回変更強制機能は約束しない。全user adminなので家族外を追加しない。

## X1-A 競合

架空product `X1-concurrent-<日時>`、location冷蔵庫、unit個、Never Expires、開始count=2。A/B双方で2を表示し、基準stock logの当該product transaction一覧を保存。A consume1、B purchase1を同じ表示からほぼ同時確定。両browser再読込後count=2、基準後にA consume1とB purchase1が各1件、余分transactionなしで合格。それ以外は不合格。1回で判定する。

## X1-B 到達後の応答消失

手動network切替は使わない。request送信前遮断では「未送信」、送信タイミング不明の遮断では「到達不明」であり、応答消失の合格試行に数えない。

desktopでPlaywrightを使う。事前に架空probe productで通常consumeを1回観測し、browser Network/Playwright logからmutationのURL・methodとproduct識別方法を確定する。本番試行ごとに新しい `X1-loss-<試行番号>-<日時>` を作成しinventoryでcount=2。対象user A、当該productのconsume transaction件数0、stock log末尾ID/時刻を基準として記録する。

対象 `consume 1` requestだけをrouteする。handler内で `route.fetch()` をawaitし、upstream status・完了時刻を記録する。2xx responseをharnessが受け取った後、pageには `route.fulfill()` せず `route.abort('failed')` して失敗表示/成功応答なしを作る。login、GET、他product、再取得requestは遮断しない。その後routeを解除し再接続/必要なら再loginする。資格情報・cookie・request bodyは記録しない。

再送前にoverviewとstock logを再取得する。有效試行（upstream 2xx完了＋pageに成功応答なし）の期待組は `(count=1, 基準後のA consume1 transaction=1件)` だけで、観測時刻を添えて「到達済み・反映済み・再送不要」と判定する。upstream完了を確認できない試行の `(2,0)` は、その観測時点で未反映に見えるだけで遅延requestが後からcommitしうるため、未反映確定や安全な再送根拠にしない。`(1,0)`, `(2,1)`, 件数>1、user/type/productを識別不能、pageが成功表示、overview/log取得不能は不合格。

`route.fetch()` が2xx前にthrow/timeoutした試行は到達・サーバ処理終了とも確認不能。直後と60秒後に同じoverview/logを記録しても参考観測に限り、`(2,0)`を最終状態と断定せず、そのproductへ再送・inventory訂正・削除をしない。後からtransactionが現れた時刻も追記する。overview/logが `(1,1)` でもharnessがupstream response完了を証明できないためX1-B合格に数えない。新productで最大3試行、かつ開始から20分で終了。どちらか先に達し有效試行を作れなければ「確認不能」、確認待ちを維持し、手動offlineで代用しない。Playwrightを使えるdesktopがなければ別の利用可能なdesktopで同手順を行う。それも無ければ確認不能。

## 証拠記録

各試行を `validation/x1-result-YYYYMMDD.md` にテンプレートで記録：日時/timezone、試行番号、browser/context A/B、架空product名、開始count、基準log末尾と該当件数、操作、route条件、`route.fetch` status/完了時刻、abort時刻、page表示、再取得count、追加logのuser/type/amount/件数、分類、判定。screenshot/Playwright traceはownerの暗号化私的保管先へ置き、文書には相対的な証拠名とSHA-256だけを書く。URL、email、password、cookie、token、実在庫は保存しない。

## backup・停止

pod停止→全persistent fileをSFTP取得し、Database accessがあれば全DB dumpも取得。秘密なし環境設定一覧と、password manager内の秘密を組にする。空podへ公式手順でrestoreしuser/product/stock/logを確認。版違い、migration error、restore不能なら元podを削除しない。X1不合格/確認不能も実在庫を入れず、自作再検討。削除/解約は別途許可を待つ。
