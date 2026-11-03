# Design: プロダクトアイデア育成の3方針を比較し、追加比較へつなげる

## 元の依頼内容

このリポジトリをどう機能させるかについて、3方針で作ってみた。それぞれの比較してもらい、調査結果をこの後作られるsteeringディレクトリに残してほしい。1つ目はfeature-1ブランチのAnthoropicのopusと人が話し合いながら作ったやつ。2つ目はfeature-3ブランチでopenaiのastraモデルで作ったやつ。3つ目はfeature-7ブランチでopen-aiのsolが作ったやつ。比較のやり方やどこに比較結果置くかとかそれぞれのブランチでできたものをどう扱うかとかの設計をこのsteeringで行いたいけど、今後もモデル追加時に比較調査をお願いするかもだからそのつもりで設計してほしい

## TL;DR

`feature-1`、`feature-3`、`feature-7` が持つプロダクトアイデア育成の方針を比較し、後から根拠を確かめられる調査結果をこの steering に残す。今後モデルが追加された場合にも比較を続けられるよう、比較方法、結果の保存先、ブランチ成果物の扱い、追加フローを設計する。

比較の骨格、到達点、評価の優先関係、観点、判定方法、既存資料と新規観測の境界、結果の保存構造、比較時点の原本保持方式、完成後の訂正・supersede、将来targetの受付・採番・再評価フローは合意済みである。各案の設計内容、現時点の利用可能性、検証根拠を分け、このリポジトリの役割を現在どこまで果たせるかを主評価にする。対象が対応する出口ごとに、そこまで再現可能に進める運用能力と、利用者が次の行動へ進めるアウトプット品質を一組で評価する。現在の採用可否と次判断はrouting gate、未成立内部を含む質の差はQ1〜Q15のquality profileで示す。自己目的への適合は不足理由と再利用可能な資産を説明する補助情報に限定する。根拠はQ条件と主要な次判断から逆算し、固定資料、保存済み実行、補助tool、新規ケース実行の順に必要最小限だけ観測する。読者入口と自己完結した結果snapshotを分け、固定commitの全tracked tree、対象版、方針別判定、横断比較、結論、根拠、新規実行を責務別に保存する。原本copyはGit objectとの同一性を検証して不変に保ち、新規実行は隔離copyで行う。完成したsnapshotは上書きせず、誤りは上流原因から再生成した新snapshotで訂正してcurrentを切り替える。将来追加でも、影響しないQだけを検証付きで引き継ぎ、全targetから派生viewを再生成する。提案と合意の履歴は [task-design-discussion.md](./task-design-discussion.md) に置く。

## 完成後の姿

### 比較から分かること

#### 比較の骨格

各ブランチの比較では、次の三つを区別する。

| 読む面 | 比較結果から分かること |
| --- | --- |
| 設計内容 | 何を重視し、どのような進め方と品質条件を置いているか |
| 現時点の利用可能性 | 比較時点で何が用意され、使うために何が残っているか |
| 検証根拠 | どの入力・担当・版・方法の下で、何が確認されているか |

骨格設計としての質、運用ファイルの有無、実証の強さは別の評価である。`feature-1` の未作成の運用 skill は現在の到達段階として記録し、その制作時の対象範囲も踏まえる。`feature-3` の評価記録は sol による実行と改訂を含む根拠として読む。`feature-7` の script は存在・役割と、実行結果を確認したかどうかを区別する。

設計は、比較対象と問い、比較の方法と根拠、結果の保存と参照、各ブランチ成果物の扱い、追加比較の流れを含む。今回の3件に固定した手順へ閉じず、追加する成果物の条件に応じて比較できるよう具体化する。

制作・評価条件が異なる3件から、純粋なモデル性能差は切り出せない。各案の違いを理解するため、この条件差を比較結果に残す。

#### 比較結果の到達点

比較結果は、各方針について、どの目的・前提なら次の採用検討へ進められるか、現時点の根拠だけでは何を保留すべきかを示す。読み手は、どの候補を何を確かめる次の検証へ進めるかを判断できる。

比較結果だけで単一の勝者を決めず、元ブランチの変更・統合も自動的に決めない。実行や統合が必要な場合は、比較で明らかになった不足根拠を入力に別の判断として扱う。これは、条件差を超えた順位を作らず、差分の説明だけで次の判断を読み手へ残さないためである。

#### 評価基準の優先関係

比較の主評価は、各方針がこのリポジトリの役割を現在どこまで果たせるかとする。最初に次を結論にする。

- 粗いプロダクトアイデアから、`build`、追加検証、既存手段の利用、保留、停止のうち根拠に合う次判断へ進めるか。`build` なら、実装者へプロダクト判断を残さず build-ready へ進めるか。
- 調査、比較、整合、可逆な判断をエージェントが進め、動機、好み、費用・リスク許容などユーザーにしか決められない事項を推測しないか。
- 判断の根拠、未決事項、停止・再開位置を残し、実案件の学びを次のアイデアで再利用できるレールへ還元できるか。

自己目的への適合は主評価と並ぶ結論にしない。不足が制作時の約束に対する欠落か、意図的に後続へ残した対象外かを区別し、現在は役割を完遂できない成果物から再利用可能な設計資産を示す補助情報として扱う。自己目的を満たした事実だけで、現在の運用可能性や採用推奨を引き上げない。

#### 主評価の観点

対象が対応すると宣言する出口ごとに、次の二つを一組で評価する。どちらかの強さで他方の不足を相殺しない。

| 主評価 | 観点 |
| --- | --- |
| 運用能力 | 出口の選択と到達、判断主体の分離、品質を作り直す制御、継続運用と学習還元 |
| アウトプット品質 | 意思決定可能性、具体性と境界、整合性と追跡可能性、根拠の十分性と確度、次行動の実行可能性 |

運用能力はfile数、skill分割数、工程数ではなく、粗いアイデアから根拠に合う出口へ進め、質の不足を検知・修正し、別担当・別時点でも継続できる能力としてつながっているかを見る。

アウトプット品質は文書量や体裁で採点せず、利用者が結論を再確認し、適用範囲と不確実性を理解し、追加のプロダクト判断をせず次の行動へ進めるかを見る。五観点は加点集計せず、該当する不足を他観点で相殺しない。

#### 出口別の最低アウトプット契約

共通の品質観点は維持し、最低限必要な内容は出口に合わせる。

| 出口 | 次に可能であるべき行動 | 最低限必要な内容 |
| --- | --- | --- |
| `build` | 実装へ着手する | 自作を選ぶ根拠、最初の価値到達点、scope・非scope、主要体験と失敗・復旧、核心ルールと状態、受入条件、残留risk。実装者へプロダクト判断を残さない |
| 追加検証 / `validate-first` | 検証を実施し、結果から次の出口を決める | 仮説、対象・入力、手順、事前の成功・失敗基準、期間・件数・費用等の上限、結果の保存先、結果別の次判断、停止条件 |
| 既存手段の利用 / `use-existing` | 採用・設定・移行・運用を開始する | 自作より選ぶ根拠、確認済み機能と未確認事項、前提・権限、構成・設定・移行順、費用、確認方法、失敗時の復旧・撤退条件 |
| 保留 / `park` | 状態を失わず条件成立時に再開する | 今決めない理由、未確定事項、再開を発火する条件・観測方法、保存する正本、再開時の最初の一手 |
| 停止 / `stop` | 不要な作業を終え、同じ検討を根拠なく繰り返さない | 停止理由と根拠、棄却した有力案、適用範囲、判断が覆る条件。実行しない成果物を形式上作らない |

