<a href="https://animations.dev/">
<img width="320" height="168" alt="opengraph-image-pwu6ef" src="https://github.com/user-attachments/assets/a405a37f-1a1a-4e8d-8fd6-269ee6d4fba6" />
</a>

[English](./README.md) | [简体中文](./README.zh-CN.md) | [日本語](./README.ja.md)

# デザインエンジニア向けスキル

[![skills.sh](https://skills.sh/b/emilkowalski/skills)](https://skills.sh/emilkowalski/skills)

デザイナーやエンジニアが、より優れたユーザーインターフェースを構築するためのスキルです。

アニメーションやデザイン全般について、正しい選択ができたかどうかを判断するのは簡単ではありません。これらのスキルは、正しい判断へより早くたどり着けるようにすることを目的としています。

これらは、Vercel や Linear などの企業で働いてきた私の長年の経験に基づいています。

ここにあるすべてのスキルは、分野に関する専門知識から生まれた副産物です。AI はそのような専門知識に取って代わるものではありません。専門知識から引き出せる価値を増幅し、周囲と比べてあなたの能力を大きく高めてくれます。

ですから、コーディングやデザインを学ぶ、あるいはほかの分野で専門性を磨いてください。それらは非常に価値のあるものです。

私のスキルに関する最新情報は、こちらで受け取れます。

[ニュースレターに登録](https://animations.dev/skills)

## インストール

```bash
npx skills@latest add emilkowalski/skills
```

## なぜ使うのか？

エージェントには優れた審美眼がありません

エージェントがアニメーションに適した要素を選べない場面を、私は何度も見てきました。本来 `ease-out` を使うべき登場アニメーションに `ease-in` イージングを使うことがあります（[その理由はこちら](https://emilkowal.ski/ui/7-practical-animation-tips#4.-choose-the-right-easing)）。また、半透明のシャドウではなく、単色の境界線を選ぶこともあります。

こうした小さな要素が積み重なり、インターフェースは素晴らしいものになるか、あるいは……今ひとつのものになります。

[Agents with Taste](https://emilkowal.ski/ui/agents-with-taste) で説明しているように、これらのスキルは、エージェントが犯す可能性のある細かな間違いをすべて挙げ、その修正方法を説明します。

これは、優れたインターフェースを作るための近道です。粗製濫造されたものがあふれる中で、ひときわ目立つための近道でもあります。

## リファレンス

- **[emil-design-eng](./skills/emil-design-eng/SKILL.md)** — 主にアニメーションについて扱い、デザインに関するアドバイスも含む中心的なスキルです。
- **[review-animations](./skills/review-animations/SKILL.md)** — 私のルールに基づいて、アニメーションを厳しくレビューします。
- **[improve-animations](./skills/improve-animations/SKILL.md)** — コードベース内のすべてのアニメーションを監査し、どのエージェントでも実行できる、優先順位付きの自己完結した計画を作成します。
- **[find-animation-opportunities](./skills/find-animation-opportunities/SKILL.md)** — UI の中でモーションが本当に効果を発揮する場所を探しつつ、アニメーションを付けるべきでないものも示します。
- **[animation-vocabulary](./skills/animation-vocabulary/SKILL.md)** — 適切な言葉で要望を正確に伝え、AI からより優れたアニメーションを引き出します。
- **[apple-design](./skills/apple-design/SKILL.md)** — Apple の WWDC デザイントークから抽出したインターフェースデザインと滑らかな動きの原則を、Web 向けに翻訳・再構成したものです。
- **[pick-ui-library](./skills/pick-ui-library/SKILL.md)** — AI に toast コンポーネントを一から作らせたり、放棄されたパッケージをインストールさせたりせず、私が使用し信頼しているライブラリを基に、エージェントがタスクに適したライブラリを選べるようにします。

### アニメーションを改善する

[shadcn/improve](https://github.com/shadcn/improve) から着想を得ています。最も高性能なモデルを使ってプロジェクト内のアニメーションを監査し、その実行をより低コストのモデルに引き継ぎます。
`improve-animations` はコードベース全体（単一の diff ではありません）を調査し、8 つのカテゴリー（目的と頻度、イージングと時間、物理的な動き、中断可能性、パフォーマンス、アクセシビリティ、一貫性、見逃している改善機会）にわたって監査したうえで、優先順位付きの指摘事項を表で提示します。対応したい項目を選ぶと、自己完結した計画を `plans/` に書き出します。計画には、対象ファイル、具体的な曲線、正確な時間、感触の確認項目が含まれているため、別のエージェントが背景知識や独自の審美眼なしで実行できます。このスキル自体がソースコードに手を加えることはありません。

```
> improve the animations in this codebase
> improve-animations quick        # hotspots only
> improve-animations performance  # one category
> improve-animations plan add press feedback to all buttons
> improve-animations execute plans/001-fix-dropdown-easing.md
```
