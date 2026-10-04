# Round 3 report, list 3 (43 Notes)

Every Note was rebuilt with `tools/build.sh` and printed "Built". "Words per visual" and "figure share" count only the numbered teaching sections (Summary, Sources and Key terms are left out). All new figures are Plotly (charts and frame animations to GIF via ffmpeg, each GIF with a `_frames.png` grid for the PDF) unless stated. Each Note with an animation now has a small `images/anim.py` helper (render frames, write GIF and frame grid); it is not a figure.

## Summary

- **All 43 Notes are done and rebuilt.** A final sweep ran `tools/build.sh` on every Note, and every one printed "Built".
- **Targets met everywhere.** Words per visual are 420 or fewer in every Note (the highest is Note 39 at 420; 42 Notes are at or under 400). Figure share is at least 66% everywhere. Before this round, 31 of the 43 Notes missed one of the two targets.
- **102 new figures and animations**, all Plotly (charts, tables, 3D scenes and frame animations to GIF with a `_frames.png` grid). Every one was checked as an image and on its PDF page. Each script asserts the Note's own numbers, so the picture cannot drift from the text.
- **No matplotlib left in my Notes.** Two older scripts used seaborn and were rewritten in Plotly with the same data: `outlier_line.py` in Note 23 (now an animation) and `charts.py` in Note 25.
- **Glossary IDs** were added at first use throughout, looked up with `merge_glossary.py --id`. I also ran a semantic check, bold term against glossary definition. It found eight IDs whose glossary entry meant something else (precision, scaling, sparse, magnitude, weight, weights, rank, dimension), and I removed them. `glossary.md` and `merge_glossary.py` were not touched.
- **New Key terms for the merge:** only one, *Truncated normal*, added to Note 261's Key terms table. It already exists as G-2023, but that entry's definition is the Keras "redraw beyond two standard deviations" sense, so the merge may want to widen it to "a normal distribution restricted to a range".

**Text fixes worth flagging:**
- Note 252: a cube sum was 4.073, not 4.074.
- Note 262: the Box-Cox result is not a bell despite skewness near 0, now stated.
- Note 46: the timing ratio varies between runs, so the text now gives both measured values.
- Note 281: one interval catching 94.2% of new means was luck; the average is 0.837, now shown.

Each change is in its Note's entry below.

**Other notes:**
- Each Note with an animation has a small `images/anim.py` helper. It renders the frames and writes the GIF and frame grid; it is not a figure.
- `28-column-transformer/images/column_flow.gif` is 3.1 MB. It existed before this round and was left alone.
- No Keras runs were needed. Note 49's new figures use PCA fitted once on the Keras MNIST copy, stored as two small CSVs.
- Every `data/` folder stays under 1 MB.
- "Words per visual" and "figure share" were measured with one script over the numbered teaching sections, leaving out Summary, Sources and Key terms. Embedded `where_this_fits` maps were not counted.

## 223-frequency-tables-and-graphs
- **Visuals added:**
  - `running_total.gif` (Plotly frames): the vacation table built one category at a time; each step shows f, f/200 and the running total F, ending at 200 (section 2.1).
  - `bin_count.gif` (Plotly frames): the 714 Titanic ages in 2, 8, 20 and 80 bins, showing how the bin count hides or reveals the shape (section 3).
  - `two_features.png` (Plotly): class x survival crosstab, mean/median/max age per sex, and age band x sex crosstab, all from the Titanic numbers in the text, asserted (section 4).
- **Ladder:** section 3 now says what a bin is in three numbered steps (cut, place, count) before naming the histogram; section 4 shows the picture before the three cases.
- **Words per visual / figure share:** 495 and 60% before; 307 and 100% after.
- **Text fixed:** Overview contents sentence turned into a list (§9); glossary IDs added at first use for 17 terms (descriptive statistics, feature, observation, frequency distribution table, relative and cumulative frequency, pie chart, bin, histogram, bimodal, bivariate and multivariate analysis, contingency table, crosstab, aggregate, pivot table, hue, 3D scatter plot, facet grid). The Beach formula was rewritten so GitHub does not read `}_{` as italics.
- **New Key terms:** none.

## 23-what-is-feature-engineering
- **Visuals added:**
  - `outlier_line.gif` (Plotly frames), replacing the seaborn still `outlier_line.png` (matplotlib is not allowed): the three outliers are added one at a time and the least-squares line is refitted; the slope falls 1.91, 1.57, 1.20, 0.90 (asserted to fall at each step) (section 6.4).
  - `mnist_blank.gif` (Plotly frames): for each of the 784 MNIST pixels, the share of the 70,000 images where it is not blank; three thresholds drop 65, 290 and 441 pixels. Data `data/mnist_blank_share.csv` (6 KB), computed from the Keras copy of MNIST (section 8.1).
- **Ladder:** section 6.4 now explains why the line tilts (least squares keeps the total squared distance small, so far points pull it) with the slope numbers; section 8.1 backs "edge pixels are blank" with measured counts before naming the selection techniques.
- **Words per visual / figure share:** 251 and 100% before; 243 and 100% after.
- **Text fixed:** glossary IDs added at first use for 24 terms (EDA, feature, target, observation, feature engineering, raw data, domain knowledge, the four parts, mode, imputation, binning, outlier, linear regression, slope, feature scaling, log and Box-Cox transforms, MNIST, forward selection, backward elimination, PCA, LDA, high-dimensional data). Figures renumbered.
- **New Key terms:** none (slope is in the glossary already).

## 230-percentiles-and-box-plots
- **Visuals added:**
  - `percentile_rank.gif` (Plotly frames): each of the ten marks owns one tenth of a 0 to 100 scale; for 78, 84, 88, 93 and 99 the blocks below fill blue, the mark's own block orange, and the line stops halfway through it (5, 25, 35, 55, 95; checked against `scipy.stats.percentileofscore`) (section 3.2).
  - `iqr_robust.png` (Plotly): the ten values of section 5 with 1500 and with 15000; the box and IQR (94.25) stay, the mean (377.6 to 1727.6) and SD (406 to 4664) move (section 4, which had no figure).
- **Ladder:** section 4 now shows the robustness of the IQR with numbers and the reason (quartiles depend on middle positions; mean and SD add up every value) before naming **robustness**; section 3.2 names the percentile rank, then the picture, then the formula.
- **Words per visual / figure share:** about 457 and 67% before (4 visuals, section 4 had none); 345 and 83% after.
- **Text fixed:** Overview chain of ideas turned into a numbered list (§9); IDs added for quantiles, observation, feature, quartiles, quintiles, deciles, percentiles, median, percentile rank, five-number summary, IQR, robustness, standard deviation, box plot, fence, outlier, skewness. Two `}_{` formulas rewritten for GitHub.
- **New Key terms:** none.

