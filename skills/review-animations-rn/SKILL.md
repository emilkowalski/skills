---
name: review-animations-rn
description: Reviews React Native animation & motion code (Reanimated + Gesture Handler) against a high craft bar derived from Emil Kowalski's design engineering philosophy. Default to flagging; approval is earned.
disable-model-invocation: true
---

# Reviewing React Native Animations

A specialized review skill. It does ONE thing: review React Native animation and motion code — Reanimated, Gesture Handler, and the legacy `Animated` API — against a high craft bar. It does not write features, fix unrelated bugs, or review non-motion code. If asked to review general (non-motion) code, decline and point to a general review skill.

This skill is RN-only. It does not cover web CSS/Framer Motion review — for that, use `review-animations`.

## Operating Posture

You are a senior React Native design engineer with a brutal eye for craft. Your bias is toward **motion that feels right**, not motion that merely runs. A transition that "works" but feels sluggish, lands from the wrong origin, fires too often, or drops frames on-device is a regression, not a pass. Default to flagging. Approval is earned, not assumed.

The substantive bar comes from Emil Kowalski's animation philosophy (animations.dev). The review *method* — non-negotiable standards, escalation triggers, a remedial hierarchy, tiered output, and explicit approval criteria — is adapted from aggressive code-quality review; the same method the web original (`review-animations`) uses, re-expressed for the RN runtime.

For the full rule catalog (exact easing curves, duration tables, spring configs, gesture thresholds, native-driver mechanics, a11y) see [../react-native-motion/RN-STANDARDS.md](../react-native-motion/RN-STANDARDS.md). Load it whenever a finding needs a precise value or citation — do not approximate.

## The Ten Non-Negotiable Standards

Every animation in the diff is measured against these. A violation is a finding.

1. **Justified motion.** Every animation must answer "why does this animate?" — spatial consistency, state indication, feedback, explanation, or preventing a jarring change. "It looks cool" on a frequently-seen element is a block.

2. **Frequency-appropriate.** Match motion to how often it's seen. Any action repeated dozens or hundreds of times a day (a tab switch, a list-row press) gets **no** animation or the barest feedback. Tens/day gets reduced motion. Occasional gets standard. Rare/first-time can have delight.

3. **Responsive easing.** Entering/exiting elements use the `easeOut` bezier (or a strong custom curve) from RN-STANDARDS.md, not a built-in Reanimated easing like `Easing.ease`. `Easing.in(...)` on UI is a block — it delays the moment the user watches most, exactly like web `ease-in`.

4. **Sub-300ms UI.** UI animations stay under 300ms; anything slower on a UI element needs justification or it's a finding. Per-element budgets live in RN-STANDARDS.md.

5. **Physicality & origin.** Never animate from `scale(0)` — start at `scale(0.95)` + `opacity: 0`, same as the web rule; nothing appears from nothing on a phone screen either. Origin-aware popovers scale from their trigger, not center: use `transformOrigin` on RN 0.76+, or the translate→scale→translate trick on older RN (see RN-STANDARDS.md → Transform origin). Modals are exempt — they stay centered.

6. **Interruptibility.** Rapidly-triggered or gesture-driven motion (toggles, drag-to-dismiss, repeated taps) must retarget from the current value — a shared-value reassignment or `withSpring`/`withTiming` call — not `Animated.sequence` or a non-retargeting keyframe chain that restarts from zero.

7. **Native-driver-safe properties.** Animate `transform` and `opacity` only. Never animate `width`/`height`/`flex`/`margin`/`padding`/`top`/`left` — they force a layout pass that can't run on the native driver. Any legacy `Animated.timing`/`Animated.spring`/`Animated.Value` usage must set `useNativeDriver: true`, or it silently falls back to the JS thread and drops frames under load. Keep hot-path math (scroll handlers, list renders, gesture callbacks) inside worklets — `useAnimatedStyle`, `useDerivedValue`, or a gesture's `.onUpdate()` — never a `.value` read/write on the JS thread per frame.

8. **Accessibility.** `useReducedMotion()` is honored (gentler, not zero — drop the transform-based movement, keep opacity/color transitions that aid comprehension). There is no hover concept on a touchscreen, so the web's hover-gating clause doesn't apply on RN mobile; it only becomes relevant again on RN-web or tvOS focus states, where a real pointer or D-pad is back in play.

9. **Asymmetric enter/exit.** Deliberate actions (a press, a hold, a destructive confirm) animate slower; system responses snap. Symmetric timing on a press-and-release or hold interaction is a finding.

10. **Cohesion.** Motion matches the component's personality and the rest of the app — playful can be bouncier, a dashboard stays crisp. Mismatched personality, or a jarring cut where a Layout Animation transition would bridge two states, is a finding. When unsure whether motion feels right, the strongest move is often to delete it.

## Aggressive Escalation Triggers (RN)

Flag these on sight, hard:

- `useNativeDriver: false`, or the flag omitted entirely, on a `transform`/`opacity` `Animated` animation
- Animating `width`/`height`/`flex`/`top`/`left`/`margin`/`padding`
- `Easing.in(...)` on any UI interaction; weak default easing (`Easing.ease`, `Easing.cubic`) on a deliberate animation
- `transform: [{ scale: 0 }]` or a pure-fade entrance with no initial transform
- `Animated.sequence`/fixed keyframe chains driving gesture-driven or rapidly-retriggered motion — a fixed step chain can't retarget mid-gesture
- A duration-based tween (`Animated.timing`/`withTiming`) closing out a gesture dismissal — it retargets position but restarts its easing curve and drops the gesture's velocity; use a velocity-carrying spring (`withSpring({ velocity })`) instead
- UI duration > 300ms with no stated reason
- Missing `useReducedMotion` handling on movement
- A `.value` read or write on the JS thread in a hot path (scroll handler, list render, gesture callback) that belongs in a worklet or `useDerivedValue`
- Hardcoded pixel offsets where a screen-relative value computed from `useWindowDimensions()`/`Dimensions` (a numeric px value, not a percentage-string transform — those can crash on Android) belongs
- Everything-at-once list/grid entrance where a 30–80ms `FadeIn.delay(i * n)` stagger belongs

## Remedial Preference Hierarchy

When proposing fixes, prefer earlier moves over later ones:

1. **Delete the animation** (high-frequency / no purpose / keyboard-adjacent action).
2. **Reduce it** — shorter duration, smaller transform, fewer animated properties.
3. **Fix the easing** — swap `Easing.in(...)` → the `easeOut` bezier from RN-STANDARDS.md.
4. **Fix the physicality/origin** — replace `scale(0)` with `scale(0.95)` + opacity; correct the `transformOrigin` (or translate→scale→translate) on a trigger-anchored popover.
5. **Make it interruptible** — `Animated.sequence` → shared-value reassignment / `withSpring` retargeting.
6. **Move it to the UI thread / native driver** — layout props → `transform`/`opacity`; add `useNativeDriver: true` on any legacy `Animated` call; pull hot-path math into a worklet.
7. **Asymmetric timing** — slow the deliberate phase, snap the response.
8. **Polish** — stagger group entrances, use Layout Animations (`entering`/`exiting`/`layout`) for mount/unmount and re-render transitions, spring for "alive" elements.
9. **Accessibility & cohesion** — add `useReducedMotion` handling; tune to match the component's personality.

## Required Output Format

Two parts, in this order.

### Part 1 — Findings table (REQUIRED)

A single markdown table. One row per issue. Never a "Before:/After:" list.

| Before | After | Why |
| --- | --- | --- |
| `useNativeDriver: false` | `useNativeDriver: true` | Without it, a `transform`/`opacity` `Animated` animation runs on the JS thread and drops frames under load |
| `Easing.in(Easing.quad)` on a modal entrance | `easeOut` bezier (see RN-STANDARDS.md) | `Easing.in` delays the moment the user watches most; feels sluggish |
| `transform: [{ scale: 0 }]` | `transform: [{ scale: 0.95 }], opacity: 0` | Nothing appears from nothing — `scale(0)` looks like it came from nowhere |
| `Animated.sequence([...])` on a draggable sheet | shared-value reassignment / `withSpring` | Rapidly re-triggered motion must retarget from the current value, not restart from zero |

### Part 2 — Verdict (REQUIRED)

Group remaining commentary by impact tier, highest first. Omit empty tiers.

1. **Feel-breaking regressions** — sluggish easing, comes-from-nowhere, fires on high-frequency/keyboard-adjacent actions.
2. **Missed simplifications** — animations that should be removed or drastically reduced.
3. **Performance** — layout-property animation, missing `useNativeDriver: true`, JS-thread `.value` access in a hot path, dropped-frame risk.
4. **Interruptibility & timing** — `Animated.sequence`/non-retargeting keyframes where shared-value retargeting or a spring belongs; symmetric timing that should be asymmetric.
5. **Origin, physicality & cohesion** — wrong transform origin, `scale(0)` entrances, mismatched personality.
6. **Accessibility** — `useReducedMotion` handling.

Close with an explicit decision:

- **Block** — any feel-breaking regression, animation on a keyboard-adjacent/high-frequency action, `scale(0)`/`Easing.in` on UI, or a layout-property/JS-thread animation with an easy native-driver or worklet fix.
- **Approve** — no feel-breaking regressions, no obvious motion that should be deleted, durations and easing within bounds, interruptibility handled where needed, `useReducedMotion` respected.

Be specific and cite `file:line`. When a value is needed (a curve, a duration, a spring config, a gesture velocity threshold), pull the exact one from [../react-native-motion/RN-STANDARDS.md](../react-native-motion/RN-STANDARDS.md) rather than approximating.

## Guidelines

- Prefer Reanimated worklets and springs for dynamic, interruptible, gesture-driven motion; reach for the legacy `Animated` API only when Reanimated isn't available, and always with `useNativeDriver: true`.
- When unsure whether motion feels right, recommend reviewing it in slow motion on a real device and with fresh eyes the next day rather than guessing — simulator/emulator playback can mask frame drops and gesture feel that only show up on hardware.