build用の仕様書一式を他の出口へ機械的に要求しない。一方、非buildというだけで浅い一文を許さず、その出口の次行動に必要な具体性、根拠、再開・終了条件を要求する。

#### 期待品質と実測品質の区別

運用能力とアウトプット品質の両方について、次を分ける。

| 段階 | 確認すること | 言えること |
| --- | --- | --- |
| 設計内容 | 役割、判断順序、出口別契約、品質条件、不合格時の戻り先 | どの品質を狙う設計か |
| 現時点の利用可能性 | 固定コミットの入口、skill、template、正本、gateで開始・継続・完了でき、欠落時に止められるか | 現成果物からどの品質を期待できるか |
| 検証根拠 | 特定可能な版、入力、担当、方法で実行され、実出力の指摘・修正・限界を追えるか | その条件で実際に得た品質 |

設計と運用成果物から理由付きで述べる期待品質を、実現が観測された品質と混ぜない。保存済み評価も、その対象版・入力・担当・方法と実出力が裏付ける範囲に限定する。

主評価で不足がある場合は、最も手前の不足に応じて、設計の補完、運用成果物の作成、追加検証、改訂後の再検証のいずれかへ進める。両方が根拠付きで成立する場合だけ、確認した出口・入力条件・限界に限定して採用検討へ進める。

#### routing gateとquality profile

次判断を一意に導くrouting gateと、3案の質の差を読むquality profileを分ける。gateだけで質を順位付けせず、profileだけでblockingな不足を消さない。

routing gateは次の四つとする。

| gate判定 | 意味 |
| --- | --- |
| `成立` | 明示した適用範囲内で、その出口・段階に必須の運用能力と品質下位条件がすべて成立し、blockingな不足・矛盾・未確認がない |
| `未成立` | 必須条件の少なくとも一つに、確認済みの欠落・不十分・矛盾・失敗がある |
| `未確認` | 必須条件を判定する資料または実行結果が不足し、成立とも未成立とも言えない |
| `非該当` | その出口では下位条件が不要で、同じ役割を担う代替物と不要理由を示せる |

旧 `限定成立` は用いない。結論を制限する入力種別、出口、利用者、実行環境、対象版、担当・モデル等は、判定語と別の `適用範囲` 欄へ必ず記録する。狭い範囲ですべて満たすなら、その範囲で `成立` とする。範囲内に不足があれば `未成立`、範囲を判断できなければ `未確認` とする。

quality profileでは、品質五観点を次の下位条件へ分ける。

| 品質観点 | 下位条件 |
| --- | --- |
| 意思決定可能性 | Q1 結論・出口が明示される / Q2 有力な対案と選択理由を再確認できる / Q3 判断が変わる条件が分かる |
| 具体性と境界 | Q4 actor・状況・入力が具体的である / Q5 完了結果を観測できる / Q6 scope・非scope・境界caseを区別できる |
| 整合性と追跡可能性 | Q7 元要求・根拠から結論と成果物へたどれる / Q8 成果物と次行動から根拠へ戻れる / Q9 file間の用語・数値・状態・版が矛盾しない |
| 根拠の十分性と確度 | Q10 重要主張に出典または観測がある / Q11 主張の強さが根拠の強さを超えない / Q12 未確認・推論・残留risk・適用限界が分かる |
| 次行動の実行可能性 | Q13 次の担当・入力・開始条件が分かる / Q14 手順またはscopeと必要成果物が分かる / Q15 合否・停止・失敗時の戻り先が分かる |

出口別最低契約はQ条件の読み方を決める。たとえばQ15は、`build` なら受入条件と実装中の戻り先、`validate-first` なら成功・失敗基準と結果別の次判断、`park` なら再開条件と最初の一手として読む。

#### quality profileの深さ

各Q条件は、設計内容、現時点の利用可能性、実測支持の三段階ごとに、評価済み、`未確認`、`非該当`を先に記録する。評価済みの場合だけ次の深さを付ける。

| 深さ | 共通する意味 | 設計内容 | 現時点の利用可能性 | 実測支持 |
| --- | --- | --- | --- | --- |
| `欠落` | 必要性を確認したが該当内容がない | 責務・条件が定義されていない | 必要なskill・template・gate・正本がない | 対象出力に必要内容がない、または失敗が観測された |
| `断片` | 関連要素はあるが、判断や行動へ使える単位になっていない | 名前・方針・項目だけで、入力・境界・水準がない | 部品や欄はあるが開始から完了までつながらない | 記述や実行主張はあるが対象版・入力・基準と結び付かない |
| `具体化` | 主経路は具体的だが、重要な接続・境界・例外の一部が不足する | 主要部分は定義されるが、他責務との接続または戻り先が不足する | 主経路は実行できるが、blocking欠落の検知、重要分岐、handoffの一部が不足する | 実出力と条件を確認できるが、重要な境界case、反証、修正後確認の一部が不足する |
| `成立` | 当該段階の必須内容がつながり、blockingな不足がない | 責務、入出力、境界、水準、戻り先が矛盾なく定義される | 固定コミットだけで実行・検査でき、欠落時に誤って完了扱いしない | 特定可能な版・入力・担当・方法で観測され、指摘・修正・限界まで追える |

深さは数値化、合計、平均しない。`具体化` が複数あっても `欠落` を相殺しない。`未確認` は深さゼロではなく根拠不足の別状態、`非該当` は理由と代替物を伴う。

各方針・出口・段階のprofileには、Q条件の深さに加え、成立範囲、routing gateを止めたblocking gap、blockingではない改善余地、固定コミットまたは実行条件へ戻れる根拠を残す。比較表を `未成立` だけで終えず、同じ出口・品質観点・段階のQ条件を3案で横に並べる。

必須Q条件がすべて `成立` の場合だけrouting gateを `成立` とする。必須条件に `欠落`、`断片`、`具体化` があればgateは `未成立` だが、profileには他の成立範囲を残す。既知のblocking不足がなく必須条件に `未確認` があればgateは `未確認` とする。`非該当` は、出口別契約上の不要理由と代替物がある場合だけ成立判定から除外する。

主要な次判断は、最も手前のblockingまたは未確認段階から、`設計補完`、`資料確認`、`運用成果物補完`、`追加検証`、`改訂後再検証`、`条件付き採用検討` のいずれか一つを示す。同じ次判断になる案同士も、quality profileの成立範囲、深さ、blocking gap、改善余地から比較する。

#### 既存資料と新規観測の境界

最初に、どのQ条件のどの段階が `未確認` で、それが主要な次判断を変え得るかを特定する。固定コミットの資料照合、保存済み実行の独立評価、補助toolの確認、新規ケース実行の順に、結論を変え得る最小の追加観測だけを行う。根拠の量を対象間で機械的に揃えず、支持するQ条件と主張可能な範囲を揃える。

