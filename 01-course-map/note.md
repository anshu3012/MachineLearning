---
title: "Course Map"
---

## 1. Overview

> **Key point:** The Course map ties every Note together. It shows where each idea sits in an ML project, how ideas connect, what to read first, and which algorithm to choose.

The Notes each teach one lesson. The Course map shows how those lessons fit together, in four views:

| View | Question it answers |
|---|---|
| **Pipeline map** | Where does this idea sit in a real ML project? |
| **Concept map** | How is this idea connected to the others? |
| **Learning path** | Which Notes should I read first? |
| **Algorithm chooser** | Which algorithm suits my problem? |

Each idea on the map is a **Concept**. Concepts already taught in a written Note are **confirmed**; the others are **draft**, shown faint, and are checked against their Video when their Note is written. So far, 143 of 152 Concepts are confirmed.

Every Note starts with a *Where this fits* box: a small Pipeline map with that Note's steps highlighted, plus what it builds on and what it leads to.

> **Extra:** This map is generated from one data file, `course_map/concepts.yaml`. An interactive version, where you can zoom, filter by step and click a Concept to see its links and Notes, runs with `python course_map/app.py`.

## 2. The Pipeline map

> **Key point:** Every ML project moves through the same steps, from framing the problem to monitoring the deployed model. Every Concept belongs to one step.

![The Pipeline map: 14 steps of an ML project](images/pipeline_overview.png)

Figure 1 shows the 14 steps. They follow the ML development life cycle: frame the problem, get and understand the data, clean it, engineer features, train and evaluate models, tune them, deploy, test and keep the model healthy.

Steps 3 (Understand data) and 4 (Clean) loop: exploring reveals what needs cleaning, and cleaning changes the data, so we explore again.

### 2.1 Step 0: Foundations

| Concept | Taught in | Status |
|---|---|---|
| Machine learning | [Note 1](../01-what-is-ml/note.md), [Note 2](../02-ai-vs-ml-vs-dl/note.md) | confirmed |
| Data mining | [Note 1](../01-what-is-ml/note.md), [Note 8](../08-applications-of-ml/note.md) | confirmed |
| Artificial intelligence | [Note 2](../02-ai-vs-ml-vs-dl/note.md) | confirmed |
| Symbolic AI and expert systems | [Note 2](../02-ai-vs-ml-vs-dl/note.md) | confirmed |
| Deep learning | [Note 2](../02-ai-vs-ml-vs-dl/note.md) | confirmed |
| Neural networks | [Note 2](../02-ai-vs-ml-vs-dl/note.md) | confirmed |
| Features | [Note 2](../02-ai-vs-ml-vs-dl/note.md), [Note 11](../11-tensors/note.md) | confirmed |
| Supervised learning | [Note 3](../03-types-of-ml/note.md) | confirmed |
| Regression problems | [Note 3](../03-types-of-ml/note.md) | confirmed |
| Classification problems | [Note 3](../03-types-of-ml/note.md) | confirmed |
| Unsupervised learning | [Note 3](../03-types-of-ml/note.md) | confirmed |
| Semi-supervised learning | [Note 3](../03-types-of-ml/note.md) | confirmed |
| Reinforcement learning | [Note 3](../03-types-of-ml/note.md) | confirmed |
| Batch (offline) learning | [Note 4](../04-batch-learning/note.md) | confirmed |
| Online learning | [Note 5](../05-online-learning/note.md) | confirmed |
| Out-of-core learning | [Note 5](../05-online-learning/note.md) | confirmed |
| Instance-based learning | [Note 6](../06-instance-vs-model-based/note.md) | confirmed |
| Model-based learning | [Note 6](../06-instance-vs-model-based/note.md) | confirmed |
| Applications of ML | [Note 8](../08-applications-of-ml/note.md) | confirmed |
| ML development life cycle | [Note 9](../09-mldlc/note.md), [Note 13](../13-toy-project/note.md) | confirmed |
| Tensors | [Note 11](../11-tensors/note.md) | confirmed |
| Setup: conda, Jupyter and Colab | [Note 12](../12-setup-anaconda-jupyter-colab/note.md) | confirmed |
| Eigenvectors and eigenvalues | [Note 48](../48-pca-step-by-step/note.md) | confirmed |
| Conditional probability | [Note 82](../82-conditional-probability/note.md) | confirmed |
| Independent and mutually exclusive events | [Note 83](../83-independent-events/note.md), [Note 84](../84-mutually-exclusive-events/note.md) | confirmed |
| Bayes' theorem | [Note 85](../85-bayes-theorem/note.md), [Note 86](../86-bayes-problem/note.md) | confirmed |

### 2.2 Step 1: Frame the problem

| Concept | Taught in | Status |
|---|---|---|
| Framing an ML problem | [Note 9](../09-mldlc/note.md), [Note 14](../14-framing-ml-problem/note.md) | confirmed |

### 2.3 Step 2: Get data

| Concept | Taught in | Status |
|---|---|---|
| Labelled data | [Note 3](../03-types-of-ml/note.md), [Note 7](../07-challenges-in-ml/note.md) | confirmed |
| Enough data | [Note 7](../07-challenges-in-ml/note.md) | confirmed |
| Sampling noise and bias | [Note 7](../07-challenges-in-ml/note.md) | confirmed |
| APIs | [Note 7](../07-challenges-in-ml/note.md), [Note 9](../09-mldlc/note.md), [Note 17](../17-fetching-data-from-api/note.md) | confirmed |
| Web scraping | [Note 7](../07-challenges-in-ml/note.md), [Note 9](../09-mldlc/note.md), [Note 18](../18-web-scraping/note.md) | confirmed |
| CSV files | [Note 9](../09-mldlc/note.md), [Note 13](../13-toy-project/note.md), [Note 15](../15-working-with-csv/note.md) | confirmed |
| JSON and SQL data | [Note 16](../16-working-with-json-and-sql/note.md) | confirmed |

### 2.4 Step 3: Understand data

