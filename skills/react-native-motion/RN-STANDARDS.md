# React Native Motion Standards Reference

Reanimated 3 + Gesture Handler 2 mechanics for Emil Kowalski's animation standards. Same values, same decisions — translated to the RN runtime. For the "why" behind any rule, follow the linked section in the web original.

## Easing

> Web original: [STANDARDS.md → Easing](../review-animations/STANDARDS.md).

Same decision order as the web: entering/exiting → `easeOut`, on-screen movement → `easeInOut`, drawers → `easeDrawer`. Built-in Reanimated easings (`Easing.ease`, `Easing.cubic`) are as weak as their CSS equivalents — export the same strong custom beziers as constants and reuse them everywhere:

```ts
import { Easing } from 'react-native-reanimated';

export const easeOut    = Easing.bezier(0.23, 1, 0.32, 1);    // strong ease-out — entering/exiting
export const easeInOut  = Easing.bezier(0.77, 0, 0.175, 1);   // on-screen movement
export const easeDrawer = Easing.bezier(0.32, 0.72, 0, 1);    // iOS-like drawer
```

```ts
opacity.value = withTiming(1, { duration: 200, easing: easeOut });
```

**Rule: never `Easing.in(...)` on UI** — same reasoning as web `ease-in`: it starts slow and delays the exact moment the user is watching. If you find yourself reaching for `Easing.in`, you almost certainly want `easeOut` instead.

## Duration

> Web original: [STANDARDS.md → Duration](../review-animations/STANDARDS.md).

Identical table, identical numbers — RN's UI thread doesn't buy you a bigger duration budget:

| Element | Duration |
| --- | --- |
| Button press feedback | 100–160ms |
| Tooltips, small popovers | 125–200ms |
| Dropdowns, selects | 150–250ms |
| Modals, drawers | 200–500ms |
| Marketing / explanatory | Can be longer |

**UI animations stay under 300ms.** A faster spinner (`withRepeat` on a shorter rotation duration) makes a load feel faster at identical actual load time — the perception rule holds on-device just as it does in the browser.

## Springs

> Web original: [STANDARDS.md → Springs](../review-animations/STANDARDS.md).

Reanimated ships both of Apple's spring vocabularies. Prefer `dampingRatio`/`duration` — it's the RN analogue of `{ type: "spring", duration, bounce }` — and drop to the physics form only when you need finer control:

```ts
withSpring(target, { dampingRatio: 1,   duration: 400 }); // critically damped, no overshoot
withSpring(target, { dampingRatio: 0.8, duration: 400 }); // slight bounce — momentum only
withSpring(target, { mass: 1, stiffness: 100, damping: 10 }); // physics form (more control)
```

Mapping to Apple's `damping`/`response` (the values you'd see in a SwiftUI or UIKit spring):

| Apple (damping / response) | Reanimated |
| --- | --- |
| `1.0 / 0.3–0.4` (no overshoot) | `dampingRatio: 1, duration: 300–400` |
| `~0.8` (slight bounce) | `dampingRatio: 0.8, duration: 300–400` |

Keep bounce subtle — `dampingRatio` in the `0.7–0.9` range corresponds to the web's bounce `0.1–0.3`. Reserve bounce (`dampingRatio < 1`) for drag-to-dismiss and gesture hand-off, not fade-ins or modals: a spring maintains velocity when interrupted (unlike `withTiming`, which restarts easing from the current value but not momentum), so it's the right tool exactly where the web uses it — gestures the user might reverse mid-motion.

## Performance & the native driver

> Web original: [STANDARDS.md → Performance](../review-animations/STANDARDS.md).

This is the biggest RN-specific fork from the web rules, because RN has two animation runtimes with very different rules.

**Reanimated worklets run on the UI thread**, not the JS thread — this is RN's analogue of CSS running off the main thread. A `useAnimatedStyle` callback is compiled to run on the UI thread every frame, independent of JS thread load (script execution, network responses, list re-renders). There is no `useNativeDriver` flag to set for Reanimated — it's UI-thread by construction.

**The legacy `Animated` API is different and stricter.** If you're touching `Animated.timing`, `Animated.spring`, or `Animated.Value` directly (not Reanimated), you MUST pass `useNativeDriver: true` or the animation runs on the JS thread and drops frames under load — exactly like a Framer Motion shorthand falling back to `requestAnimationFrame`. But the native driver only supports **`transform` and `opacity`**. It cannot animate layout properties — `width`, `height`, `margin`, `padding`, `top`, `left` — because those force a layout pass, and a layout pass has to run on the JS thread regardless of the flag. `backgroundColor` fails for a different reason: it's not a layout property, but the legacy native driver has no native color interpolation, so it also falls back to the JS thread ("Style property `backgroundColor` is not supported by native animated module"). This is the RN form of "only animate transform and opacity": the web rule exists because those properties skip layout/paint; the RN rule exists because they're the only ones the native driver can execute at all — for color, reach for a Reanimated worklet instead, which interpolates color on the UI thread.

