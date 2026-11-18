# 作る前提の再ドライランの実行条件

- build_policy: require-build（三件とも）
- 指定の出典: 利用者の「そのあと作る前提でもう1回ドライラン回そう」。記録の反映後に別のCodex processで試す具体案へ、利用者が「ok」と応答した。
- 入力: inputs.mdの三件。assistantが用意した架空の設定で、実際の利用者の経験/採用や実利用の結果ではない。元の設定を変更して通過させない。
- 実行範囲: レールを使った判断/設計と必要な局所の技術probe。製品本体の実装/導入/実利用、購入/外部への連絡/新規契約、commit/pushを含めない。
- 作ること自体の望みや費用上限などの事実を追加しない。制作規模/手段は探索する。成立しない時は不足と復活条件を残して保留出来る。
- 使用するshared skillのread-onlyの実体: /workspace/.cache/grow-product-ideas/plugins/tumeda-dev/plugins/tumeda-dev（8.2.5）。この写しの通常のplugin読込みと異なるなら、その差を実行結果へ残す。共有cacheは編集しない。
- 操作対象: この検査用workspaceのみ。元repositoryの会話/過去のCの成果/steeringは読まず編集しない。検査設定に無い実際の事実が要る時は創作で埋めない。
