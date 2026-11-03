# 内部検討記録: 論点5 — skillの配置先

**discussion:** [task-design-discussion.md](../task-design-discussion/task-design-discussion.md)

**論点:** 論点5

## 開始context

論点2でskill14種をすべて作ると決めた。前回designはリポジトリ構成で`.claude/skills/`を運用skillの置き場所としている。論点4で、前回designは保持対象ではなく、機能させるための仮説として扱うと決めた。

配置先は、レールをどのagentで動かすかで変わる。`.claude/skills/`はClaude Codeがリポジトリ内のskillとして読む場所である。Claude Code以外のagentでもレールを動かすなら、そのagentが読める場所や形式が要る。

決める範囲は、skill14種の配置先である。名前は別の論点で扱う。

<a id="iteration-0"></a>

## イテレーション0: レールをどのagentで動かすか

<a id="iteration-0-record-1"></a>

### 確認: 利用者がClaude Code以外のagentも使っているか

#### 問いと確認先

レールを動かすagentの候補を、利用者の既存環境から確認する。確認先は、このリポジトリの`CLAUDE.md`と、利用者が保守する`tumeda-dev` pluginのrepositoryである。

#### 結果

- このリポジトリの`CLAUDE.md`は、`tumeda-dev`のlocal開発時に`.agents/plugins/marketplace.json`のsourceを確認するとしている。
- `tumeda-dev` pluginは`plugins/tumeda-dev/.claude-plugin/`と`plugins/tumeda-dev/.codex-plugin/`の両方を持ち、Claude CodeとCodexの両方へ配布されている。plugin repository直下には`AGENTS.md`と`CLAUDE.md`の両方がある。
- 前回designの依頼原文には、骨格の後に「anthoropicのfableやopenaiのastraにちゃんと回していく」とある。fable・astraの作業は別issueであり、その中身は読まない（論点3の決定）。

#### 解釈と残る不足

利用者はClaude CodeとCodexの両方を使っている。ただし、このリポジトリのレール（アイデアを通す運用skill）をどちらのagentで動かすつもりかは、既存の記録からは分からない。これは利用者が決める前提であり、調べて確定できない。

<a id="iteration-1"></a>

## イテレーション1: Claude CodeとCodexの両方から読める配置にする

入口は認識合わせ0への回答「Codexでも使うかも」である。レールはCodexでも動かす可能性がある。

<a id="iteration-1-record-1"></a>

### 調査: 利用者が両agentへskillを見せている既存の形

#### 問いと確認先

利用者が既にClaude CodeとCodexの両方からskillを使っている形があるかを確かめる。確認先は`/Users/takahiroumeda/src/github.com/tumeda1992/ai_agent_dev_skill_plugin/`の直下と`.agents/`、`.claude/`である。

#### 結果

- `.agents/skills`は`../plugins/tumeda-dev/skills`へのsymbolic link
- `.claude/skills`は`../.agents/skills`へのsymbolic link
- `CLAUDE.md`は`AGENTS.md`へのsymbolic link。`.agents/`と`.claude/`配下にも同様の`CLAUDE.md -> AGENTS.md`がある
- `.agents/plugins/marketplace.json`が存在する

#### 解釈

利用者の環境では、`.agents/skills`を正本、`.claude/skills`をそこへのlinkとする形で、両agentからskillを使っている。Codexが`.agents/skills`を読むことは、この運用が成立していることを根拠とし、Codexの仕様文書は確認していない。

<a id="iteration-1-record-2"></a>

### 判断: skillの正本を`.agents/skills/`に置き、`.claude/skills`をlinkにするか

#### 必須条件

レールを動かす可能性のあるagent（Claude Code、Codex）の両方からskillが読めること。skillの二重管理が起きないこと。

#### 評価

- 提案する形は、利用者の既存運用と同じであり、両agentから読める実績がある
- `.claude/skills`は実体を持たないため、二重管理が起きない
- 代償はsymbolic linkが一つ増えること。後から移す場合はskill14種の移動と参照pathの修正が要るため、今置く方が安い

#### 範囲外として分けたもの

Codexへプロジェクト指示を渡す方法（`AGENTS.md`の扱い）は、skillの配置とは別の問いであり、別論点にする。
