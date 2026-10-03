# Glossary

Every ML term in the notes, in plain English, with the Note that first explains it.

| Term | Meaning | First explained |
|---|---|---|
| .dt accessor | The pandas tool that applies date and time methods to every value of a datetime column. | [Video 34](34-date-and-time/note.md) |
| .str accessor | The pandas tool that applies a text method to every value of a column. | [Video 33](33-mixed-variables/note.md) |
| 5% rule of thumb | Apply CCA only to columns missing less than about 5% of their values. | [Video 35](35-complete-case-analysis/note.md) |
| 68-95-99.7 rule (empirical rule) | In a normal column, about 68.3%, 95.4% and 99.7% of values lie within 1, 2 and 3 standard deviations of the mean. | [Video 42](42-outliers-zscore/note.md) |
| @ (matrix multiplication) | Python's operator for multiplying matrices and vectors. | [Video 55](55-multiple-lr-code/note.md) |
| `add_indicator=True` | The `SimpleImputer` setting that imputes and appends missing indicators in one step. | [Video 38](38-missing-indicator-random-sample/note.md) |
| `base_score` | XGBoost's starting prediction; a probability for classification. | [Video 125](125-xgboost-classification/note.md) |
| `BayesianRidge` | A linear regression with built-in shrinkage of the weights; the default model of `IterativeImputer`. | [Video 40](40-iterative-imputer-mice/note.md) |
| `best_params_` | The best combination of settings found by `GridSearchCV`. | [Video 38](38-missing-indicator-random-sample/note.md) |
| `clip` | pandas method that moves every value below a lower bound up to it and every value above an upper bound down to it. | [Video 44](44-outliers-percentile/note.md) |
| `cv_results_` | The scores of every combination tried by `GridSearchCV`. | [Video 38](38-missing-indicator-random-sample/note.md) |
| `enable_iterative_imputer` | The import that switches on the experimental `IterativeImputer`. | [Video 40](40-iterative-imputer-mice/note.md) |
| `fill_value` | The value `SimpleImputer` uses with `strategy="constant"`. | [Video 36](36-imputing-numerical-data/note.md) |
| `fillna` | The pandas method that replaces every `NaN` with a given value. | [Video 36](36-imputing-numerical-data/note.md) |
| `find`, `find_all` | Return the first matching tag, or a list of all matching tags. | [Video 18](18-web-scraping/note.md) |
| `GridSearchCV` | The scikit-learn class that cross-validates every combination of settings in a grid and keeps the best. | [Video 29](29-pipelines/note.md) |
| `ignore_index` | Setting of `pd.concat` that renumbers the joined rows from 0. | [Video 17](17-fetching-data-from-api/note.md) |
| `IterativeImputer` | scikit-learn's class for MICE; still experimental. | [Video 40](40-iterative-imputer-mice/note.md) |
| `json_normalize` | pandas function that turns nested JSON into flat columns. | [Video 17](17-fetching-data-from-api/note.md) |
| `KNNImputer` | scikit-learn's class for KNN imputation. | [Video 39](39-knn-imputer/note.md) |
| `max_iter` | The largest number of iterations `IterativeImputer` runs; default 10. | [Video 40](40-iterative-imputer-mice/note.md) |
| `min_child_weight` | Smallest allowed sum of $p(1-p)$ (in regression: number of rows) in a leaf; default 1. | [Video 125](125-xgboost-classification/note.md) |
| `MissingIndicator` | The scikit-learn class that builds missing indicator columns; `features_` lists the columns with gaps. | [Video 38](38-missing-indicator-random-sample/note.md) |
| `n_neighbors` (k) | The number of nearest rows the KNN imputer averages; default 5. | [Video 39](39-knn-imputer/note.md) |
| `np.where` | NumPy function that picks one value where a condition is true and another where it is false. | [Video 42](42-outliers-zscore/note.md) |
| `pd.concat` | pandas function that joins several DataFrames into one. | [Video 17](17-fetching-data-from-api/note.md) |
| `quantile` | pandas method that returns a percentile, given as a fraction (0.25 for the 25th). | [Video 43](43-outliers-iqr/note.md) |
| `random_state` | A seed that fixes a random draw, so the same code gives the same result. | [Video 38](38-missing-indicator-random-sample/note.md) |
| `read_json` | pandas function that reads JSON from a file or a URL into a DataFrame. | [Video 16](16-working-with-json-and-sql/note.md) |
| `read_sql_query` | pandas function that runs an SQL query and returns a DataFrame. | [Video 16](16-working-with-json-and-sql/note.md) |
| `sample(n)` | The pandas method that draws `n` values at random from a Series or DataFrame. | [Video 38](38-missing-indicator-random-sample/note.md) |
| `sample_posterior` | Draw each fill at random from the model's spread, giving several plausible filled tables. | [Video 40](40-iterative-imputer-mice/note.md) |
| `statistics_` | The fill values a fitted `SimpleImputer` has learned, one per column. | [Video 36](36-imputing-numerical-data/note.md) |
| `step__param` name | The full name of a setting inside a pipeline: step names and the parameter joined by `__`. | [Video 29](29-pipelines/note.md) |
| `strategy="constant"` | The `SimpleImputer` setting that fills every gap with `fill_value`. | [Video 37](37-missing-categorical-data/note.md) |
| `strategy="most_frequent"` | The `SimpleImputer` setting for mode imputation. | [Video 37](37-missing-categorical-data/note.md) |
| `strategy` | The `SimpleImputer` parameter choosing the fill rule: mean, median, most_frequent or constant. | [Video 36](36-imputing-numerical-data/note.md) |
| `tol` | The size of change below which `IterativeImputer` stops early; default 0.001. | [Video 40](40-iterative-imputer-mice/note.md) |
| A/B testing | Comparing an old and a new version on two random groups of users. | [Video 9](09-mldlc/note.md) |
| Absolute value | A number's size without its sign. | [Video 25](25-normalization/note.md) |
| absolute_error | A criterion that splits by mean absolute error; leaves predict the median. | [Video 99](99-regression-trees/note.md) |
| Accuracy | The fraction of predictions that are correct. | [Video 13](13-toy-project/note.md) |
| AdaBoost (Adaptive Boosting) | A boosting algorithm that trains weak learners in sequence on reweighted data and combines them by an alpha-weighted vote. | [Video 115](115-adaboost-intuition/note.md) |
| Addition rule | For mutually exclusive events, $P(A \cup B) = P(A) + P(B)$. | [Video 84](84-mutually-exclusive-events/note.md) |
| Additive modelling | Building a complex function as a sum of simple functions, each capturing part of what the others missed. | [Video 121](121-gradient-boosting-regression-maths/note.md) |
| Adjusted Rand score | A number that is 1.0 when two labelings group the points identically, whatever the label numbers. | [Video 130](130-kmeans-from-scratch/note.md) |
| Adjusted R² | R² with a penalty for the number of input columns. | [Video 52](52-regression-metrics/note.md) |
| Agent | The learner in reinforcement learning. | [Video 3](03-types-of-ml/note.md) |
| Agglomerative clustering | Bottom-up hierarchical clustering: start with one cluster per point and merge the closest pair repeatedly. | [Video 131](131-hierarchical-clustering/note.md) |
| AgglomerativeClustering | scikit-learn's class for agglomerative clustering. | [Video 131](131-hierarchical-clustering/note.md) |
| Aggregation | Combining the base models' predictions into one: mode for classes, mean for numbers. | [Video 105](105-bagging-intuition/note.md) |
| AGI (artificial general intelligence) | A machine with all the abilities of human intelligence. Does not exist yet. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Alert | A warning in the report about a column that may need attention. | [Video 22](22-pandas-profiling/note.md) |
| Alpha (model weight) | A base model's say in AdaBoost's final vote; larger when it made fewer mistakes. | [Video 115](115-adaboost-intuition/note.md) |
| Anaconda Navigator | Anaconda's point-and-click window for environments and packages. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| Anaconda | The best-known data science distribution, with Navigator and Spyder. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| Anomaly detection | Finding rows that do not fit the pattern of the rest. | [Video 3](03-types-of-ml/note.md) |
| API (Application Programming Interface) | A service that returns data when our code asks for it; a website's API hands out its data on request. | [Video 7](07-challenges-in-ml/note.md) |
| API key | A secret code that tells the API who is asking. | [Video 17](17-fetching-data-from-api/note.md) |
| API token | A secret file or key that lets a program use a website's API as us. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| Approximate tree learning (histogram-based training) | Finding a split by trying only the edges of bins the column has been cut into. | [Video 123](123-xgboost-intro/note.md) |
| Arbitrary value imputation | Filling every gap with one fixed value that never occurs, such as 99 or $-1$. | [Video 36](36-imputing-numerical-data/note.md) |
| arg max | The value of the variable that makes an expression largest. | [Video 88](88-naive-bayes-maths/note.md) |
| Arg min | The value of a variable that makes an expression smallest, written $\arg\min$. | [Video 121](121-gradient-boosting-regression-maths/note.md) |
| Array | The programming name for a tensor (as in NumPy). | [Video 11](11-tensors/note.md) |
| Artificial Intelligence (AI) | The field of building machines that show intelligence. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Association rule learning | Finding items that tend to occur together. | [Video 3](03-types-of-ml/note.md) |
| Assumption (of a model) | A condition the data must meet for the model's results to be reliable. | [Video 56](56-linear-regression-assumptions/note.md) |
| Atomic value | A single piece of information in a cell, not several combined. | [Video 45](45-feature-construction-splitting/note.md) |
| Attribute | A `name="value"` setting inside an opening tag. | [Video 18](18-web-scraping/note.md) |
| AUC | The area under the ROC curve; a single score from 0.5 (random) to 1 (perfect). | [Video 78](78-roc-auc/note.md) |
| Autocorrelation | Each residual is related to the one before it in row order. | [Video 56](56-linear-regression-assumptions/note.md) |
| Average linkage | Cluster distance = mean of all distances between the two clusters' points. | [Video 131](131-hierarchical-clustering/note.md) |
| Average record size | The memory one row takes, on average. | [Video 22](22-pandas-profiling/note.md) |
| Axis | One direction along which a tensor's items are arranged. | [Video 11](11-tensors/note.md) |
| Axis-parallel split | A cut that tests one column, so it is a line, plane or hyperplane parallel to the other axes. | [Video 97](97-decision-trees-intuition/note.md) |
| B2B | Business to business: a product that helps a company run its business. | [Video 8](08-applications-of-ml/note.md) |
| B2C | Business to customer: a product sold to ordinary users. | [Video 8](08-applications-of-ml/note.md) |
| Backward elimination | Feature selection that starts with all columns and removes the worst at a time. | [Video 23](23-what-is-feature-engineering/note.md) |
| Bagging (bootstrap aggregation) | Averaging many models trained on different samples of the data to reduce variance. | [Video 101](101-ensemble-learning/note.md) |
| Bagging regressor | A bagging ensemble of regressors that predicts the mean of their predictions. | [Video 107](107-bagging-regressor/note.md) |
| Bagging | Averaging many models trained on different samples of the data to reduce variance. | [Video 62](62-bias-variance/note.md) |
| BaggingClassifier | scikit-learn class for bagging, pasting, random subspaces and random patches in classification. | [Video 106](106-bagging-classifier/note.md) |
| BaggingRegressor | scikit-learn class for bagging, pasting, random subspaces and random patches in regression. | [Video 107](107-bagging-regressor/note.md) |
| Bar plot | One bar per category, its height the mean of a numerical column. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| base environment | The environment the installer creates, holding conda itself. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| Base model | One of the models inside an ensemble. | [Video 101](101-ensemble-learning/note.md) |
| Base prediction ($F_0$) | The first model of gradient boosting; for regression, the mean of the target. | [Video 120](120-gradient-boosting-intuition/note.md) |
| Batch (mini-batch) | A small group of training rows used for one update. | [Video 60](60-mini-batch-gradient-descent/note.md) |
| Batch gradient descent | Gradient descent that uses all training rows for every update. | [Video 58](58-batch-gradient-descent/note.md) |
| Batch learning | Training on the whole dataset at once, offline, then deploying. | [Video 4](04-batch-learning/note.md) |
| Batch size | The number of rows in each batch; a hyperparameter. | [Video 60](60-mini-batch-gradient-descent/note.md) |
| Bayes' theorem | $P(A \mid B) = P(B \mid A) P(A) / P(B)$: the rule that reverses a conditional probability. | [Video 85](85-bayes-theorem/note.md) |
| Bayesian statistics | The branch of statistics that treats probabilities as beliefs updated by Bayes' theorem. | [Video 85](85-bayes-theorem/note.md) |
| BeautifulSoup | Python library that parses HTML into a searchable tree. | [Video 18](18-web-scraping/note.md) |
| Bell curve | The curve of a normal distribution. | [Video 42](42-outliers-zscore/note.md) |
| BernoulliNB | Naive Bayes for binary (yes/no) inputs. | [Video 90](90-gaussian-naive-bayes/note.md) |
| Best-fit line | The line with the smallest total error over all the training points. | [Video 50](50-simple-linear-regression/note.md) |
| best_score_ | The best mean cross-validated score found by a search. | [Video 112](112-random-forest-tuning/note.md) |
| Beta testing | Releasing a new version to a small group of trusted users first. | [Video 9](09-mldlc/note.md) |
| Bias | Error from a model being too simple to capture the true relationship. | [Video 62](62-bias-variance/note.md) |
| Bias-variance trade-off | Lowering bias by adding complexity tends to raise variance, and the reverse. | [Video 62](62-bias-variance/note.md) |
| Biased model | A model pushed towards wrong answers, e.g. by bad data. | [Video 5](05-online-learning/note.md) |
| Big picture | The end product and how it will be used, which decides the type of ML problem. | [Video 14](14-framing-ml-problem/note.md) |
| Bimodal | A distribution with two peaks. | [Video 31](31-power-transformer/note.md) |
| Bin edge | A boundary between two neighbouring bins. | [Video 32](32-binning-binarization/note.md) |
| Bin | One of the equal ranges a histogram splits the data into. | [Video 20](20-univariate-analysis/note.md) |
| bin_edges_ | The fitted `KBinsDiscretizer` attribute holding the learned edges. | [Video 32](32-binning-binarization/note.md) |
| Binarization | Turning a continuous column into 0 or 1 by comparing it with one threshold. | [Video 32](32-binning-binarization/note.md) |
| Binarizer | scikit-learn's class for binarization, with parameters `threshold` and `copy`. | [Video 32](32-binning-binarization/note.md) |
| Binary cross entropy (log loss) | The average cross entropy for two classes, the loss function of logistic regression. | [Video 73](73-log-loss/note.md) |
| Binary file | A file that is not plain text, such as a saved model. | [Video 9](09-mldlc/note.md) |
| Binning | Grouping a numerical column into ranges that act as categories. | [Video 23](23-what-is-feature-engineering/note.md) |
| Binomial distribution | The distribution of the number of successes in $n$ independent trials with the same success probability. | [Video 102](102-voting-ensemble/note.md) |
| Bivariate analysis | Studying two variables together. | [Video 20](20-univariate-analysis/note.md) |
| Black box model | A model that gives predictions without showing how each input contributed. | [Video 91](91-knn/note.md) |
| Blending | Stacking in which the meta-model is trained on the base models' predictions for a hold-out validation set. | [Video 127](127-stacking-blending/note.md) |
| BMI | Body mass index: weight (kg) divided by height (m) squared. | [Video 7](07-challenges-in-ml/note.md) |
| Boolean indexing | Selecting rows with an array of True/False values, e.g. `X[y_means == 0]`. | [Video 129](129-kmeans-code/note.md) |
| Boosting | Combining many simple models in sequence to reduce bias. | [Video 62](62-bias-variance/note.md) |
| Bootstrap sample | A sample of the same size drawn from the data with replacement. | [Video 66](66-ridge-key-points/note.md) |
| bootstrap | BaggingClassifier setting: draw rows with replacement (True, bagging) or without (False, pasting). | [Video 106](106-bagging-classifier/note.md) |
| bootstrap_features | BaggingClassifier setting: draw columns with replacement or without. | [Video 106](106-bagging-classifier/note.md) |
| Bootstrapping | Drawing random samples of the data to train each base model. | [Video 105](105-bagging-intuition/note.md) |
| Border point | A point with fewer than MinPts points within eps, but with a core point among them. | [Video 132](132-dbscan/note.md) |
| Boston housing data | 506 Boston districts, 13 inputs and the median home value; removed from scikit-learn in version 1.2. | [Video 99](99-regression-trees/note.md) |
| Bot | A program that visits websites automatically. | [Video 18](18-web-scraping/note.md) |
| Box plot | A graph of the five-number summary, with outliers drawn as dots. | [Video 20](20-univariate-analysis/note.md) |
| Box-Cox transform | $(x^\lambda - 1)/\lambda$, or $\ln x$ when $\lambda = 0$; works only on values above 0. | [Video 31](31-power-transformer/note.md) |
| Branch (subtree) | A node together with everything below it. | [Video 97](97-decision-trees-intuition/note.md) |
| Buying behaviour | The pattern of what a customer buys. | [Video 8](08-applications-of-ml/note.md) |
| C (SVM) | The weight on the classification error; a large C means few mistakes and a narrow margin, a small C a wide margin. | [Video 94](94-svm-soft-margin/note.md) |
| C | The inverse of the regularisation strength in LogisticRegression; smaller C means stronger regularisation. | [Video 81](81-logistic-hyperparameters/note.md) |
| Cache memory | A small, fast memory inside the processor that holds data used again and again. | [Video 123](123-xgboost-intro/note.md) |
| CalibratedClassifierCV | scikit-learn wrapper that gives a classifier, such as an SVM, calibrated probabilities. | [Video 103](103-voting-classifier/note.md) |
| Capping | Replacing every value beyond a limit with the limit itself. | [Video 41](41-what-are-outliers/note.md) |
| cars.csv | dtreeviz's sample data: 392 cars with MPG, weight, engine size and cylinders. | [Video 100](100-dtreeviz/note.md) |
| CART | Classification and regression trees: the tree algorithm used for both kinds of problem. | [Video 97](97-decision-trees-intuition/note.md) |
| CatBoost | Yandex's gradient boosting library, with built-in handling of categorical columns. | [Video 123](123-xgboost-intro/note.md) |
| Categorical cross entropy | The loss of softmax regression: the average of −log(probability of the true class). | [Video 79](79-softmax-regression/note.md) |
| Categorical data (categorical column) | Data made of categories: labels rather than numbers. | [Video 3](03-types-of-ml/note.md) |
| CategoricalNB | scikit-learn's Naive Bayes for categorical inputs. | [Video 89](89-naive-bayes-code/note.md) |
| categories_ | The attribute holding the categories `OrdinalEncoder` learned, in order. | [Video 26](26-ordinal-label-encoding/note.md) |
| Category share | The rows in one category divided by the rows that have a value. | [Video 37](37-missing-categorical-data/note.md) |
| Category | One of the fixed groups of a categorical column. | [Video 20](20-univariate-analysis/note.md) |
| ccp_alpha | Cost-complexity pruning strength: the penalty per leaf when a grown tree is pruned back. | [Video 111](111-random-forest-hyperparameters/note.md) |
| Cell | One block of a notebook, holding either code or Markdown. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| Centred data | Data whose mean is 0. | [Video 25](25-normalization/note.md) |
| Centroid initialization | Picking the first k centroids, here at random from the data. | [Video 128](128-kmeans-intuition/note.md) |
| Centroid | The centre of one group in k-means. | [Video 32](32-binning-binarization/note.md) |
| Centroid-based clustering | Clustering built around centroids, such as k-means. | [Video 132](132-dbscan/note.md) |
| Chain rule of probability | Writing a joint probability as a product of conditional probabilities, one variable at a time. | [Video 88](88-naive-bayes-maths/note.md) |
| Chain rule | To differentiate a function of a function, multiply the outer derivative by the inner derivative. | [Video 74](74-sigmoid-derivative/note.md) |
| Chained assignment | Selecting part of a DataFrame and then changing that selection in a second step; does nothing in pandas 3. | [Video 45](45-feature-construction-splitting/note.md) |
| Chained equations | One prediction model per column, each using the latest fills of the others. | [Video 40](40-iterative-imputer-mice/note.md) |
| Channel | One colour layer of an image (red, green or blue). | [Video 11](11-tensors/note.md) |
| Chi-squared test (chi2) | A test scoring how strongly a column is linked to the target; needs values of 0 or more. | [Video 29](29-pipelines/note.md) |
| Cholesky solver | A scikit-learn Ridge solver that solves the closed-form equation directly. | [Video 64](64-ridge-regression-maths/note.md) |
| Chunk | A piece of a file, read as a small DataFrame. | [Video 15](15-working-with-csv/note.md) |
| Churn rate | The percentage of customers who leave during a given period. | [Video 14](14-framing-ml-problem/note.md) |
| Churn | Customers leaving a platform or service. | [Video 14](14-framing-ml-problem/note.md) |
| Class prior | The share of training rows in a class. | [Video 87](87-naive-bayes-intuition/note.md) |
| Class | An attribute that labels tags; used to select the right ones. | [Video 18](18-web-scraping/note.md) |
| class_sep | make_classification setting for how far apart the classes are. | [Video 71](71-perceptron-code/note.md) |
| class_weight | A setting that weights each class's mistakes in the loss; "balanced" helps rare classes. | [Video 81](81-logistic-hyperparameters/note.md) |
| classes_ | The attribute holding the classes `LabelEncoder` learned, in order. | [Video 26](26-ordinal-label-encoding/note.md) |
| Classification error (SVM) | The term $\sum \xi_i$ of the SVM loss: the total slack of all points. | [Video 94](94-svm-soft-margin/note.md) |
| Classification metric | A number that measures how well a classification model performs. | [Video 76](76-accuracy-confusion-matrix/note.md) |
| Classification | Supervised learning with a categorical output. | [Video 3](03-types-of-ml/note.md) |
| classification_report | scikit-learn function that prints precision, recall, F1 and support for every class. | [Video 77](77-precision-recall-f1/note.md) |
| Client, server | The program that asks, and the computer that answers. | [Video 17](17-fetching-data-from-api/note.md) |
| Closed-form solution | An answer given directly by a formula of ordinary operations. | [Video 51](51-linear-regression-maths/note.md) |
| Cluster | One group found by clustering. | [Video 3](03-types-of-ml/note.md) |
| cluster_centers_ | The coordinates of the final centroids of a fitted `KMeans`. | [Video 129](129-kmeans-code/note.md) |
| Clustering | Splitting data into groups of similar rows. | [Video 3](03-types-of-ml/note.md) |
| Clustermap | A heatmap with rows and columns reordered so similar ones sit together. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| coef_ | The fitted slope (one per input column) in scikit-learn. | [Video 50](50-simple-linear-regression/note.md) |
| Coefficient ($\beta_i$) | The weight of one input column: the change in the output per unit of that input, others fixed. | [Video 53](53-multiple-linear-regression/note.md) |
| Coefficient of variation (CV) | Standard deviation divided by mean: spread relative to the average. | [Video 22](22-pandas-profiling/note.md) |
| Coefficient path | How each coefficient changes as the regularisation strength grows. | [Video 66](66-ridge-key-points/note.md) |
| Coefficient vector ($\beta$) | All the coefficients of the model, $\beta_0$ to $\beta_m$, as one column. | [Video 54](54-multiple-lr-maths/note.md) |
| Column block | XGBoost's storage of the data one sorted column per block, so each core can work on one feature. | [Video 123](123-xgboost-intro/note.md) |
| Column sampling (feature sampling) | Giving each base model a random subset of the columns. | [Video 108](108-random-forest-intro/note.md) |
| Column transformer | A scikit-learn class that applies different transformations to different columns at once (covered two Notes later). | [Video 26](26-ordinal-label-encoding/note.md) |
| ColumnTransformer | The scikit-learn class (in `sklearn.compose`) that implements the column transformer. | [Video 28](28-column-transformer/note.md) |
| Combined sampling | Giving each base model random rows and random columns together. | [Video 108](108-random-forest-intro/note.md) |
| Complete case analysis (CCA) | Dropping every row that has a missing value in any chosen column; also called listwise deletion. | [Video 35](35-complete-case-analysis/note.md) |
| Complete case | A row with a value in every column used. | [Video 35](35-complete-case-analysis/note.md) |
| Complete linkage | Cluster distance = distance of the farthest pair of points. | [Video 131](131-hierarchical-clustering/note.md) |
| components_ | The eigenvectors of the fitted PCA, one per row. | [Video 49](49-pca-mnist/note.md) |
| Compression | Storing data in less space. | [Video 11](11-tensors/note.md) |
| conda | A package and environment manager for Python and other software. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| conda-forge | A free, community-run conda channel. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| Conditional independence | Independence that holds once a third variable (here the class) is known. | [Video 88](88-naive-bayes-maths/note.md) |
| Conditional probability | The probability of an event given that another event has happened: $P(A \mid B)$. | [Video 82](82-conditional-probability/note.md) |
| Condorcet's jury theorem | A majority of independent voters, each right with probability above 0.5, is right more often than any one voter, and more so as voters are added. | [Video 102](102-voting-ensemble/note.md) |
| Confidence interval | A range in which the true mean most likely lies. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Confusion matrix | A table counting predictions for every pair of actual and predicted class. | [Video 76](76-accuracy-confusion-matrix/note.md) |
| Connection object | The open link to a database (`conn`) that queries go through. | [Video 16](16-working-with-json-and-sql/note.md) |
| Connector | A library that lets Python talk to a database. | [Video 16](16-working-with-json-and-sql/note.md) |
| Constrained form | Writing regularisation as a hard limit on the size of the coefficients. | [Video 66](66-ridge-key-points/note.md) |
| Constrained optimisation | Maximising or minimising a function while keeping one or more constraints true. | [Video 93](93-svm-maths/note.md) |
| Constraint | A condition the solution must satisfy; in SVM, $y_i (w^T x_i + b) \geq 1$ for every training point. | [Video 93](93-svm-maths/note.md) |
| Constructor (`__init__`) | The method that runs when an object is created and stores its settings. | [Video 130](130-kmeans-from-scratch/note.md) |
| Container | A tag (often a `div`) that holds everything about one item, such as one company. | [Video 18](18-web-scraping/note.md) |
| Contour plot | A map of a surface seen from above, with lines joining points of equal height. | [Video 57](57-gradient-descent/note.md) |
| Converge | To settle at a minimum, with steps becoming negligible. | [Video 57](57-gradient-descent/note.md) |
| Convergence (k-means) | The point where the centroids stop moving between rounds, so the algorithm stops. | [Video 128](128-kmeans-intuition/note.md) |
| Convergence | The point where the fills hardly change between two iterations. | [Video 40](40-iterative-imputer-mice/note.md) |
| ConvergenceWarning | A warning that the solver stopped at max_iter before reaching the minimum. | [Video 81](81-logistic-hyperparameters/note.md) |
| Conversion rate | The share of people reached who become customers. | [Video 8](08-applications-of-ml/note.md) |
| Convex function | A function where a straight line between any two points of its curve never goes below the curve; it has a single minimum. | [Video 57](57-gradient-descent/note.md) |
| Coordinate descent | An optimisation method that updates one coefficient at a time; used by scikit-learn's Lasso. | [Video 68](68-lasso-sparsity/note.md) |
| Core point | A point with at least MinPts points within eps. | [Video 132](132-dbscan/note.md) |
| Correlation between base models | How alike two base models' predictions are; the less alike, the more an ensemble cuts variance. | [Video 110](110-bagging-vs-random-forest/note.md) |
| Correlation | How two columns move together, from -1 to +1. | [Video 19](19-understanding-your-data/note.md) |
| Count plot | A bar chart with one bar per category, as tall as its frequency. | [Video 20](20-univariate-analysis/note.md) |
| Covariance matrix | A square table of all variances (diagonal) and covariances (off-diagonal) of the columns. | [Video 48](48-pca-step-by-step/note.md) |
| Covariance | How two columns move together: positive if they rise together, negative if not. | [Video 48](48-pca-step-by-step/note.md) |
| Cover | XGBoost's name for the sum of $p(1-p)$ (in regression: the number of rows) in a node. | [Video 125](125-xgboost-classification/note.md) |
| Cramér's V | A measure of the link between two categorical columns, from 0 to 1. | [Video 22](22-pandas-profiling/note.md) |
| Credit scoring | Predicting whether a loan applicant will repay. | [Video 8](08-applications-of-ml/note.md) |
| criterion | The DecisionTreeClassifier hyperparameter choosing the impurity measure: "gini" (default), "entropy" or "log_loss". | [Video 97](97-decision-trees-intuition/note.md) |
| Cross entropy | The negative log-likelihood; smaller is better. | [Video 73](73-log-loss/note.md) |
| Cross-validated accuracy | Accuracy averaged over several train-test splits of the data, an estimate of performance on new data. | [Video 80](80-polynomial-logistic-regression/note.md) |
| Cross-validation | Testing a model by training and testing it several times on different parts of the training data. | [Video 29](29-pipelines/note.md) |
| Crosstab | A table counting the rows for every pair of categories of two columns. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| CSV file | A text file holding a table, with commas between values. | [Video 13](13-toy-project/note.md) |
| Cumulative explained variance | The share of the variance kept by the first k components together. | [Video 49](49-pca-mnist/note.md) |
| Cumulative sum | The running total of a list of numbers; it turns weights into ranges on the line from 0 to 1. | [Video 116](116-adaboost-step-by-step/note.md) |
| Curse of dimensionality | The problems that appear when data has too many dimensions: lower performance and more computation. | [Video 46](46-curse-of-dimensionality/note.md) |
| Custom binning | Binning with edges we choose from domain knowledge; also called domain-based binning. | [Video 32](32-binning-binarization/note.md) |
| Customer profile | A summary of what kind of buyer a customer is, built from their purchases. | [Video 8](08-applications-of-ml/note.md) |
| Customer segmentation | Grouping customers by their buying behaviour. | [Video 8](08-applications-of-ml/note.md) |
| Cut-offs | The two percentiles chosen as limits, such as 1 and 99 or 5 and 95. | [Video 44](44-outliers-percentile/note.md) |
| Cutting the dendrogram | Drawing a horizontal line through the dendrogram; the lines it crosses are the clusters. | [Video 131](131-hierarchical-clustering/note.md) |
| Dash | A Python library for building interactive web apps with Plotly charts. | [Video 81](81-logistic-hyperparameters/note.md) |
| Data analysis | Finding patterns and hidden information in data, mainly by plotting graphs. | [Video 1](01-what-is-ml/note.md) |
| Data cleaning | Fixing errors, gaps and inconsistencies in data. | [Video 7](07-challenges-in-ml/note.md) |
| Data engineer | The specialist who collects and organises data from company systems. | [Video 14](14-framing-ml-problem/note.md) |
| Data leakage | Information from the test set leaking into training. | [Video 13](13-toy-project/note.md) |
| Data mining | Using ML on data to extract patterns too hidden for graphs. | [Video 1](01-what-is-ml/note.md) |
| Data pipeline | A channel that carries data from one point to another. | [Video 17](17-fetching-data-from-api/note.md) |
| Data preprocessing | Changes made to the data before training, so an algorithm can use it. | [Video 9](09-mldlc/note.md) |
| Data type (dtype) | The kind of values a column holds, such as `int64`, `float64` or `str`. | [Video 19](19-understanding-your-data/note.md) |
| Data warehouse | A separate store of copied company data, safe to analyse without touching the live database. | [Video 9](09-mldlc/note.md) |
| Data | Examples of inputs together with their outputs. | [Video 1](01-what-is-ml/note.md) |
| Database server | A program that holds databases and answers queries, such as MySQL. | [Video 16](16-working-with-json-and-sql/note.md) |
| Database | A program that stores data as tables and answers queries. | [Video 16](16-working-with-json-and-sql/note.md) |
| Datetime | A value pandas understands as a point in time, with date and time parts. | [Video 34](34-date-and-time/note.md) |
| datetime64 | The pandas column type for datetimes; `[us]` means microsecond resolution. | [Video 34](34-date-and-time/note.md) |
| Day of week | The weekday as a number, Monday = 0 to Sunday = 6 (`.dt.dayofweek`). | [Video 34](34-date-and-time/note.md) |
| DBSCAN | Density-based spatial clustering of applications with noise: clusters dense regions and labels lonely points as noise. | [Video 132](132-dbscan/note.md) |
| Dead zone | The range of S for which the Lasso slope is exactly 0. | [Video 68](68-lasso-sparsity/note.md) |
| Decision boundary | A line or curve that separates the classes in classification. | [Video 6](06-instance-vs-model-based/note.md) |
| Decision node | A node in the middle of a tree that asks a question and splits again. | [Video 97](97-decision-trees-intuition/note.md) |
| Decision region | The part of the input space in which a model predicts a given class. | [Video 79](79-softmax-regression/note.md) |
| Decision rule (SVM) | Predict +1 if $w \cdot u + b \geq 0$ and −1 otherwise. | [Video 93](93-svm-maths/note.md) |
| Decision stump | A decision tree with maximum depth 1: one split, two regions. | [Video 115](115-adaboost-intuition/note.md) |
| Decision surface | A plot colouring every point of the input space by the class the model would predict there. | [Video 91](91-knn/note.md) |
| Decision tree | A model that predicts by asking a chain of questions about the input columns: nested if-else conditions. | [Video 97](97-decision-trees-intuition/note.md) |
| DecisionTreeRegressor | scikit-learn's regression tree. | [Video 99](99-regression-trees/note.md) |
| Deep Learning (DL) | Machine Learning that uses neural networks with many layers; finds features by itself. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Default direction | The side of a split that rows with a missing value follow. | [Video 123](123-xgboost-intro/note.md) |
| Degree | The highest power used in the polynomial. | [Video 61](61-polynomial-regression/note.md) |
| Delivery routing | Planning the most efficient route for deliveries. | [Video 8](08-applications-of-ml/note.md) |
| Demand forecasting | Predicting how much of something will be needed, where and when. | [Video 8](08-applications-of-ml/note.md) |
| Dendrogram | A tree showing which rows (or columns) were joined as similar, and in what order. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Dense region, sparse region | An area with many points close together; an area with few points. | [Video 132](132-dbscan/note.md) |
| Density plot | A histogram with a smooth KDE curve on top. | [Video 20](20-univariate-analysis/note.md) |
| Density-based clustering | Clustering that finds dense regions of points separated by sparse regions. | [Video 132](132-dbscan/note.md) |
| Density-connected | Linked by a chain of core points with every step at most eps. | [Video 132](132-dbscan/note.md) |
| Dependent events | Events that are not independent: knowing one changes the probability of the other. | [Video 83](83-independent-events/note.md) |
| Dependent variable | The output column (y). | [Video 13](13-toy-project/note.md) |
| Deploy | Move a model from development to production. | [Video 4](04-batch-learning/note.md) |
| Deployment | Putting a model on a server so users can reach it. | [Video 7](07-challenges-in-ml/note.md) |
| Depth | The number of questions on the longest path from a tree's root to a leaf. | [Video 98](98-decision-tree-hyperparameters/note.md) |
| Derivative | The slope of a function at a point. | [Video 51](51-linear-regression-maths/note.md) |
| Descriptive statistics | Numbers that summarise data, such as count, mean, spread and percentiles. | [Video 19](19-understanding-your-data/note.md) |
| Design matrix ($X$) | The data as a matrix, one row per data point, with a first column of 1s for the intercept. | [Video 54](54-multiple-lr-maths/note.md) |
| Development environment | Our own machine, where we build and train a model. | [Video 4](04-batch-learning/note.md) |
| Diabetes dataset | scikit-learn's built-in data of 442 patients, 10 standardised inputs, and disease progression one year later. | [Video 55](55-multiple-lr-code/note.md) |
| Differentiable loss | A loss function whose derivative exists at every point, so it can be minimised with derivatives. | [Video 121](121-gradient-boosting-regression-maths/note.md) |
| Differential entropy | The entropy of a continuous variable; higher for a more spread-out distribution. | [Video 97](97-decision-trees-intuition/note.md) |
| Dimension | One input column (one feature); a different meaning from the dimensions (axes) of a tensor in Video 11. | [Video 3](03-types-of-ml/note.md) |
| Dimensionality reduction | Reducing the number of input columns while keeping the information. | [Video 3](03-types-of-ml/note.md) |
| Dimensionality | The number of columns (features) in the data. | [Video 27](27-one-hot-encoding/note.md) |
| Dirty data | Data with errors, gaps, duplicates or inconsistencies. | [Video 9](09-mldlc/note.md) |
| Discretization | Turning a continuous column into a discrete one by cutting its range into intervals. | [Video 32](32-binning-binarization/note.md) |
| Distance weight (nan-Euclidean) | All columns divided by the columns present in both rows; makes up for the skipped columns. | [Video 39](39-knn-imputer/note.md) |
| Distance weighting | Each neighbour counts in proportion to 1 / its distance, so nearer rows count more. | [Video 39](39-knn-imputer/note.md) |
| Distance | A number measuring how far apart two points are; small distance = similar. | [Video 6](06-instance-vs-model-based/note.md) |
| distance_threshold | Height at which `AgglomerativeClustering` stops merging, instead of a fixed number of clusters. | [Video 131](131-hierarchical-clustering/note.md) |
| Distributed computing | Sharing one job between several machines (nodes), coordinated by a master node. | [Video 123](123-xgboost-intro/note.md) |
| Distribution | How a column's values spread over their range. | [Video 20](20-univariate-analysis/note.md) |
| Diverge | To move further away with each step, the loss growing instead of shrinking. | [Video 57](57-gradient-descent/note.md) |
| Divisive clustering | Top-down hierarchical clustering: start with one cluster and split repeatedly. | [Video 131](131-hierarchical-clustering/note.md) |
| Domain knowledge | Knowledge of the field the data comes from. | [Video 23](23-what-is-feature-engineering/note.md) |
| Donor | A row that has a value in the column being filled, so it can be a neighbour. | [Video 39](39-knn-imputer/note.md) |
| Dot product | Multiply matching components of two vectors and add; $u^{\mathsf T}x$. | [Video 48](48-pca-step-by-step/note.md) |
| dropna | The pandas method that drops rows (or columns) with missing values. | [Video 35](35-complete-case-analysis/note.md) |
| dtreeviz | A Python library that draws decision trees with the training data shown at every node. | [Video 100](100-dtreeviz/note.md) |
| dtype | The data type of a column, such as `int64`, `float64` or `str`. | [Video 15](15-working-with-csv/note.md) |
| Dummy variable trap | The multicollinearity caused by keeping all $n$ dummy columns, which always add up to 1. | [Video 27](27-one-hot-encoding/note.md) |
| Dummy variable | One of the 0/1 columns created by one-hot encoding. | [Video 27](27-one-hot-encoding/note.md) |
| Duplicate row | A row identical to another row in every column. | [Video 19](19-understanding-your-data/note.md) |
| Durbin-Watson statistic | A number from 0 to 4 measuring autocorrelation of residuals; about 2 means none. | [Video 56](56-linear-regression-assumptions/note.md) |
| Eager learning | Another name for model-based learning: all the work done up front. | [Video 6](06-instance-vs-model-based/note.md) |
| Early stopping | Stopping training when the score on held-out data is best, before full convergence; this keeps coefficients small, so it also acts as regularisation. | [Video 58](58-batch-gradient-descent/note.md) |
| Economy rate | A bowler's runs conceded per over. | [Video 45](45-feature-construction-splitting/note.md) |
| Eigen-decomposition | Finding all the eigenvalues and eigenvectors of a matrix. | [Video 48](48-pca-step-by-step/note.md) |
| Eigenvalue | The factor by which a matrix stretches its eigenvector. | [Video 48](48-pca-step-by-step/note.md) |
| Eigenvector | A vector that a matrix only stretches or shrinks, without turning it. | [Video 48](48-pca-step-by-step/note.md) |
| Elastic Net regression | Linear regression with both the L1 and the L2 penalty. | [Video 69](69-elastic-net/note.md) |
| Elastic Net | Linear regression with a mix of the L1 and L2 penalties. | [Video 63](63-ridge-regression-intuition/note.md) |
| ElasticNetCV | scikit-learn's Elastic Net that picks alpha and l1_ratio by cross-validation. | [Video 69](69-elastic-net/note.md) |
| Elbow curve | A plot of WCSS against the number of clusters k. | [Video 128](128-kmeans-intuition/note.md) |
| Elbow method | Choosing k at the point where the elbow curve bends from steep to flat. | [Video 128](128-kmeans-intuition/note.md) |
| Elbow point | The k after which adding clusters barely lowers WCSS. | [Video 128](128-kmeans-intuition/note.md) |
| encode | The `KBinsDiscretizer` parameter choosing ordinal (bin numbers) or one-hot output. | [Video 32](32-binning-binarization/note.md) |
| Encoding | Two senses: the rulebook that maps text characters to stored bytes (Video 15); or turning categories into numbers (categorical encoding, Video 26). | [Video 15](15-working-with-csv/note.md) |
| End of distribution imputation | Filling every gap with a value at the edge of the distribution: $\mu \pm 3\sigma$ or $Q_3 + 1.5\,\text{IQR}$. | [Video 36](36-imputing-numerical-data/note.md) |
| End-to-end product | A complete product, from raw data to software that users use. | [Video 9](09-mldlc/note.md) |
| Endpoint | One address of an API that returns one kind of data. | [Video 17](17-fetching-data-from-api/note.md) |
| Ensemble learning | Combining several models into one stronger model. | [Video 9](09-mldlc/note.md) |
| Entropy | A measure of disorder: $-\sum p_i \log_2 p_i$; 0 when pure, 1 for a 50/50 two-class node. | [Video 97](97-decision-trees-intuition/note.md) |
| Environment file | A file (`environment.yml`) listing an environment's packages and versions. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| Environment variable | A named value stored on the computer, outside the code, read with `os.environ`. | [Video 17](17-fetching-data-from-api/note.md) |
| Environment | The world the agent acts in. | [Video 3](03-types-of-ml/note.md) |
| Epoch | One full update of the parameters using the whole training set. | [Video 57](57-gradient-descent/note.md) |
| eps (epsilon) | The radius of the neighbourhood DBSCAN examines around each point. | [Video 132](132-dbscan/note.md) |
| eps-neighbourhood | All points within distance eps of a point. | [Video 132](132-dbscan/note.md) |
| Equal frequency binning | Binning into bins holding the same number of rows, with the quantiles as edges; also called quantile binning. | [Video 32](32-binning-binarization/note.md) |
| Equal width binning | Binning into bins of the same width, $(\max - \min)/k$; also called uniform binning. | [Video 32](32-binning-binarization/note.md) |
| Error (residual) | The gap between an actual value and the model's prediction. | [Video 50](50-simple-linear-regression/note.md) |
| Error function (loss function) | A formula for how wrong the model is; here the sum of squared errors. | [Video 51](51-linear-regression-maths/note.md) |
| errors="coerce" | The `pd.to_numeric` option that turns values it cannot convert into NaN instead of stopping. | [Video 33](33-mixed-variables/note.md) |
| estimator | The base model that bagging copies (formerly base_estimator). | [Video 106](106-bagging-classifier/note.md) |
| estimators_features_ | The column numbers each trained base model was given. | [Video 106](106-bagging-classifier/note.md) |
| estimators_samples_ | The row numbers each trained base model was given. | [Video 106](106-bagging-classifier/note.md) |
| Eta ($\eta$) | XGBoost's name for the learning rate; default 0.3. | [Video 124](124-xgboost-regression/note.md) |
| eta0 | The starting learning rate in SGDRegressor. | [Video 59](59-stochastic-gradient-descent/note.md) |
| ETL | Extract, transform, load: copying data from source systems into a warehouse. | [Video 9](09-mldlc/note.md) |
| Euclidean distance | The straight-line distance between two points. | [Video 39](39-knn-imputer/note.md) |
| Event | A set of outcomes, such as "the sum is at most 10". | [Video 82](82-conditional-probability/note.md) |
| Evidence | The overall probability of the observed evidence. | [Video 85](85-bayes-theorem/note.md) |
| Exact greedy algorithm | Finding a split by trying the midpoint between every pair of neighbouring sorted values. | [Video 123](123-xgboost-intro/note.md) |
| Expert system | Early AI: a human expert's knowledge written as rules, plus a program that applies them. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Explained variance ratio | One component's share of the total variance: its eigenvalue divided by the sum of all. | [Video 49](49-pca-mnist/note.md) |
| Explained variance | The variance along a principal component; its eigenvalue. | [Video 48](48-pca-step-by-step/note.md) |
| explained_variance_ | The eigenvalues of the fitted PCA, largest first. | [Video 49](49-pca-mnist/note.md) |
| Explicit programming | A human writing out every rule the computer follows. ML avoids it. | [Video 1](01-what-is-ml/note.md) |
| Exploratory data analysis (EDA) | Exploring data with summaries and plots to find patterns. | [Video 13](13-toy-project/note.md) |
| export_graphviz | scikit-learn function that writes a tree as Graphviz DOT text. | [Video 100](100-dtreeviz/note.md) |
| export_text | scikit-learn function that prints a trained tree as indented text. | [Video 110](110-bagging-vs-random-forest/note.md) |
| Extrapolation | Predicting for inputs outside the range of the training data. | [Video 50](50-simple-linear-regression/note.md) |
| f-string | Text starting with `f` in which `{name}` is replaced by a value. | [Video 17](17-fetching-data-from-api/note.md) |
| F1 score | The harmonic mean of precision and recall. | [Video 77](77-precision-recall-f1/note.md) |
| False negative (FN) | Predicted negative, but actually positive; a Type II error. | [Video 76](76-accuracy-confusion-matrix/note.md) |
| False positive (FP) | Predicted positive, but actually negative; a Type I error. | [Video 76](76-accuracy-confusion-matrix/note.md) |
| False positive rate (FPR) | The fraction of real negatives the model wrongly flags. | [Video 78](78-roc-auc/note.md) |
| Family size | `SibSp` + `Parch` + 1: the number of people in a passenger's travelling family. | [Video 45](45-feature-construction-splitting/note.md) |
| Family type | Family size grouped into alone, small family (2 to 4) and large family (5 or more). | [Video 45](45-feature-construction-splitting/note.md) |
| Feature construction | Creating a new column by hand from existing ones, e.g. rooms + washrooms into area. | [Video 23](23-what-is-feature-engineering/note.md) |
| Feature engineering | Choosing, removing and creating features. | [Video 7](07-challenges-in-ml/note.md) |
| Feature extraction | Letting an algorithm such as PCA produce new columns from the existing ones (compare feature construction, where we make them by hand). | [Video 23](23-what-is-feature-engineering/note.md) |
| Feature importance | A column's share of all the impurity reduction in a tree; the shares add up to 1. | [Video 99](99-regression-trees/note.md) |
| Feature map ($\phi$) | The explicit transformation of a point into the higher-dimensional space. | [Video 96](96-kernel-trick-code/note.md) |
| Feature scaling | Putting columns on the same scale, so no column dominates distances. | [Video 6](06-instance-vs-model-based/note.md) |
| Feature selection | Keeping only the useful input columns and dropping the rest. | [Video 23](23-what-is-feature-engineering/note.md) |
| Feature splitting | Breaking a column that holds several facts into one column per fact. | [Video 45](45-feature-construction-splitting/note.md) |
| Feature transformation | Changing a column into a form the model can use better. | [Video 23](23-what-is-feature-engineering/note.md) |
| Feature | One piece of information about each example that a model uses (e.g. a student's CGPA). | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| feature_importances_ | The fitted attribute holding the feature importance of every column. | [Video 99](99-regression-trees/note.md) |
| Fence | A limit 1.5 IQR beyond the box; values past it are possible outliers. | [Video 20](20-univariate-analysis/note.md) |
| fit / transform | Learn the scaler's numbers from the training set / apply them to any data. | [Video 24](24-standardization/note.md) |
| fit_predict | Trains a clustering model and returns the cluster of every row. | [Video 129](129-kmeans-code/note.md) |
| fit_transform | Fit and transform in one call; used on the training set only. | [Video 28](28-column-transformer/note.md) |
| Five-number summary | Minimum, Q1, median, Q3 and maximum. | [Video 20](20-univariate-analysis/note.md) |
| For loop | Code that repeats once for each item of a collection. | [Video 15](15-working-with-csv/note.md) |
| Forest-level hyperparameters | The settings that shape the forest itself: n_estimators, max_features, bootstrap, max_samples. | [Video 111](111-random-forest-hyperparameters/note.md) |
| Format string | A pattern such as `"%d/%m/%Y"` telling `pd.to_datetime` how dates are written. | [Video 34](34-date-and-time/note.md) |
| Forward selection | Feature selection that starts empty and adds the best column at a time. | [Video 23](23-what-is-feature-engineering/note.md) |
| Frame | One image in a video. | [Video 11](11-tensors/note.md) |
| Framing an ML problem | Turning a business problem into a precise ML task that can be built and measured. | [Video 14](14-framing-ml-problem/note.md) |
| Framing the problem | Deciding the goal, users, cost, team and approach before any work starts. | [Video 9](09-mldlc/note.md) |
| Fraud detection | Spotting dishonest transactions; here the outliers are what we want to find. | [Video 41](41-what-are-outliers/note.md) |
| Frequency | How many times a value or category occurs. | [Video 20](20-univariate-analysis/note.md) |
| Fully grown tree | A tree split until every leaf is pure; usually overfits. | [Video 98](98-decision-tree-hyperparameters/note.md) |
| func | The `FunctionTransformer` parameter that holds the function to apply. | [Video 30](30-function-transformer/note.md) |
| Function, lambda | A named reusable piece of code (`def`), and a one-line unnamed one. | [Video 15](15-working-with-csv/note.md) |
| FunctionTransformer | scikit-learn's class that applies any function we give it to the data. | [Video 30](30-function-transformer/note.md) |
| Gain (XGBoost) | Similarity of the two children minus similarity of the parent; the split with the largest gain is chosen. | [Video 124](124-xgboost-regression/note.md) |
| Gamma ($\gamma$, `min_split_loss`) | Minimum gain a split must exceed to be kept; default 0. | [Video 124](124-xgboost-regression/note.md) |
| gamma | How far one point's influence reaches in the RBF kernel; large gamma gives tighter boundaries. | [Video 96](96-kernel-trick-code/note.md) |
| Garbage in, garbage out | Bad input data always gives bad results. | [Video 7](07-challenges-in-ml/note.md) |
| Gaussian Naive Bayes | Naive Bayes that models each numerical input as normally distributed within each class. | [Video 90](90-gaussian-naive-bayes/note.md) |
| GaussianNB | scikit-learn's Gaussian Naive Bayes. | [Video 90](90-gaussian-naive-bayes/note.md) |
| Generalisation | How well a model performs on new data it was not trained on. | [Video 71](71-perceptron-code/note.md) |
| get_dummies | pandas function that one-hot encodes columns; `drop_first=True` keeps $n - 1$. | [Video 27](27-one-hot-encoding/note.md) |
| get_feature_names_out | `OneHotEncoder` method that returns the names of the new columns. | [Video 27](27-one-hot-encoding/note.md) |
| Gini impurity | A measure of impurity: $1 - \sum p_i^2$; 0 when pure, 0.5 for a 50/50 two-class node. | [Video 97](97-decision-trees-intuition/note.md) |
| Global minimum | The lowest point of the whole function. | [Video 57](57-gradient-descent/note.md) |
| Good fit | Capturing the pattern while ignoring the noise. | [Video 7](07-challenges-in-ml/note.md) |
| Google Colab | Google's browser-based Jupyter notebooks, saved in Google Drive. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| GPU | A graphics chip that runs deep learning maths much faster than a CPU. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| Gradient $g_i$ | First derivative of row $i$'s loss with respect to the previous prediction. | [Video 126](126-xgboost-maths/note.md) |
| Gradient boosting | A boosting algorithm that starts from a simple guess and adds trees one by one, each trained on the mistakes (pseudo-residuals) of the ensemble so far. | [Video 120](120-gradient-boosting-intuition/note.md) |
| Gradient descent | Finding the lowest point of a function by repeated small steps downhill. | [Video 57](57-gradient-descent/note.md) |
| Gradient | The vector of partial derivatives of the loss; it points in the direction of steepest increase. | [Video 57](57-gradient-descent/note.md) |
| Graphviz | The graph-drawing program (`dot`) that lays out tree diagrams for dtreeviz and export_graphviz. | [Video 100](100-dtreeviz/note.md) |
| Greedy search | Taking the best split at each node without looking ahead. | [Video 97](97-decision-trees-intuition/note.md) |
| Grid search | Training a model for every combination of listed settings and keeping the best by cross-validation. | [Video 38](38-missing-indicator-random-sample/note.md) |
| Grouping effect | Elastic Net's tendency to give correlated inputs similar coefficients instead of keeping only one. | [Video 69](69-elastic-net/note.md) |
| handle_unknown | `OneHotEncoder` parameter that decides what happens to categories never seen in training. | [Video 27](27-one-hot-encoding/note.md) |
| handle_unknown="ignore" | `OneHotEncoder` setting that outputs all zeros for a category not seen in training. | [Video 29](29-pipelines/note.md) |
| Hard voting | Predicting the label that most base models predict. | [Video 103](103-voting-classifier/note.md) |
| Hard-margin SVM | The SVM that allows no point inside the margin or on the wrong side; it needs perfectly separable data. | [Video 93](93-svm-maths/note.md) |
| Harmonic mean | An average that stays close to the smaller of the values: $2ab/(a + b)$ for two values. | [Video 77](77-precision-recall-f1/note.md) |
| Header | The line of a file that holds the column names. | [Video 15](15-working-with-csv/note.md) |
| Headers | Extra information sent with a request, such as the User-Agent. | [Video 18](18-web-scraping/note.md) |
| Heatmap | A table drawn as coloured cells, darker for larger values. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Hessian $h_i$ | Second derivative of row $i$'s loss with respect to the previous prediction. | [Video 126](126-xgboost-maths/note.md) |
| Heteroscedasticity | The spread of the residuals changes with the predicted value, often as a funnel. | [Video 56](56-linear-regression-assumptions/note.md) |
| Hierarchical clustering | Clustering that builds a hierarchy of clusters, from single points up to one cluster. | [Video 131](131-hierarchical-clustering/note.md) |
| High bias, low variance algorithm | An algorithm too simple to fit the training data well but stable across samples, such as linear regression; it underfits. | [Video 109](109-random-forest-bias-variance/note.md) |
| High cardinality | A categorical column with very many different categories. | [Video 22](22-pandas-profiling/note.md) |
| High-dimensional data | Data with a very large number of columns. | [Video 46](46-curse-of-dimensionality/note.md) |
| Hinge loss | $\max(0, 1 - y(w^T x + b))$ per point: the error term of the soft-margin SVM. | [Video 94](94-svm-soft-margin/note.md) |
| Histogram | A bar chart of how many values fall in each equal range (bin) of a numerical column. | [Video 20](20-univariate-analysis/note.md) |
| Hold-out set | Rows set aside before training, used only to produce honest predictions or scores. | [Video 127](127-stacking-blending/note.md) |
| Homoscedasticity | The residuals have the same spread for all predicted values. | [Video 56](56-linear-regression-assumptions/note.md) |
| HTML | The language web pages are written in: a tree of nested tags. | [Video 18](18-web-scraping/note.md) |
| Hue, style, size | Plot settings that show an extra column by colour, marker shape or dot size. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Hyper-cuboid | A box in many dimensions: the region a tree's cuts carve out. | [Video 97](97-decision-trees-intuition/note.md) |
| Hyperparameter tuning | Trying several hyperparameter values and keeping the best. | [Video 29](29-pipelines/note.md) |
| Hyperparameter | A setting of an algorithm chosen before training, such as a tree's `max_depth`. | [Video 29](29-pipelines/note.md) |
| Hyperplane | A flat surface in more than three dimensions; the model for three or more input columns. | [Video 53](53-multiple-linear-regression/note.md) |
| Hypothesis function | A model written as a function $h(x)$ that maps an input to a prediction. | [Video 115](115-adaboost-intuition/note.md) |
| Identity matrix | The matrix that leaves every vector unchanged. | [Video 48](48-pca-step-by-step/note.md) |
| If-else ladder | A long chain of hand-written conditions, one per case. | [Video 1](01-what-is-ml/note.md) |
| Image classification | Deciding what a picture contains, e.g. dog or not dog. | [Video 1](01-what-is-ml/note.md) |
| Imbalanced data | Data in which one class is much rarer than another. | [Video 76](76-accuracy-confusion-matrix/note.md) |
| Imputation | Filling in missing values, for example with the mean, median or mode. | [Video 23](23-what-is-feature-engineering/note.md) |
| include_bias | PolynomialFeatures setting that adds a column of 1s. | [Video 61](61-polynomial-regression/note.md) |
| Incremental learning | Training on small pieces of data over time (the opposite of batch). | [Video 4](04-batch-learning/note.md) |
| Incremental training | Training in small steps, keeping what was learned before. | [Video 5](05-online-learning/note.md) |
| Independent events | Events where one happening does not change the probability of the other. | [Video 83](83-independent-events/note.md) |
| Independent models | Models whose mistakes are unrelated, so one being wrong says nothing about the others. | [Video 102](102-voting-ensemble/note.md) |
| Independent variables | The input columns (X). | [Video 13](13-toy-project/note.md) |
| Index | The row labels of a DataFrame. | [Video 15](15-working-with-csv/note.md) |
| Inertia | A big organisation's resistance to changing direction once it has started. | [Video 14](14-framing-ml-problem/note.md) |
| inertia_ | The WCSS of a fitted `KMeans` model. | [Video 129](129-kmeans-code/note.md) |
| Inference engine | The part of an expert system that applies the rules to answer a question. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Inference | Learning how the inputs affect the output, rather than only predicting it. | [Video 91](91-knn/note.md) |
| Information gain | The drop in entropy from a parent to its weighted children; the tree splits on the highest. | [Video 97](97-decision-trees-intuition/note.md) |
| Input / output | The columns we know / the column we want to predict. | [Video 3](03-types-of-ml/note.md) |
| Inspect | Browser tool that shows which tag draws each part of a page. | [Video 18](18-web-scraping/note.md) |
| Instance set $I_j$ | The rows that land in leaf $j$. | [Video 126](126-xgboost-maths/note.md) |
| Instance-based learning | Learning by storing the training data and comparing new points with it. | [Video 6](06-instance-vs-model-based/note.md) |
| Interaction term | A product of two inputs, such as $xy$, that lets one input's effect depend on another. | [Video 61](61-polynomial-regression/note.md) |
| Intercept | The line's value when the input is 0; $b$ in $y = mx + b$. | [Video 50](50-simple-linear-regression/note.md) |
| intercept_ | The fitted intercept in scikit-learn. | [Video 50](50-simple-linear-regression/note.md) |
| Interpretability | How well people can understand why a model makes its decisions. | [Video 114](114-feature-importance/note.md) |
| Interquartile range (IQR) | Q3 - Q1: the width of the middle half of the data. | [Video 20](20-univariate-analysis/note.md) |
| Intersection (A ∩ B) | The event that both A and B happen. | [Video 82](82-conditional-probability/note.md) |
| Inverse matrix | The matrix that undoes another: their product is the identity matrix. | [Video 54](54-multiple-lr-maths/note.md) |
| IoT sensor | A device that measures something and sends the readings over the internet. | [Video 8](08-applications-of-ml/note.md) |
| IQR method (IQR rule, IQR proximity rule) | Outlier detection that flags values beyond 1.5 IQR outside the box ($Q_1$ to $Q_3$); for skewed columns. | [Video 20](20-univariate-analysis/note.md) |
| isnull | The pandas method that marks each missing cell `True`. | [Video 35](35-complete-case-analysis/note.md) |
| ISO week | The week number of the ISO calendar, from `.dt.isocalendar().week`; week 1 holds the year's first Thursday. | [Video 34](34-date-and-time/note.md) |
| Iteration (MICE) | One pass that re-predicts the gaps of every column once, in order. | [Video 40](40-iterative-imputer-mice/note.md) |
| Iteration 0 | The starting table, with every gap filled by its column mean. | [Video 40](40-iterative-imputer-mice/note.md) |
| Iterative imputer | Multivariate imputation that predicts each column from the others, repeatedly; its algorithm is MICE. | [Video 35](35-complete-case-analysis/note.md) |
| joblib | A library that saves and loads Python objects like pickle, better suited to large arrays. | [Video 29](29-pipelines/note.md) |
| Joint probability | The probability that two events happen together, $P(A \cap B)$. | [Video 86](86-bayes-problem/note.md) |
| JSON (JavaScript Object Notation) | A plain-text format for structured data, made of objects and arrays, that almost every language can read; used by APIs. | [Video 9](09-mldlc/note.md) |
| JSON Lines | A JSON file with one object per line, read with `lines=True`. | [Video 16](16-working-with-json-and-sql/note.md) |
| JSON viewer | A tool that lays out JSON text as a tree to show its structure. | [Video 17](17-fetching-data-from-api/note.md) |
| Jupyter | Tool for notebooks that mix code, output and text. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| JupyterLab | The program that runs Jupyter notebooks in a web browser. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| k (n_neighbors) | The number of neighbours that vote; KNN's main hyperparameter. | [Video 91](91-knn/note.md) |
| k | The number of clusters k-means makes; chosen by us. | [Video 128](128-kmeans-intuition/note.md) |
| k-distance plot | Sorted distances from every point to its k-th nearest point, used to choose eps. | [Video 132](132-dbscan/note.md) |
| k-means binning | Binning whose edges lie halfway between the centres of the groups found by k-means. | [Video 32](32-binning-binarization/note.md) |
| k-means | A clustering algorithm that repeatedly assigns points to the nearest centre and moves each centre to the mean of its points. | [Video 32](32-binning-binarization/note.md) |
| k-means++ | The default start of `KMeans`: centroids picked one by one, far-away points more likely. | [Video 129](129-kmeans-code/note.md) |
| K-nearest neighbours (KNN) | Predicting from the answers of the k closest stored points. | [Video 6](06-instance-vs-model-based/note.md) |
| Kaggle | A website for sharing datasets and notebooks and for ML competitions. | [Video 17](17-fetching-data-from-api/note.md) |
| KBinsDiscretizer | scikit-learn's class for equal width, equal frequency and k-means binning. | [Video 32](32-binning-binarization/note.md) |
| KDE plot | A smooth estimate of a column's PDF, built from the data. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Kernel (SVM) | The function that maps the data to the higher-dimensional space (not the Jupyter kernel). | [Video 95](95-kernel-trick-intuition/note.md) |
| Kernel density estimate (KDE) | A smooth curve that estimates a column's distribution from its values. | [Video 20](20-univariate-analysis/note.md) |
| Kernel function $K(a, b)$ | A function that returns $\phi(a) \cdot \phi(b)$ directly from the original points. | [Video 96](96-kernel-trick-code/note.md) |
| Kernel transformation | Applying a kernel to the data. | [Video 95](95-kernel-trick-intuition/note.md) |
| Kernel trick | Making non-linear data separable by mapping it to a higher dimension, without building the new columns. | [Video 95](95-kernel-trick-intuition/note.md) |
| Kernel | The running Python process behind a notebook. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| KMeans | scikit-learn's k-means class, in `sklearn.cluster`. | [Video 129](129-kmeans-code/note.md) |
| KNeighborsClassifier | scikit-learn's KNN classifier; `n_neighbors=5` by default. | [Video 91](91-knn/note.md) |
| KNN imputer | Multivariate imputation from the most similar rows (`KNNImputer`). | [Video 35](35-complete-case-analysis/note.md) |
| Knowledge base | The collection of rules inside an expert system. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Kurtosis | How heavy the tails of a distribution are compared with a normal curve. | [Video 22](22-pandas-profiling/note.md) |
| L1 regularisation | Another name for the absolute-value penalty used by Lasso. | [Video 67](67-lasso-regression/note.md) |
| l1_ratio | The share of the total penalty given to the L1 (Lasso) part. | [Video 69](69-elastic-net/note.md) |
| L2 regularisation | Another name for the squared-coefficient penalty used by Ridge. | [Video 63](63-ridge-regression-intuition/note.md) |
| Label encoding | Replacing the classes of the target by 0, 1, 2, ...; for the output column only. | [Video 26](26-ordinal-label-encoding/note.md) |
| LabelEncoder | scikit-learn's class for label encoding the target. | [Video 26](26-ordinal-label-encoding/note.md) |
| Labelled data | Data that includes the output column. | [Video 3](03-types-of-ml/note.md) |
| labels_ | The cluster number of every training row, after fitting. | [Video 129](129-kmeans-code/note.md) |
| Lambda ($\lambda$) | The power used by a power transform, learned separately for each column. | [Video 31](31-power-transformer/note.md) |
| Lambda ($\lambda$, `reg_lambda`) | Regularisation parameter added to the denominators; shrinks scores and outputs; default 1. | [Video 124](124-xgboost-regression/note.md) |
| Lambda | A one-line Python function without a name, such as `lambda x: x**2`. | [Video 30](30-function-transformer/note.md) |
| lambdas_ | The `PowerTransformer` attribute holding the learned $\lambda$ of each column. | [Video 31](31-power-transformer/note.md) |
| Laplace smoothing | Adding a small count (usually 1) to every count so that no probability is 0. | [Video 89](89-naive-bayes-code/note.md) |
| Lasso regression | Linear regression with a penalty on the sum of absolute coefficients (L1). | [Video 63](63-ridge-regression-intuition/note.md) |
| Latency | The delay between a request and its answer; high for KNN on large data. | [Video 91](91-knn/note.md) |
| Law of total probability | $P(B) = \sum_i P(B \mid A_i) P(A_i)$, when the $A_i$ are mutually exclusive and cover every case. | [Video 86](86-bayes-problem/note.md) |
| Layer | One step in a neural network; each layer builds on what the previous one found. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Lazy learning | Another name for instance-based learning: no work until a question arrives. | [Video 6](06-instance-vs-model-based/note.md) |
| lbfgs | The default solver of LogisticRegression; supports L2 or no penalty. | [Video 81](81-logistic-hyperparameters/note.md) |
| LDA | Linear discriminant analysis: a supervised method that finds the directions that best separate the classes. | [Video 49](49-pca-mnist/note.md) |
| Leaf node | A node that is not split; it gives the prediction. | [Video 97](97-decision-trees-intuition/note.md) |
| Leaf value ($\gamma_{jm}$) | The constant a leaf adds to the model, chosen to minimise the loss of the rows in that leaf. | [Video 121](121-gradient-boosting-regression-maths/note.md) |
| Leaf value in log-odds | $\sum r / \sum p(1-p)$ over a leaf's rows: the amount the leaf adds to the log-odds. | [Video 122](122-gradient-boosting-classification/note.md) |
| Leaf weight $w_j$ | The output value of leaf $j$ of a tree. | [Video 126](126-xgboost-maths/note.md) |
| Learning rate ($\eta$) in gradient boosting | The fraction of each tree's output that is added to the model, the same for every tree; typically 0.1. | [Video 120](120-gradient-boosting-intuition/note.md) |
| Learning rate ($\eta$) | How strongly each update changes the model; in gradient descent, the number the slope is multiplied by to get the step size. | [Video 5](05-online-learning/note.md) |
| Learning rate (AdaBoost) | A multiplier on every weak learner's alpha; values below 1 slow learning. | [Video 118](118-adaboost-hyperparameters/note.md) |
| Learning schedule | A rule that changes the learning rate during training, usually shrinking it. | [Video 59](59-stochastic-gradient-descent/note.md) |
| Learning | Finding rules (patterns) from examples. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| LightGBM | Microsoft's gradient boosting library, aimed at speed and low memory use. | [Video 123](123-xgboost-intro/note.md) |
| Likelihood | The probability of what we observed, given a hypothesis; for a classifier, the product over all points of the probabilities it gives to their true classes. | [Video 73](73-log-loss/note.md) |
| Line plot | A scatter plot with the dots joined in order, used when x is time. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Linear interpolation | Placing a percentile between two neighbouring sorted values, in proportion to its position; the pandas default. | [Video 44](44-outliers-percentile/note.md) |
| Linear regression | An algorithm that fits the straight line closest to all the points. | [Video 23](23-what-is-feature-engineering/note.md) |
| Linear relationship | A relationship between two columns that follows a straight line. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Linear transformation | A change of the whole plane by a matrix that keeps grid lines straight and evenly spaced. | [Video 48](48-pca-step-by-step/note.md) |
| Linearly separable | Data whose classes a straight line, plane or hyperplane can split. | [Video 70](70-perceptron-trick/note.md) |
| Linkage | The rule for the distance between two clusters. | [Video 131](131-hierarchical-clustering/note.md) |
| List of grids | Several parameter grids passed together, so incompatible values never meet. | [Video 112](112-random-forest-tuning/note.md) |
| List, dictionary | Python's ordered collection `[...]`, and its `key: value` pairs `{...}`. | [Video 15](15-working-with-csv/note.md) |
| Load balancing | Spreading requests across servers so all users are served quickly. | [Video 9](09-mldlc/note.md) |
| Local minimum | A point lower than everything around it, but not the lowest overall. | [Video 57](57-gradient-descent/note.md) |
| Local optimum (k-means) | A clustering where k-means has stopped but a better one exists, caused by a bad start. | [Video 130](130-kmeans-from-scratch/note.md) |
| Log transform | Replacing each value with its logarithm; pulls in a long right tail. | [Video 30](30-function-transformer/note.md) |
| Log-likelihood | The log of the likelihood: the sum of the log probabilities. | [Video 73](73-log-loss/note.md) |
| Log-odds | The natural log of the odds, $\ln(p/(1-p))$; any number, 0 at a probability of 0.5. | [Video 122](122-gradient-boosting-classification/note.md) |
| log1p | NumPy's $\log(1 + x)$, a log transform that also works when a value is 0. | [Video 30](30-function-transformer/note.md) |
| Logistic function | Another name for the sigmoid function. | [Video 72](72-sigmoid-function/note.md) |
| Logistic regression | A classification algorithm that finds a separating boundary. | [Video 13](13-toy-project/note.md) |
| Lookup table | The stored probabilities that Naive Bayes computes during training. | [Video 89](89-naive-bayes-code/note.md) |
| Loss function | A formula that measures how wrong a model's predictions are. | [Video 73](73-log-loss/note.md) |
| Low bias, high variance algorithm | An algorithm that fits its training data very well but changes a lot with the data, such as a fully grown tree; it overfits. | [Video 109](109-random-forest-bias-variance/note.md) |
| LPA | Lakh rupees per annum: a salary in hundreds of thousands of rupees per year. | [Video 50](50-simple-linear-regression/note.md) |
| Machine Learning (ML) | Using statistics to let a machine find patterns (rules) in data by itself. | [Video 1](01-what-is-ml/note.md) |
| Macro average | The plain mean of a metric over all classes. | [Video 77](77-precision-recall-f1/note.md) |
| Magnitude | The number part of a quantity, as opposed to its unit. | [Video 25](25-normalization/note.md) |
| Majority vote | Predicting the class that most of the neighbours have. | [Video 91](91-knn/note.md) |
| make_blobs | scikit-learn function that generates points around chosen centres. | [Video 129](129-kmeans-code/note.md) |
| make_circles | A scikit-learn generator of two concentric circles of points, a standard non-linear test dataset. | [Video 96](96-kernel-trick-code/note.md) |
| make_classification | scikit-learn function that creates random classification data. | [Video 71](71-perceptron-code/note.md) |
| make_column_transformer | Function that builds a column transformer from (transformer, columns) pairs, without names. | [Video 29](29-pipelines/note.md) |
| make_moons | scikit-learn function that creates two interlocking half-moon classes. | [Video 80](80-polynomial-logistic-regression/note.md) |
| make_pipeline | Function that builds a pipeline from objects alone, naming each step after its class. | [Video 29](29-pipelines/note.md) |
| make_regression | scikit-learn function that generates data following a linear pattern plus noise. | [Video 53](53-multiple-linear-regression/note.md) |
| MAP rule | Maximum a posteriori: predict the class with the largest posterior probability. | [Video 88](88-naive-bayes-maths/note.md) |
| MAR | Missing at random: the gaps depend on another, recorded column. | [Video 35](35-complete-case-analysis/note.md) |
| Margin (gap) | The distance from a separating line to the nearest point of a class. | [Video 71](71-perceptron-code/note.md) |
| Margin (SVM) | The full width between $\pi^+$ and $\pi^-$ (later shown to be $2/\lVert w \rVert$): twice the one-sided margin of the perceptron code Note. | [Video 92](92-svm-intuition/note.md) |
| Margin error | The term $\lVert w \rVert$/2 of the SVM loss; small when the margin is wide. | [Video 94](94-svm-soft-margin/note.md) |
| Margin-maximising hyperplane | The separating hyperplane with the largest margin: the SVM decision boundary. | [Video 92](92-svm-intuition/note.md) |
| Markdown | A simple way to format text with symbols such as `#` and `**`. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| Mathematical problem | A business goal restated as a measurable target, such as a churn rate to reach. | [Video 14](14-framing-ml-problem/note.md) |
| Mathematical transformation | Applying one mathematical formula to every value of a column. | [Video 30](30-function-transformer/note.md) |
| Matrix calculus | Rules for differentiating expressions with vectors and matrices. | [Video 54](54-multiple-lr-maths/note.md) |
| Matrix | A table of numbers: a 2D tensor. | [Video 11](11-tensors/note.md) |
| Max-abs scaling | Divide by the largest absolute value in the column, giving values from -1 to 1. | [Video 25](25-normalization/note.md) |
| max_depth | The cap on a tree's depth; None lets it grow until every leaf is pure. | [Video 98](98-decision-tree-hyperparameters/note.md) |
| max_features | The number of randomly chosen columns a tree considers at each split. | [Video 98](98-decision-tree-hyperparameters/note.md) |
| max_iter | The maximum number of epochs in SGDRegressor. | [Video 59](59-stochastic-gradient-descent/note.md) |
| max_leaf_nodes | The cap on the number of leaves; the tree grows best-first until it is reached. | [Video 98](98-decision-tree-hyperparameters/note.md) |
| max_samples | The number or share of rows each base model gets. | [Video 106](106-bagging-classifier/note.md) |
| MaxAbsScaler | scikit-learn's class for max-abs scaling. | [Video 25](25-normalization/note.md) |
| Maximum likelihood | Choosing the parameter value under which the observed data is most likely; used to find $\lambda$. | [Video 31](31-power-transformer/note.md) |
| MCAR | Missing completely at random: the gaps have no relation to any value in the data. | [Video 35](35-complete-case-analysis/note.md) |
| Mean absolute deviation | The average absolute distance of the points from their mean. | [Video 47](47-pca-geometric-intuition/note.md) |
| Mean absolute error (MAE) | The average absolute difference between actual and predicted values. | [Video 52](52-regression-metrics/note.md) |
| Mean centring | Subtracting the mean from every value, so the column's mean becomes 0. | [Video 24](24-standardization/note.md) |
| Mean decrease in impurity (MDI) | Impurity-based feature importance: a column's share of the total weighted impurity decrease of its splits, averaged over the trees; also called Gini importance. | [Video 114](114-feature-importance/note.md) |
| Mean imputation | Filling every gap with the mean of the column's known values. | [Video 36](36-imputing-numerical-data/note.md) |
| Mean normalization | Subtract the mean and divide by the range, giving values from -1 to 1 centred on 0. | [Video 25](25-normalization/note.md) |
| Mean squared error (MSE) | The average squared difference between actual and predicted values. | [Video 52](52-regression-metrics/note.md) |
| Mean squared error loss | The average squared error; its derivatives do not grow with the number of rows. | [Video 58](58-batch-gradient-descent/note.md) |
| Mean | The average of the values; the centre of the data. | [Video 19](19-understanding-your-data/note.md) |
| mean(axis=0) | The mean of each column of an array. | [Video 130](130-kmeans-from-scratch/note.md) |
| Median absolute deviation (MAD) | The median distance of the values from their median. | [Video 22](22-pandas-profiling/note.md) |
| Median imputation | Filling every gap with the median of the column's known values; better for skewed columns. | [Video 36](36-imputing-numerical-data/note.md) |
| Median | The middle value of sorted data; the 50% percentile. | [Video 19](19-understanding-your-data/note.md) |
| meshgrid | NumPy function that builds every combination of x and y values: the grid for a decision surface. | [Video 91](91-knn/note.md) |
| Meta-model | The model in stacking that is trained on the base models' predictions. | [Video 101](101-ensemble-learning/note.md) |
| method | The `PowerTransformer` parameter that picks `"box-cox"` or `"yeo-johnson"`. | [Video 31](31-power-transformer/note.md) |
| Metric | A number that tells whether the work is moving in the right direction. | [Video 14](14-framing-ml-problem/note.md) |
| MICE | Multivariate Imputation by Chained Equations: the algorithm behind the iterative imputer. | [Video 40](40-iterative-imputer-mice/note.md) |
| Min-max scaling | Subtract the column's minimum and divide by its range, giving values from 0 to 1; the main normalization technique. | [Video 25](25-normalization/note.md) |
| min_frequency | `OneHotEncoder` parameter that merges rare categories into one column. | [Video 27](27-one-hot-encoding/note.md) |
| min_impurity_decrease | The smallest weighted impurity decrease a split must give to be made. | [Video 98](98-decision-tree-hyperparameters/note.md) |
| min_samples_leaf | The smallest number of rows every leaf must keep. | [Video 98](98-decision-tree-hyperparameters/note.md) |
| min_samples_split | The smallest number of rows a node must hold to be split. | [Video 98](98-decision-tree-hyperparameters/note.md) |
| Mini-batch gradient descent | Gradient descent that uses a small random group of rows for every update. | [Video 58](58-batch-gradient-descent/note.md) |
| Mini-batch | A small group of data points used for one training step. | [Video 5](05-online-learning/note.md) |
| Miniforge | A small installer with only conda and Python, using conda-forge. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| Minkowski distance | A family of distances: p = 2 is Euclidean, p = 1 is Manhattan. | [Video 91](91-knn/note.md) |
| MinMaxScaler | scikit-learn's class for min-max scaling. | [Video 25](25-normalization/note.md) |
| MinPts (min_samples) | The number of points an eps-neighbourhood needs for the point to be a core point. | [Video 132](132-dbscan/note.md) |
| Missing category imputation | Filling every gap in a categorical column with a new category, "Missing". | [Video 37](37-missing-categorical-data/note.md) |
| Missing indicator | A 0/1 column recording whether a value was missing. | [Video 35](35-complete-case-analysis/note.md) |
| Missing value | An empty entry, shown by pandas as `NaN`. | [Video 15](15-working-with-csv/note.md) |
| Missing values | Empty cells in the data. | [Video 7](07-challenges-in-ml/note.md) |
| Mixed variable | A column holding both numerical and categorical data. | [Video 33](33-mixed-variables/note.md) |
| ML algorithm | A general method that finds the pattern between inputs and outputs in data. | [Video 1](01-what-is-ml/note.md) |
| MLDLC | Machine learning development life cycle: the guidelines for building an ML product from idea to product. | [Video 9](09-mldlc/note.md) |
| MLOps | Running and maintaining ML models in production. | [Video 7](07-challenges-in-ml/note.md) |
| MNAR | Missing not at random: the gaps depend on the missing value itself. | [Video 35](35-complete-case-analysis/note.md) |
| MNIST | A dataset of about 70,000 handwritten-digit images of 28 × 28 pixels. | [Video 23](23-what-is-feature-engineering/note.md) |
| Mode | The most common value of a column. | [Video 23](23-what-is-feature-engineering/note.md) |
| Model deployment | Putting a model on a server so users can reach it. | [Video 9](09-mldlc/note.md) |
| Model drift / concept drift | A model's accuracy dropping as the real world changes; sometimes called model rot. | [Video 4](04-batch-learning/note.md) |
| Model selection | Training several algorithms and keeping the best. | [Video 13](13-toy-project/note.md) |
| Model training | Giving data to an algorithm so it learns the pattern. | [Video 9](09-mldlc/note.md) |
| Model | The logic produced by training, used to give outputs for new inputs. | [Video 1](01-what-is-ml/note.md) |
| Model-based learning | Learning a mathematical function from the data and predicting with it. | [Video 6](06-instance-vs-model-based/note.md) |
| monotonic_cst | Setting that forces predictions to only rise or only fall as a column grows. | [Video 111](111-random-forest-hyperparameters/note.md) |
| Monotonicity | Whether a column's values only go up, or only go down, from row to row. | [Video 22](22-pandas-profiling/note.md) |
| Most frequent value imputation (mode imputation) | Filling every gap in a column with its mode. | [Video 37](37-missing-categorical-data/note.md) |
| Multi-layer stacking | Stacking with more than one layer of base models below the meta-model. | [Video 127](127-stacking-blending/note.md) |
| Multicollinearity | A mathematical relationship between input columns, so that one can be calculated from the others. | [Video 27](27-one-hot-encoding/note.md) |
| Multinomial logistic regression | Another name for softmax regression. | [Video 79](79-softmax-regression/note.md) |
| MultinomialNB | Naive Bayes for count data, such as word counts. | [Video 90](90-gaussian-naive-bayes/note.md) |
| Multiple imputation | Making several filled copies of the data to see how unsure the fills are. | [Video 40](40-iterative-imputer-mice/note.md) |
| Multiple linear regression | Linear regression with several input columns. | [Video 50](50-simple-linear-regression/note.md) |
| Multivariate analysis | Studying more than two variables together. | [Video 20](20-univariate-analysis/note.md) |
| Multivariate imputation | Imputation that also uses the other columns. | [Video 35](35-complete-case-analysis/note.md) |
| Mutually exclusive events | Events that cannot happen at the same time; their intersection has probability 0. | [Video 84](84-mutually-exclusive-events/note.md) |
| n_bins | The `KBinsDiscretizer` parameter for the number of bins. | [Video 32](32-binning-binarization/note.md) |
| n_components | The number of principal components PCA keeps; a number between 0 and 1 means a share of the variance. | [Video 49](49-pca-mnist/note.md) |
| n_estimators (AdaBoost) | The maximum number of weak learners, one per boosting stage. | [Video 118](118-adaboost-hyperparameters/note.md) |
| n_estimators | The number of base models in an ensemble. | [Video 106](106-bagging-classifier/note.md) |
| n_init | How many times `KMeans` restarts from new centroids; the run with the lowest inertia is kept. | [Video 129](129-kmeans-code/note.md) |
| n_iter | The number of random combinations RandomizedSearchCV tries (default 10). | [Video 112](112-random-forest-tuning/note.md) |
| n_jobs | scikit-learn setting for how many CPU cores to use in parallel; -1 means all. | [Video 104](104-voting-regressor/note.md) |
| Naive assumption | The assumption that the inputs are conditionally independent given the class. | [Video 87](87-naive-bayes-intuition/note.md) |
| Naive Bayes classifier | A classifier that applies Bayes' theorem with the assumption that inputs are independent within each class. | [Video 87](87-naive-bayes-intuition/note.md) |
| Naive Bayes | A classification algorithm based on Bayes' theorem (later Notes). | [Video 82](82-conditional-probability/note.md) |
| named_steps | Dictionary of a pipeline's steps, from each name to its object. | [Video 29](29-pipelines/note.md) |
| nan-Euclidean distance | The Euclidean distance over the columns both rows have, scaled by (all columns / used columns). | [Video 39](39-knn-imputer/note.md) |
| Narrow AI | AI that does one specific task. All AI today is narrow. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| NaT | "Not a time": the missing value of a datetime column. | [Video 34](34-date-and-time/note.md) |
| Natural language processing (NLP) | The part of ML that works with human language. | [Video 8](08-applications-of-ml/note.md) |
| Nearest neighbours | The rows at the smallest distance from a given row. | [Video 39](39-knn-imputer/note.md) |
| Negative gradient | Minus the derivative of the loss with respect to the prediction; the direction that lowers the loss fastest. | [Video 121](121-gradient-boosting-regression-maths/note.md) |
| Negative hyperplane ($\pi^-$) | The copy of the separating hyperplane moved out until it touches the first negative point. | [Video 92](92-svm-intuition/note.md) |
| Neighbours | The k training points closest to the query point. | [Video 91](91-knn/note.md) |
| Neural network | The model DL uses, loosely inspired by neurons in the brain. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Newton step | Minimising a function by fitting a parabola from its first and second derivatives and jumping to the parabola's lowest point. | [Video 122](122-gradient-boosting-classification/note.md) |
| Node number | A node's index in the fitted tree, assigned depth-first starting from 0 at the root. | [Video 100](100-dtreeviz/note.md) |
| Node-level column sampling | Drawing a new random set of columns before every split (random forest). | [Video 110](110-bagging-vs-random-forest/note.md) |
| Noise (irreducible error) | Randomness in the data that no model can predict. | [Video 62](62-bias-variance/note.md) |
| Noise point | A point that is neither core nor border; DBSCAN labels it -1. | [Video 132](132-dbscan/note.md) |
| Nominal data | Categorical data whose categories have no order, such as states. | [Video 26](26-ordinal-label-encoding/note.md) |
| Non-closed-form solution | An answer reached by improving a guess step by step. | [Video 51](51-linear-regression-maths/note.md) |
| Non-linear data | Data whose classes no straight line, plane or hyperplane can separate. | [Video 95](95-kernel-trick-intuition/note.md) |
| Non-null | Not missing. | [Video 19](19-understanding-your-data/note.md) |
| Norm of a vector | The length of a vector, $\lVert w \rVert = \sqrt{w_1^2 + w_2^2 + \dots}$. | [Video 93](93-svm-maths/note.md) |
| Normal distribution | A symmetric, bell-shaped distribution. | [Video 20](20-univariate-analysis/note.md) |
| Normal equation | $\beta = (X^{\mathsf T}X)^{-1}X^{\mathsf T}y$: the closed-form solution of linear regression. | [Video 54](54-multiple-lr-maths/note.md) |
| Normal equations | $X^{\mathsf T}X\beta = X^{\mathsf T}y$: the conditions that the best coefficients satisfy. | [Video 54](54-multiple-lr-maths/note.md) |
| Normalisation (of weights) | Dividing every weight by their sum so they add up to 1. | [Video 116](116-adaboost-step-by-step/note.md) |
| Normalization | The type of feature scaling that squeezes values into a fixed range, such as 0 to 1. | [Video 25](25-normalization/note.md) |
| Normalized importances | Importances divided by their total, so they add up to 1. | [Video 114](114-feature-importance/note.md) |
| Notebook | A `.ipynb` file of cells, each with its output underneath. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| np.argmin | NumPy function returning the position of the smallest value. | [Video 130](130-kmeans-from-scratch/note.md) |
| np.concatenate | NumPy function that joins arrays; with `axis=1` it puts them side by side. | [Video 28](28-column-transformer/note.md) |
| np.insert | NumPy function that inserts values into an array at a given position. | [Video 55](55-multiple-lr-code/note.md) |
| np.linalg.inv | NumPy function that computes the inverse of a square matrix. | [Video 55](55-multiple-lr-code/note.md) |
| np.linalg.lstsq | NumPy function that finds the least-squares solution of a linear system. | [Video 55](55-multiple-lr-code/note.md) |
| Nullable integer (Int64) | The pandas integer type that can also hold a missing value, `<NA>`. | [Video 33](33-mixed-variables/note.md) |
| Nullity matrix | A picture of the whole table with missing values drawn as white lines. | [Video 22](22-pandas-profiling/note.md) |
| Numerical data | Data made of numbers. | [Video 3](03-types-of-ml/note.md) |
| Objective function | The quantity an algorithm tries to make as large or as small as possible. | [Video 48](48-pca-step-by-step/note.md) |
| Observation | The report's word for a row. | [Video 22](22-pandas-profiling/note.md) |
| Odds | How often an event happens divided by how often it does not, e.g. 5 placed to 3 not placed is $5/3$. | [Video 122](122-gradient-boosting-classification/note.md) |
| Offline learning | Another name for batch learning. | [Video 4](04-batch-learning/note.md) |
| OLTP | Online transaction processing: the database that records every action as it happens. | [Video 14](14-framing-ml-problem/note.md) |
| One-hot encoding | Replacing a nominal column by one 0/1 column per category, with a single 1 in each row; also used to represent words. | [Video 11](11-tensors/note.md) |
| One-vs-rest | Training one binary classifier per class, each separating that class from all others. | [Video 79](79-softmax-regression/note.md) |
| OneHotEncoder | scikit-learn's class for one-hot encoding; remembers the categories it learned. | [Video 27](27-one-hot-encoding/note.md) |
| Online learning | Training incrementally on mini-batches while the model is live in production. | [Video 5](05-online-learning/note.md) |
| OOB prediction | A row's prediction from only the trees whose bootstrap sample missed it. | [Video 113](113-oob-score/note.md) |
| oob_decision_function_ | Each training row's class probabilities from its OOB trees. | [Video 113](113-oob-score/note.md) |
| oob_prediction_ | Each training row's OOB prediction, for a regressor. | [Video 113](113-oob-score/note.md) |
| oob_score_ | The accuracy (classifier) or $R^2$ (regressor) of the OOB predictions. | [Video 113](113-oob-score/note.md) |
| OPTICS | Another density-based clustering algorithm. | [Video 132](132-dbscan/note.md) |
| Optimal number of features | The number of columns at which a model performs best. | [Video 46](46-curse-of-dimensionality/note.md) |
| Optimisation algorithm | A method for finding the parameter values that make a function as small (or large) as possible. | [Video 57](57-gradient-descent/note.md) |
| Ordinal data | Categorical data whose categories have a natural order, such as Poor < Average < Good. | [Video 26](26-ordinal-label-encoding/note.md) |
| Ordinal encoding | Replacing ordered categories by 0, 1, 2, ... in their order; for input columns. | [Video 26](26-ordinal-label-encoding/note.md) |
| OrdinalEncoder | scikit-learn's class for ordinal encoding; takes the order through `categories`. | [Video 26](26-ordinal-label-encoding/note.md) |
| Ordinary least squares (OLS) | The closed-form method for linear regression: the line with the smallest sum of squared errors. | [Video 51](51-linear-regression-maths/note.md) |
| Out-of-bag (OOB) evaluation | Testing a bagging model by predicting each training row with only the base models that never saw it. | [Video 113](113-oob-score/note.md) |
| Out-of-bag (OOB) score | The ensemble's accuracy measured on the rows each model never saw. | [Video 106](106-bagging-classifier/note.md) |
| Out-of-bag rows | The rows a base model never saw because its bootstrap sample missed them (about 37%). | [Video 105](105-bagging-intuition/note.md) |
| Out-of-core computing | Training on data bigger than the RAM by loading it chunk by chunk. | [Video 123](123-xgboost-intro/note.md) |
| Out-of-core learning | Training on data too big for memory by feeding it in chunks, offline. | [Video 5](05-online-learning/note.md) |
| Out-of-fold prediction | A prediction for a row made by a model trained on the other folds, never on that row. | [Video 127](127-stacking-blending/note.md) |
| Outlier detection | Setting a lower and an upper limit; values outside them are outliers. | [Video 41](41-what-are-outliers/note.md) |
| Outlier | A value far from the rest of the data. | [Video 20](20-univariate-analysis/note.md) |
| Outliers | Values far from the rest, often mistakes. | [Video 7](07-challenges-in-ml/note.md) |
| Output value (classification) | sum of residuals / ($\sum p(1-p) + \lambda$), in log-odds. | [Video 125](125-xgboost-classification/note.md) |
| Output value (leaf weight) | A leaf's prediction: sum of residuals / (number of residuals + $\lambda$). | [Video 124](124-xgboost-regression/note.md) |
| Overfitting | Learning the training data too closely, noise included; fails on new data. | [Video 7](07-challenges-in-ml/note.md) |
| Package manager | A program that downloads and installs libraries in versions that fit together. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| Package | A library packed for installation. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| Pair plot | A grid of scatter plots of every pair of numerical columns, with histograms on the diagonal. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Pandas Profiling | The library that builds a profiling report from a DataFrame, now named `fg-data-profiling`. | [Video 22](22-pandas-profiling/note.md) |
| pandas, DataFrame | Python's main table library, and its name for a table. | [Video 13](13-toy-project/note.md) |
| Parallel learning | Training the base models independently, so they can all be trained at once (bagging). | [Video 119](119-bagging-vs-boosting/note.md) |
| Parallel processing | Splitting one job among several processor cores working at the same time. | [Video 123](123-xgboost-intro/note.md) |
| Parameter grid | A dictionary of hyperparameter names and the values to try for each. | [Video 112](112-random-forest-tuning/note.md) |
| Parameter | A named setting passed to a function, like `sep=";"`. | [Video 15](15-working-with-csv/note.md) |
| Parameters | The numbers that describe a learned model, e.g. slope and intercept. | [Video 6](06-instance-vs-model-based/note.md) |
| Parse, parser | Read text and build a structure from it; the part that does this. | [Video 18](18-web-scraping/note.md) |
| Parser | The part of a program that reads text and splits it into pieces. | [Video 15](15-working-with-csv/note.md) |
| Partial derivative | The slope of a function of several variables in one variable, holding the others fixed. | [Video 51](51-linear-regression-maths/note.md) |
| partial_fit | A scikit-learn method that continues training from where the model left off. | [Video 5](05-online-learning/note.md) |
| passthrough | The `remainder` option that keeps untouched columns unchanged. | [Video 28](28-column-transformer/note.md) |
| Past defaulters | Past borrowers who did not repay their loan. | [Video 8](08-applications-of-ml/note.md) |
| Pasting | Bagging with rows sampled without replacement. | [Video 105](105-bagging-intuition/note.md) |
| Pattern | The relationship between input and output that the algorithm discovers. | [Video 1](01-what-is-ml/note.md) |
| PCA | Principal component analysis, a dimensionality reduction technique. | [Video 3](03-types-of-ml/note.md) |
| pd.crosstab | pandas function that counts how often each pair of values from two columns occurs. | [Video 89](89-naive-bayes-code/note.md) |
| pd.cut | The pandas function that puts values into intervals we give it. | [Video 32](32-binning-binarization/note.md) |
| pd.to_datetime | The pandas function that converts text to datetime values. | [Video 34](34-date-and-time/note.md) |
| pd.to_numeric | The pandas function that converts values to numbers. | [Video 33](33-mixed-variables/note.md) |
| Pearson correlation coefficient | The usual measure of correlation, written $r$; the one `df.corr()` computes. | [Video 19](19-understanding-your-data/note.md) |
| Pearson's r | The correlation coefficient for straight-line relationships between two numerical columns. | [Video 22](22-pandas-profiling/note.md) |
| penalty | SGDRegressor setting that adds a regularisation penalty, such as "l2" for Ridge. | [Video 65](65-ridge-gradient-descent/note.md) |
| penalty=None | LogisticRegression setting that switches regularisation off. | [Video 75](75-logistic-gradient-descent/note.md) |
| Per-row seed | A seed taken from a row's own values, so the same input always gets the same random fill. | [Video 38](38-missing-indicator-random-sample/note.md) |
| Percentile method (percentile rule) | Outlier detection that flags values below a low percentile or above a high one (e.g. 1st and 99th); for any column. | [Video 44](44-outliers-percentile/note.md) |
| Percentile | The value below which a given share of the data lies. | [Video 19](19-understanding-your-data/note.md) |
| Perceptron trick | Moving a line towards each misclassified point until the classes are separated. | [Video 70](70-perceptron-trick/note.md) |
| Perceptron | The smallest building block of a neural network; one artificial neuron. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Perfect separation | When a line splits the training classes with no mistakes; unregularised weights then grow without limit. | [Video 75](75-logistic-gradient-descent/note.md) |
| Performance metric | A number that measures how well a model works. | [Video 9](09-mldlc/note.md) |
| Permutation importance | The drop in a model's test score when one column's values are shuffled. | [Video 114](114-feature-importance/note.md) |
| permutation_importance | scikit-learn function (in `sklearn.inspection`) that computes permutation importance. | [Video 114](114-feature-importance/note.md) |
| phpMyAdmin | A web page for creating and managing MySQL databases. | [Video 16](16-working-with-json-and-sql/note.md) |
| pickle | A Python module that saves objects to a file and loads them back. | [Video 13](13-toy-project/note.md) |
| Pie chart | A circle split into slices sized by each category's share. | [Video 20](20-univariate-analysis/note.md) |
| pip | Python's own package manager, which installs from PyPI. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| Pipeline (class) | The scikit-learn class (in `sklearn.pipeline`) that builds a pipeline from a list of (name, object) tuples. | [Video 29](29-pipelines/note.md) |
| Pipeline | One object that bundles several processing steps and a model. | [Video 13](13-toy-project/note.md) |
| Pivot table | A grid with one column's values as rows, another's as columns, and a third in the cells. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Pixel | One dot of an image, stored as one or more numbers. | [Video 11](11-tensors/note.md) |
| Plane | A flat surface in 3D; the model for two input columns. | [Video 53](53-multiple-linear-regression/note.md) |
| Plateau | A nearly flat region of the loss, where steps become very small. | [Video 57](57-gradient-descent/note.md) |
| Policy | The agent's rules for which action to take. | [Video 3](03-types-of-ml/note.md) |
| Polynomial features | New input columns made from powers and products of the original inputs. | [Video 80](80-polynomial-logistic-regression/note.md) |
| Polynomial kernel | A kernel built from powers of the inputs, such as $x^2$. | [Video 95](95-kernel-trick-intuition/note.md) |
| Polynomial regression | Linear regression on powers (and products) of the inputs, to fit curves. | [Video 61](61-polynomial-regression/note.md) |
| PolynomialFeatures | scikit-learn transformer that creates the power and product columns. | [Video 61](61-polynomial-regression/note.md) |
| Positive and negative side | The two halves of the plane where Ax + By + C is above or below 0. | [Video 70](70-perceptron-trick/note.md) |
| Positive hyperplane ($\pi^+$) | The copy of the separating hyperplane moved out until it touches the first positive point. | [Video 92](92-svm-intuition/note.md) |
| Posterior | The probability of an event after the evidence is taken into account. | [Video 85](85-bayes-theorem/note.md) |
| Power transformer | A transform that raises each column to a learned power $\lambda$ to make it close to normal. | [Video 31](31-power-transformer/note.md) |
| PowerTransformer | scikit-learn's class for the Box-Cox and Yeo-Johnson transforms (next Note). | [Video 30](30-function-transformer/note.md) |
| Precision | Of all items predicted positive, the fraction that really are positive. | [Video 14](14-framing-ml-problem/note.md) |
| Predict | Use a trained model to give an answer for new data it has not seen. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| predict_proba | scikit-learn method that returns predicted probabilities instead of classes. | [Video 78](78-roc-auc/note.md) |
| Prediction ($\hat{y}$) | The value the model gives for an input; the hat marks a prediction. | [Video 51](51-linear-regression-maths/note.md) |
| Prediction path | The nodes a row passes through, from the root to the leaf that predicts it. | [Video 100](100-dtreeviz/note.md) |
| Predictive maintenance | Repairing a machine before it breaks, based on predicted faults. | [Video 8](08-applications-of-ml/note.md) |
| Preprocessing | Cleaning and preparing data before training. | [Video 13](13-toy-project/note.md) |
| Principal component analysis (PCA) | An unsupervised feature extraction technique that builds new columns along the directions of greatest variance. | [Video 47](47-pca-geometric-intuition/note.md) |
| Principal component | A new axis found by PCA; PC1 holds the most variance, PC2 the next most. | [Video 47](47-pca-geometric-intuition/note.md) |
| Prior | The probability of an event before any evidence is seen. | [Video 85](85-bayes-theorem/note.md) |
| Probabilistic interpretation | Reading the model's output as the probability of the positive class. | [Video 72](72-sigmoid-function/note.md) |
| Probability density function (PDF) | A curve showing how likely each value is; areas under it are probabilities. | [Video 20](20-univariate-analysis/note.md) |
| Probability density | The height of a continuous distribution's curve; compares how likely nearby values are. | [Video 90](90-gaussian-naive-bayes/note.md) |
| Probability tree | A diagram in which each path multiplies the probabilities along its branches. | [Video 86](86-bayes-problem/note.md) |
| Product rule for independent events | $P(A \cap B) = P(A) \times P(B)$. | [Video 83](83-independent-events/note.md) |
| Production code | The code that runs the deployed model on a server, for example behind a website. | [Video 29](29-pipelines/note.md) |
| Production environment | The server where a model serves real users. | [Video 4](04-batch-learning/note.md) |
| Profiling report | An automatic EDA report describing every column and pair of columns of a dataset. | [Video 22](22-pandas-profiling/note.md) |
| Program | Logic written by us that turns an input into an output. | [Video 1](01-what-is-ml/note.md) |
| Projection | Dropping each point onto an axis or line, like casting a shadow. | [Video 47](47-pca-geometric-intuition/note.md) |
| Proportional to (∝) | Equal up to a constant factor that is the same for every class. | [Video 88](88-naive-bayes-maths/note.md) |
| Proximity matrix | An n × n table of the distances between every pair of points or clusters. | [Video 131](131-hierarchical-clustering/note.md) |
| Pruning | Stopping a tree early or cutting it back so it does not overfit. | [Video 98](98-decision-tree-hyperparameters/note.md) |
| Pseudo-residual | The mistake on one row that the next tree learns; for squared error it is actual minus predicted. | [Video 120](120-gradient-boosting-intuition/note.md) |
| Pure leaf | A leaf whose training rows all belong to one class. | [Video 100](100-dtreeviz/note.md) |
| Push and pull | Moving the line away from a correctly classified point, or towards a misclassified one. | [Video 72](72-sigmoid-function/note.md) |
| PyPI | The Python Package Index, the public store of Python packages. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| Q-Q plot | A plot of a column's sorted values against the values a normal distribution would have; points on the line mean normal. | [Video 30](30-function-transformer/note.md) |
| QuantileTransformer | scikit-learn's third mathematical transformer, not covered in these Notes. | [Video 30](30-function-transformer/note.md) |
| Quarter | One of four three-month parts of a year. | [Video 34](34-date-and-time/note.md) |
| Quartiles | The 25%, 50% and 75% percentiles, which cut the data into four equal groups. | [Video 19](19-understanding-your-data/note.md) |
| Query parameters | Settings after the `?` in a URL, joined by `&`, such as `page=1`. | [Video 17](17-fetching-data-from-api/note.md) |
| Query point | The new point whose class we want to predict. | [Video 91](91-knn/note.md) |
| Query | A request for data, written in SQL. | [Video 16](16-working-with-json-and-sql/note.md) |
| Random forest | Bagging with decision trees as the base models. | [Video 101](101-ensemble-learning/note.md) |
| Random patches | Bagging in which each model gets random rows and random columns. | [Video 105](105-bagging-intuition/note.md) |
| Random sample imputation | Filling each gap with a value drawn at random from the column's known values. | [Video 38](38-missing-indicator-random-sample/note.md) |
| Random seed | A number that fixes a random number generator so that a run can be repeated exactly. | [Video 117](117-adaboost-from-scratch/note.md) |
| Random subspaces | Bagging in which each model gets all rows but a random subset of columns. | [Video 105](105-bagging-intuition/note.md) |
| RandomForestClassifier | scikit-learn's random forest for classification. | [Video 108](108-random-forest-intro/note.md) |
| RandomForestRegressor | scikit-learn's random forest for regression. | [Video 108](108-random-forest-intro/note.md) |
| RandomizedSearchCV | Tuning that cross-validates a fixed number of randomly drawn hyperparameter combinations. | [Video 99](99-regression-trees/note.md) |
| Rank | The number of axes of a tensor (ndim in NumPy). | [Video 11](11-tensors/note.md) |
| RapidAPI | A website listing many APIs, including free ones. | [Video 17](17-fetching-data-from-api/note.md) |
| Rate limit | The most requests an API accepts in a given time. | [Video 17](17-fetching-data-from-api/note.md) |
| Raw data | Data as it arrives, before any preparation. | [Video 23](23-what-is-feature-engineering/note.md) |
| Raw string | A Python string written `r"..."`, in which a backslash is kept as it is. | [Video 33](33-mixed-variables/note.md) |
| RBF kernel | Radial basis function kernel, built on $e^{-(\text{distance})^2}$; the most used SVM kernel. | [Video 95](95-kernel-trick-intuition/note.md) |
| Reader | What `read_csv` returns with `chunksize`: it hands out one chunk at a time. | [Video 15](15-working-with-csv/note.md) |
| Recall (sensitivity) | Of all items that really are positive, the fraction the model found. | [Video 14](14-framing-ml-problem/note.md) |
| Reciprocal transform | Replacing each value with $1/x$; reverses the order of the values. | [Video 30](30-function-transformer/note.md) |
| Recommendation engine | A model that suggests items, such as movies, to users. | [Video 4](04-batch-learning/note.md) |
| Reduced sample space | The outcomes that remain possible once the condition is known. | [Video 82](82-conditional-probability/note.md) |
| Reference category | The category whose dummy column is dropped; it is shown by all zeros. | [Video 27](27-one-hot-encoding/note.md) |
| Regression metric | A number that summarises how close a regression model's predictions are to the true values. | [Video 52](52-regression-metrics/note.md) |
| Regression tree | A decision tree whose leaves predict numbers: the mean output of their training rows. | [Video 99](99-regression-trees/note.md) |
| Regression | Supervised learning with a numerical output. | [Video 3](03-types-of-ml/note.md) |
| Regular expression | A short pattern that describes text, such as `\d+` for "one or more digits". | [Video 33](33-mixed-variables/note.md) |
| Regularisation term $\Omega$ | XGBoost's penalty on a tree: $\gamma T + \frac{1}{2}\lambda\sum_j w_j^2$. | [Video 126](126-xgboost-maths/note.md) |
| Regularisation | Penalising large coefficients to reduce a model's variance. | [Video 62](62-bias-variance/note.md) |
| Reinforcement learning | Learning by acting and receiving rewards or punishments. | [Video 3](03-types-of-ml/note.md) |
| Relative path | A file's location, starting from the folder the code runs in. | [Video 15](15-working-with-csv/note.md) |
| remainder | The `ColumnTransformer` parameter for untouched columns: `"drop"` (default) or `"passthrough"`. | [Video 28](28-column-transformer/note.md) |
| Representative sample | A sample that reflects the whole situation fairly. | [Video 7](07-challenges-in-ml/note.md) |
| Request, response | What we send to a server, and what it sends back. | [Video 18](18-web-scraping/note.md) |
| requests | Python library that sends web requests. | [Video 17](17-fetching-data-from-api/note.md) |
| Residual sum of squares | The total squared error of the model's predictions. | [Video 52](52-regression-metrics/note.md) |
| Residual | The error on one data point: actual minus predicted value. | [Video 56](56-linear-regression-assumptions/note.md) |
| Response | What `requests.get` returns: the status code plus the reply. | [Video 17](17-fetching-data-from-api/note.md) |
| Retrain | Train a model again, here from scratch on old + new data. | [Video 4](04-batch-learning/note.md) |
| Reward / punishment | Good / bad feedback after an action. | [Video 3](03-types-of-ml/note.md) |
| Ridge regression | Linear regression with a penalty on the sum of squared coefficients. | [Video 63](63-ridge-regression-intuition/note.md) |
| River | A Python library for online machine learning. | [Video 5](05-online-learning/note.md) |
| robots.txt | A file at a site's root listing what bots are asked not to visit. | [Video 18](18-web-scraping/note.md) |
| Robust scaling | Subtract the median and divide by the interquartile range; copes well with outliers. | [Video 25](25-normalization/note.md) |
| Robustness | Performing well even when the data changes somewhat. | [Video 101](101-ensemble-learning/note.md) |
| RobustScaler | scikit-learn's class for robust scaling. | [Video 25](25-normalization/note.md) |
| ROC curve | A plot of TPR against FPR for every threshold. | [Video 78](78-roc-auc/note.md) |
| Rollback | Restoring a model to an earlier, good version. | [Video 5](05-online-learning/note.md) |
| Root mean squared error (RMSE) | The square root of MSE, in the output's units. | [Video 52](52-regression-metrics/note.md) |
| Root node | The first node of a tree, holding all the training rows. | [Video 97](97-decision-trees-intuition/note.md) |
| Row sampling | Giving each base model a random subset of the rows. | [Video 108](108-random-forest-intro/note.md) |
| RPM | Revolutions per minute: how fast a motor turns. | [Video 8](08-applications-of-ml/note.md) |
| Runge's phenomenon | The large swings of a high-degree polynomial near the ends of the interval it is fitted on. | [Video 121](121-gradient-boosting-regression-maths/note.md) |
| R² score (coefficient of determination) | 1 minus the model's squared error divided by the squared error of always predicting the mean: 1 is perfect, 0 is no better than the average. | [Video 31](31-power-transformer/note.md) |
| Saddle point | A flat point that curves up in one direction and down in another. | [Video 57](57-gradient-descent/note.md) |
| saga | A stochastic solver that supports every penalty, including Elastic Net. | [Video 81](81-logistic-hyperparameters/note.md) |
| SAMME | The AdaBoost variant in scikit-learn: alpha without the factor 1/2, only misclassified rows reweighted; same decisions. | [Video 117](117-adaboost-from-scratch/note.md) |
| SAMME.R | An AdaBoost variant that used predicted probabilities; removed from scikit-learn. | [Video 118](118-adaboost-hyperparameters/note.md) |
| Sample space | The set of all possible outcomes of an experiment. | [Video 82](82-conditional-probability/note.md) |
| Sample weight | A number attached to each row saying how important it is; AdaBoost starts every row at 1/n. | [Video 116](116-adaboost-step-by-step/note.md) |
| Sample | The part of the real world that our data covers. | [Video 7](07-challenges-in-ml/note.md) |
| sample_weight | The argument of `fit` that tells a scikit-learn model how much each row counts. | [Video 117](117-adaboost-from-scratch/note.md) |
| Sampling bias | An unrepresentative sample caused by how the data was collected. | [Video 7](07-challenges-in-ml/note.md) |
| Sampling noise | An unrepresentative sample caused by being too small. | [Video 7](07-challenges-in-ml/note.md) |
| Scalar | A single number: a 0D tensor. | [Video 11](11-tensors/note.md) |
| Scaling | Bringing input columns to similar ranges. | [Video 13](13-toy-project/note.md) |
| Scatter plot | One dot per row, with one numerical column on each axis. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| scikit-learn | Python's main library for classical ML. | [Video 13](13-toy-project/note.md) |
| Score | Likelihood × prior for a class; proportional to the posterior. | [Video 87](87-naive-bayes-intuition/note.md) |
| SDLC | Software development life cycle: the standard process for building ordinary software. | [Video 9](09-mldlc/note.md) |
| SelectKBest | scikit-learn class that scores every column and keeps the `k` best. | [Video 29](29-pipelines/note.md) |
| Semester | One of two six-month halves of a year. | [Video 34](34-date-and-time/note.md) |
| Semi-supervised learning | Learning from a few labelled rows and many unlabelled ones. | [Video 3](03-types-of-ml/note.md) |
| Sentiment analysis | Deciding whether a text expresses a positive or negative opinion. | [Video 8](08-applications-of-ml/note.md) |
| Separator | The character between values on a line, such as `,` or a tab. | [Video 15](15-working-with-csv/note.md) |
| Sequential data | Data fed one piece after another, in order. | [Video 5](05-online-learning/note.md) |
| Sequential learning | Training the base models one after another, each depending on the previous ones (boosting). | [Video 119](119-bagging-vs-boosting/note.md) |
| Series | pandas' one-column structure: values with an index. | [Video 15](15-working-with-csv/note.md) |
| Server | A computer that is always on and that users reach over the internet. | [Video 4](04-batch-learning/note.md) |
| set_output | Method that makes a transformer return a pandas DataFrame with `transform="pandas"`. | [Video 28](28-column-transformer/note.md) |
| set_params | Method that changes a model's settings after it is created. | [Video 111](111-random-forest-hyperparameters/note.md) |
| SGDRegressor | A scikit-learn model that does linear regression step by step. | [Video 5](05-online-learning/note.md) |
| Shallow decision tree | A decision tree with a small maximum depth; high bias, low variance. | [Video 119](119-bagging-vs-boosting/note.md) |
| Shape | The number of items along each axis. | [Video 11](11-tensors/note.md) |
| Shapiro-Wilk test | A statistical test of whether data follows a normal distribution. | [Video 56](56-linear-regression-assumptions/note.md) |
| Shrinkage | The pulling of coefficients towards 0 by a penalty. | [Video 63](63-ridge-regression-intuition/note.md) |
| Shuffling | Putting the rows in a new random order before each epoch. | [Video 60](60-mini-batch-gradient-descent/note.md) |
| Sigmoid function | $\sigma(z) = 1/(1 + e^{-z})$; an S-shaped curve that maps any number into the range 0 to 1. | [Video 72](72-sigmoid-function/note.md) |
| Sigmoid kernel | The S-shaped kernel $\tanh(\gamma\, x \cdot x' + r)$. | [Video 95](95-kernel-trick-intuition/note.md) |
| Sign function | Returns +1 for a positive number and -1 for a negative one. | [Video 115](115-adaboost-intuition/note.md) |
| Similarity score (classification) | (sum of residuals)$^2$ / ($\sum p(1-p) + \lambda$), with $p$ the previous probabilities. | [Video 125](125-xgboost-classification/note.md) |
| Similarity score | (sum of residuals)$^2$ / (number of residuals + $\lambda$): how much a leaf's residuals agree. | [Video 124](124-xgboost-regression/note.md) |
| Similarity | How alike two data points are. | [Video 6](06-instance-vs-model-based/note.md) |
| Simple linear regression | Linear regression with one input column. | [Video 50](50-simple-linear-regression/note.md) |
| SimpleImputer | scikit-learn's class that fills missing values, by default with the column's mean. | [Video 28](28-column-transformer/note.md) |
| Simulated annealing | Lowering the learning rate gradually so the search settles down. | [Video 59](59-stochastic-gradient-descent/note.md) |
| Single linkage | Cluster distance = distance of the closest pair of points. | [Video 131](131-hierarchical-clustering/note.md) |
| Size | The total number of items: the product of the shape. | [Video 11](11-tensors/note.md) |
| Skewness | A number for how lopsided a distribution is: 0 symmetric, positive right tail, negative left tail. | [Video 20](20-univariate-analysis/note.md) |
| Slack (ξ) | How far a training point lies on the wrong side of its own hyperplane; 0 if it is on the correct side. | [Video 94](94-svm-soft-margin/note.md) |
| slice(0, 10) | Python object meaning positions 0 up to, not including, 10. | [Video 29](29-pipelines/note.md) |
| Slope | How much the output changes for one unit of change in the input; $m$ in $y = mx + b$. | [Video 50](50-simple-linear-regression/note.md) |
| Soft thresholding | Moving a value towards 0 by a fixed amount, and setting it to 0 if it would cross 0. | [Video 68](68-lasso-sparsity/note.md) |
| Soft voting | Predicting the class with the highest average predicted probability across the base models. | [Video 103](103-voting-classifier/note.md) |
| Soft-margin SVM | The SVM that allows points inside the margin or on the wrong side, at a cost controlled by C. | [Video 94](94-svm-soft-margin/note.md) |
| Softmax function | Turns a list of scores into probabilities: $e^{z_k} / \sum_j e^{z_j}$. | [Video 79](79-softmax-regression/note.md) |
| Softmax regression | Logistic regression extended to any number of classes using the softmax function. | [Video 79](79-softmax-regression/note.md) |
| Software integration | Building a model into the software that users use. | [Video 7](07-challenges-in-ml/note.md) |
| Solver | The method a model uses to find its best settings during training. | [Video 24](24-standardization/note.md) |
| Spam classifier | A program that decides whether an email is spam or not. | [Video 1](01-what-is-ml/note.md) |
| Sparse data | Two senses: a table that is mostly zeros (as after one-hot encoding); or, in many dimensions, a space where most regions hold no points. | [Video 25](25-normalization/note.md) |
| Sparse matrix | A table stored as only its non-zero entries, to save memory. | [Video 27](27-one-hot-encoding/note.md) |
| Sparse model | A model in which many coefficients are exactly 0. | [Video 67](67-lasso-regression/note.md) |
| sparse_output | `OneHotEncoder` parameter; `False` returns a normal NumPy array. | [Video 27](27-one-hot-encoding/note.md) |
| Sparsity | Having many coefficients exactly equal to 0. | [Video 68](68-lasso-sparsity/note.md) |
| Sparsity-aware split finding | Choosing, at each split, the side (left or right) for missing values by comparing the gain of both. | [Video 123](123-xgboost-intro/note.md) |
| splitter | "best" searches every threshold; "random" draws thresholds at random. | [Video 98](98-decision-tree-hyperparameters/note.md) |
| Splitting criterion (threshold) | The value a numerical question compares against, such as petal length $\le$ 2.45. | [Video 97](97-decision-trees-intuition/note.md) |
| Splitting | Dividing a node's rows into parts according to a question. | [Video 97](97-decision-trees-intuition/note.md) |
| Spyder | A Python code editor that shows variables and tables in memory. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| SQL (Structured Query Language) | The language for asking a database for data. | [Video 16](16-working-with-json-and-sql/note.md) |
| SQLAlchemy | A Python library that connects to many kinds of database; pandas supports it fully. | [Video 16](16-working-with-json-and-sql/note.md) |
| SQLite | A database stored in a single file, built into Python, needing no server. | [Video 16](16-working-with-json-and-sql/note.md) |
| Square root transform | Replacing each value with $\sqrt{x}$; a milder version of the log. | [Video 30](30-function-transformer/note.md) |
| Square transform | Replacing each value with $x^2$; used for left-skewed data. | [Video 30](30-function-transformer/note.md) |
| Square-root rule | A rough starting value for k: about $\sqrt{n}$, made odd. | [Video 91](91-knn/note.md) |
| squared_error | DecisionTreeRegressor's default criterion: split by mean squared error, leaves predict the mean. | [Video 99](99-regression-trees/note.md) |
| Stacking | An ensemble in which a meta-model learns how to weight the base models' outputs. | [Video 101](101-ensemble-learning/note.md) |
| Stage-wise additive model | A model built as a sum of base models added one at a time. | [Video 115](115-adaboost-intuition/note.md) |
| staged_score | A method that gives an ensemble's score after each added stage. | [Video 118](118-adaboost-hyperparameters/note.md) |
| Standard deviation | How far values typically lie from the mean; divide by $n - 1$ for a sample (pandas default) or by $n$ for a population (NumPy default). | [Video 19](19-understanding-your-data/note.md) |
| Standardization | Scaling a column to mean 0 and standard deviation 1. | [Video 13](13-toy-project/note.md) |
| standardize | The `PowerTransformer` parameter (on by default) that rescales the output to mean 0 and standard deviation 1. | [Video 31](31-power-transformer/note.md) |
| StandardScaler | scikit-learn's class that standardizes columns with `fit` and `transform`. | [Video 24](24-standardization/note.md) |
| Static model | A model that learns nothing new after deployment. | [Video 4](04-batch-learning/note.md) |
| statsmodels | A Python library for statistical models and tests. | [Video 56](56-linear-regression-assumptions/note.md) |
| Status code | A number saying how a request went: 200 OK, 401, 404, 500. | [Video 17](17-fetching-data-from-api/note.md) |
| Step function | A function that outputs 1 for positive inputs and 0 otherwise. | [Video 70](70-perceptron-trick/note.md) |
| step__parameter | How a pipeline step's parameter is named: step name, two underscores, parameter name. | [Video 29](29-pipelines/note.md) |
| Stochastic error | A random, unmeasurable influence that scatters data around its trend. | [Video 50](50-simple-linear-regression/note.md) |
| Stochastic gradient descent (SGD) | Gradient descent that uses one random row for every update. | [Video 58](58-batch-gradient-descent/note.md) |
| Stochastic | Involving randomness. | [Video 59](59-stochastic-gradient-descent/note.md) |
| str dtype | The pandas 3 type for text columns, replacing `object`. | [Video 33](33-mixed-variables/note.md) |
| str.extract | The pandas method that returns the part of each value matching a regular expression. | [Video 33](33-mixed-variables/note.md) |
| strategy | The `KBinsDiscretizer` parameter choosing uniform, quantile or kmeans. | [Video 32](32-binning-binarization/note.md) |
| Strike rate | A batter's runs per 100 balls faced. | [Video 45](45-feature-construction-splitting/note.md) |
| Strong learner | A model with high accuracy. | [Video 115](115-adaboost-intuition/note.md) |
| Structure score | The best objective of a tree, $-\frac{1}{2}\sum_j G_j^2/(H_j + \lambda) + \gamma T$; lower is better. | [Video 126](126-xgboost-maths/note.md) |
| Subscription | A model where customers pay a fixed amount every month (or year). | [Video 14](14-framing-ml-problem/note.md) |
| Sum of squared errors (SSE) | The sum of the squared residuals; a regression tree splits where the SSE of the two sides is smallest. | [Video 99](99-regression-trees/note.md) |
| Sum of squared errors | The squares of all the errors added up; the quantity the best-fit line makes smallest. | [Video 50](50-simple-linear-regression/note.md) |
| Supervised binning | Binning that also uses the target, such as decision tree binning. | [Video 32](32-binning-binarization/note.md) |
| Supervised learning | Learning from data with inputs and outputs, to predict outputs. | [Video 3](03-types-of-ml/note.md) |
| Supervision | Correct answers that guide an algorithm while it learns. | [Video 3](03-types-of-ml/note.md) |
| Support vector machine (SVM) | A classifier that separates the classes with the hyperplane that has the widest margin. | [Video 92](92-svm-intuition/note.md) |
| Support vector regression (SVR) | The regression version of SVM. | [Video 92](92-svm-intuition/note.md) |
| Support vectors | The training points that lie on $\pi^+$ or $\pi^-$; they alone fix the SVM line. | [Video 92](92-svm-intuition/note.md) |
| Support | The number of items that really belong to a class. | [Video 77](77-precision-recall-f1/note.md) |
| Surge pricing | Raising fares when demand is much higher than supply. | [Video 8](08-applications-of-ml/note.md) |
| Symbolic AI | Early AI where humans write the knowledge as rules. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Tag | One element of HTML, such as `<h2>TCS</h2>`. | [Video 18](18-web-scraping/note.md) |
| Target leakage | Building an input column from the answer itself, so the model sees information it would not have in real use. | [Video 52](52-regression-metrics/note.md) |
| Target, label | Other names for the output column. | [Video 3](03-types-of-ml/note.md) |
| Targeted marketing | Advertising only to the people most likely to buy. | [Video 8](08-applications-of-ml/note.md) |
| Taylor series | Approximation of a function near a point by a polynomial built from its derivatives there. | [Video 126](126-xgboost-maths/note.md) |
| Tensor | A container of numbers arranged along one or more axes. | [Video 11](11-tensors/note.md) |
| Terminal region | The part of the input space that ends in one leaf of a tree, written $R_{jm}$ for leaf $j$ of tree $m$. | [Video 121](121-gradient-boosting-regression-maths/note.md) |
| Test set | The part hidden during training, used to check the model. | [Video 13](13-toy-project/note.md) |
| Theoretical quantile | Where a value would sit if the data were perfectly normal (the horizontal axis of a Q-Q plot). | [Video 30](30-function-transformer/note.md) |
| Threshold | The value that separates 0 from 1 in binarization. | [Video 32](32-binning-binarization/note.md) |
| Tidy data | Data with one observation per row and one atomic value per cell. | [Video 45](45-feature-construction-splitting/note.md) |
| Time series | Data recorded at regular time intervals. | [Video 11](11-tensors/note.md) |
| Timedelta | A length of time, the result of subtracting two datetimes. | [Video 34](34-date-and-time/note.md) |
| Timestamp | pandas' type for a single point in time. | [Video 34](34-date-and-time/note.md) |
| Title | The word before a name, such as Mr, Mrs, Miss or Master. | [Video 45](45-feature-construction-splitting/note.md) |
| Top categories | Keeping only the most frequent categories and merging the rest into one "uncommon" category. | [Video 27](27-one-hot-encoding/note.md) |
| Total sum of squares | The total squared error of always predicting the mean. | [Video 52](52-regression-metrics/note.md) |
| TPU | Google's chip built only for deep learning maths. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| Train | Let a model learn by making predictions, measuring its errors and adjusting to reduce them. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Train-test split | Dividing the data into training and test sets. | [Video 13](13-toy-project/note.md) |
| Training set | The part of the data the model learns from. | [Video 13](13-toy-project/note.md) |
| Training | The step in which an algorithm learns the pattern from data. | [Video 1](01-what-is-ml/note.md) |
| transformers | The `ColumnTransformer` parameter: a list of (name, transformer, columns) tuples. | [Video 28](28-column-transformer/note.md) |
| transformers_ | List of a fitted column transformer's (name, transformer, columns) tuples. | [Video 29](29-pipelines/note.md) |
| Transpose | A matrix or vector with rows and columns swapped. | [Video 48](48-pca-step-by-step/note.md) |
| Tree-based algorithm | An algorithm that splits the data with simple conditions; hardly affected by outliers. | [Video 41](41-what-are-outliers/note.md) |
| Tree-level column sampling | Drawing one random set of columns per tree, before the tree is grown; every split of that tree uses only those columns (bagging). | [Video 110](110-bagging-vs-random-forest/note.md) |
| Trimming | Removing the rows that hold outliers. | [Video 41](41-what-are-outliers/note.md) |
| True negative (TN) | Predicted negative, and actually negative. | [Video 76](76-accuracy-confusion-matrix/note.md) |
| True positive (TP) | Predicted positive, and actually positive. | [Video 76](76-accuracy-confusion-matrix/note.md) |
| True positive rate (TPR) | The fraction of real positives the model flags; the same as recall. | [Video 78](78-roc-auc/note.md) |
| TSV file | Like a CSV file, with tabs between values. | [Video 15](15-working-with-csv/note.md) |
| Type 1 mixed variable | A column whose cells each contain a category and a number together, such as `C85`. | [Video 33](33-mixed-variables/note.md) |
| Type 2 mixed variable | A column with a number in some rows and a category in others. | [Video 33](33-mixed-variables/note.md) |
| Underfitting | Being too simple to capture the pattern; fails on all data. | [Video 7](07-challenges-in-ml/note.md) |
| Underflow | A number too close to 0 for the computer to store, which then becomes 0 or loses precision. | [Video 73](73-log-loss/note.md) |
| Understanding the data | The project stage where we learn what is in the data before cleaning or modelling. | [Video 19](19-understanding-your-data/note.md) |
| Uniform weighting | Every neighbour counts equally: the fill is their plain mean. | [Video 39](39-knn-imputer/note.md) |
| Union (A ∪ B) | The event that A or B (or both) happens. | [Video 84](84-mutually-exclusive-events/note.md) |
| Unit hypercube | The same box in three or more dimensions (a unit cube in three). | [Video 25](25-normalization/note.md) |
| Unit square | The square from (0, 0) to (1, 1), into which min-max scaling presses two columns. | [Video 25](25-normalization/note.md) |
| Unit vector | A vector of length 1, used to describe a direction. | [Video 48](48-pca-step-by-step/note.md) |
| Univariate analysis | Studying one variable on its own. | [Video 20](20-univariate-analysis/note.md) |
| Univariate imputation | Imputation that uses only the column with the gap. | [Video 35](35-complete-case-analysis/note.md) |
| Unreasonable effectiveness of data | With enough data, different algorithms perform about the same. | [Video 7](07-challenges-in-ml/note.md) |
| Unsupervised binning | Binning that uses only the column's own values. | [Video 32](32-binning-binarization/note.md) |
| Unsupervised learning | Learning from inputs only, to find structure. | [Video 3](03-types-of-ml/note.md) |
| Upper / lower limit | $\mu + 3\sigma$ and $\mu - 3\sigma$; values beyond them are outliers. | [Video 42](42-outliers-zscore/note.md) |
| Upsampling (resampling by weight) | Drawing a new dataset in which each row is picked with probability equal to its weight. | [Video 116](116-adaboost-step-by-step/note.md) |
| User-Agent | A short text a browser sends to say what it is. | [Video 15](15-working-with-csv/note.md) |
| UTF-8 | The most common encoding, and `read_csv`'s default. | [Video 15](15-working-with-csv/note.md) |
| Validation set | Data held back from training to check and tune a model before the final test. | [Video 113](113-oob-score/note.md) |
| Vanishing gradient | Gradients shrinking towards 0 as they pass through many layers, which slows learning. | [Video 74](74-sigmoid-derivative/note.md) |
| Variable | One column of a dataset. | [Video 20](20-univariate-analysis/note.md) |
| Variance (of a model) | How much a model's predictions change when it is trained on a different sample of the data; a different meaning from the variance of a column. | [Video 62](62-bias-variance/note.md) |
| Variance (of data) | The average squared distance of the values from their mean; the square of the standard deviation; divide by $n$ for a population (NumPy default) or $n - 1$ for a sample (pandas default). | [Video 47](47-pca-geometric-intuition/note.md) |
| Variance inflation factor (VIF) | $1 / (1 - R_j^2)$: how well the other inputs predict input $j$; above 5 signals multicollinearity. | [Video 56](56-linear-regression-assumptions/note.md) |
| Variance reduction | The drop in mean squared error from a node to its children; the regression version of information gain. | [Video 99](99-regression-trees/note.md) |
| Vector | A list of numbers: a 1D tensor. | [Video 11](11-tensors/note.md) |
| Vectorisation | Writing a computation as operations on whole arrays instead of Python loops. | [Video 58](58-batch-gradient-descent/note.md) |
| Vectorization | Converting data such as text into vectors of numbers. | [Video 11](11-tensors/note.md) |
| verbose | scikit-learn setting that prints progress messages during training. | [Video 106](106-bagging-classifier/note.md) |
| View Page Source | Browser option that shows a page's raw HTML. | [Video 18](18-web-scraping/note.md) |
| Virtual environment | A separate folder of Python and packages for one project. | [Video 12](12-setup-anaconda-jupyter-colab/note.md) |
| Vocabulary | The list of unique words in a set of texts. | [Video 11](11-tensors/note.md) |
| Volatile | Changing quickly and unpredictably. | [Video 14](14-framing-ml-problem/note.md) |
| Voting classifier | A classifier that combines several trained classifiers by voting. | [Video 103](103-voting-classifier/note.md) |
| Voting ensemble | Several models trained on the same data, combined by majority vote (classification) or mean (regression). | [Video 102](102-voting-ensemble/note.md) |
| Voting regressor | A regressor that predicts the mean (or weighted mean) of several trained regressors' predictions. | [Video 104](104-voting-regressor/note.md) |
| Vowpal Wabbit | A fast learning library that supports online learning. | [Video 5](05-online-learning/note.md) |
| Ward linkage | Cluster distance = increase in total squared distance to the centroids caused by merging. | [Video 131](131-hierarchical-clustering/note.md) |
| warm_start | Setting that keeps already-trained trees and adds new ones on the next fit. | [Video 111](111-random-forest-hyperparameters/note.md) |
| Wayback Machine | A web archive that keeps copies of web pages as they were. | [Video 18](18-web-scraping/note.md) |
| WCSS (inertia) | Within-cluster sum of squares: the sum of squared distances from each point to its own centroid. | [Video 128](128-kmeans-intuition/note.md) |
| Weak learner | A model whose accuracy is only a little better than random guessing. | [Video 115](115-adaboost-intuition/note.md) |
| Web scraping | Writing code that extracts data from web pages. | [Video 7](07-challenges-in-ml/note.md) |
| Weight decay | Another name for the L2 penalty: each gradient step shrinks the coefficients by a fixed factor. | [Video 65](65-ridge-gradient-descent/note.md) |
| Weight update | Multiplying misclassified rows' weights by $e^{\alpha}$ and correct rows' weights by $e^{-\alpha}$. | [Video 116](116-adaboost-step-by-step/note.md) |
| Weight-based algorithm | An algorithm that learns one number per input column from all the points; sensitive to outliers. | [Video 41](41-what-are-outliers/note.md) |
| Weighted average | The mean of a metric over classes, weighted by each class's support. | [Video 77](77-precision-recall-f1/note.md) |
| Weighted error | The total sample weight of the rows a model misclassifies. | [Video 116](116-adaboost-step-by-step/note.md) |
| Weighted impurity decrease | A split's impurity drop, weighted by the share of rows reaching the node: the $\Delta$ of `min_impurity_decrease`. | [Video 114](114-feature-importance/note.md) |
| Weighted quantile sketch | XGBoost's method for placing bin edges at (Hessian-weighted) quantiles of a column. | [Video 123](123-xgboost-intro/note.md) |
| weights | VotingClassifier and VotingRegressor setting that gives each base model's vote a different importance. | [Video 103](103-voting-classifier/note.md) |
| Winsorization | Capping with limits set by percentiles. | [Video 41](41-what-are-outliers/note.md) |
| Wisdom of the crowd | The combined judgement of many is often more accurate than any one member's. | [Video 101](101-ensemble-learning/note.md) |
| With replacement | Sampling in which each drawn item is put back, so it can be drawn again. | [Video 105](105-bagging-intuition/note.md) |
| X, y | Usual names for the input table and the output column. | [Video 11](11-tensors/note.md) |
| XAMPP | A free package that runs a web server and a MySQL server on one computer. | [Video 16](16-working-with-json-and-sql/note.md) |
| XGBoost | eXtreme Gradient Boosting: a library that implements gradient boosting with many speed and accuracy optimisations. | [Video 123](123-xgboost-intro/note.md) |
| Yeo-Johnson transform | A variation of Box-Cox that also works on zero and negative values; scikit-learn's default. | [Video 31](31-power-transformer/note.md) |
| Z-score method | Outlier detection that flags values more than 3 standard deviations from the mean; for roughly normal columns. | [Video 42](42-outliers-zscore/note.md) |
| Z-score normalization | Another name for standardization. | [Video 24](24-standardization/note.md) |
| Z-score | A value after standardization: how many standard deviations it lies from the mean. | [Video 24](24-standardization/note.md) |
| Zero-frequency problem | A probability of 0 for a value never seen with a class, which forces that class's score to 0. | [Video 89](89-naive-bayes-code/note.md) |
| λ (lambda), alpha | The strength of the regularisation penalty; alpha in scikit-learn. | [Video 63](63-ridge-regression-intuition/note.md) |
