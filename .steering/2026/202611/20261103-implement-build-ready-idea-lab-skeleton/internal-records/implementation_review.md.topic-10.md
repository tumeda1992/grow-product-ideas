# 内部検討記録: 論点10 — 問いの進行と決定過程を、層ごとのdirectoryにまとめるか

**discussion:** [implementation_review.md](../implementation_review/implementation_review.md)

**論点:** 論点10

## 開始context

論点3で決定過程を層ごとの記録`<層>-discussion.md`にし、論点9で問いの進行を`questions/`に索引と問いごとのfileで置くと決めた。利用者から、層のdirectoryに決定過程と`questions/`が並ぶ形とどちらがよいかを問われた。

<a id="iteration-0"></a>

## イテレーション0: 二つの配置の比較

<a id="iteration-0-record-1"></a>

### 判断

層の閉じ、後続、還元は層を単位に読み、問いのセットとgateも層単位である。種類ごとに分けると同じ層を二か所で突き合わせる。層ごとにまとめると、全体の索引を失うが、`grow-product-idea`が四つの層のREADMEを読む手間は小さく、広がった視野は層を上から読めばほぼ起きた順になる。内部検討記録も層ごとに分かれる。推奨は層ごと。materialsは層をまたいで使うため直下。記録名は`discussion.md`。