| Concept | Taught in | Status |
|---|---|---|
| Exploratory data analysis | [Note 9](../09-mldlc/note.md), [Note 13](../13-toy-project/note.md), [Note 19](../19-understanding-your-data/note.md) | confirmed |
| Univariate analysis | [Note 9](../09-mldlc/note.md), [Note 20](../20-univariate-analysis/note.md) | confirmed |
| Bivariate and multivariate analysis | [Note 9](../09-mldlc/note.md), [Note 21](../21-bivariate-multivariate-analysis/note.md) | confirmed |
| Imbalanced data | [Note 9](../09-mldlc/note.md), Video 133, coming | confirmed |
| Variance | [Note 19](../19-understanding-your-data/note.md), [Note 47](../47-pca-geometric-intuition/note.md) | confirmed |
| Correlation | [Note 19](../19-understanding-your-data/note.md), [Note 21](../21-bivariate-multivariate-analysis/note.md) | confirmed |
| Descriptive statistics | [Note 19](../19-understanding-your-data/note.md) | confirmed |
| Skewness | [Note 20](../20-univariate-analysis/note.md) | confirmed |
| Pandas Profiling | [Note 22](../22-pandas-profiling/note.md) | confirmed |
| Q-Q plot | [Note 30](../30-function-transformer/note.md) | confirmed |
| Covariance and covariance matrix | [Note 48](../48-pca-step-by-step/note.md) | confirmed |

### 2.5 Step 4: Clean

| Concept | Taught in | Status |
|---|---|---|
| Poor-quality data | [Note 7](../07-challenges-in-ml/note.md), [Note 9](../09-mldlc/note.md) | confirmed |
| Missing values | [Note 7](../07-challenges-in-ml/note.md), [Note 9](../09-mldlc/note.md), [Note 23](../23-what-is-feature-engineering/note.md), [Note 35](../35-complete-case-analysis/note.md), [Note 36](../36-imputing-numerical-data/note.md), [Note 37](../37-missing-categorical-data/note.md), [Note 38](../38-missing-indicator-random-sample/note.md) | confirmed |
| Outliers | [Note 7](../07-challenges-in-ml/note.md), [Note 9](../09-mldlc/note.md), [Note 20](../20-univariate-analysis/note.md), [Note 23](../23-what-is-feature-engineering/note.md), [Note 41](../41-what-are-outliers/note.md) | confirmed |
| Simple imputation (mean, median, mode, constant) | [Note 23](../23-what-is-feature-engineering/note.md), [Note 36](../36-imputing-numerical-data/note.md), [Note 37](../37-missing-categorical-data/note.md) | confirmed |
| Complete case analysis | [Note 35](../35-complete-case-analysis/note.md) | confirmed |
| Missing indicator | [Note 38](../38-missing-indicator-random-sample/note.md) | confirmed |
| Random sample imputation | [Note 38](../38-missing-indicator-random-sample/note.md) | confirmed |
| KNN imputer | [Note 39](../39-knn-imputer/note.md) | confirmed |
| Iterative imputation (MICE) | [Note 40](../40-iterative-imputer-mice/note.md) | confirmed |
| Trimming outliers | [Note 41](../41-what-are-outliers/note.md), [Note 42](../42-outliers-zscore/note.md), [Note 43](../43-outliers-iqr/note.md), [Note 44](../44-outliers-percentile/note.md) | confirmed |
| Capping (winsorization) | [Note 41](../41-what-are-outliers/note.md), [Note 42](../42-outliers-zscore/note.md), [Note 43](../43-outliers-iqr/note.md), [Note 44](../44-outliers-percentile/note.md) | confirmed |
| Z-score outlier method | [Note 41](../41-what-are-outliers/note.md), [Note 42](../42-outliers-zscore/note.md) | confirmed |
| IQR outlier method | [Note 41](../41-what-are-outliers/note.md), [Note 43](../43-outliers-iqr/note.md) | confirmed |
| Percentile outlier method | [Note 41](../41-what-are-outliers/note.md), [Note 44](../44-outliers-percentile/note.md) | confirmed |

### 2.6 Step 5: Engineer features

| Concept | Taught in | Status |
|---|---|---|
| Feature construction and splitting | [Note 3](../03-types-of-ml/note.md), [Note 7](../07-challenges-in-ml/note.md), [Note 9](../09-mldlc/note.md), [Note 23](../23-what-is-feature-engineering/note.md), [Note 45](../45-feature-construction-splitting/note.md) | confirmed |
| Feature scaling | [Note 6](../06-instance-vs-model-based/note.md), [Note 9](../09-mldlc/note.md), [Note 13](../13-toy-project/note.md), [Note 23](../23-what-is-feature-engineering/note.md), [Note 24](../24-standardization/note.md) | confirmed |
| Feature engineering | [Note 7](../07-challenges-in-ml/note.md), [Note 9](../09-mldlc/note.md), [Note 23](../23-what-is-feature-engineering/note.md) | confirmed |
| Feature selection | [Note 9](../09-mldlc/note.md), [Note 13](../13-toy-project/note.md), [Note 23](../23-what-is-feature-engineering/note.md), [Note 46](../46-curse-of-dimensionality/note.md) | confirmed |
| Standardization | [Note 9](../09-mldlc/note.md), [Note 13](../13-toy-project/note.md), [Note 24](../24-standardization/note.md) | confirmed |
| One-hot encoding | [Note 11](../11-tensors/note.md), [Note 23](../23-what-is-feature-engineering/note.md), [Note 27](../27-one-hot-encoding/note.md) | confirmed |
| ML pipelines | [Note 13](../13-toy-project/note.md), [Note 29](../29-pipelines/note.md), [Note 38](../38-missing-indicator-random-sample/note.md) | confirmed |
| Encoding categorical data | [Note 23](../23-what-is-feature-engineering/note.md), [Note 26](../26-ordinal-label-encoding/note.md) | confirmed |
| Binning and binarization | [Note 23](../23-what-is-feature-engineering/note.md), [Note 32](../32-binning-binarization/note.md) | confirmed |
| Feature transformation | [Note 23](../23-what-is-feature-engineering/note.md) | confirmed |
| Normalization | [Note 25](../25-normalization/note.md) | confirmed |
| Ordinal and label encoding | [Note 26](../26-ordinal-label-encoding/note.md) | confirmed |
| Column transformer | [Note 28](../28-column-transformer/note.md) | confirmed |
| Function transformer | [Note 30](../30-function-transformer/note.md) | confirmed |
| Power transformer | [Note 31](../31-power-transformer/note.md) | confirmed |
| Mixed variables | [Note 33](../33-mixed-variables/note.md) | confirmed |
| Date and time features | [Note 34](../34-date-and-time/note.md) | confirmed |
| Feature importance | [Note 99](../99-regression-trees/note.md), [Note 100](../100-dtreeviz/note.md), [Note 114](../114-feature-importance/note.md) | confirmed |
| Permutation importance | [Note 114](../114-feature-importance/note.md) | confirmed |

