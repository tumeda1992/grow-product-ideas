# レビュー結果

- 対象と版：2026-09-13版のproposal・design・handoff・evidence・decisions・validation（最終内容ハッシュは下記）。
- レビュー方法：受取視点の自己レビュー。
- 結果：合格。

## 実際に確認したこと

- 原文が問題を限定しているため、不要な別解釈を増やさず検索/編集を非目標にした。
- 自作推奨を原文、Python公式資料、POSIX awk仕様、V1へ逆照合した。
- 0円は許容制約、1.5〜3.5時間等は仮見積として分離した。上限時間は設定されていない。
- K1〜K3を選び、V1の実測と製品実装時に残るT9/T10を区別した。
- handoffだけで最初の縦場面と危険場面を実装する受取確認を行い、主要判断の欠落なし。

## 指摘と対応

| ID | 重要度 | 問題 | 対応 | 結果 |
| --- | --- | --- | --- | --- |
| RV1 | 重要 | 空一致と対象なしが同じ空出力 | foundを別管理し終了0/1に分離 | 解消、V1 |
| RV2 | 重要 | 不正UTF-8を途中まで出力しうる | 全体strict decode後に1回出力 | 設計で解消、T9へ |
| RV3 | 軽微 | 同一入力へのshellリダイレクトはプログラム外で原本を壊す | 利用READMEの禁止警告をhandoffへ追加 | 解消 |

## 完成判定

build-ready。要求・比較・CLI公開契約・重点リスク・実装順・合格条件が確定し、重要な未決事項はない。製品コード未実装と市場実証済みを意味しない。

## 最終内容ハッシュ

レビュー対象を固定するSHA-256：

```text
b25e1a3b567fbcf2ba271c35c4bc0da7cb7ed4e1ffbdf6fdce0162a1fc048bfb  README.md
02126f413f640b50a6dce1a80d16d629e0e9658d820064136297b3c5b01f9190  proposal.md
e10636ef3edafb78665e1bba6930378008829d1050cc9dbb16fd86a7a22a3820  design.md
5c6b6f4f03c3aad880368d082acc59e9e188893cfe2fb702fe532cfa81ae03a7  handoff.md
614e0177ca662cdd1ebc0b270b5a6cda12b3ff2e6289e85233dfc31f45cf631b  evidence.md
38759d708fe2b1297f89dc7ddfcd927269d89d74344a9fc4edf0939b8cd7c4d7  decisions.md
d94b101b5ebee34f847ac35531a0656d70698755c98a9645d36dfcde0593de18  validation/extractor_probe.py
5bc8de76f0280b375df5402c6c9b9e526f99e121c86c39d5246afb5e825146ee  validation/run_probe.py
```

## レールへ戻す学び

空の一致と不存在は出力だけでは区別できず、終了コードの早期確定が必要だった。今回の既存フローで扱えたため共通レール変更候補はない。
