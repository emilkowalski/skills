---
name: react-native-motion
description: Emil Kowalski's animation & design-engineering philosophy, translated for React Native (Reanimated + Gesture Handler). Use when building or reviewing animations, gestures, transitions, or press feedback in a React Native / Expo app — easing, duration, springs, interruptibility, the native-driver performance model, and reduced motion, with exact RN values in RN-STANDARDS.md.
---

# React Native Motion

This is Emil Kowalski's design-engineering philosophy applied to React Native. For the full version and the deeper "why" behind every rule, read the web original: [emil-design-eng](../emil-design-eng/SKILL.md). Everything here targets **Reanimated 3/4 + react-native-gesture-handler 2** as the default stack; the legacy `Animated` API and Moti are noted only where their behavior actually differs from that default.

## Core philosophy (compressed)

**Taste is trained, not innate.** You build the instinct for what feels right by studying great interfaces and asking why they work — reverse-engineer motion the same way on-device that you would in a browser. See the original for the full argument.

**Unseen details compound.** Users never consciously notice correct easing, correct duration, or a popover that scales from its trigger instead of its center — that's the point. A thousand invisible-but-correct decisions is what "feels right" is made of.

**Beauty is leverage.** People pick apps based on the whole feel, not just function. On mobile this is even more visceral — a screen is held in the hand, not viewed through a mouse — so a jarring transition or a laggy press state costs more than it would on the web.

## The Animation Decision Framework

Answer these four questions, in order, before writing any animation code.

### 1. Should this animate at all?

Ask how often the user will see it.

| Frequency | Decision |
| --- | --- |
| 100+ times/day (keyboard shortcuts, command palette toggle) | No animation. Ever. |
| Tens of times/day (frequent toggles, list nav) | Remove or drastically reduce |
| Occasional (modals, drawers, toasts) | Standard animation |
| Rare/first-time (onboarding, celebrations) | Can add delight |

**RN note:** there are no keyboard shortcuts on mobile, but the same logic applies to anything a user repeats dozens or hundreds of times a session — a tab switch, a list row press, a chat bubble appearing. If it fires that often, treat it like the web treats keyboard actions: cut the animation or make it near-instant.

### 2. What is the purpose?

Every animation needs an answer to "why does this move?" Valid purposes: **spatial consistency** (a sheet exits the way it entered), **state indication** (a button morphs to show a state change), **feedback** (a press scales down to confirm the touch registered), **explanation** (an onboarding animation shows how a feature works), or **preventing a jarring change** (a view appearing with no transition feels broken).

If the honest answer is "it looks cool" and the element is something the user sees frequently, don't animate it.

### 3. What easing?

- Entering/exiting → `easeOut` (starts fast, feels responsive)
- Moving/morphing on screen → `easeInOut`
- Color → default ease
- Constant motion (marquee, progress) → linear
- **Never `Easing.in(...)` on UI** — it delays the exact moment the user is watching most closely.

```ts
opacity.value = withTiming(1, { duration: 200, easing: easeOut });
```

The exact bezier constants (`easeOut`, `easeInOut`, `easeDrawer`) live in RN-STANDARDS.md → Easing — don't recreate them ad hoc, import the shared constants.

### 4. How fast?

UI animations stay under 300ms. See RN-STANDARDS.md → Duration for the full table (press feedback, tooltips, dropdowns, modals) — the numbers are identical to the web, RN's UI thread doesn't buy a bigger budget.

## RN component principles

**Press feedback.** Track press state in a shared value, not a pseudo-class — RN has no `:active`.

```tsx
const scale = useSharedValue(1);
const style = useAnimatedStyle(() => ({ transform: [{ scale: scale.value }] }));

<Pressable
  onPressIn={()  => { scale.value = withTiming(0.97, { duration: 120, easing: easeOut }); }}
  onPressOut={() => { scale.value = withTiming(1,    { duration: 120, easing: easeOut }); }}>
  <Animated.View style={style}>{children}</Animated.View>
</Pressable>
```

Never animate an entrance from `scale(0)` — nothing in the real world appears from nothing. Start at `0.95` + `opacity: 0` instead.

**Enter/exit with Layout Animations.** Reanimated's `entering`/`exiting`/`layout` props replace the `useEffect` + `mounted` dance entirely:

```tsx
<Animated.View entering={FadeIn} exiting={FadeOut} layout={LinearTransition} />
```

Stagger list items with `FadeIn.delay(i * 50)` — keep the delay in the 30–80ms window; longer feels slow, and stagger should never block interaction.

**Interruptibility.** Reassigning a shared value mid-flight (`scale.value = withSpring(...)` or `withTiming(...)` called again before the previous animation settles) retargets smoothly from the current value. `Animated.sequence` (legacy API) restarts from zero on interruption instead. For anything rapidly triggered or gesture-driven — repeated taps, a drag that can reverse — prefer shared-value retargeting over sequences.

## Gestures & drag

Gesture Handler's `Gesture.Pan()` keeps the whole interaction on the UI thread. Hand off velocity to a spring on release, use `withDecay` for momentum, and apply rubber-banding at boundaries instead of a hard stop:

```ts
const pan = Gesture.Pan()
  .onUpdate((e) => { translateY.value = e.translationY; })
  .onEnd((e) => { translateY.value = withSpring(0, { velocity: e.velocityY }); });
```

See [apple-design](../apple-design/SKILL.md) for the physics rationale behind velocity hand-off and rubber-banding. See RN-STANDARDS.md → Gestures & drag for the full worked example, including the `withDecay`/rubber-band helper and the web-to-RN velocity unit conversion.

## Performance

Reanimated worklets run on the UI thread by construction — there's no `useNativeDriver` flag to set, and only `transform`/`opacity` are cheap to animate (layout properties like `width`, `height`, `padding` force a layout pass regardless of thread). The legacy `Animated` API is stricter: without `useNativeDriver: true` it runs on the JS thread and drops frames, and even with it, it can only drive `transform`/`opacity` — never layout props or `backgroundColor`. Full detail, including the JS/UI-thread hot-path rule, is in RN-STANDARDS.md → Performance & the native driver.

## Review Format (Required)

When reviewing RN animation code, use a markdown table with Before/After columns — never a "Before:"/"After:" list.

| Before | After | Why |
| --- | --- | --- |
| `Animated.timing(x, { useNativeDriver: false })` | `useNativeDriver: true` (or a Reanimated worklet) | Off the native driver, transform/opacity animate on the JS thread and drop frames |
| `withTiming(0, { easing: Easing.in(Easing.quad) })` on a dropdown | `easeOut` bezier | `ease-in` delays the moment the user watches most; feels sluggish |
| `transform: [{ scale: 0 }]` entrance | `scale: 0.95` + `opacity: 0` | Nothing in the real world appears from nothing |
| `Animated.sequence([...])` on a rapidly re-triggered press | Retarget a shared value (`scale.value = withTiming(...)`) | Sequences restart from zero on interruption; shared-value retargeting picks up from the current value |
| Animating `width`/`height` to reveal content | `overflow: 'hidden'` + `transform: [{ scaleX }]` on a fixed-size view | Layout props force a JS-thread layout pass; `transform` stays on the UI thread |

For exact curves, durations, spring configs, and gesture thresholds, load `RN-STANDARDS.md`.
