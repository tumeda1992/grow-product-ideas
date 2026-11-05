# 内部検討記録: 論点13 — 確かめること自体が規約・安全に触れる技術検証

**discussion:** [implementation_review.md](../implementation_review/implementation_review.md)

**論点:** 論点13

## 開始context

Kindleの件で、ハイライトの読み取りを確かめるには、ログインが要るページを自動で読む必要があり、規約に触れうる。verify-technical-feasibilityに、確かめる行為のリスクを見る手順が無い。

<a id="iteration-0"></a>

## イテレーション0: どこで見るか

| 案 | 評価 |
| --- | --- |
| 材料skillが動かす直前に見て、触れるなら動かさず返す | 動かす主体が見られる。最終判断は利用者へ |
| settle-questionが起動前に見る | 何を動かすかは材料skillが決めるため、見落とす |
| risks-of-buildingの問いで扱う | 作った後のリスクの問いであり、確かめる時点で起きる損害を防げない |
