# fg-formatfix (class-level patch on top of Slimefun-f172239-Beta)

Makes the shared `DecimalFormat` instances thread-safe (one instance per thread via `ThreadLocal`):

- `NumberUtils.DECIMAL_FORMAT` (`#.##`) - used by `getCompactDouble`, `roundDecimalNumber`, `getAsMillis`, `reparseDouble`, `EnergyNet` holograms
- `LoreBuilder.hungerFormat` (`#.0`)
- `TapeMeasure.format` (`##.###`)
- shaded `DoughTimings.FORMAT` (`0.########`) - `DoughTimings.java` here is the shaded dough class patched the same way (it lives in a dependency, not in this repo)

Patterns, locales and rounding are unchanged. Origin: a JVM native crash in a Slimefun scheduler thread on a busy server
(2026-09-18); the unsynchronised formatter race is a confirmed risk, not a proven sole cause.

Build: compile the 3 repo classes (package names relocated to `io.github.thebusybiscuit.slimefun4.libraries.*` as in the shadow jar)
plus `DoughTimings.java` against the published `Slimefun-<commit>-Beta.jar`, then
`python sf_patch_jar.py <orig.jar> <classes-dir> <out.jar> <commit>-Beta <commit>-Beta-fg-formatfix.1`.
Verified with a 558M-operation concurrent stress test (`-Xverify:all`, strict): 0 mismatches.
