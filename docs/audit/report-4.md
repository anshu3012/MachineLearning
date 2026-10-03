# Claims audit, group 4

29 Notes checked (123–134, 210–231, 240–261). 130 findings: 108 UNSUPPORTED, 17 WRONG FACT and 5 WRONG CITATION. All edited folders were rebuilt. Every Note had findings.

## Counts per Note

123: 9 · 124: 6 · 125: 2 · 126: 4 · 127: 3 · 128: 2 · 129: 6 · 130: 3 · 131: 5 · 132: 6 · 133: 11 · 134: 14 · 210: 5 · 220: 2 · 221: 5 · 222: 2 · 223: 1 · 230: 2 · 231: 2 · 240: 3 · 241: 2 · 242: 3 · 243: 7 · 250: 5 · 251: 2 · 252: 4 · 253: 1 · 260: 8 · 261: 5

## Wrong facts and wrong citations (fixed)

| Note | Claim | Fix |
|---|---|---|
| 126 | "log loss: even a single leaf has no simple formula" | reworded; the derivation is in an Extra |
| 129 | k-means++ described as plain D² sampling | scikit-learn runs greedy k-means++ (KMeans docs) |
| 130 | "n_init and k-means++ do exactly this job" | only n_init restarts |
| 132 | MinPts = "number of columns + 1" | WRONG CITATION; Ester 1996 §4.2 gives MinPts = 4 for 2-D data |
| 132 | the visualiser's features | WRONG CITATION; reworded to the Harris page |
| 133 | "almost every model accepts sample_weight" | "many"; KNeighborsClassifier does not |
| 134 | TPE good group "about the best 10%" | Optuna default: 10%, at most 25 (Bergstra 2011) |
| 134 | "flat lines after trial 30" | no study improved after trial 29 |
| 134 | importances "computed with fANOVA" | the Optuna 5.0 default is PED-ANOVA (Watanabe 2023) |
| 134 | SVM scaled "because it measures distances" | WRONG CITATION; scikit-learn SVM tips |
| 220 | "sample average is close to the national average" | the lecture says the two can be very different |
| 221 | "μ and x̄ are usually close" | reworded |
| 221 | diving drops the highest and lowest score | diving drops the 2 highest and 2 lowest of 7 (USA Diving) |
| 230 | a long whisker means the middle half is lopsided | a long whisker shows a longer tail |
| 243 | `sns.distplot` "removed" | deprecated, not removed (seaborn 0.13) |
| 251 | CLT: "almost any distribution" gives normal averages | approximately normal, and it needs a finite variance (Pishro-Nik §7.1.2) |

## Tested claims (selection)

- **123:** missing-value direction: cross-validation 0.828 / 0.834.
- **124:** γ = 2 keeps both splits; γ = 3 removes both.
- **126:** the gap shrinks from 0.055 to 0.009 over 100 trees.
- **127:** K = 2 vs K = 10 out-of-fold log loss is 0.238 vs 0.215. Blending vs stacking over 30 splits is 0.806 vs 0.809, which is chance.
- **129:** ARI 1.0. Nearest-centroid distance ratios are 1.08 raw and 2.56 scaled.
- **131:** Ward distance 2.380 in both scipy and scikit-learn; `affinity` raises a TypeError in scikit-learn 1.9.
- **133:** with real rows only, F1 is 0.398 (the leaky score was 0.885).
- **134:** reshuffled cross-validation averages 0.772, not 0.790. Median imputation leaves accuracy at 0.745. CV noise (0.760–0.795) is wider than the gaps between samplers. SVC trials range from 0.650 to 0.780.
- **241:** over 1,000 repeats of 100 rolls, the median lowest share is 0.12 and the median highest is 0.22.
- **243:** the log density is −1328.8 while its exponential underflows to 0. With the bandwidth fixed, about 16 peaks at n = 1,000 and 3.1 at n = 100,000.
- **250:** the integral is checked numerically (2.5066).
- **260:** pandas vs scipy 0.478 vs 0.461 at n = 500; 35 distinct sepal lengths; Laplace ends −5.41 / 4.82.

## Sources added (selection)

- Chen and Guestrin 2016; the XGBoost, Optuna, scikit-learn, imblearn, SciPy, seaborn and statsmodels docs.
- Textbooks: ESL, ISLR, MML, Pishro-Nik, Wasserman 2004, Silverman 1986, Taylor 1997, Bruce et al. 2020.
- Papers: Ester 1996, Arthur and Vassilvitskii 2007, Chawla 2002, Lin 2017, Shahriari 2016, Jones 1998, Bergstra 2011, Cawley and Talbot 2010, Hutter 2014, Watanabe 2023, Rousseeuw 1987, Schubert 2022, Stevens 1946, Akoglu 2018, Joanes and Gill 1998, Doane and Seward 2011, von Hippel 2005, Bulmer 1979, Westfall 2014, Ghasemi and Zahediasl 2012, Clementi and Gallegati 2005, Prokhorenkova 2018, Sigrist 2021.

## UNRESOLVED (removed from Note)

- **123 §7.7:** "the GPU's fixed cost only pays off on much bigger datasets." Testing it needs the GPU, which agents may not use.
- **127:** "the reason a larger K is usually preferred."
- **127 §9.3:** "holding 49 out hurts both models." The 30-split test refuted this.
- **128:** "the elbow method stays the most common first look."
- **134:** "smarter search pays off most on larger data and with more hyperparameters."
- **134:** "this is why comparing algorithms by their default settings can mislead."
- **260 §8:** "the more the line's slope has to change."

## Restored intuitions

124, 126, 127, 221, 222, 223 and 251.

## For the citation check

- **Taken from search summaries, not opened:**
  - Wilcox 2012 (the 20% trim);
  - the FIG Code of Points;
  - Bulmer 1979 (checked only through secondary sources);
  - Davis 2000 (via *Discover*).
- **Weaker than a textbook:**
  - Wikipedia, "XGBoost" (123);
  - Oja, LibreTexts (231).
- **Notebook cells without saved outputs:** 124, 125, 126, 127 and 129. These cells were run as standalone scripts.