Practical implications:
- Prefer Reanimated over legacy `Animated` for anything performance-sensitive — it sidesteps the whole `useNativeDriver` limitation.
- Never animate `width`/`height` to reveal or resize a view. Animate `transform: [{ scaleX }]` on a fixed-size element instead (see Reveal & clip below).
- **Never read or write `.value` on the JS thread in a hot path** (scroll handlers, list renders, gesture callbacks called from JS). Keep the math inside worklets — `useAnimatedStyle`, `useDerivedValue`, or a `.onUpdate()` gesture callback — so it never crosses the JS/UI thread bridge per frame.

## Press feedback

> Web original: [STANDARDS.md → Physicality](../review-animations/STANDARDS.md).

RN has no `:active` pseudo-class — press state is tracked in a shared value via `Pressable`'s `onPressIn`/`onPressOut`. Same scale value, same duration, same easing as the web rule:

```tsx
const scale = useSharedValue(1);
const style = useAnimatedStyle(() => ({ transform: [{ scale: scale.value }] }));

<Pressable
  onPressIn={()  => { scale.value = withTiming(0.97, { duration: 120, easing: easeOut }); }}
  onPressOut={() => { scale.value = withTiming(1,    { duration: 120, easing: easeOut }); }}>
  <Animated.View style={style}>{children}</Animated.View>
</Pressable>
```

`scale` on an `Animated.View` scales its children too, just like CSS `scale()` — font, icons, and content shrink together. Subtle range: `0.95–0.98`. Never animate from `scale(0)` on entrance — start at `0.95` + `opacity: 0`, same as the web rule; RN doesn't get a pass on this because nothing in the real world appears from nothing on a phone screen either.

## Transform origin

> Web original: [STANDARDS.md → Physicality](../review-animations/STANDARDS.md).

RN gotcha: there is no `transform-origin` before React Native 0.76. RN 0.76+ adds a limited `transformOrigin` style prop that works for the common cases:

```tsx
<Animated.View style={[style, { transformOrigin: 'top left' }]} />
```

On older RN, fake it with the translate → scale → translate trick — translate the anchor point to the origin, scale, then translate back:

```ts
const ORIGIN_X = triggerX - popoverX; // offset from popover's own top-left to the trigger
const ORIGIN_Y = triggerY - popoverY;

const style = useAnimatedStyle(() => ({
  transform: [
    { translateX: ORIGIN_X }, { translateY: ORIGIN_Y },
    { scale: scale.value },
    { translateX: -ORIGIN_X }, { translateY: -ORIGIN_Y },
  ],
}));
```

Origin-aware popovers should scale from the trigger, not the center — same rule as the web. **Modals stay centered** and are exempt, same exception as the web rule.

## Reveal & clip (no clip-path)

> Web original: [STANDARDS.md → Transforms & clip-path](../review-animations/STANDARDS.md).

RN has no `clip-path` — there's no CSS engine underneath. Three options, in order of preference:

- **`overflow: 'hidden'` + an overlay `Animated.View` animating `scaleX`/`scaleY` from an edge.** Cheapest, fully GPU-driven via `transform`. Works for the reveal-on-scroll and hold-to-delete patterns the web rule describes — anchor the transform origin to the edge you're revealing from instead of animating `clip-path` inset values.
- **`@react-native-masked-view/masked-view`** for soft or gradient masks (a fade-to-transparent edge, a shaped cutout) that a hard-edged `overflow: hidden` can't express.
- **`@shopify/react-native-skia`** for true GPU clipping on complex reveal shapes (arbitrary paths, animated masks) — the RN equivalent of arbitrary `clip-path` shapes, at the cost of a heavier dependency.

Avoid animating a wrapper's `width` to reveal content — like the web rule, this forces a layout pass on the JS thread instead of running as a pure `transform` on the UI thread.

## Gestures & drag

> Web original: [STANDARDS.md → Gestures & drag](../review-animations/STANDARDS.md).

Gesture Handler v2 replaces pointer/touch event listeners with a declarative gesture object; Reanimated worklets keep the whole interaction on the UI thread:

```ts
const pan = Gesture.Pan()
  .onUpdate((e) => { translateY.value = e.translationY; })
  .onEnd((e) => {
    // velocity is px/s (web's 0.11 px/ms ≈ 110 px/s)
    if (Math.abs(e.translationY) > THRESHOLD || Math.abs(e.velocityY) > 500) {
      translateY.value = withTiming(SCREEN_H, { duration: 250, easing: easeOut }); // dismiss
    } else {
      translateY.value = withSpring(0, { velocity: e.velocityY }); // hand off velocity
    }
  });
```

Note the unit conversion: the web's velocity threshold (`~0.11` px/ms) is expressed in px/s by Gesture Handler, so the RN equivalent is roughly `~110` px/s — the constant in the example above (`500`) is set higher because `velocityY` on RN measures raw finger speed rather than a smoothed drag delta; tune per gesture.

