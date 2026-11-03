---
name: compare-build-and-alternative-costs
description: 作る費用（作る時間と保守し続ける時間）と、代案を使い続ける費用（代金と残る手間）を同じ尺度へ揃えて比べた材料（cost-comparison）を作る材料skill。`settle-question`から起動される。
---

# compare-build-and-alternative-costs

材料`cost-comparison`を作る。受け取るもの、粒度、再利用は`what-defines-a-product/README.md`の「材料」節に、置き方と入口の形は`product-plans/README.md`に従う。

## 作る手順

1. 比べる対象を決める。要求した問いによって対象が違う。
   - `why-to-build/build-cost-pays-off`: 作る案と、`existing-alternatives`の主な候補
   - `what-to-build/scope-in-and-out`: スコープの案ごと
   - `how-far-to-build/first-build-cut`: 区切りの案ごと
2. 作る時間を見積もる。`experience-sketch`の画面の枚数と主要な操作の数から、過去に作ったものと比べて出す。`experience-sketch`が無い、または粒度が足りない時は、`settle-question`へ返す。
3. 作った後に保守し続ける時間を見積もる。依存先の変更への追従、不具合の修正、データの手当てを入れる。
4. 代案の費用を出す。代金と、代案で残る痛みに使い続ける手間の時間を出す。
5. 全てを同じ尺度に揃える。

## 同じ尺度へ揃える

- 既定は時間に揃える。個人開発では使える時間が一番の制約であり、実感に合いやすい。
- 代案の代金が大きい時は、自分の時間を時給で金額に換算し、金額に揃えた比較も添える。
- 長く使う見込みがある時は、何か月・何年で作る方が安くなるか（逆転点）を出す。

作ること自体の楽しみや学びの価値は、費用に混ぜない。混ぜると比較にならない。

## 落ちる精度

心臓部のロジックの難しさを過小評価しやすい。`technical-feasibility`がある時は、それを見積りに反映し、無い時はその旨を「確かめた方法と限界」に書く。
