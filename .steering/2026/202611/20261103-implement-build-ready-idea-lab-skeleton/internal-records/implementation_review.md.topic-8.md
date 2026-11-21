# 内部検討記録: 論点8 — 正本（プロダクトの説明）の中身の形式

**discussion:** [implementation_review.md](../implementation_review/implementation_review.md)

**論点:** 論点8

## 開始context

論点7で、正本をプロダクトを構成要素ごとに説明する文書にすると決めた。中身の形式を決める。

<a id="iteration-0"></a>

## イテレーション0: 見出し構成

<a id="iteration-0-record-1"></a>

### 判断: 問いの答えから構成要素を取り出す

四層の16問の答えが説明するものを、プロダクトの構成要素として並べた。

| 構成要素の節 | 決める問い |
| --- | --- |
| 解く痛み | why-to-build/pain-to-solve |
| 作る理由 | why-to-build/existing-alternatives-fall-short、build-cost-pays-off、reason-to-build-anyway |
| リスクと手当て | why-to-build/risks-of-building |
| 要求 | what-to-build/requirements |
| 解き方 | what-to-build/solution-shape |
| スコープの内と外 | what-to-build/scope-in-and-out |
| 最初に作る分 | how-far-to-build/first-build-cut |
| 運用で済ませること | how-far-to-build/handled-by-operation |
| AIに任せる範囲 | how-far-to-build/ai-autonomy-range |
| 体験 | how-to-build/experience |
| 画面 | how-to-build/screens |
| データ | how-to-build/tables |
| モジュール | how-to-build/modules |
| 後から返済する負債 | how-to-build/debt-to-repay-later |

「作る理由」だけが三問をまとめる。並びは問いの依存の順と一致するが、読む人の理解の順として選んだ。対応表は雛形のコメントに置き、層fileへは書かない。
