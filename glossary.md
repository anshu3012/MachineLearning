# Glossary

Every ML term in the notes, in plain English, with the Note that first explains it.

| Term | Meaning | First explained |
|---|---|---|
| $1/(1-\beta)$ | The rough number of recent values the EWMA averages over: 10 for $\beta = 0.9$. | [DL Note 1033](1033-exponentially-weighted-moving-average/note.md) |
| $\alpha$ (Pareto shape) | The tail index: larger means a thinner tail. | [Maths Note 262](262-pareto-and-power-law/note.md) |
| $\alpha$ | One minus the confidence level: the share of intervals that miss the parameter. | [Maths Note 280](280-confidence-intervals-z-procedure/note.md) |
| $\beta$ (beta) | The EWMA's constant between 0 and 1: the weight kept on the past; usually 0.9 in deep learning. | [DL Note 1033](1033-exponentially-weighted-moving-average/note.md) |
| $\beta$ | The probability of a Type II error. | [Maths Note 292](292-errors-power-and-tails/note.md) |
| $\beta_1$, $\beta_2$ | Adam's decay factors for $m_t$ and $v_t$; defaults 0.9 and 0.999. | [DL Note 1038](1038-adam/note.md) |
| $\binom{n}{k}$ ($n$ choose $k$) | The number of ways to choose $k$ items out of $n$. | [Maths Note 241](241-pmf-and-discrete-cdf/note.md) |
| $\delta$ (Huber) | The error size where Huber loss switches from squared to absolute; a hyperparameter. | [DL Note 1014](1014-dl-loss-functions/note.md) |
| $\epsilon$ (epsilon) | A tiny number added to the variance to avoid dividing by 0; 0.001 in Keras. | [DL Note 1031](1031-batch-normalization/note.md) |
| $\gamma$ (scale) and $\beta$ (shift) | The two learnable parameters per node of a batch normalisation layer; start at 1 and 0 in Keras. | [DL Note 1031](1031-batch-normalization/note.md) |
| $\hat{\mu}$ | An estimate of the population mean $\mu$. | [Maths Note 272](272-estimating-a-mean-with-the-clt/note.md) |
| $\int_a^b f(x)\,dx$ | The area under $f$ from $a$ to $b$; for a PDF, $P(a \le X \le b)$. | [Maths Note 242](242-pdf-and-continuous-cdf/note.md) |
| $\partial L/\partial z$ | The derivative of the loss with respect to a node's weighted sum; every weight entering the node multiplies it by its own input. | [DL Note 1016](1016-backpropagation-how/note.md) |
| $\Phi(z)$ | The CDF of the standard normal distribution: the area to the left of $z$. | [Maths Note 251](251-standard-normal-and-z-table/note.md) |
| $\phi(z)$ | The PDF of the standard normal distribution. | [Maths Note 251](251-standard-normal-and-z-table/note.md) |
| $\text{Lognormal}(\mu, \sigma^2)$ | The distribution of $X$ when $\ln X \sim N(\mu, \sigma^2)$. | [Maths Note 261](261-uniform-and-log-normal/note.md) |
| $\theta$ (theta) | One symbol for all the parameters of a model. | [Maths Note 631](631-maximum-likelihood-estimation/note.md) |
| $A^{\mathsf T}A$ | The symmetric, positive semi-definite matrix whose eigenvectors are the right singular vectors and whose eigenvalues are the squared singular values. | [Maths Note 611](611-computing-the-svd/note.md) |
| $b_{ij}$ | The bias of node $j$ in layer $i$. | [DL Note 1008](1008-mlp-notation/note.md) |
| $N(\mu, \sigma^2)$ | A normal distribution with mean $\mu$ and variance $\sigma^2$. | [Maths Note 250](250-normal-distribution/note.md) |
| $O_{ij}$ | The output of node $j$ in layer $i$. | [DL Note 1008](1008-mlp-notation/note.md) |
| $P(X = x)$ | The probability that the random variable $X$ takes the value $x$. | [Maths Note 241](241-pmf-and-discrete-cdf/note.md) |
| $P(X = x, Y = y)$ | The joint probability that $X$ takes the value $x$ and $Y$ the value $y$ together. | [Maths Note 341](341-joint-marginal-conditional-probability/note.md) |
| $V_0$ | The starting value of the EWMA: 0, or the first value $\theta_1$. | [DL Note 1033](1033-exponentially-weighted-moving-average/note.md) |
| $W^{k}_{ij}$ | The weight entering layer $k$, from node $i$ of layer $k-1$ to node $j$ of layer $k$. | [DL Note 1008](1008-mlp-notation/note.md) |
| $w_0$ | The constant term; it shifts the hyperplane away from the origin, and is 0 when the hyperplane passes through the origin. | [Maths Note 363](363-equation-of-a-hyperplane/note.md) |
| $W_i$, $W_h$, $W_o$ | Input weights, recurrent (feedback) weights and output weights of an RNN. | [DL Note 1056](1056-rnn-forward-propagation/note.md) |
| $x_m$ (Pareto) | The minimum possible value, where the Pareto curve starts and peaks. | [Maths Note 262](262-pareto-and-power-law/note.md) |
| $Y \sim \text{Po}(\lambda)$ | Notation: $Y$ follows a Poisson distribution with rate $\lambda$; likewise $\text{Bern}(p)$ and $B(n, p)$. | [Maths Note 560](560-poisson-distribution/note.md) |
| .dt accessor | The pandas tool that applies date and time methods to every value of a datetime column. | [Note 34](34-date-and-time/note.md) |
| .str accessor | The pandas tool that applies a text method to every value of a column. | [Note 33](33-mixed-variables/note.md) |
| 0-1 loss | A loss that counts 1 for every misclassified point and 0 for every correct one. | [DL Note 1006](1006-perceptron-loss/note.md) |
| 2D density plot | A plot of the joint density of two numerical columns, usually as filled contours. | [Maths Note 253](253-pdf-and-cdf-in-practice/note.md) |
| 3D scatter plot | A scatter plot of three numerical columns on three axes. | [Maths Note 223](223-frequency-tables-and-graphs/note.md) |
| 4-3-2-1 network | A network described by its layer sizes, input first. | [DL Note 1008](1008-mlp-notation/note.md) |
| 5% rule of thumb | Apply CCA only to columns missing less than about 5% of their values. | [Note 35](35-complete-case-analysis/note.md) |
| 68-95-99.7 rule (empirical rule) | In a normal column, about 68.3%, 95.4% and 99.7% of values lie within 1, 2 and 3 standard deviations of the mean. | [Note 42](42-outliers-zscore/note.md) |
| 80-20 rule (Pareto principle) | About 20% of the causes produce about 80% of the results, e.g. 20% of people hold 80% of the wealth. | [Maths Note 262](262-pareto-and-power-law/note.md) |
| @ (matrix multiplication) | Python's operator for multiplying matrices and vectors. | [Note 55](55-multiple-lr-code/note.md) |
| `add_indicator=True` | The `SimpleImputer` setting that imputes and appends missing indicators in one step. | [Note 38](38-missing-indicator-random-sample/note.md) |
| `alternative` (scipy) | The argument of scipy's tests that sets the direction of $H_1$: `"two-sided"`, `"less"` or `"greater"`. | [Maths Note 301](301-one-sample-t-test/note.md) |
| `base_score` | XGBoost's starting prediction; a probability for classification. | [Note 125](125-xgboost-classification/note.md) |
| `batch_size=1` | Keras setting that updates the weights after every single row. | [DL Note 1016](1016-backpropagation-how/note.md) |
| `batch_size` | Keras setting: the number of rows used for each update; $n$, 1 or in between gives batch, stochastic or mini-batch. | [DL Note 1020](1020-gradient-descent-in-neural-networks/note.md) |
| `BatchNormalization` | The Keras layer for batch normalisation. | [DL Note 1031](1031-batch-normalization/note.md) |
| `BayesianRidge` | A linear regression with built-in shrinkage of the weights; the default model of `IterativeImputer`. | [Note 40](40-iterative-imputer-mice/note.md) |
| `best_params_` | The best combination of settings found by `GridSearchCV`. | [Note 38](38-missing-indicator-random-sample/note.md) |
| `build_model(hp)` | The function that builds and compiles one network, asking `hp` for each tuned value. | [DL Note 1039](1039-keras-tuner/note.md) |
| `bw_adjust` | seaborn's multiplier on its default KDE bandwidth. | [Maths Note 243](243-density-estimation-kde/note.md) |
| `clip` | pandas method that moves every value below a lower bound up to it and every value above an upper bound down to it. | [Note 44](44-outliers-percentile/note.md) |
| `cv_results_` | The scores of every combination tried by `GridSearchCV`. | [Note 38](38-missing-indicator-random-sample/note.md) |
| `Dropout` layer | Keras layer that switches off a fraction $p$ of the previous layer's outputs at each training step; inactive at prediction. | [DL Note 1025](1025-dropout-code/note.md) |
| `EarlyStopping` | The Keras callback that stops training when a monitored quantity stops improving. | [DL Note 1022](1022-early-stopping/note.md) |
| `Embedding` layer | The Keras layer holding the embedding matrix $E$; looks up one row per word. | [DL Note 1057](1057-rnn-sentiment-analysis/note.md) |
| `enable_iterative_imputer` | The import that switches on the experimental `IterativeImputer`. | [Note 40](40-iterative-imputer-mice/note.md) |
| `ewm` | The pandas method for exponentially weighted calculations; `alpha` $= 1 - \beta$. | [DL Note 1033](1033-exponentially-weighted-moving-average/note.md) |
| `fill_value` | The value `SimpleImputer` uses with `strategy="constant"`. | [Note 36](36-imputing-numerical-data/note.md) |
| `fillna` | The pandas method that replaces every `NaN` with a given value. | [Note 36](36-imputing-numerical-data/note.md) |
| `find`, `find_all` | Return the first matching tag, or a list of all matching tags. | [Note 18](18-web-scraping/note.md) |
| `fit` | Trains the model on given inputs and outputs for a number of epochs. | [DL Note 1011](1011-customer-churn-ann/note.md) |
| `get_weights()` / `set_weights()` | Keras methods that read and replace a model's weight and bias arrays. | [DL Note 1029](1029-weight-initialization/note.md) |
| `get_weights()` | Returns a layer's weight matrix and bias vector. | [DL Note 1011](1011-customer-churn-ann/note.md) |
| `get_weights` | Keras method that returns every weight and bias array of a model. | [DL Note 1026](1026-regularization-in-dl/note.md) |
| `GridSearchCV` | The scikit-learn class that cross-validates every combination of settings in a grid and keeps the best. | [Note 29](29-pipelines/note.md) |
| `hp.Choice` | Declares a hyperparameter that takes one value from a list. | [DL Note 1039](1039-keras-tuner/note.md) |
| `hp.Float` | Declares a decimal hyperparameter in a range; `sampling="log"` spreads its values evenly over powers of ten. | [DL Note 1039](1039-keras-tuner/note.md) |
| `hp.Int` | Declares a whole-number hyperparameter between a minimum and a maximum, with an optional step. | [DL Note 1039](1039-keras-tuner/note.md) |
| `ignore_index` | Setting of `pd.concat` that renumbers the joined rows from 0. | [Note 17](17-fetching-data-from-api/note.md) |
| `IterativeImputer` | scikit-learn's class for MICE; still experimental. | [Note 40](40-iterative-imputer-mice/note.md) |
| `json_normalize` | pandas function that turns nested JSON into flat columns. | [Note 17](17-fetching-data-from-api/note.md) |
| `keras.datasets.mnist` | Keras's built-in copy of MNIST, already split 60,000 / 10,000. | [DL Note 1012](1012-mnist-ann/note.md) |
| `keras.Input` | The first item of a Sequential model; gives the shape of one input row. | [DL Note 1011](1011-customer-churn-ann/note.md) |
| `keras.optimizers.SGD` | Plain gradient descent in Keras, with a fixed learning rate. | [DL Note 1016](1016-backpropagation-how/note.md) |
| `kernel_initializer` | The `Dense` argument that chooses how a layer's weight matrix starts; default `glorot_uniform`. | [DL Note 1030](1030-xavier-he-initialization/note.md) |
| `kernel_regularizer` | Keras `Dense` setting that adds an L1 or L2 penalty on the layer's weights. | [DL Note 1026](1026-regularization-in-dl/note.md) |
| `KernelDensity` | scikit-learn's KDE; `score_samples` returns log densities. | [Maths Note 243](243-density-estimation-kde/note.md) |
| `KNNImputer` | scikit-learn's class for KNN imputation. | [Note 39](39-knn-imputer/note.md) |
| `lru_cache` | Python's built-in memoization: it stores the results of a function automatically. | [DL Note 1019](1019-mlp-memoization/note.md) |
| `make_circles` | scikit-learn function that generates two concentric rings of observations, one ring per class. | [DL Note 1027](1027-activation-functions/note.md) |
| `make_moons` | scikit-learn function that generates two interleaving half-moon classes. | [DL Note 1018](1018-vanishing-exploding-gradients/note.md) |
| `max_iter` (IterativeImputer) | The largest number of rounds `IterativeImputer` runs; default 10. | [Note 40](40-iterative-imputer-mice/note.md) |
| `max_iter` (KMeans) | The largest number of assign-and-move rounds k-means may run. | [Note 130](130-kmeans-from-scratch/note.md) |
| `max_iter` (LogisticRegression) | The largest number of solver iterations; default 100, raised when a ConvergenceWarning appears. | [Note 81](81-logistic-hyperparameters/note.md) |
| `max_iter` (SGDRegressor) | The maximum number of epochs in `SGDRegressor`. | [Note 59](59-stochastic-gradient-descent/note.md) |
| `min_child_weight` | Smallest allowed sum of $p(1-p)$ (in regression: number of rows) in a leaf; default 1. | [Note 125](125-xgboost-classification/note.md) |
| `min_delta` | The smallest change of the monitored quantity that counts as an improvement. | [DL Note 1022](1022-early-stopping/note.md) |
| `MissingIndicator` | The scikit-learn class that builds missing indicator columns; `features_` lists the columns with gaps. | [Note 38](38-missing-indicator-random-sample/note.md) |
| `model.summary()` | Prints each layer's output shape and number of trainable parameters. | [DL Note 1011](1011-customer-churn-ann/note.md) |
| `n_neighbors` (k) | The number of nearest rows the KNN imputer averages; default 5. | [Note 39](39-knn-imputer/note.md) |
| `normalize` (`pd.crosstab`) | Turns counts into probabilities: `"all"` joint, `"index"` per row, `"columns"` per column. | [Maths Note 341](341-joint-marginal-conditional-probability/note.md) |
| `np.where` | NumPy function that picks one value where a condition is true and another where it is false. | [Note 42](42-outliers-zscore/note.md) |
| `pd.concat` | pandas function that joins several DataFrames into one. | [Note 17](17-fetching-data-from-api/note.md) |
| `quantile` | pandas method that returns a percentile, given as a fraction (0.25 for the 25th). | [Note 43](43-outliers-iqr/note.md) |
| `random_state` | A seed that fixes a random draw, so the same code gives the same result. | [Note 38](38-missing-indicator-random-sample/note.md) |
| `RandomSearch` | A tuner that tries random combinations of the hyperparameter values. | [DL Note 1039](1039-keras-tuner/note.md) |
| `read_json` | pandas function that reads JSON from a file or a URL into a DataFrame. | [Note 16](16-working-with-json-and-sql/note.md) |
| `read_sql_query` | pandas function that runs an SQL query and returns a DataFrame. | [Note 16](16-working-with-json-and-sql/note.md) |
| `reg_covar` | scikit-learn's small number added to the covariance diagonals so no component collapses. | [Maths Note 640](640-gaussian-mixture-models/note.md) |
| `RepeatVector` | Keras layer that repeats one vector at several time steps. | [DL Note 1058](1058-types-of-rnn/note.md) |
| `restore_best_weights` | `EarlyStopping` setting that puts back the weights of the best epoch at the end. | [DL Note 1022](1022-early-stopping/note.md) |
| `return_sequences` | SimpleRNN argument: `False` returns the last hidden state, `True` returns every hidden state. | [DL Note 1057](1057-rnn-sentiment-analysis/note.md) |
| `rho` | Keras' name for RMSProp's decay factor $\beta$; default 0.9. | [DL Note 1037](1037-rmsprop/note.md) |
| `sample(n)` | The pandas method that draws `n` values at random from a Series or DataFrame. | [Note 38](38-missing-indicator-random-sample/note.md) |
| `sample_posterior` | Draw each fill at random from the model's spread, giving several plausible filled tables. | [Note 40](40-iterative-imputer-mice/note.md) |
| `set_weights` / `get_weights` | Keras methods to write and read a model's weights and biases, as a list of arrays. | [DL Note 1016](1016-backpropagation-how/note.md) |
| `shuffle=False` | Keras setting that keeps the rows in their original order in every epoch. | [DL Note 1016](1016-backpropagation-how/note.md) |
| `SimpleRNN` | The Keras layer for a basic RNN; input shape (batch size, time steps, input features). | [DL Note 1056](1056-rnn-forward-propagation/note.md) |
| `statistics_` | The fill values a fitted `SimpleImputer` has learned, one per column. | [Note 36](36-imputing-numerical-data/note.md) |
| `step__param` name | The full name of a setting inside a pipeline: step names and the parameter joined by `__`. | [Note 29](29-pipelines/note.md) |
| `strategy="constant"` (SimpleImputer) | The `SimpleImputer` setting that fills every gap with `fill_value`. | [Note 37](37-missing-categorical-data/note.md) |
| `strategy="most_frequent"` (SimpleImputer) | The `SimpleImputer` setting for mode imputation. | [Note 37](37-missing-categorical-data/note.md) |
| `strategy` (KBinsDiscretizer) | The `KBinsDiscretizer` parameter choosing uniform, quantile or kmeans binning. | [Note 32](32-binning-binarization/note.md) |
| `strategy` (SimpleImputer) | The `SimpleImputer` parameter choosing the fill rule: mean, median, most_frequent or constant. | [Note 36](36-imputing-numerical-data/note.md) |
| `to_categorical` | Keras function that one-hot encodes integer labels. | [DL Note 1012](1012-mnist-ann/note.md) |
| `tol` | The size of change below which `IterativeImputer` stops early; default 0.001. | [Note 40](40-iterative-imputer-mice/note.md) |
| `validation_split` | The share of the training rows Keras holds back as a validation set. | [DL Note 1011](1011-customer-churn-ann/note.md) |
| A/B testing | Comparing an old and a new version on two random groups of users. | [Note 9](09-mldlc/note.md) |
| Absolute value | A number's size without its sign. | [Note 25](25-normalization/note.md) |
| absolute_error | A criterion that splits by mean absolute error; leaves predict the median. | [Note 99](99-regression-trees/note.md) |
| Accumulator $v_t$ | The running record of squared gradients that divides the learning rate. | [DL Note 1037](1037-rmsprop/note.md) |
| Accuracy | The fraction of predictions that are correct. | [Note 13](13-toy-project/note.md) |
| Acquisition function | The rule that picks the next trial from the surrogate, such as expected improvement. | [Note 134](134-optuna/note.md) |
| Activation ($a^{k}$) | The vector of outputs of layer $k$; $a^{0}$ is the input row. | [DL Note 1010](1010-forward-propagation/note.md) |
| Activation function | The function that turns $z$ into the output, bringing it into a fixed range. | [DL Note 1004](1004-perceptron/note.md) |
| Active constraint | An inequality constraint that holds with equality at the answer; its multiplier can be positive. | [Maths Note 620](620-lagrange-multipliers/note.md) |
| AdaBoost (Adaptive Boosting) | A boosting algorithm that trains weak learners in sequence on reweighted data and combines them by an alpha-weighted vote. | [Note 115](115-adaboost-intuition/note.md) |
| AdaGrad | An optimizer that gives each parameter its own learning rate, $\eta/(\sqrt{v_t}+\epsilon)$, where $v_t$ sums its past squared gradients. | [DL Note 1036](1036-adagrad/note.md) |
| Adam | The optimizer used in these projects; optimizers are taught later. | [DL Note 1011](1011-customer-churn-ann/note.md) |
| AdamW | Adam with true weight decay applied directly to the weights, not through the loss. | [DL Note 1026](1026-regularization-in-dl/note.md) |
| Adaptive learning rate | A learning rate that changes during training according to the gradients seen so far. | [DL Note 1036](1036-adagrad/note.md) |
| Addition rule | For mutually exclusive events, $P(A \cup B) = P(A) + P(B)$. | [Note 84](84-mutually-exclusive-events/note.md) |
| Additive modelling | Building a complex function as a sum of simple functions, each capturing part of what the others missed. | [Note 121](121-gradient-boosting-regression-maths/note.md) |
| Adjusted Rand index (ARI) | A score for how well a clustering matches the true groups: 1 for identical, about 0 for random. | [Maths Note 640](640-gaussian-mixture-models/note.md) |
| Adjusted Rand score | A number that is 1.0 when two labelings group the points identically, whatever the label numbers. | [Note 130](130-kmeans-from-scratch/note.md) |
| Adjusted R² | R² with a penalty for the number of input columns. | [Note 52](52-regression-metrics/note.md) |
| Affine transformation | A linear transformation followed by a shift, $A\mathbf{x} + \mathbf{b}$. | [Maths Note 500](500-linear-transformations-and-matrices/note.md) |
| Agent | The learner in reinforcement learning. | [Note 3](03-types-of-ml/note.md) |
| Agglomerative clustering | Bottom-up hierarchical clustering: start with one cluster per point and merge the closest pair repeatedly. | [Note 131](131-hierarchical-clustering/note.md) |
| AgglomerativeClustering | scikit-learn's class for agglomerative clustering. | [Note 131](131-hierarchical-clustering/note.md) |
| Aggregate | One summary number (mean, median, maximum, ...) computed from a group of values. | [Maths Note 223](223-frequency-tables-and-graphs/note.md) |
| Aggregation | Combining the base models' predictions into one: mode for classes, mean for numbers. | [Note 105](105-bagging-intuition/note.md) |
| AGI (artificial general intelligence) | A machine with all the abilities of human intelligence. Does not exist yet. | [Note 2](02-ai-vs-ml-vs-dl/note.md) |
| AI winter | A period when funding and interest in AI collapse. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| Alert | A warning in the report about a column that may need attention. | [Note 22](22-pandas-profiling/note.md) |
| AlexNet | The deep network on GPUs that won ImageNet 2012. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| Alpha (model weight) | A base model's say in AdaBoost's final vote; larger when it made fewer mistakes. | [Note 115](115-adaboost-intuition/note.md) |
| Alternative hypothesis ($H_1$, $H_a$) | The statement that contradicts $H_0$ and claims an effect, difference or relationship. | [Maths Note 290](290-null-and-alternative-hypotheses/note.md) |
| Anaconda Navigator | Anaconda's point-and-click window for environments and packages. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| Anaconda | The best-known data science distribution, with Navigator and Spyder. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| Analytic function | A function equal to its Taylor series near every point. | [Maths Note 600](600-derivatives-of-one-variable/note.md) |
| AND, OR | Logic functions: 1 when both inputs are 1 (AND), or when at least one is (OR). | [DL Note 1007](1007-problem-with-perceptron/note.md) |
| Anderson-Darling test | Another statistical test of whether data follows a given distribution. | [Maths Note 260](260-kurtosis-and-qq-plots/note.md) |
| Anomaly detection | Finding rows that do not fit the pattern of the rest. | [Note 3](03-types-of-ml/note.md) |
| ANOVA table | The table of SS, df, MS, F and p for each source of variation. | [Maths Note 572](572-one-way-anova/note.md) |
| ANOVA | Analysis of variance: a test comparing the means of several groups. | [Maths Note 572](572-one-way-anova/note.md) |
| API (Application Programming Interface) | A service that returns data when our code asks for it; a website's API hands out its data on request. | [Note 7](07-challenges-in-ml/note.md) |
| API key | A secret code that tells the API who is asking. | [Note 17](17-fetching-data-from-api/note.md) |
| API token | A secret file or key that lets a program use a website's API as us. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| Approximate tree learning (histogram-based training) | Finding a split by trying only the edges of bins the column has been cut into. | [Note 123](123-xgboost-intro/note.md) |
| Arbitrary value imputation | Filling every gap with one fixed value that never occurs, such as 99 or $-1$. | [Note 36](36-imputing-numerical-data/note.md) |
| Architecture (of a network) | How a network's nodes are connected: how many, of what kind, and which connections. | [DL Note 1002](1002-what-is-deep-learning/note.md) |
| arg max | The value of the variable that makes an expression largest. | [Note 88](88-naive-bayes-maths/note.md) |
| Arg min | The value of a variable that makes an expression smallest, written $\arg\min$. | [Note 121](121-gradient-boosting-regression-maths/note.md) |
| argmax | The position of the largest value; on 10 class probabilities, the predicted class. | [DL Note 1012](1012-mnist-ann/note.md) |
| argmin | The values of the variables that make an expression smallest. | [DL Note 1006](1006-perceptron-loss/note.md) |
| Array | The programming name for a tensor (as in NumPy). | [Note 11](11-tensors/note.md) |
| Artificial Intelligence (AI) | The field of building machines that show intelligence. | [Note 2](02-ai-vs-ml-vs-dl/note.md) |
| Artificial neural network (ANN) | The simplest neural network: neurons in layers, each layer connected to the next by weights. | [DL Note 1002](1002-what-is-deep-learning/note.md) |
| ASIC | A chip custom-made for one job, such as the TPU. | [DL Note 1002](1002-what-is-deep-learning/note.md) |
| Association rule learning | Finding items that tend to occur together. | [Note 3](03-types-of-ml/note.md) |
| Associativity | $(AB)C = A(BC)$: the grouping of a product does not matter. | [Maths Note 510](510-matrix-multiplication-as-composition/note.md) |
| Assumption (of a model) | A condition the data must meet for the model's results to be reliable. | [Note 56](56-linear-regression-assumptions/note.md) |
| Asymptotic | Coming ever closer to a line without touching it, like the normal curve's tails and the x axis. | [Maths Note 250](250-normal-distribution/note.md) |
| Atomic value | A single piece of information in a cell, not several combined. | [Note 45](45-feature-construction-splitting/note.md) |
| Attention | A mechanism that lets each output step weigh all input positions and focus on the useful ones. | [DL Note 1067](1067-history-of-llms/note.md) |
| Attribute | A `name="value"` setting inside an opening tag. | [Note 18](18-web-scraping/note.md) |
| AUC | The area under the ROC curve; a single score from 0.5 (random) to 1 (perfect). | [Note 78](78-roc-auc/note.md) |
| Autocorrelation | Each residual is related to the one before it in row order. | [Note 56](56-linear-regression-assumptions/note.md) |
| Autoencoder | A network with a narrow middle layer that learns to compress data and rebuild it. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| Automatic differentiation | Software that computes exact derivatives of a program by the chain rule on its elementary operations; reverse mode is backpropagation. | [Maths Note 602](602-jacobian-and-matrix-gradients/note.md) |
| Average linkage | Cluster distance = mean of all distances between the two clusters' points. | [Note 131](131-hierarchical-clustering/note.md) |
| Average record size | The memory one row takes, on average. | [Note 22](22-pandas-profiling/note.md) |
| Axioms of probability | The three rules every probability obeys: non-negative, $P(S) = 1$, mutually exclusive events add. | [Maths Note 331](331-empirical-and-theoretical-probability/note.md) |
| Axis of rotation | The line a 3D rotation leaves in place: an eigenvector with eigenvalue 1. | [Maths Note 530](530-eigenvectors-and-eigenvalues/note.md) |
| Axis | One direction along which a tensor's items are arranged. | [Note 11](11-tensors/note.md) |
| Axis-parallel split | A cut that tests one column, so it is a line, plane or hyperplane parallel to the other axes. | [Note 97](97-decision-trees-intuition/note.md) |
| B2B | Business to business: a product that helps a company run its business. | [Note 8](08-applications-of-ml/note.md) |
| B2C | Business to customer: a product sold to ordinary users. | [Note 8](08-applications-of-ml/note.md) |
| Backpropagation through time (BPTT) | Backpropagation applied to an RNN unfolded in time. | [DL Note 1059](1059-backpropagation-through-time/note.md) |
| Backpropagation | Computing the gradient of a loss by applying the chain rule backward through the computation graph. | [Maths Note 602](602-jacobian-and-matrix-gradients/note.md) |
| Backward elimination | Feature selection that starts with all columns and removes the worst at a time. | [Note 23](23-what-is-feature-engineering/note.md) |
| Bag of words | Turning a text into a vector of word counts over the vocabulary. | [Maths Note 360](360-vectors-and-feature-vectors/note.md) |
| Bagging (bootstrap aggregation) | Averaging many models trained on different samples of the data to reduce variance. | [Note 101](101-ensemble-learning/note.md) |
| Bagging regressor | A bagging ensemble of regressors that predicts the mean of their predictions. | [Note 107](107-bagging-regressor/note.md) |
| BaggingClassifier | scikit-learn class for bagging, pasting, random subspaces and random patches in classification. | [Note 106](106-bagging-classifier/note.md) |
| BaggingRegressor | scikit-learn class for bagging, pasting, random subspaces and random patches in regression. | [Note 107](107-bagging-regressor/note.md) |
| Balanced random forest | A random forest in which every tree is trained on a balanced sample. | [Note 133](133-imbalanced-data/note.md) |
| Bandwidth | The width (for a Gaussian kernel, the standard deviation) of each kernel; sets the KDE's smoothness. | [Maths Note 243](243-density-estimation-kde/note.md) |
| Bar plot | One bar per category, its height the mean of a numerical column. | [Note 21](21-bivariate-multivariate-analysis/note.md) |
| base environment | The environment the installer creates, holding conda itself. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| Base model | One of the models inside an ensemble. | [Note 101](101-ensemble-learning/note.md) |
| Base prediction ($F_0$) | The first model of gradient boosting; for regression, the mean of the target. | [Note 120](120-gradient-boosting-intuition/note.md) |
| Basis | A linearly independent set of vectors that spans the whole space. | [Maths Note 490](490-linear-combinations-span-and-basis/note.md) |
| Batch (mini-batch) | A small group of training observations used for one update; Keras uses 32 by default. | [Note 60](60-mini-batch-gradient-descent/note.md) |
| Batch gradient descent | Gradient descent that uses all training rows for every update. | [Note 58](58-batch-gradient-descent/note.md) |
| Batch learning | Training on the whole dataset at once, offline, then deploying. | [Note 4](04-batch-learning/note.md) |
| Batch normalisation | A layer that re-centres and re-scales the values passing between layers during training. | [DL Note 1018](1018-vanishing-exploding-gradients/note.md) |
| Batch size | The number of rows in each batch; a hyperparameter. | [Note 60](60-mini-batch-gradient-descent/note.md) |
| Bayes' theorem | $P(A \mid B) = P(B \mid A) P(A) / P(B)$: the rule that reverses a conditional probability. | [Note 85](85-bayes-theorem/note.md) |
| Bayesian optimisation | Tuning that models the score as a function of the hyperparameters and uses all earlier trials to choose the next one. | [Note 134](134-optuna/note.md) |
| Bayesian statistics | The branch of statistics that treats probabilities as beliefs updated by Bayes' theorem. | [Note 85](85-bayes-theorem/note.md) |
| BeautifulSoup | Python library that parses HTML into a searchable tree. | [Note 18](18-web-scraping/note.md) |
| Bell curve | The curve of a normal distribution. | [Note 42](42-outliers-zscore/note.md) |
| Bernoulli distribution | One trial with two outcomes: 1 with probability $p$, 0 with probability $1 - p$. | [Maths Note 241](241-pmf-and-discrete-cdf/note.md) |
| Bernoulli trial | One random experiment with exactly two outcomes, success (1) and failure (0). | [Maths Note 270](270-bernoulli-and-binomial/note.md) |
| BernoulliNB | Naive Bayes for binary (yes/no) inputs. | [Note 90](90-gaussian-naive-bayes/note.md) |
| Bessel's correction | Dividing by $n - 1$ instead of $n$, so the sample variance is right on average. | [Maths Note 222](222-measures-of-dispersion/note.md) |
| Best-fit line | The line with the smallest total error over all the training points. | [Note 50](50-simple-linear-regression/note.md) |
| best_score_ | The best mean cross-validated score found by a search. | [Note 29](29-pipelines/note.md) |
| Beta testing | Releasing a new version to a small group of trusted users first. | [Note 9](09-mldlc/note.md) |
| BFGS | The most used quasi-Newton update; keeps the Hessian stand-in symmetric and positive definite. | [Maths Note 603](603-hessian-and-multivariate-taylor/note.md) |
| Bias (of a perceptron) | The weight on a constant input of 1; it shifts the boundary away from the origin. | [DL Note 1004](1004-perceptron/note.md) |
| Bias correction | Dividing an EWMA started at 0 by $1 - \beta^t$ so it is not too small in the first steps. | [DL Note 1038](1038-adam/note.md) |
| Bias vector ($b^{k}$) | The biases of all nodes of layer $k$. | [DL Note 1010](1010-forward-propagation/note.md) |
| Bias | Error from a model being too simple to capture the true relationship. | [Note 62](62-bias-variance/note.md) |
| Bias-variance trade-off | Lowering bias by adding complexity tends to raise variance, and the reverse. | [Note 62](62-bias-variance/note.md) |
| Biased estimator | An estimator that is systematically too high or too low on average. | [Maths Note 632](632-mle-for-common-distributions/note.md) |
| Biased model | A model pushed towards wrong answers, e.g. by bad data. | [Note 5](05-online-learning/note.md) |
| Big picture | The end product and how it will be used, which decides the type of ML problem. | [Note 14](14-framing-ml-problem/note.md) |
| Bimodal | A distribution with two peaks. | [Note 31](31-power-transformer/note.md) |
| Bin edge | A boundary between two neighbouring bins. | [Note 32](32-binning-binarization/note.md) |
| Bin | One of the equal ranges a histogram splits the data into. | [Note 20](20-univariate-analysis/note.md) |
| bin_edges_ | The fitted `KBinsDiscretizer` attribute holding the learned edges. | [Note 32](32-binning-binarization/note.md) |
| Binarization | Turning a continuous column into 0 or 1 by comparing it with one threshold. | [Note 32](32-binning-binarization/note.md) |
| Binarizer | scikit-learn's class for binarization, with parameters `threshold` and `copy`. | [Note 32](32-binning-binarization/note.md) |
| Binary classifier | A model that separates exactly two classes. | [DL Note 1004](1004-perceptron/note.md) |
| Binary cross entropy (log loss) | The average cross entropy for two classes, the loss function of logistic regression. | [Note 73](73-log-loss/note.md) |
| Binary file | A file that is not plain text, such as a saved model. | [Note 9](09-mldlc/note.md) |
| Binning | Grouping a numerical column into ranges that act as categories. | [Note 23](23-what-is-feature-engineering/note.md) |
| Binomial distribution | The distribution of the number of successes in $n$ independent trials with the same success probability. | [Note 102](102-voting-ensemble/note.md) |
| Binomial experiment | A fixed number $n$ of independent Bernoulli trials with the same success probability $p$. | [Maths Note 270](270-bernoulli-and-binomial/note.md) |
| Bivariate analysis | Studying two variables together. | [Note 20](20-univariate-analysis/note.md) |
| Black box model | A model that gives predictions without showing how each input contributed. | [Note 91](91-knn/note.md) |
| Blending | Stacking in which the meta-model is trained on the base models' predictions for a hold-out validation set. | [Note 127](127-stacking-blending/note.md) |
| BLEU score | A measure of translation quality: how many word sequences of a translation match a human reference. | [DL Note 1067](1067-history-of-llms/note.md) |
| BMI | Body mass index: weight (kg) divided by height (m) squared. | [Note 7](07-challenges-in-ml/note.md) |
| Boolean indexing | Selecting rows with an array of True/False values, e.g. `X[y_means == 0]`. | [Note 129](129-kmeans-code/note.md) |
| Boosting | Combining many simple models in sequence to reduce bias. | [Note 62](62-bias-variance/note.md) |
| Bootstrap sample | A sample of the same size drawn from the data with replacement. | [Note 66](66-ridge-key-points/note.md) |
| bootstrap | BaggingClassifier setting: draw rows with replacement (True, bagging) or without (False, pasting). | [Note 106](106-bagging-classifier/note.md) |
| bootstrap_features | BaggingClassifier setting: draw columns with replacement or without. | [Note 106](106-bagging-classifier/note.md) |
| Bootstrapping | Drawing random samples of the data to train each base model. | [Note 101](101-ensemble-learning/note.md) |
| Border point | A point with fewer than MinPts points within eps, but with a core point among them. | [Note 132](132-dbscan/note.md) |
| Boston housing data | 506 Boston districts, 13 inputs and the median home value; removed from scikit-learn in version 1.2. | [Note 99](99-regression-trees/note.md) |
| Bot | A program that visits websites automatically. | [Note 18](18-web-scraping/note.md) |
| Box plot | A graph of the five-number summary, with outliers drawn as dots. | [Note 20](20-univariate-analysis/note.md) |
| Box-and-whisker plot | Another name for a box plot. | [Maths Note 230](230-percentiles-and-box-plots/note.md) |
| Box-Cox transform | $(x^\lambda - 1)/\lambda$, or $\ln x$ when $\lambda = 0$; works only on values above 0. | [Note 31](31-power-transformer/note.md) |
| Branch (subtree) | A node together with everything below it. | [Note 97](97-decision-trees-intuition/note.md) |
| Broadcasting | NumPy stretching a scalar (or smaller array) to match a bigger array before an operation. | [Maths Note 361](361-magnitude-distance-and-scalar-operations/note.md) |
| Buying behaviour | The pattern of what a customer buys. | [Note 8](08-applications-of-ml/note.md) |
| C (SVM) | The weight on the classification error; a large C means few mistakes and a narrow margin, a small C a wide margin. | [Note 94](94-svm-soft-margin/note.md) |
| C | The inverse of the regularisation strength in LogisticRegression; smaller C means stronger regularisation. | [Note 81](81-logistic-hyperparameters/note.md) |
| Cache memory | A small, fast memory inside the processor that holds data used again and again. | [Note 123](123-xgboost-intro/note.md) |
| Calculus | The branch of mathematics about change: differentiation and integration. | [Maths Note 440](440-role-of-maths-in-ml/note.md) |
| CalibratedClassifierCV | scikit-learn wrapper that gives a classifier, such as an SVM, calibrated probabilities. | [Note 103](103-voting-classifier/note.md) |
| Callback | An object whose code Keras runs at set points during training, for example after every epoch. | [DL Note 1022](1022-early-stopping/note.md) |
| Capping | Replacing every value beyond a limit with the limit itself. | [Note 41](41-what-are-outliers/note.md) |
| cars.csv | dtreeviz's sample data: 392 cars with MPG, weight, engine size and cylinders. | [Note 100](100-dtreeviz/note.md) |
| CART | Classification and regression trees: the tree algorithm used for both kinds of problem. | [Note 97](97-decision-trees-intuition/note.md) |
| CatBoost | Yandex's gradient boosting library, with built-in handling of categorical columns. | [Note 123](123-xgboost-intro/note.md) |
| Categorical cross entropy | The loss of softmax regression: the average of −log(probability of the true class). | [Note 79](79-softmax-regression/note.md) |
| Categorical cross-entropy | $-\sum_j y_j \log \hat{y}_j$ with one-hot labels; the loss for more than two classes, with a softmax output. | [DL Note 1014](1014-dl-loss-functions/note.md) |
| Categorical data (categorical column) | Data made of categories: labels rather than numbers. | [Note 3](03-types-of-ml/note.md) |
| Categorical distribution | The distribution of one trial with more than two outcomes; Bernoulli is its two-outcome case. | [Maths Note 270](270-bernoulli-and-binomial/note.md) |
| CategoricalNB | scikit-learn's Naive Bayes for categorical inputs. | [Note 89](89-naive-bayes-code/note.md) |
| categories_ | The attribute holding the categories `OrdinalEncoder` learned, in order. | [Note 26](26-ordinal-label-encoding/note.md) |
| Category share | The rows in one category divided by the rows that have a value. | [Note 37](37-missing-categorical-data/note.md) |
| Category | One of the fixed groups of a categorical column. | [Note 20](20-univariate-analysis/note.md) |
| Causation | A cause-and-effect relationship: changing one thing changes the other. | [Maths Note 231](231-covariance-and-correlation/note.md) |
| ccp_alpha | Cost-complexity pruning strength: the penalty per leaf when a grown tree is pruned back. | [Note 111](111-random-forest-hyperparameters/note.md) |
| Cell | One block of a notebook, holding either code or Markdown. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| Central difference | The numerical derivative $(f(x + h) - f(x - h))/(2h)$, more accurate than a one-sided step. | [Maths Note 600](600-derivatives-of-one-variable/note.md) |
| Central limit theorem | Averages of samples follow a normal distribution, whatever the distribution of the data. | [Maths Note 271](271-sampling-distribution-and-clt/note.md) |
| Centred data | Data whose mean is 0. | [Note 25](25-normalization/note.md) |
| Centroid initialization | Picking the first k centroids, here at random from the data. | [Note 128](128-kmeans-intuition/note.md) |
| Centroid | The centre of one group in k-means. | [Note 32](32-binning-binarization/note.md) |
| Centroid-based clustering | Clustering built around centroids, such as k-means. | [Note 132](132-dbscan/note.md) |
| Chain rule of probability | Writing a joint probability as a product of conditional probabilities, one variable at a time. | [Note 88](88-naive-bayes-maths/note.md) |
| Chain rule with Jacobians | The Jacobian of a composition is the product of the Jacobians, in the same order. | [Maths Note 602](602-jacobian-and-matrix-gradients/note.md) |
| Chain rule | To differentiate a function of a function, multiply the outer derivative by the inner derivative. | [Note 74](74-sigmoid-derivative/note.md) |
| Chained assignment | Selecting part of a DataFrame and then changing that selection in a second step; does nothing in pandas 3. | [Note 45](45-feature-construction-splitting/note.md) |
| Chained equations | One prediction model per column, each using the latest fills of the others. | [Note 40](40-iterative-imputer-mice/note.md) |
| Change of basis matrix | A matrix $P$ whose columns are the new basis vectors. | [Maths Note 530](530-eigenvectors-and-eigenvalues/note.md) |
| Channel | One colour layer of an image (red, green or blue). | [Note 11](11-tensors/note.md) |
| Characteristic polynomial | $\det(A - \lambda I)$; its roots are the eigenvalues. | [Maths Note 530](530-eigenvectors-and-eigenvalues/note.md) |
| Chi-square distribution | The distribution of $\chi^2$ under $H_0$: positive, right-skewed, with one parameter, the degrees of freedom. | [Maths Note 571](571-chi-square-tests/note.md) |
| Chi-square statistic $\chi^2$ | $\sum (O - E)^2 / E$: the total mismatch between observed and expected counts. | [Maths Note 571](571-chi-square-tests/note.md) |
| Chi-square test of independence | A chi-square test of whether two categorical columns are related; $df = (r - 1)(c - 1)$. | [Maths Note 571](571-chi-square-tests/note.md) |
| Chi-square test | A test of whether categorical counts match expected counts (goodness of fit) or whether two categorical columns are related (independence). | [Maths Note 571](571-chi-square-tests/note.md) |
| Chi-squared test (chi2) | A test scoring how strongly a column is linked to the target; needs values of 0 or more. | [Note 29](29-pipelines/note.md) |
| Cholesky solver | A scikit-learn Ridge solver that solves the closed-form equation directly. | [Note 64](64-ridge-regression-maths/note.md) |
| Chord | The straight line joining two points on a function's graph. | [Maths Note 590](590-convex-and-non-convex-cost-functions/note.md) |
| Chunk | A piece of a file, read as a small DataFrame. | [Note 15](15-working-with-csv/note.md) |
| Churn rate | The percentage of customers who leave during a given period. | [Note 14](14-framing-ml-problem/note.md) |
| Churn | Customers leaving a platform or service. | [Note 14](14-framing-ml-problem/note.md) |
| Class prior | The share of training rows in a class. | [Note 87](87-naive-bayes-intuition/note.md) |
| Class | An attribute that labels tags; used to select the right ones. | [Note 18](18-web-scraping/note.md) |
| class_sep | make_classification setting for how far apart the classes are. | [Note 71](71-perceptron-code/note.md) |
| class_weight | A setting that weights each class's mistakes in the loss; "balanced" helps rare classes. | [Note 81](81-logistic-hyperparameters/note.md) |
| classes_ | The attribute holding the classes `LabelEncoder` learned, in order. | [Note 26](26-ordinal-label-encoding/note.md) |
| Classification error (SVM) | The term $\sum \xi_i$ of the SVM loss: the total slack of all points. | [Note 94](94-svm-soft-margin/note.md) |
| Classification metric | A number that measures how well a classification model performs. | [Note 76](76-accuracy-confusion-matrix/note.md) |
| Classification | Supervised learning with a categorical output. | [Note 3](03-types-of-ml/note.md) |
| classification_report | scikit-learn function that prints precision, recall, F1 and support for every class. | [Note 77](77-precision-recall-f1/note.md) |
| Client, server | The program that asks, and the computer that answers. | [Note 17](17-fetching-data-from-api/note.md) |
| Closed-form solution | An answer given directly by a formula of ordinary operations. | [Note 51](51-linear-regression-maths/note.md) |
| Cluster | One group found by clustering. | [Note 3](03-types-of-ml/note.md) |
| cluster_centers_ | The coordinates of the final centroids of a fitted `KMeans`. | [Note 129](129-kmeans-code/note.md) |
| Clustering | Splitting data into groups of similar rows. | [Note 3](03-types-of-ml/note.md) |
| Clustermap | A heatmap with rows and columns reordered so similar ones sit together. | [Note 21](21-bivariate-multivariate-analysis/note.md) |
| Codomain | The set in which a function's outputs lie. | [Maths Note 600](600-derivatives-of-one-variable/note.md) |
| coef_ | The fitted slope (one per input column) in scikit-learn. | [Note 50](50-simple-linear-regression/note.md) |
| Coefficient ($\beta_i$) | The weight of one input column: the change in the output per unit of that input, others fixed. | [Note 53](53-multiple-linear-regression/note.md) |
| Coefficient of variation (CV) | Standard deviation divided by mean: spread relative to the average. | [Note 22](22-pandas-profiling/note.md) |
| Coefficient path | How each coefficient changes as the regularisation strength grows. | [Note 66](66-ridge-key-points/note.md) |
| Coefficient vector ($\beta$) | All the coefficients of the model, $\beta_0$ to $\beta_m$, as one column. | [Note 54](54-multiple-lr-maths/note.md) |
| Column block | XGBoost's storage of the data one sorted column per block, so each core can work on one feature. | [Note 123](123-xgboost-intro/note.md) |
| Column sampling (feature sampling) | Giving each base model a random subset of the columns. | [Note 108](108-random-forest-intro/note.md) |
| Column space | The span of the columns of a matrix: every output it can produce. | [Maths Note 500](500-linear-transformations-and-matrices/note.md) |
| Column transformer | A scikit-learn class that applies different transformations to different columns at once (covered two Notes later). | [Note 26](26-ordinal-label-encoding/note.md) |
| Column vector | A vector written as one column, shape $n \times 1$; the default meaning of "vector". | [Maths Note 360](360-vectors-and-feature-vectors/note.md) |
| ColumnTransformer | The scikit-learn class (in `sklearn.compose`) that implements the column transformer. | [Note 28](28-column-transformer/note.md) |
| Combined sampling | Giving each base model random rows and random columns together. | [Note 108](108-random-forest-intro/note.md) |
| Combining perceptrons | Feeding several perceptrons' outputs, weighted and with a bias, into another perceptron. | [DL Note 1009](1009-mlp-intuition/note.md) |
| Commutative law | $a \cdot b = b \cdot a$. | [Maths Note 362](362-dot-product-and-cosine-similarity/note.md) |
| Compile | Choosing the loss, the optimizer and the metrics before training. | [DL Note 1011](1011-customer-churn-ann/note.md) |
| Complement ($A^c$) | The event that $A$ does not happen: every outcome not in $A$. | [Maths Note 331](331-empirical-and-theoretical-probability/note.md) |
| Complement rule | $P(A^c) = 1 - P(A)$. | [Maths Note 331](331-empirical-and-theoretical-probability/note.md) |
| Complementary slackness | For each inequality constraint, the multiplier or the constraint value is 0. | [Maths Note 620](620-lagrange-multipliers/note.md) |
| Complete case analysis (CCA) | Dropping every row that has a missing value in any chosen column; also called listwise deletion. | [Note 35](35-complete-case-analysis/note.md) |
| Complete case | A row with a value in every column used. | [Note 35](35-complete-case-analysis/note.md) |
| Complete linkage | Cluster distance = distance of the farthest pair of points. | [Note 131](131-hierarchical-clustering/note.md) |
| Component | One number of a vector, its position along one axis. | [Maths Note 360](360-vectors-and-feature-vectors/note.md) |
| components_ | The eigenvectors of the fitted PCA, one per row. | [Note 49](49-pca-mnist/note.md) |
| Composition | Applying one transformation and then another, seen as one overall transformation. | [Maths Note 510](510-matrix-multiplication-as-composition/note.md) |
| Compound event | An event with two or more outcomes. | [Maths Note 330](330-events-and-types-of-events/note.md) |
| Compression | Storing data in less space. | [Note 11](11-tensors/note.md) |
| Computation graph | A function broken into elementary steps, each a node, with arrows for the flow of values. | [Maths Note 602](602-jacobian-and-matrix-gradients/note.md) |
| Concave function | The negative of a convex function; every chord lies on or below its graph. | [Maths Note 621](621-convex-sets-and-functions/note.md) |
| conda | A package and environment manager for Python and other software. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| conda-forge | A free, community-run conda channel. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| Condition number | $\sigma_1 / \sigma_n$: how much a matrix can magnify errors when we solve with it. | [Maths Note 611](611-computing-the-svd/note.md) |
| Conditional hyperparameter | A hyperparameter that exists only for some values of another, such as `units_3`. | [DL Note 1039](1039-keras-tuner/note.md) |
| Conditional independence | Independence that holds once a third variable (here the class) is known. | [Note 88](88-naive-bayes-maths/note.md) |
| Conditional probability | The probability of an event given that another event has happened: $P(A \mid B)$. | [Note 82](82-conditional-probability/note.md) |
| Condorcet's jury theorem | A majority of independent voters, each right with probability above 0.5, is right more often than any one voter, and more so as voters are added. | [Note 102](102-voting-ensemble/note.md) |
| Confidence interval | An interval built by a method that captures the true parameter in a stated share of repeated samples (e.g. 95%). | [Maths Note 280](280-confidence-intervals-z-procedure/note.md) |
| Confidence level | The share of intervals built by the method that contain the parameter, such as 95%; written $1 - \alpha$. | [Maths Note 280](280-confidence-intervals-z-procedure/note.md) |
| Confounding variable | A hidden factor that drives two variables and makes them correlated. | [Maths Note 231](231-covariance-and-correlation/note.md) |
| Confusion matrix | A table counting predictions for every pair of actual and predicted class. | [Note 76](76-accuracy-confusion-matrix/note.md) |
| Connection object | The open link to a database (`conn`) that queries go through. | [Note 16](16-working-with-json-and-sql/note.md) |
| Connector | A library that lets Python talk to a database. | [Note 16](16-working-with-json-and-sql/note.md) |
| Consistency (of an estimator) | Getting closer to the true parameter value as the amount of data grows. | [Maths Note 631](631-maximum-likelihood-estimation/note.md) |
| Constrained form | Writing regularisation as a hard limit on the size of the coefficients. | [Note 66](66-ridge-key-points/note.md) |
| Constrained optimisation | Maximising or minimising a function while keeping one or more constraints true. | [Note 93](93-svm-maths/note.md) |
| Constraint | A condition the solution must satisfy; in SVM, $y_i (w^T x_i + b) \geq 1$ for every training point. | [Note 93](93-svm-maths/note.md) |
| Constructor (`__init__`) | The method that runs when an object is created and stores its settings. | [Note 130](130-kmeans-from-scratch/note.md) |
| Container | A tag (often a `div`) that holds everything about one item, such as one company. | [Note 18](18-web-scraping/note.md) |
| Context vector | The summary of the input that the decoder works from; one fixed vector in the plain encoder–decoder, a new one per output word with attention. | [DL Note 1067](1067-history-of-llms/note.md) |
| Contextual learning | Studying a maths topic together with the ML algorithm that uses it, instead of the whole subject up front. | [Maths Note 580](580-learning-maths-for-ml/note.md) |
| Contingency table | A table of counts for every pair of categories of two columns; another name for a crosstab. | [Note 21](21-bivariate-multivariate-analysis/note.md) |
| Continuous data | Numerical data that can take any value in a range. | [Maths Note 220](220-what-is-statistics/note.md) |
| Continuous random variable | A random variable that can take any value in a range, such as a CGPA. | [Maths Note 240](240-random-variables-and-distributions/note.md) |
| Continuous uniform distribution $U(a, b)$ | A continuous variable spread evenly between $a$ and $b$, with density $1/(b - a)$. | [Maths Note 261](261-uniform-and-log-normal/note.md) |
| Contour plot | A map of a surface seen from above, with lines joining points of equal height. | [Note 57](57-gradient-descent/note.md) |
| Converge | To settle at a minimum, with steps becoming negligible. | [Note 57](57-gradient-descent/note.md) |
| Convergence (k-means) | The point where the centroids stop moving between rounds, so the algorithm stops. | [Note 128](128-kmeans-intuition/note.md) |
| Convergence speed | How many epochs a method needs to reach a good solution, as opposed to the time per epoch. | [DL Note 1020](1020-gradient-descent-in-neural-networks/note.md) |
| Convergence | The point where the fills hardly change between two iterations. | [Note 40](40-iterative-imputer-mice/note.md) |
| ConvergenceWarning | A warning that the solver stopped at max_iter before reaching the minimum. | [Note 81](81-logistic-hyperparameters/note.md) |
| Conversion rate | The share of people reached who become customers. | [Note 8](08-applications-of-ml/note.md) |
| Convex combination | A weighted sum with non-negative weights that add up to 1. | [Maths Note 640](640-gaussian-mixture-models/note.md) |
| Convex function | A function where a straight line between any two points of its curve never goes below the curve; it has a single minimum. | [Note 57](57-gradient-descent/note.md) |
| Convex optimisation problem | Minimising a convex function subject to convex inequality constraints and affine equality constraints. | [Maths Note 621](621-convex-sets-and-functions/note.md) |
| Convex set | A set that contains the whole segment between any two of its points. | [Maths Note 621](621-convex-sets-and-functions/note.md) |
| Convolutional layer | A layer that slides small filters over an image. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| Convolutional neural network (CNN) | A network with at least one convolutional layer; the standard network for images. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| Coordinate descent | An optimisation method that updates one coefficient at a time; used by scikit-learn's Lasso. | [Note 68](68-lasso-sparsity/note.md) |
| Core point | A point with at least MinPts points within eps. | [Note 132](132-dbscan/note.md) |
| Corrected resampled t-test | A paired t-test for cross-validation scores that allows for the overlap between training sets. | [Maths Note 302](302-two-sample-and-paired-t-tests/note.md) |
| Correlation between base models | How alike two base models' predictions are; the less alike, the more an ensemble cuts variance. | [Note 110](110-bagging-vs-random-forest/note.md) |
| Correlation test | A t-test of $H_0: \rho = 0$, using $t = r\sqrt{n-2}/\sqrt{1-r^2}$ with $n - 2$ degrees of freedom. | [Maths Note 570](570-choosing-a-hypothesis-test/note.md) |
| Correlation | How two columns move together, from -1 to +1. | [Note 19](19-understanding-your-data/note.md) |
| Cosine similarity | The cosine of the angle between two vectors, from -1 to 1. | [Maths Note 362](362-dot-product-and-cosine-similarity/note.md) |
| Cost function | Another name for the loss function, read as a function of the model's parameters. | [Maths Note 590](590-convex-and-non-convex-cost-functions/note.md) |
| Cost-sensitive learning | Changing the learning so that mistakes on some classes cost more. | [Note 133](133-imbalanced-data/note.md) |
| Count plot | A bar chart with one bar per category, as tall as its frequency. | [Note 20](20-univariate-analysis/note.md) |
| Covariance matrix | A square table of all variances (diagonal) and covariances (off-diagonal) of the columns. | [Note 48](48-pca-step-by-step/note.md) |
| Covariance | How two columns move together: positive if they rise together, negative if not. | [Note 48](48-pca-step-by-step/note.md) |
| Covariate shift | A change in the distribution of a model's inputs while the input-output relationship stays the same. | [DL Note 1031](1031-batch-normalization/note.md) |
| Cover | XGBoost's name for the sum of $p(1-p)$ (in regression: the number of rows) in a node. | [Note 125](125-xgboost-classification/note.md) |
| Coverage | The share of intervals from repeated samples that contain the true parameter; equals the confidence level when the assumptions hold. | [Maths Note 281](281-interpreting-confidence-intervals/note.md) |
| Cramér's V | A measure of the link between two categorical columns, from 0 to 1. | [Note 22](22-pandas-profiling/note.md) |
| Credible interval | The Bayesian counterpart of a confidence interval, read as a probability statement about the parameter. | [Maths Note 281](281-interpreting-confidence-intervals/note.md) |
| Credit scoring | Predicting whether a loan applicant will repay. | [Note 8](08-applications-of-ml/note.md) |
| criterion | The DecisionTreeClassifier hyperparameter choosing the impurity measure: "gini" (default), "entropy" or "log_loss". | [Note 97](97-decision-trees-intuition/note.md) |
| Critical value | The z (or t) value that leaves $\alpha/2$ in each tail; 1.96 for 95% on the standard normal curve. | [Maths Note 280](280-confidence-intervals-z-procedure/note.md) |
| Cross entropy | The negative log-likelihood; smaller is better. | [Note 73](73-log-loss/note.md) |
| Cross product (vector product) | A product of two 3D vectors that gives a vector perpendicular to both. | [Maths Note 362](362-dot-product-and-cosine-similarity/note.md) |
| Cross-validated accuracy | Accuracy averaged over several train-test splits of the data, an estimate of performance on new data. | [Note 80](80-polynomial-logistic-regression/note.md) |
| Cross-validation | Testing a model by training and testing it several times on different parts of the training data. | [Note 29](29-pipelines/note.md) |
| Crosstab | A table counting the rows for every pair of categories of two columns. | [Note 21](21-bivariate-multivariate-analysis/note.md) |
| CSV file | A text file holding a table, with commas between values. | [Note 13](13-toy-project/note.md) |
| CUDA | NVIDIA's platform for programming GPUs. | [DL Note 1002](1002-what-is-deep-learning/note.md) |
| Cumulative distribution function (CDF) | The function giving $P(X \le x)$, the probability of a value at most $x$. | [Maths Note 240](240-random-variables-and-distributions/note.md) |
| Cumulative explained variance | The share of the variance kept by the first k components together. | [Note 49](49-pca-mnist/note.md) |
| Cumulative frequency | The running total of the frequencies, up to and including a category. | [Maths Note 223](223-frequency-tables-and-graphs/note.md) |
| Cumulative relative frequency | The running total of the relative frequencies; ends at 1. | [Maths Note 223](223-frequency-tables-and-graphs/note.md) |
| Cumulative sum | The running total of a list of numbers; it turns weights into ranges on the line from 0 to 1. | [Note 116](116-adaboost-step-by-step/note.md) |
| Curse of dimensionality | The problems that appear when data has too many dimensions: lower performance and more computation. | [Note 46](46-curse-of-dimensionality/note.md) |
| Curvature | How fast the slope of a surface changes; given in each direction by the Hessian. | [Maths Note 603](603-hessian-and-multivariate-taylor/note.md) |
| Custom binning | Binning with edges we choose from domain knowledge; also called domain-based binning. | [Note 32](32-binning-binarization/note.md) |
| Custom loss function | A loss written by the user, passed to libraries such as XGBoost with its gradient and Hessian. | [Note 133](133-imbalanced-data/note.md) |
| Customer profile | A summary of what kind of buyer a customer is, built from their purchases. | [Note 8](08-applications-of-ml/note.md) |
| Customer segmentation | Grouping customers by their buying behaviour. | [Note 8](08-applications-of-ml/note.md) |
| Cut-offs | The two percentiles chosen as limits, such as 1 and 99 or 5 and 95. | [Note 44](44-outliers-percentile/note.md) |
| Cutting the dendrogram | Drawing a horizontal line through the dendrogram; the lines it crosses are the clusters. | [Note 131](131-hierarchical-clustering/note.md) |
| Damping | Reducing the size of the oscillations. | [DL Note 1035](1035-nesterov-accelerated-gradient/note.md) |
| Dash | A Python library for building interactive web apps with Plotly charts. | [Note 81](81-logistic-hyperparameters/note.md) |
| Data analysis | Finding patterns and hidden information in data, mainly by plotting graphs. | [Note 1](01-what-is-ml/note.md) |
| Data augmentation | Enlarging a dataset by making changed copies of its examples, such as zoomed or shifted images. | [Maths Note 261](261-uniform-and-log-normal/note.md) |
| Data cleaning | Fixing errors, gaps and inconsistencies in data. | [Note 7](07-challenges-in-ml/note.md) |
| Data engineer | The specialist who collects and organises data from company systems. | [Note 14](14-framing-ml-problem/note.md) |
| Data hungry | Needing a lot of data before results become reliable. | [DL Note 1002](1002-what-is-deep-learning/note.md) |
| Data leakage | Information from the test set leaking into training. | [Note 13](13-toy-project/note.md) |
| Data matrix | The feature vectors of a dataset stacked as rows. | [Maths Note 500](500-linear-transformations-and-matrices/note.md) |
| Data mining | Using ML on data to extract patterns too hidden for graphs. | [Note 1](01-what-is-ml/note.md) |
| Data pipeline | A channel that carries data from one point to another. | [Note 17](17-fetching-data-from-api/note.md) |
| Data preprocessing | Changes made to the data before training, so an algorithm can use it. | [Note 9](09-mldlc/note.md) |
| Data type (dtype) | The kind of values a column holds, such as `int64`, `float64` or `str`. | [Note 19](19-understanding-your-data/note.md) |
| Data warehouse | A separate store of copied company data, safe to analyse without touching the live database. | [Note 9](09-mldlc/note.md) |
| Data | Examples of inputs together with their outputs. | [Note 1](01-what-is-ml/note.md) |
| Database server | A program that holds databases and answers queries, such as MySQL. | [Note 16](16-working-with-json-and-sql/note.md) |
| Database | A program that stores data as tables and answers queries. | [Note 16](16-working-with-json-and-sql/note.md) |
| Datetime | A value pandas understands as a point in time, with date and time parts. | [Note 34](34-date-and-time/note.md) |
| datetime64 | The pandas column type for datetimes; `[us]` means microsecond resolution. | [Note 34](34-date-and-time/note.md) |
| Day of week | The weekday as a number, Monday = 0 to Sunday = 6 (`.dt.dayofweek`). | [Note 34](34-date-and-time/note.md) |
| DBSCAN | Density-based spatial clustering of applications with noise: clusters dense regions and labels lonely points as noise. | [Note 132](132-dbscan/note.md) |
| ddof | NumPy and pandas argument: the number subtracted from $n$ in the variance's denominator. | [Maths Note 222](222-measures-of-dispersion/note.md) |
| De Morgan's law | $(A \cup B)^c = A^c \cap B^c$ and $(A \cap B)^c = A^c \cup B^c$. | [Maths Note 340](340-venn-diagrams-and-contingency-tables/note.md) |
| Dead neuron | A node whose output is 0 for every input; it gets no updates and stays that way. | [DL Note 1028](1028-relu-variants/note.md) |
| Dead zone | The range of S for which the Lasso slope is exactly 0. | [Note 68](68-lasso-sparsity/note.md) |
| Decay factor $\beta$ | How much of the old velocity is kept each step; 0 gives plain gradient descent, usually 0.9. | [DL Note 1034](1034-sgd-with-momentum/note.md) |
| Deciles | The 10th, 20th, ..., 90th percentiles: cuts into 10 groups. | [Maths Note 230](230-percentiles-and-box-plots/note.md) |
| Decision boundary | A line or curve that separates the classes in classification. | [Note 6](06-instance-vs-model-based/note.md) |
| Decision node | A node in the middle of a tree that asks a question and splits again. | [Note 97](97-decision-trees-intuition/note.md) |
| Decision region | The part of the input space in which a model predicts a given class. | [Note 79](79-softmax-regression/note.md) |
| Decision rule (SVM) | Predict +1 if $w \cdot u + b \geq 0$ and −1 otherwise. | [Note 93](93-svm-maths/note.md) |
| Decision stump | A decision tree with maximum depth 1: one split, two regions. | [Note 115](115-adaboost-intuition/note.md) |
| Decision surface | A plot colouring every point of the input space by the class the model would predict there. | [Note 91](91-knn/note.md) |
| Decision tree | A model that predicts by asking a chain of questions about the input columns: nested if-else conditions. | [Note 97](97-decision-trees-intuition/note.md) |
| DecisionTreeRegressor | scikit-learn's regression tree. | [Note 99](99-regression-trees/note.md) |
| Decoder | The part of a seq2seq model that writes the output sequence. | [DL Note 1067](1067-history-of-llms/note.md) |
| Decoding notation | Shrinking a formula's indices to two or three cases and writing every case out by hand. | [Maths Note 580](580-learning-maths-for-ml/note.md) |
| Deep belief network | Hinton's 2006 many-layered network, trained with unsupervised pre-training. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| Deep Learning (DL) | Machine Learning that uses neural networks with many layers; finds features by itself. | [Note 2](02-ai-vs-ml-vs-dl/note.md) |
| Deep network | A neural network with many hidden layers. | [DL Note 1002](1002-what-is-deep-learning/note.md) |
| Deep neural network | A neural network with many hidden layers. | [DL Note 1018](1018-vanishing-exploding-gradients/note.md) |
| Deep reinforcement learning | Reinforcement learning with deep neural networks. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| Default direction | The side of a split that rows with a missing value follow. | [Note 123](123-xgboost-intro/note.md) |
| Define-by-run | Building the search space while the objective function runs, so it can depend on earlier choices. | [Note 134](134-optuna/note.md) |
| Degree | The highest power used in the polynomial. | [Note 61](61-polynomial-regression/note.md) |
| Degrees of freedom | The parameter of the t-distribution; $n - 1$ for a sample of size $n$, the number of deviations free to vary. | [Maths Note 282](282-t-procedure/note.md) |
| Delivery routing | Planning the most efficient route for deliveries. | [Note 8](08-applications-of-ml/note.md) |
| Demand forecasting | Predicting how much of something will be needed, where and when. | [Note 8](08-applications-of-ml/note.md) |
| Dendrites, nucleus, axon | The input branches, the processing centre and the output fibre of a neuron. | [DL Note 1004](1004-perceptron/note.md) |
| Dendrogram | A tree showing which rows (or columns) were joined as similar, and in what order. | [Note 21](21-bivariate-multivariate-analysis/note.md) |
| Dense (fully connected) layer | A layer whose every node receives the output of every node in the layer before. | [DL Note 1011](1011-customer-churn-ann/note.md) |
| Dense region, sparse region | An area with many points close together; an area with few points. | [Note 132](132-dbscan/note.md) |
| Dense representation | A short representation where most values are non-zero. | [DL Note 1057](1057-rnn-sentiment-analysis/note.md) |
| Density estimation | Estimating the PDF of a random variable from observed data. | [Maths Note 243](243-density-estimation-kde/note.md) |
| Density plot | A histogram with a smooth KDE curve on top. | [Note 20](20-univariate-analysis/note.md) |
| Density-based clustering | Clustering that finds dense regions of points separated by sparse regions. | [Note 132](132-dbscan/note.md) |
| Density-connected | Linked by a chain of core points with every step at most eps. | [Note 132](132-dbscan/note.md) |
| Dependent events | Events that are not independent: knowing one changes the probability of the other. | [Note 83](83-independent-events/note.md) |
| Dependent variable | The output column (y). | [Note 13](13-toy-project/note.md) |
| Deploy | Move a model from development to production. | [Note 4](04-batch-learning/note.md) |
| Deployment | Putting a model on a server so users can reach it. | [Note 7](07-challenges-in-ml/note.md) |
| Depth | The number of questions on the longest path from a tree's root to a leaf. | [Note 98](98-decision-tree-hyperparameters/note.md) |
| Derivative | The slope of a function at a point. | [Note 51](51-linear-regression-maths/note.md) |
| Descriptive statistics | Numbers that summarise data, such as count, mean, spread and percentiles. | [Note 19](19-understanding-your-data/note.md) |
| Design matrix ($X$) | The data as a matrix, one row per data point, with a first column of 1s for the intercept. | [Note 54](54-multiple-lr-maths/note.md) |
| Determinant | The factor by which a matrix scales areas (volumes in 3D); 0 when it squishes space into a lower dimension. | [Maths Note 530](530-eigenvectors-and-eigenvalues/note.md) |
| Development environment | Our own machine, where we build and train a model. | [Note 4](04-batch-learning/note.md) |
| Diabetes dataset | scikit-learn's built-in data of 442 patients, 10 standardised inputs, and disease progression one year later. | [Note 55](55-multiple-lr-code/note.md) |
| Diagonal matrix | A matrix with zeros everywhere off the diagonal; it scales each axis by its own factor. | [Maths Note 500](500-linear-transformations-and-matrices/note.md) |
| Diagonalisation | Writing $A = PDP^{-1}$ with $D$ diagonal, using an eigenbasis. | [Maths Note 530](530-eigenvectors-and-eigenvalues/note.md) |
| Dictionary (Python) | A lookup table from keys to values, written `{key: value}`. | [DL Note 1019](1019-mlp-memoization/note.md) |
| Difference quotient | $(f(x + h) - f(x))/h$: the slope of the secant line, the average slope over a step $h$. | [Maths Note 600](600-derivatives-of-one-variable/note.md) |
| Differentiable loss | A loss function whose derivative exists at every point, so it can be minimised with derivatives. | [Note 121](121-gradient-boosting-regression-maths/note.md) |
| Differentiable | Having a derivative at a point (or at every point). | [Maths Note 600](600-derivatives-of-one-variable/note.md) |
| Differential entropy | The entropy of a continuous variable; higher for a more spread-out distribution. | [Note 97](97-decision-trees-intuition/note.md) |
| Differentiation | Finding the slope of a curve at each point; the derivative of the CDF is the PDF. | [Maths Note 242](242-pdf-and-continuous-cdf/note.md) |
| Dimension of a vector | The dimension of the space it lives in: its number of components. | [Maths Note 360](360-vectors-and-feature-vectors/note.md) |
| Dimension | One input column (one feature); a different meaning from the dimensions (axes) of a tensor in Video 11. | [Note 3](03-types-of-ml/note.md) |
| Dimensionality reduction | Reducing the number of input columns while keeping the information. | [Note 3](03-types-of-ml/note.md) |
| Dimensionality | The number of columns (features) in the data. | [Note 27](27-one-hot-encoding/note.md) |
| Directional derivative | The slope of $f$ along a unit vector $\mathbf{u}$: $\nabla f \cdot \mathbf{u}$. | [Maths Note 601](601-partial-derivatives-and-gradients/note.md) |
| Dirty data | Data with errors, gaps, duplicates or inconsistencies. | [Note 9](09-mldlc/note.md) |
| Discrete data | Numerical data that takes only separate values, usually counts. | [Maths Note 220](220-what-is-statistics/note.md) |
| Discrete random variable | A random variable that takes separate values, such as a die's face. | [Maths Note 240](240-random-variables-and-distributions/note.md) |
| Discrete uniform distribution | A discrete distribution in which every possible value is equally likely, such as a fair die. | [Maths Note 241](241-pmf-and-discrete-cdf/note.md) |
| Discretization | Turning a continuous column into a discrete one by cutting its range into intervals. | [Note 32](32-binning-binarization/note.md) |
| Discriminator | The GAN network that judges whether data is real or fake. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| Distance weight (nan-Euclidean) | All columns divided by the columns present in both rows; makes up for the skipped columns. | [Note 39](39-knn-imputer/note.md) |
| Distance weighting | Each neighbour counts in proportion to 1 / its distance, so nearer rows count more. | [Note 39](39-knn-imputer/note.md) |
| Distance | A number measuring how far apart two points are; small distance = similar. | [Note 6](06-instance-vs-model-based/note.md) |
| distance_threshold | Height at which `AgglomerativeClustering` stops merging, instead of a fixed number of clusters. | [Note 131](131-hierarchical-clustering/note.md) |
| Distributed computing | Sharing one job between several machines (nodes), coordinated by a master node. | [Note 123](123-xgboost-intro/note.md) |
| Distribution | How a column's values spread over their range. | [Note 20](20-univariate-analysis/note.md) |
| Distributive law | $a \cdot (b + c) = a \cdot b + a \cdot c$. | [Maths Note 362](362-dot-product-and-cosine-similarity/note.md) |
| Diverge | To move further away with each step, the loss growing instead of shrinking. | [Note 57](57-gradient-descent/note.md) |
| Divergence | Updates that overshoot more and more, so the parameter and the loss run away. | [DL Note 1017](1017-backpropagation-why/note.md) |
| Divisive clustering | Top-down hierarchical clustering: start with one cluster and split repeatedly. | [Note 131](131-hierarchical-clustering/note.md) |
| Domain knowledge | Knowledge of the field the data comes from. | [Note 23](23-what-is-feature-engineering/note.md) |
| Domain | The set of allowed inputs of a function. | [Maths Note 600](600-derivatives-of-one-variable/note.md) |
| Donor | A row that has a value in the column being filled, so it can be a neighbour. | [Note 39](39-knn-imputer/note.md) |
| Dot product | Multiply matching components of two vectors and add; $u^{\mathsf T}x$. | [Note 48](48-pca-step-by-step/note.md) |
| dropna | The pandas method that drops rows (or columns) with missing values. | [Note 35](35-complete-case-analysis/note.md) |
| Dropout rate ($p$) | The probability that each node of a layer is switched off in a training step. | [DL Note 1024](1024-dropout/note.md) |
| Dropout | Switching off a random set of input and hidden nodes at every training step, to reduce overfitting. | [DL Note 1024](1024-dropout/note.md) |
| dtreeviz | A Python library that draws decision trees with the training data shown at every node. | [Note 100](100-dtreeviz/note.md) |
| dtype | The data type of a column, such as `int64`, `float64` or `str`. | [Note 15](15-working-with-csv/note.md) |
| Dual problem | Maximise the dual function $D(\boldsymbol{\lambda}) = \min_{\mathbf{x}} \mathcal{L}$ over multipliers $\boldsymbol{\lambda} \ge 0$. | [Maths Note 620](620-lagrange-multipliers/note.md) |
| Dual vector | The vector whose dot product computes a given linear transformation to numbers. | [Maths Note 520](520-dot-product-and-duality/note.md) |
| Duality | The correspondence between vectors and linear transformations to numbers: each is a dot product with exactly one vector. | [Maths Note 520](520-dot-product-and-duality/note.md) |
| Dummy copy $W^{(t)}$ | A copy of a shared weight used only at time step $t$; the gradient of the shared weight is the sum over the copies. | [DL Note 1059](1059-backpropagation-through-time/note.md) |
| Dummy variable trap | The multicollinearity caused by keeping all $n$ dummy columns, which always add up to 1. | [Note 27](27-one-hot-encoding/note.md) |
| Dummy variable | One of the 0/1 columns created by one-hot encoding. | [Note 27](27-one-hot-encoding/note.md) |
| Duplicate row | A row identical to another row in every column. | [Note 19](19-understanding-your-data/note.md) |
| Durbin-Watson statistic | A number from 0 to 4 measuring autocorrelation of residuals; about 2 means none. | [Note 56](56-linear-regression-assumptions/note.md) |
| Dying ReLU problem | ReLU nodes ending up with a negative weighted sum for every input, so they output 0 and stop learning. | [DL Note 1028](1028-relu-variants/note.md) |
| Dying ReLU | A ReLU node whose input stays negative, so its slope and updates stay 0. | [DL Note 1018](1018-vanishing-exploding-gradients/note.md) |
| Dynamic programming | Solving a problem by reusing the stored solutions of its overlapping sub-problems. | [DL Note 1019](1019-mlp-memoization/note.md) |
| Dynamic search space | A search space in which some hyperparameters exist only for some values of another, such as the algorithm. | [Note 134](134-optuna/note.md) |
| E-step | Compute the responsibilities (posterior probabilities of the latent labels) from the current parameters. | [Maths Note 641](641-expectation-maximization/note.md) |
| Eager learning | Another name for model-based learning: all the work done up front. | [Note 6](06-instance-vs-model-based/note.md) |
| Early stopping | Stopping training when the score on held-out data is best, before full convergence; this keeps coefficients small, so it also acts as regularisation. | [Note 58](58-batch-gradient-descent/note.md) |
| Eckart–Young theorem | The truncated SVD is the closest rank-$k$ matrix to $A$; its spectral error is $\sigma_{k+1}$. | [Maths Note 612](612-low-rank-approximation/note.md) |
| Economy rate | A bowler's runs conceded per over. | [Note 45](45-feature-construction-splitting/note.md) |
| Edge TPU | A small Google chip for running networks on drones, watches and glasses. | [DL Note 1002](1002-what-is-deep-learning/note.md) |
| Effective learning rate | The learning rate a parameter actually gets after AdaGrad's division: $\eta/(\sqrt{v_t}+\epsilon)$. | [DL Note 1036](1036-adagrad/note.md) |
| Eigen-decomposition | Finding all the eigenvalues and eigenvectors of a matrix. | [Note 48](48-pca-step-by-step/note.md) |
| Eigenbasis | A basis made of eigenvectors of a matrix. | [Maths Note 530](530-eigenvectors-and-eigenvalues/note.md) |
| Eigenvalue | The factor by which a matrix stretches its eigenvector. | [Note 48](48-pca-step-by-step/note.md) |
| Eigenvector | A vector that a matrix only stretches or shrinks, without turning it. | [Note 48](48-pca-step-by-step/note.md) |
| Elastic Net regression | Linear regression with both the L1 and the L2 penalty. | [Note 69](69-elastic-net/note.md) |
| Elastic Net | Linear regression with a mix of the L1 and L2 penalties. | [Note 63](63-ridge-regression-intuition/note.md) |
| ElasticNetCV | scikit-learn's Elastic Net that picks alpha and l1_ratio by cross-validation. | [Note 69](69-elastic-net/note.md) |
| Elbow curve | A plot of WCSS against the number of clusters k. | [Note 128](128-kmeans-intuition/note.md) |
| Elbow method | Choosing k at the point where the elbow curve bends from steep to flat. | [Note 128](128-kmeans-intuition/note.md) |
| Elbow point | The k after which adding clusters barely lowers WCSS. | [Note 128](128-kmeans-intuition/note.md) |
| Elongated bowl | A loss surface stretched in one direction, with long elliptical contours. | [DL Note 1036](1036-adagrad/note.md) |
| ELU | Exponential linear unit: $z$ for $z \ge 0$, $\alpha(e^{z} - 1)$ for $z < 0$. | [DL Note 1028](1028-relu-variants/note.md) |
| EM algorithm (expectation maximization) | An iterative method for maximum likelihood with latent variables: alternate an E-step and an M-step. | [Maths Note 641](641-expectation-maximization/note.md) |
| Embedding | A learned vector representing a user, item or word, compared with others by dot products. | [Maths Note 520](520-dot-product-and-duality/note.md) |
| Empirical (experimental) probability | The share of trials in which an event happened. | [Maths Note 331](331-empirical-and-theoretical-probability/note.md) |
| Empirical CDF (ECDF) | The share of a sample's values at or below $x$; a step-function estimate of the CDF. | [Maths Note 253](253-pdf-and-cdf-in-practice/note.md) |
| encode | The `KBinsDiscretizer` parameter choosing ordinal (bin numbers) or one-hot output. | [Note 32](32-binning-binarization/note.md) |
| Encoder | The part of a seq2seq model that reads the input sequence and summarises it. | [DL Note 1067](1067-history-of-llms/note.md) |
| Encoding | Two senses: the rulebook that maps text characters to stored bytes (Video 15); or turning categories into numbers (categorical encoding, Video 26). | [Note 15](15-working-with-csv/note.md) |
| End of distribution imputation | Filling every gap with a value at the edge of the distribution: $\mu \pm 3\sigma$ or $Q_3 + 1.5\,\text{IQR}$. | [Note 36](36-imputing-numerical-data/note.md) |
| End-to-end product | A complete product, from raw data to software that users use. | [Note 9](09-mldlc/note.md) |
| Endpoint | One address of an API that returns one kind of data. | [Note 17](17-fetching-data-from-api/note.md) |
| Ensemble learning | Combining several models into one stronger model. | [Note 9](09-mldlc/note.md) |
| Entropy | A measure of disorder: $-\sum p_i \log_2 p_i$; 0 when pure, 1 for a 50/50 two-class node. | [Note 97](97-decision-trees-intuition/note.md) |
| Environment file | A file (`environment.yml`) listing an environment's packages and versions. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| Environment variable | A named value stored on the computer, outside the code, read with `os.environ`. | [Note 17](17-fetching-data-from-api/note.md) |
| Environment | The world the agent acts in. | [Note 3](03-types-of-ml/note.md) |
| Epigraph | The region on and above a function's graph; convex exactly when the function is convex. | [Maths Note 621](621-convex-sets-and-functions/note.md) |
| Epoch | One full update of the parameters using the whole training set. | [Note 57](57-gradient-descent/note.md) |
| eps (epsilon) | The radius of the neighbourhood DBSCAN examines around each point. | [Note 132](132-dbscan/note.md) |
| eps-neighbourhood | All points within distance eps of a point. | [Note 132](132-dbscan/note.md) |
| Equal frequency binning | Binning into bins holding the same number of rows, with the quantiles as edges; also called quantile binning. | [Note 32](32-binning-binarization/note.md) |
| Equal variances (homogeneity of variance) | The assumption that two populations have the same variance. | [Maths Note 302](302-two-sample-and-paired-t-tests/note.md) |
| Equal width binning | Binning into bins of the same width, $(\max - \min)/k$; also called uniform binning. | [Note 32](32-binning-binarization/note.md) |
| Equally likely outcomes | Outcomes that all have the same probability, such as the faces of a fair die. | [Maths Note 331](331-empirical-and-theoretical-probability/note.md) |
| Equation of a hyperplane | $w^{\mathsf T}x + w_0 = 0$: one equation for a line, plane or hyperplane in any dimension. | [Maths Note 363](363-equation-of-a-hyperplane/note.md) |
| Equiprobable | Equally likely. | [Maths Note 240](240-random-variables-and-distributions/note.md) |
| Error (residual) | The gap between an actual value and the model's prediction. | [Note 50](50-simple-linear-regression/note.md) |
| Error function (loss function) | A formula for how wrong the model is; here the sum of squared errors. | [Note 51](51-linear-regression-maths/note.md) |
| errors="coerce" | The `pd.to_numeric` option that turns values it cannot convert into NaN instead of stopping. | [Note 33](33-mixed-variables/note.md) |
| Estimated PMF | Each value's share of many repeated trials, used as its probability. | [Maths Note 241](241-pmf-and-discrete-cdf/note.md) |
| estimator | The base model that bagging copies (formerly base_estimator). | [Note 106](106-bagging-classifier/note.md) |
| estimators_features_ | The column numbers each trained base model was given. | [Note 106](106-bagging-classifier/note.md) |
| estimators_samples_ | The row numbers each trained base model was given. | [Note 106](106-bagging-classifier/note.md) |
| Eta ($\eta$) | XGBoost's name for the learning rate; default 0.3. | [Note 124](124-xgboost-regression/note.md) |
| eta0 | The starting learning rate in SGDRegressor. | [Note 59](59-stochastic-gradient-descent/note.md) |
| ETL | Extract, transform, load: copying data from source systems into a warehouse. | [Note 9](09-mldlc/note.md) |
| Euclidean distance | The straight-line distance between two points. | [Note 39](39-knn-imputer/note.md) |
| Euler's number $e$ | A fixed number, about 2.71828, that appears in the Poisson PMF. | [Maths Note 560](560-poisson-distribution/note.md) |
| Event | A set of outcomes, such as "the sum is at most 10". | [Note 82](82-conditional-probability/note.md) |
| Evidence | The overall probability of the observed evidence. | [Note 85](85-bayes-theorem/note.md) |
| Exact greedy algorithm | Finding a split by trying the midpoint between every pair of neighbouring sorted values. | [Note 123](123-xgboost-intro/note.md) |
| Excess kurtosis | Kurtosis minus 3, so a normal distribution scores 0. | [Maths Note 260](260-kurtosis-and-qq-plots/note.md) |
| Exhaustive events | Events that together cover the whole sample space, so at least one always happens. | [Maths Note 330](330-events-and-types-of-events/note.md) |
| Expected complete-data log-likelihood $Q$ | The log-likelihood of observations and labels together, averaged over the labels with the responsibilities. | [Maths Note 641](641-expectation-maximization/note.md) |
| Expected count $E$ | The number of rows a category or cell would hold on average if $H_0$ were true. | [Maths Note 571](571-chi-square-tests/note.md) |
| Expected improvement | How much better than the best score so far a point is expected to be, given the surrogate's mean and uncertainty. | [Note 134](134-optuna/note.md) |
| Expected value $E[X]$ | The probability-weighted average of a random variable's values; its long-run mean; also written $\mu$. | [Maths Note 332](332-expected-value-and-variance/note.md) |
| Expert system | Early AI: a human expert's knowledge written as rules, plus a program that applies them. | [Note 2](02-ai-vs-ml-vs-dl/note.md) |
| Explained variance ratio | One component's share of the total variance: its eigenvalue divided by the sum of all. | [Note 49](49-pca-mnist/note.md) |
| Explained variance | The variance along a principal component; its eigenvalue. | [Note 48](48-pca-step-by-step/note.md) |
| explained_variance_ | The eigenvalues of the fitted PCA, largest first. | [Note 49](49-pca-mnist/note.md) |
| Explicit programming | A human writing out every rule the computer follows. ML avoids it. | [Note 1](01-what-is-ml/note.md) |
| Exploding gradient | Gradients growing huge as they pass back through many layers, making updates erratic. | [DL Note 1018](1018-vanishing-exploding-gradients/note.md) |
| Exploratory data analysis (EDA) | Exploring data with summaries and plots to find patterns. | [Note 13](13-toy-project/note.md) |
| Exponential distribution | A right-skewed continuous distribution of waiting times between random events. | [Maths Note 271](271-sampling-distribution-and-clt/note.md) |
| Exponential time | Work that is multiplied by a constant factor with every step of the input size. | [DL Note 1019](1019-mlp-memoization/note.md) |
| Exponentially weighted moving average (EWMA) | A running average updated as $V_t = \beta V_{t-1} + (1-\beta)\theta_t$, where older values count less and less. | [DL Note 1033](1033-exponentially-weighted-moving-average/note.md) |
| export_graphviz | scikit-learn function that writes a tree as Graphviz DOT text. | [Note 100](100-dtreeviz/note.md) |
| export_text | scikit-learn function that prints a trained tree as indented text. | [Note 110](110-bagging-vs-random-forest/note.md) |
| Extrapolation | Predicting for inputs outside the range of the training data. | [Note 50](50-simple-linear-regression/note.md) |
| F distribution | The distribution of a ratio of two variances; two degrees-of-freedom parameters, right-skewed. | [Maths Note 572](572-one-way-anova/note.md) |
| F statistic | $MSB / MSW$: between-group variance over within-group variance. | [Maths Note 572](572-one-way-anova/note.md) |
| f-string | Text starting with `f` in which `{name}` is replaced by a value. | [Note 17](17-fetching-data-from-api/note.md) |
| F-test | Another test that compares two variances. | [Maths Note 302](302-two-sample-and-paired-t-tests/note.md) |
| F1 score | The harmonic mean of precision and recall. | [Note 77](77-precision-recall-f1/note.md) |
| Facet grid | The same plot repeated side by side, one panel per category of another column. | [Maths Note 223](223-frequency-tables-and-graphs/note.md) |
| Fail to reject $H_0$ | The decision that the evidence against $H_0$ is not strong enough; it does not prove $H_0$. | [Maths Note 290](290-null-and-alternative-hypotheses/note.md) |
| False negative (FN) | Predicted negative, but actually positive; a Type II error. | [Note 76](76-accuracy-confusion-matrix/note.md) |
| False positive (FP) | Predicted positive, but actually negative; a Type I error. | [Note 76](76-accuracy-confusion-matrix/note.md) |
| False positive rate (FPR) | The fraction of real negatives the model wrongly flags. | [Note 78](78-roc-auc/note.md) |
| Family size | `SibSp` + `Parch` + 1: the number of people in a passenger's travelling family. | [Note 45](45-feature-construction-splitting/note.md) |
| Family type | Family size grouped into alone, small family (2 to 4) and large family (5 or more). | [Note 45](45-feature-construction-splitting/note.md) |
| Familywise error rate | The probability of at least one Type I error over several tests: $1 - (1 - \alpha)^m$. | [Maths Note 572](572-one-way-anova/note.md) |
| Famous probability distributions | Common named shapes such as normal, uniform, binomial and Poisson. | [Maths Note 240](240-random-variables-and-distributions/note.md) |
| Fan-in | The number of inputs coming into a node: the size of the previous layer. | [DL Note 1030](1030-xavier-he-initialization/note.md) |
| Fan-out | The number of outputs leaving a node: the size of the next layer. | [DL Note 1030](1030-xavier-he-initialization/note.md) |
| Fat tail (heavy tail) | A tail that falls to zero slowly, so extreme values are relatively common. | [Maths Note 260](260-kurtosis-and-qq-plots/note.md) |
| Favourable outcome | An outcome that belongs to the event we are measuring. | [Maths Note 331](331-empirical-and-theoretical-probability/note.md) |
| Feasible region | The set of points that satisfy every constraint. | [Maths Note 620](620-lagrange-multipliers/note.md) |
| Feature construction | Creating a new column by hand from existing ones, e.g. rooms + washrooms into area. | [Note 23](23-what-is-feature-engineering/note.md) |
| Feature engineering | Choosing, removing and creating features. | [Note 7](07-challenges-in-ml/note.md) |
| Feature extraction | Letting an algorithm such as PCA produce new columns from the existing ones (compare feature construction, where we make them by hand). | [Note 23](23-what-is-feature-engineering/note.md) |
| Feature importance (weights) | Reading the size of a weight as how much its input matters, fair only on scaled inputs. | [DL Note 1004](1004-perceptron/note.md) |
| Feature importance | A column's share of all the impurity reduction in a tree; the shares add up to 1. | [Note 99](99-regression-trees/note.md) |
| Feature map ($\phi$) | The explicit transformation of a point into the higher-dimensional space. | [Note 96](96-kernel-trick-code/note.md) |
| Feature scaling | Putting columns on the same scale, so no column dominates distances. | [Note 6](06-instance-vs-model-based/note.md) |
| Feature selection | Keeping only the useful input columns and dropping the rest. | [Note 23](23-what-is-feature-engineering/note.md) |
| Feature splitting | Breaking a column that holds several facts into one column per fact. | [Note 45](45-feature-construction-splitting/note.md) |
| Feature transformation | Changing a column into a form the model can use better. | [Note 23](23-what-is-feature-engineering/note.md) |
| Feature vector | The vector of input values of one data point. | [Maths Note 360](360-vectors-and-feature-vectors/note.md) |
| Feature | One piece of information about each example that a model uses (e.g. a student's CGPA). | [Note 2](02-ai-vs-ml-vs-dl/note.md) |
| feature_importances_ | The fitted attribute holding the feature importance of every column. | [Note 99](99-regression-trees/note.md) |
| Feed-forward network | A network in which information moves only from the first layer to the last. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| Fence | A limit 1.5 IQR beyond the box; values past it are possible outliers. | [Note 20](20-univariate-analysis/note.md) |
| Fine-tuning | Training a pre-trained model further on a small dataset for a specific task. | [DL Note 1067](1067-history-of-llms/note.md) |
| First moment $m_t$ | The EWMA of the gradient: an estimate of its mean. | [DL Note 1038](1038-adam/note.md) |
| First-order condition | A differentiable function is convex exactly when every tangent plane lies on or below its graph. | [Maths Note 621](621-convex-sets-and-functions/note.md) |
| Fisher's exact test | An exact test for small 2 by 2 tables, used when expected counts fall below 5. | [Maths Note 571](571-chi-square-tests/note.md) |
| fit / transform | Learn the scaler's numbers from the training set / apply them to any data. | [Note 24](24-standardization/note.md) |
| fit_predict | Trains a clustering model and returns the cluster of every row. | [Note 129](129-kmeans-code/note.md) |
| fit_transform | Fit and transform in one call; used on the training set only. | [Note 28](28-column-transformer/note.md) |
| Fitting a distribution | Choosing a family of distributions for data, then choosing its parameters. | [Maths Note 631](631-maximum-likelihood-estimation/note.md) |
| Five-number summary | Minimum, Q1, median, Q3 and maximum. | [Note 20](20-univariate-analysis/note.md) |
| Flatten layer | A layer that reshapes a multi-dimensional input into one dimension; no parameters. | [DL Note 1012](1012-mnist-ann/note.md) |
| Flattening | Reshaping a matrix into one long vector so that derivatives stay matrices. | [Maths Note 602](602-jacobian-and-matrix-gradients/note.md) |
| For loop | Code that repeats once for each item of a collection. | [Note 15](15-working-with-csv/note.md) |
| Forest-level hyperparameters | The settings that shape the forest itself: n_estimators, max_features, bootstrap, max_samples. | [Note 111](111-random-forest-hyperparameters/note.md) |
| Format string | A pattern such as `"%d/%m/%Y"` telling `pd.to_datetime` how dates are written. | [Note 34](34-date-and-time/note.md) |
| Forward propagation | Passing one row of inputs through the network, layer by layer, to get the prediction. | [DL Note 1010](1010-forward-propagation/note.md) |
| Forward selection | Feature selection that starts empty and adds the best column at a time. | [Note 23](23-what-is-feature-engineering/note.md) |
| Four fundamental subspaces | Row space, null space, column space and left null space of a matrix. | [Maths Note 611](611-computing-the-svd/note.md) |
| FPGA | A reprogrammable chip: fast and low-power, but expensive. | [DL Note 1002](1002-what-is-deep-learning/note.md) |
| Frame | One image in a video. | [Note 11](11-tensors/note.md) |
| Framing an ML problem | Turning a business problem into a precise ML task that can be built and measured. | [Note 14](14-framing-ml-problem/note.md) |
| Framing the problem | Deciding the goal, users, cost, team and approach before any work starts. | [Note 9](09-mldlc/note.md) |
| Fraud detection | Spotting dishonest transactions; here the outliers are what we want to find. | [Note 41](41-what-are-outliers/note.md) |
| Frequency distribution table | A table of each value or category with the number of times it occurs. | [Maths Note 223](223-frequency-tables-and-graphs/note.md) |
| Frequency | How many times a value or category occurs. | [Note 20](20-univariate-analysis/note.md) |
| Frobenius norm | The square root of the sum of all squared entries of a matrix, $\sqrt{\sum\sigma_i^2}$. | [Maths Note 612](612-low-rank-approximation/note.md) |
| Full SVD | The SVD with square $U$ and $V$, and $\Sigma$ the same shape as $A$. | [Maths Note 610](610-svd-geometry/note.md) |
| Fully grown tree | A tree split until every leaf is pure; usually overfits. | [Note 98](98-decision-tree-hyperparameters/note.md) |
| func | The `FunctionTransformer` parameter that holds the function to apply. | [Note 30](30-function-transformer/note.md) |
| Function of several variables | $f: \mathbb{R}^n \to \mathbb{R}$: a vector of $n$ numbers in, one number out. | [Maths Note 601](601-partial-derivatives-and-gradients/note.md) |
| Function | A rule that assigns exactly one output to every input, written $f: \mathbb{R} \to \mathbb{R}$, $x \mapsto f(x)$. | [Maths Note 600](600-derivatives-of-one-variable/note.md) |
| Function, lambda | A named reusable piece of code (`def`), and a one-line unnamed one. | [Note 15](15-working-with-csv/note.md) |
| FunctionTransformer | scikit-learn's class that applies any function we give it to the data. | [Note 30](30-function-transformer/note.md) |
| Gain (XGBoost) | Similarity of the two children minus similarity of the parent; the split with the largest gain is chosen. | [Note 124](124-xgboost-regression/note.md) |
| Gamma ($\gamma$, `min_split_loss`) | Minimum gain a split must exceed to be kept; default 0. | [Note 124](124-xgboost-regression/note.md) |
| Gamma distribution | A family of right-skewed continuous distributions with a shape and a scale parameter. | [Maths Note 271](271-sampling-distribution-and-clt/note.md) |
| gamma | How far one point's influence reaches in the RBF kernel; large gamma gives tighter boundaries. | [Note 96](96-kernel-trick-code/note.md) |
| Garbage in, garbage out | Bad input data always gives bad results. | [Note 7](07-challenges-in-ml/note.md) |
| Gaussian distribution | Another name for the normal distribution. | [Maths Note 250](250-normal-distribution/note.md) |
| Gaussian kernel | A kernel shaped like the normal curve; the usual default. | [Maths Note 243](243-density-estimation-kde/note.md) |
| Gaussian mixture model (GMM) | A density built as a weighted sum of $K$ normal densities, $\sum_k \pi_k N(x \mid \mu_k, \sigma_k^2)$. | [Maths Note 640](640-gaussian-mixture-models/note.md) |
| Gaussian Naive Bayes | Naive Bayes that models each numerical input as normally distributed within each class. | [Note 90](90-gaussian-naive-bayes/note.md) |
| Gaussian noise | Noise drawn from $N(0, \sigma^2)$; under MLE it gives the squared-error loss. | [Maths Note 633](633-mle-in-machine-learning/note.md) |
| Gaussian process | A model that predicts a value and its uncertainty at every point; a common surrogate. | [Note 134](134-optuna/note.md) |
| GaussianNB | scikit-learn's Gaussian Naive Bayes. | [Note 90](90-gaussian-naive-bayes/note.md) |
| General addition rule | $P(A \cup B) = P(A) + P(B) - P(A \cap B)$, for any two events. | [Maths Note 331](331-empirical-and-theoretical-probability/note.md) |
| Generalisation | How well a model performs on new data it was not trained on. | [Note 71](71-perceptron-code/note.md) |
| Generative adversarial network (GAN) | A generator and a discriminator competing, so that the generator learns to create realistic new data. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| Generative process | A step-by-step recipe that produces data from a model. | [Maths Note 640](640-gaussian-mixture-models/note.md) |
| Generator | The GAN network that creates new data. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| Geometric mean | The $n$-th root of the product of $n$ values; the average of growth factors. | [Maths Note 221](221-measures-of-central-tendency/note.md) |
| get_dummies | pandas function that one-hot encodes columns; `drop_first=True` keeps $n - 1$. | [Note 27](27-one-hot-encoding/note.md) |
| get_feature_names_out | `OneHotEncoder` method that returns the names of the new columns. | [Note 27](27-one-hot-encoding/note.md) |
| Gini impurity | A measure of impurity: $1 - \sum p_i^2$; 0 when pure, 0.5 for a 50/50 two-class node. | [Note 97](97-decision-trees-intuition/note.md) |
| Global minimum | The lowest point of the whole function. | [Note 57](57-gradient-descent/note.md) |
| Glorot (Xavier) and He initialisation | Ways to choose the spread of random starting weights from the layer sizes. | [DL Note 1018](1018-vanishing-exploding-gradients/note.md) |
| Good fit | Capturing the pattern while ignoring the noise. | [Note 7](07-challenges-in-ml/note.md) |
| Goodness-of-fit test | A chi-square test of whether one categorical column follows claimed proportions; $df = k - 1$. | [Maths Note 571](571-chi-square-tests/note.md) |
| Google Colab | Google's browser-based Jupyter notebooks, saved in Google Drive. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| GPU | A graphics chip that runs deep learning maths much faster than a CPU. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| Gradient $g_i$ | First derivative of row $i$'s loss with respect to the previous prediction. | [Note 126](126-xgboost-maths/note.md) |
| Gradient as a row vector | $\nabla f = [\partial f/\partial x_1, \dots, \partial f/\partial x_n] \in \mathbb{R}^{1 \times n}$, the convention that makes the chain rule a matrix product. | [Maths Note 601](601-partial-derivatives-and-gradients/note.md) |
| Gradient boosting | A boosting algorithm that starts from a simple guess and adds trees one by one, each trained on the mistakes (pseudo-residuals) of the ensemble so far. | [Note 120](120-gradient-boosting-intuition/note.md) |
| Gradient checking | Testing a gradient formula against finite-difference estimates, using the relative error. | [Maths Note 601](601-partial-derivatives-and-gradients/note.md) |
| Gradient clipping | Scaling a gradient down to a maximum size before the update. | [DL Note 1018](1018-vanishing-exploding-gradients/note.md) |
| Gradient descent | Finding the lowest point of a function by repeated small steps downhill. | [Note 57](57-gradient-descent/note.md) |
| Gradient of the loss | The collection of the derivatives of the loss with respect to every weight and bias. | [DL Note 1015](1015-backpropagation-what/note.md) |
| Gradient | The vector of partial derivatives of the loss; it points in the direction of steepest increase. | [Note 57](57-gradient-descent/note.md) |
| Grand mean | The mean of all values from all groups together. | [Maths Note 572](572-one-way-anova/note.md) |
| Grand total | The sum of every cell of a contingency table: the size of the whole sample. | [Maths Note 340](340-venn-diagrams-and-contingency-tables/note.md) |
| Graphviz | The graph-drawing program (`dot`) that lays out tree diagrams for dtreeviz and export_graphviz. | [Note 100](100-dtreeviz/note.md) |
| GRE, TOEFL | Exams taken by students applying to graduate programmes abroad; the first two inputs of the admission data. | [DL Note 1013](1013-graduate-admission-ann/note.md) |
| Greedy search | Taking the best split at each node without looking ahead. | [Note 97](97-decision-trees-intuition/note.md) |
| Grid search | Training a model for every combination of listed settings and keeping the best by cross-validation. | [Note 29](29-pipelines/note.md) |
| Grouping effect | Elastic Net's tendency to give correlated inputs similar coefficients instead of keeping only one. | [Note 69](69-elastic-net/note.md) |
| handle_unknown | `OneHotEncoder` parameter that decides what happens to categories never seen in training. | [Note 27](27-one-hot-encoding/note.md) |
| handle_unknown="ignore" | `OneHotEncoder` setting that outputs all zeros for a category not seen in training. | [Note 29](29-pipelines/note.md) |
| Hard assignment | Giving each observation wholly to one cluster (responsibility 0 or 1). | [Maths Note 641](641-expectation-maximization/note.md) |
| Hard voting | Predicting the label that most base models predict. | [Note 103](103-voting-classifier/note.md) |
| Hard-margin SVM | The SVM that allows no point inside the margin or on the wrong side; it needs perfectly separable data. | [Note 93](93-svm-maths/note.md) |
| Harmonic mean | An average that stays close to the smaller of the values: $2ab/(a + b)$ for two values. | [Note 77](77-precision-recall-f1/note.md) |
| He normal | Starting weights from a normal distribution with standard deviation $\sqrt{2/\text{fan-in}}$; for ReLU. | [DL Note 1030](1030-xavier-he-initialization/note.md) |
| He uniform | Starting weights spread evenly between $\pm\sqrt{6/\text{fan-in}}$; for ReLU. | [DL Note 1030](1030-xavier-he-initialization/note.md) |
| Header | The line of a file that holds the column names. | [Note 15](15-working-with-csv/note.md) |
| Headers | Extra information sent with a request, such as the User-Agent. | [Note 18](18-web-scraping/note.md) |
| Heatmap | A table drawn as coloured cells, darker for larger values. | [Note 21](21-bivariate-multivariate-analysis/note.md) |
| Hessian $h_i$ | Second derivative of row $i$'s loss with respect to the previous prediction. | [Note 126](126-xgboost-maths/note.md) |
| Hessian matrix | The symmetric $n \times n$ matrix of all second partial derivatives of $f: \mathbb{R}^n \to \mathbb{R}$; it measures curvature. | [Maths Note 603](603-hessian-and-multivariate-taylor/note.md) |
| Heteroscedasticity | The spread of the residuals changes with the predicted value, often as a funnel. | [Note 56](56-linear-regression-assumptions/note.md) |
| Hidden layer | Any layer between the input and output layers. | [DL Note 1002](1002-what-is-deep-learning/note.md) |
| Hidden state ($h_t$) | The recurrent layer's output at time step $t$; the network's summary of the inputs so far. | [DL Note 1056](1056-rnn-forward-propagation/note.md) |
| hidden_layer_sizes | MLPClassifier setting: the number of nodes in each hidden layer, e.g. (4, 4). | [DL Note 1009](1009-mlp-intuition/note.md) |
| Hierarchical clustering | Clustering that builds a hierarchy of clusters, from single points up to one cluster. | [Note 131](131-hierarchical-clustering/note.md) |
| High bias, low variance algorithm | An algorithm too simple to fit the training data well but stable across samples, such as linear regression; it underfits. | [Note 105](105-bagging-intuition/note.md) |
| High cardinality | A categorical column with very many different categories. | [Note 22](22-pandas-profiling/note.md) |
| High-dimensional data | Data with a very large number of columns. | [Note 46](46-curse-of-dimensionality/note.md) |
| Hinge loss | $\max(0, 1 - y(w^T x + b))$ per point: the error term of the soft-margin SVM. | [Note 94](94-svm-soft-margin/note.md) |
| Histogram | A bar chart of how many values fall in each equal range (bin) of a numerical column. | [Note 20](20-univariate-analysis/note.md) |
| History object | What `fit` returns: the loss and metrics of every epoch. | [DL Note 1011](1011-customer-churn-ann/note.md) |
| Hold-out set | Rows set aside before training, used only to produce honest predictions or scores. | [Note 127](127-stacking-blending/note.md) |
| Homoscedasticity | The residuals have the same spread for all predicted values. | [Note 56](56-linear-regression-assumptions/note.md) |
| HTML | The language web pages are written in: a tree of nested tags. | [Note 18](18-web-scraping/note.md) |
| Huber loss | Half the squared error for errors up to $\delta$, a straight line beyond; MSE for small errors, MAE for large ones. | [DL Note 1014](1014-dl-loss-functions/note.md) |
| Hue, style, size | Plot settings that show an extra column by colour, marker shape or dot size. | [Note 21](21-bivariate-multivariate-analysis/note.md) |
| Hyper-cuboid | A box in many dimensions: the region a tree's cuts carve out. | [Note 97](97-decision-trees-intuition/note.md) |
| Hyperparameter importance | How much each hyperparameter affected the score in a study; the values add up to 1. | [Note 134](134-optuna/note.md) |
| Hyperparameter tuning | Trying several hyperparameter values and keeping the best. | [Note 29](29-pipelines/note.md) |
| Hyperparameter | A setting of an algorithm chosen before training, such as a tree's `max_depth`. | [Note 29](29-pipelines/note.md) |
| Hyperplane | A flat surface in more than three dimensions; the model for three or more input columns. | [Note 53](53-multiple-linear-regression/note.md) |
| Hypothesis function | A model written as a function $h(x)$ that maps an input to a prediction. | [Note 115](115-adaboost-intuition/note.md) |
| Hypothesis testing | Checking a claim about a population parameter with a sample. | [Maths Note 220](220-what-is-statistics/note.md) |
| Identity initialisation | Starting the recurrent weight matrix as the identity matrix. | [DL Note 1060](1060-problems-with-rnn/note.md) |
| Identity matrix | The matrix that leaves every vector unchanged. | [Note 48](48-pca-step-by-step/note.md) |
| If-else ladder | A long chain of hand-written conditions, one per case. | [Note 1](01-what-is-ml/note.md) |
| Image captioning | Producing a sentence that describes an image. | [DL Note 1058](1058-types-of-rnn/note.md) |
| Image classification | Deciding what a picture contains, e.g. dog or not dog. | [Note 1](01-what-is-ml/note.md) |
| ImageNet | A very large labelled image dataset with a yearly classification competition. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| Imbalanced data | Data in which one class is much rarer than another. | [Note 9](09-mldlc/note.md) |
| imbalanced-learn | A Python library (`imblearn`) of resampling techniques and balanced ensembles, with a `fit_resample` method. | [Note 133](133-imbalanced-data/note.md) |
| IMDB dataset | 50,000 film reviews labelled positive or negative, a standard sentiment-analysis dataset. | [DL Note 1055](1055-why-rnn/note.md) |
| Immediate derivative | The derivative of $h_t$ with respect to a weight with $h_{t-1}$ held fixed: only the weight's direct use at step $t$. | [DL Note 1059](1059-backpropagation-through-time/note.md) |
| Impossible event | The empty event $\varnothing$; probability 0. | [Maths Note 330](330-events-and-types-of-events/note.md) |
| Imputation | Filling in missing values, for example with the mean, median or mode. | [Note 23](23-what-is-feature-engineering/note.md) |
| Inactive constraint | An inequality constraint that holds strictly at the answer; its multiplier is 0. | [Maths Note 620](620-lagrange-multipliers/note.md) |
| include_bias | PolynomialFeatures setting that adds a column of 1s. | [Note 61](61-polynomial-regression/note.md) |
| Increasing function | A function whose output grows whenever its input grows, such as the log; it keeps the position of a maximum. | [Maths Note 631](631-maximum-likelihood-estimation/note.md) |
| Incremental learning | Training on small pieces of data over time (the opposite of batch). | [Note 4](04-batch-learning/note.md) |
| Incremental training | Training in small steps, keeping what was learned before. | [Note 5](05-online-learning/note.md) |
| Independent and identically distributed (i.i.d.) | Values that do not affect each other and all come from the same distribution. | [Maths Note 271](271-sampling-distribution-and-clt/note.md) |
| Independent events | Events where one happening does not change the probability of the other. | [Note 83](83-independent-events/note.md) |
| Independent models | Models whose mistakes are unrelated, so one being wrong says nothing about the others. | [Note 102](102-voting-ensemble/note.md) |
| Independent two-sample t-test | A t-test comparing the means of two separate, non-overlapping groups. | [Maths Note 301](301-one-sample-t-test/note.md) |
| Independent variables | The input columns (X). | [Note 13](13-toy-project/note.md) |
| Index | The row labels of a DataFrame. | [Note 15](15-working-with-csv/note.md) |
| Inertia | A big organisation's resistance to changing direction once it has started. | [Note 14](14-framing-ml-problem/note.md) |
| inertia_ | The WCSS of a fitted `KMeans` model. | [Note 129](129-kmeans-code/note.md) |
| Inference (vs prediction) | Learning how the inputs affect the output, rather than only predicting it; not the deployment sense (running a trained model) nor inferential statistics. | [Note 91](91-knn/note.md) |
| Inference engine | The part of an expert system that applies the rules to answer a question. | [Note 2](02-ai-vs-ml-vs-dl/note.md) |
| Inference | A conclusion about a population drawn from a sample. | [Maths Note 220](220-what-is-statistics/note.md) |
| Inferential statistics | Statistics that draws conclusions about a population from a sample. | [Maths Note 220](220-what-is-statistics/note.md) |
| Inflection point | A point where a curve switches between bending down and bending up; for the normal curve, at $\mu \pm \sigma$. | [Maths Note 250](250-normal-distribution/note.md) |
| Information gain | The drop in entropy from a parent to its weighted children; the tree splits on the highest. | [Note 97](97-decision-trees-intuition/note.md) |
| Initialisation | Choosing the starting values of the weights and biases. | [DL Note 1015](1015-backpropagation-what/note.md) |
| Input / output | The columns we know / the column we want to predict. | [Note 3](03-types-of-ml/note.md) |
| Input layer | The first layer, with one node per input column. | [DL Note 1002](1002-what-is-deep-learning/note.md) |
| Inspect | Browser tool that shows which tag draws each part of a page. | [Note 18](18-web-scraping/note.md) |
| Instance set $I_j$ | The rows that land in leaf $j$. | [Note 126](126-xgboost-maths/note.md) |
| Instance-based learning | Learning by storing the training data and comparing new points with it. | [Note 6](06-instance-vs-model-based/note.md) |
| Integer encoding | Replacing each word by its index in the vocabulary. | [DL Note 1057](1057-rnn-sentiment-analysis/note.md) |
| Integration | Finding the area under a curve by adding up infinitely many thin strips. | [Maths Note 242](242-pdf-and-continuous-cdf/note.md) |
| Interaction term | A product of two inputs, such as $xy$, that lets one input's effect depend on another. | [Note 61](61-polynomial-regression/note.md) |
| Intercept | The line's value when the input is 0; $b$ in $y = mx + b$. | [Note 50](50-simple-linear-regression/note.md) |
| intercept_ | The fitted intercept in scikit-learn. | [Note 50](50-simple-linear-regression/note.md) |
| Internal covariate shift | The change in the distribution of a network's activations caused by its parameters changing during training. | [DL Note 1031](1031-batch-normalization/note.md) |
| Interpolation | Placing a new point on the segment between two existing points. | [Note 133](133-imbalanced-data/note.md) |
| Interpretability | How well people can understand why a model makes its decisions. | [Note 114](114-feature-importance/note.md) |
| Interquartile range (IQR) | Q3 - Q1: the width of the middle half of the data. | [Note 20](20-univariate-analysis/note.md) |
| Intersection (A ∩ B) | The event that both A and B happen. | [Note 82](82-conditional-probability/note.md) |
| Inverse matrix | The matrix that undoes another: their product is the identity matrix. | [Note 54](54-multiple-lr-maths/note.md) |
| Inverted dropout | Dropout that scales the kept outputs up by $1/(1-p)$ during training, so prediction needs no change; what Keras does. | [DL Note 1024](1024-dropout/note.md) |
| IoT sensor | A device that measures something and sends the readings over the internet. | [Note 8](08-applications-of-ml/note.md) |
| IQR method (IQR rule, IQR proximity rule) | Outlier detection that flags values beyond 1.5 IQR outside the box ($Q_1$ to $Q_3$); for skewed columns. | [Note 20](20-univariate-analysis/note.md) |
| Iris dataset | 150 iris flowers of three species, with four measurements each; a classic classification dataset. | [Maths Note 253](253-pdf-and-cdf-in-practice/note.md) |
| isnull | The pandas method that marks each missing cell `True`. | [Note 35](35-complete-case-analysis/note.md) |
| ISO week | The week number of the ISO calendar, from `.dt.isocalendar().week`; week 1 holds the year's first Thursday. | [Note 34](34-date-and-time/note.md) |
| Iteration (MICE) | One pass that re-predicts the gaps of every column once, in order. | [Note 40](40-iterative-imputer-mice/note.md) |
| Iteration 0 | The starting table, with every gap filled by its column mean. | [Note 40](40-iterative-imputer-mice/note.md) |
| Iterative imputer | Multivariate imputation that predicts each column from the others, repeatedly; its algorithm is MICE. | [Note 35](35-complete-case-analysis/note.md) |
| Jacobian determinant | $\det J$: the factor by which a function scales small areas or volumes near a point. | [Maths Note 602](602-jacobian-and-matrix-gradients/note.md) |
| Jacobian | The $m \times n$ matrix of all first partial derivatives, $J_{ij} = \partial f_i/\partial x_j$. | [Maths Note 602](602-jacobian-and-matrix-gradients/note.md) |
| Jensen's inequality (for the log) | The log of a weighted average is at least the weighted average of the logs. | [Maths Note 641](641-expectation-maximization/note.md) |
| Jensen's inequality | For a convex function, the function of a weighted average is at most the weighted average of the function. | [Maths Note 621](621-convex-sets-and-functions/note.md) |
| joblib | A library that saves and loads Python objects like pickle, better suited to large arrays. | [Note 29](29-pipelines/note.md) |
| Joint probability distribution | The joint probabilities of every combination of values of two variables; they sum to 1. | [Maths Note 341](341-joint-marginal-conditional-probability/note.md) |
| Joint probability | The probability that two events happen together, $P(A \cap B)$. | [Note 86](86-bayes-problem/note.md) |
| JSON (JavaScript Object Notation) | A plain-text format for structured data, made of objects and arrays, that almost every language can read; used by APIs. | [Note 9](09-mldlc/note.md) |
| JSON Lines | A JSON file with one object per line, read with `lines=True`. | [Note 16](16-working-with-json-and-sql/note.md) |
| JSON viewer | A tool that lays out JSON text as a tree to show its structure. | [Note 17](17-fetching-data-from-api/note.md) |
| Jupyter | Tool for notebooks that mix code, output and text. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| JupyterLab | The program that runs Jupyter notebooks in a web browser. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| k (n_neighbors) | The number of neighbours that vote; KNN's main hyperparameter. | [Note 91](91-knn/note.md) |
| k | The number of clusters k-means makes; chosen by us. | [Note 128](128-kmeans-intuition/note.md) |
| k-distance plot | Sorted distances from every point to its k-th nearest point, used to choose eps. | [Note 132](132-dbscan/note.md) |
| k-means binning | Binning whose edges lie halfway between the centres of the groups found by k-means. | [Note 32](32-binning-binarization/note.md) |
| k-means | A clustering algorithm that repeatedly assigns points to the nearest centre and moves each centre to the mean of its points. | [Note 32](32-binning-binarization/note.md) |
| k-means++ | The default start of `KMeans`: centroids picked one by one, far-away points more likely. | [Note 129](129-kmeans-code/note.md) |
| K-nearest neighbours (KNN) | Predicting from the answers of the k closest stored points. | [Note 6](06-instance-vs-model-based/note.md) |
| Kaggle | A website for sharing datasets and notebooks and for ML competitions. | [Note 17](17-fetching-data-from-api/note.md) |
| KBinsDiscretizer | scikit-learn's class for equal width, equal frequency and k-means binning. | [Note 32](32-binning-binarization/note.md) |
| Keras Tuner | A Python library (`keras_tuner`) that searches for good hyperparameters of a Keras model. | [DL Note 1039](1039-keras-tuner/note.md) |
| Keras workflow | Build, compile, fit, predict: the four steps of every Keras model. | [DL Note 1011](1011-customer-churn-ann/note.md) |
| Keras | The high-level interface built into TensorFlow for defining and training networks. | [DL Note 1001](1001-dl-scope-and-prerequisites/note.md) |
| Kernel (SVM) | The function that maps the data to the higher-dimensional space (not the Jupyter kernel). | [Note 95](95-kernel-trick-intuition/note.md) |
| Kernel density estimate (KDE) | A smooth curve that estimates a column's PDF from its values, built by adding a kernel centred on every data point; a KDE plot draws it. | [Note 20](20-univariate-analysis/note.md) |
| Kernel function $K(a, b)$ | A function that returns $\phi(a) \cdot \phi(b)$ directly from the original points. | [Note 96](96-kernel-trick-code/note.md) |
| Kernel transformation | Applying a kernel to the data. | [Note 95](95-kernel-trick-intuition/note.md) |
| Kernel trick | Making non-linear data separable by mapping it to a higher dimension, without building the new columns. | [Note 95](95-kernel-trick-intuition/note.md) |
| Kernel | The running Python process behind a notebook. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| KKT conditions | Stationarity, primal feasibility, dual feasibility and complementary slackness: the checks for a constrained minimum. | [Maths Note 620](620-lagrange-multipliers/note.md) |
| KL divergence, focal loss, triplet loss | Losses for autoencoders, object detection and embeddings, taught with those networks. | [DL Note 1014](1014-dl-loss-functions/note.md) |
| KMeans | scikit-learn's k-means class, in `sklearn.cluster`. | [Note 129](129-kmeans-code/note.md) |
| KNeighborsClassifier | scikit-learn's KNN classifier; `n_neighbors=5` by default. | [Note 91](91-knn/note.md) |
| KNN imputer | Multivariate imputation from the most similar rows (`KNNImputer`). | [Note 35](35-complete-case-analysis/note.md) |
| Knowledge base | The collection of rules inside an expert system. | [Note 2](02-ai-vs-ml-vs-dl/note.md) |
| Kruskal-Wallis test | A rank-based alternative to one-way ANOVA that does not assume normality. | [Maths Note 572](572-one-way-anova/note.md) |
| Kurtosis risk | In finance, the risk of extreme gains or losses from fat-tailed returns. | [Maths Note 260](260-kurtosis-and-qq-plots/note.md) |
| Kurtosis | How heavy the tails of a distribution are compared with a normal curve; the fourth moment. | [Maths Note 260](260-kurtosis-and-qq-plots/note.md) |
| L-BFGS | Limited-memory BFGS: keeps only the last few step and gradient-change pairs; scikit-learn's default logistic regression solver. | [Maths Note 603](603-hessian-and-multivariate-taylor/note.md) |
| L1 loss | Another name for the mean absolute error used as a training loss. | [DL Note 1014](1014-dl-loss-functions/note.md) |
| L1 norm | The sum of the absolute values of the components. | [Maths Note 361](361-magnitude-distance-and-scalar-operations/note.md) |
| L1 regularisation | Another name for the absolute-value penalty used by Lasso. | [Note 67](67-lasso-regression/note.md) |
| l1_ratio | The share of the total penalty given to the L1 (Lasso) part. | [Note 69](69-elastic-net/note.md) |
| L2 norm | The usual magnitude: square root of the sum of squared components. | [Maths Note 361](361-magnitude-distance-and-scalar-operations/note.md) |
| L2 regularisation | Another name for the squared-coefficient penalty used by Ridge. | [Note 63](63-ridge-regression-intuition/note.md) |
| Label encoding | Replacing the classes of the target by 0, 1, 2, ...; for the output column only. | [Note 26](26-ordinal-label-encoding/note.md) |
| Label | The true class of an example, here the digit an image shows. | [DL Note 1012](1012-mnist-ann/note.md) |
| LabelEncoder | scikit-learn's class for label encoding the target. | [Note 26](26-ordinal-label-encoding/note.md) |
| Labelled data | Data that includes the output column. | [Note 3](03-types-of-ml/note.md) |
| labels_ | The cluster number of every training row, after fitting. | [Note 129](129-kmeans-code/note.md) |
| Lagrange multiplier | A number attached to one constraint; at the answer it scales the constraint's gradient to match the objective's, and measures how much the constraint costs. | [Maths Note 620](620-lagrange-multipliers/note.md) |
| Lagrangian | The objective plus each constraint function times its multiplier: $f + \sum_i \lambda_i g_i$. | [Maths Note 620](620-lagrange-multipliers/note.md) |
| Lambda ($\lambda$) | The power used by a power transform, learned separately for each column. | [Note 31](31-power-transformer/note.md) |
| Lambda ($\lambda$, `reg_lambda`) | Regularisation parameter added to the denominators; shrinks scores and outputs; default 1. | [Note 124](124-xgboost-regression/note.md) |
| Lambda | A one-line Python function without a name, such as `lambda x: x**2`. | [Note 30](30-function-transformer/note.md) |
| lambdas_ | The `PowerTransformer` attribute holding the learned $\lambda$ of each column. | [Note 31](31-power-transformer/note.md) |
| Language modelling | Training a model to predict the next word of a text. | [DL Note 1067](1067-history-of-llms/note.md) |
| Laplace approximation | Approximating a distribution near its peak by a normal distribution built from the Hessian. | [Maths Note 603](603-hessian-and-multivariate-taylor/note.md) |
| Laplace distribution | A peaked, heavy-tailed distribution with density $e^{-\lvert x - \mu\rvert/b}/(2b)$. | [Maths Note 633](633-mle-in-machine-learning/note.md) |
| Laplace smoothing | Adding a small count (usually 1) to every count so that no probability is 0. | [Note 89](89-naive-bayes-code/note.md) |
| Large language model (LLM) | A transformer language model with billions of parameters, trained on a vast amount of text. | [DL Note 1067](1067-history-of-llms/note.md) |
| Lasso regression | Linear regression with a penalty on the sum of absolute coefficients (L1). | [Note 63](63-ridge-regression-intuition/note.md) |
| Latency | The delay between a request and its answer; high for KNN on large data. | [Note 91](91-knn/note.md) |
| Latent semantic analysis (LSA) | Describing documents by their top-$k$ singular directions of the document-word matrix, so that texts on one topic align. | [Maths Note 613](613-svd-in-machine-learning/note.md) |
| Latent variable | A variable in a model that is never observed, such as the component that produced a point. | [Maths Note 640](640-gaussian-mixture-models/note.md) |
| Law of large numbers | The more trials, the closer a share of trials gets to the true probability. | [Maths Note 241](241-pmf-and-discrete-cdf/note.md) |
| Law of total probability | $P(B) = \sum_i P(B \mid A_i) P(A_i)$, when the $A_i$ are mutually exclusive and cover every case. | [Note 86](86-bayes-problem/note.md) |
| Layer number | The position of a layer, from 0 for the input layer to the output layer. | [DL Note 1008](1008-mlp-notation/note.md) |
| Layer | One step in a neural network; each layer builds on what the previous one found. | [Note 2](02-ai-vs-ml-vs-dl/note.md) |
| Lazy learning | Another name for instance-based learning: no work until a question arrives. | [Note 6](06-instance-vs-model-based/note.md) |
| lbfgs | The default solver of LogisticRegression; supports L2 or no penalty. | [Note 81](81-logistic-hyperparameters/note.md) |
| LDA | Linear discriminant analysis: a supervised method that finds the directions that best separate the classes. | [Note 49](49-pca-mnist/note.md) |
| Leaf node | A node that is not split; it gives the prediction. | [Note 97](97-decision-trees-intuition/note.md) |
| Leaf value ($\gamma_{jm}$) | The constant a leaf adds to the model, chosen to minimise the loss of the rows in that leaf. | [Note 121](121-gradient-boosting-regression-maths/note.md) |
| Leaf value in log-odds | $\sum r / \sum p(1-p)$ over a leaf's rows: the amount the leaf adds to the log-odds. | [Note 122](122-gradient-boosting-classification/note.md) |
| Leaf weight $w_j$ | The output value of leaf $j$ of a tree. | [Note 126](126-xgboost-maths/note.md) |
| Leaky ReLU | A ReLU variant with a small slope for negative inputs, so nodes do not die. | [DL Note 1018](1018-vanishing-exploding-gradients/note.md) |
| Learning rate ($\eta$) in gradient boosting | The fraction of each tree's output that is added to the model, the same for every tree; typically 0.1. | [Note 120](120-gradient-boosting-intuition/note.md) |
| Learning rate ($\eta$) | How strongly each update changes the model; in gradient descent, the number the slope is multiplied by to get the step size. | [Note 5](05-online-learning/note.md) |
| Learning rate (AdaBoost) | A multiplier on every weak learner's alpha; values below 1 slow learning. | [Note 118](118-adaboost-hyperparameters/note.md) |
| Learning rate scheduler | A rule that changes the learning rate as training goes on. | [DL Note 1021](1021-improving-a-neural-network/note.md) |
| Learning rate warm-up | Starting training with a very small learning rate and raising it over the first epochs. | [DL Note 1021](1021-improving-a-neural-network/note.md) |
| Learning schedule | A rule that changes the learning rate during training, usually shrinking it. | [Note 59](59-stochastic-gradient-descent/note.md) |
| Learning | Finding rules (patterns) from examples. | [Note 2](02-ai-vs-ml-vs-dl/note.md) |
| Learning-rate schedule | A plan, fixed before training, for lowering the learning rate during training. | [DL Note 1032](1032-optimizers-in-deep-learning/note.md) |
| Least-squares loss | $\lVert \mathbf{y} - \Phi\boldsymbol{\theta} \rVert^2$; its gradient is $-2(\mathbf{y} - \Phi\boldsymbol{\theta})^{\mathsf T}\Phi$. | [Maths Note 602](602-jacobian-and-matrix-gradients/note.md) |
| LeCun initialisation | Normal starting weights with standard deviation $\sqrt{1/\text{fan-in}}$; Keras' `lecun_normal`. | [DL Note 1030](1030-xavier-he-initialization/note.md) |
| Left null space | The output directions perpendicular to every column; spanned by the remaining $\mathbf{u}_i$. | [Maths Note 611](611-computing-the-svd/note.md) |
| Left singular vector ($\mathbf{u}_i$) | An output direction of the SVD; a column of $U$. | [Maths Note 610](610-svd-geometry/note.md) |
| Leptokurtic | Excess kurtosis above 0: fatter tails than normal. | [Maths Note 260](260-kurtosis-and-qq-plots/note.md) |
| Levene's test | A hypothesis test with $H_0$: the groups have equal variances. | [Maths Note 302](302-two-sample-and-paired-t-tests/note.md) |
| LiDAR | A sensor that measures distances to nearby objects with laser light. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| LightGBM | Microsoft's gradient boosting library, aimed at speed and low memory use. | [Note 123](123-xgboost-intro/note.md) |
| Likelihood function $L(\theta \mid \text{data})$ | The likelihood as a function of the parameters, with the data held fixed. | [Maths Note 630](630-probability-vs-likelihood/note.md) |
| Likelihood | How probable the observed data is under given parameter values; read as a function of the parameters with the data fixed. | [Maths Note 630](630-probability-vs-likelihood/note.md) |
| Limit | The value an expression approaches as a quantity (such as $h$) gets arbitrarily close to a target (such as 0). | [Maths Note 600](600-derivatives-of-one-variable/note.md) |
| Line plot | A scatter plot with the dots joined in order, used when x is time. | [Note 21](21-bivariate-multivariate-analysis/note.md) |
| Linear activation | $f(z) = z$: the node outputs its weighted sum unchanged; used in the output layer for regression. | [DL Note 1013](1013-graduate-admission-ann/note.md) |
| Linear algebra | The branch of mathematics that studies linear equations, vectors and matrices. | [Maths Note 360](360-vectors-and-feature-vectors/note.md) |
| Linear combination | A sum of scaled vectors, $a_1\mathbf{v}_1 + \dots + a_k\mathbf{v}_k$. | [Maths Note 490](490-linear-combinations-span-and-basis/note.md) |
| Linear interpolation | Placing a percentile between two neighbouring sorted values, in proportion to its position; the pandas default. | [Note 44](44-outliers-percentile/note.md) |
| Linear program | Minimising a linear function subject to linear inequality constraints. | [Maths Note 622](622-linear-and-quadratic-programming/note.md) |
| Linear regression | An algorithm that fits the straight line closest to all the points. | [Note 23](23-what-is-feature-engineering/note.md) |
| Linear relationship | A relationship between two columns that follows a straight line. | [Note 21](21-bivariate-multivariate-analysis/note.md) |
| Linear transformation to the number line | A function from vectors to numbers that keeps evenly spaced dots evenly spaced; its matrix is $1 \times n$. | [Maths Note 520](520-dot-product-and-duality/note.md) |
| Linear transformation | A change of the whole plane by a matrix that keeps grid lines straight and evenly spaced. | [Note 48](48-pca-step-by-step/note.md) |
| Linear variants of ReLU | ReLU variants with a straight line on the negative side: Leaky ReLU and PReLU. | [DL Note 1028](1028-relu-variants/note.md) |
| Linearisation | Replacing a function near a point by its tangent line (its first-order Taylor polynomial). | [Maths Note 600](600-derivatives-of-one-variable/note.md) |
| Linearity of expectation | $E[aX + bY + c] = a\,E[X] + b\,E[Y] + c$, for any random variables. | [Maths Note 332](332-expected-value-and-variance/note.md) |
| Linearly dependent | At least one vector is a linear combination of the others, so it adds nothing to the span. | [Maths Note 490](490-linear-combinations-span-and-basis/note.md) |
| Linearly independent | Every vector adds a new direction to the span. | [Maths Note 490](490-linear-combinations-span-and-basis/note.md) |
| Linearly separable | Data whose classes a straight line, plane or hyperplane can split. | [Note 70](70-perceptron-trick/note.md) |
| Linkage | The rule for the distance between two clusters. | [Note 131](131-hierarchical-clustering/note.md) |
| List of grids | Several parameter grids passed together, so incompatible values never meet. | [Note 112](112-random-forest-tuning/note.md) |
| List, dictionary | Python's ordered collection `[...]`, and its `key: value` pairs `{...}`. | [Note 15](15-working-with-csv/note.md) |
| Load balancing | Spreading requests across servers so all users are served quickly. | [Note 9](09-mldlc/note.md) |
| Local linear map | The linear transformation a smooth function behaves like near a point; its matrix is the Jacobian. | [Maths Note 602](602-jacobian-and-matrix-gradients/note.md) |
| Local maximum | A point higher than everything near it but not the highest overall. | [Maths Note 641](641-expectation-maximization/note.md) |
| Local minimum | A point lower than everything around it, but not the lowest overall. | [Note 57](57-gradient-descent/note.md) |
| Local optimum (k-means) | A clustering where k-means has stopped but a better one exists, caused by a bad start. | [Note 130](130-kmeans-from-scratch/note.md) |
| Log transform | Replacing each value with its logarithm; pulls in a long right tail. | [Note 30](30-function-transformer/note.md) |
| Log-likelihood | The log of the likelihood: the sum of the log probabilities. | [Note 73](73-log-loss/note.md) |
| Log-log plot | A plot of $\ln y$ against $\ln x$, on which a power law is a straight line. | [Maths Note 262](262-pareto-and-power-law/note.md) |
| Log-normal distribution | A right-skewed continuous distribution whose logarithm is normal. | [Maths Note 261](261-uniform-and-log-normal/note.md) |
| Log-odds | The natural log of the odds, $\ln(p/(1-p))$; any number, 0 at a probability of 0.5. | [Note 122](122-gradient-boosting-classification/note.md) |
| log1p | NumPy's $\log(1 + x)$, a log transform that also works when a value is 0. | [Note 30](30-function-transformer/note.md) |
| Logistic function | Another name for the sigmoid function. | [Note 72](72-sigmoid-function/note.md) |
| Logistic regression | A classification algorithm that finds a separating boundary. | [Note 13](13-toy-project/note.md) |
| Long-term dependency problem | A simple RNN's failure to learn long-term dependencies, caused by the vanishing gradient through time. | [DL Note 1060](1060-problems-with-rnn/note.md) |
| Long-term dependency | An output that depends on an input many time steps earlier. | [DL Note 1060](1060-problems-with-rnn/note.md) |
| Look-ahead point | Where the momentum jump alone would take the weights: $w_t - \beta v_{t-1}$. | [DL Note 1035](1035-nesterov-accelerated-gradient/note.md) |
| Lookup table | The stored probabilities that Naive Bayes computes during training. | [Note 89](89-naive-bayes-code/note.md) |
| Loss function (error function) | The error of the model on one training row. | [DL Note 1014](1014-dl-loss-functions/note.md) |
| Loss function | A formula that measures how wrong a model's predictions are. | [Note 73](73-log-loss/note.md) |
| Low bias, high variance algorithm | An algorithm that fits its training data very well but changes a lot with the data, such as a fully grown tree; it overfits. | [Note 105](105-bagging-intuition/note.md) |
| Lower and upper limit | The two ends of a confidence interval. | [Maths Note 280](280-confidence-intervals-z-procedure/note.md) |
| Lower bound $B(\theta; q)$ | A function below the log-likelihood everywhere, equal to it when $q$ are the current responsibilities. | [Maths Note 641](641-expectation-maximization/note.md) |
| LPA | Lakh rupees per annum: a salary in hundreds of thousands of rupees per year. | [Note 50](50-simple-linear-regression/note.md) |
| LSTM (long short-term memory) | An improved RNN that remembers over longer sequences. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| M-step | Re-estimate the parameters as responsibility-weighted averages, with the responsibilities held fixed. | [Maths Note 641](641-expectation-maximization/note.md) |
| Machine Learning (ML) | Using statistics to let a machine find patterns (rules) in data by itself. | [Note 1](01-what-is-ml/note.md) |
| Machine translation | Translating a sentence from one language into another. | [DL Note 1058](1058-types-of-rnn/note.md) |
| Maclaurin series | The Taylor series around $x_0 = 0$. | [Maths Note 600](600-derivatives-of-one-variable/note.md) |
| Macro average | The plain mean of a metric over all classes. | [Note 77](77-precision-recall-f1/note.md) |
| Magnitude | The number part of a quantity, as opposed to its unit. | [Note 25](25-normalization/note.md) |
| Majority class | The class with the most rows in imbalanced data. | [Note 133](133-imbalanced-data/note.md) |
| Majority vote | Predicting the class that most voters choose: the k neighbours in KNN, or the base models of an ensemble. | [Note 91](91-knn/note.md) |
| make_blobs | scikit-learn function that generates points around chosen centres. | [Note 129](129-kmeans-code/note.md) |
| make_circles | A scikit-learn generator of two concentric circles of points, a standard non-linear test dataset. | [Note 96](96-kernel-trick-code/note.md) |
| make_classification | scikit-learn function that creates random classification data. | [Note 71](71-perceptron-code/note.md) |
| make_column_transformer | Function that builds a column transformer from (transformer, columns) pairs, without names. | [Note 29](29-pipelines/note.md) |
| make_moons | scikit-learn function that creates two interlocking half-moon classes. | [Note 80](80-polynomial-logistic-regression/note.md) |
| make_pipeline | Function that builds a pipeline from objects alone, naming each step after its class. | [Note 29](29-pipelines/note.md) |
| make_regression | scikit-learn function that generates data following a linear pattern plus noise. | [Note 53](53-multiple-linear-regression/note.md) |
| Many-to-many RNN | An RNN that takes a sequence and produces a sequence; also called sequence-to-sequence. | [DL Note 1058](1058-types-of-rnn/note.md) |
| Many-to-one RNN | An RNN that reads a sequence and gives one output at the end. | [DL Note 1058](1058-types-of-rnn/note.md) |
| Many-to-one | An RNN task with a sequence as input and a single output. | [DL Note 1059](1059-backpropagation-through-time/note.md) |
| MAP rule | Maximum a posteriori: predict the class with the largest posterior probability. | [Note 88](88-naive-bayes-maths/note.md) |
| MAR | Missing at random: the gaps depend on another, recorded column. | [Note 35](35-complete-case-analysis/note.md) |
| Margin (gap) | The distance from a separating line to the nearest point of a class. | [Note 71](71-perceptron-code/note.md) |
| Margin (SVM) | The full width between $\pi^+$ and $\pi^-$ (later shown to be $2/\lVert w \rVert$): twice the one-sided margin of the perceptron code Note. | [Note 92](92-svm-intuition/note.md) |
| Margin error | The term $\lVert w \rVert$/2 of the SVM loss; small when the margin is wide. | [Note 94](94-svm-soft-margin/note.md) |
| Margin of error | The distance from the point estimate to either end of a confidence interval. | [Maths Note 280](280-confidence-intervals-z-procedure/note.md) |
| Margin-maximising hyperplane | The separating hyperplane with the largest margin: the SVM decision boundary. | [Note 92](92-svm-intuition/note.md) |
| Marginal (simple, unconditional) probability | The probability of one variable's value whatever the other variable does. | [Maths Note 341](341-joint-marginal-conditional-probability/note.md) |
| Marginal probability distribution | All the marginal probabilities of one variable, read from a joint table. | [Maths Note 341](341-joint-marginal-conditional-probability/note.md) |
| Marginalising | Summing a joint distribution over one variable to remove it. | [Maths Note 341](341-joint-marginal-conditional-probability/note.md) |
| Margins | The row and column totals of a contingency table, where marginal probabilities are read. | [Maths Note 341](341-joint-marginal-conditional-probability/note.md) |
| Markdown | A simple way to format text with symbols such as `#` and `**`. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| Masked language model | A pre-training task that hides some words and asks the model to predict them from both sides (BERT). | [DL Note 1067](1067-history-of-llms/note.md) |
| Mathematical problem | A business goal restated as a measurable target, such as a churn rate to reach. | [Note 14](14-framing-ml-problem/note.md) |
| Mathematical transformation | Applying one mathematical formula to every value of a column. | [Note 30](30-function-transformer/note.md) |
| Matrix (of a transformation) | The grid of numbers whose columns are where the basis vectors land. | [Maths Note 500](500-linear-transformations-and-matrices/note.md) |
| Matrix calculus | Rules for differentiating expressions with vectors and matrices. | [Note 54](54-multiple-lr-maths/note.md) |
| Matrix factorisation (decomposition) | Writing a matrix as a product of simpler matrices. | [Maths Note 350](350-linear-algebra-roadmap/note.md) |
| Matrix factorisation (recommenders) | Predicting ratings as a viewer vector times a film vector, fitted on the known ratings only. | [Maths Note 613](613-svd-in-machine-learning/note.md) |
| Matrix product | The matrix $BA$ of the composition "apply $A$, then $B$". | [Maths Note 510](510-matrix-multiplication-as-composition/note.md) |
| Matrix | A table of numbers: a 2D tensor. | [Note 11](11-tensors/note.md) |
| Matrix-vector multiplication | $A\mathbf{x}$: the linear combination of the columns of $A$ with the coordinates of $\mathbf{x}$ as scalars. | [Maths Note 500](500-linear-transformations-and-matrices/note.md) |
| Max-abs scaling | Divide by the largest absolute value in the column, giving values from -1 to 1. | [Note 25](25-normalization/note.md) |
| max_depth | The cap on a tree's depth; None lets it grow until every leaf is pure. | [Note 98](98-decision-tree-hyperparameters/note.md) |
| max_features | The number of randomly chosen columns a tree considers at each split. | [Note 98](98-decision-tree-hyperparameters/note.md) |
| max_leaf_nodes | The cap on the number of leaves; the tree grows best-first until it is reached. | [Note 98](98-decision-tree-hyperparameters/note.md) |
| max_samples | The number or share of rows each base model gets. | [Note 106](106-bagging-classifier/note.md) |
| MaxAbsScaler | scikit-learn's class for max-abs scaling. | [Note 25](25-normalization/note.md) |
| Maximum a posteriori (MAP) estimation | Choosing the parameters with the largest posterior: minimise NLL minus the log prior. | [Maths Note 633](633-mle-in-machine-learning/note.md) |
| Maximum likelihood estimate $\hat\theta_{\text{ML}}$ | The parameter value where the likelihood function is highest. | [Maths Note 631](631-maximum-likelihood-estimation/note.md) |
| Maximum likelihood estimation (MLE) | Fitting parameters by making the likelihood of the observed data as large as possible. | [Maths Note 631](631-maximum-likelihood-estimation/note.md) |
| MCAR | Missing completely at random: the gaps have no relation to any value in the data. | [Note 35](35-complete-case-analysis/note.md) |
| Mean absolute deviation | The average absolute distance of the points from their mean. Sometimes also abbreviated MAD, which clashes with the median absolute deviation. | [Note 47](47-pca-geometric-intuition/note.md) |
| Mean absolute error (MAE) | The average absolute difference between actual and predicted values. | [Note 52](52-regression-metrics/note.md) |
| Mean centring | Subtracting the mean from every value, so the column's mean becomes 0. | [Note 24](24-standardization/note.md) |
| Mean decrease in impurity (MDI) | Impurity-based feature importance: a column's share of the total weighted impurity decrease of its splits, averaged over the trees; also called Gini importance. | [Note 114](114-feature-importance/note.md) |
| Mean imputation | Filling every gap with the mean of the column's known values. | [Note 36](36-imputing-numerical-data/note.md) |
| Mean normalization | Subtract the mean and divide by the range, giving values from -1 to 1 centred on 0. | [Note 25](25-normalization/note.md) |
| Mean of a random variable | Another name for its expected value. | [Maths Note 332](332-expected-value-and-variance/note.md) |
| Mean square (MSB, MSW) | A sum of squares divided by its degrees of freedom: a variance. | [Maths Note 572](572-one-way-anova/note.md) |
| Mean squared error (MSE) | The average squared difference between actual and predicted values. | [Note 52](52-regression-metrics/note.md) |
| Mean squared error loss | The average squared error; its derivatives do not grow with the number of rows. | [Note 58](58-batch-gradient-descent/note.md) |
| Mean | The average of the values; the centre of the data. | [Note 19](19-understanding-your-data/note.md) |
| mean(axis=0) | The mean of each column of an array. | [Note 130](130-kmeans-from-scratch/note.md) |
| Measure of central tendency | A single number for the typical, central value of a column. | [Maths Note 221](221-measures-of-central-tendency/note.md) |
| Measure of dispersion | A number that describes how spread out a column is around its centre. | [Maths Note 222](222-measures-of-dispersion/note.md) |
| Median absolute deviation (MAD) | The median distance of the values from their median. | [Note 22](22-pandas-profiling/note.md) |
| Median imputation | Filling every gap with the median of the column's known values; better for skewed columns. | [Note 36](36-imputing-numerical-data/note.md) |
| Median | The middle value of sorted data; the 50% percentile. | [Note 19](19-understanding-your-data/note.md) |
| Memoization | Storing the result of a function call and returning the stored result when the same input comes again. | [DL Note 1019](1019-mlp-memoization/note.md) |
| meshgrid | NumPy function that builds every combination of x and y values: the grid for a decision surface. | [Note 91](91-knn/note.md) |
| Mesokurtic | Excess kurtosis of 0, like every normal distribution. | [Maths Note 260](260-kurtosis-and-qq-plots/note.md) |
| Meta-model | The model in stacking that is trained on the base models' predictions. | [Note 101](101-ensemble-learning/note.md) |
| method | The `PowerTransformer` parameter that picks `"box-cox"` or `"yeo-johnson"`. | [Note 31](31-power-transformer/note.md) |
| Metric | A number that tells whether the work is moving in the right direction. | [Note 14](14-framing-ml-problem/note.md) |
| MICE | Multivariate Imputation by Chained Equations: the algorithm behind the iterative imputer. | [Note 40](40-iterative-imputer-mice/note.md) |
| Min-max scaling | Subtract the column's minimum and divide by its range, giving values from 0 to 1; the main normalization technique. | [Note 25](25-normalization/note.md) |
| min_frequency | `OneHotEncoder` parameter that merges rare categories into one column. | [Note 27](27-one-hot-encoding/note.md) |
| min_impurity_decrease | The smallest weighted impurity decrease a split must give to be made. | [Note 98](98-decision-tree-hyperparameters/note.md) |
| min_samples_leaf | The smallest number of rows every leaf must keep. | [Note 98](98-decision-tree-hyperparameters/note.md) |
| min_samples_split | The smallest number of rows a node must hold to be split. | [Note 98](98-decision-tree-hyperparameters/note.md) |
| Mini-batch gradient descent | Gradient descent that uses a small random group of rows for every update. | [Note 58](58-batch-gradient-descent/note.md) |
| Mini-batch | A small group of data points used for one training step. | [Note 5](05-online-learning/note.md) |
| Miniforge | A small installer with only conda and Python, using conda-forge. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| Minimax inequality | For any function of two arguments, the max of the min is at most the min of the max. | [Maths Note 620](620-lagrange-multipliers/note.md) |
| Minimum-norm solution | Among all equally good least-squares solutions, the one with the smallest length; what $A^{+}\mathbf{b}$ returns. | [Maths Note 613](613-svd-in-machine-learning/note.md) |
| Minkowski distance | A family of distances: p = 2 is Euclidean, p = 1 is Manhattan. | [Note 91](91-knn/note.md) |
| MinMaxScaler | scikit-learn's class for min-max scaling. | [Note 25](25-normalization/note.md) |
| Minority class | The rare class in imbalanced data, usually the one we need to find. | [Note 133](133-imbalanced-data/note.md) |
| Minorizer / majorizer | A surrogate that lies below (minorizer) or above (majorizer) the objective and touches it at the current point. | [Maths Note 641](641-expectation-maximization/note.md) |
| MinPts (min_samples) | The number of points an eps-neighbourhood needs for the point to be a core point. | [Note 132](132-dbscan/note.md) |
| Missing category imputation | Filling every gap in a categorical column with a new category, "Missing". | [Note 37](37-missing-categorical-data/note.md) |
| Missing indicator | A 0/1 column recording whether a value was missing. | [Note 35](35-complete-case-analysis/note.md) |
| Missing value | An empty entry, shown by pandas as `NaN`. | [Note 15](15-working-with-csv/note.md) |
| Missing values | Empty cells in the data. | [Note 7](07-challenges-in-ml/note.md) |
| Mixed partial derivative | A second partial derivative with respect to two different variables, such as $\partial^2 f/\partial y\,\partial x$. | [Maths Note 603](603-hessian-and-multivariate-taylor/note.md) |
| Mixed variable | A column holding both numerical and categorical data. | [Note 33](33-mixed-variables/note.md) |
| Mixture weight $\pi_k$ | The share of the mixture given to component $k$; weights are non-negative and add up to 1. | [Maths Note 640](640-gaussian-mixture-models/note.md) |
| ML algorithm | A general method that finds the pattern between inputs and outputs in data. | [Note 1](01-what-is-ml/note.md) |
| MLDLC | Machine learning development life cycle: the guidelines for building an ML product from idea to product. | [Note 9](09-mldlc/note.md) |
| MLE of a binomial $p$ | $\hat p = x/n$, the observed share of successes. | [Maths Note 632](632-mle-for-common-distributions/note.md) |
| MLE of a normal distribution | $\hat\mu = \bar{x}$ and $\hat\sigma^2 = \sum(x_i - \bar{x})^2/n$. | [Maths Note 632](632-mle-for-common-distributions/note.md) |
| MLE of an exponential rate | $\hat\lambda = n/\sum x_i = 1/\bar{x}$. | [Maths Note 632](632-mle-for-common-distributions/note.md) |
| MLOps | Running and maintaining ML models in production. | [Note 7](07-challenges-in-ml/note.md) |
| MLPClassifier | scikit-learn's multi-layer perceptron for classification. | [DL Note 1009](1009-mlp-intuition/note.md) |
| MM algorithm | Minorize–maximize (or majorize–minimize): repeatedly optimise a simpler surrogate that bounds the objective and touches it at the current point. | [Maths Note 641](641-expectation-maximization/note.md) |
| MNAR | Missing not at random: the gaps depend on the missing value itself. | [Note 35](35-complete-case-analysis/note.md) |
| MNIST | A dataset of about 70,000 handwritten-digit images of 28 × 28 pixels. | [Note 23](23-what-is-feature-engineering/note.md) |
| Mode | The most common value of a column. | [Note 23](23-what-is-feature-engineering/note.md) |
| Model deployment | Putting a model on a server so users can reach it. | [Note 9](09-mldlc/note.md) |
| Model drift / concept drift | A model's accuracy dropping as the real world changes; sometimes called model rot. | [Note 4](04-batch-learning/note.md) |
| Model selection | Training several algorithms and keeping the best. | [Note 13](13-toy-project/note.md) |
| Model training | Giving data to an algorithm so it learns the pattern. | [Note 9](09-mldlc/note.md) |
| Model | The logic produced by training, used to give outputs for new inputs. | [Note 1](01-what-is-ml/note.md) |
| Model-based learning | Learning a mathematical function from the data and predicting with it. | [Note 6](06-instance-vs-model-based/note.md) |
| Momentum (optimizer) | Gradient descent that moves by a velocity, an exponentially decaying average of past gradients. | [DL Note 1034](1034-sgd-with-momentum/note.md) |
| monotonic_cst | Setting that forces predictions to only rise or only fall as a column grows. | [Note 111](111-random-forest-hyperparameters/note.md) |
| Monotonicity | Whether a column's values only go up, or only go down, from row to row. | [Note 22](22-pandas-profiling/note.md) |
| Moore's law | The number of transistors on a chip doubles about every two years. | [DL Note 1002](1002-what-is-deep-learning/note.md) |
| Moore–Penrose pseudo-inverse ($A^{+}$) | $V\Sigma^{+}U^{\mathsf T}$: the SVD inverted with zero singular values left at zero. | [Maths Note 613](613-svd-in-machine-learning/note.md) |
| More extreme | Having as much or more evidence against $H_0$, in the direction(s) of $H_1$. | [Maths Note 300](300-p-values/note.md) |
| Most frequent value imputation (mode imputation) | Filling every gap in a column with its mode. | [Note 37](37-missing-categorical-data/note.md) |
| Moving mean and moving variance | Running averages of each node's batch mean and variance, kept during training and used for prediction. | [DL Note 1031](1031-batch-normalization/note.md) |
| Multi-class output layer | An output layer with one node per class; the highest output gives the prediction. | [DL Note 1009](1009-mlp-intuition/note.md) |
| Multi-layer perceptron (MLP) | Many perceptrons organised in layers: input, hidden and output. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| Multi-layer stacking | Stacking with more than one layer of base models below the meta-model. | [Note 127](127-stacking-blending/note.md) |
| Multicollinearity | A mathematical relationship between input columns, so that one can be calculated from the others. | [Note 27](27-one-hot-encoding/note.md) |
| Multimodal | Having more than one mode (two modes: bimodal). | [Maths Note 221](221-measures-of-central-tendency/note.md) |
| Multinomial logistic regression | Another name for softmax regression. | [Note 79](79-softmax-regression/note.md) |
| MultinomialNB | Naive Bayes for count data, such as word counts. | [Note 90](90-gaussian-naive-bayes/note.md) |
| Multiple imputation | Making several filled copies of the data to see how unsure the fills are. | [Note 40](40-iterative-imputer-mice/note.md) |
| Multiple linear regression | Linear regression with several input columns. | [Note 50](50-simple-linear-regression/note.md) |
| Multivariate analysis | Studying more than two variables together. | [Note 20](20-univariate-analysis/note.md) |
| Multivariate chain rule | The derivative through intermediate variables: multiply along each path and add the paths; a row gradient times a matrix of inner derivatives. | [Maths Note 601](601-partial-derivatives-and-gradients/note.md) |
| Multivariate imputation | Imputation that also uses the other columns. | [Note 35](35-complete-case-analysis/note.md) |
| Multivariate normal distribution | The normal distribution of a vector, set by a mean vector and a covariance matrix. | [Maths Note 640](640-gaussian-mixture-models/note.md) |
| Multivariate Taylor polynomial | The multivariate Taylor series cut after the $k = n$ term. | [Maths Note 603](603-hessian-and-multivariate-taylor/note.md) |
| Multivariate Taylor series | $\sum_k D^k f(\mathbf{x}_0)\,\boldsymbol{\delta}^k / k!$: approximation of $f$ near $\mathbf{x}_0$ from its derivatives there. | [Maths Note 603](603-hessian-and-multivariate-taylor/note.md) |
| Mutually exclusive events | Events that cannot happen at the same time; their intersection has probability 0. | [Note 84](84-mutually-exclusive-events/note.md) |
| n_bins | The `KBinsDiscretizer` parameter for the number of bins. | [Note 32](32-binning-binarization/note.md) |
| n_components | The number of principal components PCA keeps; a number between 0 and 1 means a share of the variance. | [Note 49](49-pca-mnist/note.md) |
| n_estimators (AdaBoost) | The maximum number of weak learners, one per boosting stage. | [Note 118](118-adaboost-hyperparameters/note.md) |
| n_estimators | The number of base models in an ensemble. | [Note 106](106-bagging-classifier/note.md) |
| n_init | How many times `KMeans` restarts from new centroids; the run with the lowest inertia is kept. | [Note 129](129-kmeans-code/note.md) |
| n_iter | The number of random combinations RandomizedSearchCV tries (default 10). | [Note 99](99-regression-trees/note.md) |
| n_jobs | scikit-learn setting for how many CPU cores to use in parallel; -1 means all. | [Note 104](104-voting-regressor/note.md) |
| Nabla ($\nabla$) | The symbol for the gradient. | [Maths Note 601](601-partial-derivatives-and-gradients/note.md) |
| Naive assumption | The assumption that the inputs are conditionally independent given the class. | [Note 87](87-naive-bayes-intuition/note.md) |
| Naive Bayes classifier | A classifier that applies Bayes' theorem with the assumption that inputs are independent within each class. | [Note 87](87-naive-bayes-intuition/note.md) |
| Naive Bayes | A classification algorithm based on Bayes' theorem (later Notes). | [Note 82](82-conditional-probability/note.md) |
| Named entity recognition (NER) | Marking the words of a sentence that are entities, such as times and places. | [DL Note 1058](1058-types-of-rnn/note.md) |
| named_steps | Dictionary of a pipeline's steps, from each name to its object. | [Note 29](29-pipelines/note.md) |
| nan-Euclidean distance | The Euclidean distance over the columns both rows have, scaled by (all columns / used columns). | [Note 39](39-knn-imputer/note.md) |
| Narrow AI | AI that does one specific task. All AI today is narrow. | [Note 2](02-ai-vs-ml-vs-dl/note.md) |
| NaT | "Not a time": the missing value of a datetime column. | [Note 34](34-date-and-time/note.md) |
| Natural language processing (NLP) | The part of ML that works with human language. | [Note 8](08-applications-of-ml/note.md) |
| Nearest neighbours | The rows at the smallest distance from a given row. | [Note 39](39-knn-imputer/note.md) |
| Negative gradient | Minus the derivative of the loss with respect to the prediction; the direction that lowers the loss fastest. | [Note 121](121-gradient-boosting-regression-maths/note.md) |
| Negative hyperplane ($\pi^-$) | The copy of the separating hyperplane moved out until it touches the first negative point. | [Note 92](92-svm-intuition/note.md) |
| Negative log-likelihood (NLL) | Minus the log-likelihood; minimised instead of maximising the likelihood. | [Maths Note 631](631-maximum-likelihood-estimation/note.md) |
| Negative power | $a^{-n} = 1/a^{n}$. | [Maths Note 560](560-poisson-distribution/note.md) |
| Negative skew (left skew) | A long tail on the left: a few very small values. | [Note 20](20-univariate-analysis/note.md) |
| Neighbours | The k training points closest to the query point. | [Note 91](91-knn/note.md) |
| Nesterov accelerated gradient (NAG) | Momentum that computes the gradient at the look-ahead point instead of the current point. | [DL Note 1035](1035-nesterov-accelerated-gradient/note.md) |
| Neural network | The model DL uses, loosely inspired by neurons in the brain. | [Note 2](02-ai-vs-ml-vs-dl/note.md) |
| Neuron (in a network) | One unit of a neural network; in an ANN, a perceptron. | [DL Note 1002](1002-what-is-deep-learning/note.md) |
| Neuron | A brain cell: dendrites take signals in, the nucleus processes them, the axon sends the result on. | [DL Note 1004](1004-perceptron/note.md) |
| Neuroplasticity | The brain's connections strengthening, weakening, vanishing or forming over time. | [DL Note 1004](1004-perceptron/note.md) |
| Newton step | Minimising a function by fitting a parabola from its first and second derivatives and jumping to the parabola's lowest point. | [Note 122](122-gradient-boosting-classification/note.md) |
| Newton's method | Repeatedly jumping to the minimum of the second-order Taylor polynomial: $\boldsymbol{\delta} = -H^{-1}\nabla f^{\mathsf T}$. | [Maths Note 603](603-hessian-and-multivariate-taylor/note.md) |
| NLP | Natural language processing: ML on text. | [Maths Note 360](360-vectors-and-feature-vectors/note.md) |
| Node number | A node's index in the fitted tree, assigned depth-first starting from 0 at the root. | [Note 100](100-dtreeviz/note.md) |
| Node-level column sampling | Drawing a new random set of columns before every split (random forest). | [Note 110](110-bagging-vs-random-forest/note.md) |
| Noise ($\varepsilon$) | The random part of a target that the model's prediction does not explain. | [Maths Note 633](633-mle-in-machine-learning/note.md) |
| Noise (irreducible error) | Randomness in the data that no model can predict. | [Note 62](62-bias-variance/note.md) |
| Noise floor | The flat run of small singular values that random noise produces. | [Maths Note 612](612-low-rank-approximation/note.md) |
| Noise point | A point that is neither core nor border; DBSCAN labels it -1. | [Note 132](132-dbscan/note.md) |
| Nominal data | Categorical data whose categories have no order, such as states. | [Note 26](26-ordinal-label-encoding/note.md) |
| Non-closed-form solution | An answer reached by improving a guess step by step. | [Note 51](51-linear-regression-maths/note.md) |
| Non-convex function | A function where some chord lies below part of the curve; it can have several local minima. | [Maths Note 590](590-convex-and-non-convex-cost-functions/note.md) |
| Non-Gaussian distribution | Any distribution that is not normal. | [Maths Note 261](261-uniform-and-log-normal/note.md) |
| Non-linear data | Data whose classes no straight line, plane or hyperplane can separate. | [Note 95](95-kernel-trick-intuition/note.md) |
| Non-linear variants of ReLU | ReLU variants with a curve on the negative side: ELU and SELU. | [DL Note 1028](1028-relu-variants/note.md) |
| Non-null | Not missing. | [Note 19](19-understanding-your-data/note.md) |
| Non-parametric density estimation | Estimating a PDF from the data with no assumption about its shape. | [Maths Note 243](243-density-estimation-kde/note.md) |
| Non-saturating function | A function with no upper limit on its output, such as ReLU for positive inputs. | [DL Note 1027](1027-activation-functions/note.md) |
| Non-sequential data | Data whose features can be listed in any order without changing the meaning, such as a table row. | [DL Note 1055](1055-why-rnn/note.md) |
| Non-trainable parameter | A stored number that gradient descent does not update, such as a moving mean. | [DL Note 1031](1031-batch-normalization/note.md) |
| Norm (magnitude, length) of a vector | Its distance from the origin, $\lVert w \rVert = \sqrt{w_1^2 + w_2^2 + \dots}$; strictly the L2 norm. | [Note 93](93-svm-maths/note.md) |
| Normal distribution | A symmetric, bell-shaped distribution. | [Note 20](20-univariate-analysis/note.md) |
| Normal equation | $\beta = (X^{\mathsf T}X)^{-1}X^{\mathsf T}y$: the closed-form solution of linear regression. | [Note 54](54-multiple-lr-maths/note.md) |
| Normal equations | $X^{\mathsf T}X\beta = X^{\mathsf T}y$: the conditions that the best coefficients satisfy. | [Note 54](54-multiple-lr-maths/note.md) |
| Normal vector | A vector perpendicular to a line, plane or hyperplane; for $w^{\mathsf T}x + w_0 = 0$ it is $w$. | [Maths Note 363](363-equation-of-a-hyperplane/note.md) |
| Normalisation (of weights) | Dividing every weight by their sum so they add up to 1. | [Note 116](116-adaboost-step-by-step/note.md) |
| Normalization | The type of feature scaling that squeezes values into a fixed range, such as 0 to 1. | [Note 25](25-normalization/note.md) |
| Normalized importances | Importances divided by their total, so they add up to 1. | [Note 114](114-feature-importance/note.md) |
| Normalizing inputs | Bringing every input column of a network to the same scale before training, by standardization or normalization. | [DL Note 1023](1023-data-scaling-in-ann/note.md) |
| Not commutative | The order of the factors matters: $AB \neq BA$ in general. | [Maths Note 510](510-matrix-multiplication-as-composition/note.md) |
| Notebook | A `.ipynb` file of cells, each with its output underneath. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| np.argmin | NumPy function returning the position of the smallest value. | [Note 130](130-kmeans-from-scratch/note.md) |
| np.concatenate | NumPy function that joins arrays; with `axis=1` it puts them side by side. | [Note 28](28-column-transformer/note.md) |
| np.insert | NumPy function that inserts values into an array at a given position. | [Note 55](55-multiple-lr-code/note.md) |
| np.linalg.inv | NumPy function that computes the inverse of a square matrix. | [Note 55](55-multiple-lr-code/note.md) |
| np.linalg.lstsq | NumPy function that finds the least-squares solution of a linear system. | [Note 55](55-multiple-lr-code/note.md) |
| NPU | A neural processing unit: a chip in phones that speeds up networks. | [DL Note 1002](1002-what-is-deep-learning/note.md) |
| Null hypothesis ($H_0$) | The statement of no effect, no difference or no relationship; assumed true until the data gives strong evidence against it. | [Maths Note 290](290-null-and-alternative-hypotheses/note.md) |
| Null space | All vectors a matrix sends to $\mathbf{0}$; spanned by the $\mathbf{v}_i$ with $\sigma_i = 0$. | [Maths Note 611](611-computing-the-svd/note.md) |
| Nullable integer (Int64) | The pandas integer type that can also hold a missing value, `<NA>`. | [Note 33](33-mixed-variables/note.md) |
| Nullity matrix | A picture of the whole table with missing values drawn as white lines. | [Note 22](22-pandas-profiling/note.md) |
| Number of samples ($k$) | How many samples are drawn; different from the sample size $n$. | [Maths Note 272](272-estimating-a-mean-with-the-clt/note.md) |
| Numerator layout | Writing derivatives with outputs as rows and inputs as columns. | [Maths Note 602](602-jacobian-and-matrix-gradients/note.md) |
| Numerical data | Data made of numbers. | [Note 3](03-types-of-ml/note.md) |
| Numerical derivative | An estimate of a derivative from a difference quotient with a small step $h$. | [Maths Note 600](600-derivatives-of-one-variable/note.md) |
| NumPy | Python's library for arrays and linear algebra. | [Maths Note 350](350-linear-algebra-roadmap/note.md) |
| Objective function (Optuna) | The function a search optimises: it takes a trial's hyperparameter values and returns a score. | [Note 134](134-optuna/note.md) |
| Objective function (XGBoost) | The quantity XGBoost minimises: the loss plus a regularisation term. | [Note 126](126-xgboost-maths/note.md) |
| Objective function | The quantity an algorithm tries to make as large or as small as possible. | [Note 48](48-pca-step-by-step/note.md) |
| Objective | The metric the tuner maximises or minimises, such as `val_accuracy`. | [DL Note 1039](1039-keras-tuner/note.md) |
| Observation | One record of a dataset: one row of the data table. | [Note 22](22-pandas-profiling/note.md) |
| Observed count $O$ | The number of sample rows in a category or table cell. | [Maths Note 571](571-chi-square-tests/note.md) |
| Odds | How often an event happens divided by how often it does not, e.g. 5 placed to 3 not placed is $5/3$. | [Note 122](122-gradient-boosting-classification/note.md) |
| Offline learning | Another name for batch learning. | [Note 4](04-batch-learning/note.md) |
| OLTP | Online transaction processing: the database that records every action as it happens. | [Note 14](14-framing-ml-problem/note.md) |
| One-hot encoding | Replacing a nominal column by one 0/1 column per category, with a single 1 in each row; also used to represent words. | [Note 11](11-tensors/note.md) |
| One-sample proportion test | A z-test of whether the proportion of one category in the population equals a claimed value $\pi_0$. | [Maths Note 570](570-choosing-a-hypothesis-test/note.md) |
| One-sample t-test | Tests whether a population mean equals a claimed value, from one sample, with $\sigma$ unknown: $t = (\bar{x} - \mu_0)/(s/\sqrt{n})$. | [Maths Note 301](301-one-sample-t-test/note.md) |
| One-sided and two-sided critical value | The value leaving the whole $\alpha$ in one tail, or $\alpha/2$ in each of the two tails. | [Maths Note 282](282-t-procedure/note.md) |
| One-tailed p-value | The tail area beyond the test statistic on the side that $H_1$ points to. | [Maths Note 300](300-p-values/note.md) |
| One-tailed test (one-sided test) | A test whose $H_1$ has a direction ($>$ or $<$), with the whole rejection region in one tail. | [Maths Note 292](292-errors-power-and-tails/note.md) |
| One-to-many RNN | An RNN that takes one non-sequential input and produces a sequence. | [DL Note 1058](1058-types-of-rnn/note.md) |
| One-to-one | A network with non-sequential input and output: an ordinary ANN or CNN, not an RNN. | [DL Note 1058](1058-types-of-rnn/note.md) |
| One-vs-rest | Training one binary classifier per class, each separating that class from all others. | [Note 79](79-softmax-regression/note.md) |
| One-way ANOVA | A test of whether three or more group means are equal, with the groups defined by one categorical column. | [Maths Note 572](572-one-way-anova/note.md) |
| OneHotEncoder | scikit-learn's class for one-hot encoding; remembers the categories it learned. | [Note 27](27-one-hot-encoding/note.md) |
| Online learning | Training incrementally on mini-batches while the model is live in production. | [Note 5](05-online-learning/note.md) |
| OOB prediction | A row's prediction from only the trees whose bootstrap sample missed it. | [Note 113](113-oob-score/note.md) |
| oob_decision_function_ | Each training row's class probabilities from its OOB trees. | [Note 113](113-oob-score/note.md) |
| oob_prediction_ | Each training row's OOB prediction, for a regressor. | [Note 113](113-oob-score/note.md) |
| oob_score_ | The accuracy (classifier) or $R^2$ (regressor) of the OOB predictions. | [Note 113](113-oob-score/note.md) |
| OPTICS | Another density-based clustering algorithm. | [Note 132](132-dbscan/note.md) |
| Optimal number of features | The number of columns at which a model performs best. | [Note 46](46-curse-of-dimensionality/note.md) |
| Optimisation algorithm | A method for finding the parameter values that make a function as small (or large) as possible. | [Note 57](57-gradient-descent/note.md) |
| Optimisation problem | Finding the inputs (here the weights and biases) that make a function (here the loss) smallest. | [DL Note 1032](1032-optimizers-in-deep-learning/note.md) |
| Optimisation | Changing a model step by step until its error is as small as possible. | [Maths Note 440](440-role-of-maths-in-ml/note.md) |
| Optimizer | The rule that turns gradients into weight updates, such as plain gradient descent or Adam. | [DL Note 1021](1021-improving-a-neural-network/note.md) |
| Optuna | A Python framework for hyperparameter tuning built around Bayesian optimisation. | [Note 134](134-optuna/note.md) |
| Ordinal data | Categorical data whose categories have a natural order, such as Poor < Average < Good. | [Note 26](26-ordinal-label-encoding/note.md) |
| Ordinal encoding | Replacing ordered categories by 0, 1, 2, ... in their order; for input columns. | [Note 26](26-ordinal-label-encoding/note.md) |
| OrdinalEncoder | scikit-learn's class for ordinal encoding; takes the order through `categories`. | [Note 26](26-ordinal-label-encoding/note.md) |
| Ordinary least squares (OLS) | The closed-form method for linear regression: the line with the smallest sum of squared errors. | [Note 51](51-linear-regression-maths/note.md) |
| Orthogonal matrix | A square matrix with orthonormal columns; it rotates or flips, and its inverse is its transpose. | [Maths Note 610](610-svd-geometry/note.md) |
| Orthogonal | Perpendicular; for non-zero vectors, dot product 0. | [Maths Note 362](362-dot-product-and-cosine-similarity/note.md) |
| Orthonormal | Vectors of length 1 that are all perpendicular to each other. | [Maths Note 610](610-svd-geometry/note.md) |
| Oscillation | Swinging back and forth past the minimum before settling. | [DL Note 1035](1035-nesterov-accelerated-gradient/note.md) |
| Out-of-bag (OOB) evaluation, OOB score | Testing a bagging model by predicting each training row with only the base models that never saw it; the OOB score is the accuracy (or $R^2$) of those predictions. | [Note 113](113-oob-score/note.md) |
| Out-of-bag rows | The rows a base model never saw because its bootstrap sample missed them (about 37%). | [Note 105](105-bagging-intuition/note.md) |
| Out-of-core computing | Training on data bigger than the RAM by loading it chunk by chunk. | [Note 123](123-xgboost-intro/note.md) |
| Out-of-core learning | Training on data too big for memory by feeding it in chunks, offline. | [Note 5](05-online-learning/note.md) |
| Out-of-fold prediction | A prediction for a row made by a model trained on the other folds, never on that row. | [Note 127](127-stacking-blending/note.md) |
| Out-of-vocabulary (OOV) token | A placeholder, `[UNK]`, for words not in the vocabulary. | [DL Note 1057](1057-rnn-sentiment-analysis/note.md) |
| Outcome | The single result of one trial, such as heads or a 3. | [Maths Note 330](330-events-and-types-of-events/note.md) |
| Outer product | $\boldsymbol{\delta}\boldsymbol{\delta}^{\mathsf T}$, the matrix of all products $\delta_i\delta_j$; more copies give tensors. | [Maths Note 603](603-hessian-and-multivariate-taylor/note.md) |
| Outlier detection | Setting a lower and an upper limit; values outside them are outliers. | [Note 41](41-what-are-outliers/note.md) |
| Outlier | A value far from the rest of the data. | [Note 20](20-univariate-analysis/note.md) |
| Outliers | Values far from the rest, often mistakes. | [Note 7](07-challenges-in-ml/note.md) |
| Output layer | The last layer, which gives the prediction. | [DL Note 1002](1002-what-is-deep-learning/note.md) |
| Output value (classification) | sum of residuals / ($\sum p(1-p) + \lambda$), in log-odds. | [Note 125](125-xgboost-classification/note.md) |
| Output value (leaf weight) | A leaf's prediction: sum of residuals / (number of residuals + $\lambda$). | [Note 124](124-xgboost-regression/note.md) |
| Overdispersion | Count data whose variance is clearly larger than its mean, a sign that a Poisson model does not fit. | [Maths Note 560](560-poisson-distribution/note.md) |
| Overfitting | Learning the training data too closely, noise included; fails on new data. | [Note 7](07-challenges-in-ml/note.md) |
| Overshooting | Moving past the minimum because of the built-up velocity, then swinging back. | [DL Note 1034](1034-sgd-with-momentum/note.md) |
| P-value approach | Carrying out a test by computing a p-value, which also measures the strength of the evidence. | [Maths Note 290](290-null-and-alternative-hypotheses/note.md) |
| P-value decision rule | Reject $H_0$ if $p \le \alpha$, otherwise fail to reject it. | [Maths Note 300](300-p-values/note.md) |
| P-value | The probability, assuming $H_0$ is true, of getting a sample as or more extreme than ours. | [Maths Note 300](300-p-values/note.md) |
| Package manager | A program that downloads and installs libraries in versions that fit together. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| Package | A library packed for installation. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| Padding | Adding zeros to sequences so that all have the same length. | [DL Note 1057](1057-rnn-sentiment-analysis/note.md) |
| Pair plot | A grid of scatter plots of every pair of numerical columns, with histograms on the diagonal. | [Note 21](21-bivariate-multivariate-analysis/note.md) |
| Paired observations | Two measurements that belong to the same subject or matched pair. | [Maths Note 302](302-two-sample-and-paired-t-tests/note.md) |
| Paired t-test (dependent t-test) | A t-test comparing two linked measurements of the same subjects, through their differences. | [Maths Note 301](301-one-sample-t-test/note.md) |
| Pandas Profiling | The library that builds a profiling report from a DataFrame, now named `fg-data-profiling`. | [Note 22](22-pandas-profiling/note.md) |
| pandas, DataFrame | Python's main table library, and its name for a table. | [Note 13](13-toy-project/note.md) |
| Parallel learning | Training the base models independently, so they can all be trained at once (bagging). | [Note 119](119-bagging-vs-boosting/note.md) |
| Parallel processing | Splitting one job among several processor cores working at the same time. | [Note 123](123-xgboost-intro/note.md) |
| Parameter grid | A dictionary of hyperparameter names and the values to try for each. | [Note 112](112-random-forest-tuning/note.md) |
| Parameter sharing | Using the same weights at different positions or time steps. | [DL Note 1055](1055-why-rnn/note.md) |
| Parameter | A named setting passed to a function, like `sep=";"`. | [Note 15](15-working-with-csv/note.md) |
| Parameters (of a distribution) | The numbers, such as $\mu$ and $\sigma$, that set a distribution's location, scale and shape. | [Maths Note 240](240-random-variables-and-distributions/note.md) |
| Parameters | The numbers that describe a learned model, e.g. slope and intercept. | [Note 6](06-instance-vs-model-based/note.md) |
| Parametric density estimation | Assuming a named distribution and estimating its parameters from the data. | [Maths Note 243](243-density-estimation-kde/note.md) |
| Parametric ReLU (PReLU) | Leaky ReLU whose negative slope $a$ is learned during training, one per node. | [DL Note 1028](1028-relu-variants/note.md) |
| Pareto distribution | A power-law distribution starting at $x_m$, with PDF $\alpha x_m^{\alpha}/x^{\alpha + 1}$. | [Maths Note 262](262-pareto-and-power-law/note.md) |
| Parse, parser | Read text and build a structure from it; the part that does this. | [Note 18](18-web-scraping/note.md) |
| Parser | The part of a program that reads text and splits it into pieces. | [Note 15](15-working-with-csv/note.md) |
| Part-of-speech tagging | Labelling every word of a sentence with its part of speech. | [DL Note 1058](1058-types-of-rnn/note.md) |
| Partial derivative | The slope of a function of several variables in one variable, holding the others fixed. | [Note 51](51-linear-regression-maths/note.md) |
| partial_fit | A scikit-learn method that continues training from where the model left off. | [Note 5](05-online-learning/note.md) |
| Partition | Events that are mutually exclusive and exhaustive: exactly one of them happens in every trial. | [Maths Note 330](330-events-and-types-of-events/note.md) |
| passthrough (ColumnTransformer) | The `remainder` option that keeps untouched columns unchanged. | [Note 28](28-column-transformer/note.md) |
| Passthrough (stacking) | Giving the meta-model the original input columns as well as the base models' predictions. | [Note 127](127-stacking-blending/note.md) |
| Past defaulters | Past borrowers who did not repay their loan. | [Note 8](08-applications-of-ml/note.md) |
| Pasting | Bagging with rows sampled without replacement. | [Note 105](105-bagging-intuition/note.md) |
| Path (in a network) | A route from a node to the output along connections; a derivative sums its products over all paths. | [DL Note 1019](1019-mlp-memoization/note.md) |
| Path (in the chain rule) | One route through the computation from the loss to a weight; the derivative is the sum over all paths. | [DL Note 1059](1059-backpropagation-through-time/note.md) |
| Patience | The number of epochs without improvement that early stopping waits before stopping. | [DL Note 1022](1022-early-stopping/note.md) |
| Pattern | The relationship between input and output that the algorithm discovers. | [Note 1](01-what-is-ml/note.md) |
| PCA through the SVD | Taking the principal components from $V$ of the centred data, with variances $\sigma_i^2/n$ and scores $U\Sigma$. | [Maths Note 613](613-svd-in-machine-learning/note.md) |
| PCA | Principal component analysis, a dimensionality reduction technique. | [Note 3](03-types-of-ml/note.md) |
| pd.crosstab | pandas function that counts how often each pair of values from two columns occurs. | [Note 89](89-naive-bayes-code/note.md) |
| pd.cut | The pandas function that puts values into intervals we give it. | [Note 32](32-binning-binarization/note.md) |
| pd.to_datetime | The pandas function that converts text to datetime values. | [Note 34](34-date-and-time/note.md) |
| pd.to_numeric | The pandas function that converts values to numbers. | [Note 33](33-mixed-variables/note.md) |
| Pearson correlation coefficient (Pearson's r) | The usual measure of correlation for straight-line relationships between two numerical columns, written $r$; the one `df.corr()` computes. | [Note 19](19-understanding-your-data/note.md) |
| Pearson's skewness coefficient | $3(\bar{x} - \text{median})/s$: a simple measure of skew. | [Maths Note 252](252-skewness/note.md) |
| Penalty term | The extra term added to the cost to discourage large weights. | [DL Note 1026](1026-regularization-in-dl/note.md) |
| penalty | SGDRegressor setting that adds a regularisation penalty, such as "l2" for Ridge. | [Note 65](65-ridge-gradient-descent/note.md) |
| penalty=None | LogisticRegression setting that switches regularisation off. | [Note 75](75-logistic-gradient-descent/note.md) |
| Per-row seed | A seed taken from a row's own values, so the same input always gets the same random fill. | [Note 38](38-missing-indicator-random-sample/note.md) |
| Percentile location | The position $(p/100) \times (n+1)$ of the $p$-th percentile in sorted data. | [Maths Note 230](230-percentiles-and-box-plots/note.md) |
| Percentile method (percentile rule) | Outlier detection that flags values below a low percentile or above a high one (e.g. 1st and 99th); for any column. | [Note 44](44-outliers-percentile/note.md) |
| Percentile rank | The percentile at which a given value falls: $(X + 0.5Y)/n \times 100$. | [Maths Note 230](230-percentiles-and-box-plots/note.md) |
| Percentile | The value below which a given share of the data lies. | [Note 19](19-understanding-your-data/note.md) |
| Perceptron loss | $\max(0, -y f(x))$ per point, with labels $\pm 1$: 0 when correct, $\lvert f(x) \rvert$ when not. | [DL Note 1006](1006-perceptron-loss/note.md) |
| Perceptron trick | Moving a line towards each misclassified point until the classes are separated. | [Note 70](70-perceptron-trick/note.md) |
| Perceptron | The smallest building block of a neural network; one artificial neuron. | [Note 2](02-ai-vs-ml-vs-dl/note.md) |
| Perfect separation | When a line splits the training classes with no mistakes; unregularised weights then grow without limit. | [Note 75](75-logistic-gradient-descent/note.md) |
| Performance metric | A number that measures how well a model works. | [Note 9](09-mldlc/note.md) |
| Permutation importance | The drop in a model's test score when one column's values are shuffled. | [Note 114](114-feature-importance/note.md) |
| permutation_importance | scikit-learn function (in `sklearn.inspection`) that computes permutation importance. | [Note 114](114-feature-importance/note.md) |
| phpMyAdmin | A web page for creating and managing MySQL databases. | [Note 16](16-working-with-json-and-sql/note.md) |
| pickle | A Python module that saves objects to a file and loads them back. | [Note 13](13-toy-project/note.md) |
| Pie chart | A circle split into slices sized by each category's share. | [Note 20](20-univariate-analysis/note.md) |
| pip | Python's own package manager, which installs from PyPI. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| Pipeline (class) | The scikit-learn class (in `sklearn.pipeline`) that builds a pipeline from a list of (name, object) tuples. | [Note 29](29-pipelines/note.md) |
| Pipeline | One object that bundles several processing steps and a model. | [Note 13](13-toy-project/note.md) |
| Pivot table | A grid with one column's values as rows, another's as columns, and a third in the cells. | [Note 21](21-bivariate-multivariate-analysis/note.md) |
| Pixel | One dot of an image, stored as one or more numbers. | [Note 11](11-tensors/note.md) |
| Plane | A flat surface in 3D; the model for two input columns. | [Note 53](53-multiple-linear-regression/note.md) |
| Plateau | A nearly flat region of the loss, where steps become very small. | [Note 57](57-gradient-descent/note.md) |
| Platykurtic | Excess kurtosis below 0: thinner tails than normal. | [Maths Note 260](260-kurtosis-and-qq-plots/note.md) |
| Plausibility | How believable a parameter value is in the light of the data; measured by its likelihood relative to other values. | [Maths Note 630](630-probability-vs-likelihood/note.md) |
| Point estimate | A single number computed from sample data as the best guess for an unknown population parameter. | [Maths Note 272](272-estimating-a-mean-with-the-clt/note.md) |
| Poisson distribution | A discrete distribution of counts of events, with parameter $\lambda$. | [Maths Note 560](560-poisson-distribution/note.md) |
| Poisson regression | A model that predicts the rate $\lambda$ of a count target from the features. | [Maths Note 560](560-poisson-distribution/note.md) |
| Polar coordinates | Describing a point by its distance $r$ from the origin and its angle $\theta$: $(r\cos\theta, r\sin\theta)$. | [Maths Note 602](602-jacobian-and-matrix-gradients/note.md) |
| Policy | The agent's rules for which action to take. | [Note 3](03-types-of-ml/note.md) |
| Polynomial features | New input columns made from powers and products of the original inputs. | [Note 80](80-polynomial-logistic-regression/note.md) |
| Polynomial kernel | A kernel built from powers of the inputs, such as $x^2$. | [Note 95](95-kernel-trick-intuition/note.md) |
| Polynomial regression | Linear regression on powers (and products) of the inputs, to fit curves. | [Note 61](61-polynomial-regression/note.md) |
| PolynomialFeatures | scikit-learn transformer that creates the power and product columns. | [Note 61](61-polynomial-regression/note.md) |
| Polytope | The region where a set of linear inequalities all hold: a polygon in two dimensions. | [Maths Note 622](622-linear-and-quadratic-programming/note.md) |
| Pooled standard deviation | The combined standard deviation of two groups used by Student's two-sample t-test. | [Maths Note 302](302-two-sample-and-paired-t-tests/note.md) |
| Population correlation $\rho$ | The correlation between two columns in the whole population; $r$ estimates it. | [Maths Note 570](570-choosing-a-hypothesis-test/note.md) |
| Population covariance ($\sigma_{xy}$) | Covariance of a whole population, dividing by $N$. | [Maths Note 231](231-covariance-and-correlation/note.md) |
| Population mean ($\mu$) | The mean of every value in the population. | [Maths Note 221](221-measures-of-central-tendency/note.md) |
| Population | The entire group of individuals or objects we want to study. | [Maths Note 220](220-what-is-statistics/note.md) |
| Positive and negative side | The two halves of the plane where Ax + By + C is above or below 0. | [Note 70](70-perceptron-trick/note.md) |
| Positive definite matrix | A symmetric matrix whose eigenvalues are all positive; its quadratic form is a strictly convex bowl. | [Maths Note 622](622-linear-and-quadratic-programming/note.md) |
| Positive hyperplane ($\pi^+$) | The copy of the separating hyperplane moved out until it touches the first positive point. | [Note 92](92-svm-intuition/note.md) |
| Positive semi-definite | A symmetric matrix whose eigenvalues are all 0 or positive. | [Maths Note 610](610-svd-geometry/note.md) |
| Positive skew (right skew) | A long tail on the right: a few very large values. | [Note 20](20-univariate-analysis/note.md) |
| Post-hoc test | A test run after ANOVA rejects, to find which groups differ. | [Maths Note 572](572-one-way-anova/note.md) |
| Posterior $p(\theta \mid \text{data})$ | The distribution over the parameters after seeing the data; proportional to likelihood × prior. | [Maths Note 633](633-mle-in-machine-learning/note.md) |
| Posterior | The probability of an event after the evidence is taken into account. | [Note 85](85-bayes-theorem/note.md) |
| Power iteration | Finding the top eigenvector by multiplying a vector by the matrix again and again. | [Maths Note 530](530-eigenvectors-and-eigenvalues/note.md) |
| Power law | A relationship $y = k\,x^{a}$: one variable proportional to a power of the other. | [Maths Note 262](262-pareto-and-power-law/note.md) |
| Power of a test | $1 - \beta$: the probability of rejecting $H_0$ when it is false. | [Maths Note 292](292-errors-power-and-tails/note.md) |
| Power rule | $(x^n)' = n x^{n-1}$. | [Maths Note 600](600-derivatives-of-one-variable/note.md) |
| Power series | An infinite sum $\sum a_k (x - c)^k$; the Taylor series is a special case. | [Maths Note 600](600-derivatives-of-one-variable/note.md) |
| Power transformer | A transform that raises each column to a learned power $\lambda$ to make it close to normal. | [Note 31](31-power-transformer/note.md) |
| PowerTransformer | scikit-learn's class for the Box-Cox and Yeo-Johnson transforms (next Note). | [Note 30](30-function-transformer/note.md) |
| Pre-training | The first, general training of a model on a large dataset. | [DL Note 1067](1067-history-of-llms/note.md) |
| Precision | Of all items predicted positive, the fraction that really are positive. | [Note 14](14-framing-ml-problem/note.md) |
| Predict | Use a trained model to give an answer for new data it has not seen. | [Note 2](02-ai-vs-ml-vs-dl/note.md) |
| predict_proba | scikit-learn method that returns predicted probabilities instead of classes. | [Note 78](78-roc-auc/note.md) |
| Prediction ($\hat{y}$) | The value the model gives for an input; the hat marks a prediction. | [Note 51](51-linear-regression-maths/note.md) |
| Prediction path | The nodes a row passes through, from the root to the leaf that predicts it. | [Note 100](100-dtreeviz/note.md) |
| Predictive maintenance | Repairing a machine before it breaks, based on predicted faults. | [Note 8](08-applications-of-ml/note.md) |
| Preprocessing | Cleaning and preparing data before training. | [Note 13](13-toy-project/note.md) |
| Primal problem | The original constrained problem, in the variables $\mathbf{x}$. | [Maths Note 620](620-lagrange-multipliers/note.md) |
| Principal component analysis (PCA) | An unsupervised feature extraction technique that builds new columns along the directions of greatest variance. | [Note 47](47-pca-geometric-intuition/note.md) |
| Principal component | A new axis found by PCA; PC1 holds the most variance, PC2 the next most. | [Note 47](47-pca-geometric-intuition/note.md) |
| Prior $p(\theta)$ | A distribution over the parameters expressing what we believe before seeing data. | [Maths Note 633](633-mle-in-machine-learning/note.md) |
| Prior | The probability of an event before any evidence is seen. | [Note 85](85-bayes-theorem/note.md) |
| Probabilistic interpretation | Reading the model's output as the probability of the positive class. | [Note 72](72-sigmoid-function/note.md) |
| Probabilistic model | A model that outputs a distribution $p(y \mid x, \theta)$ over the target rather than a single value. | [Maths Note 633](633-mle-in-machine-learning/note.md) |
| Probability density function (PDF) | A curve showing how likely each value is; areas under it are probabilities. | [Note 20](20-univariate-analysis/note.md) |
| Probability density | The height of a continuous distribution's curve; compares how likely nearby values are. | [Note 20](20-univariate-analysis/note.md) |
| Probability distribution function | A formula $y = f(x)$ giving the probability of each outcome; the umbrella term for PMF and PDF. | [Maths Note 240](240-random-variables-and-distributions/note.md) |
| Probability distribution | A list of every possible outcome of a random variable with its probability. | [Maths Note 240](240-random-variables-and-distributions/note.md) |
| Probability mass function (PMF) | The probability distribution function of a discrete random variable. | [Maths Note 240](240-random-variables-and-distributions/note.md) |
| Probability tree | A diagram in which each path multiplies the probabilities along its branches. | [Note 86](86-bayes-problem/note.md) |
| Probability | A number from 0 to 1 measuring how likely an event is; written $P(A)$. | [Maths Note 331](331-empirical-and-theoretical-probability/note.md) |
| Product rule for independent events | $P(A \cap B) = P(A) \times P(B)$. | [Note 83](83-independent-events/note.md) |
| Product rule | $(fg)' = f'g + fg'$. | [Maths Note 600](600-derivatives-of-one-variable/note.md) |
| Production code | The code that runs the deployed model on a server, for example behind a website. | [Note 29](29-pipelines/note.md) |
| Production environment | The server where a model serves real users. | [Note 4](04-batch-learning/note.md) |
| Profiling report | An automatic EDA report describing every column and pair of columns of a dataset. | [Note 22](22-pandas-profiling/note.md) |
| Program | Logic written by us that turns an input into an output. | [Note 1](01-what-is-ml/note.md) |
| Projection view of the dot product | $\mathbf{v} \cdot \mathbf{w}$ = signed length of the projection of $\mathbf{w}$ onto $\mathbf{v}$, times $\lVert \mathbf{v} \rVert$. | [Maths Note 520](520-dot-product-and-duality/note.md) |
| Projection | Dropping a point or vector straight onto an axis, a line or another vector's direction, like casting a shadow. | [Note 47](47-pca-geometric-intuition/note.md) |
| Proportional to (∝) | Equal up to a constant factor that is the same for every class. | [Note 88](88-naive-bayes-maths/note.md) |
| Proximity matrix | An n × n table of the distances between every pair of points or clusters. | [Note 131](131-hierarchical-clustering/note.md) |
| Pruning (Optuna) | Stopping an unpromising trial early, before its training finishes. | [Note 134](134-optuna/note.md) |
| Pruning | Stopping a tree early or cutting it back so it does not overfit. | [Note 98](98-decision-tree-hyperparameters/note.md) |
| Pseudo-residual | The mistake on one row that the next tree learns; for squared error it is actual minus predicted. | [Note 120](120-gradient-boosting-intuition/note.md) |
| Public dataset | A labelled dataset released for anyone to use. | [DL Note 1002](1002-what-is-deep-learning/note.md) |
| Pure leaf | A leaf whose training rows all belong to one class. | [Note 100](100-dtreeviz/note.md) |
| Push and pull | Moving the line away from a correctly classified point, or towards a misclassified one. | [Note 72](72-sigmoid-function/note.md) |
| PyPI | The Python Package Index, the public store of Python packages. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| Pyramid structure | Hidden layers with fewer neurons in each later layer, such as 64-32-16; an old rule of thumb, not needed. | [DL Note 1021](1021-improving-a-neural-network/note.md) |
| PyTorch | Meta's deep learning library, most used in research. | [DL Note 1001](1001-dl-scope-and-prerequisites/note.md) |
| Q-Q plot | A plot of a column's sorted values against the values a theoretical distribution, often the normal, would have; points on the line mean the data follows it. | [Note 30](30-function-transformer/note.md) |
| Quadratic form | An expression like $x^{\mathsf T}Ax$: a sum of squared and cross terms of a vector's components. | [Maths Note 350](350-linear-algebra-roadmap/note.md) |
| Quadratic program | Minimising a convex quadratic function subject to linear inequality constraints. | [Maths Note 622](622-linear-and-quadratic-programming/note.md) |
| Quantiles | Values that cut sorted data into equal-sized groups. | [Maths Note 230](230-percentiles-and-box-plots/note.md) |
| QuantileTransformer | scikit-learn's third mathematical transformer, not covered in these Notes. | [Note 30](30-function-transformer/note.md) |
| Quarter | One of four three-month parts of a year. | [Note 34](34-date-and-time/note.md) |
| Quartiles | The 25%, 50% and 75% percentiles, which cut the data into four equal groups. | [Note 19](19-understanding-your-data/note.md) |
| Quasi-Newton method | Newton's method with the Hessian replaced by a matrix built from gradient changes. | [Maths Note 603](603-hessian-and-multivariate-taylor/note.md) |
| Query parameters | Settings after the `?` in a URL, joined by `&`, such as `page=1`. | [Note 17](17-fetching-data-from-api/note.md) |
| Query point | The new point whose class we want to predict. | [Note 91](91-knn/note.md) |
| Query | A request for data, written in SQL. | [Note 16](16-working-with-json-and-sql/note.md) |
| Quintiles | The 20th, 40th, 60th and 80th percentiles: cuts into 5 groups. | [Maths Note 230](230-percentiles-and-box-plots/note.md) |
| Quotient rule | $(f/g)' = (f'g - fg')/g^2$. | [Maths Note 600](600-derivatives-of-one-variable/note.md) |
| Random experiment | An experiment whose outcome cannot be predicted, such as a coin toss. | [Maths Note 240](240-random-variables-and-distributions/note.md) |
| Random forest | Bagging with decision trees as the base models. | [Note 108](108-random-forest-intro/note.md) |
| Random initialization | Starting a model's parameters at random values, often drawn from a uniform distribution. | [Maths Note 261](261-uniform-and-log-normal/note.md) |
| Random oversampling | Copying randomly chosen minority rows until the classes are equal. | [Note 133](133-imbalanced-data/note.md) |
| Random patches | Bagging in which each model gets random rows and random columns. | [Note 105](105-bagging-intuition/note.md) |
| Random sample imputation | Filling each gap with a value drawn at random from the column's known values. | [Note 38](38-missing-indicator-random-sample/note.md) |
| Random seed | A number that fixes a random number generator so that a run can be repeated exactly. | [Note 117](117-adaboost-from-scratch/note.md) |
| Random subspaces | Bagging in which each model gets all rows but a random subset of columns. | [Note 105](105-bagging-intuition/note.md) |
| Random undersampling | Dropping randomly chosen majority rows until the classes are equal. | [Note 133](133-imbalanced-data/note.md) |
| Random variable | The possible numerical outcomes of a random experiment; strictly, a function from outcomes to numbers. | [Maths Note 240](240-random-variables-and-distributions/note.md) |
| RandomForestClassifier | scikit-learn's random forest for classification. | [Note 108](108-random-forest-intro/note.md) |
| RandomForestRegressor | scikit-learn's random forest for regression. | [Note 108](108-random-forest-intro/note.md) |
| Randomised controlled trial | An experiment that assigns a treatment at random, to test causation. | [Maths Note 231](231-covariance-and-correlation/note.md) |
| Randomized SVD | A fast method that finds only the top $k$ singular vectors, used by scikit-learn for large data. | [Maths Note 613](613-svd-in-machine-learning/note.md) |
| RandomizedSearchCV | Tuning that cross-validates a fixed number of randomly drawn hyperparameter combinations. | [Note 99](99-regression-trees/note.md) |
| Range | The largest value minus the smallest. | [Maths Note 222](222-measures-of-dispersion/note.md) |
| Rank (of a matrix) | The number of linearly independent columns. | [Maths Note 490](490-linear-combinations-span-and-basis/note.md) |
| Rank | The number of axes of a tensor (ndim in NumPy). | [Note 11](11-tensors/note.md) |
| Rank-$k$ approximation (truncated SVD) | The sum of the first $k$ layers, $\hat{A}_k = U_k\Sigma_kV_k^{\mathsf T}$. | [Maths Note 612](612-low-rank-approximation/note.md) |
| Rank-1 layer | One term $\sigma_i\mathbf{u}_i\mathbf{v}_i^{\mathsf T}$ of the SVD written as a sum. | [Maths Note 612](612-low-rank-approximation/note.md) |
| RapidAPI | A website listing many APIs, including free ones. | [Note 17](17-fetching-data-from-api/note.md) |
| Rate $\lambda$ | The average number of events per interval; the only parameter of the Poisson distribution. | [Maths Note 560](560-poisson-distribution/note.md) |
| Rate limit | The most requests an API accepts in a given time. | [Note 17](17-fetching-data-from-api/note.md) |
| Rate of change | How much one quantity changes per unit change of another; the meaning of a derivative. | [DL Note 1017](1017-backpropagation-why/note.md) |
| Rate parameter $\lambda$ | The average number of events per unit time; the average wait is $1/\lambda$. | [Maths Note 632](632-mle-for-common-distributions/note.md) |
| Raw data | Data as it arrives, before any preparation. | [Note 23](23-what-is-feature-engineering/note.md) |
| Raw string | A Python string written `r"..."`, in which a backslash is kept as it is. | [Note 33](33-mixed-variables/note.md) |
| RBF kernel | Radial basis function kernel, built on $e^{-(\text{distance})^2}$; the most used SVM kernel. | [Note 95](95-kernel-trick-intuition/note.md) |
| Reader | What `read_csv` returns with `chunksize`: it hands out one chunk at a time. | [Note 15](15-working-with-csv/note.md) |
| Recall (sensitivity) | Of all items that really are positive, the fraction the model found. | [Note 14](14-framing-ml-problem/note.md) |
| Reciprocal transform | Replacing each value with $1/x$; reverses the order of the values. | [Note 30](30-function-transformer/note.md) |
| Recommendation engine | A model that suggests items, such as movies, to users. | [Note 4](04-batch-learning/note.md) |
| Recommender system | A system that suggests items a user is likely to like. | [Maths Note 360](360-vectors-and-feature-vectors/note.md) |
| Recurrent layer | A hidden layer whose output at one time step is an input to itself at the next. | [DL Note 1056](1056-rnn-forward-propagation/note.md) |
| Recurrent neural network (RNN) | A network whose hidden-layer output is fed back in, so it remembers earlier steps of a sequence. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| Recursion | A function that calls itself on smaller inputs. | [DL Note 1019](1019-mlp-memoization/note.md) |
| Reduced sample space | The outcomes that remain possible once the condition is known. | [Note 82](82-conditional-probability/note.md) |
| Reference category | The category whose dummy column is dropped; it is shown by all zeros. | [Note 27](27-one-hot-encoding/note.md) |
| Reflection | An orthogonal transformation that mirrors space; determinant $-1$. | [Maths Note 610](610-svd-geometry/note.md) |
| Regression metric | A number that summarises how close a regression model's predictions are to the true values. | [Note 52](52-regression-metrics/note.md) |
| Regression output layer | One node per predicted number, with the linear activation. | [DL Note 1013](1013-graduate-admission-ann/note.md) |
| Regression tree | A decision tree whose leaves predict numbers: the mean output of their training rows. | [Note 99](99-regression-trees/note.md) |
| Regression | Supervised learning with a numerical output. | [Note 3](03-types-of-ml/note.md) |
| Regular expression | A short pattern that describes text, such as `\d+` for "one or more digits". | [Note 33](33-mixed-variables/note.md) |
| Regularisation by randomisation | A name for dropout: reducing overfitting through random choices during training. | [DL Note 1025](1025-dropout-code/note.md) |
| Regularisation term $\Omega$ | XGBoost's penalty on a tree: $\gamma T + \frac{1}{2}\lambda\sum_j w_j^2$. | [Note 126](126-xgboost-maths/note.md) |
| Regularisation | Penalising large coefficients to reduce a model's variance. | [Note 62](62-bias-variance/note.md) |
| Reinforcement learning | Learning by acting and receiving rewards or punishments. | [Note 3](03-types-of-ml/note.md) |
| Reject $H_0$ | The decision that the data gives strong enough evidence against $H_0$. | [Maths Note 290](290-null-and-alternative-hypotheses/note.md) |
| Rejection region (critical region) | The values of the test statistic for which we reject $H_0$; its area under $H_0$ is $\alpha$. | [Maths Note 291](291-rejection-region-and-z-test/note.md) |
| Rejection region approach | Carrying out a test by checking whether the test statistic falls beyond a fixed boundary. | [Maths Note 290](290-null-and-alternative-hypotheses/note.md) |
| Relative frequency | A category's share of all the data: its frequency divided by the total. | [Maths Note 223](223-frequency-tables-and-graphs/note.md) |
| Relative path | A file's location, starting from the folder the code runs in. | [Note 15](15-working-with-csv/note.md) |
| ReLU | An activation function used in most deep networks, taught in a later Note. | [DL Note 1009](1009-mlp-intuition/note.md) |
| remainder | The `ColumnTransformer` parameter for untouched columns: `"drop"` (default) or `"passthrough"`. | [Note 28](28-column-transformer/note.md) |
| Representation learning (feature learning) | Letting the algorithm discover useful features from raw data, instead of engineering them by hand. | [DL Note 1002](1002-what-is-deep-learning/note.md) |
| Representative sample | A sample that reflects the whole situation fairly. | [Note 7](07-challenges-in-ml/note.md) |
| Request, response | What we send to a server, and what it sends back. | [Note 18](18-web-scraping/note.md) |
| requests | Python library that sends web requests. | [Note 17](17-fetching-data-from-api/note.md) |
| Required sample size | $n = (z_{\alpha/2}\,\sigma/E)^2$: the smallest sample giving a margin of error $E$. | [Maths Note 281](281-interpreting-confidence-intervals/note.md) |
| Resampling | Changing the number of rows per class to balance the data. | [Note 133](133-imbalanced-data/note.md) |
| Research hypothesis | Another name for the alternative hypothesis: the idea that came out of research. | [Maths Note 290](290-null-and-alternative-hypotheses/note.md) |
| Residual block | A block whose input is added to its output, giving the gradient a shortcut. | [DL Note 1018](1018-vanishing-exploding-gradients/note.md) |
| Residual sum of squares | The total squared error of the model's predictions. | [Note 52](52-regression-metrics/note.md) |
| Residual | The error on one data point: actual minus predicted value. | [Note 56](56-linear-regression-assumptions/note.md) |
| Response | What `requests.get` returns: the status code plus the reply. | [Note 17](17-fetching-data-from-api/note.md) |
| Responsibility $r_{nk}$ | The posterior probability that component $k$ produced point $n$. | [Maths Note 640](640-gaussian-mixture-models/note.md) |
| Retrain | Train a model again, here from scratch on old + new data. | [Note 4](04-batch-learning/note.md) |
| Reward / punishment | Good / bad feedback after an action. | [Note 3](03-types-of-ml/note.md) |
| Ridge regression | Linear regression with a penalty on the sum of squared coefficients. | [Note 63](63-ridge-regression-intuition/note.md) |
| Right singular vector ($\mathbf{v}_i$) | An input direction of the SVD; a column of $V$. | [Maths Note 610](610-svd-geometry/note.md) |
| Right-tailed and left-tailed test | One-tailed tests for $H_1: \mu > \mu_0$ and $H_1: \mu < \mu_0$. | [Maths Note 292](292-errors-power-and-tails/note.md) |
| River | A Python library for online machine learning. | [Note 5](05-online-learning/note.md) |
| RLHF | Reinforcement learning from human feedback: improving a model with a reward model trained on human rankings of its outputs. | [DL Note 1067](1067-history-of-llms/note.md) |
| RMSProp | AdaGrad with an EWMA of squared gradients in place of their sum: $v_t = \beta v_{t-1} + (1-\beta)g_t^2$. | [DL Note 1037](1037-rmsprop/note.md) |
| robots.txt | A file at a site's root listing what bots are asked not to visit. | [Note 18](18-web-scraping/note.md) |
| Robust scaling | Subtract the median and divide by the interquartile range; copes well with outliers. | [Note 25](25-normalization/note.md) |
| Robustness | Performing well even when the data changes somewhat. | [Note 101](101-ensemble-learning/note.md) |
| RobustScaler | scikit-learn's class for robust scaling. | [Note 25](25-normalization/note.md) |
| ROC curve | A plot of TPR against FPR for every threshold. | [Note 78](78-roc-auc/note.md) |
| Rollback | Restoring a model to an earlier, good version. | [Note 5](05-online-learning/note.md) |
| Root mean square | The square root of the average of squared values: the typical size of the gradients. | [DL Note 1037](1037-rmsprop/note.md) |
| Root mean squared error (RMSE) | The square root of MSE, in the output's units. | [Note 52](52-regression-metrics/note.md) |
| Root node | The first node of a tree, holding all the training rows. | [Note 97](97-decision-trees-intuition/note.md) |
| Rotation matrix | The matrix of a rotation about the origin; by 90°, columns $[0, 1]$ and $[-1, 0]$. | [Maths Note 500](500-linear-transformations-and-matrices/note.md) |
| Rotation | An orthogonal matrix with determinant $+1$: turns space without stretching or flipping. | [Maths Note 610](610-svd-geometry/note.md) |
| Row and column totals | The sums in the margins of a contingency table; each counts one whole event. | [Maths Note 340](340-venn-diagrams-and-contingency-tables/note.md) |
| Row sampling | Giving each base model a random subset of the rows. | [Note 108](108-random-forest-intro/note.md) |
| Row space | The span of the rows of a matrix; spanned by the $\mathbf{v}_i$ with $\sigma_i > 0$. | [Maths Note 611](611-computing-the-svd/note.md) |
| Row vector | A vector written as one row, shape $1 \times n$. | [Maths Note 360](360-vectors-and-feature-vectors/note.md) |
| RPM | Revolutions per minute: how fast a motor turns. | [Note 8](08-applications-of-ml/note.md) |
| Runge's phenomenon | The large swings of a high-degree polynomial near the ends of the interval it is fitted on. | [Note 121](121-gradient-boosting-regression-maths/note.md) |
| R² score (coefficient of determination) | 1 minus the model's squared error divided by the squared error of always predicting the mean: 1 is perfect, 0 is no better than the average. | [Note 31](31-power-transformer/note.md) |
| Saddle point | A flat point that curves up in one direction and down in another. | [Note 57](57-gradient-descent/note.md) |
| saga | A stochastic solver that supports every penalty, including Elastic Net. | [Note 81](81-logistic-hyperparameters/note.md) |
| Same-length many-to-many | Many-to-many with one output per input time step. | [DL Note 1058](1058-types-of-rnn/note.md) |
| SAMME | The AdaBoost variant in scikit-learn: alpha without the factor 1/2, only misclassified rows reweighted; same decisions. | [Note 117](117-adaboost-from-scratch/note.md) |
| SAMME.R | An AdaBoost variant that used predicted probabilities; removed from scikit-learn. | [Note 118](118-adaboost-hyperparameters/note.md) |
| Sample covariance ($s_{xy}$) | Covariance of a sample, dividing by $n - 1$. | [Maths Note 231](231-covariance-and-correlation/note.md) |
| Sample mean ($\bar{x}$) | The mean of the values in a sample. | [Maths Note 221](221-measures-of-central-tendency/note.md) |
| Sample proportion $\hat{p}$ | The share of a category in the sample, such as 26 men out of 60. | [Maths Note 570](570-choosing-a-hypothesis-test/note.md) |
| Sample size ($n$) | The number of values in one sample. | [Maths Note 271](271-sampling-distribution-and-clt/note.md) |
| Sample skewness $G_1$ | The third moment of the standardized values with a small-sample correction; what pandas' `skew()` returns. | [Maths Note 252](252-skewness/note.md) |
| Sample space | The set of all possible outcomes of an experiment. | [Note 82](82-conditional-probability/note.md) |
| Sample weight | A number attached to each row saying how important it is; AdaBoost starts every row at 1/n. | [Note 116](116-adaboost-step-by-step/note.md) |
| Sample | The part of the real world that our data covers. | [Note 7](07-challenges-in-ml/note.md) |
| sample_weight | The argument of `fit` that tells a scikit-learn model how much each row counts. | [Note 117](117-adaboost-from-scratch/note.md) |
| Sampler | In Optuna, the algorithm that suggests the next trial's hyperparameter values. | [Note 134](134-optuna/note.md) |
| Sampling bias | An unrepresentative sample caused by how the data was collected. | [Note 7](07-challenges-in-ml/note.md) |
| Sampling distribution of the sample mean | The distribution of the means of many samples of size $n$. | [Maths Note 271](271-sampling-distribution-and-clt/note.md) |
| Sampling distribution | The distribution of a statistic computed from many independent samples of the same size from one population. | [Maths Note 271](271-sampling-distribution-and-clt/note.md) |
| Sampling noise | An unrepresentative sample caused by being too small. | [Note 7](07-challenges-in-ml/note.md) |
| Sampling techniques | Ways of drawing a good sample from a population. | [Maths Note 220](220-what-is-statistics/note.md) |
| Saturating function | A function that squeezes any input into a bounded range, so its slope goes to 0 at the ends. | [DL Note 1027](1027-activation-functions/note.md) |
| Scalar product | Another name for the dot product, whose result is a scalar. | [Maths Note 362](362-dot-product-and-cosine-similarity/note.md) |
| Scalar | A single number: a 0D tensor. | [Note 11](11-tensors/note.md) |
| Scale (in SciPy) | SciPy's parameter for the exponential distribution, the average wait $1/\lambda$. | [Maths Note 632](632-mle-for-common-distributions/note.md) |
| Scaling (a vector) | Multiplying or dividing every component of a vector by a scalar. | [Maths Note 361](361-magnitude-distance-and-scalar-operations/note.md) |
| Scaling | Bringing input columns to similar ranges. | [Note 13](13-toy-project/note.md) |
| Scatter plot | One dot per row, with one numerical column on each axis. | [Note 21](21-bivariate-multivariate-analysis/note.md) |
| scikit-learn | Python's main library for classical ML. | [Note 13](13-toy-project/note.md) |
| SciPy | A library built on NumPy with more scientific routines. | [Maths Note 350](350-linear-algebra-roadmap/note.md) |
| Score | Likelihood × prior for a class; proportional to the posterior. | [Note 87](87-naive-bayes-intuition/note.md) |
| Scott's rule | A rule-of-thumb bandwidth: $s \times n^{-1/5}$. | [Maths Note 243](243-density-estimation-kde/note.md) |
| SDLC | Software development life cycle: the standard process for building ordinary software. | [Note 9](09-mldlc/note.md) |
| Search space | The ranges or lists of values each hyperparameter may take during tuning. | [Note 134](134-optuna/note.md) |
| Secant equation | $B_{k+1}\mathbf{s} = \mathbf{y}$: the Hessian stand-in must reproduce the last gradient change. | [Maths Note 603](603-hessian-and-multivariate-taylor/note.md) |
| Secant line | A straight line through two points of a curve. | [Maths Note 600](600-derivatives-of-one-variable/note.md) |
| Second moment $v_t$ | The EWMA of the squared gradient: an estimate of its mean square. | [DL Note 1038](1038-adam/note.md) |
| Second partial derivative | A partial derivative of a partial derivative, such as $\partial^2 f/\partial x^2$. | [Maths Note 603](603-hessian-and-multivariate-taylor/note.md) |
| Second-order condition | A twice-differentiable function is convex exactly when its Hessian is positive semi-definite everywhere. | [Maths Note 621](621-convex-sets-and-functions/note.md) |
| SelectKBest | scikit-learn class that scores every column and keeps the `k` best. | [Note 29](29-pipelines/note.md) |
| Self-attention | Attention in which the words of one sequence attend to each other. | [DL Note 1067](1067-history-of-llms/note.md) |
| Self-normalising | Keeping the activations of every layer at mean 0 and standard deviation 1 without a separate normalisation step. | [DL Note 1028](1028-relu-variants/note.md) |
| SELU | Scaled ELU, $\lambda \approx 1.0507$ times ELU with $\alpha \approx 1.6733$; self-normalising. | [DL Note 1028](1028-relu-variants/note.md) |
| Semester | One of two six-month halves of a year. | [Note 34](34-date-and-time/note.md) |
| Semi-supervised learning | Learning from a few labelled rows and many unlabelled ones. | [Note 3](03-types-of-ml/note.md) |
| Sentiment analysis | Deciding whether a text expresses a positive or negative opinion. | [Note 8](08-applications-of-ml/note.md) |
| Separator | The character between values on a line, such as `,` or a tab. | [Note 15](15-working-with-csv/note.md) |
| Sequence-to-sequence (seq2seq) model | A model whose input and output are both sequences. | [DL Note 1058](1058-types-of-rnn/note.md) |
| Sequence-to-sequence (seq2seq) task | A task with a sequence as input and a sequence as output, possibly of different lengths, such as translation. | [DL Note 1067](1067-history-of-llms/note.md) |
| Sequential data | Data fed one piece after another, in order. | [Note 5](05-online-learning/note.md) |
| Sequential learning | Training the base models one after another, each depending on the previous ones (boosting). | [Note 119](119-bagging-vs-boosting/note.md) |
| Sequential model | A Keras model whose layers form one stack, each feeding the next. | [DL Note 1011](1011-customer-churn-ann/note.md) |
| Series | pandas' one-column structure: values with an index. | [Note 15](15-working-with-csv/note.md) |
| Server | A computer that is always on and that users reach over the internet. | [Note 4](04-batch-learning/note.md) |
| set_output | Method that makes a transformer return a pandas DataFrame with `transform="pandas"`. | [Note 28](28-column-transformer/note.md) |
| set_params | Method that changes a model's settings after it is created. | [Note 111](111-random-forest-hyperparameters/note.md) |
| SGDClassifier | scikit-learn's linear classifier trained with SGD, with a choice of loss (perceptron, log loss, hinge, ...). | [DL Note 1006](1006-perceptron-loss/note.md) |
| SGDRegressor | A scikit-learn model that does linear regression step by step. | [Note 5](05-online-learning/note.md) |
| Shadow price | The multiplier read as the gain in the best value per extra unit of a limited resource. | [Maths Note 620](620-lagrange-multipliers/note.md) |
| Shallow decision tree | A decision tree with a small maximum depth; high bias, low variance. | [Note 119](119-bagging-vs-boosting/note.md) |
| Shape rule | $(m \times n)(n \times p) = m \times p$; the inner sizes must match. | [Maths Note 510](510-matrix-multiplication-as-composition/note.md) |
| Shape | The number of items along each axis. | [Note 11](11-tensors/note.md) |
| Shapiro-Wilk test | A statistical test of whether data follows a normal distribution. | [Note 56](56-linear-regression-assumptions/note.md) |
| Shear | A transformation that keeps $\hat{\imath}$ fixed and slants $\hat{\jmath}$, sliding horizontal lines sideways. | [Maths Note 500](500-linear-transformations-and-matrices/note.md) |
| Shifting | Adding or subtracting a scalar to every component of a vector. | [Maths Note 361](361-magnitude-distance-and-scalar-operations/note.md) |
| Short-term and long-term contributions | The terms of the BPTT gradient for recent and for distant inputs. | [DL Note 1060](1060-problems-with-rnn/note.md) |
| Shortcut variance formula | $\mathrm{Var}(X) = E[X^2] - (E[X])^2$. | [Maths Note 332](332-expected-value-and-variance/note.md) |
| Shrinkage (boosting) | Scaling down each base model's contribution so the ensemble learns in small steps and overfits less. | [Note 118](118-adaboost-hyperparameters/note.md) |
| Shrinkage | The pulling of coefficients towards 0 by a penalty. | [Note 63](63-ridge-regression-intuition/note.md) |
| Shuffling | Putting the rows in a new random order before each epoch. | [Note 60](60-mini-batch-gradient-descent/note.md) |
| Sigmoid function | $\sigma(z) = 1/(1 + e^{-z})$; an S-shaped curve that maps any number into the range 0 to 1. | [Note 72](72-sigmoid-function/note.md) |
| Sigmoid kernel | The S-shaped kernel $\tanh(\gamma\, x \cdot x' + r)$. | [Note 95](95-kernel-trick-intuition/note.md) |
| Sign function | Returns +1 for a positive number and -1 for a negative one. | [Note 115](115-adaboost-intuition/note.md) |
| Significance level ($\alpha$) | The probability of rejecting $H_0$ when it is actually true; fixed before the test, usually 0.05. | [Maths Note 291](291-rejection-region-and-z-test/note.md) |
| Similarity measure | A number that says how alike two vectors are. | [Maths Note 362](362-dot-product-and-cosine-similarity/note.md) |
| Similarity score (classification) | (sum of residuals)$^2$ / ($\sum p(1-p) + \lambda$), with $p$ the previous probabilities. | [Note 125](125-xgboost-classification/note.md) |
| Similarity score | (sum of residuals)$^2$ / (number of residuals + $\lambda$): how much a leaf's residuals agree. | [Note 124](124-xgboost-regression/note.md) |
| Similarity | How alike two data points are. | [Note 6](06-instance-vs-model-based/note.md) |
| Simple (elementary) event | An event with exactly one outcome. | [Maths Note 330](330-events-and-types-of-events/note.md) |
| Simple linear regression | Linear regression with one input column. | [Note 50](50-simple-linear-regression/note.md) |
| SimpleImputer | scikit-learn's class that fills missing values, by default with the column's mean. | [Note 28](28-column-transformer/note.md) |
| Simulated annealing | Lowering the learning rate gradually so the search settles down. | [Note 59](59-stochastic-gradient-descent/note.md) |
| Single linkage | Cluster distance = distance of the closest pair of points. | [Note 131](131-hierarchical-clustering/note.md) |
| Singular value ($\sigma_i$) | A stretch factor of a matrix: the length of $A\mathbf{v}_i$; never negative, listed largest first. | [Maths Note 610](610-svd-geometry/note.md) |
| Singular value decomposition (SVD) | Writing any matrix as $A = U\Sigma V^{\mathsf T}$: orthogonal, diagonal, orthogonal. | [Maths Note 610](610-svd-geometry/note.md) |
| Singular value equation | $A\mathbf{v}_i = \sigma_i\mathbf{u}_i$. | [Maths Note 610](610-svd-geometry/note.md) |
| Size | The total number of items: the product of the shape. | [Note 11](11-tensors/note.md) |
| Skewness | A number for how lopsided a distribution is: 0 symmetric, positive right tail, negative left tail. | [Note 20](20-univariate-analysis/note.md) |
| Skip connection through time | A connection from a hidden state several steps back directly to the present. | [DL Note 1060](1060-problems-with-rnn/note.md) |
| Slack (ξ) | How far a training point lies on the wrong side of its own hyperplane; 0 if it is on the correct side. | [Note 94](94-svm-soft-margin/note.md) |
| Slater's condition | Some point satisfies every inequality constraint strictly; together with convexity it guarantees strong duality. | [Maths Note 621](621-convex-sets-and-functions/note.md) |
| slice(0, 10) | Python object meaning positions 0 up to, not including, 10. | [Note 29](29-pipelines/note.md) |
| Slope | How much the output changes for one unit of change in the input; $m$ in $y = mx + b$. | [Note 50](50-simple-linear-regression/note.md) |
| Slow convergence | Reaching a good solution only after very many epochs. | [DL Note 1029](1029-weight-initialization/note.md) |
| SMOTE | Synthetic Minority Over-sampling Technique: new minority rows by interpolation between minority neighbours. | [Note 133](133-imbalanced-data/note.md) |
| Soft assignment | Sharing a point among clusters by probabilities instead of giving it to one. | [Maths Note 640](640-gaussian-mixture-models/note.md) |
| Soft thresholding | Moving a value towards 0 by a fixed amount, and setting it to 0 if it would cross 0. | [Note 68](68-lasso-sparsity/note.md) |
| Soft voting | Predicting the class with the highest average predicted probability across the base models. | [Note 103](103-voting-classifier/note.md) |
| Soft-margin SVM | The SVM that allows points inside the margin or on the wrong side, at a cost controlled by C. | [Note 94](94-svm-soft-margin/note.md) |
| Softmax function | Turns a list of scores into probabilities: $e^{z_k} / \sum_j e^{z_j}$. | [Note 79](79-softmax-regression/note.md) |
| Softmax output layer | An output layer with one node per class whose outputs are probabilities adding up to 1. | [DL Note 1012](1012-mnist-ann/note.md) |
| Softmax regression | Logistic regression extended to any number of classes using the softmax function. | [Note 79](79-softmax-regression/note.md) |
| Softplus | The function $\ln(1 + e^z)$, a smooth convex curve whose derivative is the sigmoid. | [Maths Note 621](621-convex-sets-and-functions/note.md) |
| Software integration | Building a model into the software that users use. | [Note 7](07-challenges-in-ml/note.md) |
| Solver | The method a model uses to find its best settings during training. | [Note 24](24-standardization/note.md) |
| Spam classifier | A program that decides whether an email is spam or not. | [Note 1](01-what-is-ml/note.md) |
| Span | The set of all linear combinations of some vectors. | [Maths Note 490](490-linear-combinations-span-and-basis/note.md) |
| Sparse categorical cross-entropy | Categorical cross-entropy for labels written as integers. | [DL Note 1012](1012-mnist-ann/note.md) |
| Sparse data | Two senses: a table that is mostly zeros (as after one-hot encoding); or, in many dimensions, a space where most regions hold no points. | [Note 25](25-normalization/note.md) |
| Sparse feature | A feature whose values are mostly zero, such as "studied at an IIT". | [DL Note 1036](1036-adagrad/note.md) |
| Sparse matrix | A table stored as only its non-zero entries, to save memory. | [Note 27](27-one-hot-encoding/note.md) |
| Sparse model | A model in which many coefficients are exactly 0. | [Note 67](67-lasso-regression/note.md) |
| Sparse representation | A representation where most values are 0. | [DL Note 1057](1057-rnn-sentiment-analysis/note.md) |
| sparse_output | `OneHotEncoder` parameter; `False` returns a normal NumPy array. | [Note 27](27-one-hot-encoding/note.md) |
| Sparsity | Having many coefficients exactly equal to 0. | [Note 68](68-lasso-sparsity/note.md) |
| Sparsity-aware split finding | Choosing, at each split, the side (left or right) for missing values by comparing the gain of both. | [Note 123](123-xgboost-intro/note.md) |
| Spectral norm | The largest stretch of a matrix, $\lVert M\rVert_2 = \sigma_1$. | [Maths Note 612](612-low-rank-approximation/note.md) |
| splitter | "best" searches every threshold; "random" draws thresholds at random. | [Note 98](98-decision-tree-hyperparameters/note.md) |
| Splitting criterion (threshold) | The value a numerical question compares against, such as petal length $\le$ 2.45. | [Note 97](97-decision-trees-intuition/note.md) |
| Splitting | Dividing a node's rows into parts according to a question. | [Note 97](97-decision-trees-intuition/note.md) |
| Spyder | A Python code editor that shows variables and tables in memory. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| SQL (Structured Query Language) | The language for asking a database for data. | [Note 16](16-working-with-json-and-sql/note.md) |
| SQLAlchemy | A Python library that connects to many kinds of database; pandas supports it fully. | [Note 16](16-working-with-json-and-sql/note.md) |
| SQLite | A database stored in a single file, built into Python, needing no server. | [Note 16](16-working-with-json-and-sql/note.md) |
| Square root transform | Replacing each value with $\sqrt{x}$; a milder version of the log. | [Note 30](30-function-transformer/note.md) |
| Square transform | Replacing each value with $x^2$; used for left-skewed data. | [Note 30](30-function-transformer/note.md) |
| Square-root rule | A rough starting value for k: about $\sqrt{n}$, made odd. | [Note 91](91-knn/note.md) |
| Squared loss (L2 loss) | Another name for the mean squared error used as a training loss. | [DL Note 1014](1014-dl-loss-functions/note.md) |
| squared_error | DecisionTreeRegressor's default criterion: split by mean squared error, leaves predict the mean. | [Note 99](99-regression-trees/note.md) |
| Stacking | An ensemble in which a meta-model learns how to weight the base models' outputs. | [Note 127](127-stacking-blending/note.md) |
| Stage-wise additive model | A model built as a sum of base models added one at a time. | [Note 115](115-adaboost-intuition/note.md) |
| staged_score | A method that gives an ensemble's score after each added stage. | [Note 118](118-adaboost-hyperparameters/note.md) |
| Standard basis ($\hat{\imath}$, $\hat{\jmath}$) | The unit vectors along the axes, $[1, 0]$ and $[0, 1]$ in 2D. | [Maths Note 490](490-linear-combinations-span-and-basis/note.md) |
| Standard deviation of a random variable | The square root of its variance, in the units of $X$. | [Maths Note 332](332-expected-value-and-variance/note.md) |
| Standard deviation | How far values typically lie from the mean; divide by $n - 1$ for a sample (pandas default) or by $n$ for a population (NumPy default). | [Note 19](19-understanding-your-data/note.md) |
| Standard error | The standard deviation of a sampling distribution; for the mean, $\sigma/\sqrt{n}$. | [Maths Note 271](271-sampling-distribution-and-clt/note.md) |
| Standard normal distribution | The normal distribution with mean 0 and standard deviation 1, written $Z \sim N(0, 1)$. | [Maths Note 251](251-standard-normal-and-z-table/note.md) |
| Standardization | Scaling a column to mean 0 and standard deviation 1. | [Note 13](13-toy-project/note.md) |
| standardize | The `PowerTransformer` parameter (on by default) that rescales the output to mean 0 and standard deviation 1. | [Note 31](31-power-transformer/note.md) |
| StandardScaler | scikit-learn's class that standardizes columns with `fit` and `transform`. | [Note 24](24-standardization/note.md) |
| Static model | A model that learns nothing new after deployment. | [Note 4](04-batch-learning/note.md) |
| Stationary point | A point where the derivative (or every partial derivative) is zero: a minimum, a maximum or a saddle point. | [Maths Note 590](590-convex-and-non-convex-cost-functions/note.md) |
| Statistic | A number computed from a sample, such as $\bar{x}$; an estimate of a parameter. | [Maths Note 220](220-what-is-statistics/note.md) |
| Statistical hypothesis test | A method of statistical inference that decides whether the data sufficiently supports a hypothesis about a population parameter. | [Maths Note 290](290-null-and-alternative-hypotheses/note.md) |
| Statistical moments | Averages of distances from the mean raised to a power: mean, variance, skewness, kurtosis. | [Maths Note 260](260-kurtosis-and-qq-plots/note.md) |
| Statistical test | A procedure for hypothesis testing. | [Maths Note 220](220-what-is-statistics/note.md) |
| Statistics | The branch of mathematics for collecting, analysing, interpreting and presenting data. | [Maths Note 220](220-what-is-statistics/note.md) |
| statsmodels | A Python library for statistical models and tests. | [Note 56](56-linear-regression-assumptions/note.md) |
| Status code | A number saying how a request went: 200 OK, 401, 404, 500. | [Note 17](17-fetching-data-from-api/note.md) |
| Status quo | Another name for the null hypothesis: the current state of things. | [Maths Note 290](290-null-and-alternative-hypotheses/note.md) |
| Steepest ascent | The direction in which $f$ increases fastest: the direction of the gradient. | [Maths Note 601](601-partial-derivatives-and-gradients/note.md) |
| Step function | A function that outputs 1 for positive inputs and 0 otherwise. | [Note 70](70-perceptron-trick/note.md) |
| step__parameter | How a pipeline step's parameter is named: step name, two underscores, parameter name. | [Note 29](29-pipelines/note.md) |
| Stochastic error | A random, unmeasurable influence that scatters data around its trend. | [Note 50](50-simple-linear-regression/note.md) |
| Stochastic gradient descent (SGD) | Gradient descent that uses one random row for every update. | [Note 58](58-batch-gradient-descent/note.md) |
| Stochastic | Involving randomness. | [Note 59](59-stochastic-gradient-descent/note.md) |
| Stopping rule | The condition that ends a training loop: a fixed number of loops, or convergence. | [DL Note 1005](1005-perceptron-trick/note.md) |
| str dtype | The pandas 3 type for text columns, replacing `object`. | [Note 33](33-mixed-variables/note.md) |
| str.extract | The pandas method that returns the part of each value matching a regular expression. | [Note 33](33-mixed-variables/note.md) |
| Strength of a relationship | How closely the points follow a straight line; measured by $\lvert r \rvert$. | [Maths Note 231](231-covariance-and-correlation/note.md) |
| Strength of evidence | How strongly the data speaks against $H_0$; the rejection region approach does not measure it. | [Maths Note 291](291-rejection-region-and-z-test/note.md) |
| Strictly convex function | A function that lies strictly below every chord between two different points; it has at most one minimum. | [Maths Note 590](590-convex-and-non-convex-cost-functions/note.md) |
| Strike rate | A batter's runs per 100 balls faced. | [Note 45](45-feature-construction-splitting/note.md) |
| Strong duality | The dual maximum equals the primal minimum; true for convex problems. | [Maths Note 620](620-lagrange-multipliers/note.md) |
| Strong learner | A model with high accuracy. | [Note 115](115-adaboost-intuition/note.md) |
| Structure score | The best objective of a tree, $-\frac{1}{2}\sum_j G_j^2/(H_j + \lambda) + \gamma T$; lower is better. | [Note 126](126-xgboost-maths/note.md) |
| Student's t-distribution | The symmetric, fat-tailed distribution of $(\bar{X} - \mu)/(s/\sqrt{n})$; approaches the standard normal as $n$ grows. | [Maths Note 282](282-t-procedure/note.md) |
| Study | In Optuna, one optimisation session: a collection of trials aimed at optimising the objective function. | [Note 134](134-optuna/note.md) |
| Sub-network | The smaller network left after some nodes are switched off; it shares the full network's weights. | [DL Note 1024](1024-dropout/note.md) |
| Subgradient | A slope used at a corner of a function, where the ordinary derivative does not exist. | [DL Note 1006](1006-perceptron-loss/note.md) |
| Subscription | A model where customers pay a fixed amount every month (or year). | [Note 14](14-framing-ml-problem/note.md) |
| Sum of squared errors (SSE) | The sum of the squared residuals; a regression tree splits where the SSE of the two sides is smallest. | [Note 99](99-regression-trees/note.md) |
| Sum of squared errors | The squares of all the errors added up; the quantity the best-fit line makes smallest. | [Note 50](50-simple-linear-regression/note.md) |
| Sum of squares (SST, SSB, SSW) | Total, between-group and within-group squared distances; $SST = SSB + SSW$. | [Maths Note 572](572-one-way-anova/note.md) |
| Summation ($z$) | The weighted sum $w_1x_1 + w_2x_2 + \dots + b$ inside a perceptron. | [DL Note 1004](1004-perceptron/note.md) |
| Supervised binning | Binning that also uses the target, such as decision tree binning. | [Note 32](32-binning-binarization/note.md) |
| Supervised learning | Learning from data with inputs and outputs, to predict outputs. | [Note 3](03-types-of-ml/note.md) |
| Supervision | Correct answers that guide an algorithm while it learns. | [Note 3](03-types-of-ml/note.md) |
| Support vector machine (SVM) | A classifier that separates the classes with the hyperplane that has the widest margin. | [Note 92](92-svm-intuition/note.md) |
| Support vector regression (SVR) | The regression version of SVM. | [Note 92](92-svm-intuition/note.md) |
| Support vectors | The training points that lie on $\pi^+$ or $\pi^-$; they alone fix the SVM line. | [Note 92](92-svm-intuition/note.md) |
| Support | The number of items that really belong to a class. | [Note 77](77-precision-recall-f1/note.md) |
| Sure (certain) event | The whole sample space; probability 1. | [Maths Note 330](330-events-and-types-of-events/note.md) |
| Surge pricing | Raising fares when demand is much higher than supply. | [Note 8](08-applications-of-ml/note.md) |
| Surrogate model | The model of the unknown score function that Bayesian optimisation builds from the trials. | [Note 134](134-optuna/note.md) |
| Survival function | One minus the CDF: the probability of a value above $x$; `sf` in scipy. | [Maths Note 270](270-bernoulli-and-binomial/note.md) |
| SVD (singular value decomposition) | A factorisation that works for any matrix, square or not. | [Maths Note 350](350-linear-algebra-roadmap/note.md) |
| Symbolic AI | Early AI where humans write the knowledge as rules. | [Note 2](02-ai-vs-ml-vs-dl/note.md) |
| Symmetric matrix | A square matrix equal to its own transpose. | [Maths Note 610](610-svd-geometry/note.md) |
| Symmetry problem | Nodes that start with equal weights get equal updates and stay identical, so a layer acts like one node. | [DL Note 1029](1029-weight-initialization/note.md) |
| Synthetic data | Rows created by an algorithm rather than collected. | [Note 133](133-imbalanced-data/note.md) |
| T critical value | $t_{\alpha/2,\,n-1}$: the t value leaving $\alpha/2$ in each tail; 2.045 for 95% and $n = 30$. | [Maths Note 282](282-t-procedure/note.md) |
| T statistic | The value of $t$ computed from the sample in a t-test. | [Maths Note 301](301-one-sample-t-test/note.md) |
| T-procedure | The confidence interval $\bar{x} \pm t_{\alpha/2,\,n-1}\,s/\sqrt{n}$, used when $\sigma$ is unknown. | [Maths Note 282](282-t-procedure/note.md) |
| T-table | A table of t critical values by degrees of freedom and tail area. | [Maths Note 282](282-t-procedure/note.md) |
| T-test | A hypothesis test about means that uses the sample standard deviation and Student's t-distribution. | [Maths Note 301](301-one-sample-t-test/note.md) |
| Tag | One element of HTML, such as `<h2>TCS</h2>`. | [Note 18](18-web-scraping/note.md) |
| Tail (of a distribution) | The part of the curve far from the centre, where values are rare. | [Maths Note 250](250-normal-distribution/note.md) |
| Tail event | An event with a very low probability but a very large effect. | [Maths Note 252](252-skewness/note.md) |
| Tailedness | How much probability lies far from the mean, in the tails. | [Maths Note 260](260-kurtosis-and-qq-plots/note.md) |
| Tangent line | The line that touches a curve at one point with the curve's slope there; the limit of secant lines. | [Maths Note 600](600-derivatives-of-one-variable/note.md) |
| Tangent plane | The flat plane that touches a surface at a point with the same gradient; the first-order Taylor approximation. | [Maths Note 603](603-hessian-and-multivariate-taylor/note.md) |
| Tanh (hyperbolic tangent) | The activation $(e^{z}-e^{-z})/(e^{z}+e^{-z})$, an S-curve from $-1$ to 1 with derivative $1 - \tanh^2(z)$. | [DL Note 1027](1027-activation-functions/note.md) |
| Target leakage | Building an input column from the answer itself, so the model sees information it would not have in real use. | [Note 52](52-regression-metrics/note.md) |
| Target | The output we predict, such as the class. | [DL Note 1027](1027-activation-functions/note.md) |
| Target, label | Other names for the output column. | [Note 3](03-types-of-ml/note.md) |
| Targeted marketing | Advertising only to the people most likely to buy. | [Note 8](08-applications-of-ml/note.md) |
| Taylor polynomial | The Taylor series cut after the $(x - x_0)^n$ term. | [Maths Note 600](600-derivatives-of-one-variable/note.md) |
| Taylor series | Approximation of a function near a point by a polynomial built from its derivatives there. | [Note 126](126-xgboost-maths/note.md) |
| Tensor | A container of numbers arranged along one or more axes. | [Note 11](11-tensors/note.md) |
| TensorFlow Playground | A website that trains small neural networks in the browser and shows their boundaries. | [DL Note 1007](1007-problem-with-perceptron/note.md) |
| TensorFlow | Google's deep learning library. | [DL Note 1001](1001-dl-scope-and-prerequisites/note.md) |
| Terminal region | The part of the input space that ends in one leaf of a tree, written $R_{jm}$ for leaf $j$ of tree $m$. | [Note 121](121-gradient-boosting-regression-maths/note.md) |
| Terminal velocity | The step size momentum reaches when every gradient is the same: $\eta g/(1-\beta)$. | [DL Note 1034](1034-sgd-with-momentum/note.md) |
| Test set | The part hidden during training, used to check the model. | [Note 13](13-toy-project/note.md) |
| Test statistic | The number a test computes from the sample to make its decision, such as $z$ or $t$. | [Maths Note 290](290-null-and-alternative-hypotheses/note.md) |
| tf.GradientTape | TensorFlow's tool that records a computation and returns its exact derivatives automatically. | [DL Note 1015](1015-backpropagation-what/note.md) |
| Theoretical (classical) probability | Favourable outcomes divided by all outcomes, for equally likely outcomes. | [Maths Note 331](331-empirical-and-theoretical-probability/note.md) |
| Theoretical distribution | The known distribution that data is compared with, for example on a Q-Q plot. | [Maths Note 260](260-kurtosis-and-qq-plots/note.md) |
| Theoretical quantile | Where a value would sit if the data were perfectly normal (the horizontal axis of a Q-Q plot). | [Note 30](30-function-transformer/note.md) |
| Thin (reduced) SVD | The SVD with only the columns of $U$ that meet the diagonal of $\Sigma$. | [Maths Note 610](610-svd-geometry/note.md) |
| Threshold (classification) | The probability above which a prediction counts as class 1. | [DL Note 1011](1011-customer-churn-ann/note.md) |
| Threshold | The value that separates 0 from 1 in binarization. | [Note 32](32-binning-binarization/note.md) |
| Tidy data | Data with one observation per row and one atomic value per cell. | [Note 45](45-feature-construction-splitting/note.md) |
| Time series | Data recorded at regular time intervals. | [Note 11](11-tensors/note.md) |
| Time step | One position in the sequence; word $j$ enters at $t = j$. | [DL Note 1056](1056-rnn-forward-propagation/note.md) |
| Timedelta | A length of time, the result of subtracting two datetimes. | [Note 34](34-date-and-time/note.md) |
| Timestamp | pandas' type for a single point in time. | [Note 34](34-date-and-time/note.md) |
| Title | The word before a name, such as Mr, Mrs, Miss or Master. | [Note 45](45-feature-construction-splitting/note.md) |
| Tokenization | Splitting a text into words (tokens). | [DL Note 1057](1057-rnn-sentiment-analysis/note.md) |
| Top categories | Keeping only the most frequent categories and merging the rest into one "uncommon" category. | [Note 27](27-one-hot-encoding/note.md) |
| Total responsibility $N_k$ | The sum of the responsibilities of component $k$ over all points. | [Maths Note 640](640-gaussian-mixture-models/note.md) |
| Total sum of squares | The total squared error of always predicting the mean. | [Note 52](52-regression-metrics/note.md) |
| TPE | Tree-structured Parzen Estimator, Optuna's default Bayesian sampler. | [Note 134](134-optuna/note.md) |
| TPU | Google's chip built only for deep learning maths. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| Train | Let a model learn by making predictions, measuring its errors and adjusting to reduce them. | [Note 2](02-ai-vs-ml-vs-dl/note.md) |
| Train-test split | Dividing the data into training and test sets. | [Note 13](13-toy-project/note.md) |
| Trainable parameter | A weight or bias whose value training must find. | [DL Note 1008](1008-mlp-notation/note.md) |
| Training (a perceptron) | Finding its weights and bias from labelled data. | [DL Note 1005](1005-perceptron-trick/note.md) |
| Training curves (learning curves) | Loss or accuracy plotted against the epoch, for the training and validation sets. | [DL Note 1011](1011-customer-churn-ann/note.md) |
| Training set | The part of the data the model learns from. | [Note 13](13-toy-project/note.md) |
| Training | The step in which an algorithm learns the pattern from data. | [Note 1](01-what-is-ml/note.md) |
| Transfer function | Another name for the activation function. | [DL Note 1027](1027-activation-functions/note.md) |
| Transfer learning | Reusing a network trained by others on a big dataset for our own problem. | [DL Note 1002](1002-what-is-deep-learning/note.md) |
| Transformation | A function that takes a vector in and gives a vector out. | [Maths Note 500](500-linear-transformations-and-matrices/note.md) |
| Transformer | A seq2seq architecture built from attention and dense layers, with no RNN, that processes all words in parallel. | [DL Note 1067](1067-history-of-llms/note.md) |
| transformers | The `ColumnTransformer` parameter: a list of (name, transformer, columns) tuples. | [Note 28](28-column-transformer/note.md) |
| transformers_ | List of a fitted column transformer's (name, transformer, columns) tuples. | [Note 29](29-pipelines/note.md) |
| Transpose | A matrix or vector with rows and columns swapped. | [Note 48](48-pca-step-by-step/note.md) |
| Tree-based algorithm | An algorithm that splits the data with simple conditions; hardly affected by outliers. | [Note 41](41-what-are-outliers/note.md) |
| Tree-level column sampling | Drawing one random set of columns per tree, before the tree is grown; every split of that tree uses only those columns (bagging). | [Note 110](110-bagging-vs-random-forest/note.md) |
| Trial (probability) | One run of a random experiment; it gives exactly one outcome. | [Maths Note 330](330-events-and-types-of-events/note.md) |
| Trial | In Optuna, one run of the objective function with one set of hyperparameter values. | [Note 134](134-optuna/note.md) |
| Trimmed mean | The mean after removing a fixed share of the smallest and largest values. | [Maths Note 221](221-measures-of-central-tendency/note.md) |
| Trimming percentage | The share of values removed from each end for a trimmed mean. | [Maths Note 221](221-measures-of-central-tendency/note.md) |
| Trimming | Removing the rows that hold outliers. | [Note 41](41-what-are-outliers/note.md) |
| True negative (TN) | Predicted negative, and actually negative. | [Note 76](76-accuracy-confusion-matrix/note.md) |
| True positive (TP) | Predicted positive, and actually positive. | [Note 76](76-accuracy-confusion-matrix/note.md) |
| True positive rate (TPR) | The fraction of real positives the model flags; the same as recall. | [Note 78](78-roc-auc/note.md) |
| Truncated normal | A normal distribution with values beyond two standard deviations redrawn. | [DL Note 1030](1030-xavier-he-initialization/note.md) |
| TruncatedSVD | scikit-learn's rank-$k$ SVD without centring; works on sparse matrices. | [Maths Note 613](613-svd-in-machine-learning/note.md) |
| TSV file | Like a CSV file, with tabs between values. | [Note 15](15-working-with-csv/note.md) |
| Tukey's HSD | A post-hoc test comparing every pair of groups with the overall Type I error held at $\alpha$. | [Maths Note 572](572-one-way-anova/note.md) |
| Two-tailed p-value | The tail areas beyond $-\lvert z \rvert$ and $+\lvert z \rvert$ together: $2\,\Phi(-\lvert z \rvert)$ for a z-test. | [Maths Note 300](300-p-values/note.md) |
| Two-tailed test (two-sided test) | A test whose $H_1$ is $\neq$, with $\alpha/2$ in each tail. | [Maths Note 292](292-errors-power-and-tails/note.md) |
| Two-way ANOVA | ANOVA for one numerical column and two categorical columns. | [Maths Note 570](570-choosing-a-hypothesis-test/note.md) |
| Type 1 mixed variable | A column whose cells each contain a category and a number together, such as `C85`. | [Note 33](33-mixed-variables/note.md) |
| Type 2 mixed variable | A column with a number in some rows and a category in others. | [Note 33](33-mixed-variables/note.md) |
| Type I error (false positive) | Rejecting $H_0$ when it is actually true; its probability is $\alpha$. | [Maths Note 292](292-errors-power-and-tails/note.md) |
| Type II error (false negative) | Failing to reject $H_0$ when it is actually false; its probability is $\beta$. | [Maths Note 292](292-errors-power-and-tails/note.md) |
| Unbiased estimator | An estimator whose average over many samples equals the true value. | [Maths Note 632](632-mle-for-common-distributions/note.md) |
| Underfitting | Being too simple to capture the pattern; fails on all data. | [Note 7](07-challenges-in-ml/note.md) |
| Underflow | A number too close to 0 for the computer to store, which then becomes 0 or loses precision. | [Note 73](73-log-loss/note.md) |
| Underlying distribution | The distribution that produced the data points. | [Maths Note 243](243-density-estimation-kde/note.md) |
| Understanding the data | The project stage where we learn what is in the data before cleaning or modelling. | [Note 19](19-understanding-your-data/note.md) |
| Unfolding (unrolling) | Drawing the recurrent layer once per time step, so the loop becomes a chain. | [DL Note 1056](1056-rnn-forward-propagation/note.md) |
| Uniform distribution | A distribution in which every outcome in a range is equally likely. | [Maths Note 261](261-uniform-and-log-normal/note.md) |
| Uniform weighting | Every neighbour counts equally: the fill is their plain mean. | [Note 39](39-knn-imputer/note.md) |
| Union (A ∪ B) | The event that A or B (or both) happens. | [Note 84](84-mutually-exclusive-events/note.md) |
| Unit hypercube | The same box in three or more dimensions (a unit cube in three). | [Note 25](25-normalization/note.md) |
| Unit square | The square from (0, 0) to (1, 1), into which min-max scaling presses two columns. | [Note 25](25-normalization/note.md) |
| Unit vector | A vector of length 1, used to describe a direction. | [Note 48](48-pca-step-by-step/note.md) |
| Univariate analysis | Studying one variable on its own. | [Note 20](20-univariate-analysis/note.md) |
| Univariate imputation | Imputation that uses only the column with the gap. | [Note 35](35-complete-case-analysis/note.md) |
| Universal approximation theorem | A network with a hidden layer and enough neurons can approximate any continuous function. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| Universal set ($U$) | The rectangle of a Venn diagram; in probability, the sample space, with $P(U) = 1$. | [Maths Note 340](340-venn-diagrams-and-contingency-tables/note.md) |
| Unpaired t-test | Another name for the independent two-sample t-test. | [Maths Note 302](302-two-sample-and-paired-t-tests/note.md) |
| Unreasonable effectiveness of data | With enough data, different algorithms perform about the same. | [Note 7](07-challenges-in-ml/note.md) |
| Unstable training | Training that does not progress because exploding gradients make the updates huge. | [DL Note 1060](1060-problems-with-rnn/note.md) |
| Unsupervised binning | Binning that uses only the column's own values. | [Note 32](32-binning-binarization/note.md) |
| Unsupervised learning | Learning from inputs only, to find structure. | [Note 3](03-types-of-ml/note.md) |
| Unsupervised pre-training | Setting a network's starting weights with a network trained layer by layer, instead of at random. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| Updates per epoch | $\lceil n / \text{batch size} \rceil$: the number of batches in one pass over the data. | [DL Note 1020](1020-gradient-descent-in-neural-networks/note.md) |
| Upper / lower limit | $\mu + 3\sigma$ and $\mu - 3\sigma$; values beyond them are outliers. | [Note 42](42-outliers-zscore/note.md) |
| Upsampling (resampling by weight) | Drawing a new dataset in which each row is picked with probability equal to its weight. | [Note 116](116-adaboost-step-by-step/note.md) |
| User-Agent | A short text a browser sends to say what it is. | [Note 15](15-working-with-csv/note.md) |
| UTF-8 | The most common encoding, and `read_csv`'s default. | [Note 15](15-working-with-csv/note.md) |
| Validation set (blending) | The hold-out part of the training data in blending, on which the meta-model is trained. | [Note 127](127-stacking-blending/note.md) |
| Validation set | Data held back from training to check and tune a model before the final test. | [Note 113](113-oob-score/note.md) |
| Vanilla gradient descent | Another name for batch gradient descent, the plain version. | [DL Note 1020](1020-gradient-descent-in-neural-networks/note.md) |
| Vanishing gradient | Gradients shrinking towards 0 as they pass through many layers, which slows learning. | [DL Note 1018](1018-vanishing-exploding-gradients/note.md) |
| Variable | One column of a dataset. | [Note 20](20-univariate-analysis/note.md) |
| Variable-length many-to-many | Many-to-many whose output length can differ from its input length. | [DL Note 1058](1058-types-of-rnn/note.md) |
| Variance (of a model) | How much a model's predictions change when it is trained on a different sample of the data; a different meaning from the variance of a column. | [Note 62](62-bias-variance/note.md) |
| Variance (of data) | The average squared distance of the values from their mean; the square of the standard deviation; divide by $n$ for a population (NumPy default) or $n - 1$ for a sample (pandas default). | [Note 47](47-pca-geometric-intuition/note.md) |
| Variance inflation factor (VIF) | $1 / (1 - R_j^2)$: how well the other inputs predict input $j$; above 5 signals multicollinearity. | [Note 56](56-linear-regression-assumptions/note.md) |
| Variance of a random variable | $\mathrm{Var}(X) = E[(X - E[X])^2]$: the expected squared distance from the expected value. | [Maths Note 332](332-expected-value-and-variance/note.md) |
| Variance reduction | The drop in mean squared error from a node to its children; the regression version of information gain. | [Note 99](99-regression-trees/note.md) |
| Vector (geometric view) | A point in a coordinate system, drawn as an arrow from the origin. | [Maths Note 360](360-vectors-and-feature-vectors/note.md) |
| Vector addition | Adding matching components; geometrically, placing the second arrow's tail at the first arrow's tip. | [Maths Note 490](490-linear-combinations-span-and-basis/note.md) |
| Vector | A list of numbers: a 1D tensor. | [Note 11](11-tensors/note.md) |
| Vector-valued function | $\mathbf{f}: \mathbb{R}^n \to \mathbb{R}^m$: several numbers in, several numbers out; a stack of $m$ ordinary functions. | [Maths Note 602](602-jacobian-and-matrix-gradients/note.md) |
| Vectorisation | Writing a computation as operations on whole arrays instead of Python loops. | [Note 58](58-batch-gradient-descent/note.md) |
| Vectorization | Converting data such as text into vectors of numbers. | [Note 11](11-tensors/note.md) |
| Velocity $v$ | The direction and size of the current move, built from past gradients: $v_t = \beta v_{t-1} + \eta\,\nabla L(w_t)$. | [DL Note 1034](1034-sgd-with-momentum/note.md) |
| Venn diagram | A picture of events as circles inside a rectangle; overlaps show shared outcomes. | [Maths Note 340](340-venn-diagrams-and-contingency-tables/note.md) |
| verbose | scikit-learn setting that prints progress messages during training. | [Note 106](106-bagging-classifier/note.md) |
| View Page Source | Browser option that shows a page's raw HTML. | [Note 18](18-web-scraping/note.md) |
| Virtual environment | A separate folder of Python and packages for one project. | [Note 12](12-setup-anaconda-jupyter-colab/note.md) |
| Vocabulary | The list of unique words in a set of texts. | [Note 11](11-tensors/note.md) |
| Volatile | Changing quickly and unpredictably. | [Note 14](14-framing-ml-problem/note.md) |
| Voting classifier | A classifier that combines several trained classifiers by voting. | [Note 103](103-voting-classifier/note.md) |
| Voting ensemble | Several models trained on the same data, combined by majority vote (classification) or mean (regression). | [Note 102](102-voting-ensemble/note.md) |
| Voting regressor | A regressor that predicts the mean (or weighted mean) of several trained regressors' predictions. | [Note 104](104-voting-regressor/note.md) |
| Vowpal Wabbit | A fast learning library that supports online learning. | [Note 5](05-online-learning/note.md) |
| Ward linkage | Cluster distance = increase in total squared distance to the centroids caused by merging. | [Note 131](131-hierarchical-clustering/note.md) |
| warm_start | Setting that keeps already-trained trees and adds new ones on the next fit. | [Note 111](111-random-forest-hyperparameters/note.md) |
| Wayback Machine | A web archive that keeps copies of web pages as they were. | [Note 18](18-web-scraping/note.md) |
| WCSS (inertia) | Within-cluster sum of squares: the sum of squared distances from each point to its own centroid. | [Note 128](128-kmeans-intuition/note.md) |
| Weak duality | Every value of the dual function is at most the primal minimum. | [Maths Note 620](620-lagrange-multipliers/note.md) |
| Weak learner | A model whose accuracy is only a little better than random guessing. | [Note 115](115-adaboost-intuition/note.md) |
| Web scraping | Writing code that extracts data from web pages. | [Note 7](07-challenges-in-ml/note.md) |
| Weight (in a network) | A learned number on a connection between two neurons. | [DL Note 1002](1002-what-is-deep-learning/note.md) |
| Weight decay factor | $1 - \eta\lambda$, the factor by which L2 regularisation shrinks every weight at each update. | [DL Note 1026](1026-regularization-in-dl/note.md) |
| Weight decay | Another name for the L2 penalty: each gradient step shrinks the coefficients by a fixed factor. | [Note 65](65-ridge-gradient-descent/note.md) |
| Weight matrix ($W^{k}$) | All weights entering layer $k$: one row per node of layer $k-1$, one column per node of layer $k$. | [DL Note 1010](1010-forward-propagation/note.md) |
| Weight update | Multiplying misclassified rows' weights by $e^{\alpha}$ and correct rows' weights by $e^{-\alpha}$. | [Note 116](116-adaboost-step-by-step/note.md) |
| Weight | A number saying how much a value counts in a weighted mean. | [Maths Note 221](221-measures-of-central-tendency/note.md) |
| Weight-based algorithm | An algorithm that learns one number per input column from all the points; sensitive to outliers. | [Note 41](41-what-are-outliers/note.md) |
| Weighted average | The mean of a metric over classes, weighted by each class's support. | [Note 77](77-precision-recall-f1/note.md) |
| Weighted error | The total sample weight of the rows a model misclassifies. | [Note 116](116-adaboost-step-by-step/note.md) |
| Weighted impurity decrease | A split's impurity drop, weighted by the share of rows reaching the node: the $\Delta$ of `min_impurity_decrease`. | [Note 114](114-feature-importance/note.md) |
| Weighted input ($z^{k}$) | $W^{k\mathsf T} a^{k-1} + b^{k}$: a layer's sums before the activation. | [DL Note 1010](1010-forward-propagation/note.md) |
| Weighted mean | A mean in which each value is multiplied by a weight saying how much it counts. | [Maths Note 221](221-measures-of-central-tendency/note.md) |
| Weighted quantile sketch | XGBoost's method for placing bin edges at (Hessian-weighted) quantiles of a column. | [Note 123](123-xgboost-intro/note.md) |
| weights | VotingClassifier and VotingRegressor setting that gives each base model's vote a different importance. | [Note 103](103-voting-classifier/note.md) |
| Welch's ANOVA | A version of ANOVA that does not assume equal variances. | [Maths Note 572](572-one-way-anova/note.md) |
| Welch's t-test | The two-sample t-test that does not assume equal variances. | [Maths Note 302](302-two-sample-and-paired-t-tests/note.md) |
| Winsorization | Capping with limits set by percentiles. | [Note 41](41-what-are-outliers/note.md) |
| Wisdom of the crowd | The combined judgement of many is often more accurate than any one member's. | [Note 101](101-ensemble-learning/note.md) |
| With replacement | Sampling in which each drawn item is put back, so it can be drawn again. | [Note 105](105-bagging-intuition/note.md) |
| Without replacement | Drawing items without putting them back, so later draws depend on earlier ones. | [Maths Note 330](330-events-and-types-of-events/note.md) |
| Word embedding | A learned real-valued vector for each word; words used in similar ways get nearby vectors. | [DL Note 1057](1057-rnn-sentiment-analysis/note.md) |
| X, y | Usual names for the input table and the output column. | [Note 11](11-tensors/note.md) |
| XAMPP | A free package that runs a web server and a MySQL server on one computer. | [Note 16](16-working-with-json-and-sql/note.md) |
| Xavier (Glorot) normal | Starting weights from a normal distribution with standard deviation $\sqrt{1/\text{fan-in}}$ or $\sqrt{2/(\text{fan-in} + \text{fan-out})}$. | [DL Note 1030](1030-xavier-he-initialization/note.md) |
| Xavier (Glorot) uniform | Starting weights spread evenly between $\pm\sqrt{6/(\text{fan-in} + \text{fan-out})}$. | [DL Note 1030](1030-xavier-he-initialization/note.md) |
| XGBoost | eXtreme Gradient Boosting: a library that implements gradient boosting with many speed and accuracy optimisations. | [Note 123](123-xgboost-intro/note.md) |
| XOR | The logic function that outputs 1 when exactly one of two inputs is 1. | [DL Note 1003](1003-nn-types-history-applications/note.md) |
| Yates' continuity correction | A small adjustment to $\chi^2$ for 2 by 2 tables, applied by default in `chi2_contingency`. | [Maths Note 571](571-chi-square-tests/note.md) |
| Yeo-Johnson transform | A variation of Box-Cox that also works on zero and negative values; scikit-learn's default. | [Note 31](31-power-transformer/note.md) |
| Z statistic | The value of $z$ computed from the sample in a z-test. | [Maths Note 291](291-rejection-region-and-z-test/note.md) |
| Z-procedure | The confidence interval $\bar{x} \pm z_{\alpha/2}\,\sigma/\sqrt{n}$, used when $\sigma$ is known. | [Maths Note 280](280-confidence-intervals-z-procedure/note.md) |
| Z-score method | Outlier detection that flags values more than 3 standard deviations from the mean; for roughly normal columns. | [Note 42](42-outliers-zscore/note.md) |
| Z-score normalization | Another name for standardization. | [Note 24](24-standardization/note.md) |
| Z-score | A value after standardization: how many standard deviations it lies from the mean. | [Note 24](24-standardization/note.md) |
| Z-table | A table of $\Phi(z)$ for many values of $z$, used to find normal probabilities. | [Maths Note 251](251-standard-normal-and-z-table/note.md) |
| Z-test (one-sample) | A test of a population mean when $\sigma$ is known and $\bar{X}$ is normal, using $z = (\bar{x} - \mu_0)/(\sigma/\sqrt{n})$. | [Maths Note 291](291-rejection-region-and-z-test/note.md) |
| Zero initialisation | Starting every weight (and bias) at 0; with ReLU or tanh nothing trains. | [DL Note 1029](1029-weight-initialization/note.md) |
| Zero padding (text) | Adding all-zero word vectors to shorter texts so that every text has the same length. | [DL Note 1055](1055-why-rnn/note.md) |
| Zero-centred activation | An activation whose outputs average about 0, positive and negative. | [DL Note 1027](1027-activation-functions/note.md) |
| Zero-frequency problem | A probability of 0 for a value never seen with a class, which forces that class's score to 0. | [Note 89](89-naive-bayes-code/note.md) |
| λ (lambda), alpha | The strength of the regularisation penalty; alpha in scikit-learn. | [Note 63](63-ridge-regression-intuition/note.md) |
