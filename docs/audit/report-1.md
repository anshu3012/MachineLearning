# Claims audit, group 1 (Notes 35–62)

28 Notes checked. 129 findings: 106 UNSUPPORTED, 20 WRONG FACT, 3 WRONG CITATION. Every Note had at least one finding. All 28 Notes rebuilt and printed "Built".

Each Note now has a Sources list just before the Key terms. The text uses short citation tags. Long proofs and experiments sit in Extra boxes. Good intuitions are kept.

## Findings

| Note | quote (short) | verdict | action |
|---|---|---|---|
| 35 | "since versions 1.3 and 1.4, decision trees and random forests" accept NaN | UNSUPPORTED | sourced: scikit-learn User Guide "Estimators that handle NaN values"; release highlights 1.3 and 1.4 |
| 35 | MCAR / MAR / MNAR Extra | UNSUPPORTED | sourced: Rubin, "Inference and Missing Data", Biometrika 63(3), 1976 |
| 35 | "We cannot prove … MCAR, because the values that would tell us are missing" | UNSUPPORTED | sourced and reworded: Little, "A Test of MCAR…", JASA 83(404), 1988 |
| 35 | "A value of 20 stands for 'more than 20 years'" | UNSUPPORTED | removed (UNRESOLVED; only a blog backed it); tall bar now explained by counts only: 3,434 rows at 20 vs 304 at 19 |
| 36 | "This is called data leakage" | UNSUPPORTED | sourced: scikit-learn User Guide, Common pitfalls, "Data leakage" |
| 36 | "Both skip missing values pair by pair" | UNSUPPORTED | sourced: pandas `DataFrame.cov` / `DataFrame.corr` docs |
| 36 | "A column with no values at all is dropped…" | WRONG FACT | sourced and corrected: scikit-learn `SimpleImputer` API (only when strategy is not "constant") |
| 36 | "Feature-engine use Q3 + 3×IQR by default" | WRONG FACT | sourced and corrected: Feature-engine `EndTailImputer` docs |
| 37 | "results are usually no better than with mode imputation" | UNSUPPORTED | removed (UNRESOLVED); transcript's "not always good" kept |
| 37 | "So the gaps are probably not random" | UNSUPPORTED | derived: MCAR definition plus price gap (102,000 vs 188,000 dollars) |
| 37 | "in pandas 3, fillna(inplace=True) on a single column no longer changes…" | UNSUPPORTED | sourced: pandas User Guide, Copy-on-Write |
| 37 | Empty FireplaceQu = "no fireplace", GarageQual = "no garage" | UNSUPPORTED | sourced: De Cock, J. Stat. Education 19(3), 2011 |
| 37 | "So the gaps are MNAR … This explains why houses with a gap sold for less" | UNSUPPORTED | "missing because the thing does not exist" kept, sourced: De Cock 2011; price link removed (UNRESOLVED) |
| 38 | "and keeping the shape matters less to them" (trees) | UNSUPPORTED | kept as a labelled intuition (trees split on order), which points the right way |
| 38 | "A model, especially a linear one, would learn a weaker link" | UNSUPPORTED | reworded to the observation plus the transcript point |
| 38 | Imputer settings tie "because mean and median are close" | UNSUPPORTED | tested: Age = 0 → 78.8%, Age = 99 → 78.9%, Age removed → 78.8%; Age barely matters, so no fill could change the score |
| 38 | "On a bigger dataset … the scores would separate" | UNSUPPORTED | tested: same experiment, written into the Note |
| 38 | "report test score, not CV score, because the settings were chosen to maximise it" | UNSUPPORTED | sourced: Cawley & Talbot, JMLR 11, 2010 |
| 39 | nan-Euclidean weight rationale | UNSUPPORTED | sourced: scikit-learn `nan_euclidean_distances` docs; Dixon, IEEE Trans. SMC 9(10), 1979 |
| 39 | "The fewer columns two rows share, the less reliable their distance" | UNSUPPORTED | derived: row 4's distance could be 2.45 or 42.94 depending on unknown f2 |
| 39 | "In scikit-learn, those rows are called donors" | WRONG CITATION | sourced and corrected: User Guide wording; "potential donors" in `KNNImputer` source |
| 39 | "neighbours chosen almost only by Fare"; scaling gives a fair say | UNSUPPORTED | tested: scaling changes 74% of fills, accuracy stays 0.704; sourced: `StandardScaler` API |
| 40 | IterativeImputer stores models, not rows | UNSUPPORTED | sourced: scikit-learn API, `imputation_sequence_` |
| 40 | "fits those rows exactly and extrapolates wildly" | UNSUPPORTED | tested: residuals 0.00 at settled values; two gap inputs outside training range (maths shown) |
| 40 | "experimental … may change without warning" | UNSUPPORTED | sourced and reworded: scikit-learn docs ("without a deprecation cycle") |
| 40 | "R&D and Marketing are strongly related, so each helps predict the other" | UNSUPPORTED | tested: shuffling each column alone raises iterative error to 8.10, worse than mean imputer 7.78 |
| 40 | MICE originally means multiple imputation | UNSUPPORTED | sourced: Rubin 1987; van Buuren & Groothuis-Oudshoorn, JSS 45(3), 2011 |
| 41 | "median … is only 18,500 rupees" (salaries never given) | UNSUPPORTED | derived: listed the nine salaries, (18,000 + 19,000)/2 |
| 41 | Trees depend only on order, so input outliers barely matter | UNSUPPORTED | sourced: Hastie, Tibshirani & Friedman, *ESL* 2nd ed., 2009, §10.7 |
| 41 | "Also affected: … KNN … PCA … SVMs" | WRONG FACT | sourced and corrected: ESL Table 10.1 rates k-NN robust to input outliers; k-means (ESL §14.3.10), SVM, StandardScaler kept; PCA kept, sourced: Hubert et al., ROBPCA, Technometrics 47(1), 2005; KNN removed (UNRESOLVED) |
| 41 | GBM with squared error is pulled by outliers; Huber loss helps | UNSUPPORTED | sourced: ESL §10.6 and §10.9 |
| 42 | "A few very large outliers can stretch the standard deviation so much that they end up inside the limits" | UNSUPPORTED | sourced: Shiffler, "Maximum Z scores and outliers", Am. Stat. 1988; NIST e-Handbook 1.3.5.17 (max z ≤ (n−1)/√n; for n = 10 that is 2.85) |
| 42 | "cgpa … has 67.9%, 95.7% and 99.5%" | UNSUPPORTED | tested: new notebook cell gives 0.679 / 0.957 / 0.995 |
| 42 | "In this data no CGPA lies in that gap" | UNSUPPORTED | tested: same cell shows 0 values in each gap |
| 42 | "On a skewed column the mean and standard deviation are pulled towards the long tail…" | UNSUPPORTED | tested: marks column mean 32.23 > median 28; limits −25.17 and 89.62, so the lower limit can never fire; 8 flagged (0.8%), not 0.3% |
| 43 | "The factor 1.5 is a convention from John Tukey … some people use 3" | UNSUPPORTED | sourced: Tukey, *Exploratory Data Analysis*, 1977; NIST e-Handbook 7.1.6 |
| 43 | "each round would move the fences in and flag new values" | WRONG FACT | tested: repeated trimming stops after 2 rounds (984 rows left) |
| 43 | "percentiles, which do not care about the shape" | UNSUPPORTED | kept as an intuition (percentiles exist for any shape) |
| 43 | "the far tail is often genuine" | UNSUPPORTED | reworded: "can be perfectly genuine", with data: 15 real marks 86–100 ("often" dropped) |
| 43 | "lower fence is often below every possible value" | UNSUPPORTED | reworded with data: "can" be, as here (−23.5) |
| 44 | "Other tools use slightly different rules" | UNSUPPORTED | sourced: pandas `Series.quantile` docs; Hyndman & Fan, Am. Stat. 1996 (definition 7) |
| 44 | "Charles P. Winsor (1895 to 1951), an engineer … Tukey named it" | WRONG CITATION | sourced: Hastings, Mosteller, Tukey & Winsor, Ann. Math. Stat. 1947; Brillinger, "Tukey, John Wilder" |
| 44 | "On the test set they are only close to 1%, which is expected" | UNSUPPORTED | sourced (maths): Binomial(2000, 0.01) mean 20, sd 4.4; observed 23 and 16 lie within one sd |
| 44 | "Weight, with almost no outliers" | UNSUPPORTED | tested: 1 value beyond IQR fences, 200 beyond 1st/99th percentiles |
| 44 | "Winsorization is often used exactly this way: to calm the tails…" | UNSUPPORTED | kept as an intuition ("calms the tails; does not hunt for errors"); usage claim "often used" dropped |
| 45 | "A ratio often says more than either of its parts, because it removes the effect of size" | UNSUPPORTED | sourced in part: Kuhn & Johnson, *Feature Engineering and Selection*, 2019, Sec 1.1; "removes the effect of size" kept as an intuition (price per square foot) |
| 45 | "The usual definition of tidy data, from … Hadley Wickham" | UNSUPPORTED | sourced: Wickham & Grolemund, *R for Data Science*, 2017, Sec 12.2 |
| 45 | "group rare titles into one category" | UNSUPPORTED | sourced: scikit-learn User Guide, "Infrequent categories" |
| 45 | "Adding the Sex column instead gives 80.2%" | WRONG FACT | tested: 80.5% on the same 10×10 CV |
| 45 | "the title does a little better because 'Master' also marks young boys" | UNSUPPORTED | tested: Sex + Master flag gives 82.9% vs title 81.6%, which confirms it |
| 45 | "As one number 0, 1, 2, the model must treat 'large' as 'even more…'" | UNSUPPORTED | derived: one weight w adds 0, w, 2w, so the effect is monotone |
| 46 | "This is why the KNN accuracy fell as we added columns" | UNSUPPORTED | tested (Extra box): nearest neighbour same digit 98.8% → 72.5% (64 → 464 cols); nearest/average distance 0.34 → 0.89 |
| 46 | "distances also become almost all the same" | UNSUPPORTED | sourced: Beyer et al., "When is 'nearest neighbor' meaningful?", ICDT 1999 |
| 46 | "Useless and redundant columns make the data sparse…" | UNSUPPORTED | reworded to what the test shows (useless features); "redundant" removed (UNRESOLVED: a copied feature does not spread data) |
| 46 | "took about twice as long" | WRONG FACT | tested: about 1.6× (2.2 s vs 1.4 s) |
| 47 | "Karl Pearson in 1901 … Hotelling in 1933" | UNSUPPORTED | sourced: Pearson, Phil. Mag. 1901; Hotelling, J. Educ. Psych. 1933 |
| 47 | "corrects for a sample looking less spread out than the population" | UNSUPPORTED | sourced: Casella & Berger, *Statistical Inference*, 2nd ed., 2002, Thm 5.2.6 |
| 48 | "(Lagrange multipliers) gives exactly Cu = λu" | UNSUPPORTED | sourced: Bishop, *PRML*, 2006, Sec 12.1.1 |
| 48 | "In two dimensions there are two eigenvector directions…" | WRONG FACT | reworded: "at most"; a 90° rotation has no real eigenvector; symmetric matrices have the full set |
| 48 | "symmetric, which guarantees … eigenvalues are 0 or positive" | UNSUPPORTED | sourced: Strang, *Intro to Linear Algebra*, 5th ed., 2016, Sec 6.4; derived: λ = uᵀCu, a variance |
| 48 | "Mean centring is sometimes called optional" | UNSUPPORTED | reworded: centring matters for the projection, not the components (shown in the box) |
| 48 | "it never changes which direction is PC1" | UNSUPPORTED | derived: n vs n−1 only scales C, so eigenvectors stay the same |
| 49 | "The extra components add more noise than signal for KNN" | UNSUPPORTED | tested: components 101–300 alone give 76%; shuffling them lowers 300-component accuracy 94.5% → 93.3%, so they carry class information; Note now says so |
| 49 | "Edge pixels are almost always 0; standardising stretches their rare tiny changes…" | UNSUPPORTED | tested: dropping pixels inked in <5% of images, then standardising, gives 95.9% (vs 94.0% all standardised, 96.8% raw); most of the loss comes back |
| 49 | "PCA puts the noisy directions last, which is why 50 components beat all 784" | WRONG FACT | tested (refuted): components 51–784 alone give 78%; shuffling them drops 94.0% → 90.3%; Note states this |
| 49 | "For images, PCA is often run on unscaled pixels" | UNSUPPORTED | tested: unscaled PCA, 50 components, 97.3% |
| 49 | "Digits with few dark pixels, like 1, sit at one end of PC1" | UNSUPPORTED | tested: corr(PC1, inked pixels) = 0.80; 1s average 85 inked pixels, 0s 191 |
| 49 | "That is why the 2D and 3D pictures overlap so much" | UNSUPPORTED | derived: first 3 components hold only 14% of the variance, so the overlap follows |
| 49 | "LDA … kernel PCA or t-SNE exist" | UNSUPPORTED | sourced: Bishop, *PRML*, 2006, §4.1.4, §12.3; van der Maaten & Hinton, JMLR 9, 2008 |
| 50 | "A model is only trustworthy within the range of the data" | UNSUPPORTED | sourced: NIST/SEMATECH e-Handbook §4.1.4.1, tied to the 54.9 LPA prediction at CGPA 100 |
| 51 | "Its `fit` does nothing more than these few sums" | WRONG FACT | sourced: scikit-learn LinearRegression docs (uses scipy.linalg.lstsq) |
| 51 | "always a minimum, because E is a sum of squares: a bowl" | UNSUPPORTED | derived: second-derivative test, determinant 4n·Σ(x−x̄)² > 0 |
| 51 | "an old object keeps its old m and b" | WRONG FACT | sourced: Python Language Reference §8.8; checked by running it |
| 52 | "RMSE always ≥ MAE, because the squares give extra weight" | UNSUPPORTED | derived (proof in an Extra box): MSE − MAE² = (1/n)Σ(aᵢ − MAE)² ≥ 0; intuition kept in the text |
| 52 | "remaining 22% comes from things not in the data, such as interviews" | UNSUPPORTED | kept as an intuition (things not in the data, such as interviews), which points the right way |
| 52 | "the model can always bend a little closer…, even by chance" | UNSUPPORTED | derived: new coefficient 0 gives the old fit, so SS_res cannot rise and R² cannot fall |
| 52 | "it is target leakage" | UNSUPPORTED | sourced: Kaufman, Rosset, Perlich & Stitelman, ACM TKDD 6(4), 2012 |
| 53 | "The noise added to the data limits how good any plane can be" | UNSUPPORTED | tested (changed only noise): test R² 0.61 / 0.85 / 1.0 at noise 50 / 25 / 0 |
| 53 | "Standardising the inputs puts all coefficients on the same footing" | UNSUPPORTED | sourced: Gelman, Statistics in Medicine 27, 2008; both inputs std ≈ 1, so 58.6 vs 29.1 is fair |
| 54 | "The last rule holds because XᵀX is symmetric" | UNSUPPORTED | sourced: Deisenroth, Faisal & Ong, *MML*, 2020, §5.5 eqs 5.105, 5.107; symmetry step shown |
| 54 | "with a numerically safer method than a literal inverse" | UNSUPPORTED | sourced: scikit-learn docs; LAPACK DGELSD (SVD-based) |
| 54 | "very slow and memory-hungry" | UNSUPPORTED | derived: 20,000 columns ≈ 11 min and 3.2 GB |
| 54 | "Libraries handle this with a pseudo-inverse" | UNSUPPORTED | sourced: LAPACK DGELSD (minimum-norm solution for rank-deficient X) |
| 55 | "inputs come already standardised (centred and scaled)" | WRONG FACT | sourced: scikit-learn Diabetes docs (scaled by std × √n, so each column's sum of squares is 1) |
| 55 | "large opposite coefficients of s1 and s2 … Regularisation tames this" | UNSUPPORTED | tested: corr(s1,s2) 0.895, VIF 56/37; bootstrap coef std 464/369 (bmi 77), co-move at −0.97; Ridge α=0.1 gives −73/−81 |
| 55 | "it is slower and can lose accuracy" / "Two safer NumPy functions" | WRONG FACT | tested: timing difference negligible ("slower" removed); inv and solve errors 3e-5/9e-5 vs lstsq 1e-11; Note now credits not forming XᵀX |
| 55 | "uses a least-squares solver of the second kind" | UNSUPPORTED | sourced: scikit-learn LinearRegression docs |
| 56 | "Lists online vary from three to seven" | WRONG FACT | reworded to "five to seven" (transcript says 5, 6, 7) |
| 56 | "polynomial regression … or a transformation … can make it linear" | UNSUPPORTED | sourced: James et al., *ISL* 2nd ed., 2021, §3.3.3 |
| 56 | "coefficients … swing wildly while the predictions stay fine" | UNSUPPORTED | sourced: ISL §3.3.3 (Fig 3.15, Table 3.11); Kutner et al., *Applied Linear Statistical Models* 5th ed., §7.6 |
| 56 | "without add_constant the values can be wrong for data not centred" | WRONG FACT | tested: statsmodels 0.15 gives the same VIF with and without it, even centred at 5; removed as a side remark (UNRESOLVED) |
| 56 | "dropping…, combining (PCA), or regularisation" | UNSUPPORTED | sourced: ISL §3.3.3; Hoerl & Kennard, Technometrics 1970 |
| 56 | "With large datasets these tests flag tiny, harmless departures" | UNSUPPORTED | sourced: Ghasemi & Zahediasl, 2012, §3 |
| 56 | "heteroscedasticity is common: house-price model is often off…" | UNSUPPORTED | sourced: ISL §3.3.3 ("is common" restored), house-price example kept |
| 56 | "predictions still unbiased, but … p-values become wrong; log fix" | UNSUPPORTED | sourced: Wooldridge, *Introductory Econometrics* §8.1; ISL §3.3.3 |
| 56 | "mostly happens with data that has an order" | UNSUPPORTED | sourced: ISL §3.3.3 |
| 56 | "model is missing something that changes gradually, such as a time trend" | UNSUPPORTED | tested: with a slow sin(t/25) input left out, Durbin-Watson 0.40; with it added, 2.09 |
| 56 | Durbin-Watson "about 2 / 0 / 4" | UNSUPPORTED | sourced: statsmodels `durbin_watson` docs; tied to 2.31 |
| 57 | "Each slope is about one fifth…" | UNSUPPORTED | derived: b_new − b* = (1 − 2nη)(b_old − b*) = 0.2×; also explains divergence at 0.26 (factor −1.08) |
| 57 | "try 0.001, 0.01 and 0.1" | UNSUPPORTED | sourced: Goodfellow et al., *Deep Learning*, 2016, §11.4.3 |
| 57 | "updating b first … (here, slightly wrong) algorithm" | WRONG FACT | tested: sequential version gives m = 28.157, as close to OLS as simultaneous |
| 57 | "convex … exactly one minimum … always reaches" | WRONG FACT | sourced: Boyd & Vandenberghe, 2004, §4.2.2; added "with a small enough learning rate" |
| 57 | "random restarts, momentum, adaptive LR designed to escape local minima" | UNSUPPORTED | sourced: Goodfellow §8.2, §8.3.2, §8.5; restarts from transcript |
| 57 | "learning rate must be small … blowing up in the steep direction" | UNSUPPORTED | sourced: Goodfellow §4.3.1 |
| 58 | "about 13 times faster" | WRONG FACT | tested: 13 to 80 times depending on the machine; reworded |
| 58 | "is not luck. Stopping early keeps coefficients smaller…" | WRONG FACT | sourced: Goodfellow §7.8; reworded: the gain here is mostly luck of the split; tested (Extra box): coef size 809 vs 1,525 OLS, but GD beat OLS on only 12 of 20 splits (mean +0.005) |
| 58 | "s1, s2 strongly related … long flat valley" | UNSUPPORTED | tested: corr 0.895, flattest direction along s1/s2/s3, curvature ratio 447; sourced: ISL Fig 3.15, Goodfellow §4.3.1 |
| 59 | "probably the most widely used … basis of NN training" | UNSUPPORTED | sourced: Goodfellow §8.3.1, §5.9 |
| 59 | "shuffle once per epoch … SGDRegressor does this" | UNSUPPORTED | sourced: scikit-learn `SGDRegressor` docs |
| 59 | "advantage … number of passes … data is huge" | UNSUPPORTED | sourced: Goodfellow §5.9 |
| 59 | "This is one reason it is used for neural networks" | UNSUPPORTED | removed (UNRESOLVED) |
| 59 | "Gradually lowering LR is sometimes called simulated annealing" | WRONG CITATION | sourced: Kirkpatrick, Gelatt & Vecchi, Science 1983 (Géron not verified); cooling-metal intuition kept |
| 59 | "invscaling shrinks the rate too fast" | UNSUPPORTED | tested: power_t=0 gives 0.43; 1,000 epochs 0.39; 5,000 epochs 0.45 |
| 59 | "hint to raise max_iter or the learning rate" | WRONG FACT | reworded to what the warning says (increase max_iter) |
| 60 | "typically 16 to 256"; "version most used" | UNSUPPORTED | sourced: Goodfellow §8.1.3 |
| 60 | "Shuffling once and slicing … is the usual choice" | UNSUPPORTED | sourced: Goodfellow §8.1.3 |
| 60 | "Averaging over 10 rows cancels much of the noise" | UNSUPPORTED | derived: σ/√B = 0.32σ for B = 10 (Goodfellow §8.1.3) |
| 60 | "8 to 32 usually work well" / "8 to 32 worked best here" | WRONG FACT | reworded to the data (8 was best); sourced: Masters & Luschi, 2018 |
| 60 | "larger batch … can often take a larger learning rate" | UNSUPPORTED | sourced: Goodfellow §8.1.3; Goyal et al., 2017 |
| 60 | "powers of two … hardware"; memory | UNSUPPORTED | sourced: Goodfellow §8.1.3 |
| 61 | "the remaining difference is the noise" | UNSUPPORTED | tested: same rows, no noise, give exactly 2, 0.9, 0.8 |
| 61 | "Training R² rises … because more columns" | UNSUPPORTED | derived: models are nested |
| 61 | "wildness … is the overfitting, not a numerical error" | UNSUPPORTED | tested: condition number 4.5e8 raw vs 1.1e6 scaled; exact least-squares fit gives test R² −3,727 vs −9.35, so it is overfitting; sourced: Goodfellow §4.2 |
| 61 | "interaction term lets effect of x depend on y" | UNSUPPORTED | derived: ∂ẑ/∂x = β_x + β_xy·y |
| 61 | "columns outnumber the rows, and the model overfits" | UNSUPPORTED | sourced: ISL §6.4.2 |
| 62 | "bias² creeps up … side effect of wild swings" | UNSUPPORTED | derived and tested: E[(f̄ − f)²] = bias² + var/N; var/200 = 0.18 > 0.079 |
| 62 | trade-off claim; error formula | UNSUPPORTED | sourced: ISL §2.2.2, eq. 2.7 |
| 62 | regularisation / bagging / boosting effects | UNSUPPORTED | sourced: ISL §6.2.1, §8.2.1, §8.2.3 |
| 62 | "terms come from statistics" (bias definition) | UNSUPPORTED | derived: tied to the average-curve definition in Section 4 |

## Counts per Note

| Note | Findings | UNSUPPORTED | WRONG FACT | WRONG CITATION |
|---|---|---|---|---|
| 35 | 4 | 4 | 0 | 0 |
| 36 | 4 | 2 | 2 | 0 |
| 37 | 5 | 5 | 0 | 0 |
| 38 | 5 | 5 | 0 | 0 |
| 39 | 4 | 3 | 0 | 1 |
| 40 | 5 | 5 | 0 | 0 |
| 41 | 4 | 3 | 1 | 0 |
| 42 | 4 | 4 | 0 | 0 |
| 43 | 5 | 4 | 1 | 0 |
| 44 | 5 | 4 | 0 | 1 |
| 45 | 6 | 5 | 1 | 0 |
| 46 | 4 | 3 | 1 | 0 |
| 47 | 2 | 2 | 0 | 0 |
| 48 | 5 | 4 | 1 | 0 |
| 49 | 7 | 6 | 1 | 0 |
| 50 | 1 | 1 | 0 | 0 |
| 51 | 3 | 1 | 2 | 0 |
| 52 | 4 | 4 | 0 | 0 |
| 53 | 2 | 2 | 0 | 0 |
| 54 | 4 | 4 | 0 | 0 |
| 55 | 4 | 2 | 2 | 0 |
| 56 | 11 | 9 | 2 | 0 |
| 57 | 6 | 4 | 2 | 0 |
| 58 | 3 | 1 | 2 | 0 |
| 59 | 7 | 5 | 1 | 1 |
| 60 | 6 | 5 | 1 | 0 |
| 61 | 5 | 5 | 0 | 0 |
| 62 | 4 | 4 | 0 | 0 |
| **Total** | **129** | **106** | **20** | **3** |

## UNRESOLVED (removed from Note)

- 37: "This explains why houses with a gap sold for less in Figure 3."
- 37: "When there are few gaps, the new category is small, and the results are usually no better than with mode imputation."
- 41: "KNN" in the list of algorithms hurt by outliers (ESL Table 10.1 rates k-NN robust to input outliers)
- 35: "A value of 20 stands for 'more than 20 years'" (only a blog backed it; not needed for learning)
- 46: the word "redundant" in "Useless and redundant columns make the data sparse and hide the real pattern." (the test covered only useless features; a copied feature does not spread the data)
- 59: "This is one reason it is used for neural networks." (no source says escaping local minima is why SGD is used; Goodfellow covers saddle points only)
- 56: "`variance_inflation_factor` expects the data to contain a constant column; without `add_constant` the values can be wrong for data that is not centred on 0." (refuted by test on statsmodels 0.15; not needed for learning)

Notes 49–55: nothing removed.

## Worst findings

1. **Note 49:** "PCA puts the noisy directions last, which is why 50 components beat all 784." The test refutes it: components 51–784 alone reach 78% accuracy, and shuffling them lowers accuracy. They carry class information; they are not noise.
2. **Note 48:** "In two dimensions there are two eigenvector directions." False in general: a rotation has none. Only symmetric matrices always have the full set.
3. **Note 58:** "Is not luck: stopping early keeps coefficients smaller." Early stopping beat OLS on only 12 of 20 splits (mean gain +0.005). The Note now says the gain here is mostly the luck of the split.

Also notable:
- **Note 41:** KNN was listed as hurt by outliers, but ESL Table 10.1 rates it robust to input outliers.
- **Note 55:** `solve` was called "safer" than `inv`. The test shows both are equally inaccurate; only `lstsq` is accurate.
- **Note 51:** "fit does nothing more than these few sums." scikit-learn actually uses `scipy.linalg.lstsq`.

## Remaining caveats

- In the new text, "column" has not yet been switched to feature / target / observation. That is left for the planned naming pass.
- The "## Sources" heading is numbered in Notes 35–48 (for example "## 10. Sources") and unnumbered in 49–62.
