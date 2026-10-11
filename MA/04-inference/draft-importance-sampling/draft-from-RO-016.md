# Moved from RO-016 on 2026-10-10: importance sampling

From RO-016 (Particle Filter) §4.2.1. Context: a particle filter's particles after the move step are samples of the predicted belief $\overline{\text{bel}}(x)$; the update is $\text{bel}(x) = \eta\ p(z \mid x)\ \overline{\text{bel}}(x)$. The "Check on the corridor" that followed was deleted, not moved. Glossary rows to restore:

| <span id="G-2495">G-2495</span> | Importance sampling | Drawing samples from a distribution we can sample (the proposal) and weighting each by target over proposal, so the weighted samples stand for a distribution we cannot sample directly (the target). | [Note RO-016](RO/localization/02-bayes-filters/RO-016-particle-filter/RO-016-particle-filter.md#421-why-weighting-gives-the-right-belief-importance-sampling) | Particle filter |
| <span id="G-2496">G-2496</span> | Proposal distribution | In importance sampling, the distribution the samples are actually drawn from; in a particle filter, the predicted belief produced by the move step. | [Note RO-016](RO/localization/02-bayes-filters/RO-016-particle-filter/RO-016-particle-filter.md#421-why-weighting-gives-the-right-belief-importance-sampling) | Particle filter |
| <span id="G-2497">G-2497</span> | Target distribution | In importance sampling, the distribution we want samples from but cannot draw directly; in a particle filter, the updated belief after a reading. | [Note RO-016](RO/localization/02-bayes-filters/RO-016-particle-filter/RO-016-particle-filter.md#421-why-weighting-gives-the-right-belief-importance-sampling) | Particle filter |

We want particles drawn from the updated belief $\text{bel}(x)$, but we cannot draw from it directly: its shape is the unknown we are computing. What we have are particles drawn from the predicted belief $\overline{\text{bel}}(x)$, because the move step (Section 4.4) produces them. The trick is to keep those particles and correct for the mismatch with weights.

The distribution we want samples from is the **target distribution** (G-2497), $f$; the one we can sample from is the **proposal distribution** (G-2496), $g$. A sample drawn from $g$ at a place where $f$ is twice as high as $g$ should count twice. So each sample gets the weight

$$w = f(x) / g(x)$$

and a weighted set of samples from $g$ then stands for $f$. Drawing from one distribution and weighting by the ratio to stand for another is **importance sampling** (G-2495) (Freiburg PF slides; Labbe ch.12). It needs $g$ to be above zero wherever $f$ is.

For the particle filter, the target and the proposal are the two sides of the update formula:

$$f(x) = \eta\ p(z \mid x)\ \overline{\text{bel}}(x)$$

$$g(x) = \overline{\text{bel}}(x)$$

Their ratio is

$$\frac{f(x)}{g(x)} = \eta\ p(z \mid x)$$

so the weight is just the sensor model, up to the constant $\eta$ that normalising removes (Freiburg PF slides). That is the weight of Section 4.2.
