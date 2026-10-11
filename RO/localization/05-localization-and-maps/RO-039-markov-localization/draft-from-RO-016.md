# Moved from RO-016 on 2026-10-10: the particle filter among the Bayes filters

From RO-016 (Particle Filter) §6, whole (text, table and its Sources paragraph). "Our corridor" is RO-016's 10 m looped corridor with three doors. No glossary rows.

## 6. The particle filter among the Bayes filters

> **Key point:** All three filters run the same predict and update; they differ in how they store the belief, which decides what shapes they can hold and what they cost.

| | Grid filter | Particle filter | Kalman filter |
|---|---|---|---|
| Belief stored as | one number per cell | $M$ weighted samples | a mean and a covariance |
| Shapes it can hold | any, at the grid's resolution | any, given enough particles | one bell curve |
| Models it needs | any | any we can sample from and evaluate | linear, with Gaussian noise |
| Cost grows with state dimension | very fast | fast | slowly |
| Our corridor | works | works | fails after reading 1 |

Sources: Labbe ch.12 (summary); Freiburg PF slides; Freiburg KF slides. The [Kalman filter](../RO-017-kalman-filter/RO-017-kalman-filter.md#22-a-gaussian-is-two-numbers) is the cheapest when its conditions hold, and its extended form handles curved models with one bump ([extended Kalman filter](../RO-018-extended-kalman-filter/RO-018-extended-kalman-filter.md#41-the-algorithm)); the particle filter is the choice when the belief has several bumps, as in our corridor or in a robot that must find itself on a map from scratch.
