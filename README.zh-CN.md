<a href="https://animations.dev/">
<img width="320" height="168" alt="opengraph-image-pwu6ef" src="https://github.com/user-attachments/assets/a405a37f-1a1a-4e8d-8fd6-269ee6d4fba6" />
</a>

[English](./README.md) | [简体中文](./README.zh-CN.md) | [日本語](./README.ja.md)

# 面向设计工程师的技能

[![skills.sh](https://skills.sh/b/emilkowalski/skills)](https://skills.sh/emilkowalski/skills)

帮助设计师和工程师构建更出色的用户界面。

无论是动画还是整体设计，要判断自己是否做出了正确的选择都很困难。这些技能旨在帮助你更快地做出正确决策。

它们源自我在 Vercel、Linear 等公司多年的工作经验。

这里的所有技能都是领域专业知识的衍生产物。AI 不会取代这种专业知识，而是会放大它所能带来的价值，让你相较他人获得显著提升。

因此，请学习编程、设计，或在其他任何领域培养专业能力。这些能力极其宝贵。

你可以在这里持续了解我的最新技能：

[订阅新闻通讯](https://animations.dev/skills)

## 安装

```bash
npx skills@latest add emilkowalski/skills
```

## 为什么要使用它？

智能体并不具备出色的审美判断

我见过许多这样的情况：智能体无法为动画选对元素。例如，本应使用 `ease-out` 的入场动画却采用了 `ease-in` 缓动（[原因见此](https://emilkowal.ski/ui/7-practical-animation-tips#4.-choose-the-right-easing)）；又或者，它们会选择实线边框，而不是半透明阴影。

所有这些细节叠加起来，最终会让你的界面要么令人惊艳，要么只是……不尽如人意。

正如 [Agents with Taste](https://emilkowal.ski/ui/agents-with-taste) 中所述，这些技能列出了智能体可能犯下的所有细微错误，并说明如何修正它们。

这是你打造出色界面的捷径，也是在粗制滥造的内容浪潮中脱颖而出的捷径。

## 参考

- **[emil-design-eng](./skills/emil-design-eng/SKILL.md)** — 核心技能，主要涵盖动画，同时也提供一些设计建议。
- **[review-animations](./skills/review-animations/SKILL.md)** — 根据我的规则，以严格的方式审查你的动画。
- **[improve-animations](./skills/improve-animations/SKILL.md)** — 审核代码库中的所有动画，并生成按优先级排列、内容自洽且任何智能体都能执行的计划。
- **[find-animation-opportunities](./skills/find-animation-opportunities/SKILL.md)** — 在你的 UI 中寻找真正适合加入动效的位置，同时指出哪些内容不应添加动画。
- **[animation-vocabulary](./skills/animation-vocabulary/SKILL.md)** — 使用准确的词语清楚表达需求，从而让 AI 生成更好的动画。
- **[apple-design](./skills/apple-design/SKILL.md)** — 从 Apple 的 WWDC 设计演讲中提炼界面设计与流畅动效原则，并将其转化为适用于 Web 的内容。
- **[pick-ui-library](./skills/pick-ui-library/SKILL.md)** — 让智能体根据我使用并信任的库为任务选择合适的方案，而不是让 AI 手写一个 toast 组件或安装已经弃用的软件包。

### 改进动画

受 [shadcn/improve](https://github.com/shadcn/improve) 启发：使用能力最强的模型审核项目中的动画，再将执行工作交给成本更低的模型。
`improve-animations` 会检查整个代码库（而不只是单个 diff），从八个类别进行审核（目的与频率、缓动与时长、物理感、可中断性、性能、无障碍、连贯性以及错失的改进机会），并展示一张按优先级排列的问题表。选择你想处理的问题后，它会把内容自洽的计划写入 `plans/`，其中包含确切的文件、曲线、时长以及体验检查，另一个智能体无需任何背景信息或审美判断即可执行。它本身绝不会修改你的源代码。

```
> improve the animations in this codebase
> improve-animations quick        # hotspots only
> improve-animations performance  # one category
> improve-animations plan add press feedback to all buttons
> improve-animations execute plans/001-fix-dropdown-easing.md
```
