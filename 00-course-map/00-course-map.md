---
title: "Course Map"
---

## 1. Overview

> **Key point:** The Course map ties every Note together. It shows where each idea sits in an ML project, how ideas connect, what to read first, and which algorithm to choose.

The Notes each teach one lesson. The **Course map** (G-2160) shows how those lessons fit together, in four views:

- [**Pipeline map**](#2-the-pipeline-map) (G-2161): where does this idea sit in a real ML project?
- [**Concept map**](#3-the-concept-map) (G-2162): how is this idea connected to the others?
- [**Learning path**](#4-the-learning-path) (G-2163): which Notes should I read first?
- [**Algorithm chooser**](#5-the-algorithm-chooser) (G-2164): which algorithm suits my problem?

Each idea on the map is a **Concept** (G-2165); the course has 335.

Every Note starts with a *Where this fits* box: a small Pipeline map with that Note's steps highlighted, plus what it builds on and what it leads to.

> **Extra:** This map is generated from one data file, `course_map/concepts.yaml`. An interactive version, where you can zoom, filter by step and click a Concept to see its links and Notes, runs with `python course_map/app.py`.

<!-- playground: images/concept_playground.html -->

## 2. The Pipeline map

> **Key point:** Every ML project moves through the same steps, from framing the problem to monitoring the deployed model. Every Concept belongs to one step.

![The Pipeline map: 14 steps of an ML project](images/pipeline_overview.png)

Figure 1 shows the 14 steps. They follow the ML development life cycle, or **MLDLC** (G-1240):

1. frame the problem;
2. get the data and understand it;
3. clean the data;
4. engineer features;
5. train and evaluate models;
6. tune them;
7. deploy, test and keep the model healthy.

Steps 3 (Understand data) and 4 (Clean) loop: exploring reveals what needs cleaning, and cleaning changes the data, so we explore again.

### 2.1 Step 0: Foundations

- [Machine learning](../ML/01-foundations/ML-001-what-is-ml/ML-001-what-is-ml.md#2-defining-machine-learning)
- [Data mining](../ML/01-foundations/ML-001-what-is-ml/ML-001-what-is-ml.md#43-data-mining-finding-hidden-patterns)
- [Artificial intelligence](../ML/01-foundations/ML-002-ai-vs-ml-vs-dl/ML-002-ai-vs-ml-vs-dl.md#2-artificial-intelligence)
- [Symbolic AI and expert systems](../ML/01-foundations/ML-002-ai-vs-ml-vs-dl/ML-002-ai-vs-ml-vs-dl.md#3-symbolic-ai-and-expert-systems)
- [Deep learning](../ML/01-foundations/ML-002-ai-vs-ml-vs-dl/ML-002-ai-vs-ml-vs-dl.md#5-deep-learning)
- [Neural networks](../ML/01-foundations/ML-002-ai-vs-ml-vs-dl/ML-002-ai-vs-ml-vs-dl.md#51-neural-networks)
- [Features](../ML/01-foundations/ML-002-ai-vs-ml-vs-dl/ML-002-ai-vs-ml-vs-dl.md#52-features-chosen-by-us-or-learned)
- [Supervised learning](../ML/01-foundations/ML-003-types-of-ml/ML-003-types-of-ml.md#2-supervised-learning)
- [Regression problems](../ML/01-foundations/ML-003-types-of-ml/ML-003-types-of-ml.md#1-overview)
- [Classification problems](../ML/01-foundations/ML-003-types-of-ml/ML-003-types-of-ml.md#1-overview)
- [Unsupervised learning](../ML/01-foundations/ML-003-types-of-ml/ML-003-types-of-ml.md#3-unsupervised-learning)
- [Semi-supervised learning](../ML/01-foundations/ML-003-types-of-ml/ML-003-types-of-ml.md#4-semi-supervised-learning)
- [Reinforcement learning](../ML/01-foundations/ML-003-types-of-ml/ML-003-types-of-ml.md#5-reinforcement-learning)
- [Batch (offline) learning](../ML/01-foundations/ML-004-batch-learning/ML-004-batch-learning.md#3-batch-learning)
- [Online learning](../ML/01-foundations/ML-005-online-learning/ML-005-online-learning.md#2-what-online-learning-is)
- [Out-of-core learning](../ML/01-foundations/ML-005-online-learning/ML-005-online-learning.md#6-out-of-core-learning)
- [Instance-based learning](../ML/01-foundations/ML-006-instance-vs-model-based/ML-006-instance-vs-model-based.md#3-instance-based-learning)
- [Model-based learning](../ML/01-foundations/ML-006-instance-vs-model-based/ML-006-instance-vs-model-based.md#4-model-based-learning)
- [Applications of ML](../ML/01-foundations/ML-008-applications-of-ml/ML-008-applications-of-ml.md#1-overview)
- [ML development life cycle](../ML/01-foundations/ML-009-mldlc/ML-009-mldlc.md#15-key-terms)
- [Tensors](../ML/01-foundations/ML-010-tensors/ML-010-tensors.md#2-what-a-tensor-is)
- [Setup: conda, Jupyter and Colab](../ML/01-foundations/ML-011-setup-anaconda-jupyter-colab/ML-011-setup-anaconda-jupyter-colab.md#3-jupyter-notebooks)
- [Chi-square tests](../MA/04-inference/MA-045-chi-square-tests/MA-045-chi-square-tests.md#1-overview)
- [Vector magnitude, distance and scalar operations](../MA/05-linear-algebra/MA-049-magnitude-distance-and-scalar-operations/MA-049-magnitude-distance-and-scalar-operations.md#2-magnitude-the-distance-from-the-origin)
- [Normal distribution](../MA/03-distributions/MA-024-normal-distribution/MA-024-normal-distribution.md#2-what-the-normal-distribution-is)
- [Eigenvectors and eigenvalues](../MA/05-linear-algebra/MA-056-eigenvectors-and-eigenvalues/MA-056-eigenvectors-and-eigenvalues.md#2-eigenvectors-stay-on-their-own-span)
- [Dot product](../MA/05-linear-algebra/MA-050-dot-product-and-cosine-similarity/MA-050-dot-product-and-cosine-similarity.md#3-computing-the-dot-product)
- [Linear transformations and matrices](../MA/05-linear-algebra/MA-053-linear-transformations-and-matrices/MA-053-linear-transformations-and-matrices.md#7-where-ml-uses-linear-transformations)
- [Derivatives of one variable](../MA/06-calculus/MA-061-derivatives-of-one-variable/MA-061-derivatives-of-one-variable.md#1-overview)
- [Equation of a hyperplane](../MA/05-linear-algebra/MA-051-equation-of-a-hyperplane/MA-051-equation-of-a-hyperplane.md#4-the-vector-form)
- [Partial derivatives and gradients](../MA/06-calculus/MA-062-partial-derivatives-and-gradients/MA-062-partial-derivatives-and-gradients.md#12-the-gradient-on-the-map)
- [Conditional probability](../MA/02-probability/MA-015-conditional-probability/MA-015-conditional-probability.md#32-a-conditional-probability-by-counting)
- [Independent and mutually exclusive events](../MA/02-probability/MA-017-mutually-exclusive-events/MA-017-mutually-exclusive-events.md#3-conditional-probability-for-mutually-exclusive-events)
- [Bayes' theorem](../MA/02-probability/MA-018-bayes-theorem/MA-018-bayes-theorem.md#1-overview)
- [Bernoulli and binomial distributions](../MA/03-distributions/MA-031-bernoulli-and-binomial/MA-031-bernoulli-and-binomial.md#2-the-bernoulli-distribution)
- [Hessian and multivariate Taylor](../MA/06-calculus/MA-064-hessian-and-multivariate-taylor/MA-064-hessian-and-multivariate-taylor.md#5-the-hessian)
- [Taylor series](../MA/06-calculus/MA-064-hessian-and-multivariate-taylor/MA-064-hessian-and-multivariate-taylor.md#6-the-multivariate-taylor-series)
- [Probability distributions](../MA/03-distributions/MA-020-random-variables-and-distributions/MA-020-random-variables-and-distributions.md#3-probability-distributions-as-tables)
- [Inferential statistics](../MA/01-descriptive-stats/MA-003-statistics-roadmap/MA-003-statistics-roadmap.md#33-inferential-statistics)
- [Population, sample, parameter and statistic](../MA/01-descriptive-stats/MA-004-what-is-statistics/MA-004-what-is-statistics.md#2-what-statistics-is)
- [Random variables](../MA/03-distributions/MA-020-random-variables-and-distributions/MA-020-random-variables-and-distributions.md#2-random-variables)
- [Probability mass function (PMF)](../MA/03-distributions/MA-021-pmf-and-discrete-cdf/MA-021-pmf-and-discrete-cdf.md#3-the-probability-mass-function)
- [Uniform distribution](../MA/03-distributions/MA-029-uniform-and-log-normal/MA-029-uniform-and-log-normal.md#2-the-uniform-distribution)
- [Log-normal distribution](../MA/03-distributions/MA-029-uniform-and-log-normal/MA-029-uniform-and-log-normal.md#3-the-log-normal-distribution)
- [Poisson distribution](../MA/03-distributions/MA-032-poisson-distribution/MA-032-poisson-distribution.md#2-what-the-poisson-distribution-describes)
- [Standard normal and the z-table](../MA/03-distributions/MA-025-standard-normal-and-z-table/MA-025-standard-normal-and-z-table.md#2-the-standard-normal-distribution)
- [Pareto distribution and power laws](../MA/03-distributions/MA-030-pareto-and-power-law/MA-030-pareto-and-power-law.md#2-power-laws)
- [Sampling distribution and standard error](../MA/04-inference/MA-033-sampling-distribution-and-clt/MA-033-sampling-distribution-and-clt.md#3-sampling-distributions)
- [Central limit theorem](../MA/04-inference/MA-033-sampling-distribution-and-clt/MA-033-sampling-distribution-and-clt.md#4-the-central-limit-theorem)
- [Confidence intervals](../MA/04-inference/MA-035-confidence-intervals-z-procedure/MA-035-confidence-intervals-z-procedure.md#4-confidence-intervals-and-confidence-levels)
- [Student's t-distribution](../MA/04-inference/MA-037-t-procedure/MA-037-t-procedure.md#5-students-t-distribution)
- [Hypothesis testing: null and alternative](../MA/04-inference/MA-038-null-and-alternative-hypotheses/MA-038-null-and-alternative-hypotheses.md#4-the-alternative-hypothesis)
- [Z-test and rejection regions](../MA/04-inference/MA-039-rejection-region-and-z-test/MA-039-rejection-region-and-z-test.md#6-the-rejection-region-and-the-critical-value)
- [Type I and II errors, power, tails](../MA/04-inference/MA-040-errors-power-and-tails/MA-040-errors-power-and-tails.md#2-type-i-and-type-ii-errors)
- [P-values](../MA/04-inference/MA-041-p-values/MA-041-p-values.md#33-the-p-value-for-53-heads)
- [T-tests: one-sample, two-sample, paired](../MA/04-inference/MA-043-two-sample-and-paired-t-tests/MA-043-two-sample-and-paired-t-tests.md#2-the-independent-two-sample-t-test)
- [Events and sample spaces](../MA/02-probability/MA-010-events-and-types-of-events/MA-010-events-and-types-of-events.md#24-sample-space)
- [Empirical vs theoretical probability, probability rules](../MA/02-probability/MA-011-empirical-and-theoretical-probability/MA-011-empirical-and-theoretical-probability.md#1-overview)
- [Expected value and variance of a random variable](../MA/02-probability/MA-012-expected-value-and-variance/MA-012-expected-value-and-variance.md#3-expected-value)
- [Venn diagrams and contingency tables](../MA/02-probability/MA-013-venn-diagrams-and-contingency-tables/MA-013-venn-diagrams-and-contingency-tables.md#2-venn-diagrams)
- [Joint and marginal probability](../MA/02-probability/MA-014-joint-marginal-conditional-probability/MA-014-joint-marginal-conditional-probability.md#2-joint-probability)
- [Linear algebra roadmap](../MA/05-linear-algebra/MA-047-linear-algebra-roadmap/MA-047-linear-algebra-roadmap.md#7-sources)
- [Vectors and feature vectors](../MA/05-linear-algebra/MA-048-vectors-and-feature-vectors/MA-048-vectors-and-feature-vectors.md#2-what-a-vector-is)
- [Role of mathematics in ML](../MA/00-why-maths/MA-001-role-of-maths-in-ml/MA-001-role-of-maths-in-ml.md#1-overview)
- [Linear combinations, span and basis](../MA/05-linear-algebra/MA-052-linear-combinations-span-and-basis/MA-052-linear-combinations-span-and-basis.md#4-coordinates-are-scalars-basis-vectors)
- [Matrix multiplication as composition](../MA/05-linear-algebra/MA-054-matrix-multiplication-as-composition/MA-054-matrix-multiplication-as-composition.md#9-sources)
- [Determinant](../MA/05-linear-algebra/MA-056-eigenvectors-and-eigenvalues/MA-056-eigenvectors-and-eigenvalues.md#32-when-can-a-matrix-send-a-non-zero-vector-to-zero)
- [Choosing a hypothesis test](../MA/04-inference/MA-044-choosing-a-hypothesis-test/MA-044-choosing-a-hypothesis-test.md#1-overview)
- [One-sample proportion test](../MA/04-inference/MA-044-choosing-a-hypothesis-test/MA-044-choosing-a-hypothesis-test.md#4-one-categorical-feature-the-one-sample-proportion-test)
- [One-way ANOVA](../MA/04-inference/MA-046-one-way-anova/MA-046-one-way-anova.md#1-overview)
- [How to learn the maths for ML](../MA/00-why-maths/MA-002-learning-maths-for-ml/MA-002-learning-maths-for-ml.md#1-overview)
- [Jacobian and matrix gradients](../MA/06-calculus/MA-063-jacobian-and-matrix-gradients/MA-063-jacobian-and-matrix-gradients.md#4-the-jacobian)
- [Singular value decomposition](../MA/05-linear-algebra/MA-057-svd-geometry/MA-057-svd-geometry.md#1-overview)
- [Lagrange multipliers, KKT and duality](../MA/07-optimisation/MA-066-lagrange-multipliers/MA-066-lagrange-multipliers.md#6-lagrangian-duality)
- [Convex sets and convex optimisation](../MA/07-optimisation/MA-067-convex-sets-and-functions/MA-067-convex-sets-and-functions.md#2-convex-sets)
- [Linear and quadratic programming](../MA/07-optimisation/MA-068-linear-and-quadratic-programming/MA-068-linear-and-quadratic-programming.md#2-linear-programming)
- [Likelihood](../MA/08-likelihood/MA-069-probability-vs-likelihood/MA-069-probability-vs-likelihood.md#22-likelihood-from-the-event-back-to-the-parameter)
- [Maximum likelihood estimation (MLE)](../MA/08-likelihood/MA-070-maximum-likelihood-estimation/MA-070-maximum-likelihood-estimation.md#72-the-maximum-likelihood-estimate)
- [Exponential distribution](../MA/08-likelihood/MA-071-mle-for-common-distributions/MA-071-mle-for-common-distributions.md#3-the-exponential-distribution)
- [Multivariate normal distribution](../MA/08-likelihood/MA-073-gaussian-mixture-models/MA-073-gaussian-mixture-models.md#71-the-multivariate-normal)
- [What deep learning is](../DL/01-basics/DL-002-what-is-deep-learning/DL-002-what-is-deep-learning.md#1-overview)
- [Representation learning](../DL/01-basics/DL-002-what-is-deep-learning/DL-002-what-is-deep-learning.md#23-the-technical-definition-representation-learning)
- [History of deep learning](../DL/01-basics/DL-003-nn-types-history-applications/DL-003-nn-types-history-applications.md#3-history-of-deep-learning)
- [Universal approximation theorem](../DL/01-basics/DL-003-nn-types-history-applications/DL-003-nn-types-history-applications.md#33-universal-approximation)
- [Memoization](../DL/01-basics/DL-019-mlp-memoization/DL-019-mlp-memoization.md#3-memoization-on-the-fibonacci-numbers)
- [Exponentially weighted moving average (EWMA)](../DL/03-optimizers/DL-033-exponentially-weighted-moving-average/DL-033-exponentially-weighted-moving-average.md#3-two-rules-behind-the-ewma)
- [Sequential data](../DL/05-rnn/DL-055-why-rnn/DL-055-why-rnn.md#3-sequential-data)

### 2.2 Step 1: Frame the problem

- [Framing an ML problem](../ML/01-foundations/ML-013-framing-ml-problem/ML-013-framing-ml-problem.md#14-key-terms)

### 2.3 Step 2: Get data

- [Labelled data](../ML/01-foundations/ML-003-types-of-ml/ML-003-types-of-ml.md#21-learning-from-inputs-and-outputs)
- [Enough data](../ML/01-foundations/ML-007-challenges-in-ml/ML-007-challenges-in-ml.md#3-not-enough-data)
- [Sampling noise and bias](../ML/01-foundations/ML-007-challenges-in-ml/ML-007-challenges-in-ml.md#42-sampling-noise-and-sampling-bias)
- [APIs](../ML/01-foundations/ML-007-challenges-in-ml/ML-007-challenges-in-ml.md#2-collecting-data)
- [Web scraping](../ML/02-getting-data/ML-017-web-scraping/ML-017-web-scraping.md#2-when-we-need-web-scraping)
- [CSV files](../ML/01-foundations/ML-009-mldlc/ML-009-mldlc.md#42-where-data-comes-from)
- [JSON and SQL data](../ML/02-getting-data/ML-015-working-with-json-and-sql/ML-015-working-with-json-and-sql.md#2-what-json-is)

### 2.4 Step 3: Understand data

- [Exploratory data analysis](../ML/02-getting-data/ML-018-understanding-your-data/ML-018-understanding-your-data.md#1-overview)
- [Univariate analysis](../ML/02-getting-data/ML-019-univariate-analysis/ML-019-univariate-analysis.md#1-overview)
- [Bivariate and multivariate analysis](../ML/02-getting-data/ML-020-bivariate-multivariate-analysis/ML-020-bivariate-multivariate-analysis.md#13-sources)
- [Imbalanced data](../ML/09-clustering-and-more/ML-127-imbalanced-data/ML-127-imbalanced-data.md#2-what-imbalanced-data-looks-like)
- [Variance](../ML/02-getting-data/ML-018-understanding-your-data/ML-018-understanding-your-data.md#71-count-mean-standard-deviation-minimum-and-maximum)
- [Correlation](../MA/01-descriptive-stats/MA-009-covariance-and-correlation/MA-009-covariance-and-correlation.md#4-correlation)
- [Descriptive statistics](../MA/01-descriptive-stats/MA-003-statistics-roadmap/MA-003-statistics-roadmap.md#31-descriptive-statistics)
- [Probability density function (PDF)](../ML/02-getting-data/ML-019-univariate-analysis/ML-019-univariate-analysis.md#7-density-plot)
- [Kernel density estimation (KDE)](../MA/03-distributions/MA-023-density-estimation-kde/MA-023-density-estimation-kde.md#5-kernel-density-estimation-kde)
- [Skewness](../MA/03-distributions/MA-026-skewness/MA-026-skewness.md#2-skewness-as-distance-from-the-normal-shape)
- [Kurtosis and moments](../MA/03-distributions/MA-028-kurtosis-and-qq-plots/MA-028-kurtosis-and-qq-plots.md#21-statistical-moments)
- [Pandas Profiling](../ML/02-getting-data/ML-021-pandas-profiling/ML-021-pandas-profiling.md#1-overview)
- [Q-Q plot](../ML/03-feature-engineering/ML-029-function-transformer/ML-029-function-transformer.md#41-how-a-q-q-plot-is-built)
- [Covariance and covariance matrix](../MA/01-descriptive-stats/MA-009-covariance-and-correlation/MA-009-covariance-and-correlation.md#2-from-mean-to-variance-to-covariance)
- [Discrete and continuous data](../MA/01-descriptive-stats/MA-004-what-is-statistics/MA-004-what-is-statistics.md#62-discrete-and-continuous-data)
- [Measures of central tendency](../MA/01-descriptive-stats/MA-005-measures-of-central-tendency/MA-005-measures-of-central-tendency.md#1-overview)
- [Bessel's correction](../MA/01-descriptive-stats/MA-006-measures-of-dispersion/MA-006-measures-of-dispersion.md#61-the-sample-version)
- [Frequency tables](../MA/01-descriptive-stats/MA-007-frequency-tables-and-graphs/MA-007-frequency-tables-and-graphs.md#2-frequency-tables-for-a-categorical-feature)
- [Percentiles, quartiles and box plots](../MA/01-descriptive-stats/MA-008-percentiles-and-box-plots/MA-008-percentiles-and-box-plots.md#3-percentiles)
- [Correlation and causation](../MA/01-descriptive-stats/MA-009-covariance-and-correlation/MA-009-covariance-and-correlation.md#4-correlation)
- [Cumulative distribution function (CDF)](../MA/03-distributions/MA-021-pmf-and-discrete-cdf/MA-021-pmf-and-discrete-cdf.md#8-the-cumulative-distribution-function-of-a-discrete-variable)
- [Density estimation](../MA/03-distributions/MA-023-density-estimation-kde/MA-023-density-estimation-kde.md#2-what-density-estimation-is)
- [Correlation significance test](../MA/04-inference/MA-044-choosing-a-hypothesis-test/MA-044-choosing-a-hypothesis-test.md#1-overview)

### 2.5 Step 4: Clean

- [Poor-quality data](../ML/01-foundations/ML-007-challenges-in-ml/ML-007-challenges-in-ml.md#5-poor-quality-data)
- [Missing values](../ML/04-missing-data-and-outliers/ML-036-missing-categorical-data/ML-036-missing-categorical-data.md#1-overview)
- [Outliers](../ML/04-missing-data-and-outliers/ML-040-what-are-outliers/ML-040-what-are-outliers.md#2-what-an-outlier-is)
- [Simple imputation (mean, median, mode, constant)](../ML/03-feature-engineering/ML-022-what-is-feature-engineering/ML-022-what-is-feature-engineering.md#1-overview)
- [Complete case analysis](../ML/04-missing-data-and-outliers/ML-034-complete-case-analysis/ML-034-complete-case-analysis.md#4-complete-case-analysis)
- [Missing indicator](../ML/04-missing-data-and-outliers/ML-037-missing-indicator-random-sample/ML-037-missing-indicator-random-sample.md#6-missing-indicator)
- [Random sample imputation](../ML/04-missing-data-and-outliers/ML-037-missing-indicator-random-sample/ML-037-missing-indicator-random-sample.md#2-random-sample-imputation)
- [KNN imputer](../ML/04-missing-data-and-outliers/ML-038-knn-imputer/ML-038-knn-imputer.md#2-univariate-and-multivariate-imputation)
- [Iterative imputation (MICE)](../ML/04-missing-data-and-outliers/ML-039-iterative-imputer-mice/ML-039-iterative-imputer-mice.md#2-when-to-use-mice)
- [Trimming outliers](../ML/04-missing-data-and-outliers/ML-040-what-are-outliers/ML-040-what-are-outliers.md#1-overview)
- [Capping (winsorization)](../ML/04-missing-data-and-outliers/ML-040-what-are-outliers/ML-040-what-are-outliers.md#72-capping)
- [Z-score outlier method](../ML/04-missing-data-and-outliers/ML-040-what-are-outliers/ML-040-what-are-outliers.md#1-overview)
- [IQR outlier method](../ML/04-missing-data-and-outliers/ML-040-what-are-outliers/ML-040-what-are-outliers.md#1-overview)
- [Percentile outlier method](../ML/04-missing-data-and-outliers/ML-043-outliers-percentile/ML-043-outliers-percentile.md#1-overview)

### 2.6 Step 5: Engineer features

- [Feature construction and splitting](../ML/05-dimensionality/ML-044-feature-construction-splitting/ML-044-feature-construction-splitting.md#2-feature-construction)
- [Feature scaling](../ML/03-feature-engineering/ML-022-what-is-feature-engineering/ML-022-what-is-feature-engineering.md#65-feature-scaling)
- [Feature engineering](../ML/03-feature-engineering/ML-022-what-is-feature-engineering/ML-022-what-is-feature-engineering.md#2-what-feature-engineering-is)
- [Feature selection](../ML/03-feature-engineering/ML-022-what-is-feature-engineering/ML-022-what-is-feature-engineering.md#8-feature-selection)
- [Standardization](../ML/03-feature-engineering/ML-023-standardization/ML-023-standardization.md#4-the-standardization-formula)
- [One-hot encoding](../ML/03-feature-engineering/ML-026-one-hot-encoding/ML-026-one-hot-encoding.md#2-how-one-hot-encoding-works)
- [ML pipelines](../ML/03-feature-engineering/ML-028-pipelines/ML-028-pipelines.md#1-overview)
- [Encoding categorical data](../ML/03-feature-engineering/ML-025-ordinal-label-encoding/ML-025-ordinal-label-encoding.md#1-overview)
- [Binning and binarization](../ML/03-feature-engineering/ML-031-binning-binarization/ML-031-binning-binarization.md#31-what-binning-is-good-for)
- [Feature transformation](../ML/03-feature-engineering/ML-022-what-is-feature-engineering/ML-022-what-is-feature-engineering.md#6-feature-transformation)
- [Normalization](../ML/03-feature-engineering/ML-024-normalization/ML-024-normalization.md#2-what-normalization-is)
- [Ordinal and label encoding](../ML/03-feature-engineering/ML-025-ordinal-label-encoding/ML-025-ordinal-label-encoding.md#22-ordinal-data)
- [Column transformer](../ML/03-feature-engineering/ML-027-column-transformer/ML-027-column-transformer.md#53-building-and-using-the-column-transformer)
- [Function transformer](../ML/03-feature-engineering/ML-029-function-transformer/ML-029-function-transformer.md#7-function-transformer-on-the-titanic-data)
- [Power transformer](../ML/03-feature-engineering/ML-030-power-transformer/ML-030-power-transformer.md#2-power-transformer-in-scikit-learn)
- [Mixed variables](../ML/03-feature-engineering/ML-032-mixed-variables/ML-032-mixed-variables.md#2-what-a-mixed-variable-is)
- [Date and time features](../ML/03-feature-engineering/ML-033-date-and-time/ML-033-date-and-time.md#2-why-date-and-time-columns-are-useful)
- [Feature importance](../ML/08-trees-and-ensembles/ML-108-feature-importance/ML-108-feature-importance.md#2-what-feature-importance-is-for)
- [Permutation importance](../ML/08-trees-and-ensembles/ML-108-feature-importance/ML-108-feature-importance.md#7-permutation-importance)
- [Random under- and oversampling](../ML/09-clustering-and-more/ML-127-imbalanced-data/ML-127-imbalanced-data.md#6-random-oversampling)
- [SMOTE](../ML/09-clustering-and-more/ML-127-imbalanced-data/ML-127-imbalanced-data.md#7-smote)
- [Bag of words](../MA/05-linear-algebra/MA-048-vectors-and-feature-vectors/MA-048-vectors-and-feature-vectors.md#42-bag-of-words)
- [Scaling inputs for neural networks](../DL/02-training/DL-023-data-scaling-in-ann/DL-023-data-scaling-in-ann.md#1-overview)
- [Data augmentation](../DL/04-cnn/DL-050-data-augmentation/DL-050-data-augmentation.md#1-overview)
- [Sequence padding](../DL/05-rnn/DL-055-why-rnn/DL-055-why-rnn.md#1-overview)
- [Tokenization and integer encoding of text](../DL/05-rnn/DL-057-rnn-sentiment-analysis/DL-057-rnn-sentiment-analysis.md#32-tokenizing-in-keras)
- [Word embeddings](../DL/05-rnn/DL-057-rnn-sentiment-analysis/DL-057-rnn-sentiment-analysis.md#6-word-embeddings)
- [Contextual embeddings](../DL/06-transformers/DL-073-what-is-self-attention/DL-073-what-is-self-attention.md#5-static-and-contextual-embeddings)
- [Meaning as direction in embedding space](../DL/06-transformers/DL-072-meaning-as-direction/DL-072-meaning-as-direction.md#1-overview)

### 2.7 Step 6: Reduce dimensions

- [Dimensionality reduction](../ML/05-dimensionality/ML-045-curse-of-dimensionality/ML-045-curse-of-dimensionality.md#6-the-solution-dimensionality-reduction)
- [PCA](../ML/01-foundations/ML-003-types-of-ml/ML-003-types-of-ml.md)
- [Feature extraction](../ML/03-feature-engineering/ML-022-what-is-feature-engineering/ML-022-what-is-feature-engineering.md#9-feature-extraction)
- [Curse of dimensionality](../ML/05-dimensionality/ML-045-curse-of-dimensionality/ML-045-curse-of-dimensionality.md#2-what-the-curse-of-dimensionality-is)
- [Low-rank approximation (truncated SVD)](../MA/05-linear-algebra/MA-059-low-rank-approximation/MA-059-low-rank-approximation.md#22-splitting-any-matrix-into-layers)
- [Latent semantic analysis](../MA/05-linear-algebra/MA-060-svd-in-machine-learning/MA-060-svd-in-machine-learning.md#3-latent-semantic-analysis)

### 2.8 Step 7: Split

- [Train-test split](../ML/01-foundations/ML-012-toy-project/ML-012-toy-project.md#6-training-and-test-sets)
- [Data leakage](../ML/01-foundations/ML-012-toy-project/ML-012-toy-project.md#7-scaling-the-inputs)

### 2.9 Step 8: Model

- [Clustering](../ML/09-clustering-and-more/ML-125-hierarchical-clustering/ML-125-hierarchical-clustering.md#4-two-kinds-of-hierarchical-clustering)
- [Anomaly detection](../ML/01-foundations/ML-003-types-of-ml/ML-003-types-of-ml.md#34-anomaly-detection)
- [Association rule learning](../ML/01-foundations/ML-003-types-of-ml/ML-003-types-of-ml.md#35-association-rule-learning)
- [Stochastic gradient descent](../ML/06-regression/ML-058-stochastic-gradient-descent/ML-058-stochastic-gradient-descent.md#3-how-stochastic-gradient-descent-works)
- [K-nearest neighbours](../ML/01-foundations/ML-006-instance-vs-model-based/ML-006-instance-vs-model-based.md#31-how-it-works)
- [Ensemble learning](../ML/08-trees-and-ensembles/ML-095-ensemble-learning/ML-095-ensemble-learning.md#1-overview)
- [Logistic regression](../ML/07-classification/ML-074-logistic-gradient-descent/ML-074-logistic-gradient-descent.md#1-overview)
- [Multicollinearity](../ML/03-feature-engineering/ML-026-one-hot-encoding/ML-026-one-hot-encoding.md#32-multicollinearity-inputs-must-not-depend-on-each-other)
- [K-means](../ML/03-feature-engineering/ML-031-binning-binarization/ML-031-binning-binarization.md#7-k-means-binning)
- [Simple linear regression](../ML/06-regression/ML-049-simple-linear-regression/ML-049-simple-linear-regression.md#1-overview)
- [Best-fit line and squared error](../ML/06-regression/ML-049-simple-linear-regression/ML-049-simple-linear-regression.md#34-the-best-fit-line)
- [Ordinary least squares (closed form)](../ML/06-regression/ML-050-linear-regression-maths/ML-050-linear-regression-maths.md#2-two-ways-to-find-m-and-b)
- [Multiple linear regression](../ML/06-regression/ML-052-multiple-linear-regression/ML-052-multiple-linear-regression.md#4-multiple-linear-regression-in-scikit-learn)
- [Normal equation](../ML/06-regression/ML-053-multiple-lr-maths/ML-053-multiple-lr-maths.md#6-the-normal-equation)
- [Assumptions of linear regression](../ML/06-regression/ML-055-linear-regression-assumptions/ML-055-linear-regression-assumptions.md#9-sources)
- [Gradient descent](../ML/06-regression/ML-056-gradient-descent/ML-056-gradient-descent.md#7-gradient-descent-as-a-class)
- [Convex and non-convex loss](../MA/07-optimisation/MA-065-convex-and-non-convex-cost-functions/MA-065-convex-and-non-convex-cost-functions.md#32-why-convexity-matters-one-minimum)
- [Batch gradient descent](../ML/06-regression/ML-057-batch-gradient-descent/ML-057-batch-gradient-descent.md#4-batch-gradient-descent-in-code)
- [Mini-batch gradient descent](../ML/06-regression/ML-059-mini-batch-gradient-descent/ML-059-mini-batch-gradient-descent.md#1-overview)
- [Polynomial regression](../ML/06-regression/ML-060-polynomial-regression/ML-060-polynomial-regression.md#1-overview)
- [Polynomial features](../ML/06-regression/ML-060-polynomial-regression/ML-060-polynomial-regression.md#1-overview)
- [Regularisation](../ML/06-regression/ML-062-ridge-regression-intuition/ML-062-ridge-regression-intuition.md#1-overview)
- [Ridge regression](../ML/06-regression/ML-062-ridge-regression-intuition/ML-062-ridge-regression-intuition.md#1-overview)
- [Lasso regression](../ML/06-regression/ML-066-lasso-regression/ML-066-lasso-regression.md#1-overview)
- [Elastic Net](../ML/06-regression/ML-068-elastic-net/ML-068-elastic-net.md#6-elastic-net-on-the-diabetes-data)
- [Perceptron trick](../ML/07-classification/ML-069-perceptron-trick/ML-069-perceptron-trick.md#5-the-perceptron-trick)
- [Sigmoid function](../ML/07-classification/ML-071-sigmoid-function/ML-071-sigmoid-function.md#4-the-sigmoid-function)
- [Log loss (binary cross entropy)](../ML/07-classification/ML-072-log-loss/ML-072-log-loss.md#62-the-loss-function)
- [Softmax regression](../ML/07-classification/ML-078-softmax-regression/ML-078-softmax-regression.md#1-overview)
- [Naive Bayes](../ML/07-classification/ML-081-naive-bayes-intuition/ML-081-naive-bayes-intuition.md#1-overview)
- [Support vector machines](../ML/07-classification/ML-086-svm-intuition/ML-086-svm-intuition.md#9-sources)
- [Hinge loss and soft margin](../ML/07-classification/ML-088-svm-soft-margin/ML-088-svm-soft-margin.md#8-why-soft-margin)
- [Kernel trick](../ML/07-classification/ML-089-kernel-trick-intuition/ML-089-kernel-trick-intuition.md#3-the-kernel-trick)
- [Entropy, information gain and Gini](../ML/08-trees-and-ensembles/ML-091-decision-trees-intuition/ML-091-decision-trees-intuition.md#6-entropy)
- [Decision trees](../ML/08-trees-and-ensembles/ML-091-decision-trees-intuition/ML-091-decision-trees-intuition.md#2-a-decision-tree-is-nested-if-else)
- [Regression trees](../ML/08-trees-and-ensembles/ML-093-regression-trees/ML-093-regression-trees.md#3-how-a-regression-tree-predicts)
- [Boosting](../ML/08-trees-and-ensembles/ML-113-bagging-vs-boosting/ML-113-bagging-vs-boosting.md#21-boosting-high-bias-low-variance-models)
- [Voting ensembles](../ML/08-trees-and-ensembles/ML-096-voting-ensemble/ML-096-voting-ensemble.md#1-overview)
- [Bagging](../ML/08-trees-and-ensembles/ML-099-bagging-intuition/ML-099-bagging-intuition.md#3-why-bagging-works)
- [Random forest](../ML/08-trees-and-ensembles/ML-102-random-forest-intro/ML-102-random-forest-intro.md#2-why-random-forests-are-so-popular)
- [AdaBoost](../ML/08-trees-and-ensembles/ML-109-adaboost-intuition/ML-109-adaboost-intuition.md#11-why-learn-adaboost)
- [Gradient boosting](../ML/08-trees-and-ensembles/ML-114-gradient-boosting-intuition/ML-114-gradient-boosting-intuition.md#13-gradient-boosting-compared-with-adaboost)
- [XGBoost](../ML/08-trees-and-ensembles/ML-117-xgboost-intro/ML-117-xgboost-intro.md#3-what-xgboost-is)
- [Stacking and blending](../ML/08-trees-and-ensembles/ML-121-stacking-blending/ML-121-stacking-blending.md#2-from-voting-to-stacking)
- [Hierarchical clustering](../ML/09-clustering-and-more/ML-125-hierarchical-clustering/ML-125-hierarchical-clustering.md#4-two-kinds-of-hierarchical-clustering)
- [DBSCAN](../ML/09-clustering-and-more/ML-126-dbscan/ML-126-dbscan.md#8-the-dbscan-algorithm-step-by-step)
- [Balanced random forest](../ML/09-clustering-and-more/ML-127-imbalanced-data/ML-127-imbalanced-data.md#8-ensemble-methods-the-balanced-random-forest)
- [Cost-sensitive learning](../ML/09-clustering-and-more/ML-127-imbalanced-data/ML-127-imbalanced-data.md#9-cost-sensitive-learning)
- [Cosine similarity](../MA/05-linear-algebra/MA-050-dot-product-and-cosine-similarity/MA-050-dot-product-and-cosine-similarity.md#6-cosine-similarity)
- [Moore-Penrose pseudo-inverse](../MA/05-linear-algebra/MA-060-svd-in-machine-learning/MA-060-svd-in-machine-learning.md#1-overview)
- [Categorical and sparse categorical cross-entropy](../MA/08-likelihood/MA-072-mle-in-machine-learning/MA-072-mle-in-machine-learning.md#5-a-categorical-target-gives-the-cross-entropy)
- [MAP estimation](../MA/08-likelihood/MA-072-mle-in-machine-learning/MA-072-mle-in-machine-learning.md#7-map-estimation-maximum-likelihood-plus-a-prior)
- [Gaussian mixture model (GMM)](../MA/08-likelihood/MA-073-gaussian-mixture-models/MA-073-gaussian-mixture-models.md#32-the-standard-terms)
- [Expectation maximization (EM)](../MA/08-likelihood/MA-074-expectation-maximization/MA-074-expectation-maximization.md#1-overview)
- [Types of neural networks](../DL/01-basics/DL-003-nn-types-history-applications/DL-003-nn-types-history-applications.md#2-types-of-neural-networks)
- [Multi-layer perceptron (MLP)](../DL/01-basics/DL-003-nn-types-history-applications/DL-003-nn-types-history-applications.md#21-multi-layer-perceptron-mlp)
- [Perceptron](../DL/01-basics/DL-004-perceptron/DL-004-perceptron.md#3-the-parts-of-a-perceptron)
- [Perceptron loss](../DL/01-basics/DL-006-perceptron-loss/DL-006-perceptron-loss.md#6-the-perceptron-loss)
- [Problem with the perceptron (XOR)](../DL/01-basics/DL-007-problem-with-perceptron/DL-007-problem-with-perceptron.md#1-overview)
- [MLP notation and parameter count](../DL/01-basics/DL-008-mlp-notation/DL-008-mlp-notation.md#7-sources)
- [Forward propagation](../DL/01-basics/DL-010-forward-propagation/DL-010-forward-propagation.md#1-overview)
- [Keras workflow](../DL/01-basics/DL-011-customer-churn-ann/DL-011-customer-churn-ann.md#11-key-terms)
- [ANN for classification](../DL/01-basics/DL-011-customer-churn-ann/DL-011-customer-churn-ann.md#1-overview)
- [ANN for regression](../DL/01-basics/DL-013-graduate-admission-ann/DL-013-graduate-admission-ann.md#1-overview)
- [Loss functions in deep learning](../DL/01-basics/DL-014-dl-loss-functions/DL-014-dl-loss-functions.md#13-sources)
- [Huber loss](../DL/01-basics/DL-014-dl-loss-functions/DL-014-dl-loss-functions.md#7-huber-loss)
- [Backpropagation](../DL/01-basics/DL-015-backpropagation-what/DL-015-backpropagation-what.md#4-the-steps-of-backpropagation)
- [Vanishing gradient](../DL/01-basics/DL-018-vanishing-exploding-gradients/DL-018-vanishing-exploding-gradients.md#3-the-vanishing-gradient-problem)
- [Exploding gradient and gradient clipping](../DL/01-basics/DL-018-vanishing-exploding-gradients/DL-018-vanishing-exploding-gradients.md#7-the-exploding-gradient-problem)
- [ReLU](../DL/02-training/DL-028-relu-variants/DL-028-relu-variants.md#3-the-dying-relu-problem)
- [Batch size in Keras](../DL/02-training/DL-020-gradient-descent-in-neural-networks/DL-020-gradient-descent-in-neural-networks.md#1-overview)
- [Dropout](../DL/02-training/DL-024-dropout/DL-024-dropout.md#4-how-dropout-works)
- [L1 and L2 regularisation in neural networks](../DL/02-training/DL-026-regularization-in-dl/DL-026-regularization-in-dl.md#10-key-terms)
- [Activation functions](../DL/02-training/DL-027-activation-functions/DL-027-activation-functions.md#3-what-an-activation-function-is)
- [Tanh](../DL/02-training/DL-027-activation-functions/DL-027-activation-functions.md#7-tanh)
- [Dying ReLU problem](../DL/02-training/DL-028-relu-variants/DL-028-relu-variants.md#3-the-dying-relu-problem)
- [Leaky ReLU, PReLU, ELU and SELU](../DL/02-training/DL-028-relu-variants/DL-028-relu-variants.md#51-leaky-relu)
- [Weight initialisation](../DL/02-training/DL-029-weight-initialization/DL-029-weight-initialization.md#1-overview)
- [Xavier and He initialisation](../DL/02-training/DL-030-xavier-he-initialization/DL-030-xavier-he-initialization.md#4-xavier-glorot-initialisation)
- [Batch normalisation](../DL/02-training/DL-031-batch-normalization/DL-031-batch-normalization.md#4-how-batch-normalisation-works-during-training)
- [Covariate shift](../DL/02-training/DL-031-batch-normalization/DL-031-batch-normalization.md#32-covariate-shift)
- [Optimizers in deep learning](../DL/03-optimizers/DL-032-optimizers-in-deep-learning/DL-032-optimizers-in-deep-learning.md#8-sources)
- [Local minima and saddle points](../DL/03-optimizers/DL-032-optimizers-in-deep-learning/DL-032-optimizers-in-deep-learning.md#54-local-minima)
- [SGD with momentum](../DL/03-optimizers/DL-034-sgd-with-momentum/DL-034-sgd-with-momentum.md#9-momentum-on-real-data-mnist)
- [Nesterov accelerated gradient (NAG)](../DL/03-optimizers/DL-035-nesterov-accelerated-gradient/DL-035-nesterov-accelerated-gradient.md#1-overview)
- [AdaGrad](../DL/03-optimizers/DL-036-adagrad/DL-036-adagrad.md#3-when-adagrad-helps)
- [RMSProp](../DL/03-optimizers/DL-037-rmsprop/DL-037-rmsprop.md#51-adagrad-against-rmsprop-on-mnist)
- [Adam](../DL/03-optimizers/DL-038-adam/DL-038-adam.md#6-adam-on-the-students-data)
- [Convolutional neural network (CNN)](../DL/04-cnn/DL-040-cnn-intuition/DL-040-cnn-intuition.md#1-overview)
- [Convolution operation and feature maps](../DL/04-cnn/DL-042-convolution-operation/DL-042-convolution-operation.md#6-the-convolution-operation)
- [Padding and strides](../DL/04-cnn/DL-043-padding-and-strides/DL-043-padding-and-strides.md#4-zero-padding)
- [Pooling](../DL/04-cnn/DL-044-pooling/DL-044-pooling.md#3-why-pooling-is-needed)
- [CNN architecture (LeNet-5)](../DL/04-cnn/DL-045-lenet-5/DL-045-lenet-5.md#3-the-general-cnn-architecture)
- [Backpropagation in a CNN](../DL/04-cnn/DL-047-backpropagation-in-cnn/DL-047-backpropagation-in-cnn.md#1-overview)
- [Image classification with a CNN (cats vs dogs)](../DL/04-cnn/DL-049-cat-vs-dog-cnn/DL-049-cat-vs-dog-cnn.md#3-the-dataset)
- [Pretrained models and ImageNet](../DL/04-cnn/DL-051-pretrained-models/DL-051-pretrained-models.md#4-imagenet-the-dataset-behind-the-models)
- [Transfer learning (feature extraction and fine-tuning)](../DL/04-cnn/DL-053-transfer-learning/DL-053-transfer-learning.md#3-why-transfer-learning)
- [Keras functional API](../DL/04-cnn/DL-054-keras-functional-api/DL-054-keras-functional-api.md#1-overview)
- [Skip connections](../DL/04-cnn/DL-054-keras-functional-api/DL-054-keras-functional-api.md#43-a-skip-connection)
- [Recurrent neural network (RNN)](../DL/05-rnn/DL-055-why-rnn/DL-055-why-rnn.md#1-overview)
- [Parameter sharing across time steps](../DL/05-rnn/DL-059-backpropagation-through-time/DL-059-backpropagation-through-time.md#1-overview)
- [Types of RNN (many-to-one, one-to-many, many-to-many)](../DL/05-rnn/DL-058-types-of-rnn/DL-058-types-of-rnn.md#6-one-to-one)
- [Sequence-to-sequence (encoder-decoder)](../DL/06-transformers/DL-068-encoder-decoder/DL-068-encoder-decoder.md#3-why-sequence-to-sequence-is-hard)
- [Backpropagation through time (BPTT)](../DL/05-rnn/DL-059-backpropagation-through-time/DL-059-backpropagation-through-time.md#1-overview)
- [Long-term dependency problem](../DL/05-rnn/DL-060-problems-with-rnn/DL-060-problems-with-rnn.md#3-the-long-term-dependency-problem)
- [LSTM (long short-term memory)](../DL/05-rnn/DL-061-lstm/DL-061-lstm.md#7-two-differences-between-an-rnn-and-an-lstm)
- [LSTM gates (forget, input, output) and cell state](../DL/05-rnn/DL-062-lstm-architecture/DL-062-lstm-architecture.md#41-cell-state-and-hidden-state-are-vectors-of-the-same-length)
- [Next-word prediction with an LSTM](../DL/05-rnn/DL-063-lstm-next-word-prediction/DL-063-lstm-next-word-prediction.md#1-overview)
- [GRU (gated recurrent unit)](../DL/05-rnn/DL-064-gru/DL-064-gru.md#1-overview)
- [Deep (stacked) RNNs](../DL/05-rnn/DL-065-deep-rnns/DL-065-deep-rnns.md#4-the-architecture-of-a-deep-rnn)
- [Bidirectional RNNs](../DL/05-rnn/DL-066-bidirectional-rnn/DL-066-bidirectional-rnn.md#4-how-a-bidirectional-rnn-works)
- [Large language models (LLMs)](../DL/06-transformers/DL-067-history-of-llms/DL-067-history-of-llms.md#8-stage-5-large-language-models-2018-onward)
- [Teacher forcing](../DL/06-transformers/DL-068-encoder-decoder/DL-068-encoder-decoder.md#52-the-forward-pass-and-teacher-forcing)
- [Attention mechanism](../DL/06-transformers/DL-069-attention-mechanism/DL-069-attention-mechanism.md#11-sources)
- [Bahdanau (additive) attention](../DL/06-transformers/DL-070-bahdanau-vs-luong-attention/DL-070-bahdanau-vs-luong-attention.md#4-bahdanau-attention)
- [Luong (multiplicative) attention](../DL/06-transformers/DL-070-bahdanau-vs-luong-attention/DL-070-bahdanau-vs-luong-attention.md#5-luong-attention)
- [Transformer](../DL/06-transformers/DL-081-transformer-encoder/DL-081-transformer-encoder.md#1-overview)
- [Self-attention (query, key, value)](../DL/06-transformers/DL-073-what-is-self-attention/DL-073-what-is-self-attention.md#6-self-attention-static-in-contextual-out)
- [Scaled dot-product attention](../DL/06-transformers/DL-075-scaled-dot-product-attention/DL-075-scaled-dot-product-attention.md#1-overview)
- [Multi-head attention](../DL/06-transformers/DL-078-multi-head-attention/DL-078-multi-head-attention.md#6-multi-head-attention-in-the-transformer)
- [Positional encoding](../DL/06-transformers/DL-079-positional-encoding/DL-079-positional-encoding.md#1-overview)
- [Layer normalisation](../DL/06-transformers/DL-080-layer-normalization/DL-080-layer-normalization.md#6-layer-normalisation)
- [Residual connections and add & norm](../DL/06-transformers/DL-081-transformer-encoder/DL-081-transformer-encoder.md#71-why-residual-connections)
- [Transformer encoder](../DL/06-transformers/DL-081-transformer-encoder/DL-081-transformer-encoder.md#10-key-terms)
- [Masked self-attention](../DL/06-transformers/DL-082-masked-self-attention/DL-082-masked-self-attention.md#1-overview)
- [Cross-attention](../DL/06-transformers/DL-083-cross-attention/DL-083-cross-attention.md#7-what-a-trained-models-cross-attention-looks-like)
- [Transformer decoder](../DL/06-transformers/DL-084-transformer-decoder/DL-084-transformer-decoder.md#11-sources)
- [Transformer inference (autoregressive decoding, KV cache, beam search)](../DL/06-transformers/DL-085-transformer-inference/DL-085-transformer-inference.md#9-sources)
- [The transformer end to end (capstone)](../DL/06-transformers/DL-086-transformer-end-to-end/DL-086-transformer-end-to-end.md#1-overview)
- [Label smoothing](../DL/06-transformers/DL-086-transformer-end-to-end/DL-086-transformer-end-to-end.md#74-regularisation-residual-dropout-and-label-smoothing)
- [Decoder-only GPT](../DL/06-transformers/DL-087-decoder-only-gpt/DL-087-decoder-only-gpt.md#1-overview)
- [GELU activation](../DL/06-transformers/DL-087-decoder-only-gpt/DL-087-decoder-only-gpt.md#1-overview)
- [Unembedding, logits, temperature and sampling](../DL/06-transformers/DL-088-unembedding-and-sampling/DL-088-unembedding-and-sampling.md#3-the-unembedding-one-dot-product-per-token)
- [MLP blocks as fact storage](../DL/06-transformers/DL-089-mlp-stores-facts/DL-089-mlp-stores-facts.md#1-overview)
- [Superposition and nearly perpendicular directions](../DL/06-transformers/DL-090-superposition/DL-090-superposition.md#8-the-superposition-hypothesis-and-a-toy-model)

### 2.10 Step 9: Evaluate

- [Overfitting](../ML/01-foundations/ML-007-challenges-in-ml/ML-007-challenges-in-ml.md#7-overfitting-and-underfitting)
- [Underfitting](../ML/01-foundations/ML-007-challenges-in-ml/ML-007-challenges-in-ml.md#7-overfitting-and-underfitting)
- [Accuracy](../ML/07-classification/ML-075-accuracy-confusion-matrix/ML-075-accuracy-confusion-matrix.md#2-accuracy)
- [Cross-validation](../ML/03-feature-engineering/ML-028-pipelines/ML-028-pipelines.md#8-cross-validation-with-a-pipeline)
- [Regression metrics](../ML/06-regression/ML-051-regression-metrics/ML-051-regression-metrics.md#1-overview)
- [Bias-variance trade-off](../ML/06-regression/ML-061-bias-variance/ML-061-bias-variance.md#1-overview)
- [Confusion matrix](../ML/07-classification/ML-075-accuracy-confusion-matrix/ML-075-accuracy-confusion-matrix.md#4-the-confusion-matrix)
- [Precision, recall and F1](../ML/07-classification/ML-076-precision-recall-f1/ML-076-precision-recall-f1.md#2-precision)
- [ROC curve and AUC](../ML/07-classification/ML-077-roc-auc/ML-077-roc-auc.md#4-the-roc-curve)
- [Decision surface and boundary](../ML/07-classification/ML-085-knn/ML-085-knn.md#5-decision-surfaces)
- [OOB score](../ML/08-trees-and-ensembles/ML-107-oob-score/ML-107-oob-score.md#3-how-the-oob-score-is-computed)
- [Training curves (History)](../DL/01-basics/DL-011-customer-churn-ann/DL-011-customer-churn-ann.md#8-training-curves)
- [Visualising what a CNN learns](../DL/04-cnn/DL-052-visualizing-cnn/DL-052-visualizing-cnn.md#1-overview)
- [Logit lens](../DL/06-transformers/DL-088-unembedding-and-sampling/DL-088-unembedding-and-sampling.md#7-the-logit-lens-watching-the-guess-form)

### 2.11 Step 10: Tune

- [Hyperparameter tuning](../ML/01-foundations/ML-009-mldlc/ML-009-mldlc.md#83-model-selection-and-hyperparameter-tuning)
- [Grid and random search](../ML/04-missing-data-and-outliers/ML-037-missing-indicator-random-sample/ML-037-missing-indicator-random-sample.md#7-choosing-the-imputer-automatically-with-grid-search)
- [Learning rate](../ML/06-regression/ML-056-gradient-descent/ML-056-gradient-descent.md#5-the-learning-rate)
- [Elbow method and WCSS](../ML/09-clustering-and-more/ML-122-kmeans-intuition/ML-122-kmeans-intuition.md#5-choosing-k-the-elbow-method)
- [Bayesian optimisation](../ML/09-clustering-and-more/ML-128-optuna/ML-128-optuna.md#1-overview)
- [Optuna](../ML/09-clustering-and-more/ML-128-optuna/ML-128-optuna.md#4-optunas-vocabulary)
- [Improving a neural network](../DL/02-training/DL-021-improving-a-neural-network/DL-021-improving-a-neural-network.md#1-overview)
- [Early stopping](../DL/02-training/DL-022-early-stopping/DL-022-early-stopping.md#4-early-stopping-in-keras)
- [Keras Tuner](../DL/03-optimizers/DL-039-keras-tuner/DL-039-keras-tuner.md#5-the-keras-tuner-workflow-choosing-the-optimizer)
- [Learning-rate warm-up schedule](../DL/06-transformers/DL-086-transformer-end-to-end/DL-086-transformer-end-to-end.md#1-overview)

### 2.12 Step 11: Deploy

- [Deployment](../ML/01-foundations/ML-004-batch-learning/ML-004-batch-learning.md#2-development-and-production)
- [Software integration](../ML/01-foundations/ML-007-challenges-in-ml/ML-007-challenges-in-ml.md#8-software-integration)
- [Saving models with pickle](../ML/01-foundations/ML-009-mldlc/ML-009-mldlc.md#1-overview)

### 2.13 Step 12: Test

- [Beta and A/B testing](../ML/01-foundations/ML-009-mldlc/ML-009-mldlc.md#101-beta-testing)

### 2.14 Step 13: Monitor and maintain

- [Model drift](../ML/01-foundations/ML-004-batch-learning/ML-004-batch-learning.md#41-models-go-stale)
- [Retraining](../ML/01-foundations/ML-004-batch-learning/ML-004-batch-learning.md#42-retraining-on-a-schedule)
- [MLOps and cost](../ML/01-foundations/ML-007-challenges-in-ml/ML-007-challenges-in-ml.md#10-cost)

## 3. The Concept map

> **Key point:** Concepts are joined by five kinds of Link. Following the Links shows why each idea exists and what it is for.

Every **Link** (G-2166) has one of five types:

- **needs**: must be understood first (logistic regression *needs* gradient descent);
- **is a kind of**: a special case (Ridge *is a kind of* regularisation);
- **fixes**: solves a problem (regularisation *fixes* overfitting);
- **compared with**: often confused or contrasted (bagging *compared with* boosting);
- **used in**: a tool used inside something else (feature scaling *used in* KNN).

The full map has 335 Concepts, too many for one page, so each topic has its own mind map (Figures 2 to 19). Each map tells the topic's story from left to right and shows only its key Concepts and links; the grey number in each box is the Note that teaches it, and dashed boxes lead to other maps. To see every Concept and every link at once, open `course_map/concept_map_3d.html` in a browser: a 3D network you can rotate and zoom, with one colour per area (rebuilt by `python course_map/map_3d.py`). The interactive app (`python course_map/app.py`) lists each Concept's links with the Notes that teach them.

![Concept map: Foundations and framing](images/concept_map_foundations.png){width=100%}

![Concept map: Getting, understanding and cleaning data](images/concept_map_data.png){width=100%}

![Concept map: Features, dimensions and splitting](images/concept_map_features.png){width=100%}

![Concept map: Models: regression, classification and gradient descent](images/concept_map_models_regression.png){width=100%}

![Concept map: Models: trees, ensembles and clustering](images/concept_map_models_trees.png){width=100%}

![Concept map: Evaluating, tuning and production](images/concept_map_production.png){width=100%}

![Concept map: Descriptive statistics and distributions](images/concept_map_descriptive.png){width=100%}

![Concept map: Probability](images/concept_map_probability.png){width=100%}

![Concept map: Sampling, inference and hypothesis tests](images/concept_map_inference.png){width=100%}

![Concept map: Linear algebra](images/concept_map_linear_algebra.png){width=100%}

![Concept map: Calculus and optimisation](images/concept_map_calculus.png){width=100%}

![Concept map: Likelihood, MLE and mixture models](images/concept_map_likelihood.png){width=100%}

![Concept map: Deep learning: perceptron to backpropagation](images/concept_map_dl_basics.png){width=100%}

![Concept map: Deep learning: training better networks](images/concept_map_dl_training.png){width=100%}

![Concept map: Deep learning: optimizers](images/concept_map_dl_optimizers.png){width=100%}

![Concept map: Deep learning: convolutional networks](images/concept_map_dl_cnn.png){width=100%}

![Concept map: Deep learning: recurrent networks](images/concept_map_dl_rnn.png){width=100%}

![Concept map: Deep learning: LLMs, attention and transformers](images/concept_map_dl_transformers.png){width=100%}

## 4. The Learning path

> **Key point:** Before each Note, read the Notes it builds on.

A Note is easiest to read when the ideas it uses are already familiar. The Notes that teach those ideas are its **prerequisites**: the Notes to read first. Each prerequisite has prerequisites of its own, so the reading order grows backwards from the Note we want, one round at a time.

![The reading order for the perceptron Note (DL-004), grown backwards. Round 1 adds the three Notes it builds on; round 2 adds the Notes that those build on. Arrows point from a prerequisite to the Note that needs it.](images/learning_path.gif)

Figure 20 builds the reading order for the perceptron Note (Note DL-004) step by step:

1. **Goal.** We want to read Note DL-004.
2. **Round 1.** Its *Where this fits* box lists Note ML-069, Note MA-050 and Note MA-051 under "Builds on".
3. **Round 2.** Each of those has its own box: Note ML-069 builds on Note ML-072, Note MA-067; Note MA-050 builds on Note MA-048; Note MA-051 builds on nothing new.
4. **Reading.** Read the picture from left to right: green Notes first, then blue, then the goal. Every arrow points from a Note to a Note that needs it.

Every Note starts with this list in its *Where this fits* box, so there is no separate table here: open the Note you want and follow its "Builds on" links. The list comes from the **needs**, **is a kind of**, **fixes** and **used in** Links of section 3.

## 5. The Algorithm chooser

> **Key point:** Two questions narrow the choice: do we have labelled outputs, and are they numbers or categories?

![The Algorithm chooser (draft)](images/algorithm_chooser.png)

Figure 21 is a starting point, not a rule: in practice we try several suitable algorithms and compare them on a test set. It is a draft until the algorithm Notes are written.

## 6. Sources

**Built from**
- CampusX, "100 Days of Machine Learning", YouTube playlist (134 videos), https://www.youtube.com/playlist?list=PLKnIA16_Rmvbr7zKYQuBfsVkjoLcJgxHH
- CampusX, "100 Days of Deep Learning", YouTube playlist (84 videos), https://www.youtube.com/playlist?list=PLKnIA16_RmvYuZauWaPlRTC54KxSNLtNn
- CampusX, "Maths for Machine Learning", YouTube playlist (23 sessions), https://www.youtube.com/playlist?list=PLKnIA16_RmvbYFaaeLY28cWeqV-3vADST
- Every Note listed in the Learning path: each Note's own Sources name the video, book or paper it was built from.

**Other references**
- The Concept map data: `course_map/concepts.yaml` in this repository.

## 7. Key terms

| Term | Meaning |
|---|---|
| Course map (G-2160) | The overview that ties all Notes together, in four views |
| Pipeline map (G-2161) | Where each Concept sits among the 14 steps of an ML project |
| Concept map (G-2162) | How Concepts are connected by Links |
| Learning path (G-2163) | Which Notes to read before which |
| Algorithm chooser (G-2164) | A flowchart from a problem's properties to suitable algorithms |
| Concept (G-2165) | One idea on the Course map |
| Link (G-2166) | A labelled connection between two Concepts |
