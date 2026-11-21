# クラウド環境の切断から作業を再開する

作業中に環境が`unavailable`・`starting`となった時、または実行基盤との接続が切れた時は、切断の報告だけでturnを終えない。
待機と監視を利用者へ伝え、復帰を確認して未完の作業へ戻る。
開始条件は状態通知と`exec-server transport disconnected`・再接続timeout等の実行基盤の失敗である。
通常のプログラムやテストの失敗は、環境停止とは分ける。
providerが停止する原因・アイドル時間の規則は、この事例からは確認できていない。

## 環境内の確認と、環境外の監視

`probe-cloud-workspace.sh`は、repositoryとbranchを照合し、一時fileへ読み書きして片付ける確認用のscriptである。
環境内のシェルが使えない間、このscript自身を常駐させて監視できるとは扱わない。

`watch-cloud-environment.js`は、エージェントの`functions.exec`で動くtool orchestrator用のrecipeである。
環境と別に呼べる状態APIを15秒ごとに確認し、現在の`running`が確認できたらシェルprobeを呼ぶ。
状態APIだけが復帰しても作業先の実行と読み書きが通るまでは待つ。
状態変化と45秒ごとの待機通知を行い、復帰時にcheckpointを返す。
待機の時間経過だけを理由に、起動処理を打ち切らない。

## 接続中にrecipeと再開点をcacheする

これはNodeで起動するdaemonではない。以下は`functions.exec`で実行する。
`repoRoot`・branch・checkpointは実際の作業に合わせる。
既存の環境IDを別のtaskへ使い回さない。

```javascript
const repoRoot = '/workspace/grow-product-ideas';
const read = await tools.exec_command({
  cmd: 'cat scripts/agent/watch-cloud-environment.js',
  workdir: repoRoot, max_output_tokens: 6000
});
if (read.exit_code !== 0) throw new Error('monitor source unavailable');
store('cloud-environment-watch/source', read.output);
store('cloud-environment-watch/config', {
  repoRoot,
  probePath: repoRoot + '/scripts/agent/probe-cloud-workspace.sh',
  expectedBranch: 'feature-16',
  checkpoint: { pending: '合意済みの未反映の変更と、続きの論点をここに記す' }
});
```

復帰確認後は、返った環境IDをこのtaskのconfigへ保持する。
次の監視中にIDが変わったら、別の環境へ書込みを再実行せず、repositoryと未完処理を再確認する。

## 切断時に待機し、復帰を確認する

先に「環境の復帰を監視して待っている。利用可能になったら続きを再開する」と利用者へ伝える。
cacheしたrecipeを次の`functions.exec`で実行する。
workspaceを読めない最中に、同じworkspaceからrecipeを読み直そうとしない。

```javascript
// @exec: {"yield_time_ms": 1000, "max_output_tokens": 1000}
const source = load('cloud-environment-watch/source');
const config = load('cloud-environment-watch/config');
if (!source || !config) throw new Error('monitor not initialized');
const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
await new AsyncFunction('tools', 'ALL_TOOLS', 'notify', 'text', 'store',
  'CLOUD_WATCH_CONFIG', source)(tools, ALL_TOOLS, notify, text, store, config);
```

`Script running with cell ID ...`となったら、同じcellを`functions.wait`で待つ。
監視中の通知は`notify`から届く。必要なら会話でも現在の状態を説明する。
同じ監視を重ねて起動したり、起動処理が長いという理由だけで利用者へ再起動を要求したりしない。
利用者が中止したら監視を終了し、未完の作業を保持する。

## 戻ったら未完部分を照合する

`ready`が返ったら、checkpointの対象fileと合意・現在の内容を読み直す。
中断直前の書込みが成功していた可能性もあるため、書込み・commit・push等を盲目的に再実行しない。
保存済みの処理は飛ばし、未完部分から元の作業や議論をそのturnで再開する。
checkpointも現在の未完部分へ更新する。

`needs_review`は、branchや環境IDの変更、書込み確認の失敗、probeの欠落等である。
この場合も元作業を捨てず、作業先の照合やprobeの復元等、返った理由に沿って復帰処理を続ける。
`blocked`は明示的な起動失敗・停止等で、原因と未完部分を報告する。
必要なtoolそのものが無い場合は、監視できていると称さず、その不足を明示する。

このrecipeはエージェントの実行が継続している間の監視であり、会話や実行host自体が終了した後の常駐サービスではない。
その場合は再開した担当が記録を読んで復帰処理を引き継ぐ。

## 検証

```sh
node --test scripts/agent/watch-cloud-environment.test.mjs
bash scripts/agent/probe-cloud-workspace.sh /workspace/grow-product-ideas manual-check feature-16
```

mockで起動待ち・transport失敗・古い状態・状態通知・環境変更等を試す。
本物のシェルprobeは一時repositoryでも試し、未commitの変更を保ち、一時fileを残さないことを確認する。
本物のクラウド環境を意図的に停止する試験は含めていない。
