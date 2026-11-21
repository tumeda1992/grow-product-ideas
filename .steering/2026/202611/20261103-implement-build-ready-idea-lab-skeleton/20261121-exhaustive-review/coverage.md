# レビューの範囲・証拠・限界

`scope=full` は、利用者がアイデアを渡してから判断記録を持ち出すまでの現行レール全体を指す。履歴の前回結論を合格の出発点に置かず、指示の順序、実際に引き渡す対象、次の担当が得られる根拠から読み直した。実行担当は指定された gpt-6.2-astra（xhigh）。開始時のbranchは feature-16、HEADは `4b8dc31c0e8242bcda6fd2a2746b25e997b23243`、追跡中の内容に変更なし。Gitの455パスは通常file 453、symlink 2。開始時の本文hashは通常fileとCLAUDE.mdのリンク先を含む454パスを固定し、リンクの型・宛先は別に照合した。[依頼と例外](evidence/request.json)・[内容一覧](evidence/snapshot.json)・[リンクの固定](evidence/snapshot-symlinks.json)

## 確認した現行ファイル

| 実物 | 照合した入口・出口 |
| --- | --- |
| [README.md](../../../../../README.md)、[AGENTS.md](../../../../../AGENTS.md)、CLAUDE.md／.claude/skillsのリンク | 依頼方法、build_policy、質問・出口、初回構築への持出し、案件から保守への返却。Git modeと両クライアントの参照先も確認 |
| [what-defines-a-product/README.md](../../../../../what-defines-a-product/README.md) | 四層の順、閉じ待ち・再判断、open／require-build、専門への一方向の依頼・変更通知、作業の操作を制限する指示の作用先 |
| [why-to-build.md](../../../../../what-defines-a-product/why-to-build.md) | 体験理解・発散・目標収束の往復、人ごとの望み、外す価値、目標／大きさ／測り。既知の価値と未知の手段が相互に依存する枝 |
| [what-must-hold.md](../../../../../what-defines-a-product/what-must-hold.md) | 全条件真の反例と条件違反の区別、条件の由来、必要性と十分性、判定の異なる手段、最低線、whyへの差し戻し |
| [how-to-solve.md](../../../../../what-defines-a-product/how-to-solve.md) | 現状・直接見る基準・候補を分けた差分、部分改善・負担と未知、8軸、採用可能な作る部分、個別の組と版全体の比較 |
| [how-to-build.md](../../../../../what-defines-a-product/how-to-build.md) | 必須の裏づけと実利用で知る未知、具体入力から利用者の次の行い、専門間の一致、導入・修正・結果不明からの復旧、委ねる裁量と上位へ戻す差 |
| [product-plans/README.md](../../../../../product-plans/README.md)、[grow-product-idea](../../../../../.agents/skills/grow-product-idea/SKILL.md) | 受付、再開、slug、採否と記録、どこを正本とするか、差し戻し、参照の保存・検査、保留と持出し |
| [canonical.md](../../../../../.agents/skills/grow-product-idea/templates/canonical.md)、[layer-record.md](../../../../../.agents/skills/grow-product-idea/templates/layer-record.md)、[check-plan-links.py](../../../../../.agents/skills/grow-product-idea/scripts/check-plan-links.py) | 受付時と採用後で書ける節、提案時に既に必要な参照、Markdownの解析と失敗時の返り。実物の雛形から参照を展開して実行 |
| [gather-target-user-voices](../../../../../.agents/skills/gather-target-user-voices/SKILL.md)、[propose-alternatives](../../../../../.agents/skills/propose-alternatives/SKILL.md) | 契機が十分な体験、発言と観測、根拠未取得の返し。原状／基準からの増分、部分案と対案を区別する規則、全体費用と局所の選択 |
| [sketch-experience](../../../../../.agents/skills/sketch-experience/SKILL.md)、[design-core-logic](../../../../../.agents/skills/design-core-logic/SKILL.md) | 代表入力・ラフ・人の行い、規則の境界と反例を通す仕事。価値の採用・技術の実証を他担当へ渡す境界 |
| [design-data-model](../../../../../.agents/skills/design-data-model/SKILL.md)、[functional-structure-design](../../../../../.agents/skills/functional-structure-design/SKILL.md) | 詳細粒度の入出力。情報・現行・履歴・参照、機能の責任・失敗・変更。必要な入力が無いまま図や表で閉じることを禁ずる規定 |
| [implementation-structure-design](../../../../../.agents/skills/implementation-structure-design/SKILL.md)、[verify-technical-feasibility](../../../../../.agents/skills/verify-technical-feasibility/SKILL.md) | 外部の結果不明・競合・再試行を扱う構成、事前の期待と実行条件、費用へ返す差。未検査の返答が技術の成立を保証しないこと |

