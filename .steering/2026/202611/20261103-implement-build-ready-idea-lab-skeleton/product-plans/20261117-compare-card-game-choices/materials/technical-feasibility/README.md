# technical-feasibility: 同一ローカル環境の実行・確定保存・単一writerを調べる

担当方法: verify-technical-feasibility。同一実行者が適用し、技術の採否は行わない。

## 依頼と粒度

| 依頼した層と決めるもの | 何のため | 求めた粒度 | この材料で満たしたか |
| --- | --- | --- | --- |
| [how-to-solve R4](../../how-to-solve/README.md#材料への依頼) | R3が返したF構成を使える対象条件か判断する | runtime・UTF-8・同directory置換前後の停止・process単位lockの観測 | T1〜T4の限定観測を取得。日本語往復、置換前後、lock保持/解放を下記に記録。電源断/ゲーム本体は未検査 |

## 中身

### 取得済み環境

2026-11-17、操作対象の検査用workspaceのshellで取得した。Linux、Debian GNU/Linux 13 trixie、Python 3.12.14、Node v24.22.1。別の家のPCやスマホを確認したことではない。Python標準libraryだけを候補にし、新しい依存installは行わない。

### 実施前の主張と検査

| ID | 主張と条件 | 入力/観測点 | 期待・反例 |
| --- | --- | --- | --- |
| T1 | このPythonでUTF-8の理由をJSONへ書き戻せる | ゲームと無関係な日本語の合成文をensure_ascii=Falseで保存/再読 | 同じUnicode文字列。誤変換なら反例 |
| T2 | このfilesystem、同directory一時file+os.replaceで、置換前にprocessを終了しても旧確定fileが読める | 旧値0、候補値1。一時書込/fsync後、置換前にos._exit。親は既知の候補を渡さず確定fileだけ読む | 旧値0。途中の不完全JSONなら反例 |
| T3 | 同条件で置換後・画面出力前にprocessが終了しても、新確定fileを再開根拠に読める | 置換直後にos._exit。親は確定fileを再読 | 新値1。表示無しを未保存へ替えない |
| T4 | このLinuxのfcntl.flockが生存中のwriterを拒否し、process終了で取得可能となる | 親がLOCK_EX/LOCK_NB保持→子取得→親close→別子取得 | 生存中はBlockingIOError、close後は取得可。二つとも取得なら反例 |

probeはJSONとlockの小さい隔離データだけを使う。ゲームの状態遷移/branch/CLI/本製品は実装しない。write失敗/電源断/別filesystem/Windows/ネットワークFSはこの方法で保証しない。

## 確かめた方法と限界

方法と期待を先に保存した。これから実行し、対象に届かなければ成功として返さない。

### 観測と返り（2026-11-17）

[probe.py](probe.py)をPython 3.12.14で実行した。[observations.json](observations.json)に実結果を保存。

- T1: 保存/再読した日本語文字列は一致した。
- T2: 子processは一時書込後・置換前にexit 17。確定fileだけを読む側には旧version 0が残った。
- T3: 子processは置換直後にexit 18、標準出力は空。確定fileには新version 1が残った。表示が無くても未保存とは限らない。
- T4: 親がlockを保持している時の別processはblocked、close後はacquired。今回の単一writerの構成を支える観測である。

失敗した主張は今回無し。ただしT4の終了はcloseで解放したもので、SIGKILLや電源断を独立に試してはいない。T2/T3はos._exitによるprocess停止で、OS/電源断の耐久性を示さない。外部APIもゲームの処理も実装していない。F構成へ返せるのは、この対象で置換の前後とwriter拒否を区別できたこと。実装のschema検証や実際の操作・負担、全ての入力の正しさは未検証。
