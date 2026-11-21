# アイデアをbuild-readyまで詰めるレールの全体レビュー

2026年11月21日。feature-16の `4b8dc31c0e8242bcda6fd2a2746b25e997b23243` を対象に、Astra（gpt-6.2-astra、xhigh）で `exhaustive-review` を実施した。対象は入口、四層、専門への依頼と返り、記録、保留・再開、初回構築への受渡し。挙動を変える改善を含む。レビュー時点では採否・適用は未実施。[検査の範囲と証拠](coverage.md)

現在の適用状況: CR-009・CR-008・CR-001・CR-002・CR-003は合意・適用・検証済み。他の11件は未採否。[適用記録](application.md)

## 結論

**替芯のhowで止まった判断は妥当。それだけでは、そこまでのwhy・whatや、止まった後の進め方は合格にならない。** 指定された初回の案件には、実店舗との対応も替芯の品番・包装写真もなく、技術検査は0件だった。条件を満たした案を創作しなかったことは確認できる。一方、最初の望み「寄り道を減らす」が、期限内に得る道を選ぶ目標と競合するときの扱いは選ばれていない。whatの4×4表は条件違反を「全て真の反例」に混ぜて一度合格し、出口で訂正された。品番だけ先に届いた場合に進める枝も、案件全体の復活条件に埋もれる。[指定案件を追った記録](coverage.md#替芯の案件で確認したこと)

**「日」は一般の反例の単位にはならない。** 問いの核は「全条件が真でも、約束した変化が偽になる具体例は何か」。二音の同時出力、複数回を通した偏り、二人の操作順では観察の単位が違う。現行は四方向を手がかりと呼びながら、言い分との全ての枡を完了条件にしている。また、この検査だけでは、同じ価値に届く別の証明方法を締め出した余計な条件を取り除けない。[CR-004](findings/CR-004-counterexample-unit.md)・[CR-005](findings/CR-005-necessity-of-conditions.md)

**1000字の依頼を扱えるとする根拠は足りない。** 現行whyには複数の目標を育て、両立・競合、失う価値を比べて本人が選ぶ方法がある。抜けるのは、その比較に載せ忘れた原文の約束、適合する過去の体験がない夢、手段の比較結果によって初めて順位を選べる目標である。長文の実試運転は行っていない。[異なる二種類の入力と後日の合否](coverage.md#長い依頼と長いwhyをどう判定するか)

**先に変えるのは、書類の量より判断の順序と責任である。** 原文から「守る約束」「まだ選ぶ価値」「制約」を取り出し、結論が変わる問いだけを先に調べ、利用者が今回の目的と損失を選ぶ。howでは局所で選んだ案を実際に組んで、その版で費用・担い手・利用者の価値が成立するかを引き受ける。build-readyはここまでの同意に加え、受け手が具体入力から結果と復旧を辿れる状態を要する。設計判断が十分に具体的な既存例はあるが、新しいリポジトリで初回構築まで成功したことは本レビューの証拠に含まない。[CR-003](findings/CR-003-conditional-goal-order.md)・[CR-006](findings/CR-006-positive-value-in-selection.md)・[CR-007](findings/CR-007-assembled-version-budget.md)・[CR-011](findings/CR-011-authority-after-copy.md)

## 優先順

1. 受け入れ前の正本参照と、未閉じのまま保留に入る経路を直す。通常入口と正当な停止の両方で、現行の指示が矛盾する。[CR-009](findings/CR-009-unaccepted-section-reference.md)・[CR-008](findings/CR-008-pause-and-resume-transitions.md)
2. 長文を試す前に、原要求の脱落、未来仮説、条件付きの目標選択を識別する。四方向を増やすことによる代用は避ける。[CR-001](findings/CR-001-unaccounted-input.md)・[CR-002](findings/CR-002-unexperienced-aspiration.md)・[CR-003](findings/CR-003-conditional-goal-order.md)・[CR-004](findings/CR-004-counterexample-unit.md)
3. 採用する版全体で、得られる体験と予算・負担が両立することを確かめる。[CR-006](findings/CR-006-positive-value-in-selection.md)・[CR-007](findings/CR-007-assembled-version-budget.md)
4. 証拠の取り方、候補別の復活、保守・後続への引渡し、案件の識別と検査結果を揃える。残る個別指摘は下表で採否を判断できる。

## 指摘索引

P1は主要な入力・出口の進行又は製品の目的・採否を壊すもの、P2は特定の条件で正しい候補・判断記録・引継ぎを失うものとした。16件中P1は7件、P2は9件。レビュー時点ではいずれも未採否。現在値は上の適用記録を参照する。

| ID | 優先度 | 起きること |
| --- | --- | --- |
| [CR-001](findings/CR-001-unaccounted-input.md) | P1 | 原文を保存しても、候補にし忘れた要求が消えたままwhyを閉じられる |
| [CR-002](findings/CR-002-unexperienced-aspiration.md) | P1 | 目標選択に使える過去の体験がないと、未来の仮説を選んでもwhyを閉じられない |
| [CR-003](findings/CR-003-conditional-goal-order.md) | P1 | 実現の見込みで優先が変わるとき、比較前に目標を一つ閉じる順序が循環する |
| [CR-004](findings/CR-004-counterexample-unit.md) | P2 | 反例の単位と探索の打ち切りを、家族の一日と四方向に固定している |
| [CR-005](findings/CR-005-necessity-of-conditions.md) | P2 | 一つの証明手段を必要条件にしても、十分性の反例では外せない |
| [CR-006](findings/CR-006-positive-value-in-selection.md) | P1 | 作る理由を二種類に限定すると、新しく可能になる利用体験を採用理由に書けない |
| [CR-007](findings/CR-007-assembled-version-budget.md) | P1 | 補う点を個別に選んだ後、実際に組み合わせた版の予算と同時成立を確定しない |
| [CR-008](findings/CR-008-pause-and-resume-transitions.md) | P1 | 未閉じで正式保留する入口と、保留・非開発を再開する分岐が進行手順にない |
| [CR-009](findings/CR-009-unaccepted-section-reference.md) | P1 | 最初の層の閉じを提案する前に、受け入れ後にしか作れない正本の節を検査する |
| [CR-010](findings/CR-010-feedback-after-stalls.md) | P2 | 停止理由を正しく記録できても、停止までに見送った目標・未検査の経路が保守に届かない |
| [CR-011](findings/CR-011-authority-after-copy.md) | P2 | 初回構築で選定を変える差が出た時、原案件と持出し先のどちらを更新するか決まらない |
| [CR-012](findings/CR-012-distinct-rules-same-placement.md) | P2 | 担い手・置き場所・制作有無が同じでも、受益者が違う対案を除いてしまう |
| [CR-013](findings/CR-013-quoted-reference-definition.md) | P2 | 引用内の参照定義を見落とし、壊れた出典を0リンク・正常で渡せる |
| [CR-014](findings/CR-014-revalidated-state.md) | P2 | 差し戻し後に『変わらない』と判断した層を、閉じた状態へ戻す手順がない |
| [CR-015](findings/CR-015-candidate-specific-unblocking.md) | P2 | 商品同定と店舗同定を一括の復活条件にすると、先に調べられる候補まで止まる |
| [CR-016](findings/CR-016-plan-identity-collision.md) | P2 | 同じ日に同じslugとなる新規案件を、既存案件と区別する責任が抜けている |
