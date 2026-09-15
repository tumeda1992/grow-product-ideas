# 根拠

## 証拠一覧

### E1 Python標準ライブラリ

- 種別：外部資料。確認日：2026-09-13、公式Python 3.12/3.13文書を閲覧。
- 出典：https://docs.python.org/3.12/library/argparse.html 、https://docs.python.org/3.13/library/pathlib.html
- 分かったこと：`argparse`はCLI引数処理を提供し、`Path`はencoding指定の読取りおよびbytes読取りを提供する。外部依存なしの構成が成立する。
- 限界：本案件固有の抽出規則は保証しない。R3/R5、D1に利用。

### E2 awk

- 種別：外部資料。確認日：2026-09-13、The Open GroupのPOSIX awk仕様を閲覧。
- 出典：https://pubs.opengroup.org/onlinepubs/009696799/utilities/awk.html
- 分かったこと：awkは入力を既定で行レコードとして順にパターン照合・処理でき、抽出代案として成立する。
- 限界：本案件の暦日検証、終了コード、UTF-8エラー時の無部分出力をそのまま提供する資料ではない。代案比較、D1に利用。

### E3 入力原文

- 種別：ユーザーの実例・制約。確認日：2026-09-13。
- 出典：[proposal.mdの入力原文](proposal.md)
- 分かったこと：形式、重複・順不同、単独Mac利用、原本不変、非目標、標準Python 3、現金0円。
- 限界：ファイル容量と利用頻度は未提示。R1〜R5、D1〜D4に利用。

## 検証結果

### V1 抽出ロジック試作

- 状況：合格。対象：K1、K2のUTF-8事前検証、設計版2026-09-13。
- 環境：macOS上のPython 3、標準ライブラリのみ。
- 事前合格条件：重複/順不同、空一致、対象なし、厳密でない見出し、不正暦日見出し、最終改行なし、CRLF、不正UTF-8の8ケースが期待値どおり。
- 方法：[extractor_probe.py](validation/extractor_probe.py) を [run_probe.py](validation/run_probe.py) から実行。
- 観測：`PASS: 8 cases`、終了0。
- 限界：検討用ロジックであり製品CLIの引数/I/Oエラーやmtime不変は未実装。handoffのT9/T10で検証する。
- 反映：designの見出し判定、bytes保持、found分離、全体decode後出力。

## 調査の終了判断

自作対awkの逆転条件と標準Pythonでの成立が確認できた。外部API・有料製品は要求に不要で、追加の製品探索は推奨を変えない。残るファイル規模は運用観測で内部方式だけを見直せる。
