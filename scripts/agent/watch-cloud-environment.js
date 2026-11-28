// Tool-orchestration recipe for functions.exec, not a Node/shell daemon.
// Cache this source with store() while the workspace is available.
// The caller supplies CLOUD_WATCH_CONFIG; never hard-code an old environment ID.
async function watchCloudEnvironment(config, api) {
  const { tools, metadata, notify, store } = api;
  const intervalMs = config.intervalMs ?? 15000;
  const heartbeatMs = config.heartbeatMs ?? 45000;
  const now = api.now ?? Date.now;
  const pause = api.pause ?? (ms => new Promise(resolve => setTimeout(resolve, ms)));
  const statusTool = metadata.find(t => /cloud_environment_environment_status$/.test(t.name));
  const stateKey = config.stateKey ?? 'cloud-environment-watch/state';
  if (!config.repoRoot || !config.probePath) throw new Error('repoRoot and probePath are required');
  if (intervalMs < 0 || heartbeatMs < 0) throw new Error('negative interval');
  if (!statusTool || typeof tools.exec_command !== 'function') {
    return { state: 'monitor_unavailable', reason: 'required_tool_missing', checkpoint: config.checkpoint ?? null };
  }
  const quote = value => "'" + String(value).replace(/'/g, "'\"'\"'") + "'";
  let environmentId = config.environmentId;
  let previousState;
  let lastNotice = -Infinity;
  let attempt = 0;
  notify('クラウド環境の利用可能性の監視を開始する。');
  for (;;) {
    attempt++;
    let status;
    let state = 'status_unavailable';
    try {
      const result = await tools[statusTool.name]({});
      if (result.isError) throw new Error('status_tool_error');
      status = result.structuredContent;
      if (!status) status = JSON.parse(result.content.find(c => c.type === 'text').text);
      if (!status || !status.environment_id) throw new Error('missing_environment_id');
      if (environmentId && status.environment_id !== environmentId) {
        const changed = { state: 'needs_review', reason: 'environment_changed', attempt,
          checkpoint: config.checkpoint ?? null };
        store(stateKey, changed);
        notify('環境の識別子が変わった。保存済みの作業先と未完処理を照合してから再開する。');
        return changed;
      }
      environmentId = status.environment_id;
      state = String(status.observed_phase ?? 'unknown').slice(0, 40);
      const observationCurrent = status.observations_current === true && !status.status_error;
      if (observationCurrent && (['failed', 'deleted', 'terminated'].includes(state) ||
          ['stopped', 'deleted', 'terminated'].includes(status.desired_phase))) {
        const stopped = { state: 'blocked', reason: 'explicit_environment_stop', environmentId, attempt,
          checkpoint: config.checkpoint ?? null };
        store(stateKey, stopped);
        notify('環境の明示的な停止または起動失敗を検出した。未完作業を保持して停止理由を報告する。');
        return stopped;
      }
      if (!observationCurrent) state = 'status_not_current';
      if (state === 'running' && !status.failure) {
        const token = `${now()}-${attempt}`;
        const command = ['bash', quote(config.probePath), quote(config.repoRoot), quote(token),
          quote(config.expectedBranch ?? '')].join(' ');
        let probe = await tools.exec_command({ cmd: command, yield_time_ms: 1000, max_output_tokens: 500 });
        let output = probe.output ?? '';
        while (probe.session_id && probe.exit_code == null) {
          if (now() - lastNotice >= heartbeatMs) {
            notify('状態APIはrunningだが、作業先の読み書き確認を待っている。確認完了まで監視を続ける。');
            lastNotice = now();
          }
          probe = await tools.write_stdin({ session_id: probe.session_id, chars: '',
            yield_time_ms: 1000, max_output_tokens: 500 });
          output += probe.output ?? '';
        }
        if ([22, 23, 126, 127].includes(probe.exit_code)) {
          const reasons = { 22: 'workspace_not_writable', 23: 'workspace_or_branch_changed',
            126: 'probe_not_executable', 127: 'probe_missing' };
          const changed = { state: 'needs_review', reason: reasons[probe.exit_code], environmentId, attempt,
            checkpoint: config.checkpoint ?? null };
          store(stateKey, changed);
          notify('接続は戻ったが、作業先または書込みの確認が通らない。未完作業を再実行せず状態を確認する。');
          return changed;
        }
        if (probe.exit_code === 0 && output.trim() === `CLOUD_WORKSPACE_READY:${token}`) {
          const ready = { state: 'ready', environmentId, repoRoot: config.repoRoot, attempt,
            checkpoint: config.checkpoint ?? null, checkedAt: now() };
          store(stateKey, ready);
          notify('環境の復帰と作業先の読み書きを確認した。保存済みの状態を照合して、未完の作業から再開する。');
          return ready;
        }
        if (probe.exit_code === 0) {
          const invalid = { state: 'needs_review', reason: 'invalid_probe_output', environmentId, attempt,
            checkpoint: config.checkpoint ?? null };
          store(stateKey, invalid);
          notify('利用確認の応答が今回のprobeと一致しない。復帰済みとせず、確認処理を調べる。');
          return invalid;
        }
        state = 'workspace_probe_failed';
      } else if (observationCurrent && status.failure) state = 'environment_failure_observed';
    } catch (_) {
      // Status/probe transport failure is evidence of unavailability, not its cause.
      state = status ? 'exec_unavailable' : 'status_unavailable';
    }
    const waiting = { state, environmentId: environmentId ?? null, attempt,
      checkpoint: config.checkpoint ?? null, checkedAt: now() };
    store(stateKey, waiting);
    if (state !== previousState || now() - lastNotice >= heartbeatMs) {
      notify(`環境の復帰を待っている（${state}）。状態監視を続け、利用可能になったら未完作業を再開する。`);
      lastNotice = now();
    }
    previousState = state;
    await pause(intervalMs);
  }
}

const cloudWatchResult = await watchCloudEnvironment(CLOUD_WATCH_CONFIG, {
  tools, metadata: ALL_TOOLS, notify, store
});
text(cloudWatchResult);
