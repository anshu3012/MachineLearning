# Round 3 report, list 4 (43 Notes)

Every Note below was rebuilt with `tools/build.sh <folder>` and printed "Built". I looked at every new PNG, every new frame grid and the PDF pages where they sit. Words per visual (wpv) and figure share (sections with a figure / numbered sections, Summary, Prerequisites, Sources and Key terms left out) come from `docs/visual-audit/measure.py`, run read-only.

All new animations are Plotly frames joined by ffmpeg into a GIF, with a `_frames.png` grid for the PDF. Each Note that gained one has a small helper, `images/gifkit.py` (frames to GIF and grid), because `tools/` is off limits. Every script asserts the Note's numbers it draws.

## Summary

All 43 Notes now meet the "strong" target: every one has at most 382 words per visual and at least 60% of its numbered sections with a figure. A final rebuild of all 43 printed "Built" for each.

| Note | wpv before | wpv after | sections with a figure, before | after |
|---|---|---|---|---|
| 51-linear-regression-maths | 392 | 193 | 3/6 | 5/6 |
| 52-regression-metrics | 378 | 244 | 4/7 | 7/7 |
| 53-multiple-linear-regression | 212 | 147 | 3/4 | 4/4 |
| 530-eigenvectors-and-eigenvalues | 520 | 321 | 4/7 | 6/7 |
| 56-linear-regression-assumptions | 332 | 209 | 4/6 | 6/6 |
| 560-poisson-distribution | 456 | 250 | 4/8 | 7/8 |
| 57-gradient-descent | 325 | 223 | 5/9 | 8/9 |
| 570-choosing-a-hypothesis-test | 270 | 218 | 7/8 | 8/8 |
| 571-chi-square-tests | 517 | 285 | 4/7 | 7/7 |
| 58-batch-gradient-descent | 335 | 242 | 4/6 | 6/6 |
| 59-stochastic-gradient-descent | 350 | 253 | 4/8 | 6/8 |
| 590-convex-and-non-convex-cost-functions | 521 | 334 | 3/5 | 5/5 |
| 600-derivatives-of-one-variable | 498 | 266 | 4/6 | 6/6 |
| 601-partial-derivatives-and-gradients | 449 | 288 | 4/7 | 7/7 |
| 603-hessian-and-multivariate-taylor | 531 | 328 | 3/6 | 6/6 |
| 61-polynomial-regression | 280 | 169 | 3/5 | 5/5 |
| 612-low-rank-approximation | 375 | 280 | 5/7 | 7/7 |
| 620-lagrange-multipliers | 579 | 316 | 4/7 | 7/7 |
| 622-linear-and-quadratic-programming | 540 | 255 | 3/3 | 3/3 |
| 63-ridge-regression-intuition | 223 | 200 | 3/4 | 4/4 |
| 630-probability-vs-likelihood | 392 | 237 | 3/6 | 6/6 |
| 64-ridge-regression-maths | 472 | 223 | 2/3 | 3/3 |
| 640-gaussian-mixture-models | 541 | 315 | 5/9 | 9/9 |
| 65-ridge-gradient-descent | 356 | 250 | 3/6 | 5/6 |
| 66-ridge-key-points | 248 | 217 | 4/6 | 5/6 |
| 67-lasso-regression | 252 | 192 | 5/8 | 7/8 |
| 70-perceptron-trick | 238 | 178 | 4/7 | 6/7 |
| 72-sigmoid-function | 320 | 233 | 4/7 | 5/7 |
| 77-precision-recall-f1 | 275 | 191 | 4/6 | 6/6 |
| 79-softmax-regression | 295 | 237 | 3/5 | 4/5 |
| 82-conditional-probability | 192 | 153 | 2/4 | 3/4 |
| 83-independent-events | 210 | 142 | 3/6 | 5/6 |
| 84-mutually-exclusive-events | 178 | 135 | 2/4 | 3/4 |
| 86-bayes-problem | 130 | 112 | 4/6 | 5/6 |
| 88-naive-bayes-maths | 182 | 136 | 4/7 | 6/7 |
| 91-knn | 484 | 370 | 5/7 | 6/7 |
| 92-svm-intuition | 349 | 245 | 3/6 | 5/6 |
| 93-svm-maths | 270 | 241 | 6/7 | 7/7 |
| 94-svm-soft-margin | 373 | 259 | 4/8 | 6/8 |
| 95-kernel-trick-intuition | 342 | 279 | 3/5 | 4/5 |
| 97-decision-trees-intuition | 392 | 328 | 8/9 | 9/9 |
| 98-decision-tree-hyperparameters | 549 | 382 | 3/5 | 3/5 |
| 99-regression-trees | 365 | 327 | 6/7 | 6/7 |

### Things the other machine needs to do
- **Glossary.** I did not run `merge_glossary.py` or edit `glossary.md`. New Key terms that are not yet in the glossary:
  - Note 93: "Norm of a vector" (the glossary has "L2 norm", G-1028, which the text now cites; either merge the new row or rename it).
  - Note 95: "Feature space" (added this round).
  - Note 99: "California housing data" (already in the Key terms table before this round, still unmerged).
- Three Key-terms rows were fixed so that a merge will not create duplicates: Note 612's "Rank $k$ approximation" now matches G-1630, and the combined "Feature, target, observation" rows of Notes 63 and 70 are split into G-772, G-1949 and G-1374.

