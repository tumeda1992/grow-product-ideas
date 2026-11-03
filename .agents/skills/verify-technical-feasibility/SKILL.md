---
name: verify-technical-feasibility
description: 動かさないと分からない技術的な不確実性（外部APIの挙動、一番難しいロジックの実現性、環境依存の動作）を、最小限のcodeを書いて確かめ、得た事実を材料（technical-feasibility）に残す材料skill。`settle-question`から起動される。
---

# verify-technical-feasibility

材料`technical-feasibility`を作る。受け取るもの、粒度、再利用は`what-defines-a-product/README.md`の「材料」節に、置き方と入口の形は`product-plans/README.md`に従う。

`tumeda-dev`の`task-design`が技術検証に使う`spike/`と同じ考え方を、アイデアの段階で使う。書いたcodeは本実装ではなく、残すのは確かめた事実である。

## 作る手順

1. 要求元の問いから、何が分からないのかを一つの問いにする（例: この外部APIは、無料枠で一日に何件取れるか）。
2. 議論や調べ物で分かるなら、codeを書かずに調べて事実を書く。動かさないと分からない時だけ、次へ進む。
3. 確かめるための最小限のcodeを、材料の入口と同じdirectoryの下に書いて動かす。秘密情報（APIの鍵等）はfileへ書かず、環境変数で渡す。
4. 確かめた事実、確かめた方法、動かした環境、確かめきれなかった範囲を入口に書く。
5. 一番難しい部分が実現できないと分かった時は、回避案（`core-logic`にある時はそれ）でなら実現できるかも書く。

技術的な不確実性が無いと判断した時も、無いと判断した理由を入口に書く。

## 持たないもの

本実装を書くこと。確かめるためのcodeは、確かめた事実を得たら役目を終える。動いたcodeを本実装の土台として育てない。