**Momentum** without a hard endpoint: `withDecay({ velocity: e.velocityY, clamp: [0, MAX] })` — the RN analogue of momentum scrolling physics, with `clamp` doing the job of a boundary the web rule handles via damping.

**Rubber-banding at boundaries** — same "resistance increases with distance" rule as the web's damping-at-boundaries rule — via a friction function applied to the raw overshoot before it's written to the shared value:

```ts
function rubberBand(overshoot: number, dimension: number, c = 0.55) {
  'worklet';
  return (overshoot * dimension * c) / (dimension + c * Math.abs(overshoot));
}
```

Gesture Handler handles pointer capture and multi-touch protection natively — a single `Gesture.Pan()` already captures the touch for its lifetime and ignores additional fingers by default, so neither of the web rule's manual safeguards need to be hand-rolled.

## Layout Animations

Reanimated's layout animation system has no direct web equivalent in Emil's set — it's an RN-native strength worth calling out on its own, roughly covering what `@starting-style` plus a list library's enter/exit transitions would do on the web:

```tsx
import Animated, { FadeIn, FadeOut, LinearTransition, SlideInDown } from 'react-native-reanimated';

<Animated.View
  entering={FadeIn.duration(200)}
  exiting={FadeOut}
  layout={LinearTransition.springify()}
/>
```

`entering`/`exiting` animate mount/unmount automatically — no `useEffect` + `mounted` flag needed. `layout` animates any position/size change caused by a re-render (an item removed from a list, a container resizing) without manual FLIP math. Stagger group entrances with `FadeIn.delay(i * 50)` — same 30–80ms window as the web rule, same reasoning: longer delays feel slow, and stagger should never block interaction while it plays. Layout animations are interruptible by default, same advantage the web rule gives CSS transitions over keyframes.

## Reduced motion & hover

> Web original: [STANDARDS.md → Accessibility](../review-animations/STANDARDS.md).

```tsx
const reduce = useReducedMotion();
const translateY = reduce ? 0 : withTiming(offset, { duration: 200, easing: easeOut });
```

`useReducedMotion()` is Reanimated's hook equivalent of the web's `useReducedMotion()`/`prefers-reduced-motion` media query. For a one-off imperative check outside a component (e.g. before kicking off an imperative animation), use `AccessibilityInfo.isReduceMotionEnabled()` directly.

Same rule as the web: reduced motion means gentler, not zero. Drop the transform-based movement, keep opacity and color transitions that aid comprehension.

**Hover is not an RN concept** — there's no pointer hovering a touchscreen, so the web's `@media (hover: hover) and (pointer: fine)` gate has no RN mobile analogue; skip it entirely for phone/tablet targets. Footnote: it becomes relevant again only on RN-web (a real mouse) or tvOS (D-pad/remote focus states), where you're effectively back on a hover-capable input and the same gating logic applies.

## Materials, haptics, numbers, sheets

- **Blur / materials** — `expo-blur`'s `<BlurView>` or `@react-native-community/blur` for the frosted-glass look CSS gets from `backdrop-filter`. Note Android support is weaker/inconsistent (software blur fallback on older Android versions) — test on-device rather than trusting the simulator.
- **Haptics** — `expo-haptics` (`Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)`) or `react-native-haptic-feedback`. Apple's multimodal-harmony rule applies directly: fire the haptic on the same frame as the visual change, e.g. at the snap point inside a gesture's `.onEnd()`, not before or after it.
- **Tabular numbers** — `style={{ fontVariant: ['tabular-nums'] }}` keeps digits from shifting width during a counting/ticking animation, the RN equivalent of CSS `font-variant-numeric: tabular-nums`.
- **Bottom sheets** — `@gorhom/bottom-sheet` is the RN analogue of Vaul: it already implements momentum, snap points, and gesture velocity hand-off, so prefer it over hand-rolling a `Gesture.Pan()` + `withSpring` sheet unless you need behavior it doesn't expose.

## Debugging

> Web original: [STANDARDS.md → Debugging](../review-animations/STANDARDS.md).

- **Slow motion** — Reanimated's animations respect a global slow-animation dev toggle; alternatively multiply durations by 2–5× temporarily, or wrap values in a logger (`useAnimatedReaction` printing to console) to inspect timing.
- **Real devices for gestures** — Gesture Handler behavior (especially multi-touch and native scroll interop) can differ from simulator/emulator; test drawers and swipes on physical hardware before shipping.
- **JS-thread vs UI-thread frame drops** — use React Native's Perf Monitor overlay or Flipper's React Native performance plugin to see which thread is dropping frames; a worklet-driven animation stuttering points at UI-thread contention (heavy native rendering), while a legacy `Animated` animation stuttering without `useNativeDriver` points at JS-thread contention.
- **Fresh eyes next day** — same as the web rule: imperfections invisible during development surface later. Review animations again after stepping away.