この9件の現役skillはレビュー**対象**として読んだ。企画を進行するために9件を起動したという意味はない。手続きとして使ったのはshared 8.2.5のexhaustive-review（対象固定・複数パス・根拠・独立した指摘）、think-through（事象と原因の切分け、別領域の反例）、document-review（成果物を採否判断に使えるかの読戻し）。findingの雛形とhigh-reasoning-reviewのモデル選択規則も照合した。元作業・出力先共に作業限定の上書きは無いとの起動時確認を用いた。

## パスごとの確認

| パス | 検査と、その結果 |
| --- | --- |
| 入口から正方向 | 原文保存 → 価値仮説 → 目標 → 条件 → 候補／版 → 設計 → 出口。条件を足すための相談、専門の根拠返却、使用禁止の操作や未確認を区別する規定は実在。原文の中で一度も候補化されなかった約束、条件付きの目標はこの方向だけでは検出しにくい |
| 反例から逆方向 | 価値あり・手間は増える案、全条件真で結果だけ崩れる案、一条件だけ偽でも価値が成立する案、各400円を組むと600円制約を越える版を検査。どの段が判断を持つか、専門の既存の救済が使えるかを再読した |
| 状態と書込みの順序 | 新規と再開、未閉じ保留、閉じ直し後の差あり／差なし、非開発の出口、採否前／後の正本の節、材料が単一fileからdirectoryへ育つ時の既存参照を確認。後者には移動時の参照更新と履歴保持が既にある |
| 選定・構築の受け手 | 指定C3の16ファイルで、実行したか・採用したか・必要な根拠を取得できたかを分けた。build-readyを称した別の初回C1からは設計の入口と実装後の受入れの一件を読み直した。再ドライランのC3は同名の実績として合算していない |
| 再反証・重複整理 | 「whyは一切発散できない」「全専門を常に呼ぶ」「一例の失敗は全案件で必ず失敗」「どの事実照会もwhyでは禁止」を退けた。閉じの順序を直しても案件識別の衝突は残るように、独立して確認・採否できる原因ごとに指摘を分けた |

## 替芯の案件で確認したこと

指定は初回の `20261117-find-compatible-pen-refills`。試運転用の当人と応答は自演で、実際の人の行動・採用・入手実績は観測されていない。同日の `20261117-check-refill-availability` は後の `require-build` 条件で行った別の試行。[初回の正本](../product-plans/20261117-find-compatible-pen-refills/README.md)・[別の再実行の正本](../product-plans/20261117-check-refill-availability/README.md)

