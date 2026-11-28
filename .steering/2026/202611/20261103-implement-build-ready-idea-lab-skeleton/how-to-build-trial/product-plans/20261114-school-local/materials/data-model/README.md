# data-model: 原情報・実際の根拠・更新の前提・転記対象を分ける

## 依頼と粒度

| 依頼した層と決めるもの | 何のため | 求めた粒度 | この材料で満たしたか |
| --- | --- | --- | --- |
| [どう作るか D1](../../how-to-build/README.md#材料への依頼)／実装・導入へ渡す設計 | 表示とlogicが現行と根拠を使い、古い変更・結果不明から再開できるようにする | 案の差、SQLite案の型・鍵・制約・具体の読み書き | 構造と読み書き、指定保存条件の根拠を反映。対象PCの条件は不足 |

## 変えた所

| 変えた所 | 前の姿 | 変えた理由 | 前に読んだ依頼 |
| --- | --- | --- | --- |
| 選択と必要時間 | [初稿schema](../technical-feasibility/schema-before-selection.sql)に保持先が無い | E1/L1の入力とS2/S3/S7の読取りを支えるため追加。現行の再確認と過去を分ける | E1/L1/F1と層の初回の接続 |
| 保存の裏づけ | 指定の保存条件を要請した段階 | T1の最終schemaへの17項目と追加の読取りを受領。対象PCには広げない | F1と層 |

## 中身

### 読取りと変更から必要な事実を分ける

[体験](../experience-sketch.md)が表示する現行と過去の根拠、[logic](../core-logic.md)の入力から、次を必要とする。

| 情報 | 意味・出所と読取り／変更 |
| --- | --- |
| item.id | 原本の一件へ内部で採番する安定した識別。題名で統合しない。重複入力の疑いは人が原本を確認し、勝手にmergeしない |
| sourceの版 | 同じ用件の原情報の確認結果。締切・本文の識別・原本の場所・確認した人と根拠を保つ。現行だけitemが参照する |
| response_decision | 現行原情報で家族が選んだ参加・見送り・要確認と根拠。原情報が変わったら再確認の不足を読める |
| action_need | 現行原情報・行いの確認した必要分数と根拠。不明はNULL、未予約でも次の人が読める |
| item.token | 同じ原情報でも引受け・根拠・予定の変更が起きたことを比較する印。原情報の版とは別 |
| evidence | 実際の署名・持出し・回収と、その対象原情報・人・時点・根拠。訂正は元を参照する新しい根拠で残す。対象の違う用件は結べない |
| acceptance | 本人がどの原情報と行いを引き受けたか。名前だけの割当欄は作らない。現行と違えば再引受けが要る |
| booking | 同じ人の予約された行い・開始終了。全用件の非重複が必要。古い原情報の予約は変更時に外し、再判断する |
| calendar_ref | 人が何を反映しようとしたか、確認できたか、元の対象の内容。予定が存在するか不明を未作成としない |
| command | 保存した要求の識別・入力と結果のtoken。成功応答を失った同じ要求を二重に適用しないために保つ |

必要なのは原本の版と、訂正・照合に使う根拠であり、全操作の全履歴ではない。
根拠は元の記録を残し、訂正の対象を示す。実装側は同じ用件の根拠だけを訂正できるよう検査し、訂正済みの元の根拠は現行の判定から除く。
校内で実際に回収されたかは人が得る事実で、columnを置けば自動取得できるものではない。

### 構造の案と、層へ返す差

一つのJSON文書を原子的に置換する案なら、読取りは単純だが、比較と複数用件の時間枠・backupの整合を別に作る必要がある。
SQLite一fileの案なら、鍵・外部鍵・transactionと条件付き更新を使え、全用件の予約も同じtransactionで検査できる。
後者を使う場合の構造は[schema.sql](schema.sql)に示す。採用は層へ返し、この材料は保存方式を勝手に選定しない。

schemaはTEXTの識別子・固定形式の時刻、INTEGERの原情報の版とtokenを使う。
時刻は同じAsia/TokyoのISO8601 `YYYY-MM-DDTHH:MM:SS+09:00` に正規化し、必須・範囲・所要時間と固定の作業枠は入口のlogicで検査する。
SQLの制約を通るだけで業務の意味が正しいとはしない。特にevidenceの訂正先の同一用件、本人の実際の引受け、実際の学校での回収は別に確かめる。
bookingの変更はDELETEとINSERTを同じtransactionで行い、UPDATEで非重複のtriggerを迂回しない。原情報の変更では同じ用件の既存bookingを外す。

### 現行の読取りと、過去の根拠

```sql
-- 表示もlogicも同じ現行から読む。
SELECT i.id,i.token,s.rev,s.due,s.body_key,s.location
FROM item i JOIN source s ON s.item_id=i.id AND s.rev=i.current_rev;
-- 根拠は対象原情報と本文の意味を保持する。
SELECT e.id,e.kind,e.source_rev,src.body_key,e.actor,e.occurred_at,e.basis
FROM evidence e JOIN source src ON src.item_id=e.item_id AND src.rev=e.source_rev
WHERE e.item_id=:id
AND NOT EXISTS(SELECT 1 FROM evidence correction WHERE correction.corrects=e.id);
```

R1金曜・本文B1へ署名後、R2木曜・本文B1を現行にしても、R1の根拠をR2の署名へ付け替えない。
logicへは現行本文と根拠の本文を別に渡すので、締切のみの変更なら使え、本文B2へ変われば要確認と読める。
提出はsubmittedという実際の回収の根拠でのみ判断し、signedやcarriedから導かない。

### 条件付き更新・要求の再実行・共有資源

全ての書込みで、一つのconnectionの `BEGIN IMMEDIATE` から始める。
同じcommand.idが既にあれば、payloadが同じ時だけ前回の結果を返し、現在の表示は別に最新を読む。違うpayloadなら要求IDの再使用として拒否する。
未実行なら `UPDATE item SET token=token+1 WHERE id=:id AND token=:expected` を行い、0件ならrollbackし古い前提を返す。
その後、必要な変更とcommandの記録を同じtransactionで行い、commit後に成功を返す。
保存途中の失敗ではtokenも根拠も一緒に戻る。BUSYは0件の古い前提と別の結果で、開始できなかった／再確認が要ると機能へ返す。

同じR2で別の引受けが先に入ればtokenが変わるので、後から保存された古い画面は拒む。
別の用件S2ではtokenの比較は成功し得るため、予約の確定時には現在の全用件の枠をtransaction内で再読込みし、非重複を検査する。
非重複のtriggerも同じ人の交差する枠を拒む。枠を表示した時点だけの検査では足りない。

### 転記の対象は原情報の版だけでは足りない

同じR2でも、担当や作業枠が変わればcalendarへ渡す内容は変わる。
calendarのtarget_payloadは用件・行い・原情報の版・担当・開始終了を固定順のJSONで保持する。
現在の引受けと枠から作る同じ形式のpayloadと一致し、outcomeもconfirmedの時だけ「現行を確認済み」と読める。
無関係な根拠記録でitem.tokenが増えたことだけでは再転記を要求しない。一方、原情報が同じでも枠が変われば確認を要する。
markerは用件idと行いから固定し、例えば `S1/prepare` とする。原情報の版は内容へ含め、原情報の版ごと別予定を作る識別にはしない。
この差は体験の予定欄・機能の照合へ返す。

### 必要な技術と操作

T1へ、同じ接続内の比較・根拠・commandの原子性、古い書込み、別用件の枠の競合、成功保存後の再実行、SQLite backupからの整合した再読取りを要請する。
人がcalendarへ反映した実際の結果はこのDBでは保証できない。機能へ、対象のpayloadを先に残すことと、結果不明の手動照合を要請する。

## 確かめた方法と限界

読取りと変更の必要から対象・鍵・現行・根拠を分け、R1→R2、同じR2の更新、別用件の枠、同じR2の枠変更を机上で当てた。
schemaとqueryの実行の根拠はT1の返りを待つ。ここではSQLite案が実行・復旧済みとはしない。

### T1を受けた更新

[技術の観測](../technical-feasibility/README.md#実行した条件と17項目の結果)で、このschemaを使う指定のtransaction条件では比較・根拠・commandがまとまり、枠の競合と部分保存・backupを期待どおりに扱えた。
本実装は過去のsourceを不変として新しい版を追加し、bookingの変更はtransaction内のDELETE/INSERTで行う。
現行PCの実行条件とruntimeは未特定で、この裏づけをそのまま実製品の保存先へ広げない。

### S2・S3・S7から戻した、選択と残時間の保持

初稿の構造には家族の選択と、未予約の行いの必要時間を保持する対象が無かった。
体験やlogicの語が存在するだけでは、次の人がその情報を読めず、Hの引継ぎを支えられない。
response_decisionで用件・原情報ごとの参加／見送り／要確認、決めた人・時点・根拠を保持し、action_needで原情報・行いごとの必要分数と根拠を保持する。
必要時間のNULLは不明で、0分の候補にしない。本文や条件が変わった場合、古い選択と時間を新しい原情報へ自動コピーしない。
締切だけ変わった時も、現行の条件で参加と残りを確かめた本人が、根拠付きでR2の行を追加する。

```sql
SELECT d.choice,d.actor,d.basis,n.action,n.minutes,n.basis
FROM item i
LEFT JOIN response_decision d ON d.item_id=i.id AND d.source_rev=i.current_rev
LEFT JOIN action_need n ON n.item_id=i.id AND n.source_rev=i.current_rev
WHERE i.id=:id;
```

現行の選択や必要時間が欠けていれば要確認を返す。過去の行は別に読めるが、現行にあるようには表示しない。
選択・時間の再確認も用件のtoken比較とcommandを使い、一つのtransactionで保存する。
この変更をE1/L1/F1へ返し、前に読んだD1の構造だけでは全入力を保持できなかったことを明示した。
