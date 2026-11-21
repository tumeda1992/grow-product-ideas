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

<a id="iteration-0-record-2"></a>

### 事後記録: 長時間offlineの再発と、復旧操作の誤案内を区別して残す

#### 再構成の出典と、記録が遅れた理由

11月13日の再開から14日の実行復帰までのchat・tool結果と、復帰後の実fileを照合した記録である。
切断中はrepositoryへ書けなかったため、当時保存したかのように記さず、今回の再開時に追記する。
元作業は70の承認済み五fileの反映後の確認だった。停止前にafterへの書込みは済み、後の検査と状態同期が未完であった。

#### 再発で確認できた事象

利用上限の回復後も、環境contextにはexecutorの設定capabilityの取得失敗とmanaged environment readinessのtimeoutが交互に現れた。
状態APIは現在のobserved phaseをrunningと返したがconnectivityはofflineで、shellは利用可能な環境が無いとして失敗した。
failureがnullであることやrunningの表示だけでは、ファイルの読取や書込みができる証拠にならなかった。
診断のmetadataには保持された記録が無く、停止の根本原因やタスクの正確な失効日時を確認する材料は得られなかった。
利用上限の回復、前回の作業からの経過、端末の変更を原因又は復旧条件と断定できる結果ではない。

再開時には、以前cacheした監視sourceとconfigを取得できなかったため、環境外のtool orchestrationで簡易の監視を組み直した。
その実行中は状態確認とshellのprobeを続けたが、復帰は確認できず、その後監視を停止した。
停止後も監視が常駐している状態にはせず、sourceやstoreの内容が会話・実行hostの終了を越えて必ず残るとも扱わない。

#### ユーザーとのやり取りで訂正したこと

assistantは使えるUIの復旧操作を確認せず、再接続・再起動を利用者へ頼んだ。利用者は次のように指摘した。

> は？こっちから打てる手はあるの？

調べられたtoolに再起動・期限延長の操作は無く、UIにその操作があるとも確認できていなかったため、その案内を訂正した。
スマホからPCネイティブアプリ、Safariでのログインし直しでも、各回の状態APIとshellはofflineと実行不能を返した。
利用者がOpenAIのサポートから求められてWi-Fiを携帯キャリア回線へ替えた後も、同じ実行不能を確認した。
これらから、利用者の操作不足とも、特定の端末・回線が原因とも結論していない。

利用者はタスクの有効期限と作業データを懸念した。assistantが短い引継ぎサマリを退避策として出したことへ、次の指摘があった。

> そんなサマリじゃ足りないくらい作業してんだよ

議論全文・内部記録・skillと設計書の変更・未追跡fileを、短いサマリから復元できないことを認めた。
アプリ側の添付情報やterminalの別経路も確認したが利用できず、その時点で実データの保全を実行できたとは報告しなかった。
接続不能とファイル削除を区別し、削除されたかどうかも確認不能と伝えた。
これらの過程は既存の監視実装の動作検証の不足と、assistantの確認前の案内・原データ保全の不足であり、利用者の設定の責任へ転嫁しない。

#### 実行復帰後に確認・保全したことと限界

利用者がサポートへ調査を依頼中に再確認を求めた時、pwdが成功し、同じ環境の状態APIもconnectedへ変わった。
feature-16の未コミット変更、議論と内部記録、作業用draftを実際に読めた。サポートの対応や端末の変更による復旧だったかは不明である。
repositoryの.git・未コミット・未追跡file、pluginの実体とgrow関連の一時資料を含む約25MBのarchiveを環境内の別directoryへ作り、2,372fileの内容一致を確認して利用者へlinkを渡した。
これは同じ環境内のコピーであり、利用者のPCへの保存完了を確認したものではない。chat transcript全体をarchiveへ含めたともしていない。

その後、利用者の明示指示でrepositoryの66fileを現状保存のWIP commit `fa38fa7` にし、origin/feature-16へpushした。
実際のremote HEADとの一致と作業treeのcleanを確認した。途中の70の検査と、引用patch等の空白の指摘は未解消としてcommit messageへ残した。
/tmpのdraftやplugin cacheが、このpushでGitHubへ保存されたわけではない。
今回の再開では、70の実fileが承認済みafterと一致することから未完の確認を終え、71の提案へ進んだ。中断した五fileの書込みを再実行していない。
監視recipeと、70の完了・71の応答待ちを示すcheckpointも、接続中にtool側へcacheし直した。現在常駐の監視を起動した状態ではない。
根本原因の特定・環境の寿命延長・提供元の修正や外部へのescalateの受領は、この実行の成果には含めない。
