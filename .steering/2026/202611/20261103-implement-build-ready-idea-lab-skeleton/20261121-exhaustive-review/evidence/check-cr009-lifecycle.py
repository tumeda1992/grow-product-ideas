"""Exercise CR-009 reference boundaries; fixtures simulate the documented writer steps."""
import json
import re
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

REVIEWED_HEAD = '29018ab3472c445ebe33190cb8d2f141f5d5096a'


def main():
    repo = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip())
    skill = repo / '.agents/skills/grow-product-idea'
    checker = skill / 'scripts/check-plan-links.py'
    layer_template = (skill / 'templates/layer-record.md').read_text()
    canonical = (skill / 'templates/canonical.md').read_text()
    initial = re.sub(r'<!--.*?-->', '', canonical, flags=re.S).split('## 前提にする条件')[0]
    initial = re.sub(r'\{[^{}]*\}', '試験用入力', initial)
    pointer = next(line for line in layer_template.splitlines() if line.startswith('- 決めるもの:'))
    assert '閉じ提案を保存済み' in pointer
    initial_pointer = re.sub(r'\{[^{}]*\}', '未採用。決め方の経過を参照', pointer)
    old_template = subprocess.check_output([
        'git', 'show', f'{REVIEWED_HEAD}:.agents/skills/grow-product-idea/templates/layer-record.md'
    ], text=True)
    old_pointer = next(line for line in old_template.splitlines() if line.startswith('- 決めるもの:'))
    old_pointer = old_pointer.replace('{節の名前}', 'アウトカム').replace('{節のアンカー}', 'アウトカム')
    observations = []

    with TemporaryDirectory() as temporary:
        root = Path(temporary)
        layer = root / 'why-to-build'
        layer.mkdir()
        (root / 'README.md').write_text(initial)
        (layer / 'discussion.md').write_text('# 決定過程\n')

        def record(state, target):
            (layer / 'README.md').write_text(
                '# 層の記録\n\n- 状態: ' + state + '\n' + target +
                '\n- 決定過程: [discussion.md](discussion.md)\n\n## 決め方\n\n検討中。\n'
            )

        def probe(name, expected_exit):
            proc = subprocess.run([sys.executable, str(checker), str(root)], text=True, capture_output=True)
            result = json.loads(proc.stdout)
            actual = {'name': name, 'expected_exit': expected_exit, 'exit': proc.returncode,
                      'local_links': result['local_links'],
                      'issues': [issue['kind'] for issue in result['issues']]}
            observations.append(actual)
            assert proc.returncode == expected_exit, actual

        record('決めている', old_pointer)
        probe('旧雛形は未採用の正本節を参照して失敗する', 2)
        record('決めている', initial_pointer)
        probe('新雛形の初回作成は未来の参照を持たない', 0)
        assert '### アウトカム' not in (root / 'README.md').read_text()
        proposal0 = '# 決定過程\n\n<a id="proposal-0"></a>\n\n## 閉じ提案0\n\n旧案。\n\n根拠: [材料](../material.md)\n'
        (root / 'material.md').write_text('# 材料\n')
        (layer / 'discussion.md').write_text(proposal0)
        record('閉じ待ち。[論点](discussion.md#proposal-0)', '- 決めるもの: [未採用案](discussion.md#proposal-0)')
        probe('保存済みの閉じ提案と根拠は採用前に検査できる', 0)
        (root / 'material.md').unlink()
        probe('提案の根拠を壊すと全体検査が失敗する', 2)
        (root / 'material.md').write_text('# 材料\n')
        proposal1 = proposal0 + '\n修正要求: 目標を修正。\n\n<a id="proposal-1"></a>\n\n## 閉じ提案1\n\n採用候補の内容V1。\n'
        (layer / 'discussion.md').write_text(proposal1)
        record('閉じ待ち。[論点](discussion.md#proposal-1)', '- 決めるもの: [修正案](discussion.md#proposal-1)')
        probe('修正後は旧履歴を保持して新提案へ参照する', 0)
        assert (layer / 'discussion.md').read_text().startswith(proposal0)
        assert '採用候補の内容V1。' not in (root / 'README.md').read_text()
        accepted = proposal1 + '\n受け入れ: 提案1を採用。\n'
        (layer / 'discussion.md').write_text(accepted)
        adopted = '### アウトカム\n\n採用候補の内容V1。\n'
        # Interrupt after the accepted canonical was saved, before layer pointers were switched.
        (root / 'README.md').write_text(initial + '\n## なぜ作るか\n\n' + adopted)
        probe('採用応答と正本だけ保存された中断点でも既存参照は実在する', 0)
        assert (layer / 'discussion.md').read_text() == accepted
        # Resume only the remaining synchronization; do not append the accepted section again.
        record('閉じた。[採用論点](discussion.md#proposal-1)', '- 決めるもの: [アウトカム](../README.md#アウトカム)')
        canonical_now = (root / 'README.md').read_text().replace('- 閉じた層: 試験用入力', '- 閉じた層: なぜ作るか')
        (root / 'README.md').write_text(canonical_now)
        probe('中断後の残り反映で正本参照と閉じた層の表示が揃う', 0)
        assert canonical_now.count('### アウトカム') == 1
        assert '- 閉じた層: なぜ作るか' in canonical_now
        assert (layer / 'README.md').read_text().startswith('# 層の記録\n\n- 状態: 閉じた。')
        assert '採用候補の内容V1。' in canonical_now
        proposal2 = accepted + '\n<a id="proposal-2"></a>\n\n## 開け直した案\n\n未採用の内容V2。\n'
        (layer / 'discussion.md').write_text(proposal2)
        record('開け直し', '- 決めるもの: [検討中の案](discussion.md#proposal-2)。前回採用: [アウトカム](../README.md#アウトカム)')
        probe('開け直しでは未採用案と前回の採用版を区別する', 0)
        assert (root / 'README.md').read_text() == canonical_now
        assert '未採用の内容V2。' not in canonical_now

    print(json.dumps({'scope': 'template-derived fixtures and existing link checker; not autonomous skill execution',
                      'source_baseline': REVIEWED_HEAD, 'observations': observations, 'ok': True}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
