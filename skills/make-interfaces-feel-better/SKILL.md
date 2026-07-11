---
name: make-interfaces-feel-better
description: Design engineering skill for the Emil Kowalski skills bundle. Full UI review stack — tokens, feature structure, Mobbin/ScreensDesign research, motion polish, product psychology. Use with emil-design-eng, review-animations, animation-vocabulary, and apple-design. Invoke with /make-interfaces-feel-better. Triggers on UI polish, design details, "make it feel better", "feels off", feature design, feature structure, interaction model, UI states, empty state, loading state, error state, generic UI, AI-looking UI, stagger animations, border radius, optical alignment, font smoothing, tabular numbers, image outlines, box shadows, OKLCH, contrast, cognitive load, affordance, signifier, defaults, friction, user psychology, and product design psychology.
---

# Details that make interfaces feel better

Great interfaces rarely come from a single thing. It's usually a collection of small details that compound into a great experience. Apply these principles when building or reviewing UI code.

## Quick Reference

| Category | When to Use |
| --- | --- |
| [Typography](typography.md) | Text wrapping, font smoothing, tabular numbers |
| [Surfaces](surfaces.md) | Border radius, optical alignment, shadows, image outlines, hit areas |
| [Animations](animations.md) | Interruptible animations, enter/exit transitions, icon animations, scale on press |
| [Performance](performance.md) | Transition specificity, `will-change` usage |
| Visual Direction | Avoiding generic UI, grounding style in subject matter, signature design choices |
| Color Systems | OKLCH, palette ramps, contrast, dark mode, design tokens |
| Feature Structure | Feature anatomy, layout pattern choice, state model, interaction behavior |
| Reference Research | Mobbin + ScreensDesign pattern mining before inventing from scratch |
| Product Psychology | Cognitive load, defaults, affordance, memory, habits, trust, motivation |
| Review Flow | Screenshot/code audit, prioritized fixes, before/after tables |

## Core Principles

### 1. Concentric Border Radius

Outer radius = inner radius + padding. Mismatched radii on nested elements is the most common thing that makes interfaces feel off.

### 2. Optical Over Geometric Alignment

When geometric centering looks off, align optically. Buttons with icons, play triangles, and asymmetric icons all need manual adjustment.

### 3. Shadows Over Borders

Layer multiple transparent `box-shadow` values for natural depth. Shadows adapt to any background; solid borders don't.

### 4. Interruptible Animations

Use CSS transitions for interactive state changes — they can be interrupted mid-animation. Reserve keyframes for staged sequences that run once.

### 5. Split and Stagger Enter Animations

Don't animate a single container. Break content into semantic chunks and stagger each with ~100ms delay.

### 6. Subtle Exit Animations

Use a small fixed `translateY` instead of full height. Exits should be softer than enters.

### 7. Contextual Icon Animations

Animate icons with `opacity`, `scale`, and `blur` instead of toggling visibility. Use exactly these values: scale from `0.25` to `1`, opacity from `0` to `1`, blur from `4px` to `0px`. If the project has `motion` or `framer-motion` in `package.json`, use `transition: { type: "spring", duration: 0.3, bounce: 0 }` — bounce must always be `0`. If no motion library is installed, keep both icons in the DOM (one absolute-positioned) and cross-fade with CSS transitions using `cubic-bezier(0.2, 0, 0, 1)` — this gives both enter and exit animations without any dependency.

### 8. Font Smoothing

Apply `-webkit-font-smoothing: antialiased` to the root layout on macOS for crisper text.

### 9. Tabular Numbers

Use `font-variant-numeric: tabular-nums` for any dynamically updating numbers to prevent layout shift.

### 10. Text Wrapping

Use `text-wrap: balance` on headings. Use `text-wrap: pretty` for body text to avoid orphans.

### 11. Image Outlines

Add a subtle `1px` outline with low opacity to images for consistent depth. The color must be pure black in light mode (`rgba(0, 0, 0, 0.1)`) and pure white in dark mode (`rgba(255, 255, 255, 0.1)`) — never a near-black like slate, zinc, or any tinted neutral. A tinted outline picks up the surface color underneath it and reads as dirt on the image edge.

### 12. Scale on Press

A subtle `scale(0.96)` on click gives buttons tactile feedback. Always use `0.96`. Never use a value smaller than `0.95` — anything below feels exaggerated. Add a `static` prop to disable it when motion would be distracting.

