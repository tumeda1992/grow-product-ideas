# 根拠

## 証拠一覧

### E1 入力原文

- 種別：ユーザーの実例。
- 確認日・方法：2026-09-13、提供発言を原文のまま proposal.md に保存。
- 分かったこと：二人、ブラウザ、品名と個数、最大50、手入力許容、非公開、月1,000円以内、共有メモで古い数へ戻った実例、不要機能、外部登録禁止。
- 分からないこと：利用頻度、端末OS、メール、実際に継続できる操作時間。
- 関係：R1〜R8、D1〜D3。

### E2 Google Sheets の共同編集と履歴

- 種別：外部資料（公式）。
- 確認日・方法：2026-09-13、[Google Docs Editors Help: Excel と Sheets の違い](https://support.google.com/docs/answer/9331278?hl=en) と [変更履歴](https://support.google.com/docs/answer/190843?hl=en-10) を閲覧。
- 適用条件：Web 版。料金と個人アカウント要件は今回未確認。
- 分かったこと：Sheets はリアルタイム共同編集、共有、自動保存、版履歴、セル編集履歴を持つ。
- 分からないこと・反証：資料は在庫用の差分更新、重複送信防止、スマホでの1タップ増減を保証しない。よって「絶対値の上書きを構造的に防ぐ」とは扱わない。
- 関係：D1。即日次善案だが R2 の確実性で自作に劣る。

### E3 Grocy の提供形態

- 種別：外部資料（公式）。
- 確認日・方法：2026-09-13、[Grocy 公式](https://grocy.info/) を閲覧。
- 分かったこと：食料・家庭用品管理の Web ベース self-hosted 製品で、最低在庫量など広い機能を持つ。Windows デスクトップ、Docker、Home Assistant の経路も案内される。
- 分からないこと：第三者マネージド版の価格・信頼性、二人向け権限の詳細。
- 関係：自宅サーバーなし、最小範囲という R4/R8 に対して過剰かつ配備制約が合わず棄却。

### E4 Supabase の価格・休止・バックアップ

- 種別：外部資料（公式）。
- 確認日・方法：2026-09-13、[Pricing](https://supabase.com/pricing)、[Free project pausing](https://supabase.com/docs/guides/platform/free-project-pausing)、[Database backups](https://supabase.com/docs/guides/platform/backups) を閲覧。
- 適用条件：Free plan、表示価格 USD。為替換算不要の0 USDのみ採用。
- 分かったこと：Free は月0 USD、DB 500MB、50,000 MAU、5GB egress。低活動なら7日程度で休止候補となり、復帰可能。Free には自動バックアップが含まれず、公式は定期的な `db dump` と外部保管を推奨。
- 分からないこと・反証：将来価格、実利用で休止を免れるか、サービス可用性。Pro は月25 USDからで、ユーザーの月1,000円上限内とは確認できないため自動移行しない。
- 関係：R6、D2、手動バックアップと休止時回復を設計へ反映。

### E5 Supabase のデータ境界と RPC

- 種別：外部資料（公式）。
- 確認日・方法：2026-09-13、[Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security) と [JavaScript RPC](https://supabase.com/docs/reference/javascript/rpc) を閲覧。
- 分かったこと：RLS と Auth を組み合わせブラウザからDBまで認可でき、`auth.uid()` で呼出者を識別できる。DB function を JavaScript client から RPC 呼出できる。公開 schema の表は RLS 有効化に加え grants も絞る必要がある。service role は RLS を迂回するためクライアントに置けない。
- 分からないこと：今回のSQLは実 Supabase 上で未実行。
- 関係：R2/R3、D2、K1〜K3。

### E6 Cloudflare Pages の静的配備と価格

- 種別：外部資料（公式）。
- 確認日・方法：2026-09-13、[Static HTML](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/) と [Pricing](https://developers.cloudflare.com/pages/functions/pricing/) を閲覧。
- 分かったこと：静的HTMLを直接アップロードでき、`*.pages.dev` が提供される。静的アセット要求は free/paid とも無料・無制限。今回は Pages Functions を使わない。
- 分からないこと：将来の価格・提供条件、実アカウントでの配備。
- 関係：R1/R6、D2。

## 検証結果

### V1 原子的な増減契約の検討用実行

- 対象：K1〜K4、設計版 2026-09-13。
- 状態：合格（検討用モデルに限る）。
- 入力・環境：Node.js、[validation/atomic-counter.mjs](validation/atomic-counter.mjs)。初期 count=2、二人の `-1/+1`、同一 request_id 再送、0未満、第三者、50/51品目。
- 事前合格条件：最終2、重複再送で再反映なし、負数/非メンバー/51件目を拒否、50件まで許可。
- 実施方法：`node validation/atomic-counter.mjs`。
- 観測結果：8 tests passed。すべての期待値が通った。
- 限界：インメモリの逐次モデルであり、Postgres のトランザクション、RLS、ネットワーク、二ブラウザは実測していない。実装時にSQL統合試験が必要。
- 反映：design.md の `adjust_item` 契約、重複キー、負数・上限・権限規則。

### V2 要求・費用・境界の机上追跡

- 対象：R1〜R8、K1〜K6、最終文書版。
- 状態：合格（机上確認）。
- 方法：具体値「牛乳2」を主場面、同時更新、再送、第三者、0、同名、51件目に通し、design.md の横断表へ追跡。比較の0円は公式無料枠、16〜30h等は仮見積と区別して12か月式を再計算。
- 観測結果：各必須要求に画面・保存・処理・合格例があり、月額見込0円は上限1,000円以下。重要な追加判断は残らなかった。
- 限界：本人の操作感、実作業時間、実サービスは未検証。

## 調査の終了判断

比較を覆す問い（既製品が R2 を保証するか、自作の無料・非公開・原子的更新の経路があるか）には回答できた。専用 pantry アプリ全件の不存在は主張しない。Grocy は環境不適合、Sheets は即日次善案、自作は公式に成立経路がある。残る未知は外部登録後の実配備と本人利用でしか確かめられず、手順・逆転条件が定まったため公開調査を終了する。
