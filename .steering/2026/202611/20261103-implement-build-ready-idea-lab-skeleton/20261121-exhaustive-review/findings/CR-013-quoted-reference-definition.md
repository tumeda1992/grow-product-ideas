# CR-013　引用内の参照定義を見落とし、壊れた出典を0リンク・正常で渡せる

- 優先度　P2
- 対象スナップショット　`4b8dc31c0e8242bcda6fd2a2746b25e997b23243`。[内容ハッシュ](../evidence/snapshot.json)
- 対象　[.agents/skills/grow-product-idea/scripts/check-plan-links.py L124–156](../../../../../../.agents/skills/grow-product-idea/scripts/check-plan-links.py)、[product-plans/README.md L103–118](../../../../../../product-plans/README.md)
- 観点　参照検査、持出し
- 由来　全体レビュー。論点105で導入した現行checkerで再現。
- 採否　未判断
- 対応状況　未着手
- 適用枠　挙動変更が必要（見落としたリンクの検査結果と終了値を、文書化した契約に揃える）
- 依存する指摘　なし

## 問題と根拠

CommonMarkの引用ブロック内にも参照定義を置ける。checkerは行頭から空白3個までの定義を認識し、引用の `>` を処理しない。短縮参照は定義側で調べた前提で読み飛ばすため、引用内の原資料を指すリンクが壊れていても `ok=true`、ローカルリンク0件を返す。規約は対応できない有効な記法も『未検査』として返すと約束している。原文の引用や調査記録で発生し得る。

## 改善案

Markdownのブロックと参照定義を解釈して検査する。または、対応する文法を絞る場合は引用内の定義を未検査として拾い、実際の参照先を確認する現行の手順へ渡す。

## 振る舞いへの影響

有効な引用そのものは引き続き使用できる。壊れた根拠を0件検査で通していた返り値が変わる。

## 検証方法・証拠

実行済み。`evidence/check-handoffs.py` の短い引用をPandocのGFM readerでHTML化すると、実在しない `missing.md` へのリンクになる。現行checkerは終了0。引用を外した対照は同じ宛先を `missing-target` として終了2。修正後は双方を欠損または要個別検査にする。[再現用スクリプト](../evidence/check-handoffs.py)・[結果](../evidence/check-handoffs.json)

## 合意・適用記録

レビューと挙動変更を含む提案までを依頼範囲とした。採否は未合意。修正・修正後の検証・適用コミットはいずれも未実施。
