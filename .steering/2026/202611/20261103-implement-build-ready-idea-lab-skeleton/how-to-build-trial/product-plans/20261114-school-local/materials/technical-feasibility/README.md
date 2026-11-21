# technical-feasibility: SQLiteの更新・競合・再実行とbackupを、選んだ条件で確かめる

## 依頼と粒度

| 依頼した層と決めるもの | 何のため | 求めた粒度 | この材料で満たしたか |
| --- | --- | --- | --- |
| [どう作るか T1](../../how-to-build/README.md#材料への依頼)／実装・導入へ渡す設計 | D1/F1の保存と復旧が依れる性質を確かめる | 実際の条件・観測・反例・限界 | SQLiteの下記条件は確認済み。対象PCの実行条件は不足しており育て中 |

## 中身

### 実行前に定めた主張と条件

[情報のschema](../data-model/schema.sql)に対して、Python標準のsqlite3、SQLite WAL、foreign_keys=ON、busy_timeout=0を使う。
本実装での一process・直列の書込みより厳しい、同じDBへの二つの独立connectionの順序を制御して検査する。多host・高負荷の試験ではない。
全書込みはBEGIN IMMEDIATE、同じcommandの照合、tokenの比較、必要な業務の再検査、変更とcommandの記録、commitの順にする。

| 主張・条件 | 期待と反例の観測 |
| --- | --- |
| 原情報の現行と根拠を分けて読める | R1金曜の署名の後、R2木曜を現行にする。表示は木曜、根拠はR1・B1のまま。submittedは0。B2にすると旧署名を現行の根拠へ使わない |
| 同じR2でも古い変更は拒否する | 二つの読取りが同じtokenを得た後、一方の引受けを保存。もう一方の書込みは0件でrollbackし、先の担当を失わない |
| 異なる用件でも同じ人の枠は重ねない | S1/S2が同じ枠を選んだ状態で順に確定。二件目はoverlap、隣接する枠なら両方成功。直接のUPDATEで検査を迂回しない |
| 変更のまとまりは途中で割れない | tokenと根拠を変更後、次の制約に違反させる。token・根拠・commandが全て元へ戻る |
| 保存後の応答を失っても同じ要求で二重に適用しない | commit後に同じcommand/payloadと古いtokenを再送。根拠とtokenは増えず、同じIDで別payloadは拒否する |
| lockの拒否と古い前提を混同しない | AがBEGIN IMMEDIATE中にBを開始する。BはBUSY。A終了後に最新を読み、未実行なら再実行できる |
| 同じ用件の現行だけを参照する | S1のcurrent_revへS2しか持たない版を指定し、commit時の外部鍵で拒否する。根拠の空欄も拒否する |
| backupで整合した時点を読み戻せる | WALの書込み中に別connectionからbackupする。未commitの部分を含めず、commit後のbackupは全変更を含む。再openとforeign_key_checkで検査する |

codeは検査用でありアプリ本体ではない。SQLiteはsourceのdueや人が実際に署名した事実を検証しない。
calendarのtarget_payloadの比較・手動照合、UI、起動と停止、backup運用の人の時間は机上の設計又は実装後の受入れであり、このSQL実行の成功と混同しない。

## 確かめた方法と限界

この時点では実行前である。[probe.py](probe.py)で検査し、観測をこの材料へ追記する。
以前の二接続の検査はtransactionの条件が違えば拒否の表れ方が変わった。今回はBEGIN IMMEDIATEを選ぶ条件を明記し、更新0件をSQLite全般の保証にしない。

### 実行した条件と17項目の結果

Python3.12.14・SQLite3.53.1・Linux、WAL、外部鍵ON、busy_timeout=0、BEGIN IMMEDIATEで実行した。
[probe.py](probe.py)を `python3 probe.py` で実行すると、一時directoryのDBに対して検査しJSONを標準出力へ返す。
実際の観測は[observations.json](observations.json)へ保存した。アプリ本体を起動した結果ではない。

| 観測した性質 | 期待と実際 |
| --- | --- |
| 現行・署名・提出 | 現行R2は木曜、署名はR1のまま、submittedは0。本文B1なら旧署名を読め、B2なら現行の根拠として読まない |
| 同じR2の競合 | 先の引受けがtoken2で保存され、後の古い要求は更新0件。先の担当は失われなかった |
| 成功応答を失った再送 | 同じcommand/payloadはrepeat、token1・根拠一件のまま。同じIDで別payloadはcommand_id_reused |
| 部分保存の失敗 | 二件目の外部鍵違反で、token・一件目の根拠・commandが全て元に戻った |
| 別用件の同じ時間枠 | S1の確定後、S2はoverlapで全体をrollback。S2のtokenは0のまま。隣接する枠は二件とも保存できた |
| 更新による検査の迂回 | bookingの直接UPDATEはreplace_booking_in_transactionで拒否した |
| 原情報の変更 | S1の古い予約だけが外れ、S2の予約を失わずS1がR2になった |
| lock | 第二のwriterはSQLITE_BUSY/code5。古い前提の0件とは違った。lock解除後の明示の再実行は保存できた |
| 関係と根拠 | 他の用件だけに存在する版への現行参照と、空の根拠は拒否され、前の状態を保った |
| backup | 書込み中に別connectionからbackupするとcommit済みのtoken0・根拠0。commit後はtoken1・根拠1。再open後のforeign_key_checkは両方とも違反なし |

17はこのcodeの観測項目数であり、全故障を網羅した数ではない。
本文B2の検査は、現行の読取りが本文の意味を使うかを問うための検査用データの差し替えであり、本実装で過去のsourceをUPDATEする許可ではない。
この検査はcorrectsの同じ用件の検査やUIでの正規化まで実装していない。
calendar・人の実施・OSのアクセス制御・Webサーバの待受け・停電時のdiskの耐久性・多hostや負荷は未検証である。

### 設計へ返す事実と、残る対象の不足

D1/F1は、ここで確かめたSQLiteと接続・transaction条件で、比較と変更の原子性、共有する枠の拒否、要求の再実行と整合したbackupを根拠にできる。
BUSYを更新0件として扱わず、commandの照合と現行の再読取りを行う必要がある。
同じschemaでも、その契約を使わない本実装の正しさはこの結果からは言えない。

固定入力は「家の既存PC」で、OS・architecture・runtimeの導入方法と権限がまだ特定されていない。
今回のLinuxの観測を、そのPCで起動・保存・復元できる事実へ替えられない。
必要なのは対象PCの実行条件を特定し、選ぶruntimeとSQLiteの供給・版と、導入・起動・backup手順がその条件で成立する根拠である。
アプリ本体の先行実装や全環境の試験を要求するものではない。
実装後に使いやすさや全画面を試すこととは別に、どのPCへ何を入れる設計かが未決なので、層の閉じへ返す。
違う設備や有料の手段が必要なら、固定入力の費用・担い手の差としてhowへ返す。

### 読取りの欠けを直した後の追加検査

D1の初稿には選択・必要時間の保持が無かった。追加したschemaに対し[selection-probe.py](selection-probe.py)を実行し、[観測](selection-observations.json)を保存した。
R1・未予約で参加と15分を読め、R2へ変えると現行の再確認無しでは両方NULLだった。
R2に要確認と不明の分数を入れるとneeds_check/NULLで読め、R1の参加・15分は過去として保持された。
不明を0とせず、旧い値を自動的に現行へ使わない構造を確かめた。候補の計算や本人の判断を実測したものではない。
元の17項目は旧schemaでの観測として保持する。今回の追加tableは元のtriggerやtransaction契約を変えず、この追加の読取りを新schemaで確かめた。

### 修正後のschemaでの再照合

選択・必要時間を追加してschemaが変わったため、元の17項目も修正後の実物で再実行し、全て期待に一致した。
現在の[observations.json](observations.json)には検査したschemaのSHA-256を付けた。
修正前の[17項目の観測](observations-before-selection.json)と、その時の[schema](schema-before-selection.sql)も保持する。
追加の読取りの検査と合わせて、最終schemaへの根拠として使える範囲を示す。実アプリ・対象PCへの射程は変わらない。
