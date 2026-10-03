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
| `BayesianRidge` | A linear regression with built-in shrinkage of the weights; the default model of `IterativeImputer`. | [Video 40](40-iterative-imputer-mice/note.md) |
| `best_params_` | The best combination of settings found by `GridSearchCV`. | [Video 38](38-missing-indicator-random-sample/note.md) |
| `clip` | pandas method that moves every value below a lower bound up to it and every value above an upper bound down to it. | [Video 44](44-outliers-percentile/note.md) |
| `cv_results_` | The scores of every combination tried by `GridSearchCV`. | [Video 38](38-missing-indicator-random-sample/note.md) |
| `enable_iterative_imputer` | The import that switches on the experimental `IterativeImputer`. | [Video 40](40-iterative-imputer-mice/note.md) |
| `fill_value` | The value `SimpleImputer` uses with `strategy="constant"`. | [Video 36](36-imputing-numerical-data/note.md) |
| `fillna` | The pandas method that replaces every `NaN` with a given value. | [Video 36](36-imputing-numerical-data/note.md) |
| `find`, `find_all` | Return the first matching tag, or a list of all matching tags. | [Video 18](18-web-scraping/note.md) |
| `GridSearchCV` | The scikit-learn class that runs a grid search with cross-validation. | [Video 38](38-missing-indicator-random-sample/note.md) |
| `ignore_index` | Setting of `pd.concat` that renumbers the joined rows from 0. | [Video 17](17-fetching-data-from-api/note.md) |
| `IterativeImputer` | scikit-learn's class for MICE; still experimental. | [Video 40](40-iterative-imputer-mice/note.md) |
| `json_normalize` | pandas function that turns nested JSON into flat columns. | [Video 17](17-fetching-data-from-api/note.md) |
| `KNNImputer` | scikit-learn's class for KNN imputation. | [Video 39](39-knn-imputer/note.md) |
| `max_iter` | The largest number of iterations `IterativeImputer` runs; default 10. | [Video 40](40-iterative-imputer-mice/note.md) |
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
| `step__param` name | The full name of a setting inside a pipeline: step names and the parameter joined by `__`. | [Video 38](38-missing-indicator-random-sample/note.md) |
| `strategy="constant"` | The `SimpleImputer` setting that fills every gap with `fill_value`. | [Video 37](37-missing-categorical-data/note.md) |
| `strategy="most_frequent"` | The `SimpleImputer` setting for mode imputation. | [Video 37](37-missing-categorical-data/note.md) |
| `strategy` | The `SimpleImputer` parameter choosing the fill rule: mean, median, most_frequent or constant. | [Video 36](36-imputing-numerical-data/note.md) |
| `tol` | The size of change below which `IterativeImputer` stops early; default 0.001. | [Video 40](40-iterative-imputer-mice/note.md) |
| Absolute value | A number's size without its sign. | [Video 25](25-normalization/note.md) |
| Accuracy | The fraction of predictions that are correct. | [Video 13](13-toy-project/note.md) |
| Adjusted R² | R² with a penalty for the number of input columns. | [Video 52](52-regression-metrics/note.md) |
| Agent | The learner in reinforcement learning. | [Video 3](03-types-of-ml/note.md) |
| AGI (artificial general intelligence) | A machine with all the abilities of human intelligence. Does not exist yet. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Alert | A warning in the report about a column that may need attention. | [Video 22](22-pandas-profiling/note.md) |
| Anomaly detection | Finding rows that do not fit the pattern of the rest. | [Video 3](03-types-of-ml/note.md) |
| API (Application Programming Interface) | A way for two programs to talk; a website's API hands out its data on request. | [Video 17](17-fetching-data-from-api/note.md) |
| API key | A secret code that tells the API who is asking. | [Video 17](17-fetching-data-from-api/note.md) |
| API | A service that returns data when our code asks for it. | [Video 7](07-challenges-in-ml/note.md) |
| Arbitrary value imputation | Filling every gap with one fixed value that never occurs, such as 99 or $-1$. | [Video 36](36-imputing-numerical-data/note.md) |
| Array | The programming name for a tensor (as in NumPy). | [Video 11](11-tensors/note.md) |
| Artificial Intelligence (AI) | The field of building machines that show intelligence. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Association rule learning | Finding items that tend to occur together. | [Video 3](03-types-of-ml/note.md) |
| Assumption (of a model) | A condition the data must meet for the model's results to be reliable. | [Video 56](56-linear-regression-assumptions/note.md) |
| Atomic value | A single piece of information in a cell, not several combined. | [Video 45](45-feature-construction-splitting/note.md) |
| Attribute | A `name="value"` setting inside an opening tag. | [Video 18](18-web-scraping/note.md) |
| Autocorrelation | Each residual is related to the one before it in row order. | [Video 56](56-linear-regression-assumptions/note.md) |
| Average record size | The memory one row takes, on average. | [Video 22](22-pandas-profiling/note.md) |
| Axis | One direction along which a tensor's items are arranged. | [Video 11](11-tensors/note.md) |
| Backward elimination | Feature selection that starts with all columns and removes the worst at a time. | [Video 46](46-curse-of-dimensionality/note.md) |
| Bar plot | One bar per category, its height the mean of a numerical column. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Batch (mini-batch) | A small group of training rows used for one update. | [Video 60](60-mini-batch-gradient-descent/note.md) |
| Batch gradient descent | Gradient descent that uses all training rows for every update. | [Video 58](58-batch-gradient-descent/note.md) |
| Batch learning | Training on the whole dataset at once, offline, then deploying. | [Video 4](04-batch-learning/note.md) |
| Batch size | The number of rows in each batch; a hyperparameter. | [Video 60](60-mini-batch-gradient-descent/note.md) |
| BeautifulSoup | Python library that parses HTML into a searchable tree. | [Video 18](18-web-scraping/note.md) |
| Bell curve | The curve of a normal distribution. | [Video 42](42-outliers-zscore/note.md) |
| Best-fit line | The line with the smallest total error over all the training points. | [Video 50](50-simple-linear-regression/note.md) |
| Biased model | A model pushed towards wrong answers, e.g. by bad data. | [Video 5](05-online-learning/note.md) |
| Bimodal | A distribution with two peaks. | [Video 31](31-power-transformer/note.md) |
| Bin edge | A boundary between two neighbouring bins. | [Video 32](32-binning-binarization/note.md) |
| Bin | One of the equal ranges a histogram splits the data into. | [Video 20](20-univariate-analysis/note.md) |
| bin_edges_ | The fitted `KBinsDiscretizer` attribute holding the learned edges. | [Video 32](32-binning-binarization/note.md) |
| Binarization | Turning a continuous column into 0 or 1 by comparing it with one threshold. | [Video 32](32-binning-binarization/note.md) |
| Binarizer | scikit-learn's class for binarization, with parameters `threshold` and `copy`. | [Video 32](32-binning-binarization/note.md) |
| Binning | Grouping a numerical column into ranges that act as categories. | [Video 23](23-what-is-feature-engineering/note.md) |
| Bivariate analysis | Studying two variables together. | [Video 20](20-univariate-analysis/note.md) |
| BMI | Body mass index: weight (kg) divided by height (m) squared. | [Video 7](07-challenges-in-ml/note.md) |
| Bot | A program that visits websites automatically. | [Video 18](18-web-scraping/note.md) |
| Box plot | A graph of the five-number summary, with outliers drawn as dots. | [Video 20](20-univariate-analysis/note.md) |
| Box-Cox transform | $(x^\lambda - 1)/\lambda$, or $\ln x$ when $\lambda = 0$; works only on values above 0. | [Video 31](31-power-transformer/note.md) |
| Capping | Replacing every value beyond a limit with the limit itself. | [Video 41](41-what-are-outliers/note.md) |
| Categorical column | A column whose values are labels rather than numbers. | [Video 23](23-what-is-feature-engineering/note.md) |
| Categorical data | Data made of categories. | [Video 3](03-types-of-ml/note.md) |
| categories_ | The attribute holding the categories `OrdinalEncoder` learned, in order. | [Video 26](26-ordinal-label-encoding/note.md) |
| Category share | The rows in one category divided by the rows that have a value. | [Video 37](37-missing-categorical-data/note.md) |
| Category | One of the fixed groups of a categorical column. | [Video 20](20-univariate-analysis/note.md) |
| Centred data | Data whose mean is 0. | [Video 25](25-normalization/note.md) |
| Centroid | The centre of one group in k-means. | [Video 32](32-binning-binarization/note.md) |
| Chained assignment | Selecting part of a DataFrame and then changing that selection in a second step; does nothing in pandas 3. | [Video 45](45-feature-construction-splitting/note.md) |
| Chained equations | One prediction model per column, each using the latest fills of the others. | [Video 40](40-iterative-imputer-mice/note.md) |
| Channel | One colour layer of an image (red, green or blue). | [Video 11](11-tensors/note.md) |
| Chi-squared test (chi2) | A test scoring how strongly a column is linked to the target; needs values of 0 or more. | [Video 29](29-pipelines/note.md) |
| Chunk | A piece of a file, read as a small DataFrame. | [Video 15](15-working-with-csv/note.md) |
| Class | An attribute that labels tags; used to select the right ones. | [Video 18](18-web-scraping/note.md) |
| classes_ | The attribute holding the classes `LabelEncoder` learned, in order. | [Video 26](26-ordinal-label-encoding/note.md) |
| Classification | Supervised learning with a categorical output. | [Video 3](03-types-of-ml/note.md) |
| Client, server | The program that asks, and the computer that answers. | [Video 17](17-fetching-data-from-api/note.md) |
| Closed-form solution | An answer given directly by a formula of ordinary operations. | [Video 51](51-linear-regression-maths/note.md) |
| Cluster | One group found by clustering. | [Video 3](03-types-of-ml/note.md) |
| Clustering | Splitting data into groups of similar rows. | [Video 3](03-types-of-ml/note.md) |
| Clustermap | A heatmap with rows and columns reordered so similar ones sit together. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| coef_ | The fitted slope (one per input column) in scikit-learn. | [Video 50](50-simple-linear-regression/note.md) |
| Coefficient ($\beta_i$) | The weight of one input column: the change in the output per unit of that input, others fixed. | [Video 53](53-multiple-linear-regression/note.md) |
| Coefficient of variation (CV) | Standard deviation divided by mean: spread relative to the average. | [Video 22](22-pandas-profiling/note.md) |
| Coefficient vector ($\beta$) | All the coefficients of the model, $\beta_0$ to $\beta_m$, as one column. | [Video 54](54-multiple-lr-maths/note.md) |
| Column transformer | A scikit-learn class that applies different transformations to different columns at once (covered two Notes later). | [Video 26](26-ordinal-label-encoding/note.md) |
| ColumnTransformer | The scikit-learn class (in `sklearn.compose`) that implements the column transformer. | [Video 28](28-column-transformer/note.md) |
| Complete case analysis (CCA) | Dropping every row that has a missing value in any chosen column; also called listwise deletion. | [Video 35](35-complete-case-analysis/note.md) |
| Complete case | A row with a value in every column used. | [Video 35](35-complete-case-analysis/note.md) |
| components_ | The eigenvectors of the fitted PCA, one per row. | [Video 49](49-pca-mnist/note.md) |
| Compression | Storing data in less space. | [Video 11](11-tensors/note.md) |
| Confidence interval | A range in which the true mean most likely lies. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Connection object | The open link to a database (`conn`) that queries go through. | [Video 16](16-working-with-json-and-sql/note.md) |
| Connector | A library that lets Python talk to a database. | [Video 16](16-working-with-json-and-sql/note.md) |
| Container | A tag (often a `div`) that holds everything about one item, such as one company. | [Video 18](18-web-scraping/note.md) |
| Contour plot | A map of a surface seen from above, with lines joining points of equal height. | [Video 57](57-gradient-descent/note.md) |
| Converge | To settle at a minimum, with steps becoming negligible. | [Video 57](57-gradient-descent/note.md) |
| Convergence | The point where the fills hardly change between two iterations. | [Video 40](40-iterative-imputer-mice/note.md) |
| Convex function | A function where a straight line between any two points of its curve never goes below the curve; it has a single minimum. | [Video 57](57-gradient-descent/note.md) |
| Correlation | How two columns move together, from -1 to +1. | [Video 19](19-understanding-your-data/note.md) |
| Count plot | A bar chart with one bar per category, as tall as its frequency. | [Video 20](20-univariate-analysis/note.md) |
| Covariance matrix | A square table of all variances (diagonal) and covariances (off-diagonal) of the columns. | [Video 48](48-pca-step-by-step/note.md) |
| Covariance | How two columns move together: positive if they rise together, negative if not. | [Video 48](48-pca-step-by-step/note.md) |
| Cramér's V | A measure of the link between two categorical columns, from 0 to 1. | [Video 22](22-pandas-profiling/note.md) |
| Cross-validation | Testing a model by training and testing it several times on different parts of the training data. | [Video 29](29-pipelines/note.md) |
| Crosstab | A table counting the rows for every pair of categories of two columns. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| CSV file | A text file holding a table, with commas between values. | [Video 13](13-toy-project/note.md) |
| Cumulative explained variance | The share of the variance kept by the first k components together. | [Video 49](49-pca-mnist/note.md) |
| Curse of dimensionality | The problems that appear when data has too many dimensions: lower performance and more computation. | [Video 46](46-curse-of-dimensionality/note.md) |
| Custom binning | Binning with edges we choose from domain knowledge; also called domain-based binning. | [Video 32](32-binning-binarization/note.md) |
| Cut-offs | The two percentiles chosen as limits, such as 1 and 99 or 5 and 95. | [Video 44](44-outliers-percentile/note.md) |
| Data cleaning | Fixing errors, gaps and inconsistencies in data. | [Video 7](07-challenges-in-ml/note.md) |
| Data leakage | Information from the test set leaking into training. | [Video 13](13-toy-project/note.md) |
| Data pipeline | A channel that carries data from one point to another. | [Video 17](17-fetching-data-from-api/note.md) |
| Data type (dtype) | The kind of values a column holds, such as `int64`, `float64` or `str`. | [Video 19](19-understanding-your-data/note.md) |
| Database server | A program that holds databases and answers queries, such as MySQL. | [Video 16](16-working-with-json-and-sql/note.md) |
| Database | A program that stores data as tables and answers queries. | [Video 16](16-working-with-json-and-sql/note.md) |
| Datetime | A value pandas understands as a point in time, with date and time parts. | [Video 34](34-date-and-time/note.md) |
| datetime64 | The pandas column type for datetimes; `[us]` means microsecond resolution. | [Video 34](34-date-and-time/note.md) |
| Day of week | The weekday as a number, Monday = 0 to Sunday = 6 (`.dt.dayofweek`). | [Video 34](34-date-and-time/note.md) |
| Decision boundary | A line or curve that separates the classes in classification. | [Video 6](06-instance-vs-model-based/note.md) |
| Deep Learning (DL) | Machine Learning that uses neural networks with many layers; finds features by itself. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Dendrogram | A tree showing which rows (or columns) were joined as similar, and in what order. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Density plot | A histogram with a smooth KDE curve on top. | [Video 20](20-univariate-analysis/note.md) |
| Dependent variable | The output column (y). | [Video 13](13-toy-project/note.md) |
| Deploy | Move a model from development to production. | [Video 4](04-batch-learning/note.md) |
| Deployment | Putting a model on a server so users can reach it. | [Video 7](07-challenges-in-ml/note.md) |
| Derivative | The slope of a function at a point. | [Video 51](51-linear-regression-maths/note.md) |
| Descriptive statistics | Numbers that summarise data, such as count, mean, spread and percentiles. | [Video 19](19-understanding-your-data/note.md) |
| Design matrix ($X$) | The data as a matrix, one row per data point, with a first column of 1s for the intercept. | [Video 54](54-multiple-lr-maths/note.md) |
| Development environment | Our own machine, where we build and train a model. | [Video 4](04-batch-learning/note.md) |
| Diabetes dataset | scikit-learn's built-in data of 442 patients, 10 standardised inputs, and disease progression one year later. | [Video 55](55-multiple-lr-code/note.md) |
| Dimension | One input column. | [Video 3](03-types-of-ml/note.md) |
| Dimensionality reduction | Reducing the number of input columns while keeping the information. | [Video 3](03-types-of-ml/note.md) |
| Dimensionality | The number of columns (features) in the data. | [Video 27](27-one-hot-encoding/note.md) |
| Discretization | Turning a continuous column into a discrete one by cutting its range into intervals. | [Video 32](32-binning-binarization/note.md) |
| Distance weight (nan-Euclidean) | All columns divided by the columns present in both rows; makes up for the skipped columns. | [Video 39](39-knn-imputer/note.md) |
| Distance weighting | Each neighbour counts in proportion to 1 / its distance, so nearer rows count more. | [Video 39](39-knn-imputer/note.md) |
| Distance | A number measuring how far apart two points are; small distance = similar. | [Video 6](06-instance-vs-model-based/note.md) |
| Distribution | How a column's values spread over their range. | [Video 20](20-univariate-analysis/note.md) |
| Diverge | To move further away with each step, the loss growing instead of shrinking. | [Video 57](57-gradient-descent/note.md) |
| Domain knowledge | Knowledge of the field the data comes from. | [Video 23](23-what-is-feature-engineering/note.md) |
| Donor | A row that has a value in the column being filled, so it can be a neighbour. | [Video 39](39-knn-imputer/note.md) |
| Dot product | Multiply matching components of two vectors and add; $u^{\mathsf T}x$. | [Video 48](48-pca-step-by-step/note.md) |
| dropna | The pandas method that drops rows (or columns) with missing values. | [Video 35](35-complete-case-analysis/note.md) |
| dtype | The data type of a column, such as `int64`, `float64` or `str`. | [Video 15](15-working-with-csv/note.md) |
| Dummy variable trap | The multicollinearity caused by keeping all $n$ dummy columns, which always add up to 1. | [Video 27](27-one-hot-encoding/note.md) |
| Dummy variable | One of the 0/1 columns created by one-hot encoding. | [Video 27](27-one-hot-encoding/note.md) |
| Duplicate row | A row identical to another row in every column. | [Video 19](19-understanding-your-data/note.md) |
| Durbin-Watson statistic | A number from 0 to 4 measuring autocorrelation of residuals; about 2 means none. | [Video 56](56-linear-regression-assumptions/note.md) |
| Eager learning | Another name for model-based learning: all the work done up front. | [Video 6](06-instance-vs-model-based/note.md) |
| Early stopping | Stopping training when the score on held-out data is best, before full convergence. | [Video 58](58-batch-gradient-descent/note.md) |
| Economy rate | A bowler's runs conceded per over. | [Video 45](45-feature-construction-splitting/note.md) |
| Eigen-decomposition | Finding all the eigenvalues and eigenvectors of a matrix. | [Video 48](48-pca-step-by-step/note.md) |
| Eigenvalue | The factor by which a matrix stretches its eigenvector. | [Video 48](48-pca-step-by-step/note.md) |
| Eigenvector | A vector that a matrix only stretches or shrinks, without turning it. | [Video 48](48-pca-step-by-step/note.md) |
| encode | The `KBinsDiscretizer` parameter choosing ordinal (bin numbers) or one-hot output. | [Video 32](32-binning-binarization/note.md) |
| Encoding | The rulebook that maps text characters to stored bytes. | [Video 15](15-working-with-csv/note.md) |
| End of distribution imputation | Filling every gap with a value at the edge of the distribution: $\mu \pm 3\sigma$ or $Q_3 + 1.5\,\text{IQR}$. | [Video 36](36-imputing-numerical-data/note.md) |
| Endpoint | One address of an API that returns one kind of data. | [Video 17](17-fetching-data-from-api/note.md) |
| Environment variable | A named value stored on the computer, outside the code, read with `os.environ`. | [Video 17](17-fetching-data-from-api/note.md) |
| Environment | The world the agent acts in. | [Video 3](03-types-of-ml/note.md) |
| Epoch | One full update of the parameters using the whole training set. | [Video 57](57-gradient-descent/note.md) |
| Equal frequency binning | Binning into bins holding the same number of rows, with the quantiles as edges; also called quantile binning. | [Video 32](32-binning-binarization/note.md) |
| Equal width binning | Binning into bins of the same width, $(\max - \min)/k$; also called uniform binning. | [Video 32](32-binning-binarization/note.md) |
| Error (residual) | The gap between an actual value and the model's prediction. | [Video 50](50-simple-linear-regression/note.md) |
| Error function (loss function) | A formula for how wrong the model is; here the sum of squared errors. | [Video 51](51-linear-regression-maths/note.md) |
| errors="coerce" | The `pd.to_numeric` option that turns values it cannot convert into NaN instead of stopping. | [Video 33](33-mixed-variables/note.md) |
| eta0 | The starting learning rate in SGDRegressor. | [Video 59](59-stochastic-gradient-descent/note.md) |
| Euclidean distance | The straight-line distance between two points. | [Video 23](23-what-is-feature-engineering/note.md) |
| Expert system | Early AI: a human expert's knowledge written as rules, plus a program that applies them. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Explained variance ratio | One component's share of the total variance: its eigenvalue divided by the sum of all. | [Video 49](49-pca-mnist/note.md) |
| Explained variance | The variance along a principal component; its eigenvalue. | [Video 48](48-pca-step-by-step/note.md) |
| explained_variance_ | The eigenvalues of the fitted PCA, largest first. | [Video 49](49-pca-mnist/note.md) |
| Explicit programming | A human writing out every rule the computer follows. ML avoids it. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Exploratory data analysis (EDA) | Exploring data with summaries and plots to find patterns. | [Video 13](13-toy-project/note.md) |
| Extrapolation | Predicting for inputs outside the range of the training data. | [Video 50](50-simple-linear-regression/note.md) |
| f-string | Text starting with `f` in which `{name}` is replaced by a value. | [Video 17](17-fetching-data-from-api/note.md) |
| Family size | `SibSp` + `Parch` + 1: the number of people in a passenger's travelling family. | [Video 45](45-feature-construction-splitting/note.md) |
| Family type | Family size grouped into alone, small family (2 to 4) and large family (5 or more). | [Video 45](45-feature-construction-splitting/note.md) |
| Feature construction | Creating a new column by hand from existing ones. | [Video 23](23-what-is-feature-engineering/note.md) |
| Feature engineering | Choosing, removing and creating features. | [Video 7](07-challenges-in-ml/note.md) |
| Feature extraction | Creating a new column from existing ones. | [Video 3](03-types-of-ml/note.md) |
| Feature scaling | Putting columns on the same scale, so no column dominates distances. | [Video 6](06-instance-vs-model-based/note.md) |
| Feature selection | Choosing which input columns to use. | [Video 13](13-toy-project/note.md) |
| Feature splitting | Breaking a column that holds several facts into one column per fact. | [Video 45](45-feature-construction-splitting/note.md) |
| Feature transformation | Changing a column into a form the model can use better. | [Video 23](23-what-is-feature-engineering/note.md) |
| Feature | One piece of information about each example that a model uses (e.g. a student's CGPA). | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Fence | A limit 1.5 IQR beyond the box; values past it are possible outliers. | [Video 20](20-univariate-analysis/note.md) |
| fit / transform | Learn the scaler's numbers from the training set / apply them to any data. | [Video 24](24-standardization/note.md) |
| fit_transform | Fit and transform in one call; used on the training set only. | [Video 28](28-column-transformer/note.md) |
| Five-number summary | Minimum, Q1, median, Q3 and maximum. | [Video 20](20-univariate-analysis/note.md) |
| For loop | Code that repeats once for each item of a collection. | [Video 15](15-working-with-csv/note.md) |
| Format string | A pattern such as `"%d/%m/%Y"` telling `pd.to_datetime` how dates are written. | [Video 34](34-date-and-time/note.md) |
| Forward selection | Feature selection that starts empty and adds the best column at a time. | [Video 46](46-curse-of-dimensionality/note.md) |
| Frame | One image in a video. | [Video 11](11-tensors/note.md) |
| Fraud detection | Spotting dishonest transactions; here the outliers are what we want to find. | [Video 41](41-what-are-outliers/note.md) |
| Frequency | How many times a value or category occurs. | [Video 20](20-univariate-analysis/note.md) |
| func | The `FunctionTransformer` parameter that holds the function to apply. | [Video 30](30-function-transformer/note.md) |
| Function, lambda | A named reusable piece of code (`def`), and a one-line unnamed one. | [Video 15](15-working-with-csv/note.md) |
| FunctionTransformer | scikit-learn's class that applies any function we give it to the data. | [Video 30](30-function-transformer/note.md) |
| Garbage in, garbage out | Bad input data always gives bad results. | [Video 7](07-challenges-in-ml/note.md) |
| get_dummies | pandas function that one-hot encodes columns; `drop_first=True` keeps $n - 1$. | [Video 27](27-one-hot-encoding/note.md) |
| get_feature_names_out | `OneHotEncoder` method that returns the names of the new columns. | [Video 27](27-one-hot-encoding/note.md) |
| Global minimum | The lowest point of the whole function. | [Video 57](57-gradient-descent/note.md) |
| Good fit | Capturing the pattern while ignoring the noise. | [Video 7](07-challenges-in-ml/note.md) |
| Gradient descent | Finding the lowest point of a function by repeated small steps downhill. | [Video 24](24-standardization/note.md) |
| Gradient | The vector of partial derivatives of the loss; it points in the direction of steepest increase. | [Video 57](57-gradient-descent/note.md) |
| Grid search | Training a model for every combination of listed settings and keeping the best by cross-validation. | [Video 38](38-missing-indicator-random-sample/note.md) |
| GridSearchCV | scikit-learn class that cross-validates every value in a grid and keeps the best. | [Video 29](29-pipelines/note.md) |
| handle_unknown | `OneHotEncoder` parameter that decides what happens to categories never seen in training. | [Video 27](27-one-hot-encoding/note.md) |
| handle_unknown="ignore" | `OneHotEncoder` setting that outputs all zeros for a category not seen in training. | [Video 29](29-pipelines/note.md) |
| Header | The line of a file that holds the column names. | [Video 15](15-working-with-csv/note.md) |
| Headers | Extra information sent with a request, such as the User-Agent. | [Video 18](18-web-scraping/note.md) |
| Heatmap | A table drawn as coloured cells, darker for larger values. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Heteroscedasticity | The spread of the residuals changes with the predicted value, often as a funnel. | [Video 56](56-linear-regression-assumptions/note.md) |
| High cardinality | A categorical column with very many different categories. | [Video 22](22-pandas-profiling/note.md) |
| High-dimensional data | Data with a very large number of columns. | [Video 46](46-curse-of-dimensionality/note.md) |
| Histogram | A bar chart of how many values fall in each equal range (bin) of a numerical column. | [Video 20](20-univariate-analysis/note.md) |
| Homoscedasticity | The residuals have the same spread for all predicted values. | [Video 56](56-linear-regression-assumptions/note.md) |
| HTML | The language web pages are written in: a tree of nested tags. | [Video 18](18-web-scraping/note.md) |
| Hue, style, size | Plot settings that show an extra column by colour, marker shape or dot size. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Hyperparameter tuning | Trying several hyperparameter values and keeping the best. | [Video 29](29-pipelines/note.md) |
| Hyperparameter | A setting of an algorithm chosen before training, such as a tree's `max_depth`. | [Video 29](29-pipelines/note.md) |
| Hyperplane | A flat surface in more than three dimensions; the model for three or more input columns. | [Video 53](53-multiple-linear-regression/note.md) |
| Identity matrix | The matrix that leaves every vector unchanged. | [Video 48](48-pca-step-by-step/note.md) |
| Imputation | Filling in missing values, for example with the mean, median or mode. | [Video 23](23-what-is-feature-engineering/note.md) |
| Incremental learning | Training on small pieces of data over time (the opposite of batch). | [Video 4](04-batch-learning/note.md) |
| Incremental training | Training in small steps, keeping what was learned before. | [Video 5](05-online-learning/note.md) |
| Independent variables | The input columns (X). | [Video 13](13-toy-project/note.md) |
| Index | The row labels of a DataFrame. | [Video 15](15-working-with-csv/note.md) |
| Inference engine | The part of an expert system that applies the rules to answer a question. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Input / output | The columns we know / the column we want to predict. | [Video 3](03-types-of-ml/note.md) |
| Inspect | Browser tool that shows which tag draws each part of a page. | [Video 18](18-web-scraping/note.md) |
| Instance-based learning | Learning by storing the training data and comparing new points with it. | [Video 6](06-instance-vs-model-based/note.md) |
| Intercept | The line's value when the input is 0; $b$ in $y = mx + b$. | [Video 50](50-simple-linear-regression/note.md) |
| intercept_ | The fitted intercept in scikit-learn. | [Video 50](50-simple-linear-regression/note.md) |
| Interquartile range (IQR) | Q3 - Q1: the width of the middle half of the data. | [Video 20](20-univariate-analysis/note.md) |
| Inverse matrix | The matrix that undoes another: their product is the identity matrix. | [Video 54](54-multiple-lr-maths/note.md) |
| IQR method (IQR proximity rule) | Outlier detection that flags values beyond 1.5 IQR outside the box ($Q_1$ to $Q_3$); for skewed columns. | [Video 43](43-outliers-iqr/note.md) |
| IQR rule | Values beyond 1.5 IQR outside the box ($Q_1$ to $Q_3$) are outliers; used for skewed columns. | [Video 41](41-what-are-outliers/note.md) |
| isnull | The pandas method that marks each missing cell `True`. | [Video 35](35-complete-case-analysis/note.md) |
| ISO week | The week number of the ISO calendar, from `.dt.isocalendar().week`; week 1 holds the year's first Thursday. | [Video 34](34-date-and-time/note.md) |
| Iteration (MICE) | One pass that re-predicts the gaps of every column once, in order. | [Video 40](40-iterative-imputer-mice/note.md) |
| Iteration 0 | The starting table, with every gap filled by its column mean. | [Video 40](40-iterative-imputer-mice/note.md) |
| Iterative imputer | Multivariate imputation that predicts each column from the others, repeatedly; its algorithm is MICE. | [Video 35](35-complete-case-analysis/note.md) |
| joblib | A library that saves and loads Python objects like pickle, better suited to large arrays. | [Video 29](29-pipelines/note.md) |
| JSON (JavaScript Object Notation) | A plain-text data format of objects and arrays that almost every language can read. | [Video 16](16-working-with-json-and-sql/note.md) |
| JSON Lines | A JSON file with one object per line, read with `lines=True`. | [Video 16](16-working-with-json-and-sql/note.md) |
| JSON viewer | A tool that lays out JSON text as a tree to show its structure. | [Video 17](17-fetching-data-from-api/note.md) |
| k-means binning | Binning whose edges lie halfway between the centres of the groups found by k-means. | [Video 32](32-binning-binarization/note.md) |
| k-means | A clustering algorithm that repeatedly assigns points to the nearest centre and moves each centre to the mean of its points. | [Video 32](32-binning-binarization/note.md) |
| K-nearest neighbours (KNN) | Predicting from the answers of the k closest stored points. | [Video 6](06-instance-vs-model-based/note.md) |
| Kaggle | A website for sharing datasets and notebooks and for ML competitions. | [Video 17](17-fetching-data-from-api/note.md) |
| KBinsDiscretizer | scikit-learn's class for equal width, equal frequency and k-means binning. | [Video 32](32-binning-binarization/note.md) |
| KDE plot | A smooth estimate of a column's PDF, built from the data. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Kernel density estimate (KDE) | A smooth curve that estimates a column's distribution from its values. | [Video 20](20-univariate-analysis/note.md) |
| KNN imputer | Multivariate imputation from the most similar rows (`KNNImputer`). | [Video 35](35-complete-case-analysis/note.md) |
| Knowledge base | The collection of rules inside an expert system. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Kurtosis | How heavy the tails of a distribution are compared with a normal curve. | [Video 22](22-pandas-profiling/note.md) |
| Label encoding | Replacing the classes of the target by 0, 1, 2, ...; for the output column only. | [Video 26](26-ordinal-label-encoding/note.md) |
| LabelEncoder | scikit-learn's class for label encoding the target. | [Video 26](26-ordinal-label-encoding/note.md) |
| Labelled data | Data that includes the output column. | [Video 3](03-types-of-ml/note.md) |
| Lambda ($\lambda$) | The power used by a power transform, learned separately for each column. | [Video 31](31-power-transformer/note.md) |
| Lambda | A one-line Python function without a name, such as `lambda x: x**2`. | [Video 30](30-function-transformer/note.md) |
| lambdas_ | The `PowerTransformer` attribute holding the learned $\lambda$ of each column. | [Video 31](31-power-transformer/note.md) |
| Layer | One step in a neural network; each layer builds on what the previous one found. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Lazy learning | Another name for instance-based learning: no work until a question arrives. | [Video 6](06-instance-vs-model-based/note.md) |
| LDA | Linear discriminant analysis: a supervised method that finds the directions that best separate the classes. | [Video 49](49-pca-mnist/note.md) |
| Learning rate ($\eta$) | The number the slope is multiplied by to get the step size. | [Video 57](57-gradient-descent/note.md) |
| Learning rate | How strongly each new piece of data changes the model. | [Video 5](05-online-learning/note.md) |
| Learning schedule | A rule that changes the learning rate during training, usually shrinking it. | [Video 59](59-stochastic-gradient-descent/note.md) |
| Learning | Finding rules (patterns) from examples. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Line plot | A scatter plot with the dots joined in order, used when x is time. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Linear interpolation | Placing a percentile between two neighbouring sorted values, in proportion to its position; the pandas default. | [Video 44](44-outliers-percentile/note.md) |
| Linear regression | An algorithm that fits the straight line closest to all the points. | [Video 23](23-what-is-feature-engineering/note.md) |
| Linear relationship | A relationship between two columns that follows a straight line. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Linear transformation | A change of the whole plane by a matrix that keeps grid lines straight and evenly spaced. | [Video 48](48-pca-step-by-step/note.md) |
| List, dictionary | Python's ordered collection `[...]`, and its `key: value` pairs `{...}`. | [Video 15](15-working-with-csv/note.md) |
| Local minimum | A point lower than everything around it, but not the lowest overall. | [Video 57](57-gradient-descent/note.md) |
| Log transform | Replacing each value with its logarithm; pulls in a long right tail. | [Video 30](30-function-transformer/note.md) |
| log1p | NumPy's $\log(1 + x)$, a log transform that also works when a value is 0. | [Video 30](30-function-transformer/note.md) |
| Logistic regression | A classification algorithm that finds a separating boundary. | [Video 13](13-toy-project/note.md) |
| LPA | Lakh rupees per annum: a salary in hundreds of thousands of rupees per year. | [Video 50](50-simple-linear-regression/note.md) |
| Machine Learning (ML) | Using statistics to let a machine find patterns (rules) in data by itself. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Magnitude | The number part of a quantity, as opposed to its unit. | [Video 25](25-normalization/note.md) |
| make_column_transformer | Function that builds a column transformer from (transformer, columns) pairs, without names. | [Video 29](29-pipelines/note.md) |
| make_pipeline | Function that builds a pipeline from objects alone, naming each step after its class. | [Video 29](29-pipelines/note.md) |
| make_regression | scikit-learn function that generates data following a linear pattern plus noise. | [Video 53](53-multiple-linear-regression/note.md) |
| MAR | Missing at random: the gaps depend on another, recorded column. | [Video 35](35-complete-case-analysis/note.md) |
| Mathematical transformation | Applying one mathematical formula to every value of a column. | [Video 30](30-function-transformer/note.md) |
| Matrix calculus | Rules for differentiating expressions with vectors and matrices. | [Video 54](54-multiple-lr-maths/note.md) |
| Matrix | A table of numbers: a 2D tensor. | [Video 11](11-tensors/note.md) |
| Max-abs scaling | Divide by the largest absolute value in the column, giving values from -1 to 1. | [Video 25](25-normalization/note.md) |
| max_iter | The maximum number of epochs in SGDRegressor. | [Video 59](59-stochastic-gradient-descent/note.md) |
| MaxAbsScaler | scikit-learn's class for max-abs scaling. | [Video 25](25-normalization/note.md) |
| Maximum likelihood | Choosing the parameter value under which the observed data is most likely; used to find $\lambda$. | [Video 31](31-power-transformer/note.md) |
| MCAR | Missing completely at random: the gaps have no relation to any value in the data. | [Video 35](35-complete-case-analysis/note.md) |
| Mean absolute deviation | The average absolute distance of the points from their mean. | [Video 47](47-pca-geometric-intuition/note.md) |
| Mean absolute error (MAE) | The average absolute difference between actual and predicted values. | [Video 52](52-regression-metrics/note.md) |
| Mean centring | Subtracting the mean from every value, so the column's mean becomes 0. | [Video 24](24-standardization/note.md) |
| Mean imputation | Filling every gap with the mean of the column's known values. | [Video 36](36-imputing-numerical-data/note.md) |
| Mean normalization | Subtract the mean and divide by the range, giving values from -1 to 1 centred on 0. | [Video 25](25-normalization/note.md) |
| Mean squared error (MSE) | The average squared difference between actual and predicted values. | [Video 52](52-regression-metrics/note.md) |
| Mean squared error loss | The average squared error; its derivatives do not grow with the number of rows. | [Video 58](58-batch-gradient-descent/note.md) |
| Mean | The average of the values; the centre of the data. | [Video 47](47-pca-geometric-intuition/note.md) |
| Median absolute deviation (MAD) | The median distance of the values from their median. | [Video 22](22-pandas-profiling/note.md) |
| Median imputation | Filling every gap with the median of the column's known values; better for skewed columns. | [Video 36](36-imputing-numerical-data/note.md) |
| Median | The middle value of sorted data; the 50% percentile. | [Video 19](19-understanding-your-data/note.md) |
| method | The `PowerTransformer` parameter that picks `"box-cox"` or `"yeo-johnson"`. | [Video 31](31-power-transformer/note.md) |
| MICE | Multivariate Imputation by Chained Equations: the algorithm behind the iterative imputer. | [Video 40](40-iterative-imputer-mice/note.md) |
| Min-max scaling | The main normalization technique. | [Video 24](24-standardization/note.md) |
| min_frequency | `OneHotEncoder` parameter that merges rare categories into one column. | [Video 27](27-one-hot-encoding/note.md) |
| Mini-batch gradient descent | Gradient descent that uses a small random group of rows for every update. | [Video 58](58-batch-gradient-descent/note.md) |
| Mini-batch | A small group of data points used for one training step. | [Video 5](05-online-learning/note.md) |
| MinMaxScaler | scikit-learn's class for min-max scaling. | [Video 25](25-normalization/note.md) |
| Missing category imputation | Filling every gap in a categorical column with a new category, "Missing". | [Video 37](37-missing-categorical-data/note.md) |
| Missing indicator | A 0/1 column recording whether a value was missing. | [Video 35](35-complete-case-analysis/note.md) |
| Missing value | An empty entry, shown by pandas as `NaN`. | [Video 15](15-working-with-csv/note.md) |
| Missing values | Empty cells in the data. | [Video 7](07-challenges-in-ml/note.md) |
| Mixed variable | A column holding both numerical and categorical data. | [Video 33](33-mixed-variables/note.md) |
| MLOps | Running and maintaining ML models in production. | [Video 7](07-challenges-in-ml/note.md) |
| MNAR | Missing not at random: the gaps depend on the missing value itself. | [Video 35](35-complete-case-analysis/note.md) |
| MNIST | A dataset of about 70,000 handwritten-digit images of 28 × 28 pixels. | [Video 23](23-what-is-feature-engineering/note.md) |
| Mode | The most common value of a column. | [Video 23](23-what-is-feature-engineering/note.md) |
| Model drift / concept drift | A model's accuracy dropping as the real world changes. | [Video 4](04-batch-learning/note.md) |
| Model selection | Training several algorithms and keeping the best. | [Video 13](13-toy-project/note.md) |
| Model-based learning | Learning a mathematical function from the data and predicting with it. | [Video 6](06-instance-vs-model-based/note.md) |
| Monotonicity | Whether a column's values only go up, or only go down, from row to row. | [Video 22](22-pandas-profiling/note.md) |
| Most frequent value imputation (mode imputation) | Filling every gap in a column with its mode. | [Video 37](37-missing-categorical-data/note.md) |
| Multicollinearity | A mathematical relationship between input columns, so that one can be calculated from the others. | [Video 27](27-one-hot-encoding/note.md) |
| Multiple imputation | Making several filled copies of the data to see how unsure the fills are. | [Video 40](40-iterative-imputer-mice/note.md) |
| Multiple linear regression | Linear regression with several input columns. | [Video 50](50-simple-linear-regression/note.md) |
| Multivariate analysis | Studying more than two variables together. | [Video 20](20-univariate-analysis/note.md) |
| Multivariate imputation | Imputation that also uses the other columns. | [Video 35](35-complete-case-analysis/note.md) |
| n_bins | The `KBinsDiscretizer` parameter for the number of bins. | [Video 32](32-binning-binarization/note.md) |
| n_components | The number of principal components PCA keeps; a number between 0 and 1 means a share of the variance. | [Video 49](49-pca-mnist/note.md) |
| named_steps | Dictionary of a pipeline's steps, from each name to its object. | [Video 29](29-pipelines/note.md) |
| nan-Euclidean distance | The Euclidean distance over the columns both rows have, scaled by (all columns / used columns). | [Video 39](39-knn-imputer/note.md) |
| Narrow AI | AI that does one specific task. All AI today is narrow. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| NaT | "Not a time": the missing value of a datetime column. | [Video 34](34-date-and-time/note.md) |
| Nearest neighbours | The rows at the smallest distance from a given row. | [Video 39](39-knn-imputer/note.md) |
| Neural network | The model DL uses, loosely inspired by neurons in the brain. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Nominal data | Categorical data whose categories have no order, such as states. | [Video 26](26-ordinal-label-encoding/note.md) |
| Non-closed-form solution | An answer reached by improving a guess step by step. | [Video 51](51-linear-regression-maths/note.md) |
| Non-null | Not missing. | [Video 19](19-understanding-your-data/note.md) |
| Normal distribution | A symmetric, bell-shaped distribution. | [Video 20](20-univariate-analysis/note.md) |
| Normal equation | $\beta = (X^{\mathsf T}X)^{-1}X^{\mathsf T}y$: the closed-form solution of linear regression. | [Video 54](54-multiple-lr-maths/note.md) |
| Normal equations | $X^{\mathsf T}X\beta = X^{\mathsf T}y$: the conditions that the best coefficients satisfy. | [Video 54](54-multiple-lr-maths/note.md) |
| Normalization | The other type of feature scaling, which squeezes values into a fixed range (next Note). | [Video 24](24-standardization/note.md) |
| np.concatenate | NumPy function that joins arrays; with `axis=1` it puts them side by side. | [Video 28](28-column-transformer/note.md) |
| np.insert | NumPy function that inserts values into an array at a given position. | [Video 55](55-multiple-lr-code/note.md) |
| np.linalg.inv | NumPy function that computes the inverse of a square matrix. | [Video 55](55-multiple-lr-code/note.md) |
| np.linalg.lstsq | NumPy function that finds the least-squares solution of a linear system. | [Video 55](55-multiple-lr-code/note.md) |
| Nullable integer (Int64) | The pandas integer type that can also hold a missing value, `<NA>`. | [Video 33](33-mixed-variables/note.md) |
| Nullity matrix | A picture of the whole table with missing values drawn as white lines. | [Video 22](22-pandas-profiling/note.md) |
| Numerical data | Data made of numbers. | [Video 3](03-types-of-ml/note.md) |
| Objective function | The quantity an algorithm tries to make as large or as small as possible. | [Video 48](48-pca-step-by-step/note.md) |
| Observation | The report's word for a row. | [Video 22](22-pandas-profiling/note.md) |
| Offline learning | Another name for batch learning. | [Video 4](04-batch-learning/note.md) |
| One-hot encoding | Representing each word or category by a vector with a single 1. | [Video 11](11-tensors/note.md) |
| OneHotEncoder | scikit-learn's class for one-hot encoding; remembers the categories it learned. | [Video 27](27-one-hot-encoding/note.md) |
| Online learning | Training incrementally on mini-batches while the model is live in production. | [Video 5](05-online-learning/note.md) |
| Optimal number of features | The number of columns at which a model performs best. | [Video 46](46-curse-of-dimensionality/note.md) |
| Optimisation algorithm | A method for finding the parameter values that make a function as small (or large) as possible. | [Video 57](57-gradient-descent/note.md) |
| Ordinal data | Categorical data whose categories have a natural order, such as Poor < Average < Good. | [Video 26](26-ordinal-label-encoding/note.md) |
| Ordinal encoding | Replacing ordered categories by 0, 1, 2, ... in their order; for input columns. | [Video 26](26-ordinal-label-encoding/note.md) |
| OrdinalEncoder | scikit-learn's class for ordinal encoding; takes the order through `categories`. | [Video 26](26-ordinal-label-encoding/note.md) |
| Ordinary least squares (OLS) | The closed-form method for linear regression: the line with the smallest sum of squared errors. | [Video 51](51-linear-regression-maths/note.md) |
| Out-of-core learning | Training on data too big for memory by feeding it in chunks, offline. | [Video 5](05-online-learning/note.md) |
| Outlier detection | Setting a lower and an upper limit; values outside them are outliers. | [Video 41](41-what-are-outliers/note.md) |
| Outlier | A value far from the rest of the data. | [Video 20](20-univariate-analysis/note.md) |
| Outliers | Values far from the rest, often mistakes. | [Video 7](07-challenges-in-ml/note.md) |
| Overfitting | Learning the training data too closely, noise included; fails on new data. | [Video 7](07-challenges-in-ml/note.md) |
| Pair plot | A grid of scatter plots of every pair of numerical columns, with histograms on the diagonal. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Pandas Profiling | The library that builds a profiling report from a DataFrame, now named `fg-data-profiling`. | [Video 22](22-pandas-profiling/note.md) |
| pandas, DataFrame | Python's main table library, and its name for a table. | [Video 13](13-toy-project/note.md) |
| Parameter | A named setting passed to a function, like `sep=";"`. | [Video 15](15-working-with-csv/note.md) |
| Parameters | The numbers that describe a learned model, e.g. slope and intercept. | [Video 6](06-instance-vs-model-based/note.md) |
| Parse, parser | Read text and build a structure from it; the part that does this. | [Video 18](18-web-scraping/note.md) |
| Parser | The part of a program that reads text and splits it into pieces. | [Video 15](15-working-with-csv/note.md) |
| Partial derivative | The slope of a function of several variables in one variable, holding the others fixed. | [Video 51](51-linear-regression-maths/note.md) |
| partial_fit | A scikit-learn method that continues training from where the model left off. | [Video 5](05-online-learning/note.md) |
| passthrough | The `remainder` option that keeps untouched columns unchanged. | [Video 28](28-column-transformer/note.md) |
| PCA | Principal component analysis, a dimensionality reduction technique. | [Video 3](03-types-of-ml/note.md) |
| pd.cut | The pandas function that puts values into intervals we give it. | [Video 32](32-binning-binarization/note.md) |
| pd.to_datetime | The pandas function that converts text to datetime values. | [Video 34](34-date-and-time/note.md) |
| pd.to_numeric | The pandas function that converts values to numbers. | [Video 33](33-mixed-variables/note.md) |
| Pearson correlation coefficient | The usual measure of correlation, written $r$; the one `df.corr()` computes. | [Video 19](19-understanding-your-data/note.md) |
| Pearson's r | The correlation coefficient for straight-line relationships between two numerical columns. | [Video 22](22-pandas-profiling/note.md) |
| Per-row seed | A seed taken from a row's own values, so the same input always gets the same random fill. | [Video 38](38-missing-indicator-random-sample/note.md) |
| Percentile method | Outlier detection that flags values below a low percentile or above a high one (e.g. 1st and 99th); for any column. | [Video 44](44-outliers-percentile/note.md) |
| Percentile rule | Values below a low percentile or above a high one (e.g. 1st, 99th) are outliers. | [Video 41](41-what-are-outliers/note.md) |
| Percentile | The value below which a given share of the data lies. | [Video 19](19-understanding-your-data/note.md) |
| Perceptron | The smallest building block of a neural network; one artificial neuron. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| phpMyAdmin | A web page for creating and managing MySQL databases. | [Video 16](16-working-with-json-and-sql/note.md) |
| pickle | A Python module that saves objects to a file and loads them back. | [Video 13](13-toy-project/note.md) |
| Pie chart | A circle split into slices sized by each category's share. | [Video 20](20-univariate-analysis/note.md) |
| Pipeline (class) | The scikit-learn class (in `sklearn.pipeline`) that builds a pipeline from a list of (name, object) tuples. | [Video 29](29-pipelines/note.md) |
| Pipeline | One object that bundles several processing steps and a model. | [Video 13](13-toy-project/note.md) |
| Pivot table | A grid with one column's values as rows, another's as columns, and a third in the cells. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| Pixel | One dot of an image, stored as one or more numbers. | [Video 11](11-tensors/note.md) |
| Plane | A flat surface in 3D; the model for two input columns. | [Video 53](53-multiple-linear-regression/note.md) |
| Plateau | A nearly flat region of the loss, where steps become very small. | [Video 57](57-gradient-descent/note.md) |
| Policy | The agent's rules for which action to take. | [Video 3](03-types-of-ml/note.md) |
| Power transformer | A transform that raises each column to a learned power $\lambda$ to make it close to normal. | [Video 31](31-power-transformer/note.md) |
| PowerTransformer | scikit-learn's class for the Box-Cox and Yeo-Johnson transforms (next Note). | [Video 30](30-function-transformer/note.md) |
| Predict | Use a trained model to give an answer for new data it has not seen. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Prediction ($\hat{y}$) | The value the model gives for an input; the hat marks a prediction. | [Video 51](51-linear-regression-maths/note.md) |
| Preprocessing | Cleaning and preparing data before training. | [Video 13](13-toy-project/note.md) |
| Principal component analysis (PCA) | An unsupervised feature extraction technique that builds new columns along the directions of greatest variance. | [Video 47](47-pca-geometric-intuition/note.md) |
| Principal component | A new axis found by PCA; PC1 holds the most variance, PC2 the next most. | [Video 47](47-pca-geometric-intuition/note.md) |
| Probability density function (PDF) | A curve showing how likely each value is; areas under it are probabilities. | [Video 20](20-univariate-analysis/note.md) |
| Production code | The code that runs the deployed model on a server, for example behind a website. | [Video 29](29-pipelines/note.md) |
| Production environment | The server where a model serves real users. | [Video 4](04-batch-learning/note.md) |
| Profiling report | An automatic EDA report describing every column and pair of columns of a dataset. | [Video 22](22-pandas-profiling/note.md) |
| Projection | Dropping each point onto an axis or line, like casting a shadow. | [Video 47](47-pca-geometric-intuition/note.md) |
| Q-Q plot | A plot of a column's sorted values against the values a normal distribution would have; points on the line mean normal. | [Video 30](30-function-transformer/note.md) |
| QuantileTransformer | scikit-learn's third mathematical transformer, not covered in these Notes. | [Video 30](30-function-transformer/note.md) |
| Quarter | One of four three-month parts of a year. | [Video 34](34-date-and-time/note.md) |
| Quartile | $Q_1$ (25th percentile) and $Q_3$ (75th percentile): they cut the sorted column into quarters. | [Video 43](43-outliers-iqr/note.md) |
| Quartiles | The 25%, 50% and 75% percentiles, which cut the data into four equal groups. | [Video 19](19-understanding-your-data/note.md) |
| Query parameters | Settings after the `?` in a URL, joined by `&`, such as `page=1`. | [Video 17](17-fetching-data-from-api/note.md) |
| Query | A request for data, written in SQL. | [Video 16](16-working-with-json-and-sql/note.md) |
| Random sample imputation | Filling each gap with a value drawn at random from the column's known values. | [Video 38](38-missing-indicator-random-sample/note.md) |
| Rank | The number of axes of a tensor (ndim in NumPy). | [Video 11](11-tensors/note.md) |
| RapidAPI | A website listing many APIs, including free ones. | [Video 17](17-fetching-data-from-api/note.md) |
| Rate limit | The most requests an API accepts in a given time. | [Video 17](17-fetching-data-from-api/note.md) |
| Raw data | Data as it arrives, before any preparation. | [Video 23](23-what-is-feature-engineering/note.md) |
| Raw string | A Python string written `r"..."`, in which a backslash is kept as it is. | [Video 33](33-mixed-variables/note.md) |
| Reader | What `read_csv` returns with `chunksize`: it hands out one chunk at a time. | [Video 15](15-working-with-csv/note.md) |
| Reciprocal transform | Replacing each value with $1/x$; reverses the order of the values. | [Video 30](30-function-transformer/note.md) |
| Recommendation engine | A model that suggests items, such as movies, to users. | [Video 4](04-batch-learning/note.md) |
| Reference category | The category whose dummy column is dropped; it is shown by all zeros. | [Video 27](27-one-hot-encoding/note.md) |
| Regression metric | A number that summarises how close a regression model's predictions are to the true values. | [Video 52](52-regression-metrics/note.md) |
| Regression | Supervised learning with a numerical output. | [Video 3](03-types-of-ml/note.md) |
| Regular expression | A short pattern that describes text, such as `\d+` for "one or more digits". | [Video 33](33-mixed-variables/note.md) |
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
| River | A Python library for online machine learning. | [Video 5](05-online-learning/note.md) |
| robots.txt | A file at a site's root listing what bots are asked not to visit. | [Video 18](18-web-scraping/note.md) |
| Robust scaler | A normalization technique that copes well with outliers. | [Video 24](24-standardization/note.md) |
| Robust scaling | Subtract the median and divide by the interquartile range; copes well with outliers. | [Video 25](25-normalization/note.md) |
| RobustScaler | scikit-learn's class for robust scaling. | [Video 25](25-normalization/note.md) |
| Rollback | Restoring a model to an earlier, good version. | [Video 5](05-online-learning/note.md) |
| Root mean squared error (RMSE) | The square root of MSE, in the output's units. | [Video 52](52-regression-metrics/note.md) |
| R² score (coefficient of determination) | 1 minus the model's squared error divided by the squared error of always predicting the mean. | [Video 52](52-regression-metrics/note.md) |
| R² score | How much of the variation in a regression target the model explains: 1 is perfect, 0 is no better than the average. | [Video 31](31-power-transformer/note.md) |
| Saddle point | A flat point that curves up in one direction and down in another. | [Video 57](57-gradient-descent/note.md) |
| Sample | The part of the real world that our data covers. | [Video 7](07-challenges-in-ml/note.md) |
| Sampling bias | An unrepresentative sample caused by how the data was collected. | [Video 7](07-challenges-in-ml/note.md) |
| Sampling noise | An unrepresentative sample caused by being too small. | [Video 7](07-challenges-in-ml/note.md) |
| Scalar | A single number: a 0D tensor. | [Video 11](11-tensors/note.md) |
| Scaling | Bringing input columns to similar ranges. | [Video 13](13-toy-project/note.md) |
| Scatter plot | One dot per row, with one numerical column on each axis. | [Video 21](21-bivariate-multivariate-analysis/note.md) |
| scikit-learn | Python's main library for classical ML. | [Video 13](13-toy-project/note.md) |
| SelectKBest | scikit-learn class that scores every column and keeps the `k` best. | [Video 29](29-pipelines/note.md) |
| Semester | One of two six-month halves of a year. | [Video 34](34-date-and-time/note.md) |
| Semi-supervised learning | Learning from a few labelled rows and many unlabelled ones. | [Video 3](03-types-of-ml/note.md) |
| Separator | The character between values on a line, such as `,` or a tab. | [Video 15](15-working-with-csv/note.md) |
| Sequential data | Data fed one piece after another, in order. | [Video 5](05-online-learning/note.md) |
| Series | pandas' one-column structure: values with an index. | [Video 15](15-working-with-csv/note.md) |
| Server | A computer that is always on and that users reach over the internet. | [Video 4](04-batch-learning/note.md) |
| set_output | Method that makes a transformer return a pandas DataFrame with `transform="pandas"`. | [Video 28](28-column-transformer/note.md) |
| SGDRegressor | A scikit-learn model that does linear regression step by step. | [Video 5](05-online-learning/note.md) |
| Shape | The number of items along each axis. | [Video 11](11-tensors/note.md) |
| Shapiro-Wilk test | A statistical test of whether data follows a normal distribution. | [Video 56](56-linear-regression-assumptions/note.md) |
| Shuffling | Putting the rows in a new random order before each epoch. | [Video 60](60-mini-batch-gradient-descent/note.md) |
| Similarity | How alike two data points are. | [Video 6](06-instance-vs-model-based/note.md) |
| Simple linear regression | Linear regression with one input column. | [Video 50](50-simple-linear-regression/note.md) |
| SimpleImputer | scikit-learn's class that fills missing values, by default with the column's mean. | [Video 28](28-column-transformer/note.md) |
| Simulated annealing | Lowering the learning rate gradually so the search settles down. | [Video 59](59-stochastic-gradient-descent/note.md) |
| Size | The total number of items: the product of the shape. | [Video 11](11-tensors/note.md) |
| Skewness | A number for how lopsided a distribution is: 0 symmetric, positive right tail, negative left tail. | [Video 20](20-univariate-analysis/note.md) |
| slice(0, 10) | Python object meaning positions 0 up to, not including, 10. | [Video 29](29-pipelines/note.md) |
| Slope | How much the output changes for one unit of change in the input; $m$ in $y = mx + b$. | [Video 50](50-simple-linear-regression/note.md) |
| Software integration | Building a model into the software that users use. | [Video 7](07-challenges-in-ml/note.md) |
| Solver | The method a model uses to find its best settings during training. | [Video 24](24-standardization/note.md) |
| Sparse data | Data where most of the space holds no points. | [Video 46](46-curse-of-dimensionality/note.md) |
| Sparse matrix | A table stored as only its non-zero entries, to save memory. | [Video 27](27-one-hot-encoding/note.md) |
| sparse_output | `OneHotEncoder` parameter; `False` returns a normal NumPy array. | [Video 27](27-one-hot-encoding/note.md) |
| SQL (Structured Query Language) | The language for asking a database for data. | [Video 16](16-working-with-json-and-sql/note.md) |
| SQLAlchemy | A Python library that connects to many kinds of database; pandas supports it fully. | [Video 16](16-working-with-json-and-sql/note.md) |
| SQLite | A database stored in a single file, built into Python, needing no server. | [Video 16](16-working-with-json-and-sql/note.md) |
| Square root transform | Replacing each value with $\sqrt{x}$; a milder version of the log. | [Video 30](30-function-transformer/note.md) |
| Square transform | Replacing each value with $x^2$; used for left-skewed data. | [Video 30](30-function-transformer/note.md) |
| Standard deviation | A measure of how spread out a column's values are. | [Video 13](13-toy-project/note.md) |
| Standardization | Scaling a column to mean 0 and standard deviation 1. | [Video 13](13-toy-project/note.md) |
| standardize | The `PowerTransformer` parameter (on by default) that rescales the output to mean 0 and standard deviation 1. | [Video 31](31-power-transformer/note.md) |
| StandardScaler | scikit-learn's class that standardizes columns with `fit` and `transform`. | [Video 24](24-standardization/note.md) |
| Static model | A model that learns nothing new after deployment. | [Video 4](04-batch-learning/note.md) |
| statsmodels | A Python library for statistical models and tests. | [Video 56](56-linear-regression-assumptions/note.md) |
| Status code | A number saying how a request went: 200 OK, 401, 404, 500. | [Video 17](17-fetching-data-from-api/note.md) |
| step__parameter | How a pipeline step's parameter is named: step name, two underscores, parameter name. | [Video 29](29-pipelines/note.md) |
| Stochastic error | A random, unmeasurable influence that scatters data around its trend. | [Video 50](50-simple-linear-regression/note.md) |
| Stochastic gradient descent (SGD) | Gradient descent that uses one random row for every update. | [Video 58](58-batch-gradient-descent/note.md) |
| Stochastic | Involving randomness. | [Video 59](59-stochastic-gradient-descent/note.md) |
| str dtype | The pandas 3 type for text columns, replacing `object`. | [Video 33](33-mixed-variables/note.md) |
| str.extract | The pandas method that returns the part of each value matching a regular expression. | [Video 33](33-mixed-variables/note.md) |
| strategy | The `KBinsDiscretizer` parameter choosing uniform, quantile or kmeans. | [Video 32](32-binning-binarization/note.md) |
| Strike rate | A batter's runs per 100 balls faced. | [Video 45](45-feature-construction-splitting/note.md) |
| Sum of squared errors | The squares of all the errors added up; the quantity the best-fit line makes smallest. | [Video 50](50-simple-linear-regression/note.md) |
| Supervised binning | Binning that also uses the target, such as decision tree binning. | [Video 32](32-binning-binarization/note.md) |
| Supervised learning | Learning from data with inputs and outputs, to predict outputs. | [Video 3](03-types-of-ml/note.md) |
| Supervision | Correct answers that guide an algorithm while it learns. | [Video 3](03-types-of-ml/note.md) |
| Symbolic AI | Early AI where humans write the knowledge as rules. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Tag | One element of HTML, such as `<h2>TCS</h2>`. | [Video 18](18-web-scraping/note.md) |
| Target leakage | Building an input column from the answer itself, so the model sees information it would not have in real use. | [Video 52](52-regression-metrics/note.md) |
| Target, label | Other names for the output column. | [Video 3](03-types-of-ml/note.md) |
| Tensor | A container of numbers arranged along one or more axes. | [Video 11](11-tensors/note.md) |
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
| Train | Let a model learn by making predictions, measuring its errors and adjusting to reduce them. | [Video 2](02-ai-vs-ml-vs-dl/note.md) |
| Train-test split | Dividing the data into training and test sets. | [Video 13](13-toy-project/note.md) |
| Training set | The part of the data the model learns from. | [Video 13](13-toy-project/note.md) |
| transformers | The `ColumnTransformer` parameter: a list of (name, transformer, columns) tuples. | [Video 28](28-column-transformer/note.md) |
| transformers_ | List of a fitted column transformer's (name, transformer, columns) tuples. | [Video 29](29-pipelines/note.md) |
| Transpose | A matrix or vector with rows and columns swapped. | [Video 48](48-pca-step-by-step/note.md) |
| Tree-based algorithm | An algorithm that splits the data with simple conditions; hardly affected by outliers. | [Video 41](41-what-are-outliers/note.md) |
| Trimming | Removing the rows that hold outliers. | [Video 41](41-what-are-outliers/note.md) |
| TSV file | Like a CSV file, with tabs between values. | [Video 15](15-working-with-csv/note.md) |
| Type 1 mixed variable | A column whose cells each contain a category and a number together, such as `C85`. | [Video 33](33-mixed-variables/note.md) |
| Type 2 mixed variable | A column with a number in some rows and a category in others. | [Video 33](33-mixed-variables/note.md) |
| Underfitting | Being too simple to capture the pattern; fails on all data. | [Video 7](07-challenges-in-ml/note.md) |
| Understanding the data | The project stage where we learn what is in the data before cleaning or modelling. | [Video 19](19-understanding-your-data/note.md) |
| Uniform weighting | Every neighbour counts equally: the fill is their plain mean. | [Video 39](39-knn-imputer/note.md) |
| Unit hypercube | The same box in three or more dimensions (a unit cube in three). | [Video 25](25-normalization/note.md) |
| Unit square | The square from (0, 0) to (1, 1), into which min-max scaling presses two columns. | [Video 25](25-normalization/note.md) |
| Unit vector | A vector of length 1, used to describe a direction. | [Video 48](48-pca-step-by-step/note.md) |
| Univariate analysis | Studying one variable on its own. | [Video 20](20-univariate-analysis/note.md) |
| Univariate imputation | Imputation that uses only the column with the gap. | [Video 35](35-complete-case-analysis/note.md) |
| Unreasonable effectiveness of data | With enough data, different algorithms perform about the same. | [Video 7](07-challenges-in-ml/note.md) |
| Unsupervised binning | Binning that uses only the column's own values. | [Video 32](32-binning-binarization/note.md) |
| Unsupervised learning | Learning from inputs only, to find structure. | [Video 3](03-types-of-ml/note.md) |
| Upper / lower limit | $\mu + 3\sigma$ and $\mu - 3\sigma$; values beyond them are outliers. | [Video 42](42-outliers-zscore/note.md) |
| User-Agent | A short text a browser sends to say what it is. | [Video 15](15-working-with-csv/note.md) |
| UTF-8 | The most common encoding, and `read_csv`'s default. | [Video 15](15-working-with-csv/note.md) |
| Variable | One column of a dataset. | [Video 20](20-univariate-analysis/note.md) |
| Variance inflation factor (VIF) | $1 / (1 - R_j^2)$: how well the other inputs predict input $j$; above 5 signals multicollinearity. | [Video 56](56-linear-regression-assumptions/note.md) |
| Variance | The average squared distance of the points from their mean. | [Video 47](47-pca-geometric-intuition/note.md) |
| Vector | A list of numbers: a 1D tensor. | [Video 11](11-tensors/note.md) |
| Vectorisation | Writing a computation as operations on whole arrays instead of Python loops. | [Video 58](58-batch-gradient-descent/note.md) |
| Vectorization | Converting data such as text into vectors of numbers. | [Video 11](11-tensors/note.md) |
| View Page Source | Browser option that shows a page's raw HTML. | [Video 18](18-web-scraping/note.md) |
| Vocabulary | The list of unique words in a set of texts. | [Video 11](11-tensors/note.md) |
| Vowpal Wabbit | A fast learning library that supports online learning. | [Video 5](05-online-learning/note.md) |
| Wayback Machine | A web archive that keeps copies of web pages as they were. | [Video 18](18-web-scraping/note.md) |
| Web scraping | Writing code that extracts data from web pages. | [Video 7](07-challenges-in-ml/note.md) |
| Weight-based algorithm | An algorithm that learns one number per input column from all the points; sensitive to outliers. | [Video 41](41-what-are-outliers/note.md) |
| Winsorization | Capping with limits set by percentiles. | [Video 41](41-what-are-outliers/note.md) |
| X, y | Usual names for the input table and the output column. | [Video 11](11-tensors/note.md) |
| XAMPP | A free package that runs a web server and a MySQL server on one computer. | [Video 16](16-working-with-json-and-sql/note.md) |
| Yeo-Johnson transform | A variation of Box-Cox that also works on zero and negative values; scikit-learn's default. | [Video 31](31-power-transformer/note.md) |
| Z-score method | Outlier detection that flags values more than 3 standard deviations from the mean; for roughly normal columns. | [Video 42](42-outliers-zscore/note.md) |
| Z-score normalization | Another name for standardization. | [Video 24](24-standardization/note.md) |
| Z-score | A value after standardization: how many standard deviations it lies from the mean. | [Video 24](24-standardization/note.md) |