### 13. Skip Animation on Page Load

Use `initial={false}` on `AnimatePresence` to prevent enter animations on first render. Verify it doesn't break intentional entrance animations.

### 14. Never Use `transition: all`

Always specify exact properties: `transition-property: scale, opacity`. Tailwind's `transition-transform` covers `transform, translate, scale, rotate`.

### 15. Use `will-change` Sparingly

Only for `transform`, `opacity`, `filter` — properties the GPU can composite. Never use `will-change: all`. Only add when you notice first-frame stutter.

### 16. Minimum Hit Area

Interactive elements need at least 40×40px hit area. Extend with a pseudo-element if the visible element is smaller. Never let hit areas of two elements overlap.

## Visual Direction Layer

Use these checks when the interface works but looks generic, templated, or like an unedited AI default.

### 17. Ground the Design in the Subject

Before choosing a look, name the product, audience, and screen job. Pull visual ideas from the product's world: its materials, artifacts, behavior, pace, and language. Do not choose a palette or layout just because it is common in SaaS templates.

### 18. One Signature Moment

Spend boldness in one place. Pick one memorable element that carries the screen: a distinctive hero treatment, interaction, typographic move, data view, visual metaphor, or layout structure. Keep the rest disciplined.

### 19. Avoid AI-Default Aesthetics

Be suspicious of warm cream plus serif plus terracotta, near-black plus acid accent, broadsheet layouts with hairline rules, generic bento grids, oversized gradient blobs, and random glassmorphism. Use them only when the brief genuinely asks for that world.

### 20. Typography Carries Personality

Type is not neutral. Choose display, body, and utility roles deliberately. Use a clear scale, intentional weights, and enough contrast between roles that hierarchy is felt before it is read.

### 21. Structure Must Mean Something

Numbers, dividers, labels, cards, and sections should encode a real relationship in the content. Do not add `01 / 02 / 03` markers unless order matters.

### 22. Motion Needs a Job

Use motion to explain continuity, give tactile feedback, focus attention, or create one orchestrated moment. Scattered decorative animation makes UI feel more generated, not more premium.

### 23. Copy Is Interface Material

Labels should name what people control, not how the system works. Buttons say exactly what happens. Empty states invite action. Errors explain what happened and how to fix it.

## Color and Token Layer

Use these checks when colors feel muddy, contrast is weak, dark mode is hand-picked, or the UI lacks a single source of truth.

### 24. Prefer OKLCH for New Color Systems

Use OKLCH when creating or repairing palettes. It keeps lightness perceptual, hue stable, and chroma easier to reason about than HSL or hand-picked hex ramps.

### 25. Change Contrast by Lightness

When foreground/background contrast fails, adjust the OKLCH `L` channel first. Chroma and hue should not be the primary contrast fix.

### 26. Build Palette Ramps, Not Random Colors

Create named tokens for background, surface, text, muted text, border/shadow, primary, accent, success, warning, and danger. Avoid one-off hex values unless they are imported brand colors.

### 27. Dark Mode Is Derived, Not Repainted

Derive dark mode from the same palette logic by remapping lightness and preserving intent. Do not hand-pick unrelated dark colors.

### 28. Check Gamut and Contrast

High chroma OKLCH values can clip in sRGB. Clamp if needed, provide fallbacks for wider-gamut color, and verify WCAG/APCA contrast for real foreground/background pairs.

### 29. Tokens Are the Design Contract

Spacing, radius, shadow, type, color, z-index, and motion should come from tokens or established local utilities. If a value repeats, promote it. If a value is unique, justify it.

## Feature Design Structure Layer

Use this layer when inventing or reshaping how a feature should look, behave, and fit into a product. Design patterns are reusable answers to common problems, but they must be adapted to the specific user goal and context.

### 30. Start With the Feature Job

Name the user goal, entry point, primary action, success outcome, and exit. If these are unclear, do not start with layout. Structure follows the job.

### 31. Choose the Pattern by Behavior

Pick the pattern that matches what the user is trying to do, not the pattern that looks nicest in a mockup.