### 2.7 Step 6: Reduce dimensions

| Concept | Taught in | Status |
|---|---|---|
| Dimensionality reduction | [Note 3](../03-types-of-ml/note.md), [Note 46](../46-curse-of-dimensionality/note.md) | confirmed |
| PCA | [Note 3](../03-types-of-ml/note.md), [Note 47](../47-pca-geometric-intuition/note.md), [Note 48](../48-pca-step-by-step/note.md), [Note 49](../49-pca-mnist/note.md) | confirmed |
| Feature extraction | [Note 23](../23-what-is-feature-engineering/note.md), [Note 46](../46-curse-of-dimensionality/note.md), [Note 47](../47-pca-geometric-intuition/note.md) | confirmed |
| Curse of dimensionality | [Note 46](../46-curse-of-dimensionality/note.md), [Note 91](../91-knn/note.md) | confirmed |

### 2.8 Step 7: Split

| Concept | Taught in | Status |
|---|---|---|
| Train-test split | [Note 13](../13-toy-project/note.md) | confirmed |
| Data leakage | [Note 13](../13-toy-project/note.md), [Note 91](../91-knn/note.md) | confirmed |

### 2.9 Step 8: Model

| Concept | Taught in | Status |
|---|---|---|
| Clustering | [Note 3](../03-types-of-ml/note.md), Video 128, coming | confirmed |
| Anomaly detection | [Note 3](../03-types-of-ml/note.md) | confirmed |
| Association rule learning | [Note 3](../03-types-of-ml/note.md) | confirmed |
| Stochastic gradient descent | [Note 5](../05-online-learning/note.md), [Note 59](../59-stochastic-gradient-descent/note.md) | confirmed |
| K-nearest neighbours | [Note 6](../06-instance-vs-model-based/note.md), [Note 91](../91-knn/note.md) | confirmed |
| Ensemble learning | [Note 9](../09-mldlc/note.md), [Note 101](../101-ensemble-learning/note.md) | confirmed |
| Logistic regression | [Note 13](../13-toy-project/note.md), [Note 70](../70-perceptron-trick/note.md), [Note 71](../71-perceptron-code/note.md), [Note 72](../72-sigmoid-function/note.md), [Note 73](../73-log-loss/note.md), [Note 75](../75-logistic-gradient-descent/note.md) | confirmed |
| Multicollinearity | [Note 27](../27-one-hot-encoding/note.md) | confirmed |
| Simple linear regression | [Note 50](../50-simple-linear-regression/note.md), [Note 51](../51-linear-regression-maths/note.md) | confirmed |
| Best-fit line and squared error | [Note 50](../50-simple-linear-regression/note.md), [Note 51](../51-linear-regression-maths/note.md) | confirmed |
| Ordinary least squares (closed form) | [Note 51](../51-linear-regression-maths/note.md) | confirmed |
| Multiple linear regression | [Note 53](../53-multiple-linear-regression/note.md), [Note 54](../54-multiple-lr-maths/note.md), [Note 55](../55-multiple-lr-code/note.md) | confirmed |
| Normal equation | [Note 54](../54-multiple-lr-maths/note.md), [Note 55](../55-multiple-lr-code/note.md) | confirmed |
| Assumptions of linear regression | [Note 56](../56-linear-regression-assumptions/note.md) | confirmed |
| Gradient descent | [Note 57](../57-gradient-descent/note.md) | confirmed |
| Convex and non-convex loss | [Note 57](../57-gradient-descent/note.md) | confirmed |
| Batch gradient descent | [Note 58](../58-batch-gradient-descent/note.md) | confirmed |
| Mini-batch gradient descent | [Note 60](../60-mini-batch-gradient-descent/note.md) | confirmed |
| Polynomial regression | [Note 61](../61-polynomial-regression/note.md) | confirmed |
| Polynomial features | [Note 61](../61-polynomial-regression/note.md), [Note 80](../80-polynomial-logistic-regression/note.md) | confirmed |
| Regularisation | [Note 63](../63-ridge-regression-intuition/note.md) | confirmed |
| Ridge regression | [Note 63](../63-ridge-regression-intuition/note.md), [Note 64](../64-ridge-regression-maths/note.md), [Note 65](../65-ridge-gradient-descent/note.md), [Note 66](../66-ridge-key-points/note.md) | confirmed |
| Lasso regression | [Note 67](../67-lasso-regression/note.md), [Note 68](../68-lasso-sparsity/note.md) | confirmed |
| Elastic Net | [Note 69](../69-elastic-net/note.md) | confirmed |
| Perceptron trick | [Note 70](../70-perceptron-trick/note.md), [Note 71](../71-perceptron-code/note.md) | confirmed |
| Sigmoid function | [Note 72](../72-sigmoid-function/note.md), [Note 74](../74-sigmoid-derivative/note.md) | confirmed |
| Log loss (binary cross entropy) | [Note 73](../73-log-loss/note.md) | confirmed |
| Softmax regression | [Note 79](../79-softmax-regression/note.md) | confirmed |
| Naive Bayes | [Note 87](../87-naive-bayes-intuition/note.md), [Note 88](../88-naive-bayes-maths/note.md), [Note 89](../89-naive-bayes-code/note.md), [Note 90](../90-gaussian-naive-bayes/note.md) | confirmed |
| Support vector machines | [Note 92](../92-svm-intuition/note.md), [Note 93](../93-svm-maths/note.md), [Note 94](../94-svm-soft-margin/note.md) | confirmed |
| Hinge loss and soft margin | [Note 94](../94-svm-soft-margin/note.md) | confirmed |
| Kernel trick | [Note 95](../95-kernel-trick-intuition/note.md), [Note 96](../96-kernel-trick-code/note.md) | confirmed |
| Entropy, information gain and Gini | [Note 97](../97-decision-trees-intuition/note.md) | confirmed |
| Decision trees | [Note 97](../97-decision-trees-intuition/note.md), [Note 98](../98-decision-tree-hyperparameters/note.md), [Note 100](../100-dtreeviz/note.md) | confirmed |
| Regression trees | [Note 99](../99-regression-trees/note.md) | confirmed |
| Boosting | [Note 101](../101-ensemble-learning/note.md), Video 119, coming | draft |
| Voting ensembles | [Note 102](../102-voting-ensemble/note.md), [Note 103](../103-voting-classifier/note.md), [Note 104](../104-voting-regressor/note.md) | confirmed |
| Bagging | [Note 105](../105-bagging-intuition/note.md), [Note 106](../106-bagging-classifier/note.md), [Note 107](../107-bagging-regressor/note.md) | confirmed |
| Random forest | [Note 108](../108-random-forest-intro/note.md), [Note 109](../109-random-forest-bias-variance/note.md), [Note 110](../110-bagging-vs-random-forest/note.md), [Note 111](../111-random-forest-hyperparameters/note.md), [Note 112](../112-random-forest-tuning/note.md), [Note 113](../113-oob-score/note.md), [Note 114](../114-feature-importance/note.md) | confirmed |
| AdaBoost | Video 115, coming, Video 116, coming, Video 117, coming, Video 118, coming | draft |
| Gradient boosting | Video 120, coming, Video 121, coming, Video 122, coming | draft |
| XGBoost | Video 123, coming, Video 124, coming, Video 125, coming, Video 126, coming | draft |
| Stacking and blending | Video 127, coming | draft |
| K-means | Video 128, coming, Video 129, coming, Video 130, coming | draft |
| Hierarchical clustering | Video 131, coming | draft |
| DBSCAN | Video 132, coming | draft |

