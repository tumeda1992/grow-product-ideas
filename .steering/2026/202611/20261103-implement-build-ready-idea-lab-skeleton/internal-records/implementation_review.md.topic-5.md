# 内部検討記録: 論点5 — 決定過程の論点の単位

**discussion:** [implementation_review.md](../implementation_review/implementation_review.md)

**論点:** 論点5

## 開始context

利用者の指摘「論点は問いごとじゃない」「並べる順は時系列に決まってんだろ」を受け、決定過程の論点の単位を見直す。

<a id="iteration-0"></a>

## イテレーション0: 論点の単位

<a id="iteration-0-record-1"></a>

### 調査: 「問いごとに一つの論点」の出所

- 設計の論点10の決定: 「問いごとに一つの論点を立て、層skillが答えを提案として保存し……層の閉じのユーザー確認gateで、ユーザーがその層の論点群へ応答し、合意した時点で決定になる」
- `settle-question/SKILL.md`手順4、`grow-product-idea/SKILL.md`手順5、design.mdの記録の置き場所の表に同じ前提がある。
- `facilitate-discussion`の論点: 「decisionは、ユーザーが採否を決める問いと、その結論の単位」。一部へ修正要求を出せることだけでは別decisionとみなさないが、別の問いへの答えなら分ける。

### 判断

論点は、問いのセットの構造ではなく、答える中で生じる判断ごとに立てる。一つの問いに複数の判断があれば複数、判断が無ければ立たない。起きた順に記録する。正本は根拠になった論点へlinkし、層の閉じでは立った未決の論点を示す。
