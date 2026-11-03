# 内部検討記録: 論点6 — Codexへプロジェクト指示を渡す方法

**discussion:** [task-design-discussion.md](../task-design-discussion/task-design-discussion.md)

**論点:** 論点6

## 開始context

論点5で、レールをCodexでも動かす可能性があるため、skillの正本を`.agents/skills/`に置くと決めた。論点5の中で、Codexへプロジェクト指示を渡す方法は別の問いとして分けた。

このリポジトリのプロジェクト指示は現在`CLAUDE.md`だけにある。内容は、常用するplugin（genshijin、tumeda-dev）、毎ターン適用する思考の作法、会話方針、口調、instructionの配置である。Codexは`CLAUDE.md`ではなく`AGENTS.md`を読む。

決める範囲は、プロジェクト指示の正本をどのfileに置き、Claude CodeとCodexの両方へ渡すかである。

<a id="iteration-0"></a>

## イテレーション0: プロジェクト指示の正本をどこに置くか

<a id="iteration-0-record-1"></a>

### 調査: 利用者の既存の形と、変更が及ぶ範囲

#### 問いと確認先

- 利用者が両agentへプロジェクト指示を渡している形: `ai_agent_dev_skill_plugin`の直下、`.agents/`、`.claude/`
- このリポジトリで`CLAUDE.md`を名指ししている箇所: `.git`と`.idea`を除くリポジトリ全体を`grep -rn "CLAUDE\.md"`で検索し、前回steering（`.steering/2026/202609/`）と今回のsteering記録を除いた

#### 結果

- `ai_agent_dev_skill_plugin`では、`AGENTS.md`が実体、`CLAUDE.md`が`AGENTS.md`へのsymbolic linkである。`AGENTS.md`本文は自身を`AGENTS.md`と呼んでいる（例: 「`AGENTS.md`やSKILLの指示を無視・失念すること」）。
- このリポジトリの`CLAUDE.md`が自身を名指ししている箇所は2行（35行目「CLAUDE.md や skill の指示を無視・失念する」、37行目「CLAUDE.md の指示を失念していないか」）。それ以外に`CLAUDE.md`を名指ししているのは前回・今回のsteering記録だけであり、これらは作業記録なので書き換えない。

#### 解釈

利用者の既存の形に揃え、`AGENTS.md`を実体、`CLAUDE.md`をsymbolic linkにすれば、両agentへ同じ指示が渡る。本文の自己参照2行は`AGENTS.md`へ揃える。