### 2.10 Step 9: Evaluate

| Concept | Taught in | Status |
|---|---|---|
| Overfitting | [Note 7](../07-challenges-in-ml/note.md), [Note 61](../61-polynomial-regression/note.md), [Note 91](../91-knn/note.md) | confirmed |
| Underfitting | [Note 7](../07-challenges-in-ml/note.md), [Note 61](../61-polynomial-regression/note.md), [Note 91](../91-knn/note.md) | confirmed |
| Accuracy | [Note 13](../13-toy-project/note.md), [Note 76](../76-accuracy-confusion-matrix/note.md), [Note 91](../91-knn/note.md) | confirmed |
| Cross-validation | [Note 29](../29-pipelines/note.md), [Note 30](../30-function-transformer/note.md), [Note 91](../91-knn/note.md), [Note 103](../103-voting-classifier/note.md), [Note 104](../104-voting-regressor/note.md), [Note 112](../112-random-forest-tuning/note.md) | confirmed |
| Regression metrics | [Note 52](../52-regression-metrics/note.md) | confirmed |
| Bias-variance trade-off | [Note 62](../62-bias-variance/note.md), [Note 109](../109-random-forest-bias-variance/note.md) | confirmed |
| Confusion matrix | [Note 76](../76-accuracy-confusion-matrix/note.md) | confirmed |
| Precision, recall and F1 | [Note 77](../77-precision-recall-f1/note.md) | confirmed |
| ROC curve and AUC | [Note 78](../78-roc-auc/note.md) | confirmed |
| Decision surface and boundary | [Note 91](../91-knn/note.md) | confirmed |
| OOB score | [Note 105](../105-bagging-intuition/note.md), [Note 106](../106-bagging-classifier/note.md), [Note 107](../107-bagging-regressor/note.md), [Note 113](../113-oob-score/note.md) | confirmed |

### 2.11 Step 10: Tune

| Concept | Taught in | Status |
|---|---|---|
| Hyperparameter tuning | [Note 9](../09-mldlc/note.md), [Note 81](../81-logistic-hyperparameters/note.md), [Note 91](../91-knn/note.md), [Note 98](../98-decision-tree-hyperparameters/note.md), [Note 111](../111-random-forest-hyperparameters/note.md), Video 118, coming | confirmed |
| Grid and random search | [Note 29](../29-pipelines/note.md), [Note 38](../38-missing-indicator-random-sample/note.md), [Note 91](../91-knn/note.md), [Note 99](../99-regression-trees/note.md), [Note 106](../106-bagging-classifier/note.md), [Note 107](../107-bagging-regressor/note.md), [Note 112](../112-random-forest-tuning/note.md) | confirmed |
| Learning rate | [Note 57](../57-gradient-descent/note.md) | confirmed |
| Optuna | Video 134, coming | draft |

### 2.12 Step 11: Deploy

| Concept | Taught in | Status |
|---|---|---|
| Deployment | [Note 4](../04-batch-learning/note.md), [Note 7](../07-challenges-in-ml/note.md), [Note 9](../09-mldlc/note.md), [Note 13](../13-toy-project/note.md), [Note 29](../29-pipelines/note.md) | confirmed |
| Software integration | [Note 7](../07-challenges-in-ml/note.md) | confirmed |
| Saving models with pickle | [Note 9](../09-mldlc/note.md), [Note 13](../13-toy-project/note.md), [Note 29](../29-pipelines/note.md) | confirmed |

### 2.13 Step 12: Test

| Concept | Taught in | Status |
|---|---|---|
| Beta and A/B testing | [Note 9](../09-mldlc/note.md) | confirmed |

### 2.14 Step 13: Monitor and maintain

| Concept | Taught in | Status |
|---|---|---|
| Model drift | [Note 4](../04-batch-learning/note.md), [Note 9](../09-mldlc/note.md) | confirmed |
| Retraining | [Note 4](../04-batch-learning/note.md), [Note 5](../05-online-learning/note.md), [Note 9](../09-mldlc/note.md) | confirmed |
| MLOps and cost | [Note 7](../07-challenges-in-ml/note.md), [Note 9](../09-mldlc/note.md) | confirmed |

## 3. The Concept map

> **Key point:** Concepts are joined by five kinds of Link. Following the Links shows why each idea exists and what it is for.

Every Link has one of five types:

| Link | Meaning | Example |
|---|---|---|
| **needs** | must be understood first | logistic regression *needs* gradient descent |
| **is a kind of** | a special case | Ridge *is a kind of* regularisation |
| **fixes** | solves a problem | regularisation *fixes* overfitting |
| **compared with** | often confused or contrasted | bagging *compared with* boosting |
| **used in** | a tool used inside something else | feature scaling *used in* KNN |

