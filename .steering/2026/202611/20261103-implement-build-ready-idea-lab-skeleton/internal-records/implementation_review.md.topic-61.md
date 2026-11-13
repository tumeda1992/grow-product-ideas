# 内部検討記録: 論点61 — クラウド環境の監視と復帰後の再開

**discussion:** [implementation_review.md](../implementation_review/implementation_review-61-65.md#論点61-クラウド環境の切断時に監視待機を伝え復帰後に作業を再開する)

**論点:** 論点61

## 開始context

実行サーバーのtransport切断と45秒の再接続timeoutを受け、環境がunavailableとなった。その後startingへ移り、今回の開始時には状態APIのrunning・observations_current=true、実際のshellとrepository読取の成功を確認した。
provider側で停止した原因や自動停止までの時間は未確認である。
利用者は切断の報告だけで止めず、エージェント側で監視し、待機を伝え、復帰後に作業・議論を再開する実装とescalateの記録を指示した。
未完の元作業は論点60の承認済みのwhatの局所改稿と、その反映後の論点59の条件の再検討である。

<a id="iteration-0"></a>

## イテレーション0: 監視・通知・照合・再開を繋ぐ

<a id="iteration-0-record-1"></a>

### 検証: workspaceが使えない間も監視でき、復帰と未完作業を取り違えないか

#### claim・方法・合格条件

監視はworkspaceのshellでなくfunctions.execのtool orchestratorで動かす。sourceを接続中にstoreし、切断中に再読を要求しない。
状態APIの現在のrunningと、repository・branch・読み書きprobeの実際の成功を復帰条件とする。
単にAPIがrunningを返すことだけで再開しない。古い観測・execの接続失敗・途中sessionも含めて確認する。
切断→starting→running、状態APIの失敗、状態APIはrunningだがexecが失敗、古い観測、定期の待機通知、環境ID・branch変更、明示的な起動失敗、probeの偽または古い出力をmockで試す。
本物のシェルprobeも一時Git repositoryと作業先へ当て、読み書きの成功と一時fileの片付け、branch不一致、既存の未commitの変更を保つことを確かめる。
成功するprobe以外は未完の書込みを再実行せず、状態とcheckpointを保持することを合格条件にする。
sourceをcacheして実toolで監視を実行し、現在の環境の利用可能性を確認する。
本物の環境を意図的に停止する試験は行わず、provider全体の可用性やturnを跨いだ常駐を保証しない。

#### 結果と実際の復帰・再開

監視recipe、シェルprobe、使い方、テスト、escalate用の006を作成した。
状態遷移のmockと本物のシェルprobeを合わせた9テストが成功し、bashの構文確認も通った。
古いfailedの観測で停止を決めてしまう問題は検討中に見つけ、現在の観測であることを停止の判断にも必要とする形へ修正して再検証した。
時間の経過だけで起動を打ち切らず、45秒ごとの通知が模擬時間で継続すること、途中sessionのprobeを新たに重ねて起動しないことも確認した。
環境ID・branchの変更、書込み不能、古いprobeの応答はreadyにせず、checkpointを保って照合へ返した。
一時repositoryでは未commitの変更がそのまま残り、probe自身の一時fileを片付けた。

監視sourceをfunctions.storeへcacheして実toolで起動した。状態APIの現在のrunningと、作業先・feature-16・実際の読み書きを確認してreadyを受け取った。
更新後のsourceもcacheし直して同じ実環境確認を通した。
その後、承認された論点60の応答を一度記録し、beforeのままだった対象へ提示済みのafterを反映した。
次に論点59の条件の作り直しへ戻り、子論点62の検討を開始した。監視だけ作って元作業を中断したままにはしていない。
checkpointも、60の適用済みと、59・62で残る条件の再検討へ更新した。

#### 確認できる限界と引渡し

意図的にクラウド環境を停止する試験、providerの自動停止の原因や一定時間、エージェントの実行host自体が終了した後の常駐は確認していない。
切断中に環境内のシェルscriptだけで監視できるという設計にはせず、実行hostのtool orchestrationと接続中のsourceのcacheを使う。
エージェントの実行hostも終了した場合は、次の担当がcheckpointと実fileを照合して再開する必要がある。
006の記録とscriptの使い方へのlinkは実在するfile・anchorへ解決した。
利用者は監視・通知・再開とescalateの記録を明示している。外部の提供元への送信・受領や、共有pluginの公開は未実施である。
