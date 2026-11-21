# 保存の境界を検査する

## 依頼と粒度

| 依頼した層と決めるもの | 何のため | 求めた粒度 | この材料で満たしたか |
| --- | --- | --- | --- |
| [どう解くか](../../how-to-solve/README.md) | Lの旧記録保全と同時書込み拒否を当てにしてよいか | 今のLinux/Python・同filesystemでの小さなprocess検査 | 6件を実行し期待通り。現在のprocess停止と排他の根拠を返す |

## 実行前に置く対象・方法・期待

verify-technical-feasibilityの方法で、主張を保存の境界に限定する。製品は実装せず、形の小さいJSONを二種類作って同じsystem callの性質を検査する。全ゲーム・CLI・データ検証はこの検査の対象外。

- 旧JSONはrev0、node root。新JSONはrev1、node a3。各試行は別の一時directoryで開始。
- 通常終了: 新JSONを全量読める。
- 一時fileをfsyncした直後にprocessをos._exitで終了: 本体は旧JSONを読める。
- os.replaceの直後に終了: 本体は新JSONを読める。表示の有無で成功を再判定しない。
- 対照: 本体を直接開きJSONの先頭だけを書いて終了するとJSONの読取りが失敗する。
- 固定lockfileを親processが排他保持し、別processが非blocking取得すると拒否される。解放後には取得できる。
- 期待と違えばLを選定の成立済み根拠にしない。得た範囲だけ返し、電源断の耐久性・任意OS・remoteFSの保証へ広げない。

## 中身

[probe.py](probe.py)が独立processを作り、[results.json](results.json)へruntimeと観測を保存する。成功例だけでなく停止・対照・排他を同じ実行で記録する。

## 確かめた方法と限界

上の期待を実行前に記した。実行後に観測を追記する。利用者の端末での導入、本製品の受入れ、実際の遊びの価値は未検査。

## 実行後の観測

2026-11-17、Python 3.12.14、現在のLinuxで実行。通常はrev1、切替前停止はrev0、切替後停止はrev1。直接上書きの対照はJSONが壊れた。別processのlock取得は保持中にexit23、解放後にexit0となった。6件が期待通り。切替後・表示前に止まる場合は起動時に現行rev/nodeを表示し、既に保存した手を人が再入力しない設計が必要。原fileを読んだだけで個々の利用者の判断を保証しない。電源断とdirectory fsyncは今回の検査外。
