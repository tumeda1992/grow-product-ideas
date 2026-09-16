# shared-fridge-counter 実装引き継ぎの独立受取評価

## 判定

**現状のままでは、会話補足なしの完全な実装引き継ぎにはしない。状態は `育成中` へ戻すのが妥当。**

主要な商品判断、画面、表、権限境界、原子的な `±1`、上限、実装順、実DBでの停止条件は十分具体的であり、ローカル実装の大半には着手できる。しかし、全mutationが受ける `request_id` の再送契約が `adjust_item` 以外で未定義で、実装者がネットワーク失敗後の公開挙動を決める必要がある。さらに履歴を「監査と誤操作回復」に使う一方、改名前後の名称を保持する仕様・列がない。どちらも単なるframework内部詳細ではなく、API契約または保存形式に関わる。

外部アカウント登録、配備、実メール決定、一週間利用が未実施であること自体は、この判定理由ではない。それらは権限を得た後の実装・導入・運用gateとして適切に分離されている。

## 対象と方法

- 最初に `/private/tmp/grow-ideas-eval.TNCj6E/shared/` 直下の `README.md`、`proposal.md`、`design.md`、`evidence.md`、`decisions.md`、`handoff.md`、`review.md` だけを読んだ。過去会話・他評価は読んでいない。
- 主場面と危険場面について、要求 → UI → RPC → transaction/RLS → items/events → 応答・回復を実装者の視点で追った。
- 文書評価後にだけ `validation/atomic-counter.mjs` を読み、実行した。
- 外部サービスへの登録、課金、公開は行っていない。

## 追加判断の分類

### 既に仕様に書いてある

| 判断 | 根拠 |
| --- | --- |
| 二人・一世帯・active最大50、品名と0..999の整数個数 | `proposal.md:19-25,30-35`、`design.md:30-35` |
| 通常更新は絶対値でなく `delta=±1`、item row lock、同transactionでevent追記 | `design.md:43-49`、`decisions.md:23-30` |
| 直接訂正・改名・archiveはversion競合を拒否 | `design.md:26,53-56` |
| 未認証・非member・別世帯をRLS/grants/RPCで拒否し、service-role keyをブラウザへ置かない | `design.md:37,70-77` |
| membership policyの再帰をsecurity-definer helperで避け、権限とsearch_pathを固定 | `design.md:37` |
| UIの失敗、未同期、focus/操作後再取得。offline書込キューは作らない | `design.md:24-26` |
| 実Postgresの並行更新、RLS、二ブラウザ、復元は実装・配備gateで検査する | `handoff.md:15-21` |
| 月1,000円超や有料機能は自動承認せず停止 | `proposal.md:24,55,71`、`design.md:68` |

### 安く変えられる裁量・普通の実装作業

| 項目 | 判定理由 |
| --- | --- |
| React等のUI framework、部品分割、色・余白・アイコン、テストframework | 明示的な裁量（`design.md:93-95`、`handoff.md:25`）。 |
| Realtimeを使うか、focus/操作後の再取得だけにするか | Realtimeは正しさの根拠ではなく、再取得が必須と確定（`design.md:24,95`）。 |
| 51件目を競合時にも防ぐためhousehold row lock、advisory lock、serializable等のどれを使うか | 「transaction内でactive件数を検査」「件数lock」「51件目拒否」という不変条件と実DB試験が確定（`design.md:39,87`、`handoff.md:17`）。手段選択は実装作業。ただしロックなしの単純countは仕様不適合。 |
| SQLSTATE/例外を共通エラーコードへ写像する内部方法 | UIへ返す意味は確定（`design.md:57`）。実装方式は局所的。 |
| U1の実メール、project ID、秘密情報の投入 | 配備時入力でありコード・データモデルを変えない（`README.md:24-27`、`handoff.md:25-27`）。 |
| 実Supabase/Cloudflareでテストを実施し、失敗なら停止すること | 未決仕様ではなく実装の合格gate（`handoff.md:15-20`）。 |

### 重要な未決・仕様穴

#### I1 `adjust_item` 以外の再送/idempotency契約がない

- 根拠：`create_item`、`set_item_count`、`rename_item`、`archive_item` はすべて `request_id` を受ける（`design.md:51-56`）が、同一IDの再送時に保存済み成功を返すのか、引数一致を何で判定するのか、不一致を `REQUEST_ID_CONFLICT` にするのかは `adjust_item` にしか書かれていない（`design.md:43-49`）。`inventory_events.id` はrequest_idそのもの（`design.md:35`）。
- 必要入力：各mutationについて、同じactor・operation・対象・引数の再送結果、不一致再利用の結果、初回commit後に応答が消えた場合のUI表示を決める。
- 影響：実装者によって「成功結果を再返却」「一意制約エラー」「DUPLICATE_NAME/STALE_VERSION」「再実行」が分かれ、通信失敗後の回復体験とevent整合性が変わる。API公開契約なので裁量扱いできない。

#### I2 改名履歴を監査・回復に使うための保存内容がない

