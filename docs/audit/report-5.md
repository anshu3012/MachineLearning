# Claims audit, group 5

22 Notes checked: 262, 270–272, 280–282, 290–292, 300–302, 330–332, 340, 341, 350, 360–362. All 22 were rebuilt, and each printed "Built".

Totals: 58 findings. 48 UNSUPPORTED, 8 WRONG FACT and 2 WRONG CITATION.

## Findings

| Note | quote (short) | verdict | action |
|---|---|---|---|
| 262 | "Pareto found this pattern while studying how land and wealth were distributed" | UNSUPPORTED | sourced: Pareto, *Cours d'économie politique* (1896–97); "land" removed |
| 262 | Extra: share held by the top p is p^(1−1/α) | UNSUPPORTED | derived in the Note from the CDF and the mean integral |
| 262 | "income is closer to log-normal; the Pareto tail describes the richest few percent" | UNSUPPORTED | sourced: Clementi and Gallegati (2005) |
| 262 | "the few largest values, which are always noisy" | UNSUPPORTED | tested (cell 6); reworded |
| 262 | Q-Q: "biggest values vary a lot from sample to sample" | UNSUPPORTED | tested: std/mean is 1% for the 500th value and 55% for the largest |
| 270 | "Bernoulli Naive Bayes assumes each input is a Bernoulli variable" | UNSUPPORTED | sourced: scikit-learn user guide §1.9.4 |
| 270 | Extra: categorical distribution | UNSUPPORTED | sourced: Murphy (2012) §2.3.2 |
| 270 | Extra: binomial skewness formula | UNSUPPORTED | sourced: Johnson, Kemp and Kotz (2005) ch. 3; tied to scipy values |
| 270 | "they get closer with more runs" | UNSUPPORTED | tested (cell 7): the gap is 0.095 at 100 runs, 0.015 at 1,000 and 0.0015 at 100,000 |
| 271 | "uniform (everyone earns the same)" | WRONG FACT | reworded: every salary in the range is equally likely |
| 271 | Extra: "the only shape that stays the same when we add copies is the normal" | WRONG FACT | sourced: Feller Vol. II §VI.1; Fischer (2011); "cancel" intuition removed |
| 271 | "for a nearly symmetric population, much smaller samples suffice" | UNSUPPORTED | derived (γ₁/√n, γ₂/n) and tested |
| 271 | "a single huge value can dominate, so the means never settle" | UNSUPPORTED | sourced: Gnedenko and Kolmogorov (1954); tested |
| 271 | "tests on regression coefficients rely on normality from the CLT" | UNSUPPORTED | sourced: Wooldridge, ch. 5 |
| 272 | "one sample of 50 holds far less information than 100 samples of 50" | UNSUPPORTED | derived: σ/√50 vs σ/√5000 |
| 272 | "100 samples of 50 hold no more information than one sample of 5000" | UNSUPPORTED | derived |
| 272 | Extra: "a sample of 50 often misses expensive tickets" | UNSUPPORTED | tested (cell 8b, 2000 runs) |
| 272 | 87.9% vs 95.6% compared across different runs | WRONG FACT | reworded; same-run value 89.0% |
| 280 | "First class has few passengers, so its interval is wide" | WRONG FACT | tested: 216 vs 184 passengers; the cause is the spread (s = 78 vs 12) |
| 280 | Extra: seaborn bootstrap gives "almost the same range" | UNSUPPORTED | sourced: seaborn docs v0.13; tested |
| 280 | "z-procedure comes first because it is simpler" | UNSUPPORTED | reworded to the maths of Note 282 |
| 281 | Extra: Bayesian credible intervals | UNSUPPORTED | sourced: Pishro-Nik (2014) §9.1.9 |
| 281 | "medical and safety use 99%, business 90%" | UNSUPPORTED | reworded to the transcript; field claims removed |
| 282 | "linked observations, interval too narrow" | UNSUPPORTED | tested: coverage 74.1% vs 95.2% |
| 282 | Gosset "a chemist at Guinness, barley and beer" | UNSUPPORTED | sourced: Student (1908); Zabell (2008); the detail removed |
| 282 | t-distribution "inherits the same count" | UNSUPPORTED | sourced: Casella and Berger §5.3 |
| 282 | Extra: bootstrap as the fix for skewed fares | UNSUPPORTED | sourced: Efron and Tibshirani (1993) ch. 13; tested: no better than the t-interval |
| 290 | "Some books write H0: μ ≤ 6; same calculation" | WRONG CITATION | derived |
| 290 | "small sample, absence of evidence" | UNSUPPORTED | sourced: Altman and Bland (1995) BMJ 311 |
| 290 | "choosing α or direction after the results" | UNSUPPORTED | derived: real α = 0.10 |
| 291 | "choosing α after the result" | UNSUPPORTED | derived |
| 292 | "Many books label it accept H0" | WRONG CITATION | reworded |
| 292 | SelectKBest; Shapiro-Wilk | UNSUPPORTED | sourced: scikit-learn docs; Shapiro and Wilk (1965) |
| 300 | Extra: six misreadings of p | UNSUPPORTED | sourced: Greenland et al. (2016) |
| 301 | Shapiro-Wilk power at n = 25 vs thousands | UNSUPPORTED | sourced: Ghasemi and Zahediasl (2012); tied to the Note's p-values |
| 302 | Extra: Welch by default | UNSUPPORTED | sourced: Delacre, Lakens and Leys (2017); tied to the data |
| 302 | Extra: paired t-test on CV folds is overconfident | UNSUPPORTED | sourced: Dietterich (1998); Nadeau and Bengio (2003) |
| 302 | "a hard fold is hard for both models" | WRONG FACT (on this data) | tested: correlation 0.11; pairing gains nothing here |
| 302 | "before-and-after studies by far the most common" | UNSUPPORTED | reworded to the transcript |
| 330 | Extra: partition and Bayes | UNSUPPORTED | sourced: Orloff and Bloom, MIT 18.05 Class 3 |
| 331 | "a gap of this size is normal with 200 draws" | UNSUPPORTED | derived: SD 0.032 |
| 331 | Axioms of probability | UNSUPPORTED | sourced: Grinstead and Snell §1.2; MML §6.1.2 |
| 331 | "Two facts follow at once" | UNSUPPORTED | derived |
| 331 | "ML works almost entirely from data" | UNSUPPORTED | narrowed to the Naive Bayes example |
| 332 | "expectation rules need no independence" | UNSUPPORTED | sourced: Grinstead and Snell §6.1–6.2 |
| 332 | Extra: σ²/n "is why bagging reduces variance" | WRONG FACT | sourced: ESL §15.2 eq. 15.1 (correlated formula) |
| 341 | "Bayes' theorem matters when the combination never appears" | WRONG FACT | derived: 2¹⁰ combinations > 891 rows; the fix is the Naive Bayes assumption |
| 341 | "class is a useful input for survival" | UNSUPPORTED | reworded to the data |
| 350 | Extra: QR and SVD in practice | UNSUPPORTED | sourced: Trefethen and Bau, Lecture 11; Koren, Bell and Volinsky (2009) |
| 350 | Extra: MML "matches this roadmap" | UNSUPPORTED | reworded to the chapter list |
| 360 | "this is why deep learning is built on linear algebra" | UNSUPPORTED | sourced: Goodfellow et al. §12.1.2 |
| 360 | "same species sit close together" | UNSUPPORTED | tested: nearest-neighbour accuracy 96.0% vs 34.7% with labels shuffled |
| 360 | Extra: one-hot is safer | UNSUPPORTED | sourced: scikit-learn §8.3.4 |
| 361 | Extra: scalar plus vector | UNSUPPORTED | sourced: MML Def. 2.9; NumPy broadcasting guide |
| 361 | "the magnitude is multiplied by \|s\|" | UNSUPPORTED | derived |
| 362 | Extra: "the cross product exists only in 3D" | WRONG FACT | sourced: Massey (1983); a 7D cross product also exists |
| 362 | Extra: cosine similarity in search | UNSUPPORTED | sourced: Manning, Raghavan and Schütze §6.3.1 |

## UNRESOLVED (removed from Note)

- 262: "land" in Pareto's data.
- 271: the "large and small values cancel" intuition.
- 281: "medical and safety use 99%, business 90%" and "below 90% misses too often".
- 282: Gosset was "a chemist" working on "barley and beer".
- 331: "machine learning works almost entirely from data".
- 362: the cross product "is central in physics and 3D graphics".

## Other changes

- 290: "YouTube channel" changed to "video channel".
- Notebooks with new or extended experiment cells: 262, 270, 271, 272, 282, 302, 360.
