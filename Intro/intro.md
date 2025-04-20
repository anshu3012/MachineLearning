# Types of ML

| Supervised Learning                        | Unsupervised Learning     | Semi-Supervised Learning          | Reinforcement Learning        |
| ------------------------------------------ | ------------------------- | --------------------------------- | ----------------------------- |
| Labeled data                               | Unlabeled data            | Mix of labeled and unlabeled data | Reward-based learning         |
| Classification (if output is categorical)  | Clustering                | Partially labeled data            | Agent-environment interaction |
| Regression (if output is numerical)        | Dimensionality reduction  |                                   |                               |
|                                            | Anomaly Detection         |                                   |                               |
|                                            | Association Rule Learning |                                   |                               |

## Supervised Learning

Supervised learning is a type of machine learning where the algorithm is trained on labeled data. This means the dataset contains both input features and corresponding output labels, allowing the model to learn the relationship between them. The goal is to predict the output for new, unseen inputs based on this learned relationship.

### Key Characteristics

- **Labeled Data**: The training dataset includes input-output pairs (e.g., IQ and CGPA as inputs, Placement as output in your example).
- **Goal**: To map inputs to outputs accurately.
- **Applications**: Classification (categorical output) and Regression (numerical output).

### Regression Dataset Example: Predicting a numerical value

| IQ (Input) | CGPA (Input) | Placement (Output) |
| ---------- | ------------ | ------------------ |
| 100        | 9.5          | Yes                |
| 90         | 8.5          | Yes                |
| 80         | 7            | No                 |
| 70         | 6.5          | No                 |

### Classification Dataset Example: Predicting a category or class

| IQ (Input) | CGPA (Input) | Package (Output) |
| ---------- | ------------ | ---------------- |
| 100        | 9.5          | 8.5              |
| 90         | 8.5          | 3.5              |
| 80         | 7            | 4.6              |
| 70         | 6.5          | 3.5              |

## Unsupervised Learning

Unsupervised learning is a type of machine learning where the algorithm learns patterns and structures from unlabeled data. Unlike supervised learning, there are no predefined labels or outcomes for the data. The goal is to identify hidden patterns, groupings, or structures within the dataset.

### 1. Clustering

Clustering is a technique in unsupervised learning where the algorithm learns patterns from unlabeled data. The goal of clustering is to group similar data points into clusters based on their features, so that data points within the same cluster are more similar to each other than to those in other clusters.

#### Key Concepts

- **Unsupervised Learning**: Unlike supervised learning, clustering doesn't rely on labeled data. Instead, it identifies inherent structures in the data.
- **Clusters**: Groups of data points that share similar characteristics.
- **Features**: The input variables used to determine similarity. In your example, "IQ" and "CGPA" are the features.

#### Example

In the table provided:

* The algorithm might group students with similar IQ and CGPA values into clusters (e.g., Cluster 0, Cluster 1, etc.).
* This could help identify patterns, such as students with high IQ and CGPA being in one group and those with lower values in another.

| IQ (Input) | CGPA (Input) | Category (4 different clusters based on input columns) |
| ---------- | ------------ | ----------------------------------------------------- |
| 100        | 9.5          | 0                                                     |
| 90         | 8.5          | 1                                                     |
| 80         | 7            | 2                                                     |

### 2. Dimensionality Reduction

Dimensionality reduction is a technique in unsupervised learning used to reduce the number of input variables (features) in a dataset while retaining as much relevant information as possible. This is particularly useful when dealing with high-dimensional data(large numbers of features i.e. cols), where too many features can lead to overfitting or computational inefficiency.

#### Key Concepts

- **Feature Reduction**: Simplifies the dataset by reducing the number of features while preserving the relationships between data points.
- **Principal Component Analysis (PCA)**: A common method that transforms the data into a set of linearly uncorrelated variables called principal components.
- **t-SNE (t-Distributed Stochastic Neighbor Embedding)**: A technique used for visualizing high-dimensional data in a lower-dimensional space (e.g., 2D or 3D).
- Dimensionality reduction can also help us to visualize the data. We can reduce the dimensionality of the data to 2 or 3 features and then visualize the data using plots.

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

This new dataset captures the most variance in the original data while reducing the number of features from 3 to 2.

## Semi-Supervised Learning

Semi-supervised learning is a type of machine learning that falls between supervised and unsupervised learning. It uses a combination of a small amount of labeled data and a large amount of unlabeled data to train the model. This approach is particularly useful when labeling data is expensive or time-consuming, but there is an abundance of unlabeled data available.

### Example: Google Photos

Google Photos uses semi-supervised learning to organize and categorize images. Here's how it works:

1. **Labeled Data**: A small subset of photos is labeled by users (e.g., tagging a person in a photo).
2. **Unlabeled Data**: The majority of photos in the user's library remain unlabeled.
3. **Learning Process**:
    - The algorithm learns from the labeled photos to recognize patterns, such as facial features, locations, or objects.
    - It then applies this knowledge to the unlabeled photos, grouping similar images together or suggesting tags.
4. **Outcome**: Over time, the system improves its accuracy in identifying and categorizing photos, even with minimal user input.

This approach allows Google Photos to provide features like automatic album creation, face recognition, and object detection with minimal manual labeling effort.

## Reinforcement Learning

Reinforcement Learning (RL) is a type of machine learning where an agent learns to make decisions by interacting with an environment. The agent takes actions, observes the outcomes, and receives feedback in the form of rewards or penalties. The goal is to learn a policy that maximizes the cumulative reward over time.

### Key Concepts

- **Agent**: The decision-maker (e.g., a robot, software, or algorithm).
- **Environment**: The system the agent interacts with (e.g., a game, a physical world, or a simulation).
- **State**: The current situation or context of the environment.
- **Action**: The decision or move the agent makes.
- **Reward**: Feedback from the environment indicating the success or failure of an action.
- **Policy**: A strategy that defines the agent's actions based on the current state.
- **Value Function**: Estimates the long-term reward for a state or action.

### How It Works

1. The agent observes the current state of the environment.
2. It selects an action based on its policy.
3. The environment transitions to a new state and provides a reward.
4. The agent updates its policy based on the reward and the new state.

### Example: Chess

- **Agent**: The chess-playing algorithm.
- **Environment**: The chessboard and rules.
- **State**: The current arrangement of pieces.
- **Action**: Moving a piece.
- **Reward**: Winning, losing, or drawing the game.

Reinforcement Learning is particularly useful in scenarios where the optimal solution is not known in advance and must be discovered through trial and error.