- 根拠：履歴は「監査と誤操作回復用」で改名eventも表示する（`design.md:12`）が、`inventory_events` には名称snapshot、before_name、after_name、metadataがない（`design.md:35`）。現在の`items.name`とのjoinでは、改名前の名称を復元できない。
- 必要入力：改名eventが現在名とkindだけで十分なのか、before/after名を保持・表示するのかを確定する。後者ならevent schemaと履歴表示・CSV/復元を更新する。
- 影響：保存形式、履歴の意味、誤改名からの回復方法が変わる。今回の到達点に履歴と改名を含めた以上、実装者が独自決定すべきではない。

## モデル試験が示したこと／示していないこと

### 実際に示したこと

`node validation/atomic-counter.mjs` は実行され、8テストが合格した。インメモリ状態機械の**逐次実行**として、次を示した。

- 初期2にAの`-1`、続いて古い表示を想定したBの`+1`を適用すると最終2になる。
- adjustの同一request_id・同一引数再送は二重反映せず、異なる引数での再利用を拒否できる。
- 0からの減算、非memberのadjust、逐次51件目作成を拒否できる。
- 2件のadjust eventを保持できる。

これは、選んだ更新契約が具体例上で矛盾しないことを示す設計用モデルとして有効である。

### 示していないこと

- 実Postgresの並行transaction、row lock、isolation、deadlock、rollback、eventとの原子性。
- 実SupabaseのAuth、grants、RLS、security-definer helper、search_path、別世帯read、未認証read。モデルの非member試験はmutationメソッド内のSet確認だけで、RLS侵入試験ではない。
- 50件上限の**並行作成**。モデルは逐次50/51件目だけであり、DB側の件数ロックを検証しない。
- 品名trim/case-insensitive、一意制約、archive後同名、訂正・改名・archive、version競合、履歴100件、CSV復元。
- ネットワーク応答消失、ブラウザ再送、Realtime/focus再取得、UI表示。
- `create_item` 等、adjust以外のrequest_id再送契約。

文書自身も `evidence.md:65` と `design.md:91` で主要な限界を明記し、実DB試験をhandoffへ残している。この分離は正しい。一方、`evidence.md:59-64` がV1の対象をK1〜K4全体とし、`proposal.md:77-80` が同名等をV1合格のように参照するのは範囲が広すぎる。現物は同名を扱っていない。また `proposal.md:77-80` の `E6/V1` は、E6がCloudflare Pages資料でK1〜K4の根拠ではない。これは根拠リンクの不整合であり、モデルの合格範囲を増やさない。

## 実装先へ残したテストの評価

実DB・配備環境へ残したこと自体は不備ではない。`handoff.md:15-20` は、入力、期待結果、停止条件を持ち、以下を正しく実装gateとしている。

- 実Postgres並行RPCで最終count=2/event=2、再送event=1、underflow拒否。
- RLS再帰エラー、未認証・非member、直API、ログアウト後の拒否。
- 50/51、同名、archive後同名、STALE_VERSION、通信失敗、履歴。
- 配備後の独立2ブラウザ、focus再取得、CSV export/復元リハーサル。

ただしI1/I2は、テストを書けば決まる事項ではない。期待値・保存内容そのものが未確定なので、実装前に設計へ戻す必要がある。反対に、並行ロックやRLS SQLの具体実装とその試験は、確定済み不変条件を満たす普通の実装作業であり、重要な仕様穴とは扱わない。

## その他の指摘

### 今回の範囲で修正できる不整合

- `proposal.md:77-80` のK1〜K4結果参照は `E6/V1` だが、E6はCloudflare Pagesであり当該リスクを裏付けない。V1も同名・RLS・実並行を検証していない。結果欄を「モデルで確認した範囲」と「実装gate」へ分ける必要がある。
- `design.md:57` のUI共通エラー一覧に、`adjust_item` が返しうる `REQUEST_ID_CONFLICT`（`design.md:47`）がない。I1の共通契約を決めた後、UI挙動を加える必要がある。
- `review.md:23` はREADMEの誤参照を修正済みとしているが、proposalの同種参照は残っている。最終レビューの「重要な未解消なし」は再判定が必要。

### 許容できる限界

- U2/H1/H2の一週間利用は、本人の現実利用でしか分からず、失敗時の縮小条件がある。小さく作った後の運用観測として妥当。
- 無料枠・休止・価格は変動するため、配備直前の公式再確認をgateにしたのは妥当。今回Webで公式ページの内容抽出を取得できなかったため、2026-09-14時点の料金を独立再保証はしていない。
- 実メールは本人しか提供できない配備入力で、設計の重要未決ではない。

## 実行した確認と限界

- 7文書を行番号付きで読解し、主場面、再送、第三者、0/51件目、改名、離脱、復旧を横断追跡した。
- 設計評価後に `node validation/atomic-counter.mjs` を実行：8/8合格。
- `review.md:3` の対象6ファイルについてSHA-1を照合し、proposal/design/handoff/evidence/decisions/validationの全てが一致した。READMEとreview自身は同欄の固定対象外。
- 製品コード、SQL migration、ブラウザUIは実装・実行していない。Supabase/Cloudflareのアカウント登録、配備、RLS侵入試験、復元、本人利用もしていない。

## 引き渡し条件

I1とI2を設計・handoff・契約テストへ反映し、V1の結果参照を現物の検証範囲へ狭めた後に再レビューする。それまでもschema/RLSの骨格や最小UIの準備は可能だが、全mutationと履歴を含む完成実装へ「追加の商品判断なし」で渡せる状態ではない。
