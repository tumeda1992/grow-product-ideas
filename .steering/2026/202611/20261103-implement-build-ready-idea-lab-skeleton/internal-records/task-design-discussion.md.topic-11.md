# 内部検討記録: 論点11 — 受け入れ基準と「1件を通し始められる」の観測方法

**discussion:** [task-design-discussion.md](../task-design-discussion/task-design-discussion.md)

**論点:** 論点11

## 開始context

論点1で、今回の終了状態を「最初のアイデアを1件通し始められ、機能するレール」が存在することとし、「1件を通し始められる」ことを観測できる形で受け入れ基準に置くと決めた。観測の方法はdesign.mdにTBDとして残っている。

論点3で、各fileは「見出し構成の合意 → 作成 → 実fileのreview」で作ると決めた。個々のfileのreviewは各fileの作成時に行う。この論点で決めるのは、全fileが揃った後に、レール全体として受け入れられるかを何で確かめるかである。

論点5・6で、レールはCodexでも動かす可能性がある（「Codexでも使うかも」）とし、skillとプロジェクト指示を両agentから読める配置にした。

<a id="iteration-0"></a>

## イテレーション0: 何を観測すれば受け入れられるか

<a id="iteration-0-record-1"></a>

### 調査: 実行環境

`which codex claude`で、`/opt/homebrew/bin/codex`（`codex-cli 0.163.0`）と`/opt/homebrew/bin/claude`があることを確認した。両方のCLIでレールを起動できる環境がある。

新しく作ったskillは、実行中のsessionには反映されない（`escalate-plugin-skill-fix`の「修正したskillは今実行中のsessionへ反映されない。skill内容はsession開始時に読み込まれる」と同じ性質）。動かして確かめるには新しいsessionが要る。

<a id="iteration-0-record-2"></a>

### 判断: 観測するものを静的な整合と動かした結果に分ける

- 静的な整合: skill間・file間の契約（skill名、材料の識別子、正本と材料の入口、テンプレートの一箇所性）が実fileで一致しているか。fileを読めば機械的に確かめられる。
- 動かした結果: 全体制御skillからアイデアを受け入れ、問い一つ分の内側のloop（問いの選択 → 層skill → 材料skill → 正本と`discussion.md`への記録 → 漏れの確認 → 閉じたの記録）が一周するか。「通し始められる」の最小の観測であり、層の閉じや出口まで進めると1件を通すこと（論点1で範囲外）に近づく。
- 使うアイデア: 試し用のアイデアを使い、確認後に`product-plans/<slug>/`を消す。実際の1件目は論点1のとおりこのsteeringの後に行う。
- Codex: 可能性の段階なので、Codexでskillとプロジェクト指示が読まれることだけを確かめ、loopの一周はClaude Codeで行う。

<a id="iteration-1"></a>

## イテレーション1: 論点1・12の決定を受けて、確かめるものを置き直す

入口は提案0への応答（内容は合意、検証は自演、終了状態の拡張）と、それを受けた論点1の再開と論点12の決定である。

<a id="iteration-1-record-1"></a>

### 判断: 自演の進め方

- 新しく作ったskillは実行中のsessionへは読み込まれない。自演は、assistantが各skillの`SKILL.md`を読み、書かれた手順どおりに進める形で行う。読み込みの仕組みは、新しいsessionでの確認（提案の3）に分ける。
- ユーザー役として答えたことは`discussion.md`に区別して残す。`product-plans/`は判断記録の堆積として残すため（論点1）、実際の利用者の判断と取り違えないようにする。
- 止まった・迷った箇所は、原因が担当skillの中身か接合面かを分けて直し、影響範囲を通し直す。
- 4は論点12から足した。build-readyで渡す要件を自演で確かめる。
