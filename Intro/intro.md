# Types of ML

| Supervised Learning                        | Unsupervised Learning     | Semi-Supervised Learning          | Reinforcement Learning        |
| ------------------------------------------ | ------------------------- | --------------------------------- | ----------------------------- |
| Labeled data                               | Unlabeled data            | Mix of labeled and unlabeled data | Reward-based learning         |
| Classification  (if output is categorical) | Clustering                | Partially labeled data            | Agent-environment interaction |
| Regression (if the output is numerical)    | Dimensionality reduction  |                                   |                               |
|                                            | Anomaly Detection         |                                   |                               |
|                                            | Association Rule Learning |                                   |                               |

## Supervised Learning

Supervised learning is a type of machine learning where the algorithm is trained on labeled data. This means the dataset contains both input features and corresponding output labels, allowing the model to learn the relationship between them. The goal is to predict the output for new, unseen inputs based on this learned relationship.
Regression Dataset example

| IQ (Input) | CGPA (Input) | Placement (Output) |
| ---------- | ------------ | ------------------ |
| 100        | 9.5          | Yes                |
| 90         | 8.5          | Yes                |
| 80         | 7            | No                 |
| 70         | 6.5          | No                 |

Classification Dataset example

| IQ (Input) | CGPA (Input) | Package (Output) |
| ---------- | ------------ | ---------------- |
| 100        | 9.5          | 8.5              |
| 90         | 8.5          | 3.5              |
| 80         | 7            | 4.6              |
| 70         | 6.5          | 3.5              |

## Unsupervised Learning

Unsupervised learning is a type of machine learning where the algorithm learns patterns and structures from unlabeled data. Unlike supervised learning, there are no predefined labels or outcomes for the data. The goal is to identify hidden patterns, groupings, or structures within the dataset.

### 1. Clustering

Clustering is a technique in unsupervised learning, a type of machine learning where the algorithm learns patterns from unlabeled data (data without predefined categories or outcomes). The goal of clustering is to group similar data points into clusters based on their features, so that data points within the same cluster are more similar to each other than to those in other clusters.

Key Concepts:

* Unsupervised Learning: Unlike supervised learning, clustering doesn't rely on labeled data. Instead, it identifies inherent structures in the data.
* Clusters: Groups of data points that share similar characteristics. For example, in your table, the "Category" column represents clusters (0, 1, 2, etc.).
* Features: The input variables used to determine similarity. In your example, "IQ" and "CGPA" are the features.

#### Example:
In the table provided:

* The algorithm might group students with similar IQ and CGPA values into clusters (e.g., Cluster 0, Cluster 1, etc.).
* This could help identify patterns, such as students with high IQ and CGPA being in one group and those with lower values in another.

| IQ (Input) | CGPA (Input) | Category (4 different clusters based on input cols) |
| ---------- | ------------ | --------------------------------------------------- |
| 100        | 9.5          | 0                                                   |
| 90         | 8.5          | 1                                                   |
| 80         | 7            | 2                                                   |

### 2. Dimensionality Reduction

Dimensionality reduction is a technique in unsupervised learning used to reduce the number of input variables (features) in a dataset while retaining as much relevant information as possible. This is particularly useful when dealing with high-dimensional data(large numbers of features i.e. cols), where too many features can lead to overfitting or computational inefficiency.

Key Concepts:

* Feature Reduction: Simplifies the dataset by reducing the number of features while preserving the relationships between data points.
* Principal Component Analysis (PCA): A common method that transforms the data into a set of linearly uncorrelated variables called principal components.
* t-SNE (t-Distributed Stochastic Neighbor Embedding): A technique used for visualizing high-dimensional data in a lower-dimensional space (e.g., 2D or 3D).
* Dimensionality reduction can also help us to visualize the data. We can reduce the dimensionality of the data to 2 or 3 features and then visualize the data using plots.

#### Example

Suppose we have the following dataset with 3 features (x, y, z) and 4 data points:

| x   | y   | z   |
| --- | --- | --- |
| 1   | 2   | 3   |
| 4   | 5   | 6   |
| 7   | 8   | 9   |
| 10  | 11  | 12  |

Using PCA, we can reduce the dimensionality to 2 features (x', y'):

| x'    | y'    |
| ----- | ----- |
| 1.58  | -0.58 |
| 4.42  | -1.42 |
| 7.26  | -2.26 |
| 10.10 | -3.10 |

This new dataset captures the most variance in the original data, while reducing the number of features from 3 to 2. For more details refer to ()