| 時点 | 当時の根拠と判定 |
| --- | --- |
| 入力 | K1で見つからず、K2で似た商品を見たが買わずに帰った。35分は移動と棚探しの合計設定。本人は空振りを減らしたい。K1/K2に実店との対応はなく、家にある包装の内容も未提供。架空の在庫や店の回答を足さない条件がある。[input.md 11–32行](../product-plans/20261117-find-compatible-pen-refills/input.md) |
| why | 全店の在庫一覧H1、期限・互換から入手の道を選ぶH2、店巡りを楽しむH3を比べ、利用者役はH2を採用。実際の入手・ペンに使えたか、寄り道時間は測りに残る。一方「得る期限を優先して二店回る」「寄り道を避けて今回は買わない」で評価が逆転する点は選んでいない。H1は道具を含み、H3はもとの語りで既に弱い。その採用記録を、元の望みを十分に発散して本人が選んだ実証に使えない。[why記録 19–41行](../product-plans/20261117-find-compatible-pen-refills/why-to-build/README.md)・[採否 13–37行](../product-plans/20261117-find-compatible-pen-refills/why-to-build/discussion.md) |
| what | W1〜W4は同一性・在庫と時点・期限・失敗後の行いを扱う。具体SKU不明でも「色と太さだけでは互換は未確認」という物差しを定めることは可能。初回は四方向の表で条件違反と全真反例を混ぜたまま「満たした」と自己採点し、出口での再照合で訂正した。後に現行本文へ条件の版と各条件の真の根拠を求める指示が入った。したがって、旧出力の同じ誤りを現行でも必ず通すとは判定しない。[what記録 17–65行](../product-plans/20261117-find-compatible-pen-refills/what-must-hold/README.md)・[訂正 27–29行](../product-plans/20261117-find-compatible-pen-refills/what-must-hold/internal-records/discussion.md.topic-1.md) |
| how | 原包装＋一件直接確認D、既存情報／通販E、自作集約T、現状N、包装確認だけの部分案を実際に出している。候補根拠と費用の確定・採用は未完。技術検査は実行0件、成立の実証0件。APIの不存在や在庫切れを主張せず、how-to-solveは未閉じのまま正式保留、how-to-buildへ未到達。商品の証拠と実店情報の両方を待つ復活条件が、先に動ける枝を塞ぐのは別問題。[候補 11–45行](../product-plans/20261117-find-compatible-pen-refills/materials/alternatives.md)・[技術検査 13–23行](../product-plans/20261117-find-compatible-pen-refills/materials/technical-feasibility.md)・[層の停止 44–62行](../product-plans/20261117-find-compatible-pen-refills/how-to-solve/README.md)・[出口の採否](../product-plans/20261117-find-compatible-pen-refills/discussion.md) |
| 保守 | 入力の帰属、whatの全真誤判定、実対象が無い技術検査を記録しており、フィードバックが皆無だったという読みは当たらない。C3固有の停止は「既存方法の範囲」として処理されている。同じ案件でSKUだけ追加した場合や、whyが取りこぼした目的の検出は検査項目になっていない。保留を記録できたことから評価できる範囲はそこまでである。[当時の継ぎ目の記録 98–110行](../integration-check/README.md#継ぎ目の摩擦) |

案件rootと3層のdiscussion、計5件の内部論点記録、正本、入力、層記録3件、専門材料2件の計16 Markdownを確認した。内部記録の採用を、実在の仕様や独立した利用者のフィードバックとは数えなかった。

## 長い依頼と長いwhyをどう判定するか

文字数は試す入口の特徴である。判断の難しさは、残すべき関係の数、根拠の有無、誰が何を選べるかで違う。下表は静的な検査から導いた**後日の試運転の合否**。今回、1000字の新規入力をレールに通す処理は実施していない。

| 後で試す場面 | 合格の観測 | 不合格の観測 |
| --- | --- | --- |
| 依頼そのものが長い。別の段落に利用者・提供者・運用者の目的、相反する公開／撤回の希望、試行で許す操作が混ざる | 原文と話者を保つ。誰が何を得て誰が引き受けるかを別々に描き、元の要望を一つ選んで採用・棄却・期限付き保留の根拠まで辿れる。操作禁止を製品の約束に移さない。別の候補を選べば何が失われるかを示す | 原文を添付しても、末尾の撤回要求が候補にも条件にも見送った判断にも現れない。提案に対する一度の同意を、提示していない前提にまで適用する |
| whyだけが壮大で長い。作る人に現実の類似体験が少なく、未来像・望む関係・価値判断が先にある | 願望と既知の事実を分け、別の未来像や両立する目標を描く。選択を変える場面を本人が理解できるように示し、重要な不明があれば、それを知ることで何を選び直すかを残す。実践後にしか分からない価値なら、何を観測するための版かを明示して選ぶ | 類似体験を捏造し、機能数、近さ、短納期だけで目標を縮小する。あるいは過去の一回が無いという同じ理由で、仮説と検証の目的も決められないまま問答が繰り返される |

共通の試金石は「安く作れる狭いもの」に最初から合わせず、原目的を保持したまま、今回届ける版・引き受ける損失・保留を選べるかである。初回C3の設定は元の発言、一回の出来事、既存情報と制約、既知と未確認が**既に分かれた入力**であり、この二種類の代用にはならない。[指定案件の入力](../product-plans/20261117-find-compatible-pen-refills/input.md)

## build-readyを受け取る側からの照合

「初回構築に足りる」を、価値の実現や製品の実装完了とは区別した。現行how-to-build 128–149、170–208行には、同じ具体入力で表示・規則・保存・外の結果を繋ぎ、必須の技術の裏づけ、実装後の受入れ、裁量を分ける方法がある。全ての専門材料を機械的に要求する規則はなく、不可欠な未知が残るなら設計を止められる。この責任を新しい専門に単に分けて押し出せば解ける、とは判定しなかった。[現行の設計方法](../../../../../what-defines-a-product/how-to-build.md)

初回C1の正本から局所例を追った。固定順・V0の親n0からA3を出す例は、初期の蓄え3から0、得点0から3、手札はA2/B5/B2、親n0を保持したn1の保存後に成功を返すところまで、規則・情報・処理をまたいで読める。受け手がこの一手を実装するためにルールを作り直す必要はない。実装後に対象となる受入れと限定的な保存probeの過去の観測も区別されている。その一方で、同じ説明用ID `b1` でも操作ラフの例は見込み文字列付き、保存例と受入れ用入力は見込みなしである。両方の入力が正当である。数字やIDが同じというだけで同一入力の照合済みにはできない。新しい案件の根拠がこの一件で十分とは判断しなかった。[C1正本 86–114行](../product-plans/20261117-explore-card-game-rule-changes/README.md)・[操作例 64–88行](../product-plans/20261117-explore-card-game-rule-changes/materials/experience-sketch.md)・[保存例 25–36行](../product-plans/20261117-explore-card-game-rule-changes/materials/data-model.md)・[実装後の受入れ 64–79行](../product-plans/20261117-explore-card-game-rule-changes/how-to-build/README.md)

作る境界はhow-to-solveに戻す規定があるが、持出し後に費用前提が崩れた場合の決定の正本・受け手が照合する版は未規定である。共同の成果を上流で個別採用した後の総費用も、最終的に採った組合せで評価する必要がある。これらが残るため、リンク検査や専門の自己評価だけをbuild-readyの裏づけに使うことはできない。[CR-007](findings/CR-007-assembled-version-budget.md)・[CR-011](findings/CR-011-authority-after-copy.md)

## 実行した検査と除外

- 素の入力を使った単体検査を実行。実テンプレートの参照を案件構造へ配置し、閉じの提案前と受け入れ後を比較した。さらに引用内の参照定義をPandoc 3.1.11.1のGFM readerと現行のPython checkerに渡した。前者は期待どおりリンク生成、後者は検査0件・成功を返した。再現スクリプトはレビューdirectory内に一時案件を作り、終了時に取り除く。[スクリプト](evidence/check-handoffs.py)・[結果](evidence/check-handoffs.json)
- 指定C3の既存16 Markdownを現行checkerで再検査し、ローカル46参照・失敗0を観測した。意味の採否や当時の手順の正しさとは別の結果である。親担当が行った現行18 Markdownの参照検査は、未展開雛形2箇所の欠損だけを返した。この値を実案件の失敗件数には使っていない。[親担当の検査](evidence/parent-reference-check.json)
- 他の反例は文書の入力・判定・状態遷移に対する静的な検査。過去案件の記載はその当時の観測として扱った。長文の自演、実店舗・メーカー・外部APIへの調査、実利用者への聞き取り、製品の実装・導入、新リポジトリでのsteering起動は実施していない。会話口調、クラウド接続監視用の `scripts/agent/`、全過去steering・archiveの個別品質は、現行製品企画の意味のレビューの対象外とした。archiveを現在の手順として使っていない。
- レビュー成果物の18 Markdownについて、repositoryを参照可能範囲として152リンクを検査し失敗0。記載した対象ファイル・行番号、各指摘の発生条件と対照、優先度の件数、旧検査と現在の判定の区別を読み直した。開始時に取得した454の内容hashに不一致はなかった。
- 修正、commit、pushは行っていない。個別の改善案は未採用であり、互いに関連するものも同時適用を前提にしていない。
