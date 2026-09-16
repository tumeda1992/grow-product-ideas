# X1：競合と応答消失の確認

製品実装ではなく、導入担当へ渡す未実施の検証手順。専用の架空データだけを使う。登録・課金・追加環境の権限を得るまで実行しない。production/HTTPS、既定資格情報の変更、二人だけのuserを先に確認する。

## 範囲と上限

X1-Aは二人の差分更新、X1-Bはサーバー応答を受け取ったが画面へ届けなかった場合の結果識別を確かめる。任意の通信障害で未反映を確定できること、全操作の冪等性、スマホ固有の通信挙動は証明しない。日常の到達不明はdesign.mdの停止手順を使う。

担当は二人分の独立browser contextを操作できる技術担当。Playwrightを使えるdesktopを用意し、実際の二台のスマホでは別途R1の逐次増減を確認する。既存環境がなければ許可されたdesktopを準備し、準備不能なら確認不能で止める。手動offlineを代わりの成功証拠にしない。

X1全体は環境準備を含め最大60分、うちX1-Bは最大3試行または20分の早い方で終了する。これは担当が採用する作業上限で、完遂時間の保証ではない。追加購入や上限延長は自動で行わない。

## X1-A

1. `X1-concurrent-<日時>` という新しい架空productを作り、場所「冷蔵庫」、単位「個」、Never Expires、開始個数2とする。基準stock log末尾を記録する。
2. A/B両contextで2を表示。各contextの対象mutationをrouteで保留するbarrierを設け、A consume 1、B purchase 1をクリックする。両requestが保留されたことを確認するまでupstreamへ送らない。片方が来ない場合は30秒で送信前abortし、確認不能とする。contextの設定とrequest特定には下記X1-Bの準備と同じ方法を使う。
3. 両requestを非同期に送信開始する。各routeで `fetch({maxRetries: 0, maxRedirects: 0, timeout: 30000})` の開始・完了時刻を記録し、一方の完了をawaitしてから他方を開始しない。追加mutationは遮断して不合格とする。得た応答を各pageへfulfillする。
4. 送信開始/完了区間が重なり、双方2xxで通常の成功表示となったことを確認する。重なりが観測できなければ有効な競合試行とせず確認不能。両者の再取得値が2、基準後にA consume 1・B purchase 1が各1件、余分なtransactionなしならこの試行の合格。違えば不合格、取得不能なら確認不能。1試行で終える。

これは同じ古い表示からの並行requestを制御するもので、DB内部の処理順まで強制しない。サーバーが正しく直列化するのは許容する。全競合の安全性証明ではなく、今回の二人・代表操作の成立確認である。通常利用で更新喪失が起きれば採用を見直す。

## X1-B

### 準備

Playwrightの新規contextでは `serviceWorkers: 'block'` とする。架空probe品目の通常consume 1を一度観測し、mutationのmethod、URL path、product識別方法を特定する。実URL・request body・資格情報は保存せず、検証中だけメモリ内で参照する。該当requestを一意に識別できなければ確認不能で止める。

試行ごとに `X1-loss-<番号>-<日時>` を新規作成し、開始個数2、Aによるconsume履歴0件、基準log末尾を記録する。他方の利用者はこの品目を更新しない。

### 応答だけを失わせる

1. 対象consume requestだけをrouteする。GET・login・他品目の操作は対象外。対象requestの検出とupstream送信を別々に数える。
2. 最初の対象requestでのみ `route.fetch({maxRetries: 0, maxRedirects: 0, timeout: 30000})` を実行する。以後の同じ品目へのmutationは送信前にabortし、再試行検出として記録する。
3. harnessがupstream 2xx応答を最後まで取得した時刻を記録し、画面へはfulfillせず `route.abort('failed')` する。2xx自体をデータ反映の証拠にはしない。
4. 対象品目のmutation遮断を残したまま、GETでoverview/logを取得する別ページから確認する。成功通知のない画面、個数1、基準後のA consume 1履歴が1件、余分な履歴なしを照合する。
5. `(個数1, 履歴1件)` で対象を特定でき、upstream送信1回・画面への成功応答なし・追加mutation試行なしなら有効試行の合格。成功画面、追加mutation試行、値や履歴の不整合は不合格。必要な観測が得られなければ確認不能。

harnessが再送を遮断して合格へ見せないため、追加mutation試行を検出した場合は失敗として扱う。対象品目の操作画面を閉じてから遮断を解除する。

### 到達不明・タイムアウト

`route.fetch` がthrow、timeout、非2xxなら有効な応答消失試行に数えない。直後・60秒後の値と履歴は参考として保存するが、`(2,0)` を未反映確定や安全な再送の根拠にしない。後からcommitする可能性がある。その品目へ再送・訂正・削除せず、後発履歴があれば記録する。新しい品目で上限内だけ再試行できる。

この条件で観測された `(1,1)` も、到達後の応答消失を制御できた証拠ではない。最大3試行/20分で有効試行がなければ確認不能。閲覧不能と製品の値不整合、試験操作の失敗を記録上で区別する。

## 記録と判定

[記録型](X1-record-template.md) から `x1-result-YYYYMMDD.md` を作る。日時・対象版・context・品目・初期値・基準履歴・操作・route条件・送信回数・upstream状態と時刻・画面状態・再取得値・履歴・判定・停止理由を残す。

認証情報を含むNetwork log/HAR/traceは保存しない。画面証拠が必要なら架空品目と結果だけへ安全化し、ownerの私的保管先へ保存する。文書には秘密を含まない証拠名とSHA-256を記す。

X1-A/Bとも合格のときだけX1合格。それ以外は確認待ちを維持し、実在庫を投入しない。不合格なら自作案を再比較、確認不能なら不足環境・観測手段と必要権限を記録して検証の再開可否を判断する。確認不能を製品欠陥とは断定しない。

## 手段の根拠

2026-09-15に [Playwright Route](https://playwright.dev/docs/api/class-route) で、fetchが応答をpageへ渡さず取得できること、abort、retry・redirect・timeout指定を確認した。[Network](https://playwright.dev/docs/network) はrequest interception時のService Worker遮断を案内する。これはharness方式の資料確認であり、Grocyに対して本手順を実行した結果ではない。
