---
name: ask-emil
description: Ask which skill or flow fits your situation. A router over the skills in this repo.
disable-model-invocation: true
---

# Ask Emil

Before stating what a skill does or recommending one, read that skill's SKILL.md: the summaries here are for orientation only. Then recommend **one** skill (or one short sequence) for the user's situation, say why in a sentence, and name the skill they'd reach for next. Don't list the whole map back at them.

A **flow** is a path through the skills. Most UI work travels one **main flow**, from idea to shipped. Some skills are **upkeep** you run on a codebase that already exists, some are **references** that sit underneath everything, and a few stand alone.

## The main flow: idea → ship

1. **Not sure what it should look or feel like?** Detour through **`/prototype`**. It builds several genuinely different versions behind a live picker, then promotes the one you pick into the real code. Reach for it whenever a design question is hard to settle in words.

2. **Build it.** Pick the builder by what's moving:
   - **`/pick-ui-library`** first if the task needs a dependency (dropdown, dialog, toast, drawer, command menu, drag and drop, charts). Don't let the agent hand-roll a toast.
   - **`/animate`** for one animation on the web: whether to animate at all, then tool, properties, curve, duration, interruption, exit.
   - **`/choreograph`** when several elements move together: staggers, hero entrances, view swaps, an item leaving while siblings close the gap.
   - **`/gestures`** when the user's finger drives it: drag, swipe, sheets, snap points, swipe-to-dismiss.
   - **`/animate-expo`** for any of the above in React Native or Expo.
   - **`/ask-sonner`** when the work is toasts with Sonner.

3. **Try to break it.** Before calling it done:
   - **`/break-ui`** feeds it worst-case data (long names, empty lists, huge counts, emoji, non-Latin text) behind a toggle and reports what broke.
   - **`/review-animations`** reviews the motion in the diff against a strict bar. Default to flagging; approval is earned.
   - **`/mobile-native`** if it runs on a phone as a web app: sticky hover, the 100vh bug, inputs that zoom, safe areas.
   - **`/animation-performance`** if anything drops frames.

4. **Learn from the session.** **`/learn-taste`** closes the loop. Run it at the end, in the same session, before you clear: it collects every design correction you made (including edits you made yourself) and turns each into a rule with its why, so the next agent doesn't repeat the mistake.

## Upkeep: a codebase that already exists

Not feature work. Run these when you have a spare moment, or when the app "feels off".

- **The motion needs work across the app** → **`/improve-animations`**. Read-only: it audits every animation and writes prioritized, self-contained plans another agent (or a cheaper model) can execute.
- **It feels static** → **`/find-animation-opportunities`**. Read-only: it proposes motion with exact values, and rejects everything that shouldn't move. Build the ones you accept with `/animate`.
- **It feels slow or over-animated** → **`/remove-animations`**. Edits code, but only to subtract: motion on keyboard actions, high-frequency surfaces, decoration with no purpose.

These three cover different questions. If the user isn't sure which, ask whether the problem is *bad* motion, *missing* motion, or *too much* motion.

## References underneath

Model-invoked skills the others lean on. Reach for them directly when the **knowledge**, not a process, is what's missing.

- **`/emil-design-eng`**: the core philosophy for UI polish, component interactions, and the invisible details. The fallback when no narrower skill fits.
- **`/apple-design`**: Apple's principles for interface design and fluid, physical motion, translated for the web.
- **`/animation-vocabulary`**: when the problem is the **word**. "What's it called when…" turns a vague description into the exact term to prompt with.

## Standalone

- **`/write-swift`**: modern Swift, Swift 6 concurrency, and native iOS code. Off the web flow entirely.

## Common situations

| You say | Reach for |
| --- | --- |
| "Animate this" | `/animate` |
| "These should come in one after another" | `/choreograph` |
| "It doesn't follow my finger" | `/gestures` |
| "It stutters" / "it's janky" | `/animation-performance` |
| "Does this animation feel right?" | `/review-animations` |
| "Make the app feel better" | `/improve-animations` |
| "What could animate here?" | `/find-animation-opportunities` |
| "Too much is moving" | `/remove-animations` |
| "Give me a few options" | `/prototype` |
| "Which library should I use?" | `/pick-ui-library` |
| "Works in Chrome, feels wrong on my phone" | `/mobile-native` |
| "Try the worst case" | `/break-ui` |
| "What's that bouncy thing called?" | `/animation-vocabulary` |
| "Stop making that mistake" | `/learn-taste` |