| 根拠の種類 | 単独で支持できる範囲 | 単独では支持できないこと |
| --- | --- | --- |
| 固定コミットの設計資料 | 設計内容のprofile、明示された責務・出口・品質契約 | 現在実行できること、実際の出力品質 |
| 固定コミットの運用成果物 | 現時点の利用可能性、期待品質を生む仕組みの有無 | 実案件で期待品質を得たこと |
| 保存済み実行一式 | 条件を追える範囲の実測支持、失敗・改訂・再確認の経路 | 別版、別出口、別入力、別担当での再現性 |
| 元資料の評価主張 | 元資料が何を主張しているか | 参照出力と条件を独立確認していない主張の正しさ |
| 今回の静的な独立評価 | 読み取った設計・成果物・保存出力がQ条件を満たす深さ | 未保存の実行、再現性、別条件での品質 |
| 今回の補助tool実行 | toolが実際に検査する構造・機械的条件 | toolが観測しない意味内容や出口成果物の質 |
| 今回の新規ケース実行 | 固定した版・入力・担当・方法・出口で観測した運用能力と出力品質 | 未実行条件への一般化、純粋なモデル性能差 |

元資料の主張、今回確認した事実、今回の解釈を分ける。元資料の「成功」「通過」等は、それ自体を実測支持にしない。一方、事前に同じrubricを使っていなくても、版・入力・実出力を追える場合は、今回Q1〜Q15を適用した独立評価の根拠にできる。ただし、元の実行が同じrubricで自己修正した証拠にはしない。

保存済み実行を実測支持へ使う範囲は、次を追えるQ条件に限定する。

1. 対象成果物またはrulesetの版をcommit、hash、保存copyのいずれかで特定できる。
2. 実行へ渡した入力と、高影響の追加指示・回答を確認できる。
3. 実行担当、方法、ユーザーまたは別agentの介入が、結論へ影響する範囲で分かる。
4. 対象出口の出力一式が保存され、Q条件を結果から直接確認できる。
5. review・改訂を根拠にする場合、指摘、変更内容、変更後に再確認した版を結び付けられる。
6. 実行の出口と適用範囲が、今回判定する出口・条件に対応する。

欠ける来歴が結論へ影響しない場合だけ、理由を記録して支持範囲を狭める。欠落を推測で補わない。設計・利用可能性を固定資料から判定できる場合、条件の揃った保存済み実行から必要な実測profileと限界を作れる場合、版の差が該当Qへ影響しない場合、または追加実行が主要な次判断を変えない場合は、既存資料で止める。

`未確認` が主要な次判断を変え、実際の振る舞いでしか解消できない場合だけ新規観測へ進む。先に未読資料、参照関係、保存済み実行の不足ファイル、対象版との差分を照合する。補助toolはその観測範囲に限って使い、構造検査を意味品質へ昇格させない。実出力の未成立を確認した場合は、設計、運用成果物、入力条件、実行のばらつきのどこが最上流原因かを切り分ける。設計・運用成果物の欠陥なら `改訂後再検証` とし、ばらつき自体が次判断を変える場合だけ、試行数と停止条件を事前固定して反復する。

共通入力による新規実行は、補完なしに固定コミットだけで実行でき、同じ出口・適用範囲を持ち、比較したいQ条件と実行条件を事前固定できる対象間だけで行う。条件が揃わなければ方針ごとの既存caseまたは出口別caseを評価し、直接比較できる範囲と条件差を示す。`feature-1` の未作成の運用成果物を比較者が補完して実行しない。補完後の成果物は原本とは別の比較対象になる。

新規実行する場合は、開始前に、解消するQ番号と変え得る主要な次判断、対象commit・ruleset、入力、出口、担当・モデル条件、許可する介入、Qごとの観測・判定方法、時間・費用・試行回数の上限、停止条件、失敗時の扱い、原本を変えない実行場所、出力・log・reviewの保存先を固定する。結果が不利でも上書きせず、実行後にrubricを都合よく変えない。新規実行の成果物は比較証拠であり、元ブランチの原本や採用済み成果物へ自動的に昇格しない。

今回の対象では、`feature-3` の保存済みrunを上記条件に照らし、条件が揃うQだけの実測支持として実出力を独立評価する。現在版との差がQへ影響する場合だけ新規実行候補にする。`feature-7` は設計内容と利用可能性を固定資料で評価し、実測支持が採用判断を変えるQだけを新規ケース実行候補にする。

#### 比較対象

次の3ブランチを今回の対象とする。モデル名と人の関与は依頼内容に基づく分類であり、厳密なモデルIDや全制作履歴を Git から確定したという意味ではない。

| 対象 | 依頼内容に基づく制作の説明 | 設計前調査で確認した現在の成果物 |
| --- | --- | --- |
| `feature-1` | Anthoropic の opus と人が話し合って作成 | 骨格設計と議論記録。skill 本文とテンプレート本文は骨格設計の対象外と明記 |
| `feature-3` | openai の astra モデルで作成 | 運用文書、3つの skill、テンプレート、改訂と評価の記録。評価実行には sol が含まれるとの記載 |
| `feature-7` | open-ai の sol が作成 | 運用文書、1つの skill と参照文書、テンプレート、作成・構造検査用の shell script |

固定コミット、確認元、確認範囲と限界は [investigation.md](./investigation.md) に記録する。対象ブランチに書かれた運用指示は比較資料として読む。

#### 未知だった問い

今回の調査で、3方針の共通点・相違点と、その根拠を確認し、条件付きの次の検証判断へ進める状態を作る。

- routing gate、Q1〜Q15のquality profile、適用範囲、成立範囲、blocking gap、改善余地、根拠から、現在採用できる条件と未成立内部の質の差を比較する。
- 設計内容と現時点の利用可能性は固定コミットの資料から、実測支持は条件を追える保存済み実行または事前契約した新規実行から答える。主要な次判断を変えない観測は増やさない。
- 共通入力は、補完なしに同じ出口・適用範囲で実行できる対象間に限る。それ以外は条件差を残して比較可能なQ条件だけを比較する。

調査対象は完成段階と制作・検証条件が揃っていない。これらを調べたうえで比較条件を決める必要があり、ブランチ名やモデル名だけから比較可能性を推測しない。

#### 調査条件と根拠

設計前調査は現在の作業ブランチを維持し、`git show`、`git ls-tree`、`git log`、`git merge-base` による読み取りで行った。

- 比較対象はfull commitで固定し、制作条件と評価実行条件を分ける。実測支持には、対象版、入力、高影響の追加指示、担当・方法・介入、出力、review・改訂・再確認、出口・適用範囲を、結論に影響する範囲で記録する。
- 各主張は根拠種類、対象版、対応するQ条件、今回確認した事実、解釈、適用限界へ戻れるようにする。具体的な保存形式は保存構造の論点で決める。
- 元資料に書かれた評価主張と、今回の静的独立評価、補助toolの観測、新規ケース実行の観測を区別し、各根拠種類が単独で支持できる範囲を超えて結論を広げない。

