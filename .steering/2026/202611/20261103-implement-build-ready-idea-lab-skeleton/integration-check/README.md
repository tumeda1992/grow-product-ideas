# Cの一式試運転

## 検査する範囲

[論点100の採用済み計画](../implementation_review/implementation_review-96-100.md#決定論点100)に従い、新しい検査用の案件をgrow-product-ideaの受け入れから出口へ通す。各層と専門の本文を使って実際の依頼・返り・採否・差し戻しと正本を作り、次が具体の根拠と値を使えるかを区切りごとに検査する。[実行仕様](../design.md#cの一式試運転論点100)が、題材・進め方・各区切りの検査と受入れの正本である。

2026-11-17、**現在のCodex CloudでC1〜C3を受け入れから実際の出口まで通した**。C1は設計のbuild-ready、C2は非開発の部分案を選び「作らない」、C3は具体入力不足で正式な保留。入力と出口を先に対応付けず、各層・専門の依頼と返り、利用者役の採否、差し戻しと読み戻しを案件内に残した。全て検査用の自演で、実際の利用者の合意・実装・実利用の効果は未確認。新規文脈とClaude Codeの実起動も未確認で、論点100の全受け入れの合格とはしない。
作る版が実際に選ばれた場合、必要なラフ・規則・情報・機能と実装構成・技術の根拠、導入・訂正・復旧・受入れと裁量までを繋ぐ。非開発・保留も実際の検討から選び、出口を三種類へ揃えるための入力変更はしない。作る経路を通さなければ、その受入れ項目は未検査とする。
このCで確かめるのは判断と設計のレールである。製品本体の実装・導入・実利用の効果、77の家のPC／実APIの宿題、80と91の保留の解除、shared pluginの改稿は今回の結果へ混ぜない。

## 起動と環境の観測

### 準備時の起点と、固定入力

準備は2026-11-16（UTC）。比較元はfeature-16の`69c778ad6d00425536d46c95b51a57404da57220`で、論点101の17コミットをpushし、実リモートの先端との一致とcleanな作業treeを確認した後に開始した。その後のCの準備と完了記録の追記は未コミットである。

入力は[inputs.md](inputs.md)の版1。各件の体験・規則・動機・着想・制約と既知／未知は検討を始める前に保存した。初期版全体のSHA-256は`0e25896f9ad895862d2d82f37bb04b7d590fcd4bee4eaee7386c2e545c2f4fd4`。将来追記する場合は、この値を新しいfileのhashと偽らず、旧版として保持し、追加理由と影響する判断を残す。

### 入力と起動手順の準備時review

初期入力を、語り・規則・当時と後の評価・制約・未確認が分かれ、手段と出口を先に選んでいないかという観点で読み直した。C1の12枚の一意性と6手の出す／休む・補充を別に計算し、各手の手札・蓄え・得点が入力表と一致した。最後は手札B5／A6／B1、蓄え2、得点7で、12枚の保存も一致した。この整合確認は、入力の一回が自分の規則に矛盾しないことを確かめたものであり、C1の価値・候補・設計を検討した結果ではない。
20fileの版と、作業記録を含む相対link・anchor72件を照合した。C仕様のdesignは採用afterと全文一致した。READMEから実行仕様へのanchorは検査で一度不一致が出たため、実際の「Cの一式試運転（論点100）」へ修正して再検査した。新規二fileの空白検査とdiscussionの番号・親子・snapshotの比較も通った。

### 今回の観測と、まだ観測していないもの

| 対象 | 準備時に実際に得たこと | この事実だけでは言えないこと |
| --- | --- | --- |
| ローカルの候補環境 | Linux、x86_64。Python3.12.14、node v24.22.1、codex-cli 0.167.0-alpha.4 | 家のPCへの導入、最終候補の構成の成立、別時点の環境の不変 |
| Codex | 現在のassistantがAGENTSとgrow、記録の置き方、採用したC計画を明示的に読んだ | セッションを閉じてresumeした事実、全skillの自動読込み、新しい文脈からの一式の適用 |
| Claude Code | claudeはPATHに無い。9skillは`.claude/skills`経由で同じ本文へ届く | Claude Codeの実起動・自動読込み又は一式実行。別の場所でも利用不能という断定 |
| shared plugin | 実際に使用するtumeda-devのCodex／Claude manifestとmarketplaceの4宣言は8.2.5で一致。元作業のtemporary-overridesは無い | shared pluginを今回変更・再配布したこと、保留007を適用したこと |

次の表は、準備時に採取した実fileの版である。hashの取得を、本文を読み適用した確認へ置き換えない。適用の開始時に、使う本文を実際に読み、変わったものがあれば対象と理由を残す。designには今回採用済みのC仕様を適用しており、そのhashは比較元commitのdesignのhashと異なる。

| file | 準備時のSHA-256 |
| --- | --- |
| `AGENTS.md` | `f1dc30aa5043545341a52d42cdc71611fb0c81d3284849088a47be5f2686c7f6` |
| `README.md` | `3e9fa278fe3076785e23cbb5c1e2ce1574ce366f3fff2d0321de6759ce0250df` |
| `what-defines-a-product/README.md` | `35145dc148fcd216f8e6c41f36d1af3c3d4b6905278d7434167e52d512b92197` |
| `product-plans/README.md` | `b034c72f85d1e571c96742b5b89f480be0eed9ea40772cb6aa0bc107e5b3cd8f` |
| `what-defines-a-product/why-to-build.md` | `58985e652e9ac3b02165c4a21c92d1405c70901efd954f6cfd45b14c2a260f1a` |
| `what-defines-a-product/what-must-hold.md` | `70587af656de98a7b2e8e6c7f5aeea7efb0f3a3fe0c88af5150c468b5efef832` |
| `what-defines-a-product/how-to-solve.md` | `c74e992dbc841435992e86413cdfc7e3fc4edd2bebbe7dffc34993fe7a4c119c` |
| `what-defines-a-product/how-to-build.md` | `da6929e27c2078b7f842eafab682255f8235d88d55768a8733da5be9848e0f68` |
| `.agents/skills/design-core-logic/SKILL.md` | `f42b6a7d3d6ab8650d89bea5165a20438cb834995c3c7dd00e16cc1c98efd939` |
| `.agents/skills/design-data-model/SKILL.md` | `c43dda1e3279a92ca93271cb8ed070dda43be0d4e65e972bcf16be09c3f4e354` |
| `.agents/skills/functional-structure-design/SKILL.md` | `5167831d009ec68a21cef11eecf0b8a2feec48847ef8e6c7fc3de0a7f3db31b1` |
| `.agents/skills/gather-target-user-voices/SKILL.md` | `24b88321592bb3c77a0ca774a6dfeb05e29d7d72948d79f6931fa217d3e42b08` |
| `.agents/skills/grow-product-idea/SKILL.md` | `69533014dce297d7b6af17977f217178e4d216e9bdc1ad2e9502827ab5f751e2` |
| `.agents/skills/implementation-structure-design/SKILL.md` | `80635ce4d2957d9eceb49a0255e75ec8acab6285fb28ad0bd9bd60109e9fdd8c` |
| `.agents/skills/propose-alternatives/SKILL.md` | `6c2c99907e29c2bec4d04fd2b55e6d0379e768c1bb1e32710a3cf47120f43246` |
| `.agents/skills/sketch-experience/SKILL.md` | `736295490fc7f80c12d6dd2486f721c5ce36e1bc1b8ae2cd2565fbbad8d2a775` |
| `.agents/skills/verify-technical-feasibility/SKILL.md` | `9a5f8c4e885e3a6f5429d1fcbf7d8172ec59b5f08efb2e0b83f9a35277d86753` |
| `.agents/skills/grow-product-idea/templates/canonical.md` | `b9af65a442caa49577894b4aa9fda7b3bc005ceef2de916a65c9dfcecaddc959` |
| `.agents/skills/grow-product-idea/templates/layer-record.md` | `51a885f67d818ec8a611ce9b301d08e13119f04b8f58be5b88eba73ae63b73a3` |
| `.steering/2026/202611/20261103-implement-build-ready-idea-lab-skeleton/design.md` | `67dc9feedabca3befab4999e07b83b57355618aa14a077dce6328164c8ecc0de` |

100イテレーション1の採用に伴うdesignのSHA-256は`95bfd097bc4034cb4d4ed4b911a26f2cf7a20a62a40b807b2bc884e82d408091`。上表の準備時のhashは当時の観測として保持し、現在のdesignの値と混同しない。

### 採用後に実行した入口と順序（当初の手順を保持）

1. このfile、inputs.md、designのCの仕様と、100の現在状態を読む。初期入力の版と、100のイテレーション1で採用したCloudの起動条件を確認する。現在の実fileを明示的に読み、使った版と不足を記録してC1から始める。
2. AGENTS、root README、grow-product-idea、層の共通README、product-plansの配置と雛形を実際に読む。C1の受け入れ時に既存のname-work-directoryでslugを決める。案件をまだ作っていないことを確認し、この作業の直下の`product-plans/<slug>/`へ置く。
3. 入力にある元の言葉を受け入れ、案件内にも判断に必要な設定を残す。why-to-buildの本文を読み、体験・価値・アウトカムを探索・比較する。検査用の当人役の応答はその旨を明記し、元の入力に結ぶ。
4. 層を閉じた時と専門の返りごとに、依頼側が具体の値・根拠・未確認を照合して次へ渡す。必要になった専門の実fileをその時に読む。未確認を満たした扱いにせず、適用漏れなら該当出力を直して再検査し、方法の欠けなら実物を元のimplementation_reviewへ返す。
5. 選んだ実際の版を、必要な層と設計・引継ぎまで通す。案件内の読み切れを確認し、実際の出口と摩擦・残る経路を記録する。その後C2、C3も同じ入口から進める。

上の手順は、毎回全専門を呼び出す固定のチェックリストではない。必要な判断と不足から呼び、局所で成立した成果を次が実際に使えたかを残す。準備時の記憶から成果を先に完成させ、後で層の記録を付ける進め方にはしない。

## 各件の入口と結果

| 件 | 案件内の成果 | 実際の到達点と未完 |
| --- | --- | --- |
| C1 | [六手の蓄え](../product-plans/20261117-explore-card-game-rule-changes/README.md) | **build-ready**。価値/五条件/版を選び、比較ラフを全commandと状態へ育て、規則・情報・責務・構成・保存境界の根拠、導入/訂正/復旧/受入れを揃えた。製品実装/導入と楽しみ・時間の実測は未完 |
| C2 | [二人の夕食](../product-plans/20261117-choose-weekday-dinners-together/README.md) | **作らない**。共同候補と変更希望から相談を再開する非開発の部分案。現物・購入前確定・実際の引受け/食事・残りの日跨ぎは全体の未達として残す。2週の実利用実験は未実施 |
| C3 | [替芯](../product-plans/20261117-find-compatible-pen-refills/README.md) | **保留**。商品品番/互換原資料とK1/K2の実store対応が無く、how-to-solveの出どころ確認で停止。層を閉じず、API/回答/価格/納期を作らない。提供されたら同じ停止点から再開 |

三件のwhyでは最初の症状から別の価値へ広げ、反証と失う良さ・負担を比べて姿へ畳んだ。C1は計算の速さから自分の次の問い、C2は献立の固定から共同の選択と自由、C3は一覧の便利さから互換と期限内入手の道へ。作る楽しみの設定はC1だけで、各件のwhyと手段選定を混同しなかった。
初期入力は版1のまま、SHA-256も変わらず。ケース内のinput.mdは各節を全文保持し、外の入力を読まなくても判断を辿れる。C3で当人役が包装の内容を追加することもしていない。

### 実際に使った方法と、依頼側が使った返り

| 方法 | 今回の具体の仕事と、次で使われた結果 |
| --- | --- |
| grow-product-ideaと四層 | 三件の受入れ/why/what/候補比較/採否と出口。C1は四層、C2は作る部分が無いので三層、C3はwhy/whatまで閉じ候補比較で保留。層を通すための架空の根拠を足さない |
| propose-alternatives | 現状/普段の道具/漸進を含む探索、強い非開発と独立の部分案、同じ期間の費用・部品別三点と八軸。C1は詳細の増分を受け再見積り、C2は部分案の失う価値、C3は全体費用が出せない不足まで返した |
| sketch-experience | C1の紙/表計算/自作の比較から、親nodeを明示する全操作のCLIラフ、無効/中断/訂正/故障まで育てた。C2は火曜/水曜を実際に記せる文字ラフへ通し、希望と了承を分けた |
| design-core-logic | C1の入力と判定順、V0元/別初手/V1の六手、無効/6手目補充/上限/終了を具体化。7点同点でも蓄え2対5になることを比較の表示へ使った |
| design-data-model | C1の必要な読書きからsnapshotと行いの木を比較し、不変root/親node/見込みと追記、具体JSON・型/制約と失敗を返す。同じn0→n1/b1を表示と処理に渡す |
| functional-structure-design | C1の巨大command/独立した規則/共通遷移と調整を比較。A3の入力→0/3/手札の結果→node追記→保存後の表示、蓄え不足なら書込まない受渡しを設計へ使った |
| implementation-structure-design | C1の同期/常駐、固定lock、最新読取り/検証/全量切替/成功、停止/競合/破損退避を同じnodeへ照合。導入・訂正・復旧の費用増分を選定へ返した |
| verify-technical-feasibility | C1は期待と対照を先に保存し、現Linux/Pythonで6件を実行。C3は実targetが無いので入口で未検査と返した。toy APIで代替しなかった |
| facilitate-discussion | 各層の採否/閉じ/出口を先に提案保存し、別に検査用の役の応答・根拠を保存。C1の費用差も新しい採否へ返した。公開判断と内部過程を分け、番号/所属を検査 |

実行時にAGENTS、grow/雛形、層/配置、呼んだ専門とsharedの実fileを読んだ。上の準備版20fileは、100イテレーション1のdesign以外は同一hashのまま使用した。sharedは8.2.5、元作業の暫定指示無し。hashは読取りや適用の代わりの証拠ではなく、具体の適用は各件の記録/材料/採否にある。
gather-target-user-voicesは今回呼んでいない。C1は規則と本人の設定、C2は両者の語りから生活上の小実験を選ぶ範囲、C3は本人しか持たない商品/店対応の不足であり、他者の公表体験を集めてもその事実を取得できない。必要な方法の呼出しと、全専門を機械的に使うことを分けた。

## 継ぎ目の摩擦

| 原事例と使った方法 | 実際の差・途中で補った判断 | 対処と再検査／保守へ残す所 |
| --- | --- | --- |
| C1 比較のラフ→logic/情報→詳細の表示 | 元も別初手もV1も7点で、点だけでは試した差が消える。V1の途中切替は元の根拠を壊す | 蓄え/手札/経過/当時の理由を比較に含め、V1は別rootから開始。三つのtraceと同じnodeを各専門/層へ照合。版の範囲は不変 |
| C1 構成→費用→閉じた選定 | 導入/参照検証/訂正/復旧/受入れの具体化で三点130/250/470分から165/310/570分へ増加。上限6時間を超えるリスクが大きくなる | [再選定](../product-plans/20261117-explore-card-game-rule-changes/how-to-solve/discussion.md#決定論点3)で開け直し、同じ範囲と6時間停止/紙へ復帰を再採用。旧値を消さず通知し、下の設計を再開した |
| C2 非開発の部分改善→出口 | 候補の共有を実際の在庫/了承/食事へ読み替えると薄い改善が全体を満たすことになる | Pの独立の改善とW2の残り/W3/W4/W5の全体未達・残る重複購入と相談を分け、C2/D2役が採否。手順のラフに火曜/水曜/連絡不能を当て、実利用の未知を保持 |
| C3 本人の具体入力→候補/技術の入口 | 包装は家にある設定でも内容が無く、K1/K2を実storeへ対応させられない。対象のない技術検査は意味を持たない | 未検査/比較未完として保留し、必要な品番/原資料/店又はURLを復活条件へ。入力追加0、外部連絡/購入0、技術実行0。保留の具体化は既存方法の範囲 |
| 三件のwhatの適用→読み戻し | 生成表に条件違反の例が混ざり、「全条件真の反例」と一括で数える自己評価が粗かった | 各whatの末尾で採用後の条件群を固定し、全言い分×四方向を再生成/判定。偽/未確認なら全真反例に数えず、真でも外の事情で未達となる限界を分けた。条件と採否は変わらず後続も確かめ直した。本文に既に全真の指示があり、現在の根拠では適用漏れ。共通方法の欠けと断定しない |
| 記録の実行補助→案件内の読み切れ | 公開contextの相対linkを内部記録へ写した時に基準directoryを変えていなかった。持ち出し検査で25件失敗 | 内部記録の引用先だけを一階層上へ直し、過去の採否/入力/本文は不変。三件を別directoryへコピーして相対link/anchor232件、13discussionの22論点を再検査し0問題。sharedの改稿はしていない |
| C3 受入れ入力の出典分類 | 設定の地の文を本人の逐語発言のようにquoteしていた | 正本で地の文/元の着想へ分類し直し、本人の追加発言としない。初期input全文とhashは保持。適用上の訂正として内部記録にも保存 |

保守側の受付は[論点100の内部記録](../internal-records/implementation_review.md.topic-100.md#iteration-1-record-6)に置く。元の入力・方法の版・実物・対処・未処理を対応付けて引き渡した。今回は案件の適用と記録の修正で対処し、共通の方法やshared pluginを追加改稿していない。適用漏れを既存のcontent_density未読だけで説明することもせず、読んだ後の返りが指定の前提を実際に保つかを検査する必要が残る。

### 検査結果と、証拠の射程

- 保存のprocess境界: 期待を実行前に置いた[probeと結果](../product-plans/20261117-explore-card-game-rule-changes/materials/technical-feasibility/README.md)6件が期待通り。通常/切替前停止/切替後停止/直接上書きの破損対照/lock保持中拒否/解放後取得。電源断・任意OS/remoteFS・本製品の正しさは保証しない。
- 案件内だけでの読取り: ケースごと別directoryへ写し、相対file/anchor232件が存在し案件外へ出ないことを確認。コピー先でsharedのdiscussion検査13集合・22論点、応答待ち無し。これだけで意味の成立を保証せず、上の同じ値の受渡しと全真の再照合を別に行った。
- 条件・費用・採否: C1の3traceと6手目の補充、費用の旧/増分/新の和、C2の未達の文言と両者役の採否、C3の止めた根拠/入力未追加を照合した。
- 入力: 全体SHA-256と各件inputの本文一致。実行で読んだレール20版のうち差は採用済みdesignのみ。新規文脈やclient自動読込みの実行証拠ではない。

## 残りと再開

現Codex Cloudの同じ文脈でのC1〜C3は出口まで通した。次に未確認なのは、新しい文脈から文書だけで適用できるか、Claude Codeを実起動して読込み・一式実行できるか。この場の再読・symlinkの一致だけでは合格にしない。実行可能な方法/環境が確定してから別に検査する。論点100の全受け入れを完了扱いにはしない。
製品本体の実装/導入と実利用の効果、77の家のPC/実APIの宿題、80/91の保留の解除、shared pluginの保守は今回未実施。三件は検査用の採否であり利用者本人のプロダクト選択ではない。Cの成果は未コミットで、既にpush済みの17コミットを今回の変更へ置き換えていない。