## 231-covariance-and-correlation
- **Visuals added:**
  - `same_variance.png` (Plotly): the section 2 rising and falling point sets, same variances (2/3), covariance +2/3 and -2/3 (asserted) (section 2, which had no figure).
  - `cov_rectangles.gif` (Plotly frames): the five employees added one at a time; each product is drawn as the rectangle from the mean lines to the point, and the running sum reaches 86, so 86 / 4 = 21.5 (asserted against the table and `np.cov`) (section 3). Our own design.
  - `r_sweep.gif` (Plotly frames): the same 60 random points with r set exactly to -1, -0.9, ..., +1 (asserted), to read strength and direction (section 4.1).
- **Ladder:** section 3 now goes table, then picture, then a three-bullet reading of the rectangles (why each product is positive), then the sign rule; section 4.1 adds a picture and a three-bullet reading before the rules of thumb.
- **Words per visual / figure share:** 662 and 60% before; 361 and 100% after.
- **Text fixed:** IDs added for feature, observation, scatter plot, mean, variance, covariance, population, sample, linear relationship, Pearson correlation coefficient, correlation, standard deviation, causation, confounding variable, randomised controlled trial. Figures renumbered.
- **New Key terms:** none.

## 240-random-variables-and-distributions
- **Visuals added:**
  - `dice_grid.gif` (Plotly frames): the 6 x 6 grid of equally likely pairs; for each sum its diagonal lights up and its bar (pairs / 36) is added, ending with the full 1/36 to 6/36 to 1/36 distribution (asserted counts) (section 3.1, which had no figure).
  - `many_dice.gif` (Plotly frames): the exact distribution of the sum of 1, 2, 3, 5 and 10 dice by repeated convolution; 10 dice give 51 sums from 60,466,176 combinations (asserted), yet the graph is one simple hump (section 4, which had no figure).
- **Ladder:** section 4 now shows the table growing out of hand, then uses the picture to motivate a formula, before naming the probability distribution function.
- **Words per visual / figure share:** 459 and 62% before; 343 and 87% after.
- **Text fixed:** Overview list-paragraph turned into a list (§9); IDs added for random variable, random experiment, sample space, discrete and continuous random variable, probability distribution, equiprobable, probability distribution function, probability density, PMF, PDF, CDF, famous probability distributions, feature, normal distribution, parameters. A quoted inline formula rewritten so GitHub renders it.
- **New Key terms:** none.

## 243-density-estimation-kde
- **Visuals added:**
  - `more_data.gif` (Plotly frames): normal PDFs fitted to the first 10, 30, 100 and 1,000 values of the Note's seed-42 sample against the true N(50, 5); the 1,000-value fit (49.86, 4.94, asserted) lies on the true curve (section 3.3).
  - `normal_fails.png` (Plotly): the Note's two-peaked data with a fitted normal (one hump near the valley) and the bandwidth-3 KDE (both peaks), same draws as `kde_bandwidth.py`, s = 10.29 asserted (section 4, which had no figure).
  - `sample_vs_population.gif` (Plotly frames): four samples of 200 from the same two-peaked population; the histogram changes, the KDE stays close to the population PDF (asserted: L1 distance under 0.25 in every frame) (section 6, which had no figure).
- **Ladder:** section 3.3 now has the worked numbers per sample size; section 4 shows why the parametric assumption fails before defining the non-parametric method; section 6 shows sample against population before the list of ingredients.
- **Words per visual / figure share:** 531 and 50% before; 356 and 83% after.
- **Text fixed:** IDs added for density estimation, observation, feature, underlying distribution, Gaussian mixture model, parametric and non-parametric density estimation, kernel density estimate, kernel, Gaussian kernel, bandwidth, sampling bias. Figures renumbered.
- **New Key terms:** none.

## 25-normalization
- **Visuals added:**
  - `units.png` (Plotly): the five weights in kilograms, grams and pounds, and all three after min-max scaling (identical 0, 0.22, 0.29, 0.36, 1; asserted) (section 2, which had no figure).
  - `wine_ranges.png` (Plotly): each wine as a tick, training and test set, before and after `MinMaxScaler`; training ranges become exactly 0 to 1, the test set's malic acid runs -0.03 to 1.03 (asserted) (section 5, which had no figure).
  - `mean_norm_steps.gif` (Plotly frames): mean normalization of the five weights in two steps, subtract 68.6, then divide by 98 (section 7, which had no figure).
  - `sparse.png` (Plotly): the Note's sparse column after max-abs scaling (zeros stay 0) and after min-max scaling (zeros become 0.333) (section 8, which had no figure).
  - `charts.py` rewritten in Plotly (it used seaborn, i.e. matplotlib); `scatter_before_after.png` and `scalers_outlier.png` show the same data as before.
- **Ladder:** section 2 now shows the unit-removal idea on numbers, with the reason it works (a change of unit scales the value, minimum and maximum alike, so it cancels); section 8 shows why max-abs keeps sparsity before the Extra explains storage.
- **Words per visual / figure share:** 594 and 50% before; 353 and 90% after.
- **Text fixed:** Overview list-paragraph turned into a list (§9); IDs added for feature scaling, normalization, feature, observation, target, magnitude, min-max scaling, unit square, unit hypercube, `MinMaxScaler`, train-test split, mean normalization, mean centring, centred data, absolute value, max-abs scaling, `MaxAbsScaler`, sparse data, median, robust scaling, `RobustScaler`. Figures renumbered.
- **New Key terms:** none.

## 251-standard-normal-and-z-table
- **Visuals added:**
  - `phi_curve.png` (Plotly): the standard normal PDF with the worked values phi(0) = 0.3989 and phi(1) = 0.2420 (asserted) (section 2, which had no figure of its own).
  - `heights_tail.png` (Plotly): N(68, 3²) with the area above 72 inches shaded, tick labels in inches and z; area 0.09176 (asserted) (section 5.1).
  - `empirical_rule.gif` (Plotly frames): the areas within 1, 2 and 3 standard deviations shaded one step at a time, with Phi(k) - 0.5 per side (68.27, 95.45, 99.73, asserted) (section 6, which had no figure).
  - `age_outliers.png` (Plotly): the 714 Titanic ages with the mean and +1, +2, +3 SD lines; the two ages beyond 73.28 (74 and 80) circled (asserted) (section 7, which had no figure).
