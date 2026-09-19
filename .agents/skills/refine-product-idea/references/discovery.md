# Discovery phase

## Outcome

`discovery.md`だけを読んだ人が、誰のどの状況の何を解くか、現在どう対処され、どの主張にどれほど根拠があるかを判断できる状態にする。

## Procedure

1. `source.md`から、明示された事実とエージェントの解釈を分ける。
2. 解決策を隠した問題文を仮に作り、その答えが元の製品以外でも成立するか確認する。
3. trigger、desired progress、current journey、frictionを具体例で通す。
4. Webまたはrepository調査が使える場合は、競合名の収集より先に現在行動を示す証拠を探す。公式仕様、価格、公開データ、実際のreview・issueなど、主張に近いsourceを優先する。
5. current alternativeを `do nothing | manual | configure | buy | assemble | build` の視野で探す。
6. 問題が起きないcounterexampleを探し、対象segmentの境界を修正する。
7. 各claimへE0〜E4を付け、source、観測日、適用範囲、反証を記録する。
8. 追加調査がverdictを変えなくなった時点で止め、問題を一段落で再定義する。

## Individual-developer adaptations

直接インタビューができないことを、架空のpersonaで補わない。自分専用なら自身の行動ログをE3相当として扱えるが、他者へ一般化しない。他者向けなら公開された過去行動をE1として使い、導入・支払・継続は未検証と残す。

調査を続ければいつか確信できるという前提を置かない。E2以上が必要な仮説は、実行可能なexperimentへ変換する。

## Adversarial checks

- そのpersonaは、名前を別の製品へ置き換えても成立する一般人になっていないか。
- painを表す値はsourceがあるか。無ければ架空の精度を与えていないか。
- 競合が存在することを需要の証明にしていないか。
- 発言やreviewを、実際の行動・支払いと同じ強さにしていないか。
- 元の製品を消しても、解くべき問題が独立して残るか。
- 問題のないcaseを見た結果、segmentまたはproblem statementが変わったか。