The full map has 152 Concepts, too many for one page, so it is shown in six areas (Figures 2 to 7). In each figure, the area's own Concepts are large and coloured by pipeline step; Concepts from other areas that link in are small and grey. Faint dots and dotted lines are drafts.

![Concept map: Foundations and framing](images/concept_map_foundations.png){height=88%}

![Concept map: Getting, understanding and cleaning data](images/concept_map_data.png){height=88%}

![Concept map: Features, dimensions and splitting](images/concept_map_features.png){height=88%}

![Concept map: Models: regression, classification and gradient descent](images/concept_map_models_1.png){height=88%}

![Concept map: Models: trees, ensembles and clustering](images/concept_map_models_2.png){height=88%}

![Concept map: Evaluating, tuning and production](images/concept_map_production.png){height=88%}

## 4. The Learning path

> **Key point:** Before each Video, read the Notes it builds on.

Each row lists a Video's Concepts and the Notes to read first. Videos marked *coming* or *deferred* do not have a Note yet.

| Video | Concepts | Read first | Note |
|---|---|---|---|
| 1 | Data mining, Machine learning | nothing | written |
| 2 | Artificial intelligence, Deep learning, Features, Machine learning, Neural networks, Symbolic AI and expert systems | nothing | written |
| 3 | Anomaly detection, Association rule learning, Classification problems, Clustering, Dimensionality reduction, Feature construction and splitting, Labelled data, PCA, Regression problems, Reinforcement learning, Semi-supervised learning, Supervised learning, Unsupervised learning | [Note 2](../02-ai-vs-ml-vs-dl/note.md) | written |
| 4 | Batch (offline) learning, Deployment, Model drift, Retraining | nothing | written |
| 5 | Online learning, Out-of-core learning, Retraining, Stochastic gradient descent | [Note 4](../04-batch-learning/note.md) | written |
| 6 | Feature scaling, Instance-based learning, K-nearest neighbours, Model-based learning | [Note 3](../03-types-of-ml/note.md) | written |
| 7 | APIs, Deployment, Enough data, Feature construction and splitting, Feature engineering, Labelled data, MLOps and cost, Missing values, Outliers, Overfitting, Poor-quality data, Sampling noise and bias, Software integration, Underfitting, Web scraping | [Note 2](../02-ai-vs-ml-vs-dl/note.md) | written |
| 8 | Applications of ML, Data mining | [Note 2](../02-ai-vs-ml-vs-dl/note.md), [Note 3](../03-types-of-ml/note.md) | written |
| 9 | APIs, Beta and A/B testing, Bivariate and multivariate analysis, CSV files, Deployment, Ensemble learning, Exploratory data analysis, Feature construction and splitting, Feature engineering, Feature scaling, Feature selection, Framing an ML problem, Hyperparameter tuning, Imbalanced data, ML development life cycle, MLOps and cost, Missing values, Model drift, Outliers, Poor-quality data, Retraining, Saving models with pickle, Standardization, Univariate analysis, Web scraping | [Note 3](../03-types-of-ml/note.md), [Note 4](../04-batch-learning/note.md), [Note 5](../05-online-learning/note.md), [Note 7](../07-challenges-in-ml/note.md) | written |
| 11 | Features, One-hot encoding, Tensors | nothing | written |
| 12 | Setup: conda, Jupyter and Colab | nothing | written |
| 13 | Accuracy, CSV files, Data leakage, Deployment, Exploratory data analysis, Feature scaling, Feature selection, Logistic regression, ML development life cycle, ML pipelines, Saving models with pickle, Standardization, Train-test split | [Note 3](../03-types-of-ml/note.md), [Note 6](../06-instance-vs-model-based/note.md), [Note 7](../07-challenges-in-ml/note.md), [Note 9](../09-mldlc/note.md) | written |
| 14 | Framing an ML problem | [Note 3](../03-types-of-ml/note.md), [Note 4](../04-batch-learning/note.md), [Note 5](../05-online-learning/note.md) | written |
| 15 | CSV files | nothing | written |
| 16 | JSON and SQL data | nothing | written |
| 17 | APIs | [Note 16](../16-working-with-json-and-sql/note.md) | written |
| 18 | Web scraping | nothing | written |
| 19 | Correlation, Descriptive statistics, Exploratory data analysis, Variance | [Note 15](../15-working-with-csv/note.md) | written |
| 20 | Outliers, Skewness, Univariate analysis | [Note 9](../09-mldlc/note.md), [Note 19](../19-understanding-your-data/note.md) | written |
| 21 | Bivariate and multivariate analysis, Correlation | [Note 19](../19-understanding-your-data/note.md), [Note 20](../20-univariate-analysis/note.md) | written |
| 22 | Pandas Profiling | [Note 12](../12-setup-anaconda-jupyter-colab/note.md) | written |
| 23 | Binning and binarization, Encoding categorical data, Feature construction and splitting, Feature engineering, Feature extraction, Feature scaling, Feature selection, Feature transformation, Missing values, One-hot encoding, Outliers, Simple imputation (mean, median, mode, constant) | [Note 11](../11-tensors/note.md), [Note 13](../13-toy-project/note.md), [Note 20](../20-univariate-analysis/note.md), [Note 21](../21-bivariate-multivariate-analysis/note.md) | written |
| 24 | Feature scaling, Standardization | [Note 13](../13-toy-project/note.md), [Note 19](../19-understanding-your-data/note.md), [Note 23](../23-what-is-feature-engineering/note.md) | written |
| 25 | Normalization | [Note 24](../24-standardization/note.md) | written |
| 26 | Encoding categorical data, Ordinal and label encoding | [Note 13](../13-toy-project/note.md), [Note 23](../23-what-is-feature-engineering/note.md) | written |
| 27 | Multicollinearity, One-hot encoding | [Note 26](../26-ordinal-label-encoding/note.md) | written |
| 28 | Column transformer | [Note 23](../23-what-is-feature-engineering/note.md), [Note 26](../26-ordinal-label-encoding/note.md) | written |
| 29 | Cross-validation, Deployment, Grid and random search, ML pipelines, Saving models with pickle | [Note 13](../13-toy-project/note.md), [Note 17](../17-fetching-data-from-api/note.md), [Note 23](../23-what-is-feature-engineering/note.md), [Note 28](../28-column-transformer/note.md) | written |
| 30 | Cross-validation, Function transformer, Q-Q plot | [Note 20](../20-univariate-analysis/note.md), [Note 23](../23-what-is-feature-engineering/note.md) | written |
| 31 | Power transformer | [Note 20](../20-univariate-analysis/note.md), [Note 23](../23-what-is-feature-engineering/note.md), [Note 30](../30-function-transformer/note.md) | written |
| 32 | Binning and binarization | [Note 23](../23-what-is-feature-engineering/note.md) | written |
| 33 | Mixed variables | [Note 23](../23-what-is-feature-engineering/note.md) | written |
| 34 | Date and time features | [Note 15](../15-working-with-csv/note.md), [Note 23](../23-what-is-feature-engineering/note.md) | written |
| 35 | Complete case analysis, Missing values | [Note 9](../09-mldlc/note.md), [Note 20](../20-univariate-analysis/note.md) | written |
| 36 | Missing values, Simple imputation (mean, median, mode, constant) | [Note 9](../09-mldlc/note.md), [Note 13](../13-toy-project/note.md) | written |
| 37 | Missing values, Simple imputation (mean, median, mode, constant) | [Note 9](../09-mldlc/note.md), [Note 13](../13-toy-project/note.md) | written |
| 38 | Grid and random search, ML pipelines, Missing indicator, Missing values, Random sample imputation | [Note 28](../28-column-transformer/note.md), [Note 29](../29-pipelines/note.md), [Note 30](../30-function-transformer/note.md), [Note 37](../37-missing-categorical-data/note.md) | written |
| 39 | KNN imputer | [Note 6](../06-instance-vs-model-based/note.md), [Note 38](../38-missing-indicator-random-sample/note.md) | written |
| 40 | Iterative imputation (MICE) | [Note 37](../37-missing-categorical-data/note.md), [Note 38](../38-missing-indicator-random-sample/note.md) | written |
| 41 | Capping (winsorization), IQR outlier method, Outliers, Percentile outlier method, Trimming outliers, Z-score outlier method | [Note 9](../09-mldlc/note.md), [Note 19](../19-understanding-your-data/note.md), [Note 20](../20-univariate-analysis/note.md), [Note 24](../24-standardization/note.md) | written |
| 42 | Capping (winsorization), Trimming outliers, Z-score outlier method | [Note 19](../19-understanding-your-data/note.md), [Note 20](../20-univariate-analysis/note.md), [Note 24](../24-standardization/note.md), [Note 41](../41-what-are-outliers/note.md) | written |
| 43 | Capping (winsorization), IQR outlier method, Trimming outliers | [Note 19](../19-understanding-your-data/note.md), [Note 20](../20-univariate-analysis/note.md), [Note 41](../41-what-are-outliers/note.md) | written |
| 44 | Capping (winsorization), Percentile outlier method, Trimming outliers | [Note 41](../41-what-are-outliers/note.md) | written |
| 45 | Feature construction and splitting | [Note 23](../23-what-is-feature-engineering/note.md), [Note 30](../30-function-transformer/note.md), [Note 32](../32-binning-binarization/note.md) | written |
| 46 | Curse of dimensionality, Dimensionality reduction, Feature extraction, Feature selection | [Note 3](../03-types-of-ml/note.md), [Note 21](../21-bivariate-multivariate-analysis/note.md), [Note 23](../23-what-is-feature-engineering/note.md) | written |
| 47 | Feature extraction, PCA, Variance | [Note 19](../19-understanding-your-data/note.md), [Note 23](../23-what-is-feature-engineering/note.md), [Note 24](../24-standardization/note.md), [Note 46](../46-curse-of-dimensionality/note.md) | written |
| 48 | Covariance and covariance matrix, Eigenvectors and eigenvalues, PCA | [Note 3](../03-types-of-ml/note.md), [Note 24](../24-standardization/note.md), [Note 46](../46-curse-of-dimensionality/note.md), [Note 47](../47-pca-geometric-intuition/note.md) | written |
| 49 | PCA | [Note 24](../24-standardization/note.md), [Note 46](../46-curse-of-dimensionality/note.md), [Note 47](../47-pca-geometric-intuition/note.md), [Note 48](../48-pca-step-by-step/note.md) | written |
| 50 | Best-fit line and squared error, Simple linear regression | [Note 3](../03-types-of-ml/note.md), [Note 6](../06-instance-vs-model-based/note.md), [Note 27](../27-one-hot-encoding/note.md) | written |
| 51 | Best-fit line and squared error, Ordinary least squares (closed form), Simple linear regression | [Note 3](../03-types-of-ml/note.md), [Note 6](../06-instance-vs-model-based/note.md), [Note 27](../27-one-hot-encoding/note.md), [Note 48](../48-pca-step-by-step/note.md) | written |
| 52 | Regression metrics | [Note 51](../51-linear-regression-maths/note.md) | written |
| 53 | Multiple linear regression | [Note 3](../03-types-of-ml/note.md), [Note 51](../51-linear-regression-maths/note.md) | written |
| 54 | Multiple linear regression, Normal equation | [Note 3](../03-types-of-ml/note.md), [Note 51](../51-linear-regression-maths/note.md) | written |
| 55 | Multiple linear regression, Normal equation | [Note 3](../03-types-of-ml/note.md), [Note 51](../51-linear-regression-maths/note.md) | written |
| 56 | Assumptions of linear regression | [Note 27](../27-one-hot-encoding/note.md), [Note 30](../30-function-transformer/note.md) | written |
| 57 | Convex and non-convex loss, Gradient descent, Learning rate | [Note 24](../24-standardization/note.md), [Note 51](../51-linear-regression-maths/note.md) | written |
| 58 | Batch gradient descent | [Note 57](../57-gradient-descent/note.md) | written |
| 59 | Stochastic gradient descent | [Note 57](../57-gradient-descent/note.md) | written |
| 60 | Mini-batch gradient descent | [Note 57](../57-gradient-descent/note.md) | written |
| 61 | Overfitting, Polynomial features, Polynomial regression, Underfitting | [Note 13](../13-toy-project/note.md), [Note 55](../55-multiple-lr-code/note.md) | written |
| 62 | Bias-variance trade-off | [Note 61](../61-polynomial-regression/note.md) | written |
| 63 | Regularisation, Ridge regression | [Note 55](../55-multiple-lr-code/note.md), [Note 57](../57-gradient-descent/note.md), [Note 61](../61-polynomial-regression/note.md), [Note 62](../62-bias-variance/note.md) | written |
| 64 | Ridge regression | [Note 55](../55-multiple-lr-code/note.md), [Note 57](../57-gradient-descent/note.md), [Note 62](../62-bias-variance/note.md), [Note 63](../63-ridge-regression-intuition/note.md) | written |
| 65 | Ridge regression | [Note 55](../55-multiple-lr-code/note.md), [Note 57](../57-gradient-descent/note.md), [Note 62](../62-bias-variance/note.md), [Note 63](../63-ridge-regression-intuition/note.md) | written |
| 66 | Ridge regression | [Note 55](../55-multiple-lr-code/note.md), [Note 57](../57-gradient-descent/note.md), [Note 62](../62-bias-variance/note.md), [Note 63](../63-ridge-regression-intuition/note.md) | written |
| 67 | Lasso regression | [Note 63](../63-ridge-regression-intuition/note.md) | written |
| 68 | Lasso regression | [Note 63](../63-ridge-regression-intuition/note.md) | written |
| 69 | Elastic Net | [Note 27](../27-one-hot-encoding/note.md), [Note 63](../63-ridge-regression-intuition/note.md), [Note 66](../66-ridge-key-points/note.md), [Note 68](../68-lasso-sparsity/note.md) | written |
| 70 | Logistic regression, Perceptron trick | [Note 3](../03-types-of-ml/note.md), [Note 6](../06-instance-vs-model-based/note.md), [Note 57](../57-gradient-descent/note.md), [Note 61](../61-polynomial-regression/note.md) | written |
| 71 | Logistic regression, Perceptron trick | [Note 3](../03-types-of-ml/note.md), [Note 6](../06-instance-vs-model-based/note.md), [Note 57](../57-gradient-descent/note.md), [Note 61](../61-polynomial-regression/note.md) | written |
| 72 | Logistic regression, Sigmoid function | [Note 6](../06-instance-vs-model-based/note.md), [Note 57](../57-gradient-descent/note.md), [Note 61](../61-polynomial-regression/note.md), [Note 71](../71-perceptron-code/note.md) | written |
| 73 | Log loss (binary cross entropy), Logistic regression | [Note 57](../57-gradient-descent/note.md), [Note 61](../61-polynomial-regression/note.md), [Note 71](../71-perceptron-code/note.md), [Note 72](../72-sigmoid-function/note.md) | written |
| 74 | Sigmoid function | nothing | written |
| 75 | Logistic regression | [Note 61](../61-polynomial-regression/note.md), [Note 71](../71-perceptron-code/note.md), [Note 73](../73-log-loss/note.md), [Note 74](../74-sigmoid-derivative/note.md) | written |
| 76 | Accuracy, Confusion matrix | [Note 9](../09-mldlc/note.md), [Note 13](../13-toy-project/note.md) | written |
| 77 | Precision, recall and F1 | [Note 9](../09-mldlc/note.md), [Note 76](../76-accuracy-confusion-matrix/note.md) | written |
| 78 | ROC curve and AUC | [Note 76](../76-accuracy-confusion-matrix/note.md), [Note 77](../77-precision-recall-f1/note.md) | written |
| 79 | Softmax regression | [Note 27](../27-one-hot-encoding/note.md), [Note 75](../75-logistic-gradient-descent/note.md) | written |
| 80 | Polynomial features | nothing | written |
| 81 | Hyperparameter tuning | [Note 61](../61-polynomial-regression/note.md) | written |
| 82 | Conditional probability | nothing | written |
| 83 | Independent and mutually exclusive events | nothing | written |
| 84 | Independent and mutually exclusive events | nothing | written |
| 85 | Bayes' theorem | [Note 82](../82-conditional-probability/note.md) | written |
| 86 | Bayes' theorem | [Note 82](../82-conditional-probability/note.md) | written |
| 87 | Naive Bayes | [Note 3](../03-types-of-ml/note.md), [Note 84](../84-mutually-exclusive-events/note.md), [Note 86](../86-bayes-problem/note.md) | written |
| 88 | Naive Bayes | [Note 3](../03-types-of-ml/note.md), [Note 84](../84-mutually-exclusive-events/note.md), [Note 86](../86-bayes-problem/note.md) | written |
| 89 | Naive Bayes | [Note 3](../03-types-of-ml/note.md), [Note 84](../84-mutually-exclusive-events/note.md), [Note 86](../86-bayes-problem/note.md) | written |
| 90 | Naive Bayes | [Note 3](../03-types-of-ml/note.md), [Note 84](../84-mutually-exclusive-events/note.md), [Note 86](../86-bayes-problem/note.md) | written |
| 91 | Accuracy, Cross-validation, Curse of dimensionality, Data leakage, Decision surface and boundary, Grid and random search, Hyperparameter tuning, K-nearest neighbours, Overfitting, Underfitting | [Note 13](../13-toy-project/note.md), [Note 24](../24-standardization/note.md), [Note 37](../37-missing-categorical-data/note.md), [Note 38](../38-missing-indicator-random-sample/note.md) | written |
| 92 | Support vector machines | [Note 3](../03-types-of-ml/note.md), [Note 63](../63-ridge-regression-intuition/note.md), [Note 71](../71-perceptron-code/note.md) | written |
| 93 | Support vector machines | [Note 3](../03-types-of-ml/note.md), [Note 63](../63-ridge-regression-intuition/note.md), [Note 71](../71-perceptron-code/note.md) | written |
| 94 | Hinge loss and soft margin, Support vector machines | [Note 3](../03-types-of-ml/note.md), [Note 63](../63-ridge-regression-intuition/note.md), [Note 71](../71-perceptron-code/note.md) | written |
| 95 | Kernel trick | nothing | written |
| 96 | Kernel trick | nothing | written |
| 97 | Decision trees, Entropy, information gain and Gini | [Note 6](../06-instance-vs-model-based/note.md), [Note 91](../91-knn/note.md) | written |
| 98 | Decision trees, Hyperparameter tuning | [Note 6](../06-instance-vs-model-based/note.md), [Note 91](../91-knn/note.md), [Note 97](../97-decision-trees-intuition/note.md) | written |
| 99 | Feature importance, Grid and random search, Regression trees | [Note 38](../38-missing-indicator-random-sample/note.md), [Note 52](../52-regression-metrics/note.md), [Note 91](../91-knn/note.md), [Note 98](../98-decision-tree-hyperparameters/note.md) | written |
| 100 | Decision trees, Feature importance | [Note 6](../06-instance-vs-model-based/note.md), [Note 91](../91-knn/note.md), [Note 97](../97-decision-trees-intuition/note.md) | written |
| 101 | Boosting, Ensemble learning | [Note 62](../62-bias-variance/note.md), [Note 100](../100-dtreeviz/note.md) | written |
| 102 | Voting ensembles | [Note 84](../84-mutually-exclusive-events/note.md), [Note 91](../91-knn/note.md), [Note 101](../101-ensemble-learning/note.md) | written |
| 103 | Cross-validation, Voting ensembles | [Note 84](../84-mutually-exclusive-events/note.md), [Note 101](../101-ensemble-learning/note.md) | written |
| 104 | Cross-validation, Voting ensembles | [Note 84](../84-mutually-exclusive-events/note.md), [Note 101](../101-ensemble-learning/note.md) | written |
| 105 | Bagging, OOB score | [Note 91](../91-knn/note.md), [Note 99](../99-regression-trees/note.md), [Note 100](../100-dtreeviz/note.md), [Note 101](../101-ensemble-learning/note.md) | written |
| 106 | Bagging, Grid and random search, OOB score | [Note 98](../98-decision-tree-hyperparameters/note.md), [Note 100](../100-dtreeviz/note.md), [Note 101](../101-ensemble-learning/note.md), [Note 104](../104-voting-regressor/note.md) | written |
| 107 | Bagging, Grid and random search, OOB score | [Note 98](../98-decision-tree-hyperparameters/note.md), [Note 100](../100-dtreeviz/note.md), [Note 101](../101-ensemble-learning/note.md), [Note 104](../104-voting-regressor/note.md) | written |
| 108 | Random forest | [Note 91](../91-knn/note.md), [Note 98](../98-decision-tree-hyperparameters/note.md), [Note 100](../100-dtreeviz/note.md), [Note 107](../107-bagging-regressor/note.md) | written |
| 109 | Bias-variance trade-off, Random forest | [Note 91](../91-knn/note.md), [Note 98](../98-decision-tree-hyperparameters/note.md), [Note 100](../100-dtreeviz/note.md), [Note 107](../107-bagging-regressor/note.md) | written |
| 110 | Random forest | [Note 91](../91-knn/note.md), [Note 98](../98-decision-tree-hyperparameters/note.md), [Note 100](../100-dtreeviz/note.md), [Note 107](../107-bagging-regressor/note.md) | written |
| 111 | Hyperparameter tuning, Random forest | [Note 91](../91-knn/note.md), [Note 100](../100-dtreeviz/note.md), [Note 107](../107-bagging-regressor/note.md) | written |
| 112 | Cross-validation, Grid and random search, Random forest | [Note 91](../91-knn/note.md), [Note 100](../100-dtreeviz/note.md), [Note 107](../107-bagging-regressor/note.md), [Note 111](../111-random-forest-hyperparameters/note.md) | written |
| 113 | OOB score, Random forest | [Note 100](../100-dtreeviz/note.md), [Note 107](../107-bagging-regressor/note.md), [Note 111](../111-random-forest-hyperparameters/note.md), [Note 112](../112-random-forest-tuning/note.md) | written |
| 114 | Feature importance, Permutation importance, Random forest | [Note 107](../107-bagging-regressor/note.md), [Note 111](../111-random-forest-hyperparameters/note.md), [Note 112](../112-random-forest-tuning/note.md), [Note 113](../113-oob-score/note.md) | written |
| 115 | AdaBoost | [Note 101](../101-ensemble-learning/note.md) | coming |
| 116 | AdaBoost | [Note 101](../101-ensemble-learning/note.md) | coming |
| 117 | AdaBoost | [Note 101](../101-ensemble-learning/note.md) | coming |
| 118 | AdaBoost, Hyperparameter tuning | [Note 91](../91-knn/note.md), [Note 101](../101-ensemble-learning/note.md) | coming |
| 119 | Boosting | [Note 101](../101-ensemble-learning/note.md) | coming |
| 120 | Gradient boosting | [Note 57](../57-gradient-descent/note.md), Video 119, coming | coming |
| 121 | Gradient boosting | [Note 57](../57-gradient-descent/note.md), Video 119, coming | coming |
| 122 | Gradient boosting | [Note 57](../57-gradient-descent/note.md), Video 119, coming | coming |
| 123 | XGBoost | Video 122, coming | coming |
| 124 | XGBoost | Video 122, coming | coming |
| 125 | XGBoost | Video 122, coming | coming |
| 126 | XGBoost | Video 122, coming | coming |
| 127 | Stacking and blending | [Note 101](../101-ensemble-learning/note.md) | coming |
| 128 | Clustering, K-means | [Note 3](../03-types-of-ml/note.md), [Note 24](../24-standardization/note.md) | coming |
| 129 | K-means | [Note 24](../24-standardization/note.md), Video 128, coming | coming |
| 130 | K-means | [Note 24](../24-standardization/note.md), Video 128, coming | coming |
| 131 | Hierarchical clustering | Video 128, coming | coming |
| 132 | DBSCAN | Video 128, coming | coming |
| 133 | Imbalanced data | nothing | coming |
| 134 | Optuna | Video 118, coming | coming |

## 5. The Algorithm chooser

> **Key point:** Two questions narrow the choice: do we have labelled outputs, and are they numbers or categories?

![The Algorithm chooser (draft)](images/algorithm_chooser.png)

Figure 8 is a starting point, not a rule: in practice we try several suitable algorithms and compare them on a test set. It is a draft until the algorithm Notes are written.

## 6. Key terms

| Term | Meaning |
|---|---|
| Course map | The overview that ties all Notes together, in four views |
| Pipeline map | Where each Concept sits among the 14 steps of an ML project |
| Concept map | How Concepts are connected by Links |
| Learning path | Which Notes to read before which |
| Algorithm chooser | A flowchart from a problem's properties to suitable algorithms |
| Concept | One idea on the Course map |
| Link | A labelled connection between two Concepts |
| Draft / confirmed | Guessed from titles / checked against a written Note |