- **Ladder:** each worked problem now has its picture next to the steps; section 6 points to the animation before the table.
- **Words per visual / figure share:** 427 and 57% before; 223 and 100% after.
- **Text fixed:** Overview list-paragraph turned into a list (§9); IDs added for standard normal distribution, z-score, standardization, feature, observation, z-table, empirical rule, outlier, residual, hypothesis testing, central limit theorem. Figures renumbered.
- **New Key terms:** none.

## 252-skewness
- **Visuals added:**
  - `fare_tail.png` (Plotly): the 891 Titanic fares on a log count scale; the 45 highest fares (5 percent, from 113.28) carry 31.5 percent of the money (asserted) (section 3, which had no figure).
  - `cube_steps.gif` (Plotly frames): the sample skewness of 1, 2, 3, 4, 10 in four steps (distances, standardized values, cubes, G1 = 1.70; asserted against pandas) (section 5, which had no figure).
  - `symmetric_not_normal.png` (Plotly): 10,000 values each from a normal, uniform and symmetric two-humped distribution, all with skewness near 0 (asserted |skew| < 0.05) (section 6.1).
- **Ladder:** section 3 now backs the tail-event idea with measured fare numbers; section 5 explains with the picture why cubing makes the far value dominate before the formula's correction factor.
- **Words per visual / figure share:** 483 and 50% before; 269 and 83% after.
- **Text fixed:** the cube sum was 4.074 in the text; the five cubes it lists, and the exact computation, give 4.073 (G1 = 1.70 unchanged). Overview list-paragraph turned into a list (§9). IDs added for feature, skewness, positive and negative skew, tail event, measures of central tendency, mode, mean, statistical moment, sample skewness, Bessel's correction, Pearson's skewness coefficient, log transform, uniform distribution, Q-Q plot. Figures renumbered.
- **New Key terms:** none.

## 253-pdf-and-cdf-in-practice
- **Visuals added:**
  - `cutoff_sweep.gif` (Plotly frames): the versicolor/virginica cut-off slides from 1.3 to 1.9 cm across the two empirical CDFs, with each class's share right and the total right (128, 142, 144, 129...; 1.7 gives 0.98, 0.90 and 144, asserted) (section 3).
  - `ecdf_build.gif` (Plotly frames): the versicolor ECDF built by a sliding cut-off, flowers at or below it turning orange; 49/50 = 0.98 at 1.7 (asserted) (section 3.1, which had no figure).
- **Ladder:** section 3 now shows why the cut-off sits where it does (trade-off between the two classes) before the formula; section 3.1 builds the ECDF before naming it as the standard estimate.
- **Words per visual / figure share:** 437 and 75% before; 287 and 75% after (the four numbered teaching sections; section 3.1 is now illustrated but counts inside section 3).
- **Text fixed:** IDs added for feature, observation, target, iris dataset, feature selection, kernel density estimate, accuracy, empirical CDF, 2D density plot, contour plot. The sweep showed that 1.6 cm ties with 1.7 cm at 144 right; the text says so.
- **New Key terms:** none.

## 26-ordinal-label-encoding
- **Visuals added:**
  - `encode_rows.gif` (Plotly table frames): `OrdinalEncoder` on the Note's customer data; `fit` learns the two category lists from the 40 training rows, then `transform` fills in the codes row by row for six training rows and two test rows (first four rows asserted against the Note's table) (section 6.5, the core process, not animated before).
- **Ladder:** section 6.5 now shows the two steps happening before the table and the `categories_` attribute; the "UG would get 1" sentence now points at a real row in the figure.
- **Words per visual / figure share:** 304 and 100% before; 274 and 100% after.
- **Text fixed:** Overview list-paragraph of techniques turned into a list (§9); IDs added for feature, target, observation, numerical data, categorical data, one-hot encoding, nominal data, ordinal data, ordinal encoding, label encoding, classification, column transformer, `OrdinalEncoder`, `categories_`, `LabelEncoder`, `classes_`. Figure 8 reference fixed.
- **New Key terms:** none.

## 260-kurtosis-and-qq-plots
- **Visuals added:**
  - `z4_seasons.gif` (Plotly frames): kurtosis of the Note's two 8-match seasons in steps (scores, z-scores, z⁴, average), kurtosis 1 and 4 (asserted with scipy) (section 3.2).
  - `shapiro_n.png` (Plotly): a new experiment for the cited claim (Ghasemi and Zahediasl 2012) that normality tests flag small departures in large samples: share of 200 samples from a t distribution with 10 df that Shapiro-Wilk rejects at 5 percent, for n = 20 to 4,000 (12 percent to 100 percent) (section 6, which had no figure).
  - `laplace_qq.png` (Plotly): the Notebook's 1,000 standardized Laplace values on a Q-Q plot; ends at -5.41 and 4.82 against ±3.20 (asserted, same seed and draws as the Notebook) (section 8; the Extra that described it in words is now a figure with its text).
- **Ladder:** section 3.2 now shows why far values dominate (two 16s against six 0s) after the worked numbers; section 6 shows the sample-size effect before the advice to read tests with a Q-Q plot; the Laplace fat-tail case moved out of an Extra into the main text next to its picture.
- **Words per visual / figure share:** 557 and 44% before; 372 and 66% after.
- **Text fixed:** IDs added for kurtosis, feature, Q-Q plot, statistical moments, variance, tailedness, fat tail, excess kurtosis, leptokurtic, mesokurtic, platykurtic, kurtosis risk, volatile, statistical test, Shapiro-Wilk test, Anderson-Darling test, p-value, Laplace distribution. Two `}_A`/`}_B` formulas rewritten for GitHub. Figures renumbered.
- **New Key terms:** none.

## 261-uniform-and-log-normal
- **Visuals added:**
  - `truncated_normal.png` (Plotly): a normal height distribution (mean 5.8, sd 0.2 ft, an illustrative choice stated in the caption) cut to 5.6 to 6 ft keeps its bell shape, against the flat U(5.6, 6); backs the text's claim that a restricted normal is not uniform (section 2.3).
  - `log_morph.gif` (Plotly frames): the Note's 1,000 simulated comment lengths transformed by (x^λ - 1)/λ from λ = 1 (raw) to λ = 0 (the log); skewness 4.41, 1.09, 0.59, -0.02 (asserted to fall at every step) (section 3).
  - `lognormal_tail.png` (Plotly): Lognormal(3, 1) with median 20.1, mean 33.1 and P(X > 100) = 0.054 shaded (asserted), inside the Extra of section 3.2.
