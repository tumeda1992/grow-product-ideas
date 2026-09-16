# 引き継ぎ

登録・購入・公開の許可ではない。README→proposal→design→本書→validation template→reviewの順に読む。

## 許可後

1. checkout税込円/月≤1,000円だけ進む。
2. Grocy pod、production、HTTPSを確認。demo/embeddedなら停止。
3. 品目前に既定admin password変更→logout→new password login。二人目だけ追加。未login/誤/旧passwordで在庫不可を確認。
4. 冷蔵庫/個/Never Expiresを作る。
5. design.md X1-Aを実行・記録。失敗なら停止。
6. design.md X1-BをPlaywrightで実行。productごとにbaselineを取り、`route.fetch()` 2xx完了後にpageへのresponseだけabortする。最大3試行/20分。upstream完了不明のproductは再送・訂正・削除せず、直後/60秒後と後発transactionを参考記録するが最終未反映とは断定しない。合格・不合格・確認不能をtemplateへ記録。不合格/確認不能は確認待ちを解かず実在庫を入れない。
7. X1合格時だけ代表5品目→最大50、backup/restore、一週間試用へ進む。

## 一週間と撤去

毎日、記録忘れ、実物不一致、結果不明、余分な入力を具体例で残す。7日後に重複購入/調理開始後不足が減ったか判断。停止前にfull backup/restore。pod削除/解約はユーザー許可後だけ。

## 相談条件

価格超過、認証不成立、X1不合格/確認不能、restore不能、家族外共有、独自機能。自作へ戻るなら、I1の全mutation再送契約とI2の改名前後名履歴/非提供を実装前に確定する。

## 受取確認

育成担当の自己確認。X1の初期値、送信前/到達不明/到達後の区別、安全な遮断、期待値/log組、証拠先、秘密除外、試行上限が揃い、実施者の追加判断なしに検証できる。実施結果は未提供で、成功とは判定していない。
