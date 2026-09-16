# 実装引き継ぎの独立評価

## 結論

**引き渡せる。** 指定された成果物だけから、会話の補足や重要な追加判断なしにCLIを実装できた。公開契約、抽出境界、失敗時の挙動、原本不変、テスト観点が相互に整合しており、重要な未決事項・矛盾は見つからなかった。`build-ready` 判定を支持する。

## 評価方法と対象

- 最初に `bounded/` 直下の `README.md`、`proposal.md`、`design.md`、`evidence.md`、`decisions.md`、`handoff.md`、`review.md` だけを読んだ。設計評価と独立実装・テストが終わるまで `validation/` は読んでいない。
- 文書に記載された要求から、捨てる評価用CLI `receiver/memo_day.py` と独立テスト `receiver/test_receiver.py` を作った。元成果物とリポジトリは変更していない。
- 最初の縦場面（重複・順不同の対象日を抽出）と、危険場面（不正UTF-8時の無部分出力、原本bytes/mtime不変）を含めて実行した。
- 設計評価後に既存 `validation/` を読み、試作を実行し、`review.md` 記載のハッシュと現物を照合した。

## 追加で判断した事項の分類

### 既に仕様に書いてある

| 判断 | 根拠 |
| --- | --- |
| CLIはDATEとFILEの2引数を受ける | `design.md:7` |
| DATEは厳密なASCII `YYYY-MM-DD` かつ実在日 | `design.md:7,22` |
| 有効見出し、同日重複、順序、無区切り連結、改行保持 | `design.md:9,14,24-28` |
| 不正暦日見出しは本文、問い合わせ日付の不正は終了2 | `proposal.md:24-25`、`design.md:11,28` |
| 一致あり/なし/利用エラーは終了0/1/2、失敗時stdout空 | `design.md:9-12`、`decisions.md:11-17` |
| 全体をUTF-8 strict検証し、成功後に1回だけ出力 | `design.md:23,26` |
| 読み取りのみでbytes/mtime不変 | `design.md:18,44`、`handoff.md:17,20` |
| 実装テストで再検証すべきT1〜T10 | `handoff.md:15-20` |

### 安く変えられる裁量

| 評価実装で選んだこと | 根拠・影響 |
| --- | --- |
| ファイル名を `memo_day.py`、テストを `test_receiver.py` にした | ファイル配置・関数名は裁量（`design.md:48-50`）。公開契約を変えない。 |
| 標準 `unittest` と `subprocess` を使った | テストフレームワークは裁量、`unittest` 推奨（`design.md:50`、`handoff.md:24`）。 |
| 診断を `error:` / `not found:` で始めた | 文言は全文固定せず原因を示す語だけが契約（`design.md:12,50`）。 |
| ディレクトリを `Path.is_file()` で事前排除した | ディレクトリは終了2という結果が仕様（`design.md:11`）。判定手段は内部詳細。 |
| 評価環境のPython 3.14.3で動かした | 最低Python版の宣言は実装先の裁量（`handoff.md:24,35`）。製品化時には選んだ最低版でも実行が必要。 |

### 重要な未決

なし。実装中に、価値、体験の流れ、保存形式、公開契約、実現可能性、費用を変える選択は発生しなかった。

## 実行した検査

- `python3 -m unittest -v`：7テストすべて合格。重複/順不同、見出し前除外、空一致と不存在の区別、余分な空白・接尾辞・不正暦日、CRLF・最終改行なし、不正DATE、不正UTF-8、FILE不存在/ディレクトリ、正常・失敗時のbytes/mtime不変を確認。
- `python3 -m py_compile memo_day.py test_receiver.py`：成功。
- 引数なし実行：stdout 0 bytes、stderrあり、終了2を確認。
- 既存 `validation/run_probe.py`：設計評価後に実行し `PASS: 8 cases`、終了0。
- `shasum -a 256`：`review.md:32-39` に記載されたREADME/proposal/design/handoff/evidence/decisions/validation 2ファイルの8ハッシュがすべて現物と一致。

## 照合結果

独立実装の抽出結果と既存試作の8ケースは同じ契約を表していた。既存試作が製品CLIの引数・I/Oエラー・mtime不変を扱わないという限界も、`evidence.md:35` と一致する。したがって試作を読まない段階でも設計単独で実装でき、後から試作へ寄せて仕様を補った箇所はない。

## 限界

- 評価用実装であり、製品の配置、利用README、実行権限付与、Macの利用者シェルでの一巡は未実施。
- macOS上のPython 3.14.3だけで実行した。製品が宣言する最低Python版での互換試験は実装先に残る。
- 読取不可は、この評価環境で権限条件を安定して作る試験をしていない。FILE不存在とディレクトリのI/O失敗経路は確認した。
- 100MB超やメモリ障害は試していない。これは公開契約を変えない許容済み負債で、見直し条件は `proposal.md:51,55` と `decisions.md:32` にある。
- 入力FILEと同一パスへのシェルリダイレクトによる切り詰めはプログラム開始前に起こるため、コードでは防げない。利用READMEでの禁止警告が引き継ぎに明記されている（`design.md:34`、`handoff.md:18`）。

## 引き渡し判定

実装者へ引き渡してよい。実装者は `handoff.md:5-20` の読み順・着手順に従い、最低Python版の宣言と利用READMEを裁量内で決め、同版でT1〜T10を通せばよい。仕様へ差し戻す重要事項はない。
