# CR-009　最初の層の閉じを提案する前に、受け入れ後にしか作れない正本の節を検査する

- 優先度　P1
- 対象スナップショット　`4b8dc31c0e8242bcda6fd2a2746b25e997b23243`。[内容ハッシュ](../evidence/snapshot.json)
- 対象　[.agents/skills/grow-product-idea/SKILL.md L82–87・91–100](../../../../../../.agents/skills/grow-product-idea/SKILL.md)、[.agents/skills/grow-product-idea/templates/canonical.md L5–12・56–72](../../../../../../.agents/skills/grow-product-idea/templates/canonical.md)、[.agents/skills/grow-product-idea/templates/layer-record.md L6–11・15–19](../../../../../../.agents/skills/grow-product-idea/templates/layer-record.md)、[product-plans/README.md L103–118](../../../../../../product-plans/README.md)
- 観点　テンプレートと保存順序
- 由来　全体レビュー。論点105の参照検査と、受け入れ後に決定内容を正本へ書く順序の相互作用。
- 採否　採用
- 対応状況　適用・検証済み
- 適用枠　挙動変更が必要
- 依存する指摘　なし

## 問題と根拠

初回の層を準備した時点の正本には受け入れ時の情報だけがある。層の記録は、正本の『アウトカム』節へのリンクを持つ。ユーザーへ閉じを提示する前に案件全体を検査し、参照不成立なら提示できない。『アウトカム』節を正本へ書くのはそのユーザーが受け入れた後である。同じパスのまま作業を進めるには、どちらかの契約を破る必要がある。標準の最初の閉じを止めるためP1。

## 改善案

提案中の決めるものは層の記録またはその提案に置き、採用前の根拠リンクは現存する提案を指す。採用を受けた同じ更新で正本の節を作り、層からその節へ張り替えて双方を検査する。

## 振る舞いへの影響

受け入れていない提案や空の見出しが正本に入らず、全体の参照検査を有効にしたまま閉じを提案できる。

## 検証方法・証拠

実行済み。実テンプレート18行の参照を案件内に配置し、discussionは先に存在させた。閉じの提案前は `../README.md#アウトカム` だけが `missing-anchor` で終了2、正本に採用節を追加した対照は終了0。この実験は層全体や対話の実行を表さない。[再現用スクリプト](../evidence/check-handoffs.py)・[実測](../evidence/check-handoffs.json)

## 合意・適用記録

2026年11月21日、[論点1・提案0](../discussion.md#提案0論点1)への利用者の「ok」を受け、3ファイルへ適用した。
役割表の「言い切り」は同じ採用済みの意味へ語を同期した。
[ライフサイクル検査](../evidence/check-cr009-lifecycle.py)は8場面で期待に一致した。[実測](../evidence/check-cr009-lifecycle.json)
これはテンプレートを展開したfixtureと現行checkerの検証であり、agentの対話全体の実行ではない。
[適用記録](../application.md)からコミットと限界を辿る。
