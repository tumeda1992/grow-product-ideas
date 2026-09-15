# 導入引き継ぎ

これは導入手順であり、登録・購入・公開の許可ではない。

## 読む順序

README.md → proposal.md → design.md → evidence.md → review.md。版はversions.md。

## 許可後の実施順

1. PikaPods AppsのGrocy価格とcheckout税込円/月を確認。1,000円超、有料年契約、不要add-onなら停止。
2. Grocy podを1つ作成。production mode、HTTPS、専用URLを確認。demo/embedded等の認証無効modeなら停止。
3. 品目を入れる前に既定admin passwordを本人のpassword manager生成値へ変更し、ログアウト→新passwordで再login。アプリ側の初回変更強制は前提にしない。
4. 二人目userだけ作成。全userがadminであるため家族外を追加しない。ログアウト、誤password、未ログイン別ブラウザ、旧passwordで在庫が見えないことを確認。
5. location「冷蔵庫」、quantity unit「個」を各1つ作る。不要featureを確認済みflagで隠す。牛乳をNever Expiresで作りinventory=2。
6. **X1（実データ前の必須gate）**：架空の牛乳2を両ブラウザで開き、A `consume 1` とB `purchase 1`を更新前の同じ表示からほぼ同時に確定する。再読込後の最終2、stock logに各userの対応transactionが各1件あることを確認する。次に別の架空品目で操作確定直後に通信を遮断して応答を見失い、再送せずoverview/logを再読込して反映済み/未反映を一意に判定する。最終値・件数不一致、判定不能、盲目的再送が必要なら不合格。実在庫を登録せず自作案へ戻る。
7. 代表5品目で入力負担を確認後、最大50まで登録。期限や価格が必須で省けない、日常更新が許容できないなら増やさず停止。
8. PikaPods公式backup手順どおり、pod停止→persistent file全体をSFTP取得し、Database accessが表示される場合は全DBもexport→pod再開。秘密を含むのでownerの暗号化私的保管先へ保存。環境変数名と非秘密設定を別記し、秘密値はpassword managerへ保存する。空podを停止し、全DB tableを置換、fileを戻し、必要な環境変数を再設定して起動logとusers/products/stock/logを確認する。版違い/migration errorなら元podを維持して停止。追加課金や別podが必要なら事前許可を得る。CSVだけでIDを再構築しない。
9. 一週間、二人が通常利用。各日「記録し忘れ」「表示と実物の不一致」「結果不明」「余分で困った入力」を短く記録。7日後、重複購入/調理開始後不足が減ったかを具体例で判断する。未観測を成功にしない。

## 戻す・相談

停止時はbackupを取得し、podの削除/解約はユーザーの明示許可を待つ。相談条件：月額上限超、認証不成立、stock更新喪失、restore不能、家族外共有、独自機能要求。自作へ戻る場合、旧I1（全mutationのactor/operation/target/args一致再送契約とrequest-id conflict）とI2（改名前後名を履歴へ保存するか、回復を提供しないか）を実装前に確定する。

## 受取確認

育成担当が会話なしの導入者視点で確認。追加の商品判断なしに価格gate、認証、最小master、X1、backup/restore、一週間観測を開始できる。実資格情報とcheckout値は導入入力。X1は未決仕様ではなく外部製品の成立確認だがR2を左右するため、合格まで確認待ちを解かない。削除/解約はこの引き継ぎだけでは許可されない。