### Facts corrected (all backed by the figure scripts' assertions)
- Note 571: the expected third-class Titanic survivors are 188, not 189.
- Note 94: the soft-margin line has ‖w‖ = 0.900 (the 0.899 belonged to Note 92's 16-point SVM), and the C = 10 loss is 26.97, not 26.95.
- Note 61: the training R² dips by 0.0002 from degree 14 to 15, which exact least squares cannot do; the conditioning Extra now names it as rounding.
- Note 61: Section 2 pointed at a figure of a different dataset; it now has its own figure.
- Note 84: the comparison figure was never referred to; it now is.

### Method and conventions
- Every animation is Plotly frames joined by ffmpeg (Manim once, for Note 530's vector motion), with a `_frames.png` grid; all GIFs are under 3 MB. Each Note that gained an animation has a small `images/gifkit.py` helper, because `tools/` is off limits.
- Every new figure uses the Note's own data or a recipe copied from its Notebook, and asserts the numbers the text quotes. Where a claim had no evidence, I ran a small experiment and reported its numbers (for example Notes 56, 61, 66, 92, 97, 98).
- No source was newly credited. Two captions mention the 3Blue1Brown lessons the Notes already credit (Notes 600 and 82), for pictures redrawn with our numbers.
- Keras was not used; no GPU runs were needed. No heavy renders needed topgro beyond this machine.
- Nothing outside my 43 folders and this report was changed, except the `pdf/<folder>.pdf` files and `images/.built_*` stamps the build writes.

### Not done
- Overview sections that are only a short outline were left without a figure where the rest of the Note already met the target (for example Notes 65, 67, 70, 79, 82 to 84).
- Note 98's figure share stayed at 3/5: its new visuals went into Section 4, where the hyperparameters live; Sections 1 and 5 are an outline and a short closing.

## Per Note

## 51-linear-regression-maths

**Visuals added** (all Plotly, data: the 160 training students of the placement data)
- `two_routes.gif` (Section 2): closed form against non-closed form. OLS jumps to the best line in one step; gradient descent from (0, 0) walks there in 6,112 steps on the error map.
- `cancel.png` (Section 3.2): a flat line at the mean package and the best line both have residuals summing to 0, but squared sums of 73.02 and 16.55. Shows why raw errors cancel.
- `square_vs_abs.png` (Section 3.2): d squared against |d|; large errors count more, and |d| has a corner at 0.
- `tangent_slice.gif` (Section 4.1): a tangent line slides along each slice of the bowl; its slope is the partial derivative, negative, then 0 at the OLS values, then positive.
- `cov_quadrants.png` (Section 4.4): the products (x - x-bar)(y - y-bar) by quadrant; 125 positive products sum to 103.06, 35 negative ones to -1.86, giving 101.204 and the slope 0.558.
- `my_vs_sklearn.png` (Section 6): the code's output; MyLR's line lies on scikit-learn's, with the three test predictions.

**Ladder changes:** Section 2 now opens with the plain idea ("jump straight to the answer, or walk towards it") before the two terms. Section 4.1 adds a worked example of the partial derivative on our numbers (-321, 0, 319) before the formal derivation. Section 4.4 explains the covariance numerator on the data before the formula's meaning.

**Terms and IDs:** feature G-772, target G-1949, observation G-1374, best-fit line G-280, linear regression G-1094, closed-form solution G-398, OLS G-1406, non-closed-form solution G-1332, gradient descent G-862, prediction G-1550, residual G-1685 (new in the text: the "error at one point" now carries its standard name), loss function G-706, sum of squared errors G-1913, mean squared error G-1201, derivative G-595, tangent line G-1945, partial derivative G-1457, chain rule G-371, mean G-1203, covariance G-496, variance G-2078. Residual and Tangent line were added to Key terms; both are already in the glossary.

**Numbers:** wpv 392 -> 193; figure share 3/6 -> 5/6.

**Text fixed:** two figure references renumbered (Figures 1 to 10), the StatQuest credit now points at Figure 5. No facts changed.

## 52-regression-metrics

**Visuals added** (Plotly, data: the 40 placement test students and the line's predictions)
- `test_errors.png` (Section 1): the 40 test errors as sticks; the thing every metric summarises.
- `mae_steps.gif` (Section 2): MAE in four steps: signed errors, their plain average (-0.041, they cancel), drop the sign, average the sizes (0.288).
- `rmse_square.png` (Section 4): every error as a square; the square with the average area (MSE 0.121) has side RMSE 0.348, longer than the average side MAE 0.288.

**Ladder changes:** Section 2 opens with the plain idea (measure each stick, ignore its direction, average) before the term and formula. Section 4 adds a geometric reading of RMSE against MAE before the formal proof in the Extra box.

**Terms and IDs:** regression metric G-1652, feature G-772, target G-1949, observation G-1374, MAE G-1194, outlier G-1420, MSE G-1201, loss function G-1130, RMSE G-1705, residual sum of squares G-1684, total sum of squares G-1993, coefficient of determination G-1717, adjusted R² G-177, target leakage G-1948. "A metric" became "a regression metric".

**Numbers:** wpv 378 -> 244; figure share 4/7 -> 7/7.

**Text fixed:** figure references renumbered (1 to 7). The leakage sentence had two colons in a row ("it is target leakage: information..."); split into two sentences.

## 53-multiple-linear-regression

**Visuals added** (Plotly, data: the Note's `make_regression` data, random_state 7, and its fitted model)
- `data_table.png` (Section 1): the first five observations, with the feature columns, the target column and one observation row coloured. Illustrates the three base terms.
- `prediction_steps.gif` (Section 3): the worked prediction built as a waterfall: intercept -1.9, plus 58.6 x 1, plus 29.1 x 0.5, gives 71.3.

**Ladder changes:** the Overview now shows the three terms on real rows before the plane geometry. Section 3 shows the term-by-term build of one prediction before the coefficient meanings.

**Terms and IDs:** feature G-772, target G-1949, observation G-1374, multiple linear regression G-1279, simple linear regression G-1808, plane G-1502, hyperplane G-911, coefficient G-407, intercept G-960, weight G-2111, standardisation G-1874, make_regression G-1153.

**Numbers:** wpv 212 -> 147; figure share 3/4 -> 4/4.

**Text fixed:** figure references renumbered (1 to 6). No facts changed.

## 530-eigenvectors-and-eigenvalues

**Visuals added**
- `rotation_axis.gif` (Section 2.1, Plotly 3D frames): a rotation about the axis through [1, 1, 1] from 0 to 120 degrees; the basis vectors sweep round, the axis vector never moves (eigenvalue 1). Asserts R u = u and a single real eigenvalue 1.
- `null_line.gif` (Section 4, Manim, because it is vector motion): the plane moves under A - 2I and then A - 3I; the eigenvector line is crushed to the origin while [1, 1] survives. Asserts every green vector maps to 0.
- `power_iteration.gif` (Section 7, Plotly): the website matrix T applied day after day to two starting splits; both slide onto the eigenvector of eigenvalue 1 and the share on page A settles at 0.833. Asserts eigenvalues 1 and 0.4.

**Ladder changes:** Section 2.1 now shows the rotation axis on a concrete rotation before the general claim. Section 4 adds a watched mechanism (the squish) between the formula and the NumPy call. The power-iteration Extra now has a worked run.

**Terms and IDs:** eigenvector G-666, eigenvalue G-665, linear transformation G-1097, span G-1838, axis of rotation G-241, identity matrix G-915, determinant G-598, characteristic polynomial G-376, diagonal matrix G-601, basis G-262, eigenbasis G-664, change of basis matrix G-374, diagonalisation G-602 (now attached to "eigen-decomposition", which had no Key-terms entry), principal component G-1563, covariance matrix G-495, power iteration G-1537.

**Numbers:** wpv 520 -> 321; figure share 4/7 -> 6/7.

**Text fixed:** figure references renumbered (1 to 7); the Overview's pointer "Figure 2" for the hand method now reads "Figures 3 and 4". No facts changed.

## 56-linear-regression-assumptions

**Visuals added** (Plotly)
- `residuals_def.png` (Section 1): the 60 test residuals as sticks to the diagonal of perfect predictions; the object assumptions 3 to 5 are about. Data: the Note's data.csv and split.
- `collinear_coefs.gif` (Section 3.1): a new experiment. The model is refitted on 20 bootstrap resamples, first with the Note's features (feature1's coefficient stays 69.9 to 78.0), then with a near-copy of feature1 added (VIF 429): feature1 swings from 21.5 to 102.5 while the pair's sum stays 69.7 to 78.0. It backs the ISL §3.3.3 claim that collinear coefficients become unreliable.
- `autocorr_fix.png` (Section 6): the Notebook's missing-trend test drawn; residuals in row order with Durbin-Watson 0.40 (a wave) and 2.09 (random) after adding the slow input.

**Ladder changes:** Section 3.1 now has the step-by-step evidence (the bootstrap refits) between the analogy and the formal VIF. Section 6 shows the cause on data before the Durbin-Watson number.

**Terms and IDs:** assumption G-220, feature G-772, observation G-1374, target G-1949, residual G-1685, correlation G-490, multicollinearity G-1273, bootstrap G-320, VIF G-2075, heatmap G-886, normal distribution G-1343, Q-Q plot G-1596, Shapiro-Wilk test G-1788, p-value G-1433, homoscedasticity G-902, heteroscedasticity G-889, autocorrelation G-230, time series G-1975, Durbin-Watson statistic G-649.

**Numbers:** wpv 332 -> 209; figure share 4/6 -> 6/6.

**Text fixed:** figure references renumbered (1 to 7). One sentence ("Autocorrelation makes the model look more certain...") moved in front of the new figure so the PDF keeps the caption.

## 560-poisson-distribution

**Visuals added** (Plotly)
- `trials_vs_rate.png` (Section 2.1): a binomial count as 10 numbered trials beside a Poisson count as random events on a time line, counted per day. One seeded simulation of each.
- `mean_var_sim.gif` (Section 5): the Notebook's 100,000-day simulation (seed 42) growing from 10 days; the histogram settles on the PMF and the running mean and variance settle at 3.994 and 3.987.
- `overdispersion.png` (Section 5 Extra): the Notebook's three overdispersion cases drawn against a Poisson PMF with the same mean (variances 3.99, 11.99, 7.96).
- `range_sum.gif` (Section 6): the bars for 0 to 6 stacked one at a time into P(Y <= 6) = 0.8893, leaving P(Y >= 7) = 0.111.

**Ladder changes:** Section 2.1 shows the trials-versus-rate contrast before the formal definition. Section 5 shows the simulation converging before the formula, and Section 6 builds the range sum step by step before the code.

**Terms and IDs:** rate G-1633, binomial distribution G-308, Poisson distribution G-1509, parameter G-1448, Euler's number G-716, negative power G-1311, PMF G-1572, skewness G-1817, expected value G-725, standard deviation G-1871, overdispersion G-1428, CDF G-515, independent events G-934, Poisson regression G-1510, target G-1949, observation G-1374, feature G-772.

**Numbers:** wpv 456 -> 250; figure share 4/8 -> 7/8 (Section 8, an all-Extra section on the Poisson conditions, has no figure; the overdispersion figure covers the broken conditions).

**Text fixed:** figure references renumbered (1 to 8). No facts changed.

## 57-gradient-descent

**Visuals added** (Plotly, data: the Note's 4-point and 100-point `make_regression` examples)
- `which_way.png` (Section 2): four points on the loss curve L(b), each with its tangent and its step arrow (minus 0.1 times the slope). Shows "against the slope" and "steep means long step".
- `slope_b_worked.png` (Section 3): the slope formula evaluated at b = 100: four residuals, their sum -295.4, times -2 gives 590.7 (the value used in Section 4).
- `class_fit.gif` (Section 7): the GDRegressor run, epoch by epoch, with its loss curve; ends at m = 28.159, b = -2.300 against OLS 28.126, -2.271.

**Ladder changes:** Section 2 now pictures the plain rule before the update formula, with numbers from the figure. Section 3 adds a worked evaluation of the derivative before Section 4's steps. Section 7 shows what the code produces.

**Terms and IDs:** gradient descent G-862, optimisation algorithm G-1398, loss function G-1130, feature G-772, observation G-1374, target G-1949, learning rate G-1068, epoch G-696, chain rule G-371, hyperparameter G-910, partial derivative G-1457, gradient G-865, contour plot G-468, converge G-469, diverge G-628, convex function G-476, local minimum G-1110, global minimum G-848, plateau G-1503, saddle point G-1718, standardisation G-1874.

**Numbers:** wpv 325 -> 223; figure share 5/9 -> 8/9.

**Text fixed:** figure references renumbered (1 to 8). No facts changed.

## 570-choosing-a-hypothesis-test

**Visuals added** (Plotly)
- `t_one_sample.png` (Section 6): the t-distribution with 59 degrees of freedom, the sample's t = -0.64, the shaded p = 0.53 tails and the 5% rejection region. Data: `data/people.csv`, with the Note's numbers asserted.
- `r_vs_n.gif` (Section 7.2): a fixed r = 0.30 with n growing from 10 to 100; the statistic slides into the rejection region, and the p-value curve crosses 0.05 at n = 44. Illustrates "sample size matters as much as r".

**Ladder changes:** Section 6 now shows the decision on the distribution before stating it; Section 7.2 adds a watched mechanism after the worked example.

**Terms and IDs:** feature G-772, null hypothesis G-1361, alternative hypothesis G-193, significance level G-1801, two-tailed test G-2028, rejection region G-1662, fail to reject G-746, observation G-1374, one-sample proportion test G-1381, correlation test G-489, sample proportion G-1726, standard error G-1872, contingency table G-464, chi-square test of independence G-380, Student's t-distribution G-1906, degrees of freedom G-578, one-sample t-test G-1382, Pearson's r G-1474, population correlation G-1522, one-way ANOVA G-1389.

**Numbers:** wpv 270 -> 218; figure share 7/8 -> 8/8.

**Text fixed:** figure references renumbered (1 to 9). The threshold n = 44 in the new text was checked by the script (my first guess of 43 was wrong and the assertion caught it).

## 571-chi-square-tests

**Visuals added** (Plotly)
- `chi2_build.gif` (Section 2): the statistic built cell by cell for the age groups against the census shares: observed and expected bars with the gaps, and the three (O - E)^2 / E blocks stacking to 3.48.
- `independence_table.png` (Section 5): observed, expected and contribution tables as heatmaps for gender by age group (chi-square 2.50).
- `small_counts.png` (Section 7.1 Extra): the Notebook's 200,000-sample simulation (seed 0) drawn as histograms against the chi-square curve; with expected counts below 1 the statistic piles onto a few spikes and the rejection rate becomes 11.2% or 2.7%.
- `cramers_v.png` (Section 7.2): the Titanic sex table at a tenth, the actual and ten times the size; chi-square grows (26.3, 263.1, 2,630.5) while V stays 0.54; and V for sex (0.54) against class (0.34).
- `titanic_class.png` (Section 6.2) was rewritten from seaborn (matplotlib) to Plotly, as the house rules require; same content.

**Ladder changes:** Section 2 explains with the picture why the adult gap counts less than the child gap before the formal statistic is named. Section 7.1 now explains the mechanism (few possible count patterns, so spikes) instead of only reporting rates. Section 7.2 shows the need for V before its use.

**Terms and IDs:** feature G-772, observed count G-1375, observation G-1374, expected count G-723, chi-square statistic G-379, chi-square distribution G-378, degrees of freedom G-578, right-tailed test G-1693, critical value G-504, goodness-of-fit test G-853, chi-square test of independence G-380, contingency table G-464, marginal probability G-1165, Yates' continuity correction G-2135, Fisher's exact test G-782, Cramér's V G-500, feature selection G-768, SelectKBest G-1762, target G-1949.

**Numbers:** wpv 517 -> 285; figure share 4/7 -> 7/7.

**Text fixed:** Section 6.2's key point said independence predicts 189 third-class survivors; the expected count is 188.46, so it now says 188 (checked in `titanic_class.py`). Figure references renumbered (1 to 8).

## 58-batch-gradient-descent

**Visuals added** (Plotly; data: the diabetes split of the Notebook, random_state 2, through a shared `images/run58.py`)
- `coef_steps.gif` (Section 2): the 10 coefficients as bars, all updated at every epoch, closing in on the OLS values; the intercept and test R² in the title.
- `code_run.png` (Section 4): what the code produces: test R² per epoch (passes OLS's 0.440 at epoch 407, ends at 0.453) and the intercept (150.5 after one epoch, 152.01 at the end).

**Ladder changes:** Section 2 now shows the m + 1 simultaneous updates on real data before the derivatives. Section 4 shows the run, not only the table.

**Terms and IDs:** feature G-772, observation G-1374, target G-1949, batch gradient descent G-264, SGD G-1892, mini-batch gradient descent G-1222, mean squared error loss G-1202, learning rate G-1068, chain rule G-371, vectorisation G-2083, early stopping G-656, correlation G-490, multicollinearity G-1273. "The **mean** squared error" became the standard term "mean squared error loss".

**Numbers:** wpv 335 -> 242; figure share 4/6 -> 6/6.

**Text fixed:** figure references renumbered (1 to 6); ISL's "Figure 3.15" kept as is.

## 59-stochastic-gradient-descent

**Visuals added** (Plotly)
- `cost_bars.png` (Section 2): the Note's own example (100,000 observations, 100 features): multiplications per update (10,000,000 against 100) and updates per epoch (1 against 100,000).
- `sgd_eta0.png` (Section 7): the Notebook's SGDRegressor runs on the diabetes data: test R² of the "invscaling" schedule at four starting rates (0.16, 0.38, 0.43, 0.45) against the constant rate (0.43) and OLS (0.44).

**Ladder changes:** Section 2 shows the cost on a picture before the general statement; Section 7 shows the starting-rate effect before the Extra details. The Overview's list-paragraph ("explains the problem..., how SGD works, its behaviour, and...") is now a bulleted list with section numbers (§9).

**Terms and IDs:** feature G-772, observation G-1374, target G-1949, batch gradient descent G-264, SGD G-1892, optimisation algorithm G-1398, epoch G-696, stochastic G-1893, learning rate G-1068, learning schedule G-1072, simulated annealing G-1810, SGDRegressor G-1783, `max_iter` (SGDRegressor) G-115, eta0 G-713.

**Numbers:** wpv 350 -> 253; figure share 4/8 -> 6/8 (Sections 1 and 8, the overview and the comparison table, have no figure).

**Text fixed:** Key terms said an observation is "one observation of the data table"; it now says "one row". Figure references renumbered (1 to 6).

## 590-convex-and-non-convex-cost-functions

**Visuals added** (Plotly; data: the Note's 21 points, y = 1.5 tanh(2x))
- `loss_of_m.gif` (Section 2): the data stays fixed while the slope m of y = mx sweeps from -1 to 3; the line and its errors on the left, the loss curve L(m) traced on the right, lowest at m = 1.02, loss 0.18.
- `chord_slices.png` (Section 5): the chord test in two dimensions cut to one: the loss along the straight path between two parameter points, against the chord. The line model stays below (0.18 against 6.05 at the midpoint); the tiny network climbs a ridge of 1.71 above a chord at 0.

**Ladder changes:** Section 2 shows "the loss is a function of the parameters" on the data before the general statement. Sections 5.1 and 5.2 now picture the chord numbers they compute.

**Terms and IDs:** convex function G-476, gradient descent G-862, local minimum G-1110, global minimum G-848, loss function G-1130, cost function G-492, chord G-384, non-convex function G-1333, strictly convex function G-1899, stationary point G-1879, saddle point G-1718.

**Numbers:** wpv 521 -> 334; figure share 3/5 -> 5/5.

**Text fixed:** figure references renumbered (1 to 5). No facts changed.

## 600-derivatives-of-one-variable

**Visuals added** (Plotly, the Note's own worked examples)
- `function_map.png` (Section 2): f: x ↦ x² as arrows from an input line to an output line; every input has one arrow, -2 and 2 share the output 4. Illustrates function, domain and codomain.
- `diff_quotient.png` (Section 3): rise 3 over run 1 for x² between 1 and 2, with the tangent slopes 2 and 4 at the ends, so "average slope" is visible.
- `chain_rates.png` (Section 5.3): the chain rule for (x² + 1)³ at x = 1 as three number lines; a nudge 0.01 becomes about 0.02, then about 0.24 (rates 2 and 12 multiply to 24). The three-number-line picture follows Sanderson's "Visualizing the chain rule and product rule", which the Note already credits; redrawn with our numbers and credited in the caption.
- `linearise_sqrt.png` (Section 6.2): √x and its tangent line at 4, with the gaps 0.0002, 0.0139 and 0.1716 at x = 4.1, 5 and 8.

**Ladder changes:** Sections 2 and 3 now start from a picture of the Note's example. Section 5.3 and 6.2 show the mechanism (rates multiplying; the curve bending away from the tangent) after the worked numbers.

**Terms and IDs:** secant line G-1758, tangent line G-1945, derivative G-595, function G-816, domain G-632, codomain G-405, difference quotient G-604, limit G-1087, differentiable G-606, power rule G-1540, numerical derivative G-1368, central difference G-363, product rule G-1577, quotient rule G-1609, chain rule G-371, composition G-431, Taylor series G-1954, Taylor polynomial G-1953, Maclaurin series G-1142, linearisation G-1099, analytic function G-197, power series G-1541.

**Numbers:** wpv 498 -> 266; figure share 4/6 -> 6/6.

**Text fixed:** figure references renumbered (1 to 8). No facts changed.

## 601-partial-derivatives-and-gradients

**Visuals added** (Plotly, the Note's running example f = x₁² + x₁x₂ + 2x₂²)
- `vector_in.png` (Section 2): four input vectors on the contour map with the one number each returns; [1, 1] and [2, -1] both give 4 and share a contour line.
- `rule_arrows.png` (Section 5): the sum rule (∇f + aᵀ = [4, 7]) and the product rule (2a + 3b = [11, 1]) as arrows added tip to tail.
- `gradcheck_h.png` (Section 7): relative error of the numerical gradient against h for the Note's three-point loss: the one-sided difference passes 10⁻⁶ only below about 3 × 10⁻⁶; the central difference is exact for this quadratic loss except for rounding (2.5e-13 at h = 10⁻⁴).

**Ladder changes:** Section 2 shows "vector in, number out" on the map before any formula. Section 5 shows what the rules mean geometrically after the worked example. Section 7 explains why the step size matters, with the mechanism (truncation against rounding) tied to the Extra of Note 600.

**Terms and IDs:** gradient G-865, gradient descent G-862, function of several variables G-815, partial derivative G-1457, nabla G-1295, gradient as a row vector G-858, directional derivative G-614, steepest ascent G-1888, multivariate chain rule G-1281, chain rule G-371, Jacobian G-980, gradient checking G-860.

**Numbers:** wpv 449 -> 288; figure share 4/7 -> 7/7.

**Text fixed:** figure references renumbered (1 to 7). No facts changed.

## 603-hessian-and-multivariate-taylor

**Visuals added** (Plotly, the running example f = x³ + xy + y² at (1, 1))
- `mixed_partials.png` (Section 2): the x-slope watched as y moves and the y-slope watched as x moves; both rise with slope 1, so the mixed derivatives agree.
- `approx_error.png` (Section 4): error maps |f - T1| and |f - T2| near (1, 1); the region with error below 0.05 is about nine times larger for T2 (asserted 9 to 10 times). The T2 error depends on x alone, because its only missing term is δx³.
- `taylor_path.gif` (Section 5.3): a point walks from (1, 1) to (1.5, 0.5); T1, T2, T3 against f along the path, reading 3.1, 3.13, 3.131 and 3.5, 4.25, 4.375 (T3 = f).

**Ladder changes:** Section 2 explains "the mixed derivatives agree" with the picture before the formal statement. Section 4 measures the plane's limits; Section 5.3 shows the orders converging on the walk.

**Terms and IDs:** tangent plane G-1946, observation G-1374, second partial derivative G-1760, mixed partial derivative G-1236, curvature G-521, Hessian matrix G-888, saddle point G-1718, multivariate Taylor polynomial G-1284, multivariate Taylor series G-1285, outer product G-1418, Newton's method G-1321, quasi-Newton method G-1603, BFGS G-283, L-BFGS G-1023, secant equation G-1757, Laplace approximation G-1043.

**Numbers:** wpv 531 -> 328; figure share 3/6 -> 6/6.

**Text fixed:** figure references renumbered (1 to 7). No facts changed.

## 61-polynomial-regression

**Visuals added** (Plotly; data: the Notebook's seeded 200 points and its 25/200 design, through a shared `images/data61.py`)
- `curve_to_plane.png` (Section 1, 3D): the training points against x and the new feature x² lie near the flat plane ŷ = 1.92 + 1.04x + 0.82x², the core trick of the Note in one picture.
- `line_misses.png` (Section 2): the best straight line (test R² 0.38) with its residuals coloured; above at both ends, below in the middle.
- `degree_sweep.gif` (Section 4): degrees 1 to 15, one per frame, with the training and test R² curves building up; test R² peaks at degree 2.

**Ladder changes:** the Overview now shows the idea (a curve in x is a plane in (x, x²)) before any code. Section 2 names the residual pattern and links it to assumption 1 of Note 56. Section 4 shows the process degree by degree before the table's verdict.

**Terms and IDs:** feature G-772, observation G-1374, target G-1949, polynomial regression G-1515, linear regression G-1094, degree G-577, PolynomialFeatures G-1516, include_bias G-929, underfitting G-2035, overfitting G-1429, hyperparameter G-910, interaction term G-959, condition number G-441.

**Numbers:** wpv 280 -> 169; figure share 3/5 -> 5/5.

**Text fixed:** the Note said training R² "rises with every extra degree", which exact least squares guarantees. Our fit dips by 0.0002 from degree 14 to 15; the condition-number Extra now says so and blames rounding (asserted in `degree_sweep.py`). Section 2 pointed at "the red line in Figure 2, left", a figure on a different 25-point design; it now points at the new figure of the 200-point data it describes. Figure references renumbered (1 to 6).

## 612-low-rank-approximation

**Visuals added** (Plotly)
- `storage.png` (Section 3): numbers stored, k(m + n + 1), against the 273,280 of the photo; 7.8% at k = 20 and break-even at k = 256.
- `eckart_young.png` (Section 4): on the Note's 2 × 2 matrix, the unit circle through the error of the truncated SVD (longest stretch 2.24) and of the other guess (3); and 20,000 seeded random rank-1 matrices, none with a spectral error below σ₂ = 2.236 (asserted).

**Ladder changes:** Section 3 shows the storage trade-off on a chart after the worked example. Section 4 adds an experiment between the theorem and its proof outline, so the "no other rank-k matrix wins" claim is seen before it is argued.

**Terms and IDs:** outer product G-1418, rank G-1629, rank-1 layer G-1631, rank-k approximation (truncated SVD) G-1630, spectral norm G-1852, Eckart–Young theorem G-657, Frobenius norm G-809, noise floor G-1328.

**Numbers:** wpv 375 -> 280; figure share 5/7 -> 7/7.

**Text fixed:** the Key terms entry "Rank $k$ approximation (truncated SVD)" did not match the glossary's "Rank-$k$ approximation (truncated SVD)" (G-1630), so a merge would have added a duplicate; it now matches. Figure references renumbered (1 to 7).

## 620-lagrange-multipliers

**Visuals added** (Plotly)
- `feasible.png` (Section 2): the Note's problem on its contour map; the feasible line, the forbidden unconstrained minimum (0, 0), the feasible (3, 0) with f = 9 and the best point (2, 1) with f = 6.
- `shadow_price.png` (Section 4.2): the best value f*(c) = 2c²/3 against the constraint position c, with its tangent of slope λ = 4 at c = 3 and the values 6.41 and 7.26 against the estimates 6.4 and 7.2.
- `ridge_lambda_t.png` (Section 7.1): a new experiment on the diabetes data (10 standardised features): each Ridge penalty λ matched with the circle size t = ‖w‖² of its weights; the curve reaches λ = 0 at the OLS size 4,295.
- `svm_alphas.png` (Section 7.2): the hard-margin linear SVM on 100 Iris flowers (setosa against versicolor, petal length and width); only 2 of 100 dual multipliers are nonzero (α = 1.18 each), the support vectors.

**Ladder changes:** Section 2 shows the feasible region before the general formulation is used. Section 4.2 draws the multiplier as a slope. Section 7 now has real-data evidence for both claims (one λ per circle; only support vectors have α > 0). The Overview's list-paragraph of Sections is now a bulleted list (§9).

**Terms and IDs:** gradient descent G-862, objective function G-1372, feasible region G-759, Lagrange multiplier G-1036, Lagrangian G-1037, shadow price G-1784, active constraint G-166, inactive constraint G-928, KKT conditions G-1013, complementary slackness G-424, primal problem G-1559, dual problem G-642, weak duality G-2103, strong duality G-1903, minimax inequality G-1225.

**Numbers:** wpv 579 -> 316; figure share 4/7 -> 7/7.

**Text fixed:** figure references renumbered (1 to 8); ESL's "Figure 3.11" kept.

## 622-linear-and-quadratic-programming

**Visuals added** (Plotly; the Note's workshop LP and triangle QP)
- `lp_normals.png` (Section 2.3): the dual condition at the best corner as arrows: the profit direction [3, 2] = 2 × oven normal + 1 × demand normal, so the multipliers are the weights.
- `shadow_bars.png` (Section 2.4): the profit re-solved with `linprog` after one more unit of each resource (13, 11, 12); the rises are the multipliers 2, 0, 1.
- `qp_kkt.png` (Section 3.2): the QP answer with −∇f = 4.5 × the active edge's normal.
- `qp_dual.png` (Section 3.3): the dual function along the edge multiplier, concave, below −12.25 and touching it at λ = 4.5.

**Ladder changes:** each derived condition (LP dual equality, KKT stationarity, QP dual) now has its geometric meaning drawn after the algebra, so the formal step is followed by a picture of what it says.

**Terms and IDs:** linear program G-1093, quadratic program G-1598, polytope G-1518, convex optimisation problem G-478, observation G-1374, positive definite matrix G-1530, quadratic form G-1597, KKT conditions G-1013, support vector machine G-1921.

**Numbers:** wpv 540 -> 255; figure share 3/3 -> 3/3 (all three numbered sections already had a figure; the gain is in words per visual).

**Text fixed:** figure reference renumbered (the QP region is now Figure 5). No facts changed.

## 63-ridge-regression-intuition

**Visuals added** (Plotly)
- `penalties.png` (Section 1): the three penalties (β², |β| and an even mix) for one coefficient; all are 0 at 0 and grow with size; the square is gentle near 0 and harsh far out, the absolute value has a corner.

**Ladder changes:** the Overview now pictures the three penalties named in its table before the Note narrows to Ridge.

**Terms and IDs:** regularisation G-1659, Ridge regression G-1691, L2 regularisation G-1029, Lasso regression G-1047, Elastic Net G-668, overfitting G-1429, feature G-772, observation G-1374, target G-1949, λ (lambda), alpha G-2150, hyperparameter G-910, bias-variance trade-off G-288, shrinkage G-1796, underfitting G-2035, standardisation G-1874.

**Numbers:** wpv 223 -> 200; figure share 3/4 -> 4/4.

**Text fixed:** the Key terms row "Feature, target, observation" was a combined term that is not in the glossary (a merge would have added it as a new entry); it is now three rows matching G-772, G-1949 and G-1374. Figure references renumbered (1 to 6), including the StatQuest credit (now Figure 4).

## 630-probability-vs-likelihood

**Visuals added** (Plotly)
- `bag_both.png` (Section 3): the bag read both ways: two probability bars for one draw with p = 2/5, and the likelihood curve p⁵ over every candidate p (0.010 at 2/5, 0.328 at 4/5).
- `one_table.png` (Section 5): one table of binomial probabilities P(k heads in 5 | p); a row (p = 0.5) is the probability reading, a column (k = 5) the likelihood reading. The single picture behind the Note's whole contrast.
- `sums.png` (Section 6): the row adds to 1; the area under the column's curve p⁵ is 1/6.

**Ladder changes:** Section 3 adds the picture of its two readings. Section 5 now shows that both definitions read one table, before the verbal definitions. Section 6 draws both sums.

**Terms and IDs:** Bernoulli distribution G-275, likelihood G-1086, observation G-1374, likelihood function G-1085, probability G-1574, plausibility G-1505 (now used in the definition of likelihood).

**Numbers:** wpv 392 -> 237; figure share 3/6 -> 6/6.

**Text fixed:** figure references renumbered (1 to 7). No facts changed.

## 64-ridge-regression-maths

**Visuals added** (Plotly; the Note's 100-observation `make_regression` example and its diabetes split)
- `ridge_lines.png` (Section 1): the OLS line (slope 27.83) and the Ridge lines for λ = 10 (24.95) and 100 (12.93), all through the point of means.
- `loss_shift.gif` (Section 2.3): the loss as a function of m (intercept at its best value) as λ grows: squared error plus the penalty bowl centred on 0; the minimum slides from 27.83 to 12.93 (asserted against the formula at every frame).
- `invertible.png` (Section 3.4 Extra): on the diabetes training data, the smallest eigenvalue of XᵀX + λI rises from 0.0073 and the condition number falls from 48,311 (about 3,290 at λ = 0.1).

**Ladder changes:** the Overview shows the result before the derivation; Section 2.3 shows why the λ in the denominator pulls the slope down, between the formula and the seesaw analogy. The invertibility Extra now has measured numbers.

**Terms and IDs:** feature G-772, observation G-1374, target G-1949, Ridge regression G-1691, identity matrix G-915, Cholesky solver G-383, closed-form solution G-398, multicollinearity G-1273, condition number G-441.

**Numbers:** wpv 472 -> 223; figure share 2/3 -> 3/3.

**Text fixed:** figure references renumbered (1 to 5). No facts changed.

## 640-gaussian-mixture-models

**Visuals added** (Plotly)
- `latent.png` (Section 4.2): 300 draws from the mixture, coloured by their hidden component and then as observed (all grey): what the latent variable is.
- `mvn_ellipses.png` (Section 5.1): contours of the Note's 2-D example (variances 1 and 4, density 0.0293 at (1, 2)) and the same with a covariance of 1.6, tilted.
- `circular.gif` (Section 7.3): the circular dependence on MML's seven points: μ₁ moves to −2.70, point −1's responsibility jumps from 0.057 to 0.56, and the formula then gives −2.34.
- `collapse.png` (Section 8): the spike on one point at σ₁ = 0.1 and the log-likelihood rising 2.30 per tenfold shrink (−17.25, −14.95, −12.65).

**Ladder changes:** Sections 4.2, 7.3 and 8 now show their mechanisms (lost labels, changing shares, the growing spike) next to the formulas.

**Terms and IDs:** observation G-1374, GMM G-829, mixture weight G-1238, convex combination G-475, generative process G-842, latent variable G-1050, multivariate normal G-1283, feature G-772, covariance matrix G-495, responsibility G-1687, soft assignment G-1826, total responsibility G-1992, adjusted Rand index G-175, multimodal G-1275, Bayes' theorem G-269, law of total probability G-1053, i.i.d. G-933, KDE G-1005, k-means G-996.

**Numbers:** wpv 541 -> 315; figure share 5/9 -> 9/9.

**Text fixed:** figure references renumbered (1 to 9); book figure numbers (11.2, 6.8b) kept.

## 65-ridge-gradient-descent

**Visuals added** (Plotly; diabetes split of the Note, test size 0.2, random state 4)
- `lr_limit.png` (Section 4): the from-scratch code's largest coefficient per epoch at learning rates 0.005 and 0.006, either side of the limit 2/353; the second grows to about 15,000, as the Extra states.
- `alpha_scale.png` (Section 6): coefficients of `SGDRegressor(alpha=0.001)` (50,000 epochs) on top of `Ridge(alpha=0.353)` and far from `Ridge(alpha=0.001)`; asserts the Extra's "within 3" and "about 840".

**Ladder changes:** the two code sections now show what the code produces, and the learning-rate Extra explains the overshoot factor (1.12 per step) seen in the figure.

**Terms and IDs:** Ridge regression G-1691, gradient descent G-862, feature G-772, observation G-1374, target G-1949, learning rate G-1068, weight decay G-2108, early stopping G-656, SGDRegressor G-1783, solver G-1836.

**Numbers:** wpv 356 -> 250; figure share 3/6 -> 5/6 (the Overview has no figure; Figure 1 follows in Section 2).

**Text fixed:** figure references renumbered (1 to 6). No facts changed.

## 66-ridge-key-points

**Visuals added** (Plotly)
- `one_vs_many.png` (Section 6): a new experiment backing Point 5. Diabetes data, 40 training observations, 200 random splits, alpha by cross-validation on the training part: with bmi alone Ridge gains nothing (0.30 against 0.31); with all 10 features it lifts test R² from 0.29 to 0.39.

**Ladder changes:** Point 5 was a claim with reasoning only; it now has evidence on the Note's data.

**Terms and IDs:** feature G-772, observation G-1374, target G-1949, Ridge regression G-1691, coefficient path G-409, bias G-287, bias-variance trade-off G-288, overfitting G-1429, underfitting G-2035, constrained form G-454, Lasso G-1047.

**Numbers:** wpv 248 -> 217; figure share 4/6 -> 5/6 (the Overview, a question-and-answer table, has no figure).

**Text fixed:** none.

## 67-lasso-regression

**Visuals added** (Plotly)
- `bias_variance.gif` (Section 6): the Notebook's bias-variance experiment drawn: 30 of the 200 degree-16 Lasso fits with their average against the true parabola, alpha by alpha, and the bias², variance and error curves (asserted to the table's values; lowest error at alpha 0.1).
- `ridge_vs_lasso.png` (Section 8): Ridge and Lasso coefficients on the diabetes split, both alpha 0.1: Lasso zeroes age, s2 and s4 (test R² 0.43), Ridge keeps all ten (0.45).

**Ladder changes:** Section 6 now pictures what high variance and high bias look like before the table's verdict; Section 8's comparison table gets a picture of the one difference that matters.

**Terms and IDs:** feature G-772, Lasso regression G-1047, L1 regularisation G-1026, observation G-1374, target G-1949, feature selection G-768, overfitting G-1429, underfitting G-2035, Elastic Net G-668.

**Numbers:** wpv 252 -> 192; figure share 5/8 -> 7/8 (the Overview has no figure).

**Text fixed:** the Lasso loss-curve figure is renumbered from 5 to 6.

## 70-perceptron-trick

**Visuals added**
- `loop.tex` (Section 5, TikZ, a still structure): the algorithm as a loop: start, pick a random point, correct side or not, do nothing or move the line, repeat, stop.
- `step_rule.png` (Section 7.2, Plotly): the step function with the Note's three points on the line 2x + 3y + 5 = 0 (w·x = 12, 21, −12 → ŷ = 1, 1, 0), linking the prediction to the sign of y − ŷ in the update rule.

**Ladder changes:** Section 5 now has its steps drawn before the farmer analogy; Section 7 shows the step function on the Note's own numbers before the compact rule.

**Terms and IDs:** logistic regression G-1120, perceptron G-1486, perceptron trick G-1485, observation G-1374, feature G-772, target G-1949, linearly separable G-1103, hyperplane G-911, positive and negative side G-1529, convergence G-472, learning rate G-1068, step function G-1889.

**Numbers:** wpv 238 -> 178; figure share 4/7 -> 6/7 (the Overview has no figure).

**Text fixed:** the combined Key-terms row "Feature, target, observation" (not a glossary term) is split into three rows matching G-772, G-1949, G-1374. Figure references renumbered (1 to 7).

## 72-sigmoid-function

**Visuals added** (Plotly)
- `step_update.png` (Section 3): y − ŷ with the step function against z: 0 for every correct point and ±1 for every wrong one at any distance, the problem the sigmoid fixes.
- `race.gif` (Section 7): the step and sigmoid perceptrons trained side by side on the Note's data with the same random points; the step line freezes after its last change at the 44th point, the sigmoid line keeps moving away from the green class (gaps 0.25 and 1.21 after 1,000 points, asserted against the table).

**Ladder changes:** Section 3 now pictures the flaw before introducing the sigmoid; Section 7 shows the process behind the table's numbers.

**Terms and IDs:** logistic regression G-1120, sigmoid function G-1798, push and pull G-1592, step function G-1889, logistic function G-1119, probabilistic interpretation G-1566, loss function G-1130.

**Numbers:** wpv 320 -> 233; figure share 4/7 -> 5/7 (the Overview and Section 2, the plan in words, have no figure).

**Text fixed:** figure references renumbered (1 to 6).

## 77-precision-recall-f1

**Visuals added** (Plotly)
- `spam_matrices.png` (Section 2): the two spam filters' confusion matrices (both accuracy 0.80) with the "predicted spam" column outlined: precision 0.50 against 0.91.
- `heart_scores.png` (Section 5): what the scikit-learn calls return on the heart-disease test set, recomputed from `data/heart.csv` with the Notebook's split and asserted to the table (logistic regression 0.800 / 0.966 / 0.875; decision tree 0.788 / 0.897 / 0.839).

**Ladder changes:** Section 2 now shows which cells the formula reads on the worked example; Section 5 shows the code's output.

**Terms and IDs:** confusion matrix G-449, precision G-1547, recall G-1641, F1 score G-743, true positive rate G-2022, harmonic mean G-880, support G-1924, macro average G-1143, weighted average G-2113, classification_report G-396.

**Numbers:** wpv 275 -> 191; figure share 4/6 -> 6/6.

**Text fixed:** figure references renumbered (1 to 6).

## 79-softmax-regression

**Visuals added** (Plotly)
- `training.gif` (Section 4.2): softmax regression trained by full-batch gradient descent on the Note's iris setup (standardised features): the three decision regions forming as the nine weights move together, and the categorical cross entropy falling from log 3 = 1.10 to 0.31 after 500 epochs (test accuracy 0.933; the Note's 0.967 is scikit-learn's converged fit).

**Ladder changes:** Section 4 had the loss formula without its process; it now shows training in action after the formula.

**Terms and IDs:** softmax regression G-1833, multinomial logistic regression G-1276, softmax function G-1830, observation G-1374, feature G-772, target G-1949, one-hot encoding G-1379, one-vs-rest G-1388, categorical cross entropy G-349, binary cross entropy G-303, decision region G-557.

**Numbers:** wpv 295 -> 237; figure share 3/5 -> 4/5 (the Overview has no figure).

**Text fixed:** the decision-regions figure is renumbered from 3 to 4.

## 82-conditional-probability

**Visuals added** (Plotly)
- `swap.png` (Section 4): the two-dice grid twice: given B the world is 33 cells and A covers 5 (5/33); given A the world is 6 cells and B covers 5 (5/6). The same overlap divided by different worlds.

**Ladder changes:** Section 4 had only the formula and a pointer to the last GIF scene; it now has its own still picture.

**Terms and IDs:** Naive Bayes G-1298, conditional probability G-444, event G-717, intersection G-967, sample space G-1729, reduced sample space G-1649.

**Numbers:** wpv 192 -> 153; figure share 2/4 -> 3/4 (the Overview has no figure).

**Text fixed:** none.

## 83-independent-events

**Visuals added** (Plotly)
- `product_area.png` (Section 2): the product rule as areas: A a band of width 1/6, B a band of height 1/6, their overlap a 1/36 rectangle.
- `coin_memory.png` (Section 4): one million simulated four-toss sequences (seed 0); after 0, 1, 2 or 3 heads the fourth toss is heads 0.499, 0.499, 0.502, 0.499 of the time, P(A | B) = P(A) on data.

**Ladder changes:** Section 2 now pictures the rule before the dice check; Section 4 adds evidence between the algebra and the counting Extra.

**Terms and IDs:** feature G-772, independent events G-934, product rule for independent events G-1576, dependent events G-590, target G-1949.

**Numbers:** wpv 210 -> 142; figure share 3/6 -> 5/6 (the Overview has no figure).

**Text fixed:** figure references renumbered (1 to 5).

## 84-mutually-exclusive-events

**Visuals added** (Plotly)
- `die_sim.png` (Section 3): one million simulated die rolls (seed 0): P(shows 3) = 0.1667 overall and exactly 0 among the rolls that showed 6; and the shares of 3, 6 and "3 or 6", whose sum gives the addition rule.

**Ladder changes:** Section 3 had the algebra only; it now has the counted evidence after it.

**Terms and IDs:** independent events G-934, mutually exclusive events G-1286, union G-2045, addition rule G-173.

**Numbers:** wpv 178 -> 135; figure share 2/4 -> 3/4 (the Overview has no figure).

**Text fixed:** the comparison figure (Figure 3) was never referred to in the text; one sentence now points to it.

## 86-bayes-problem

**Visuals added** (Plotly)
- `filter.gif` (Section 2): Bayes' theorem as filtering: a batch of 1,000 markers coloured by machine (200, 300, 500), the 24 defective ones lit up (10, 9, 5), then only those 24 left, giving the posteriors 0.417, 0.375, 0.208 by counting. Shown before any formula.

**Ladder changes:** the Note now opens the problem with the counting picture (plain idea), then the priors and likelihoods, then the law of total probability, then the formula.

**Terms and IDs:** law of total probability G-1053, Bayes' theorem G-269, prior G-1565, likelihood G-1086, probability tree G-1573, joint probability G-986, posterior G-1536, target G-1949, feature G-772.

**Numbers:** wpv 130 -> 112; figure share 4/6 -> 5/6 (the Overview has no figure).

**Text fixed:** figure references renumbered (1 to 5).

## 88-naive-bayes-maths

**Visuals added** (Plotly; the Note's 8-match cricket example, through a shared `images/nb_scores.py`)
- `evidence_drop.png` (Section 3): the scores 0.040 and 0.056 and the posteriors 0.42 and 0.58 after dividing by the evidence 0.096: dropping P(x) does not change the winner.
- `score_build.gif` (Section 6): the MAP rule built factor by factor; win leads on its prior (0.625 against 0.375) and falls behind at the toss factor (1/5 against 2/3), ending 0.040 against 0.056.

**Ladder changes:** Section 3's "evidence does not matter" is now shown on numbers; Section 6 shows the arg max as a process before stating the prediction.

**Terms and IDs:** observation G-1374, feature G-772, target G-1949, proportional to G-1584, chain rule of probability G-369, conditional independence G-443, arg max G-210, MAP rule G-1157.

**Numbers:** wpv 182 -> 136; figure share 4/7 -> 6/7 (Section 4, the chain-rule algebra, is covered by Figure 1 at the top).

**Text fixed:** figure references renumbered (1 to 6).

## 91-knn

**Visuals added** (Plotly)
- `scaling.png` (Section 3.2): the spread of the 30 breast cancer features on the training set, raw (about 0.002 to 554, `worst area` largest) against standardized (all 1), and the test accuracy raw 0.912 against scaled 0.974. It explains the 6-point gap the text reports.
- `imbalanced.png` (Section 7.4): the Notebook's imbalanced test as a confusion matrix: 1,469 common observations right but 29 of 30 rare ones missed (accuracy 0.98, recall 0.03). The Extra box became normal text because it is now the section's evidence.

**Ladder changes:** Section 3.2 explains the mechanism (one feature dominates every distance) with a picture; Section 7.4 shows its claim instead of only stating it.

**Terms and IDs:** KNN G-998, observation G-1374, feature G-772, target G-1949, query point G-1605, Euclidean distance G-715, neighbours G-1313, majority vote G-1146, Minkowski distance G-1227, standardization G-1874, accuracy G-162, k (n_neighbors) G-992, hyperparameter G-910, cross-validation G-510, decision surface G-560, overfitting G-1429, underfitting G-2035, lazy learning G-1057, instance-based learning G-955, latency G-1048, curse of dimensionality G-520, imbalanced data G-921, recall G-1641, inference G-943, black box model G-311.

**Numbers:** wpv 484 -> 370; figure share 5/7 -> 6/7 (the Overview has no figure). This Note is long (2,960 words), so its 370 words per visual sit close to the 400 limit.

**Text fixed:** figure references renumbered (1 to 8); the reference to Note 6's own Figure 2 and to Note 46's Figure 5 kept.

## 92-svm-intuition

**Visuals added** (Plotly; the Note's 16 points, through a shared `images/svm_data.py`)
- `only_sv.png` (Section 5): the hard-margin SVM trained on all 16 points and retrained on its 3 support vectors alone: the same line, w = (0.049, 0.898), b = −4.49 (equal to 3 decimals). The Extra's ISL claim is now shown, and moved into the main text as the section's evidence.
- `outlier.png` (Section 6 Extra): one extra point near the red class: the hard-margin SVM's margin falls from 2.22 to 0.56, while a soft-margin SVM (C = 1) keeps its line and margin of 2.22.

**Ladder changes:** Sections 5 and 6 now back their claims with experiments on the Note's data.

**Terms and IDs:** SVM G-1921, observation G-1374, feature G-772, target G-1949, margin G-1160, margin-maximising hyperplane G-1163, positive hyperplane G-1531, negative hyperplane G-1309, support vectors G-1923, SVR G-1922.

**Numbers:** wpv 349 -> 245; figure share 3/6 -> 5/6 (Section 3, the margin in words, uses Figure 1's anatomy).

**Text fixed:** none.

## 93-svm-maths

**Visuals added** (Plotly)
- `margin_sweep.gif` (Section 6): the optimisation problem as a search: for each direction of w (60 to 120 degrees), the widest margin that obeys every constraint, on the 16 points of Note 92. The curve has one peak, 2.22, at the direction of the SVM's w (asserted against scikit-learn's SVC).

**Ladder changes:** Section 6 now shows what "arg max 2/‖w‖ subject to the constraints" does before the code that solves it.

**Terms and IDs:** decision rule G-558, observation G-1374, feature G-772, target G-1949, constraint G-456, L2 norm G-1028, constrained optimisation G-455, hard-margin SVM G-879.

**New Key term not in the glossary:** "Norm of a vector" (already in this Note's Key terms table; the glossary has "L2 norm", G-1028, which the text now cites). Merge on the other machine, or rename the row to "L2 norm".

**Numbers:** wpv 270 -> 241; figure share 6/7 -> 7/7.

**Text fixed:** the outlier figure is renumbered from 6 to 7.

## 94-svm-soft-margin

**Visuals added** (Plotly; the Note's 18 points)
- `max_min.png` (Section 3): 2/‖w‖ and ‖w‖/2 against ‖w‖: one falls where the other rises, so maximising the first is minimising the second.
- `loss_bars.png` (Section 5): the soft-margin loss of the C = 1 line as stacked parts, margin error 0.45 plus C times 2.65, for C = 1 (3.10) and C = 10 (26.97). Recomputed with SVC and asserted.

**Ladder changes:** Section 3's rewrite and Section 5's two-term loss now each have a picture after the worked numbers.

**Terms and IDs:** soft-margin SVM G-1829, observation G-1374, feature G-772, target G-1949, slack G-1820, margin error G-1161, classification error G-393, C G-336, hyperparameter G-910, hinge loss G-898, regularisation G-1659.

**Numbers:** wpv 373 -> 259; figure share 4/8 -> 6/8 (Sections 2 and 8, short motivation and naming sections, have no figure).

**Text fixed:**
- The Note used ‖w‖ = 0.899 for the soft-margin line; that value belongs to Note 92's 16-point hard-margin SVM. The C = 1 line on this Note's 18 points has ‖w‖ = 0.8996, so the text now says 0.900 (1.33 / 0.900 = 1.48 and 0.900 / 2 = 0.45 are unchanged).
- "0.45 + 26.5 = 26.95" became "0.45 + 26.52 = 26.97": 10 × 2.652 = 26.52.
- The pointer to Note 93's outlier figure now says Figure 7 (it was renumbered in Note 93).
- Figure references renumbered (1 to 6).

## 95-kernel-trick-intuition

**Visuals added** (Plotly; the 34 points of the Note's lift animation, seed 0)
- `back_to_2d.png` (Section 5): the flat cut read back in the original plane: height z = exp(−r²) against distance r with the cut at z = 0.37, and the same cut as a circle of radius 0.99 that puts every green point inside (asserted). Note 96 already compares kernels in code, so this Note does not repeat that.

**Ladder changes:** Section 5's summary sentence ("linearly separable in a higher-dimensional space ... a curved boundary back in the original space") now has its mechanism drawn.

**Terms and IDs:** kernel trick G-1008, feature G-772, observation G-1374, non-linear data G-1335, kernel G-1004, kernel transformation G-1007, RBF kernel G-1639, polynomial kernel G-1514, sigmoid kernel G-1799, hyperparameter G-910.

**New Key term not in the glossary:** Feature space ("The space whose axes are the features; a kernel maps the data into a higher-dimensional one"), added to this Note's Key terms.

**Numbers:** wpv 342 -> 279; figure share 3/5 -> 4/5 (the Overview's figure counts; Section 2 shares Figure 2 with Section 3).

**Text fixed:** none.

## 97-decision-trees-intuition

**Visuals added** (Plotly)
- `path_length.png` (Section 5.1 Extra): a new measurement: fully grown scikit-learn trees on 1,000 to 300,000 synthetic observations need 8.2 to 23.2 questions per prediction, a straight line against log₂ n (about 1.8 questions per doubling). It backs the "logarithmic" claim and shows the tree is not perfectly balanced.
- `gain_race.gif` (Section 7.2): Step 5 one feature per frame: the 14 Play Tennis days split by each feature, child entropies, and the gains building up to outlook's 0.247 (asserted to the table).

**Ladder changes:** Section 7.2 now shows Step 5 as a process, not only a table.

**Terms and IDs:** decision tree G-561, feature G-772, observation G-1374, target G-1949, root node G-1706, splitting G-1855, decision node G-556, leaf node G-1060, branch G-332, hyper-cuboid G-907, axis-parallel split G-243, CART G-347, entropy G-691, differential entropy G-607, information gain G-946, greedy search G-871, Gini impurity G-847.

**Numbers:** wpv 392 -> 328; figure share 8/9 -> 9/9.

**Text fixed:** figure references renumbered (1 to 11).

## 98-decision-tree-hyperparameters

**Visuals added** (Plotly; the Notebook's moons split, 500 points, noise 0.3, random_state 42)
- `random_trees.png` (Section 4.2): three fully grown trees with `max_features=1` and different seeds draw different surfaces (test 0.880, 0.888, 0.864); the average vote of 50 such trees scores 0.888 against 0.856 for a single tree on average. Illustrates the Note's claim that randomness pays off only when trees are averaged.
- `leaf_sweep.gif` (Section 4.5): `min_samples_leaf` from 1 to 150: leaves fall from 43 to 2, training accuracy from 1.00 to 0.82, test accuracy peaks at 0.904 (value 10). Asserts the Note's 11 leaves at 20 and 3 at 100.

**Ladder changes:** Sections 4.2 and 4.5 now show their mechanism on the data before moving on.

**Terms and IDs:** feature G-772, observation G-1374, target G-1949, hyperparameter G-910, overfitting G-1429, underfitting G-2035, depth G-594, max_depth G-1184, fully grown tree G-813, cross-validation G-510, splitter G-1853, min_samples_split G-1221, pruning G-1587, min_samples_leaf G-1220, max_features G-1185, max_leaf_nodes G-1186, min_impurity_decrease G-1219.

**Numbers:** wpv 549 -> 382; figure share 3/5 -> 3/5 (the new figures sit in Section 4, which already had one; Sections 1 and 5 are an outline and a short closing).

**Text fixed:** the stopping-rules figure is renumbered from 4 to 6.

## 99-regression-trees

**Visuals added** (Plotly)
- `selection_bias.png` (Section 7.4): the Notebook's Boston grid: the 90 settings' cross-validated R² sorted, the winner at 0.725, and the same setting re-scored on 10 fresh shuffles of the folds at 0.663 (asserted). The "tallest of 90 people" analogy now has its picture.

**Ladder changes:** Section 7.4 adds the picture between the analogy and the measured numbers.

**Terms and IDs:** regression tree G-1654, feature G-772, observation G-1374, target G-1949, SSE G-1912, squared_error G-1864, DecisionTreeRegressor G-562, Boston housing data G-324, RandomizedSearchCV G-1625, selection bias G-2157, feature_importances_ G-773.

**New Key term not in the glossary:** "California housing data" (already in this Note's Key terms table, not yet merged).

**Numbers:** wpv 365 -> 327; figure share 6/7 -> 6/7 (the new figure is in Section 7, which already had figures; the Overview has none).

**Text fixed:** the feature-importance figure is renumbered from 8 to 9.
