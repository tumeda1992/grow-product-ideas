# 今回の到達点の設計

対象の到達点：proposal.md「到達点」の運用しながら改善できる線。条件付き部分：出口を止めるものなし。U1 は配備入力、U2 は運用観測。

## 体験と画面・入出力

### 画面

1. `/login`：メール、パスワード、ログイン。signup/パスワード再設定リンクは初版では表示しない。失敗は同じ一般メッセージにし、アカウント存在を漏らさない。
2. `/` 在庫一覧：ヘッダーに世帯名、同期状態、ログアウト。各行は `品名 | − | 個数 | ＋ | …`。名前で絞込、`品目追加`。読込中、空、通信エラーを別表示する。
3. 行の `…`：数値直接訂正、改名、アーカイブ。破壊操作は確認する。
4. `/history`：時刻、品名、操作者表示名、`+1/-1/訂正/追加/改名/アーカイブ` の直近100件。監査と誤操作回復用で、高度な検索は非目標。

テキストワイヤー：

```text
冷蔵庫                         同期済み
[品名で絞る____________] [追加]
牛乳                 [−]  2  [＋] [⋯]
卵                   [−]  6  [＋] [⋯]
[履歴]                        [ログアウト]
```

主場面：A が牛乳2の `−` を押す。ボタンをそのリクエスト中だけ無効化し「更新中」。RPC成功値1で行を更新し「同期済み」。B は Realtime 変更通知で再取得し、通知を逃しても画面focus時・操作後に再取得する。Realtime は便宜であり正しさの根拠にしない。失敗時は表示値を確定変更せず「反映できませんでした。再試行」を出す。同じ再試行は同じ request_id を使う。

直接訂正は現在値と `version` を送り、合わなければ更新せず「他の更新があります。最新値を確認してやり直す」。通常の増減は古い表示でも delta のため有効。オフラインは閲覧中の値に「未同期」を示し、書込キューを作らない。

## データと生涯

| 表 | 主な列・制約 | 生涯・所有 |
| --- | --- | --- |
| `households` | `id uuid PK`, `name text` | 管理者が導入時に1件作成 |
| `memberships` | `(household_id,user_id) PK`, `display_name`, `role owner/member` | 二人だけ。owner が追加・削除。初版UIでは変更不可 |
| `items` | `id uuid PK`, `household_id FK`, `name varchar(40)`, `count smallint check 0..999`, `version bigint`, `archived_at`, timestamps | membership の世帯所有。active は最大50。同一世帯の active な `lower(btrim(name))` を一意にする。アーカイブは一覧から除外、履歴は残す |
| `inventory_events` | `id uuid PK=request_id`, `household_id`, `item_id`, `actor_id`, `kind`, `delta nullable`, `before_count`, `after_count`, `created_at` | 各成功変更と同transactionで追記。通常UIは直近100件。世帯削除時に全削除 |

公開 schema の全表で RLS を有効化し、`anon` の全権限を revoke。`authenticated` は一覧に必要な select のみを表へ grant。書込は許可 RPC の execute のみに絞る。全 read/write は `memberships` に `auth.uid()` が存在する世帯だけ。membership を読む各 policy が自身を再帰参照しないよう、`private.user_household_ids()` を `security definer`、空の `search_path`、固定の完全修飾名で作り、PUBLIC の execute を revoke して authenticated のみに grantする。mutation RPC も固定 `search_path`、完全修飾名、明示的な execute grant とし、関数内部で `auth.uid()` と membership を再検査する。クライアントに service-role key を置かない。

品目追加は transaction 内で membership、active件数 `<50`、同名なし、初期 count 0..999 を検査。アーカイブ済み同名は自動復元せず「復元または別名」を選ばせる。世帯離脱は今回UI外。管理者手順で membership を外した瞬間からRLSでアクセス不可。最後のowner削除は拒否。

## 心臓部ロジックとモジュール

### `adjust_item(p_item_id uuid, p_delta smallint, p_request_id uuid)`

- 認証必須、delta は `-1` または `+1` のみ。
- transaction 内で item を `FOR UPDATE`、呼出者の membership、非archiveを確認。
- 同じ `request_id` の event が既にあれば、同じ actor/item/delta なら保存済み `after_count` を返す。不一致なら `REQUEST_ID_CONFLICT`。
- `new_count=current+delta` が0..999外なら `COUNT_OUT_OF_RANGE`、変更なし。
- item の count と version+1を更新し、event を追記して `{item_id,count,version,event_id}` を返す。イベント追記と更新の片方だけ成功する状態を作らない。

### その他の公開操作

