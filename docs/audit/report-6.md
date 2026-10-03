# Claims audit, group 6

23 Notes checked (363–621). 83 findings: 77 UNSUPPORTED, 6 WRONG FACT and 0 WRONG CITATION. All 23 Notes were rebuilt.

Every Note had findings. Each edited Note now uses short citation tags in the text and has a `## Sources` list.

## Wrong facts (fixed)

| Note | Claim | Fix |
|---|---|---|
| 500 | "the bias and the activation let a network learn curved boundaries" | Only the activation bends the boundary (Goodfellow §6.1, the XOR example). |
| 571 | χ² follows the chi-square distribution "because each (O−E)/√E is standard normal" | The terms are not independent, and the fixed total costs one degree of freedom (Pearson 1900). Simulation: mean χ² 1.99 for df 2; 4.9% of samples exceed the 5% critical value. |
| 571 | sklearn `chi2` on one-hot columns "matches the test of independence" | The two scores are 170.3 and 92.7. Only their sum, 263.1, equals χ². |
| 600 | `np.sin` uses Taylor-like polynomials | Fixed (Muller 2016). |
| 613 | sklearn PCA `auto` solver thresholds | Fixed to match the scikit-learn 1.9 docs. |
| 620 | "strong duality holds for convex problems" | It also needs Slater's condition (Boyd and Vandenberghe §5.2.3). |

## Unsupported claims

The 77 unsupported claims were grounded in three ways:

**Sourced:**
- textbooks: MML, ESL, ISLR, Goodfellow, Boyd and Vandenberghe, Trefethen and Bau, Nocedal and Wright, Bishop, Montgomery, Ross, OpenIntro, Thrun;
- reference pages: NIST;
- papers: Koren et al. 2009, Page et al. 1999, Maher 1982, Yates 1934, Cochran 1954, Cramér 1946, Welch 1951, Kruskal and Wallis 1952, Tukey 1949, Kleinberg et al. 2018, Rezende and Mohamed 2015, Baydin et al. 2018, Eckart and Young 1936, Wallace 1991, Gavish and Donoho 2014, Deerwester et al. 1990, Funk 2006, Penrose 1956, Bengio et al. 2013, Kaufman et al. 2012, Chen and Guestrin;
- official docs: scikit-learn, NumPy, SciPy and PyTorch.

**Derived:** 363, 560, 590.

**Tested:**
- **560, overdispersion:** a varying rate gives variance 11.99 and P(Y≥12) = 0.038, against 0.0009 for the Poisson.
- **560, rule of thumb:** the largest gap is 0.0095 at the edge of the rule and 0.023 at p = 0.2.
- **570:** adults only, r falls from 0.98 to 0.92.
- **571:** with one parameter estimated, mean χ² is 3.06 (df 3, not 4).
- **571:** n = 8 still gives 5.0% false alarms.
- **572:** familywise error simulated at 11.0% and 29.0%, against the formula's 14% and 40%; ANOVA stays at 5.0%.
- **603:** BFGS's B is ≥94% off the true Hessian for steps 0–6, and within about 30% from step 7.
- **612:** the predicted noise edge of 7.1 matches the observed floor of 5–7.

**Reworded:** 440, 580, 600, 602, 612, 613.

**Kept as sourced intuitions:** 490 (embeddings as new coordinates), 572 (the 14%/40% formula) and 612 (the noise floor).

## Counts per Note

363: 1 · 440: 3 · 490: 3 · 500: 2 · 510: 1 · 520: 1 · 530: 4 · 560: 6 · 570: 3 · 571: 7 · 572: 6 · 580: 2 · 590: 6 · 600: 4 · 601: 2 · 602: 6 · 603: 4 · 610: 2 · 611: 2 · 612: 5 · 613: 7 · 620: 3 · 621: 3

## UNRESOLVED (removed from Note)

- 621: "Almost every convex problem met in ML satisfies Slater's condition."

## Other changes

- New experiment cells in the 560, 571 and 572 notebooks.
- A Hessian-gap check in 603's `optimizer_race.py`.