- **Ladder:** section 3 now shows "the log turns it into a bell" before the notation; the Extra's numbers have their picture.
- **Words per visual / figure share:** 490 and 100% before; 298 and 100% after.
- **Text fixed:** Overview list-paragraph turned into a list (§9); IDs added for non-Gaussian distribution, uniform distribution, discrete and continuous uniform, truncated normal, random initialization, data augmentation, hyperparameter tuning, log-normal distribution, feature, observation. A quoted formula rewritten for GitHub. Figures renumbered.
- **New Key terms:** Truncated normal (already in the glossary as G-2023; added to this Note's Key terms table).

## 262-pareto-and-power-law
- **Visuals added:**
  - `power_doubling.gif` (Plotly frames): y = x⁻² at x = 1, 2, 4, 8 on ordinary and log-log axes; each doubling divides y by 4 (asserted) and the log-log points lie on a line of slope -2 (section 2, which had no figure).
  - `alpha_share.gif` (Plotly frames): share of the total held by each fifth of a Pareto population for α = 1.16, 1.5, 2, 3, from the Note's formula p^(1-1/α) (80 and 34 percent asserted) (section 3.3).
  - `boxcox_pareto.png` (Plotly): the Note's 1,000 Pareto values (scipy, seed 42) raw, after the log and after Box-Cox: skewness 7.68, 1.87, 0.30, λ = -2.17 (asserted) (section 5, which had no figure).
- **Ladder:** section 2 shows why a power law is a straight line on log-log axes before section 4 uses it; section 5's workflow is now a numbered list with a worked example.
- **Words per visual / figure share:** 732 and 60% before; 397 and 100% after.
- **Text fixed:** Overview list-paragraph turned into a list (§9); IDs added for non-Gaussian distribution, power law, 80-20 rule, Pareto distribution, log-log plot, feature, mathematical transformation, Yeo-Johnson. The Box-Cox experiment showed that its result on Pareto data has skewness near 0 but is still not a bell; the text says so and points to the "symmetric is not normal" section of the skewness Note, rather than implying every transform yields a normal shape. Figures renumbered.
- **New Key terms:** none.

## 27-one-hot-encoding
- **Visuals added:**
  - `car_categories.png` (Plotly): the categories of fuel and owner in the 8128 cars with their counts (asserted), each becoming one column (section 5, which had no figure).
  - `dummies_steps.gif` (Plotly table frames): `pd.get_dummies` on the first four cars: fuel becomes 4 columns, owner 5 (12 in all), then `drop_first=True` leaves 10 (shapes asserted) (section 6, which had no figure).
  - `brand_grouping.gif` (Plotly frames): the 32 brands, then the 13 columns after the 20 rare brands become `uncommon` (538 cars; asserted) (section 8, which had no figure).
- **Ladder:** section 6 now shows the columns appearing before the shape arithmetic; section 8 shows the before and after of the grouping.
- **Words per visual / figure share:** 610 and 62% before; 391 and 100% after.
- **Text fixed:** Overview step sentence turned into a numbered list (§9); IDs added for feature, target, observation, one-hot encoding, vector, dummy variables, independent and dependent variables, multicollinearity, dummy variable trap, dimensionality, reference category, `get_dummies`, `OneHotEncoder`, sparse matrix, column transformer. Figures renumbered.
- **New Key terms:** none.

## 270-bernoulli-and-binomial
- **Visuals added:**
  - `n_trials.gif` (Plotly frames): the PMF of heads in n fair tosses for n = 1 (the Bernoulli PMF), 2, 3, 5, 10 (n = 3 asserted as 1/8, 3/8, 3/8, 1/8) (section 3, which had no figure).
  - `buyers_pmf.png` (Plotly): Binomial(1000, 0.1) with P(X = 50) = 3.2e-9, P(X = 100) = 0.042 and P(X ≥ 70) = 0.9996 (asserted) (section 5, which had no figure).
  - `not_independent.png` (Plotly): a simulation of the Note's workshop example; independent answers match Binomial(10, 0.5), linked answers (half the workshops copy one student) pile up at 0 and 10 (section 6, which had no figure).
- **Ladder:** section 3 shows "do it n times" growing from the Bernoulli bars; section 5's table now has its picture; section 6 shows what breaking independence does before moving on.
- **Words per visual / figure share:** 464 and 50% before; 313 and 87% after.
- **Text fixed:** IDs added for Bernoulli trial, Bernoulli distribution, target, observation, binary classifier, logistic regression, Naive Bayes, feature, categorical distribution, binomial distribution, independent events, survival function, binomial experiment, A/B testing, null hypothesis. A quoted inline formula rewritten for GitHub. Figures renumbered, including the credit line in Sources (Figure 7).
- **New Key terms:** none.

## 28-column-transformer
- **Visuals added:**
  - `covid_profile.png` (Plotly): the COVID toy data's cough categories (62/38), cities (32/30/22/16) and missing values per column (fever 10), each panel naming the transformer it needs (all asserted) (section 3, which had no figure).
  - `named_output.png` (Plotly table): the first three training patients after `set_output(transform="pandas")`, headers coloured by transformer (column names and values asserted against the text) (section 6, which had no figure).
- **Ladder:** section 3 shows the problems before the table of fixes; section 6 shows the named output after the naming rule.
- **Words per visual / figure share:** 476 and 50% before; 323 and 83% after.
- **Text fixed:** IDs added for feature, missing values, imputation, column transformer, observation, target, `ColumnTransformer`, `SimpleImputer`, `np.concatenate`, `remainder`, passthrough, pipeline, `get_feature_names_out`, `set_output`. Figures renumbered.
- **New Key terms:** none.

## 281-interpreting-confidence-intervals
- **Visuals added:**
  - `misreadings.png` (Plotly): misreadings 2 and 3 measured with the Notebook's draws (seed 1): one interval (45.30 to 53.62) catches 94.2% of new sample means and 21.7% of individual values (asserted); over 2,000 other first samples the share of new means caught averages 0.837, close to the derived 0.834 (asserted within 0.01) (section 3, which had no figure).
  - `n_shrink.gif` (Plotly frames): 20 intervals from the same standardized means at n = 10 to 1000; the margin falls 9.30 to 0.93 (asserted) while the same intervals miss (section 4.3).
- **Ladder:** section 3 now shows each misreading's real number before the Extra's derivation; section 4.3 shows the shrinking intervals and states why the miss count does not change.
- **Words per visual / figure share:** 572 and 60% before; 371 and 80% after.
- **Text fixed:** IDs added for confidence interval, confidence level, standard error, credible interval, Bayesian statistics, margin of error, critical value. The text said a lucky interval catching 94.2% of new means; the figure now shows that this is one interval's luck and the average is 0.837. Figures renumbered.
- **New Key terms:** none.

## 290-null-and-alternative-hypotheses
- **Visuals added:**
  - `null_world.png` (Plotly): what H0 claims, drawn: if μ = 6, the mean of 5 lessons varies by chance; using the five lessons' spread (s = 3.16) the one-sample t-test's curve puts the observed mean 9 at t = 2.12, with 5.1 percent of the curve at or beyond it (asserted against `scipy.stats.ttest_1samp`) (section 3, which had no figure). Consistent with the Note's verdict "just barely not" at 5 percent.
- **Ladder:** section 3 now explains in plain words that H0 means "any difference is chance", shows what chance alone would do, then names the test that measures it.
- **Words per visual / figure share:** 424 and 83% before; 372 and 100% after.
- **Text fixed:** IDs added for hypothesis testing, statistical hypothesis test, inferential statistics, null hypothesis, alternative hypothesis, mutually exclusive, status quo, research hypothesis, one-tailed test, rejection region approach, p-value approach, significance level, feature, z-test, t-test, chi-square test, ANOVA, test statistic. Figures renumbered.
- **New Key terms:** none.

## 292-errors-power-and-tails
- **Visuals added:**
  - `error_sim.png` (Plotly): 200 simulated training-program tests when H0 is true (13 Type I errors) and 200 when the true mean is 52 (61 Type II errors); a 100,000-test run confirms β = 0.29 (asserted) (section 2, which had no figure).
  - `feature_tests.png` (Plotly): `f_classif` on scikit-learn's wine dataset, one ANOVA F test per feature with its p-value; `SelectKBest(k=5)` keeps the five highest F (asserted) (section 6.2, which had no figure).
- **Ladder:** section 2 now shows both errors happening, with counts, before the definitions; section 6.2's feature-selection item has a worked example.
- **Words per visual / figure share:** 556 and 66% before; 396 and 100% after.
- **Text fixed:** IDs added for Type I and Type II error, false positive and negative, confusion matrix, power of a test, one-tailed and two-tailed test, feature, paired t-test, cross-validation, target, `SelectKBest`. Figures renumbered.
- **New Key terms:** none.

## 30-function-transformer
- **Visuals added:**
  - `fare_not_normal.png` (Plotly): the 891 Titanic fares against the normal curve with the same mean and SD (32.20, 49.69; median 14.45, max 512.33; over 20 percent of the normal below 0; all asserted) (section 2, which had no figure).
  - `three_transformers.png` (Plotly): `FunctionTransformer(np.log1p)`, `PowerTransformer()` and `QuantileTransformer(normal)` on the fares: skewness 4.79 to 0.39, -0.04 and -0.93 (section 3, which had no figure).
  - `log_vs_log1p.png` (Plotly): `np.log` against `np.log1p` near 0; the 15 zero fares map to 0 (asserted) (section 5.1).
  - `transform_shapes.png` (Plotly): the log(1 + x), square root, square and reciprocal curves with the section's worked values on them (asserted) (section 6, which had no figure).
- **Ladder:** section 2 shows "real data is rarely normal" on the Note's own data before the algorithm list; section 6 ends with a picture that compares all four transforms by the slope of their curves.
- **Words per visual / figure share:** 564 and 62% before; 379 and 100% after.
- **Text fixed:** IDs added for feature, target, observation, mathematical transformation, normal distribution, skewness, linear regression, decision tree, random forest, `FunctionTransformer`, `PowerTransformer`, `QuantileTransformer`, Q-Q plot, log transform, reciprocal, square and square root transform, `func`. Figures renumbered. The experiment showed that the 15 zero fares stay a separate group after every transformer, which is why the quantile transformer's skewness is negative; the text says so.
- **New Key terms:** none.

## 300-p-values
- **Visuals added:**
  - `repeat_coin.gif` (Plotly frames): 10 to 10,000 simulated 100-toss experiments with a fair coin; the share with 53 or more heads settles near the p-value 30.9% (31.2% at 10,000; asserted within 1.5 points) (section 4.1, which had no figure).
  - `p_vs_n.png` (Plotly): the p-value of the right-tailed z-test at a fixed true effect of 0.1 cars a day (σ = 5) as the sample grows; it falls below 0.05 at about 6,765 employees (asserted) (section 4.2, which had no figure).
- **Ladder:** section 4.1's "imagine repeating" is now done and shown; the "small p-value is not a large effect" misreading has its measured picture.
- **Words per visual / figure share:** 612 and 50% before; 384 and 66% after.
- **Text fixed:** IDs added for p-value approach, p-value, binomial distribution, Bayes' theorem. Figures renumbered.
- **New Key terms:** none.

## 33-mixed-variables
- **Visuals added:**
  - `type2_split.gif` (Plotly table frames): the Type 2 column `number` split row by row on the first six rows; numbers go to `number_numerical`, `A` to `number_categorical` (values asserted against the Note's table) (section 4.2, the core process, not animated before).
- **Ladder:** section 4.2 now shows the split happening before the code.
- **Words per visual / figure share:** 331 and 100% before; 297 and 100% after.
- **Text fixed:** IDs added for feature, target, observation, mixed variable, `pd.to_numeric`, `errors="coerce"`, nullable integer, `.str` accessor, regular expression, raw string. Figures renumbered.
- **New Key terms:** none.

## 330-events-and-types-of-events
- **Visuals added:**
  - `die_trials.gif` (Plotly frames): the die experiment run in 12 simulated trials; each outcome is boxed in the sample space and the event "odd" is marked when it happens (section 2, which had no figure of its own).
  - `pclass_space.png` (Plotly): the sample space {1, 2, 3} of Pclass with 216, 184 and 491 passengers; the event "not in first class" covers 675 (asserted). Data: `data/titanic_pclass.csv` (6 KB, the two columns needed, from the Titanic file used in Note 223) (section 3.3).
  - `exclusive_exhaustive.png` (Plotly): the four rows of the section 4.6 table on die faces; overlaps purple, gaps white (properties asserted) (section 4.6).
- **Ladder:** section 2 shows experiment, trial, outcome and event happening before the remaining definitions; section 4.6 shows "overlap" and "gap" as pictures before the table.
- **Words per visual / figure share:** 579 and 75% before; 343 and 100% after.
- **Text fixed:** Overview list-paragraph turned into a list (§9); IDs added for trial, outcome, sample space, event, observation, feature, simple event, compound event, independent and dependent events, without replacement, conditional probability, mutually exclusive and exhaustive events, partition, law of total probability, impossible and sure event. Figures renumbered.
- **New Key terms:** none.

## 331-empirical-and-theoretical-probability
- **Visuals added:**
  - `titanic_classes.png` (Plotly): the empirical probability of each Titanic class (0.242, 0.207, 0.551; asserted) against the wrong "1 out of 3" (section 3.2, which had no figure).
  - `die_rolls.gif` (Plotly frames): the share of each die face after 10, 1,000 and 100,000 rolls with the Notebook's seed 7; face 3 goes from 0 to 0.1662 (asserted) (section 5, which had no figure of its own).
  - `complement.png` (Plotly): the two-toss sample space split into "at least one head" and its complement "no heads" (section 6.2, which had no figure).
- **Ladder:** section 3.2 shows the counted probabilities before the warning in section 4's Extra; section 6.2 shows why the complement is the shortcut.
- **Words per visual / figure share:** 578 and 66% before; 343 and 100% after.
- **Text fixed:** IDs added for empirical and theoretical probability, probability, relative frequency, with replacement, favourable outcome, equally likely outcomes, law of large numbers, axioms of probability, complement. Figures renumbered. The older `images/convergence.png` is built but not used by the Note (the GIF's frame grid covers it); left as it was.
- **New Key terms:** none.

## 34-date-and-time
- **Visuals added:**
  - `extract_steps.gif` (Plotly table frames): the first five order dates with one `.dt` feature added per step (year, month, day, weekday, weekend, ISO week, quarter, semester; asserted against the Note's tables) (section 5, the core process, not animated before).
  - `order_calendar.png` (Plotly heatmap): the 2019 order rows as a calendar, ISO week by weekday, with quarter boundaries (section 5.7). The script is named `order_calendar.py` because a file named `calendar.py` shadows Python's standard `calendar` module and breaks pandas.
- **Ladder:** section 5 now shows the features being built before each subsection's code.
- **Words per visual / figure share:** 378 and 100% before; 309 and 100% after.
- **Text fixed:** IDs added for feature, observation, `pd.to_datetime`, datetime, NaT, `.dt` accessor, Timestamp, Timedelta, ISO calendar (G-975). Figures renumbered.
- **New Key terms:** none.

## 340-venn-diagrams-and-contingency-tables
- **Visuals added:**
  - `table_reads.png` (Plotly): the students' probability table four times, with the cells behind P(Maths ∩ Bio), P(Maths), P(Maths ∪ Bio) and P(neither) shaded (sums asserted) (section 3.3).
  - `venn_table_link.gif` (Plotly frames): the die example; each Venn region lights up with its contingency-table cell, then each whole circle with its total (regions asserted) (section 4, which had no figure).
- **Ladder:** section 4 shows the correspondence happening before the summary table of it.
- **Words per visual / figure share:** 541 and 75% before; 341 and 100% after.
- **Text fixed:** Overview list-paragraph turned into a list (§9); IDs added for Venn diagram, universal set, intersection, union, complement, De Morgan's law, contingency table, crosstab, feature, observation. Figures renumbered.
- **New Key terms:** none.

## 35-complete-case-analysis
- **Visuals added:**
  - `remove_vs_impute.png` (Plotly tables): four real rows of the job data; row 3's missing `enrolled_university` either removes the row (and its three good values) or is filled with the mode, `no_enrollment` (asserted) (section 3, which had no figure).
  - `rows_lost.gif` (Plotly frames): complete case analysis adding the five chosen columns one at a time; rows kept fall 100, 99.7, 97.7, 95.8, 93.4, 89.7 percent (17,182 of 19,158; asserted) (section 7, which had no figure).
- **Ladder:** section 3 shows the two options on real rows before naming the imputation families; section 7's first disadvantage now has its measured picture.
- **Words per visual / figure share:** 500 and 50% before; 382 and 75% after.
- **Text fixed:** IDs added for feature, target, observation, missing value, univariate and multivariate imputation, KNN imputer, iterative imputer, MICE, missing indicator, complete case analysis, MCAR, MAR, MNAR, `dropna`, KDE, `isnull()`. Figures renumbered.
- **New Key terms:** none.

## 350-linear-algebra-roadmap
- **Visuals added:**
  - `rows_as_vectors.png` (Plotly): three iris flowers as a 3 × 2 matrix and each row as a vector in feature space (section 2, which had no figure).
  - `numpy_outputs.png` (Plotly): what the `np.linalg` lines of section 4.8 compute: |v| = 5 and the eigenvectors of A stretched by 1.38 and 3.62 (asserted with `eigh`, since A is symmetric) (section 4.8).
- **Ladder:** section 2 now shows "data is matrices and vectors" on real data before pointing to the detailed Note.
- **Words per visual / figure share:** 456 and 60% before (counted with the fixed scorer); 294 and 80% after.
- **Text fixed:** Overview list-paragraph turned into a list (§9); IDs added for matrix, vector, scalar, observation, linear transformation, tensor, eigenvalue, eigenvector, matrix factorisation, quadratic form, Moore-Penrose pseudo-inverse, NumPy, SciPy. Figures renumbered.
- **New Key terms:** none.

## 36-imputing-numerical-data
- **Visuals added:**
  - `variance_shrink.gif` (Plotly frames): the 712 training ages before and after mean imputation; 148 filled ages stack at the mean and the one-SD band narrows (variance 204.35 to 161.81, asserted) (section 3.2, which had no figure).
  - `age_family_scatter.png` (Plotly): Age against Family before and after mean imputation; the filled ages form a flat line, and the correlation weakens from -0.299 to -0.245 (asserted) (section 3.4, which had no figure).
  - `imputer_fit_transform.gif` (Plotly table frames): `SimpleImputer` in a `ColumnTransformer`; fit learns median Age 28.75 and mean Fare 32.62, transform fills six test rows (asserted) (section 4, which had no figure).
- **Ladder:** sections 3.2 and 3.4 now show the mechanism (filled values add no distance; a flat line carries no trend) before the tables.
- **Words per visual / figure share:** 530 and 83% before; 367 and 100% after.
- **Text fixed:** IDs added for feature, target, observation, mean and median imputation, data leakage, variance, covariance, correlation, missing indicator, `statistics_`, `set_output`, arbitrary value and end of distribution imputation, `fillna`. Figures renumbered.
- **New Key terms:** none.

## 361-magnitude-distance-and-scalar-operations
- **Visuals added:**
  - `length_3d.png` (Plotly 3D): the length of [2, 3, 6] by Pythagoras twice (floor diagonal √13, then hypotenuse 7; asserted) (section 2.1).
  - `mean_centring.gif` (Plotly frames): the 150 iris flowers (sepal length and width) shifted by a growing fraction of their mean until the mean sits at the origin; spread unchanged (asserted) (section 5, which had no figure).
  - `scaling.gif` (Plotly frames): [2, 3] multiplied by 1, 2, 0.5 and -1; length |s| × 3.61, direction flipped for negative s (asserted) (section 6, which had no figure of its own).
- **Ladder:** section 2.1 now derives the 3D length step by step on numbers before the general formula; section 5 shows the shift on real data.
- **Words per visual / figure share:** 514 and 50% before; 282 and 100% after.
- **Text fixed:** Overview list-paragraph turned into a list (§9); IDs added for L2 and L1 norm, Euclidean distance, KNN, shifting, broadcasting, mean centring, feature, unit vector (the glossary's "precision" and "scaling" entries mean something else, so those words got no ID). Figures renumbered.
- **New Key terms:** none.

## 362-dot-product-and-cosine-similarity
- **Visuals added:**
  - `dot_steps.gif` (Plotly frames): [1, 2, 3] · [4, 5, 6] built one pair at a time, 4 + 10 + 18 = 32 (asserted) (section 3).
  - `projection.png` (Plotly): the projection of [3, 4] onto [7, 1], length 25 / 7.07 = 3.54 (asserted) (section 4, which had no figure). A new example, because the Note's pair [3, 4] and [4, 3] gives a shadow almost the same length as b and the picture would not show the idea.
  - `angle_examples.png` (Plotly): [3, 4] with [4, 3] (16.26°) and with [-4, 3] (dot product 0) (asserted) (section 5, which had no figure of its own).
  - `text_cosine.png` (Plotly heatmap): cosine similarity of the three toy summaries plus B written twice, computed with scikit-learn (0.29, 0, 1; asserted) (section 6.2, which had no figure).
- **Ladder:** section 3 shows the recipe in motion; section 4's projection item now has a worked number and a picture; section 6.2's Extra claim (length does not matter) is visible in the table.
- **Words per visual / figure share:** 726 and 50% before; 325 and 83% after.
- **Text fixed:** Overview list-paragraph turned into a list (§9); IDs added for dot product, scalar product, cross product, transpose, commutative and distributive law, projection, orthogonal, cosine similarity, similarity measure, bag of words. Figures renumbered.
- **New Key terms:** none.

## 363-equation-of-a-hyperplane
- **Visuals added:**
  - `iris_plane.png` (Plotly 3D): iris setosa and versicolor in three features separated by the plane a linear SVM (scikit-learn `LinearSVC`) found; every flower on its own side (asserted) (section 2, which had no figure).
  - `line_forms.png` (Plotly): 2x₁ + 3x₂ − 6 = 0 in school form (slope −2/3, intercept 2) and the points [3, 0], [0, 2], [1.5, 1] that satisfy it, against [3, 2] that does not (asserted) (section 3, which had no figure; also used by section 4's example).
- **Ladder:** section 2 shows a real separating plane before arguing for the n-dimensional equation; section 3 shows the two forms of the line on one picture.
- **Words per visual / figure share:** 575 and 50% before; 367 and 83% after.
- **Text fixed:** IDs added for hyperplane, feature, plane, slope, intercept, normal vector. Figures renumbered.
- **New Key terms:** none.

## 39-knn-imputer
- **Visuals added:**
  - `k_sweep.gif` (Plotly frames): the rows of the Note's five-row example placed by their nan-Euclidean distance from row 2; k = 1 to 4 neighbours averaged: 25, 32.5, 31.67, 36.25 (each checked against `KNNImputer`) (section 3.2, which had no figure).
  - `knn_cost.png` (Plotly): a new timing experiment for disadvantage 1: `KNNImputer` against `SimpleImputer` on synthetic data from 1,000 to 16,000 rows; KNN time grows more than 100-fold for 16 times the rows (asserted; exact times depend on the machine, and the text says so) (section 6, which had no figure).
  - `hidden_ages.png` (Plotly): one split of the Note's hidden-age test, filled against true age for mean imputation (a flat line) and KNN with k = 10 (same code as the Notebook's `fill_error`) (section 7.3).
- **Ladder:** section 3.2 shows how k changes the fill before the distance details; section 6's cost claim is now measured; section 7.3 shows what "closer to the truth" looks like.
- **Words per visual / figure share:** 696 and 57% before; 420 and 85% after.
- **Text fixed:** IDs added for feature, observation, target, KNN imputer, iterative imputer, similarity, KNN, instance-based learning, nan-Euclidean distance, grid search. Figures renumbered.
- **New Key terms:** none.

## 41-what-are-outliers
- **Visuals added:**
  - `study_marks.gif` (Plotly frames): the Note's study-hours example as example data (stated in the caption): 20 students, then two outliers with few hours and top marks; slope 3.33 to 1.91 and average error on the 20 students 4.5 to 8.4 marks (asserted that slope falls and error rises) (section 3, which had no figure).
  - `detect_treat.gif` (Plotly frames): detect then treat on the 714 known Titanic ages: IQR fences at -6.69 and 64.81, the 11 outliers above, then capping onto the fence (asserted). Data: `data/titanic_age.csv` (4 KB, the known ages from the Titanic file) (section 6, which had no figure).
- **Ladder:** section 3 now explains why the line tilts (least squares) with numbers; section 6 shows the two-part workflow on real data before sections 7 and 8 detail each part.
- **Words per visual / figure share:** 363 and 66% before; 291 and 88% after.
- **Text fixed:** IDs added for feature, observation, target, outlier, linear regression, coefficient (for "weights"), anomaly detection, trimming, capping, winsorization, discretization. Figures renumbered.
- **New Key terms:** none.

## 440-role-of-maths-in-ml
- **Visuals added:**
  - `descent_steps.gif` (Plotly frames): gradient descent on an illustrative error curve (stated in the caption), seven steps from w = 5 to the minimum, with the slope drawn at each step (error falls every step, asserted) (section 3: the one process in the Note, not animated before).
- **Ladder:** section 3 now goes slope (Figure 3), then the repeated step (Figure 4), before naming gradient descent's Note.
- **Words per visual / figure share:** 181 and 100% before; 158 and 100% after.
- **Text fixed:** IDs added for linear algebra, matrix, tensor, calculus, optimisation, derivative, gradient descent, irreducible error, data leakage, probability, Naive Bayes, statistics, feature, target. Figures renumbered.
- **New Key terms:** none.

## 45-feature-construction-splitting
- **Visuals added:**
  - `family_build.gif` (Plotly table frames): Family_size = SibSp + Parch + 1 built row by row for six Titanic passengers (section 3.2).
  - `ratio_feature.png` (Plotly): illustrative numbers (stated): two batters with 45 runs; raw runs equal, strike rate 150 against 100 (asserted) (section 4, which had no figure).
  - `tidy_names.png` (Plotly tables): the first four Titanic names, packed and split into surname, title and given names (asserted) (section 5, which had no figure).
- **Ladder:** section 4 shows why a ratio feature carries information before the Extra generalises; section 5 shows untidy against tidy on the Note's own data before section 6's code.
- **Words per visual / figure share:** 575 and 62% before; 370 and 87% after.
- **Text fixed:** IDs added for feature, target, observation, feature construction, domain knowledge, family size, family type, chained assignment, strike rate, economy rate, tidy data, atomic value, feature splitting, title. Figures renumbered.
- **New Key terms:** none.

## 46-curse-of-dimensionality
- **Visuals added:**
  - `two_problems.png` (Plotly): the two problems measured on the red-line experiment (same seed): the share of images whose nearest image shows the same digit (98.8, 91.0, 72.5 percent at 64, 164, 464 features, asserted against the Note's table) and the time to score KNN (section 5, which had no figure).
- **Ladder:** section 5 now shows both problems as curves before stating the fix.
- **Words per visual / figure share:** 329 and 50% before; 286 and 66% after.
- **Text fixed:** the timing sentence quoted one ratio (1.6); the new run measured 2.4, so the text now gives both and says timings vary. IDs added for feature selection and extraction, feature, observation, target, high-dimensional data, optimal number of features, curse of dimensionality, dimensionality reduction, cross-validation, PCA, LDA. The glossary's "sparse" means "mostly zero", which the Note explicitly contrasts with its own meaning, so that word got no ID. Figures renumbered.
- **New Key terms:** none.

## 47-pca-geometric-intuition
- **Visuals added:**
  - `two_to_one.gif` (Plotly frames): the Note's 30 made-up flats move onto the PC1 line and are described by one number each; PC1 keeps 98.1 percent of the variance (asserted with scikit-learn PCA) (section 3, which had no figure).
  - `square_vs_abs.png` (Plotly): |d| with its corner at 0 against the smooth d² (section 5.4, which had no figure).
- **Ladder:** section 3 now shows the result of feature extraction (two features become one) before section 4 explains how the line is found.
- **Words per visual / figure share:** 402 and 83% before; 297 and 100% after.
- **Text fixed:** IDs added for feature, observation, target, PCA, principal components, variance, mean absolute deviation, projection, unsupervised learning. Figures renumbered.
- **New Key terms:** none.

## 48-pca-step-by-step
- **Visuals added:**
  - `variance_by_angle.png` (Plotly): PCA's objective drawn as a curve: the variance of the projections of the previous Note's 30 flats for every direction (1.33 on the rooms axis, maximum 2.61 at 45°, minimum 0.05; equal to uᵀCu and the top eigenvalue, all asserted). `flats.py` is copied from Note 47 so the folder builds on its own (section 2.3).
- **Ladder:** section 2.3 now shows the maximisation before stating it, and links the peak forward to the eigenvector answer.
- **Words per visual / figure share:** 366 and 83% before; 329 and 83% after.
- **Text fixed:** Overview plan sentence turned into a numbered list (§9); IDs added for feature, observation, target, objective function, vector, unit vector, dot product, transpose, covariance matrix, linear transformation, eigenvector, eigenvalue, identity matrix, mean centring, eigen-decomposition. Figures renumbered.
- **New Key terms:** none.

## 49-pca-mnist
- **Visuals added:**
  - `image_row.png` (Plotly heatmaps): the first MNIST training image as 28 × 28 and as part of its 784-column row, with a red line every 28 columns (section 2, which had no figure).
  - `eigen_pictures.png` (Plotly heatmaps): the first six eigenvectors reshaped to 28 × 28; variance shares 9.7, 7.2, 6.1 percent, within 0.1 point of the Note's table (asserted) (section 6, which had no figure).
  - `mnist_data.py` fits PCA once on the 70,000 Keras MNIST images and stores two small CSVs (`data/mnist_components.csv` 42 KB, `data/mnist_example.csv` 5 KB) so the folder builds without the 11 MB dataset. The Note's own numbers come from a random 42,000 of the OpenML copy; the components are fitted on all 70,000 and the text says so.
- **Ladder:** section 6 now says, with a measured number, what the first eigenvector means: the average PC1 score is about 1,000 for 0s and about −840 for 1s (measured on all 70,000 images during this round; given in the text).
- **Words per visual / figure share:** 459 and 50% before; 338 and 75% after.
- **Text fixed:** IDs added for feature, observation, target, MNIST, classification, KNN, `explained_variance_`, `components_`, eigenvalue, eigenvector, cumulative explained variance. Figures renumbered.
- **New Key terms:** none.

## 490-linear-combinations-span-and-basis
- **Visuals added:**
  - `arrows_points.png` (Plotly): iris flowers as feature vectors, 10 as arrows and all 150 as points (section 2, which had no figure).
  - `basis_or_not.png` (Plotly): reaching [3, −2] with a basis (one way, 0.5v + 2.5w), with two vectors on one line (unreachable), and with a spare vector (two different combinations); all asserted (section 8, which had no figure).
- **Ladder:** section 8 now ends with the three cases as a list and a picture, after the definition.
- **Words per visual / figure share:** 501 and 62% before; 371 and 87% after.
- **Text fixed:** IDs added for feature, observations, standard basis, linear combination, span, linearly dependent and independent, basis, scalar. (The glossary's "rank", "dimension" and "magnitude" entries carry other meanings: tensor axes, one input column, the number part of a quantity; those words got no ID here or in Note 361.) Figures renumbered.
- **New Key terms:** none.

## 50-simple-linear-regression
- **Visuals added:**
  - `test_predictions.png` (Plotly): the 40 test students (random_state = 2), each prediction on the best-fit line and its gap to the real package; first student CGPA 8.58, real 4.10, predicted 3.89, slope 0.558 (asserted) (section 4, which had no figure).
- **Ladder:** section 4 now shows what `predict` does before the table of predictions.
- **Words per visual / figure share:** 412 and 60% before; 338 and 80% after.
- **Text fixed:** IDs added for linear regression, feature, target, observation, supervised learning, regression, simple, multiple and polynomial regression, LPA, slope, intercept, stochastic error, best-fit line, sum of squared errors, extrapolation. Figures renumbered.
- **New Key terms:** none.
