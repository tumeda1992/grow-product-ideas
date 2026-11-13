import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, mkdtemp, writeFile, readdir, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { execFileSync, spawnSync } from 'node:child_process';

const source = await readFile(new URL('./watch-cloud-environment.js', import.meta.url), 'utf8');
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
const watch = await new AsyncFunction(source.split('\nconst cloudWatchResult =')[0] + '\nreturn watchCloudEnvironment;')();
const current = (extra = {}) => ({ environment_id: 'env-test', observed_phase: 'running',
  desired_phase: 'running', observations_current: true, failure: null, ...extra });
const success = command => ({ exit_code: 0,
  output: `CLOUD_WORKSPACE_READY:${command.match(/'(\d+-\d+)'/)[1]}\n` });

function harness(statuses, probes = []) {
  let time = 1000;
  let pauses = 0;
  let statusCalls = 0;
  let probeCalls = 0;
  const notices = [], states = [];
  const api = {
    metadata: [{ name: 'cloud_environment_environment_status' }],
    tools: {
      cloud_environment_environment_status: async () => {
        statusCalls++;
        const next = statuses.shift();
        if (next instanceof Error) throw next;
        if (!next) throw new Error('status sequence exhausted');
        return { structuredContent: next };
      },
      exec_command: async ({ cmd }) => {
        probeCalls++;
        const next = probes.shift();
        if (next instanceof Error) throw next;
        return next ? next(cmd) : success(cmd);
      }
    },
    notify: message => notices.push({ message, time }),
    store: (_, state) => states.push(state),
    now: () => time,
    pause: async ms => { if (++pauses > 20) throw new Error('unexpected endless polling'); time += ms; }
  };
  return { api, notices, states, counts: () => ({ statusCalls, probeCalls, pauses }) };
}
const config = { repoRoot: '/workspace/example', probePath: '/workspace/example/probe.sh',
  environmentId: 'env-test', checkpoint: 'approved-change-not-applied' };

test('waits through startup and exec transport failure, then verifies actual workspace', async () => {
  const h = harness([current({ observed_phase: 'starting' }), current(), current()],
    [new Error('exec-server transport disconnected')]);
  const result = await watch(config, h.api);
  assert.equal(result.state, 'ready');
  assert.equal(result.checkpoint, config.checkpoint);
  assert.deepEqual(h.counts(), { statusCalls: 3, probeCalls: 2, pauses: 2 });
  assert(h.states.some(s => s.state === 'exec_unavailable'));
});

test('stale readiness or failure and a failed status request never decide readiness or stop', async () => {
  const h = harness([current({ observations_current: false }),
    current({ observations_current: false, observed_phase: 'failed', failure: 'old failure' }),
    new Error('status transport'), current()]);
  const result = await watch(config, h.api);
  assert.equal(result.state, 'ready');
  assert.equal(h.counts().probeCalls, 1);
});

test('reports ongoing waiting without giving up on a long startup', async () => {
  const h = harness([...Array.from({ length: 8 }, () => current({ observed_phase: 'starting' })), current()]);
  assert.equal((await watch(config, h.api)).state, 'ready');
  const waits = h.notices.filter(n => n.message.startsWith('環境の復帰を待っている'));
  assert.deepEqual(waits.map(n => n.time), [1000, 46000, 91000]);
});

test('environment identity change preserves checkpoint and does not run shell', async () => {
  const h = harness([current({ environment_id: 'different-environment' })]);
  const result = await watch(config, h.api);
  assert.equal(result.reason, 'environment_changed');
  assert.equal(h.counts().probeCalls, 0);
  assert.equal(h.states.at(-1).checkpoint, config.checkpoint);
});

test('branch changes, missing probe and write failures require review rather than replay', async () => {
  for (const code of [22, 23, 127]) {
    const h = harness([current()], [() => ({ exit_code: code, output: '' })]);
    const result = await watch(config, h.api);
    assert.equal(result.state, 'needs_review');
    assert.equal(result.checkpoint, config.checkpoint);
    assert.equal(h.counts().pauses, 0);
  }
});

test('an explicit startup failure stops with its checkpoint', async () => {
  const h = harness([current({ observed_phase: 'failed', failure: 'startup failed' })]);
  const result = await watch(config, h.api);
  assert.equal(result.state, 'blocked');
  assert.equal(result.checkpoint, config.checkpoint);
  assert.equal(h.counts().probeCalls, 0);
});

test('a successful exit with an old token is not evidence of recovery', async () => {
  const h = harness([current()], [() => ({ exit_code: 0, output: 'CLOUD_WORKSPACE_READY:old-token\n' })]);
  assert.equal((await watch(config, h.api)).reason, 'invalid_probe_output');
});

test('a yielded probe is polled to completion without starting another command', async () => {
  let token;
  const h = harness([current()], [cmd => {
    token = cmd.match(/'(\d+-\d+)'/)[1];
    return { session_id: 4, output: '' };
  }]);
  h.api.tools.write_stdin = async ({ session_id }) => {
    assert.equal(session_id, 4);
    return { exit_code: 0, output: `CLOUD_WORKSPACE_READY:${token}\n` };
  };
  assert.equal((await watch(config, h.api)).state, 'ready');
  assert.equal(h.counts().probeCalls, 1);
});

test('real shell probe checks branch and writes, then removes only its temporary file', async () => {
  const dir = await mkdtemp(path.join(tmpdir(), 'cloud-probe-test-'));
  const probe = new URL('./probe-cloud-workspace.sh', import.meta.url).pathname;
  try {
    execFileSync('git', ['init', '--quiet', '--initial-branch=main', dir]);
    await writeFile(path.join(dir, 'keep.txt'), 'committed\n');
    execFileSync('git', ['-C', dir, 'add', 'keep.txt']);
    execFileSync('git', ['-C', dir, '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
      'commit', '--quiet', '-m', 'fixture']);
    await writeFile(path.join(dir, 'keep.txt'), 'uncommitted\n');
    const before = execFileSync('git', ['-C', dir, 'status', '--porcelain'], { encoding: 'utf8' });
    assert.equal(execFileSync('bash', [probe, dir, 'fresh-token', 'main'], { encoding: 'utf8' }),
      'CLOUD_WORKSPACE_READY:fresh-token\n');
    assert.equal(spawnSync('bash', [probe, dir, 'fresh-token', 'different']).status, 23);
    assert.equal(execFileSync('git', ['-C', dir, 'status', '--porcelain'], { encoding: 'utf8' }), before);
    assert.equal(await readFile(path.join(dir, 'keep.txt'), 'utf8'), 'uncommitted\n');
    assert(!(await readdir(dir)).some(name => name.startsWith('.cloud-readiness.')));
  } finally { await rm(dir, { recursive: true, force: true }); }
});
