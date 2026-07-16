<a href="https://animations.dev/">
<img width="320" height="168" alt="opengraph-image-pwu6ef" src="https://github.com/user-attachments/assets/a405a37f-1a1a-4e8d-8fd6-269ee6d4fba6" />
</a>

# Skills For Design Engineers

[![skills.sh](https://skills.sh/b/emilkowalski/skills)](https://skills.sh/emilkowalski/skills)

For designers and engineers to help them build better user interfaces.

Knowing whether you made a right choice when it comes to animations, or design in general, is hard. These skills aim to help you get to those right decisions faster.

They are based on my years of experience working at companies like Vercel and Linear.

All the skills here are a side-effect of domain-expertise. AI doesn’t replace such expertise, it amplifies what you can get out of it and makes you way better relative to others.

So learn to code, design, or develop expertise in any other field. It’s extremely valuable.

You can stay up to date with my skills here:

[Sign Up To The Newsletter](https://animations.dev/skills)

## Install

```bash
npx skills@latest add emilkowalski/skills
```

## Why use it?

Agents don’t have great taste

I have seen plenty of times that agents don’t pick the right ingredients for an animation. An `ease-in` easing for an enter animation when it’s supposed to be `ease-out` ([here’s why](https://emilkowal.ski/ui/7-practical-animation-tips#4.-choose-the-right-easing)). Or they choose a solid border instead of a semi-transparent shadow.

All these little things compound and make your interface either amazing, or just... not that great.

As explained in [Agents with Taste](https://emilkowal.ski/ui/agents-with-taste), these skills list all the little mistakes agents can potentially make and explain how to fix them.

This is your shortcut to great interfaces. A shortcut to stand out in a sea of slop.


## Reference

- **[emil-design-eng](./skills/emil-design-eng/SKILL.md)** — The main skill that consists of mostly animation, but also some design advice.
- **[review-animations](./skills/review-animations/SKILL.md)** — Review your animations in a strict way, based on my rules.
- **[improve-animations](./skills/improve-animations/SKILL.md)** — Audit all the animations in your codebase and get prioritized, self-contained plans that any agent can execute.
- **[find-animation-opportunities](./skills/find-animation-opportunities/SKILL.md)** — Search your UI for places that would genuinely benefit from motion, while also telling you what not to animate.
- **[animation-vocabulary](./skills/animation-vocabulary/SKILL.md)** — Get better animations from an AI by telling it exactly what you want by using the right words.
- **[apple-design](./skills/apple-design/SKILL.md)** — Apple's principles for interface design and fluid motion, distilled from their WWDC design talks and translated for the web.
- **[react-native-motion](./skills/react-native-motion/SKILL.md)** — The animation philosophy translated for React Native (Reanimated + Gesture Handler), with exact RN values in [RN-STANDARDS.md](./skills/react-native-motion/RN-STANDARDS.md).
- **[review-animations-rn](./skills/review-animations-rn/SKILL.md)** — Review React Native animations against the same strict bar, in RN terms.

### Improve animations

Inspired by [shadcn/improve](https://github.com/shadcn/improve): use your most capable model to audit animations in your project and hand the execution to cheaper models.
`improve-animations` surveys your whole codebase (not a single diff), audits it across eight categories (purpose & frequency, easing & duration, physicality, interruptibility, performance, accessibility, cohesion, missed opportunities), and presents a prioritized findings table. Pick the ones you want, and it writes self-contained plans into `plans/` — exact files, exact curves, exact durations, plus a feel check — that another agent can execute without any context or taste of its own. It never touches your source code itself.

```
> improve the animations in this codebase
> improve-animations quick        # hotspots only
> improve-animations performance  # one category
> improve-animations plan add press feedback to all buttons
> improve-animations execute plans/001-fix-dropdown-easing.md
```
