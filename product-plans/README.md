# product-plans

アイデア1件ごとに1directoryを持つ。レールを通したアイデアの判断記録の堆積である。

このREADMEは、`product-plans/<slug>/`の中の配置と名前、材料の入口の形を定める唯一の場所である。
各skillは、正本・決定過程・材料の入口を、file名ではなく役割で参照し、場所はこのREADMEで引く。

## 配置

```text
product-plans/<slug>/
├── README.md                 # 正本
├── discussion.md             # 決定過程（facilitate-discussion が作る）
├── internal-records/         # 決定過程の内部検討記録（facilitate-discussion が作る）
└── materials/
    └── <材料の識別子>/
        ├── README.md         # 材料の入口
        └── ...               # 付随file。分け方は材料skillが分量に応じて決める
```

| 役割 | 場所 | 作る担当 | 形 |
| --- | --- | --- | --- |
| 正本 | `product-plans/<slug>/README.md` | `grow-product-idea`（受け入れ時） | `grow-product-idea`の雛形 |
| 決定過程 | `product-plans/<slug>/discussion.md` | `settle-question`が`facilitate-discussion`で作る | `facilitate-discussion`の形式 |
| 材料の入口 | `product-plans/<slug>/materials/<材料の識別子>/README.md` | 材料skill | [材料の入口の形](#材料の入口の形) |

slugは`YYYYMMDD-`で始まる。

### 名前と構成が仮置きであること

正本と材料の入口の名前、正本を1fileにする構成は仮置きである。
アイデアを実際に通す中で、正本や材料が読み書きしにくい分量になった時に見直す。見直しは`refine-what-defines-a-product`の対象である。
見直す時は、このREADMEと正本の雛形だけを直す。各skillは役割で参照しているため、skillの本文は直さない。

## directoryの中だけで読み切れるようにする

`product-plans/<slug>/`は、build-readyになると写しが新しいリポジトリへ持っていかれ、初回構築の入力になる。後続のリポジトリには`what-defines-a-product/`もこのリポジトリのskillも無い。
そのため、どの出口でも、作る時からdirectoryの中だけで読み切れるように書く。

- 正本の各問いには、identifierと一緒に問いの文面と、このアイデアでの問い（言い直した文面と基準）を書く
- 定石から選んだ時は、選んだ選択肢と比べた選択肢の中身を決定過程に書く。定石の名前だけで参照しない
- 外の資料は、要点を書いたうえで出典として示す
- linkは、このdirectoryの中（正本、決定過程、材料）だけに張る

`product-plans/<slug>/`は、出口に関わらず残す。後続へ渡す時も写しを持っていき、このリポジトリの`product-plans/<slug>/`は残す。

## 材料の入口の形

材料skillは、材料の入口を次の形で作る。

````markdown
# {材料の識別子}: {この材料が何かを一文で}

## 要求した問いと粒度

| 問いのidentifier | 問いの文面 | 求めた粒度 | この材料で満たしたか |
| --- | --- | --- | --- |
| `{identifier}` | {文面} | {粒度} | {満たした / 育て中} |

## 中身

{材料の本体。調査系は集めた事実と出典、生成系は全体を一度に並べた複数案。付随fileは同じdirectoryに置き、ここから参照する}

## 確かめた方法と限界

{どこを、どう調べたか、何を作って試したか。個人版の代替で落ちる精度、調べきれなかった範囲}
````

同じ材料が既にある時は新しく作らず、「要求した問いと粒度」に行を足し、既にある中身を消さずに足りない粒度の分を足す。