- `create_item(name, initial_count, request_id)`：member、50件、正規化同名、範囲を一transactionで検査。
- `set_item_count(item_id, expected_version, new_count, request_id)`：訂正専用。version 不一致は `STALE_VERSION`。
- `rename_item(item_id, expected_version, name, request_id)`：同名・長さ・version を検査。
- `archive_item(item_id, expected_version, request_id)`：履歴を残して非表示。
- 各 mutation は共通エラーコードを返し、UI は `UNAUTHENTICATED/FORBIDDEN/NOT_FOUND/STALE_VERSION/LIMIT_REACHED/DUPLICATE_NAME/COUNT_OUT_OF_RANGE/NETWORK` を日本語表示する。

UI モジュールは AuthSession、InventoryRepository（Supabase呼出）、InventoryList、ItemEditor、History に分ける。コンポーネントはDBへ直接 update/insertせず Repository のRPCだけを使う。

## 技術と運用

- TypeScript + Vite のレスポンシブ静的Web、Supabase JS client。PWA/offline cache は初版外。
- Supabase Auth は email/password。管理者が U1 の二人を作成後、公開 signup を無効化。短い初期パスワードを配らず、十分なランダム値を安全な経路で本人へ渡し初回変更する。メール送信機能には依存しない。
- Supabase Postgres/RLS/RPC が状態と正しさを所有。Cloudflare Pages は build済み静的ファイルのみ直接 upload。環境変数には公開可能な project URL と anon/publishable key のみ。
- 検知：mutation error をその場に表示。無料枠休止メールと請求画面をownerが月1回確認。休止時はDashboardでResumeし、再ログイン・一覧・増減を確認。
- バックアップ：週試用開始前と終了後、その後継続なら月1回 `items` と `inventory_events` をCSV exportし、世帯ownerの暗号化された私的保管先へ置く。復旧は新projectへ schema migration、二人を再作成、household/membership/itemsを取り込む。event は監査用で、復旧優先は items。
- 費用ガード：有料plan/独自ドメイン/add-on/従量課金を有効化しない。価格再確認で月1,000円超なら停止して相談。

## 権限・状態表

| 主体 | 一覧/read | 増減・訂正 | 品目追加/改名/archive | membership管理 |
| --- | --- | --- | --- | --- |
| 未認証 | 拒否 | 拒否 | 拒否 | 拒否 |
| 認証済み非member | 0件/拒否 | 拒否 | 拒否 | 拒否 |
| member | 自世帯のみ | 自世帯のみ | 自世帯のみ | 拒否 |
| owner | 自世帯のみ | 自世帯のみ | 自世帯のみ | 管理手順のみ可、最後のowner削除不可 |

## 横断して確認する例

| 要求/リスク | 操作・失敗場面 | 入出力 | データの前後 | 処理 | 期待結果 |
| --- | --- | --- | --- | --- | --- |
| R1 | Aが牛乳を使用 | 一覧 `−` | 2→1、event追加 | adjust_item | B再取得で1 |
| R2/K1 | A `-1`、古い画面のB `+1` | delta 2件 | 2→1→2 | row lock + transaction | 最終2、event 2件 |
| K2 | Aの応答消失、再試行 | 同じrequest_id | 2→1→1 | idempotency | 二重減算なし |
| R3/K3 | 第三者がURL/APIへ | sessionなし/非member | 変更なし | grants+RLS+RPC membership | 0件または拒否 |
| R4/K4 | 0で`−`、51件目 | RPC | 変更なし | check/件数lock | 明示エラー |
| R5/K5 | 誤って`−` | 直後に`+`または訂正 | eventを残し復元 | adjust/set | 元の数へ回復 |
| R6 | 無料枠変更 | 配備前料金確認 | 課金なし | 手動gate | 上限超なら配備停止 |

V1 は検討用モデル、V2 は机上確認。SQL、RLS、ブラウザ統合は未実行なので handoff の配備前テストで再確認する。仕様変更時は API 契約、RLS、上記全行、V1相当テストを再実行する。

## 実装者の裁量と許容する負債

裁量：色、余白、アイコン、UIライブラリ、内部関数分割、Realtime利用の有無（focus/操作後再取得は必須）、テストframework。相談が必要：DB表・API契約、認証方式、通常操作を絶対値更新へ変える、offline書込、外部サービス追加、月額発生、履歴削除方針。

許容負債：手動CSV、休止時Resume、初版の管理UIなし、直近100件だけの履歴UI。個数とeventはDBに保持するためUI改善可能。休止や復旧負担が月1回超、データ消失、第三者提供へ拡大したら見直す。