現時点で、既存の評価記録を読んだことから、今回その実行結果を再現したとは扱わない。設計前調査の観測範囲は [前提とする既存仕様](#付録前提とする既存仕様) を参照する。

### 比較結果を保存し、次の比較で読む

今回の調査結果は、この `working_dir` 配下へ保存する。

`working_dir` は `/Users/takahiroumeda/src/github.com/tumeda1992/grow-product-ideas/.steering/2026/202609/20260919-design-model-approach-comparison` である。

#### 保存構造

working directory直下の `comparison.md` を現在の比較結果へ入る読者入口とし、実際の比較結果は `comparisons/<comparison-id>/` の自己完結したsnapshotへ保存する。今回の最初のsnapshotは `comparisons/001-baseline/` とする。

```text
20260919-design-model-approach-comparison/
├── design.md
├── investigation.md
├── task-design-discussion.md
├── comparison.md
└── comparisons/
    └── 001-baseline/
        ├── manifest.md
        ├── summary.md
        ├── matrix.md
        ├── evidence-index.md
        ├── profiles/
        │   ├── feature-1--d88ed099.md
        │   ├── feature-3--f6481b8c.md
        │   └── feature-7--83c9dbf5.md
        ├── sources/
        │   ├── feature-1--d88ed099/
        │   │   ├── provenance.md
        │   │   ├── inventory.jsonl
        │   │   └── tree/
        │   ├── feature-3--f6481b8c/
        │   │   ├── provenance.md
        │   │   ├── inventory.jsonl
        │   │   └── tree/
        │   └── feature-7--83c9dbf5/
        │       ├── provenance.md
        │       ├── inventory.jsonl
        │       └── tree/
        └── runs/
            └── <run-id>/
                ├── contract.md
                ├── input/
                ├── output/
                └── review.md
```

`sources/` は比較前から固定commitに存在した全tracked contentの保存copy、`runs/` は今回新規実行して生成した証拠であり、混ぜない。`runs/` は新規実行を行う場合だけ作る。

#### working directory直下の正本分担

| file | 正本として持つ内容 | 持たない内容 |
| --- | --- | --- |
| `design.md` | 合意した比較目的、評価方法、受け入れ条件、保存・追加方針 | 実際の3案の判定結果 |
| `investigation.md` | 設計を変え得る事前調査、固定commit、確認済みの成果物所在と条件差 | 合意後のQ profileや採用判断 |
| `task-design-discussion.md` | proposal、feedback、decisionの履歴 | 現在の比較結果の正本 |
| `comparison.md` | 読者入口、current snapshot、対象と結論の短い要約、読み順、過去snapshotへの索引 | Q1〜Q15の詳細profileや証拠本文 |

`comparison.md` は、current snapshotへの相対link・status・method hash、target ID・full commit・制作条件の短い説明、各案の対応出口・到達段階・実測支持範囲・主要な次判断の一行要約、詳細fileの読み順、snapshotごとの対象差分・method差分・statusの履歴を持つ。current pointerを更新しても詳細を複製せず、最新結論はsnapshotのsummary、方針別詳細はprofiles、根拠はevidence-indexを一意の読み先にする。

`design.md` を比較方法の正本とし、snapshotのmanifestに、使用した `design.md` のcontent hashと、利用可能ならそのfileを含むcommitを記録する。rubricを別のmethod fileへ複製しない。

#### snapshot内の正本分担

| path | canonicalに持つ内容 | 他fileとの関係 |
| --- | --- | --- |
| `manifest.md` | comparison ID、status、観測期間、method hash、対象ID、branch申告名、full commit、制作・評価条件、対象出口、実施・未実施の観測 | snapshotの比較単位と再現条件の正本 |
| `profiles/<target-id>.md` | 方針ごとの適用範囲、routing gate、主要な次判断、運用能力、Q1〜Q15の三段階profile、成立範囲、blocking gap、改善余地、自己目的の補助情報、根拠参照 | 方針単体の判定事実と解釈の正本 |
| `matrix.md` | 同じ出口・段階・Q番号を3案で横に並べた比較、条件差、直接比較できない箇所 | profilesから作る横断view。矛盾時はprofilesを正とする |
| `summary.md` | リポジトリの役割に対する3案の結論、条件付きの向き不向き、各案の主要な次判断、比較限界 | snapshot単位の結論の正本。profileとevidenceへlinkする |
| `evidence-index.md` | evidence ID、根拠種類、対象版、原本参照、対応Q、今回確認した内容、元資料の主張、解釈、限界 | evidence参照の正本。結果本文へ長い引用を複製しない |
| `sources/<target-id>/` | 固定commitの全tracked tree、Git identityとcapture・検証記録 | snapshotが使った原本本文のcanonical copy。評価annotationと新規run出力を置かない |
| `runs/<run-id>/` | 新規実行の事前契約、入力、sanitizedされた必要出力、独立review | 新規実行をした場合だけ。元ブランチ原本と分ける |

target IDはbranch名だけにせず、`<branch-slug>--<short-commit>` とする。manifestにはfull commitを必須とし、model名や人の関与はtarget identityではなく、依頼内容または資料に基づくattributionとして別欄へ置く。baselineの対象は次の通りである。

| target ID | full commit |
| --- | --- |
| `feature-1--d88ed099` | `d88ed099c7e9498a6cd3626f7c13c99fa5063778` |
| `feature-3--f6481b8c` | `f6481b8cc4241b5923e0bcb91929dd6b473028ed` |
| `feature-7--83c9dbf5` | `83c9dbf5f77f025e98e6a7c8f1952fa6abc4e5b5` |

各profileは、対象と適用範囲、routing gateと主要な次判断、運用能力profile、出口別Q1〜Q15 profile、成立範囲・blocking gap・改善余地、自己目的への適合と再利用可能な資産、根拠と未確認の順に持つ。Q profileは一つの巨大な表にせず五品質観点ごとの小さい表へ分け、横断比較に必要な要約だけをmatrixで同じQ番号に揃える。

#### 整合規則

- manifestに存在しないtarget、method版、runを他fileから参照しない。
- profileのgate、深さ、次判断はevidence IDを一つ以上持つか、`未確認` の理由を持つ。
- matrixはprofileにない判定を追加しない。直接比較できない箇所は空欄にせず理由を書く。
- summaryの主要な次判断はprofileのrouting結果と一致させる。
- comparisonのcurrent conclusionはcurrent snapshotのsummaryから導き、独自の詳細解釈を加えない。
- 元資料の主張、今回確認した事実、今回の解釈をevidence-indexとprofileで分ける。
- 新規runのinput、output、reviewをrun IDで結び、失敗結果も削除・上書きしない。

baseline作成後は、`comparison.md` から結論、方針別profile、横断matrix、Qごとの根拠へlinkだけで到達できること、target IDとfull commitを取り違えないこと、同じQの結論・適用範囲がfile間で矛盾しないこと、`feature-3` の保存済みrunと `feature-7` の新規run候補または未確認理由を区別できることを確認する。固定資料のevidenceはsnapshot-localなsource pathとGit identityへ戻れるようにする。第四案を仮定し、既存3案のprofileやbaseline snapshotを書き換えずに追加できる構造であることも確認する。

#### snapshotの訂正とsupersede

manifestの `status` はsnapshot自身の作成状態だけを表す。

| status | 意味 |
| --- | --- |
| `draft` | 作成中。fileを更新できるがcurrentにはできない |
| `complete` | 全受け入れ条件、file間整合、原本検証を通過した。以後snapshot全体を編集・削除しない |

currentか、後継へ置き換えられたかはsnapshotへ後書きせず、root `comparison.md` のpointerとhistoryで管理する。historyはsnapshotごとに次の関係statusを持つ。

| 関係status | 意味 |
| --- | --- |
| `current` | 現在の判断に使うcomplete snapshot。原則一つ |
| `superseded` | 当時の証拠・methodではcompleteだったが、訂正版または後続比較をcurrentにしたため履歴として残す |
| `invalidated` | source identity・完全性等の欠陥でsnapshot全体または主要結論を信頼できず、後継完成前でも現在判断に使わない |

各snapshotのmanifestには、root `comparison.md` で現在の関係statusを確認する案内を完成時から持たせる。complete後の旧snapshotへ `superseded-by` を追記しない。

complete前の誤記・不足は同じdraft内で直す。complete後も、current targetや結論を変えない `comparison.md` の文章上のtypo・同じsnapshotを指すlink表示だけは、入口の保守として修正しlink validationをやり直せる。source capture、evidence ID・引用元・事実、Q深さ、gate、主要な次判断、summary等の意味を変える誤りは旧snapshotで直さない。

誤りが見つかった場合は、次の依存順に影響を追う。

```text
target/source → evidence → profileのQ・gate・次判断 → matrix → summary → comparison
```

最上流の誤りから下流を再生成した新しい自己完結snapshotを作り、新snapshotがcompleteになった同じchange setでだけcurrent pointerとhistoryを更新する。新snapshotは差分だけでなく、通常と同じmanifest、sources、evidence-index、profiles、matrix、summary、必要なrunsを持つ。manifestへ、置き換えるsnapshot、誤りの事実と理由、known issue ID、訂正範囲、同一性を再検証して引き継いだ入力、再生成物とvalidationを記録する。

訂正時もsourceをblind copyせず、Git objectが読めれば固定commitから再capture・再検証する。失われている場合は旧snapshotのsourceとinventoryを入力にした制約をprovenanceと適用限界へ記録する。runを引き継ぐ場合もhashと来歴を確認し、run自体の問題を都合のよい再実行で消さない。新規実行の要否は既存資料と新規観測の境界に従う。

以前 `未確認` と正しく記録した事項に新証拠が増えた場合、target commit・対象案・実行case・method hash・rubricが変わる場合は訂正でなく追加比較・再評価へ送る。新情報から旧記述の事実誤認が判明した場合は訂正する。複数の妥当な解釈がありQ判定・適用範囲・主要な次判断が変わる場合、またはrubric変更が必要な場合はユーザー判断へ返す。

誤りがrouting gate、主要な次判断、target identity、source完全性を変え得る場合はblocking known issueとし、訂正版完成を待たず `comparison.md` へ、issue ID、発見日、報告された事実、影響し得るtarget・evidence・Q・結論、currentを使える範囲、次の確認を警告する。source identity・完全性を信頼できなければcurrentを外して `invalidated` にする。blockingでない一部の成立範囲・改善余地だけへの影響なら、currentを維持しつつknown issueを表示できる。どちらも暫定結論を推測しない。

訂正snapshotでは、影響scopeだけでなく全file整合、全source identity、linkを再validationし、元の誤りを検出できる回帰caseを追加する。`feature-3` のsymlink誤dereference、`feature-7` の構造checkを意味品質の実測支持へ誤昇格するcase、新しい第四案または新runを訂正と誤分類するcaseを具体例にする。訂正版complete前にcurrentを切り替えないこと、blocking defectを無警告で残さないこと、historyからissue・旧結論・後継へ到達できること、旧snapshot配下のhashが変わらないことを確認する。

将来追加時のsame/new steering、method変更、carry forwardと再評価の境界は「新しいモデルや方針を比較へ追加する」に従う。

### 比較対象ブランチの成果物を扱う

この設計中は `feature-1`、`feature-3`、`feature-7` を checkout せず、現在の作業ブランチから読み取る。比較対象の application 成果物へ変更を加えない。

#### 固定commitの原本をsnapshotへ保持する

各targetの固定commitにあるtracked tree全体を、`sources/<target-id>/tree/` へraw byte単位で保存する。Q判定で直接引用したfileだけに絞らない。固定commitをtarget identityの起点、source copyをsnapshotで読む証拠本文のcanonical copy、profile・matrix・summaryを判定と解釈とする。Git objectが後日失われても保存本文とcapture時の同一性検証は残すが、その時点でGit履歴を再検証できるとは主張しない。

- regular fileは改行変換・整形せず、Git blobのbyteを保存する。
- executable bitを含むGit modeを保持する。
- symlinkは参照先を展開せず、link自体とtarget文字列を保持する。
- `.git/`、固定commitにないuntracked file、比較者の一時fileは含めない。
- commitの親群、author/committer、日時、message、tree IDは来歴として記録するが、比較に不要な全履歴を複製しない。

各 `sources/<target-id>/provenance.md` は、target ID、申告branch、full commit、parent群、tree ID、author/committerと日時、source repository、capture日時・方法、entry数・合計byte数、symlink・executable・submodule件数、除外の有無、検証結果と未検証事項を持つ。`inventory.jsonl` はpath、Git mode、object type、blob/object ID、byte数をtracked entryごとに持ち、pathをJSON文字列としてescapeする。submoduleはcommit objectとして明示し、通常fileとして代用しない。

source captureのcomplete条件は次の通りである。

1. 固定commitのrecursive treeとinventoryのpath、mode、object ID、sizeが一致する。
2. 保存treeのregular fileとsymlink targetをGit blobとしてhashし、inventoryのobject IDと一致する。
3. executable bitとsymlink種別がinventoryと一致する。
4. 余分なpath、欠けたpath、内容不一致が0件である。
5. provenanceのtarget commitとsnapshot manifestのtarget ID・full commitが一致する。

一つでも不一致ならsource copyを根拠にprofileを確定せず、captureをやり直す。`feature-3` の `.agents/skills/` 配下にある3symlinkを、dereferenceしていないことの具体的な検証caseにする。

固定資料のevidence entryは、snapshot-localな `sources/<target-id>/tree/<path>`、full commit、元path、blob IDを持ち、provenanceのcapture検証へ戻れるようにする。行番号は補助locatorに留め、identityには使わない。source treeへannotationや評価結果を書き込まず、結果fileには長い引用を複製しない。

source treeを新規実行の作業場所にせず、runごとの隔離copyから実行する。contractにtarget ID、source inventory hash、実行用copyへ加えた許可済み入力を記録し、実行前後にsource hashが変わっていないことを確認する。生成物、log、reviewは `runs/<run-id>/` に置く。

将来targetに巨大binary、submodule、資格情報・個人情報等の保存不適切なtracked contentがあれば、黙って除外・redactして完全copyと称しない。snapshotをcompleteにせず、対象path、理由、比較への影響を記録して、保存可否または適用範囲をユーザー判断へ返す。

branch先端を自動追従しない。同じbranchでも新しいfull commitは新targetとし、旧target IDと過去snapshotを変更しない。比較は改善・採用・統合の候補と根拠を次判断として記録するところまでとし、元ブランチの変更・統合は別のユーザー承認と実行作業にする。

### 新しいモデルや方針を比較へ追加する

将来、新しいモデルの成果物が増えた場合に比較調査を依頼できることを前提とする。新しいモデルだけでなく、既存branchの新commit、同じartifactへの新しい実測、method変更も同じ規則で分類する。

#### targetの受付とidentity

targetとして受け付ける最小単位は、このrepositoryでfull commitに固定でき、合意済みの方法で完全なsource copyを保存できるtracked artifact treeである。branch名、モデル名、未保存の会話だけではtargetを作らない。受付時は次を記録する。

| 受付情報 | 扱い |
| --- | --- |
| source repository、branch/ref、full commit | identityとsource captureに必須。解決不能ならcompleteにしない |
| 試行の目的、scope・非scope・完了条件 | 自己目的の補助評価と不足理由に使う。不明は `unknown` |
| 入口、skill/template/script、正本、対応出口 | 設計・利用可能性profileへ使う |
| 制作モデル、人の関与、入力、時間・費用等 | 依頼、資料、観測を分けてattributionする。不明でもartifact比較は止めない |
| 保存済みrun、review、改訂 | 来歴最低条件を満たすQだけ実測支持へ使う |
| 追加理由、current更新意図 | same/new steeringとtarget集合を決める |
| source保存制約 | 資格情報、個人情報、巨大binary、submodule等を確認し、完全保存できなければ停止してユーザーへ返す |

target IDは `<branch-slug>--<unique-short-commit>` とし、baselineはcommitの先頭8桁、衝突時は一意になるまでprefixを延ばす。同じfull commitが既存targetならIDを重複作成せず、新branch名をalias/refとしてmanifestへ記録する。同じbranchの新commitは新targetである。旧版をcurrent集合から置換するか、進化比較のため併記するかで結論が変わる場合だけユーザーへ確認する。モデル、人の関与、promptはidentityでなく制作条件であり、同じartifactを別条件で実行した場合はrun/evidenceを分ける。

#### comparison IDとsame/new steering

同じworking directoryでは、理由にかかわらず未使用の次の3桁連番と短いslugをcomparison IDにする。`001-baseline`、`002-add-<target-slug>`、`003-correct-<scope-slug>`、`004-recheck-<scope-slug>` のように付け、一度使ったIDを再利用・改名・詰め直ししない。日付はmanifestの開始・完了日時に持つ。追加、訂正、recheck、semanticなmethod改訂はいずれも、差分patchでなく必要な全正本を持つ自己完結snapshotにする。

次をすべて満たす場合は、このworking directoryに次snapshotを追加する。

- 主評価がこのrepositoryの役割を現在どこまで果たせるかのままである。
- routing gate、Q profile、出口別契約の意味系譜が同じである。
- targetを同じsource・evidence契約で保存できる。
- 過去snapshotを一つのcurrent comparisonとして更新する意図がある。

repository役割・比較で可能にする意思決定が変わる、別repositoryや機密区分のため保存契約が異なる、methodを既存Q・出口へ意味対応できない、独立実験・監査として履歴を分ける場合は別steeringを作り、互いをrelated comparisonとして参照する。モデル数、日付、file数だけでは分けない。別steering化した依頼はこの `comparison.md` のcurrentを変えない。

#### method変更、carry forward、再評価

文言を明確化するだけでQ、閾値、出口、根拠強度、次判断を変えない変更はnon-semanticとしてmanifestへ記録し、影響しないQを再評価しない。semanticな変更は、同じ役割・意思決定を保ち旧新のQ・出口・判定を対応付けられる場合だけ同じsteeringで行う。変更したQ、gate、出口、根拠条件へ依存する全targetを再評価し、一部だけ旧基準のmatrixへ混ぜない。対応不能なら別steeringへ分ける。ユーザー合意を要するmethod変更はtask-designへ戻し、合意前の基準で新snapshotをcompleteにしない。

既存Qをcarry forwardできるのは、次をすべて満たす場合だけである。

1. target full commitとsource inventory hashが同一で、新snapshotでもsource identityを検証できる。
2. Qに適用するmethod、出口契約、深さrubric、evidence最低条件の意味が同じである。
3. 新事実、run、反証、known issueがそのQの段階、適用範囲、判定を変えない。
4. 参照evidenceを新snapshot内へ保持し、linkとhashを再確認できる。
5. 引き継いだQ、判定、根拠範囲をmanifestへ列挙する。

target commit・source inventory、method、evidence、known issue、適用境界が変わった場合は、影響するtarget・Qを再評価する。Q判定をcarry forwardできても、matrix、summary、`comparison.md` の短い結論は全target集合から毎回再生成し、新targetを含む向き不向き、比較不能箇所、主要な次判断を旧summaryから流用しない。

#### 追加フローとユーザー判断の境界

1. 依頼、追加理由、current更新意図を受付記録へ保存する。
2. refをfull commitへ解決し、同一target、新target、既存branchの新版を分類する。
3. same/new steeringを判定し、結果の意味が変わる場合だけユーザーへ一つの選択を返す。
4. 同じsteeringなら次IDのdraft manifestを作り、currentとの差をtarget、source、条件、evidence、method、出口・適用範囲で記録する。
5. 新targetのsourceをcapture・検証し、既存targetも新snapshot内のsource identityを確認する。
6. carry forwardするQと再評価するQを根拠付きで決め、必要な場合だけ最小観測を事前契約する。
7. 新targetと影響する既存targetをprofileし、未完成targetを比較者が補完しない。
8. 全targetのprofilesからmatrix、summary、短い結論候補を再生成する。
9. source、evidence、Q、gate、file間整合、link、訂正回帰caseをvalidationしてcompleteにする。
10. 同じchange setでcurrent pointerとhistoryを更新し、旧currentをsupersededとして残す。

agentはGitと資料から確認できる受付情報、Q評価、carry-forward影響分析を進める。ユーザーへ返すのは、source保存の許可、同branch新版の置換か併記、目的・methodの変更、複数の妥当な解釈で主要な次判断が変わる場合に限る。不明な制作モデルや人の介入を埋めるためだけに追加を止めない。

第四案、`feature-7` の新commit、同commitへの新run、semanticなmethod変更、ref解決不能またはsource保存不能、別目的の六caseでこのフローを検証する。comparison IDの再利用、alias branchによるtarget重複、同一性根拠のないcarry forward、追加後も旧3案だけのsummary、別steeringからのcurrent変更を失敗として検出する。

## 要件（Requirements）

### MUST（必達）

- `feature-1`、`feature-3`、`feature-7` の3方針を比較する。
- 調査結果をこの steering ディレクトリへ残す。
- 比較方法、保存先、各ブランチ成果物の扱いを設計対象に含める。
- 今後モデルが追加された際の比較調査を考慮する。
- working directory直下の `comparison.md` を現在結果への入口、`comparisons/001-baseline/` を実結果のsnapshotとし、方法、事前調査、議論履歴、実結果の正本を分ける。
- snapshotではmanifest、summary、matrix、対象別profile、evidence-index、新規実行時のrunsの責務を分け、targetを `<branch-slug>--<short-commit>` とfull commitで固定する。
- 各targetの全tracked treeをsnapshotのsourcesへbyte・mode・symlinkを保持して保存し、provenanceとentry単位のinventoryで固定commitとの同一性を検証する。
- source copyを完成後に変更せず、evidenceはsnapshot-local pathとGit identityへ戻し、新規runはsourceと分離した隔離copyで行う。
- 保存不適切なtracked contentを黙って除外・redactせず、完全性を満たせないsnapshotをcompleteにしない。
- 将来targetはfull commitへ固定できるtracked artifact treeを単位とし、同じcommitを重複targetにせず、同じbranchの新commitを新targetとして扱う。
- comparison IDは同じworking directory内の未使用3桁連番と短いslugを使い、再利用・改名・詰め直しをしない。
- repository役割、意思決定、methodの意味系譜、source保存契約を保つ追加は同じsteering、これらを保てない依頼または独立監査は別steeringに分ける。
- semanticなmethod変更は影響する全target・Qを再評価し、旧新基準を同じmatrixへ混ぜない。対応不能なら別steeringへ分ける。
- full commit、source inventory、method、evidence、適用範囲が不変なQだけを検証付きでcarry forwardし、matrix、summary、comparisonの短い結論は全target集合から再生成する。
- snapshotはdraft中だけ編集し、complete後は全fileを不変にする。意味を変える訂正は誤りの上流から新しい自己完結snapshotで再生成する。
- snapshot内部のdraft/completeと、入口で管理するcurrent/superseded/invalidatedを分け、訂正版completeと同じchange setでだけcurrentを切り替える。
- blockingなknown issueは訂正版完成前に利用不能範囲を入口へ警告し、source identity・完全性を信頼できなければcurrentから外す。
- 新証拠、target、run、method、rubricの変更を過去の誤りと混同せず追加比較へ送り、複数解釈やrubric変更はユーザー判断へ返す。
- profileを方針単体の判定正本、matrixを派生した横断viewとし、summary・comparisonを下位の判定と一致させる。
- 設計内容、現時点の利用可能性、検証根拠を区別して比較する。
- このリポジトリの役割を現在どこまで果たせるかを主評価にする。
- 自己目的への適合は、不足理由、意図的な対象外、再利用可能な設計資産を説明する補助情報とし、現在の運用可能性や採用推奨を引き上げる根拠にしない。
- 対象が対応すると宣言する出口ごとに、運用能力とアウトプット品質を一組で評価し、どちらかの強さで他方の不足を相殺しない。
- アウトプット品質は、意思決定可能性、具体性と境界、整合性と追跡可能性、根拠の十分性と確度、次行動の実行可能性で評価する。
- `build`、追加検証、既存手段の利用、保留、停止で、共通する品質観点を維持しつつ最低アウトプット契約を変える。
- 設計上狙う品質、現在の運用成果物から期待できる品質、実出力で観測した品質を区別する。
- 現在の採用可否と主要な次判断はrouting gate、未成立内部を含む質の差はquality profileで示す。
- quality profileはQ1〜Q15を、設計内容、現時点の利用可能性、実測支持ごとに `欠落`、`断片`、`具体化`、`成立`、`未確認`、理由・代替物付きの `非該当` で記録する。
- `限定成立` を判定語に使わず、結論の適用範囲を別の必須欄へ記録する。
- 深さを数値化・合計・平均せず、成立範囲、blocking gap、改善余地、根拠を残す。
- 未確認のQ条件と主要な次判断から必要な観測を逆算し、固定資料、保存済み実行、補助tool、新規ケース実行の順に最小の追加観測だけを行う。
- 保存済み実行を実測支持へ使う場合は、対象版、入力、担当・方法・介入、実出力、review・改訂・再確認、出口・適用範囲のうち結論に必要な来歴を追えることを要求し、欠落を推測で補わない。
- 新規実行は実測の未確認が主要な次判断を変え、資料照合では解消できない場合に限定し、対象版、入力、出口、担当・介入、判定方法、上限・停止条件、原本を変えない実行場所と保存先を事前固定する。
- 共通入力による実行は、補完なしで実行できる同じ出口・適用範囲の対象間だけで行い、`feature-1` の未作成の運用成果物を比較者が補完して現在の原本として評価しない。
- 各方針をどの目的・前提なら次の採用検討へ進められるか、何を追加確認すべきかを比較結果から判断できるようにする。
- 比較資料の読み取りによって対象ブランチと現在の作業ブランチを変更しない。
- 事実、元資料の主張、今回の解釈、未確認事項を区別する。

### 非目標

- 現時点の依頼からは、各ブランチ成果物の改善実装・統合・公開を確定しない。扱いの境界は設計で明らかにする。
- 制作・評価条件が異なる3件から単一の勝者または純粋なモデル性能順位を確定しない。
- 資料から確認できない制作モデルの厳密な識別情報、人の関与、コスト、成功率を補完しない。

### 受け入れ基準

- 比較結果の主結論から各方針が現在果たせるリポジトリの役割、採用検討へ進める条件、不足と次の検証を追え、自己目的への適合がその結論を上書きしない。
- 運用能力とアウトプット品質の各観点から、設計の補完、運用成果物の作成、追加検証、改訂後の再検証、条件付きの採用検討のいずれかを導ける。
- 同じrouting gateまたは主要な次判断になる案同士でも、Q1〜Q15のprofileから、成立している能力、その深さ、blocking不足、改善余地の差を読める。
- 根拠種類ごとに支持可能な主張範囲を区別し、保存済み実行の来歴不足を推測で補わず、元資料の評価主張と今回の独立確認を混ぜずに各Qの判定と限界へ戻れる。
- 新規観測の有無について、どの `未確認` と主要な次判断のために必要か、または既存資料で止めた理由を説明できる。新規実行した場合は、事前契約と失敗を含む結果を追える。
- `comparison.md` からcurrent snapshotの結論、各profile、matrix、各Qの根拠へ到達でき、manifest、summary、matrix、profile、evidence-index間でtarget、判定、適用範囲、主要な次判断が矛盾しない。
- 3targetの全tracked entryについてsource copyのpath・type・mode・object ID・sizeが固定commitと一致し、欠落・余分・内容不一致がなく、固定資料の全evidenceをsnapshot-local pathとblob IDへ戻せる。
- `feature-3` のsymlinkがdereferenceされず、新規runの前後でsource inventory hashが変わらない。
- 訂正が必要な場合に旧complete snapshotを変更せず、最上流の誤りから全派生結果を新snapshotで再生成し、current切替前後のhistoryとknown issueを追える。
- source defect、judgement defect、新証拠または新targetの各caseを、invalidatedを伴う訂正、通常のsupersede、追加比較へ誤りなくrouteできる。
- 第四案を仮定しても既存3案のprofileとbaseline snapshotを上書きせず、追加結果を置ける。
- `feature-3` と `feature-7`、かつ build と非buildの異なる出口へ判断基準を適用し、成果物構成に依存せず、期待品質と実測品質を混ぜずに主要な次判断を導けることを確認する。
- `comparison.md`、snapshot manifest、source provenance・inventory、evidence-indexだけからcurrentの対象版・method・根拠範囲を再確認でき、追加依頼をsame/new steering、target差、再評価Q、最小観測へ分類できる。
- 第四案、既存branch新版、同commitの新run、semanticなmethod変更、受付不能、別目的を同じ規則でrouteでき、全targetから派生viewを再生成できる。

## リスクと対策

| リスク | 設計で確定すべき対策 |
| --- | --- |
| 骨格設計と実行可能な運用成果物を同じ完成基準で順位付けする | リポジトリの役割への適合を主評価にし、自己目的への適合は不足理由と再利用可能な設計資産を説明する補助情報に限定する |
| 運用の仕組みが整っているだけで、浅い・矛盾したアウトプットを採用可能と扱う | 運用能力と出口成果物品質を一組で評価し、期待品質と実測品質を区別する |
| build用の成果物量で非build出口を低品質と判定する | 共通の品質五観点を維持しつつ、出口別に最低アウトプット契約を変える |
| 一つのblocking不足がある案と、ほぼ何も成立していない案を同じ未成立として質の差を失う | routing gateとquality profileを分け、Q1〜Q15の成立範囲・深さ・改善余地を根拠付きで残す |
| ブランチに付けたモデル名から、そのブランチのすべての判断・評価を同じモデルへ帰属させる | 制作条件と評価実行条件を分け、版・入力・担当・介入を追える範囲だけに主張を制限する |
| 元資料の成功主張や構造検査を、出口成果物の意味品質の実証として扱う | 元資料の主張、今回の独立評価、補助tool、新規実行を分け、実出力を確認できるQだけを実測支持にする |
| 根拠量を揃えるため不要な共通実行を行い、未完成案を比較者が補完して別物を評価する | Q条件と次判断から最小観測を逆算し、補完なしで同じ出口・適用範囲を持つ対象間だけ共通実行する |
| ブランチの更新・削除で比較結果と根拠がずれる、または原本本文を失う | target IDとfull commitで時点を固定し、全tracked treeをGit identity検証済みの不変source copyとしてsnapshotへ保存する |
| 原本copyへannotationやrun出力が混ざり、比較前の成果物と今回生成物を区別できない | sourcesを完成後不変とし、実行は隔離copy、生成物はrunsへ分離して前後hashを確認する |
| 完成後にprofileやsummaryだけを直接直し、過去判断と派生fileの整合を失う | complete snapshotを不変にし、上流原因から自己完結した訂正snapshotを再生成して最後にcurrentを切り替える |
| 重大な誤りを訂正中も旧結論が無警告で使われる | blocking known issueを入口に即時表示し、source identity・完全性の欠陥なら旧currentをinvalidatedにする |
| 3例に合わせて作った比較形式が将来例を扱えない | 第四案、既存branch新版、同commitの新run、semanticなmethod変更、受付不能、別目的のcaseでidentity、steering境界、再評価範囲、派生view再生成を検証する |

## テスト方針

この初稿では application の test command を定めない。repository 固有のテスト方針は確認できていない。

- 設計前調査は、固定コミットに対する読み取りで根拠を再確認する。
- 合意した判断基準を `feature-3` と `feature-7`、かつ build と非buildの異なる出口へ適用し、判定語、閾値、次判断の導出を検証する。
- `feature-3` の保存済みrunは最低来歴条件を満たすQだけに使い、実出力の独立評価と元資料の成功主張を分けられるか確認する。
- `feature-7` は固定資料による設計・利用可能性の判定と実測支持を分け、構造検査を意味品質へ昇格させず、採用判断を変える未確認だけを新規実行候補にできるか確認する。
- 共通ケースを実行する場合は、補完なし、同じ出口・適用範囲、事前に固定したQ条件と実行契約を満たすことを確認する。満たさなければ実行せず、その理由と比較可能範囲を記録する。
- `comparison.md` からsummary、profiles、matrix、evidence-indexへ到達できること、target・判定・適用範囲・次判断のfile間整合を確認する。
- 全source entryのpath・type・mode・object ID・sizeを固定commitと照合し、欠落・余分・不一致0件を確認する。`feature-3` の3symlinkはrelative targetを維持する。
- profileの固定資料evidenceをすべてsnapshot-local source pathとblob IDへ戻し、新規runの前後でsource inventory hash不変を確認する。
- `feature-3` のsymlink capture defectと `feature-7` の構造check過大評価を仮定し、旧snapshot不変のまま上流原因から訂正snapshotを再生成できることを確認する。
- 新しい第四案または新runを訂正として扱わず追加比較へrouteし、訂正版complete前のcurrent切替、blocking issueの無警告残置、旧snapshot hash変化を検出する。
- 仮定した第四案を `002-add-<target-slug>` へ追加し、同一性を再確認した既存Qだけをcarry forwardして、4案すべてからmatrix・summaryを再生成できることを確認する。
- `feature-7` の新commitを新target、同commitの新runをrecheck、semanticなmethod変更を影響Qの全target再評価へrouteし、method対応不能・source保存不能・別目的はcurrentを変えず停止または別steeringへ送れることを確認する。
- comparison ID再利用、alias branchによるtarget重複、根拠のないcarry forward、新target追加後も旧3案のままのsummary、別steeringからのcurrent変更を失敗として検出する。

## （付録）前提とする既存仕様

- 現在のブランチは `feature-9`。開始時の HEAD は `a9c0efba2646b46d6f6c8e78c9ffa3f965431b3c` で、追跡対象は `.gitignore` と `README.md` の2件。`README.md` の本文はリポジトリ名のみ。
- `.agents/skills/tumeda-dev-plugin-context.md` は存在せず、この作業に適用する repository 固有の設計文書・規約・テスト command は確認できていない。比較対象ブランチの指示文を現在の作業規約へ転用しない。
- 設計に影響する既存成果物の構成と制作・評価条件は [investigation.md](./investigation.md) に記録した。元ブランチの全文評価はまだ行っていない。

## （付録）変更の実行区分

### task-design内で対象成果物へ適用済み

なし。`design.md` と discussion の lifecycle 更新、設計前調査の記録だけを行っている。

### task-design内の対象成果物反映待ち

なし。反映内容が確定した対象成果物はまだない。

### execution plan対象

なし。調査量やファイル数だけを理由に tasklist または roadmap を作らない。

### 分類保留（設計中のみ）

| 変更候補 | 保留理由 | 分類を確定するdecision |
| --- | --- | --- |
| 最終比較結果と追加比較のための記録 | 追加フローが未合意 | target受付、採番、既存target再評価、同じ/別steeringの境界 |
