# Moved from RO-008 on 2026-10-10: normal and triangular noise from uniform random numbers

Source: RO/localization/02-bayes-filters/RO-008-probabilistic-motion-models, §5.2 (whole subsection, Figure 6 there) and the §7 Extra box on rejection sampling. Figure: images/sampling (sampling.py imports gifkit.py from RO-008's images folder for its colours). Notebook cell: notebook-cells-from-RO-008.json.

Glossary row to restore:

| <span id="G-2327">G-2327</span> | Triangular distribution | A distribution whose density is a triangle, highest in the middle and zero beyond a hard edge; used for motion noise when errors are known never to exceed a bound, and sampled as a scaled sum of two uniform numbers. | [Note RO-008](RO/localization/02-bayes-filters/RO-008-probabilistic-motion-models/RO-008-probabilistic-motion-models.md#52-normal-and-triangular-noise-from-uniform-random-numbers) | Probabilistic motion models |

Wording removed from G-2330 (Rejection sampling), which stays in RO-008: "and, more generally, to sample from any density that can be computed".

### 5.2 Normal and triangular noise from uniform random numbers

Every computer can draw **uniform** random numbers: any value in a range, such as from $-b$ to $b$, equally likely, the [uniform distribution](../../../MA/03-distributions/MA-029-uniform-and-log-normal/MA-029-uniform-and-log-normal.md#2-the-uniform-distribution) (G-2043). We build the other noises from it (Freiburg slides). Figure 6 checks each recipe with 20 000 draws, for $b = 0.1$.

![Left: 20 000 uniform numbers between -0.1 and 0.1 form a flat block. Middle: half the sum of 12 of them forms a bell that matches the normal density with standard deviation 0.1. Right: the square root of 6 over 2 times the sum of 2 of them forms a triangle that matches the triangular density with standard deviation 0.1](images/sampling.png)

**Normal noise with standard deviation $b$.** Add 12 uniform numbers from $-b$ to $b$ and halve the sum (Freiburg slides):

$$\text{sample} = \frac{1}{2}\sum_{i=1}^{12} \text{rand}(-b,\ b)$$

Why a bell: a sum of many independent random numbers is close to normal, whatever their own shape, by the [central limit theorem](../../../MA/04-inference/MA-033-sampling-distribution-and-clt/MA-033-sampling-distribution-and-clt.md#4-the-central-limit-theorem) (G-364); twelve is already enough for the eye in Figure 6. Why standard deviation $b$: one uniform number from $-b$ to $b$ has variance $b^2/3$, and for independent numbers [variances add](../../../MA/04-inference/MA-033-sampling-distribution-and-clt/MA-033-sampling-distribution-and-clt.md#42-mean-and-variance-of-the-sample-means). Halving divides the variance by 4:

$$12 \times \frac{b^2}{3} = 4b^2$$

$$\frac{4b^2}{4} = b^2$$

So the standard deviation is $b$; the notebook measures 0.1002 for $b = 0.1$.

**Triangular noise with standard deviation $b$.** Add only 2 uniform numbers and scale by $\sqrt{6}/2$. Two dice show why the result is a triangle: a total of 7 can be made in six ways, a total of 2 or 12 in only one. The variance check:

$$2 \times \frac{b^2}{3} \times \frac{6}{4} = b^2$$

A **triangular distribution** (G-2327) has a hard edge: it never gives noise larger than $\sqrt{6}\thinspace b$, about 2.45 times $b$. The normal distribution allows any size of error, however rarely, which for a robot would mean being carried off to another room. If a robot's error is known to stay within a bound, the triangular distribution says so.

## Also moved from RO-008: rejection sampling for any density

> **Extra:** Rejection sampling also draws samples from any density $f$ we can compute but not sample directly (Freiburg slides). Draw a value $x$ uniformly over the range of $f$, and a height $y$ uniformly from 0 to the largest value of $f$. Keep $x$ if the point $(x, y)$ lies under the curve, $y < f(x)$; otherwise reject it and draw again. Values where $f$ is high are kept more often, in proportion to $f$.