| User Need | Prefer This Structure | Avoid |
| --- | --- | --- |
| Compare many items | Table, dense list, split view | Card grid with hidden details |
| Choose one thing fast | Select, command menu, segmented control | Multi-step wizard |
| Create something complex | Wizard, staged form, canvas with inspector | One giant form |
| Edit one object deeply | Detail page, side panel, inspector | Modal with cramped controls |
| Monitor changing data | Dashboard, timeline, activity feed | Static marketing-style cards |
| Ask/explore iteratively | Chat, search, command palette | Deep nested settings |
| Review then approve | Preview + checklist + confirmation | Immediate destructive action |
| Navigate hierarchy | Tree, sidebar, breadcrumb, drilldown | Flat grid that hides parent context |

### 32. Define the Feature Anatomy

Every feature needs an anatomy before it needs polish: entry point, title, primary action, secondary actions, content area, guidance, feedback, settings, help, and exit path. If a part is intentionally absent, say why.

### 33. Design the State Model First

Design every state before declaring the feature done: default, first-time empty, user-cleared empty, filtered empty, loading, partial loading, success, saved, dirty/unsaved, validation error, system error, offline, permission-gated, disabled, locked, and completed.

### 34. Empty States Must Explain Status and Next Step

An empty state should answer: why is this empty, is the system done loading, what can appear here, and what should the user do next. Use one primary action when there is a clear next step.

### 35. Loading States Must Preserve Confidence

Do not show a loader for flashes under about one second. Use skeletons for large content regions, spinners for small unknown waits, determinate progress for longer known waits, and background tasks for waits long enough that the user should keep working.

### 36. Errors Need Recovery Paths

Errors should explain what happened, where it happened, and what the user can do. Do not blame the user. Keep the rest of the app usable when the error is local to one panel or request.

### 37. Progressive Disclosure Splits Primary From Advanced

Show the few controls needed for the main job first. Hide advanced, rare, or dangerous options behind disclosure, menus, inspectors, or later steps. Do not hide required information or disorient the user's focus.

### 38. Define the Interaction Contract

For each feature, specify what happens on click/tap, hover, focus, active/pressed, keyboard, escape/back, outside click, drag, long press, submit, cancel, undo, retry, and destructive confirmation.

### 39. Design Feedback at Action Speed

Every user action needs feedback: pressed state immediately, optimistic update when safe, progress while waiting, success confirmation when complete, and rollback/retry when it fails.

### 40. Mobile and Desktop May Need Different Structures

Do not just shrink desktop. Tables may become cards or drilldowns, inspectors may become bottom sheets, sidebars may become tabs, and hover-only controls need visible mobile alternatives.

### 41. Component Specs Need Behavior, Not Just Looks

When defining a component or feature, include purpose, anatomy, variants, states, interactions, accessibility, responsive behavior, copy rules, and examples of when not to use it.

## Reference Research Layer

Phat has paid access to **both** Mobbin and ScreensDesign. When creating, restructuring, or significantly improving a feature, mine **both** before inventing from scratch. Goal: extract proven patterns for structure, states, interaction, density, copy, and platform behavior — never clone skins.

### 42. Search Real Products Before Inventing (dual source)

Before designing a new feature structure, gather **3–7** relevant examples total, with **at least one from each source** when the job exists in both libraries:

| Source | How to use | Best for |
| --- | --- | --- |
| **Mobbin** | `user-mobbin` MCP: `search_screens`, `search_flows`, `search_sections` | Cross-platform flows, web sections, general UI patterns |
| **ScreensDesign** | Open [screensdesign.com](https://screensdesign.com/) in the browser (Phat is subscribed / logged in), or accept screenshots Phat pastes from the Library | iOS subscription apps, onboarding, paywalls, store screens, full video walkthroughs, revenue-aware patterns |

Prefer products with the same job-to-be-done, not just the same industry. Do not skip ScreensDesign just because Mobbin returned results.

**Access rules for ScreensDesign:**
1. Prefer live Library research in the browser while Phat is logged in.
2. If login/paywall blocks the agent, ask Phat to paste 2–4 ScreensDesign screenshots or a Library link — then continue.
3. Cite app name + screen/flow type in the pattern table (e.g. `ScreensDesign · Calm · paywall`).

### 43. Compare Behavior, Not Decorations

For each reference, capture: entry point, layout pattern, primary action, secondary actions, empty/loading/error states, progressive disclosure, mobile behavior, copy tone, and exit path. Ignore surface style unless it solves a real UX problem.

### 44. Build a Pattern Table

Summarize references before choosing a direction. Tag the source on every row.

| Reference | Source | Pattern | What to Steal | What to Avoid |
| --- | --- | --- | --- | --- |
| Product/screen name | Mobbin / ScreensDesign | Table, wizard, chat, split view, sheet, timeline, etc. | Useful structure, state, interaction, or copy behavior | Anything off-brand, too complex, or mismatched to the user goal |

### 45. Borrow the Invariant, Not the Skin

Use the shared underlying pattern from references, then adapt it to the product's audience, visual direction, platform, and constraints. Never clone proprietary layouts, art, icons, or brand styling.

### 46. Use References to Fill Missing States

Mobbin and ScreensDesign are especially useful for finding overlooked states: first-time empty, filtered empty, search no-results, permission prompts, upgrade gates, destructive confirmations, success receipts, disabled controls, and recovery paths. For paywall / onboarding / first-session retention, lean harder on ScreensDesign video walkthroughs.

### 47. Let Platform Examples Win on Platform Behavior

For iOS-native work, prioritize iOS app examples (ScreensDesign Library + Mobbin iOS) and Apple HIG behavior. For web apps, prioritize Mobbin web/sections plus responsive web examples. For mobile web, check both app and web references before choosing navigation, sheets, tabs, or forms.

## Product Psychology Layer

Use these checks when the interface is technically polished but still feels unclear, heavy, untrustworthy, or hard to start. These principles are distilled from Wouter de Bres' *Product Design Psychology* archive in Phat's Obsidian vault.

### 48. Design for Someone Who Is Not You

Your own preference is not evidence. Before deciding that a label, layout, or flow is obvious, ask what proof you have from a person who did not build it.

### 49. First Impression Does Trust Work

Users judge quality before they understand the product. The first visible state must look intentional, stable, and cared for within a few seconds.

### 50. Make Clickable Things Look Clickable

Clean UI still needs signifiers. Links, buttons, inputs, rows, and gestures must visually say what action they support.

### 51. Intuitive Means Familiar

Do not treat "intuitive" as magic. A pattern feels intuitive when it matches what this user already knows. If you introduce a new pattern, make the next step unmistakable.

### 52. Spend User Attention Carefully

Every label, option, interruption, and visual emphasis spends working memory. Remove decisions that do not help the user's next move.

### 53. Keep Patterns Stable

Users predict what comes next. Reusing shape, placement, naming, and behavior lowers effort. Breaking patterns makes people slow down and re-check the UI.

### 54. Show Instead of Relying on Memory

Most users do not remember hidden controls, previous steps, or one-time explanations. Keep the needed cue visible at the moment of action.

### 55. Design the Peak and the Ending

People remember the strongest moment and the final moment more than the average of the flow. Make success, errors, completion, and exits feel deliberate.

### 56. Start with Momentum

Progress motivates. Give users a visible first step, starter state, or partial completion so the task feels already underway.

### 57. Layout Speaks Before Copy

Spacing, grouping, alignment, and similarity tell users what belongs together before they read. If the layout says one thing and the copy says another, the layout wins.

### 58. Goals Beat Tasks

Users do not want to complete your flow. They want the outcome behind the flow. Design screens around the user's goal, not the team's feature map.

### 59. Move Value Earlier

A small reward now beats a large promise later. Pull proof, feedback, preview, or payoff as close to the first action as possible.

### 60. Watch Behavior, Not Promises

What users say they will do is weaker than what they actually do under friction. Treat calm interview intent as a clue, not proof.

### 61. Feeling Comes Before Explanation

Users often react first and explain later. If a screen feels wrong, the rational critique may be downstream of the emotional reaction.

### 62. Protect Existing Habits During Change

Redesigns feel like loss before they feel like gain. Preserve familiar anchors, explain what moved, and avoid removing a user's old path without a bridge.

### 63. Fewer Choices Usually Wins

More options can make a product harder to choose and harder to use. Collapse, default, defer, or progressively disclose choices until they are needed.

### 64. Fix the First Broken Moment

When effort leads nowhere, users stop trying. Find the first place a user gets stuck, confused, or unrewarded, then repair that moment before polishing later steps.

### 65. Metrics Are Not the User

A metric is a signal, not the person. Before optimizing a number, ask what user behavior could make the number go up while the experience gets worse.

### 66. Roadmaps and Sunk Cost Can Hide the Problem

Past effort is not evidence that a feature should ship. Reopen the problem when the work starts serving the roadmap more than the user.

### 67. Defaults Are Power

Defaults, friction, urgency, and recommendations shape behavior. Use them to help users make good decisions, not to trap them into the decision the business prefers.

## Review Workflow

When asked to make a UI better, run this loop:

1. Inspect the actual screen/code first. Identify the product, audience, screen job, framework, existing design system, and proof surface.
2. If visual output is available, review the screen as a first-time user before reading implementation details.
3. Find the first broken moment: the earliest point where trust, clarity, momentum, or action breaks.
4. If designing or restructuring a feature, mine **Mobbin and ScreensDesign** for 3–7 relevant references (at least one from each when possible) and summarize the useful patterns in a source-tagged table.
5. Define the feature anatomy, pattern choice, state model, and interaction contract before visual polish.
6. Check the system: tokens, palette, typography, spacing, radius, shadow, motion, states, accessibility, responsiveness, and copy.
7. Make the smallest coherent set of changes that improves the user's next move.
8. Verify with screenshot, dev URL, running screen, tests, or static file proof before saying done.

Prioritize fixes in this order:

| Priority | Fix First |
| --- | --- |
| P0 | Broken layout, unreadable text, inaccessible controls, blocked primary action |
| P1 | Missing hierarchy, unclear affordance, weak contrast, broken mobile state |
| P2 | Generic visual direction, inconsistent spacing/tokens, awkward motion |
| P3 | Fine polish: shadows, microcopy, optical alignment, tiny animation tuning |

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Same border radius on parent and child | Calculate `outerRadius = innerRadius + padding` |
| Icons look off-center | Adjust optically with padding or fix SVG directly |
| Hard borders between sections | Use layered `box-shadow` with transparency |
| Jarring enter/exit animations | Split, stagger, and keep exits subtle |
| Numbers cause layout shift | Apply `tabular-nums` |
| Heavy text on macOS | Apply `antialiased` to root |
| Animation plays on page load | Add `initial={false}` to `AnimatePresence` |
| `transition: all` on elements | Specify exact properties |
| First-frame animation stutter | Add `will-change: transform` (sparingly) |
| Tiny hit areas on small controls | Extend with pseudo-element to 40×40px |
| Generic AI-looking visual direction | Choose one subject-specific signature moment and remove decorative defaults |
| Random hex values scattered through code | Promote repeated values to color tokens and use OKLCH for new palettes |
| HSL/hex ramp with uneven brightness | Rebuild the ramp in OKLCH with stable hue and perceptual lightness steps |
| Dark mode hand-picked from unrelated colors | Derive dark tokens from the same palette logic |
| Weak contrast | Adjust OKLCH lightness first, then verify foreground/background pairs |
| Design uses numbers/dividers/cards as decoration | Make structure encode sequence, grouping, status, or priority |
| Motion everywhere | Keep one orchestrated motion idea and use small transitions elsewhere |
| Button copy says `Submit` or `Continue` vaguely | Name the result: `Save changes`, `Publish`, `Create account` |
| Starting a feature with cards before knowing the job | Name the user goal, entry point, primary action, success outcome, and exit first |
| Desktop layout simply shrunk onto mobile | Change structure for mobile: bottom sheet, tabs, drilldown, or visible controls |
| Only happy path designed | Add default, empty, loading, partial, error, offline, permission, disabled, and success states |
| Empty state is blank or cute but useless | Explain status, teach what belongs there, and provide a direct next step |
| Loader appears instantly and flashes | Suppress loaders under about one second |
| Long task blocks the whole interface | Move it to a background task or allow other useful interaction |
| Error says `Something went wrong` | Say what failed, where, and how to recover |
| Advanced options crowd the main task | Use progressive disclosure and keep primary controls visible |
| Component spec only describes visuals | Add anatomy, variants, states, interactions, accessibility, responsive behavior, and copy rules |
| Assuming the user sees what the designer sees | Test the screen with someone who lacks project context |
| Minimal UI hides the action | Add signifiers for click, tap, drag, edit, expand, and submit |
| Too many visible choices | Default, group, defer, or progressively disclose options |
| Flow starts from zero | Add starter progress, templates, examples, or a clear first win |
| Users must remember instructions | Keep the cue visible at the point of action |
| Redesign removes familiar anchors | Preserve old paths, map what moved, and bridge the change |
| Optimizing the metric blindly | Check how the number can improve while user trust or ease gets worse |
| Polishing the end before the first stuck point | Find and fix the first broken moment |

## Review Output Format

Always present changes as a markdown table with **Before** and **After** columns. Include every change you made — not just a subset. Never list findings as separate "Before:" / "After:" lines outside of a table. Group changes by principle using a heading above each table, and keep each row focused on a single diff so the reader can scan the whole list quickly.

For UI reviews, lead with the highest-impact changes. If the work includes implementation, include every file changed in the tables. If the work is only a review, include priority labels in the Before column.

### Example

#### Concentric border radius
| Before | After |
| --- | --- |
| `rounded-xl` on card + `rounded-xl` on inner button (`p-2`) | `rounded-2xl` on card (`12 + 8`), `rounded-lg` on inner button |
| `border-radius: 16px` on both nested surfaces | Outer `24px`, inner `16px` with `8px` padding |

#### Tabular numbers
| Before | After |
| --- | --- |
| `<span>{count}</span>` on animated counter | `<span className="tabular-nums">{count}</span>` |
| Default numerals on timer | Added `font-variant-numeric: tabular-nums` to root |

#### Scale on press
| Before | After |
| --- | --- |
| `<button className="...">` | Added `active:scale-[0.96] transition-transform` |
| `scale(0.9)` on press | Raised to `scale(0.96)` — anything below `0.95` feels exaggerated |

#### Color system
| Before | After |
| --- | --- |
| One-off `#3b82f6` and `#2563eb` values across buttons | Added `--color-primary` / `--color-primary-hover` tokens in OKLCH |
| Low-contrast muted text on surface | Adjusted text token lightness and verified contrast against `--surface` |

#### Visual direction
| Before | After |
| --- | --- |
| Generic bento cards and gradient accents unrelated to the product | Replaced with one subject-specific signature element and quieter supporting layout |
| Decorative `01 / 02 / 03` labels on unordered benefits | Removed numbering and grouped benefits by user goal |

#### Feature structure
| Before | After |
| --- | --- |
| New feature starts as a grid of cards | Chose split view because the user needs to compare items and inspect one deeply |
| Only ideal state mocked | Added first-time empty, filtered empty, loading, partial, error, offline, disabled, and success states |
| Advanced settings visible in the primary form | Moved rare controls behind disclosure and kept required controls visible |
| Modal contains a complex editor | Replaced with full detail page plus inspector because the task needs space and undo |

#### Reference research
| Before | After |
| --- | --- |
| Invented feature structure from scratch | Compared Mobbin + ScreensDesign examples, then reused the common interaction pattern |
| Used only Mobbin and skipped ScreensDesign | Pulled iOS onboarding/paywall refs from ScreensDesign Library as well |
| Copied a reference screen's visual style | Extracted only the structure/state behavior and adapted styling to the product |
| Missed no-results and permission states | Added them after checking similar production screens in both libraries |

Rows should cite the specific file and the specific property that changed when it isn't obvious from the snippet. If a principle was reviewed but nothing needed to change, omit that table entirely — empty tables add noise.

## Review Checklist

- [ ] Nested rounded elements use concentric border radius
- [ ] Icons are optically centered, not just geometrically
- [ ] Shadows used instead of borders where appropriate
- [ ] Enter animations are split and staggered
- [ ] Exit animations are subtle
- [ ] Dynamic numbers use tabular-nums
- [ ] Font smoothing is applied
- [ ] Headings use text-wrap: balance
- [ ] Images have subtle outlines
- [ ] Buttons use scale on press where appropriate
- [ ] AnimatePresence uses `initial={false}` for default-state elements
- [ ] No `transition: all` — only specific properties
- [ ] `will-change` only on transform/opacity/filter, never `all`
- [ ] Interactive elements have at least 40×40px hit area
- [ ] Product, audience, screen job, and proof surface are clear
- [ ] Visual direction is grounded in the product's subject matter
- [ ] Design has one justified signature moment
- [ ] Generic AI-default aesthetics were removed or justified
- [ ] Typography roles, scale, weights, and spacing are intentional
- [ ] Structural devices encode real sequence, grouping, priority, or status
- [ ] Copy names user-recognizable actions and outcomes
- [ ] Repeated colors, spacing, radius, shadows, type, and motion use tokens
- [ ] New or repaired palettes use OKLCH where the stack supports it
- [ ] Foreground/background contrast is checked in real pairings
- [ ] Dark mode is derived from the same token logic
- [ ] User goal, entry point, primary action, success outcome, and exit are named
- [ ] Layout pattern matches the behavior the user needs
- [ ] Feature anatomy is defined before polish
- [ ] Default, empty, loading, partial, success, dirty, error, offline, permission, disabled, locked, and completed states are covered where relevant
- [ ] Empty states explain status and provide a direct next step
- [ ] Loading states match wait time and preserve system confidence
- [ ] Errors explain what happened and how to recover
- [ ] Progressive disclosure keeps primary controls visible and advanced controls available
- [ ] Interaction contract covers click/tap, hover, focus, keyboard, cancel, submit, retry, undo, and destructive confirmation
- [ ] Mobile structure is intentionally adapted, not just shrunk
- [ ] Component specs include purpose, anatomy, variants, states, interactions, accessibility, responsive behavior, and copy rules
- [ ] Mobbin references were checked (MCP `search_screens` / `search_flows` / `search_sections` when available)
- [ ] ScreensDesign references were checked (browser Library at screensdesign.com, or Phat-pasted Library screenshots)
- [ ] Pattern table tags each row with source (Mobbin vs ScreensDesign)
- [ ] References were summarized by structure, states, interaction, copy, and platform behavior
- [ ] Borrowed patterns are adapted to this product instead of copied visually
- [ ] First impression communicates trust and quality within a few seconds
- [ ] Primary actions have visible signifiers
- [ ] UI patterns are stable across similar controls and screens
- [ ] The next needed cue is visible instead of relying on memory
- [ ] Choices are defaulted, grouped, deferred, or progressively disclosed
- [ ] The user's real goal is visible, not just the product task
- [ ] Value, payoff, or feedback appears as early as possible
- [ ] Existing user habits are protected during redesigns
- [ ] The first stuck or unrewarded moment has been identified
- [ ] Defaults and friction serve the user, not just the business metric

## Reference Files

- [typography.md](typography.md) — Text wrapping, font smoothing, tabular numbers
- [surfaces.md](surfaces.md) — Border radius, optical alignment, shadows, image outlines
- [animations.md](animations.md) — Interruptible animations, enter/exit transitions, icon animations, scale on press
- [performance.md](performance.md) — Transition specificity, `will-change` usage
- GitHub reference: `https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md` — distinctive visual direction and anti-generic design process
- GitHub reference: `https://github.com/jakubkrehel/oklch-skill` — OKLCH color systems, contrast, palette ramps, and dark mode
- GitHub reference: `https://github.com/veluthoor/ui-ux-design-review-agent` — UI review flow, prioritized critique, palettes, component redesigns, and accessibility pass
- HCI patterns reference: `https://www.mit.edu/~jtidwell/common_ground_onefile.html` — design patterns as reusable solutions for common problems in context
- NN/g reference: `https://www.nngroup.com/articles/empty-state-interface-design/` — empty states should communicate status, teach the feature, and provide direct paths to key tasks
- NN/g reference: `https://www.nngroup.com/articles/progressive-disclosure/` — show primary controls first and reveal specialized options on request
- Primer reference: `https://primer.style/product/ui-patterns/loading/` — loading states by wait time, skeletons, determinate progress, and background tasks
- Primer reference: `https://primer.style/product/ui-patterns/progressive-disclosure/` — disclosure should maintain context and pair icons with clear text
- Material reference: `https://m1.material.io/patterns/errors.html` — errors should explain the issue, avoid blame, preserve usable context, and offer recovery
- Apple reference: `https://developer.apple.com/design/human-interface-guidelines` — platform guidance for clear, intuitive, native-feeling feature behavior
- Mobbin: `https://mobbin.com/` — via `user-mobbin` MCP (`search_screens`, `search_flows`, `search_sections`) for production app/web flows, states, and platform patterns
- ScreensDesign: `https://screensdesign.com/` — Phat has a Pro subscription; use Library (and Create when generating) for iOS onboarding, paywalls, store screens, and video walkthroughs. Prefer live browser research while logged in; otherwise ask Phat to paste Library screenshots
- Product Design Psychology source note: `/Users/hiepphatnguyen/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian Vault/Research/Product Design Psychology/Product Design Psychology.md`
- Product Design Psychology full archive: `/Users/hiepphatnguyen/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian Vault/Research/Product Design Psychology/Product Design Psychology - Full Book.md`
