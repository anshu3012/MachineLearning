"""k-means from scratch: the five steps as a small class, with the same fit_predict interface as scikit-learn.
Run `python kmeans.py` for a self-check against scikit-learn."""
import numpy as np


class KMeans:
    def __init__(self, n_clusters=2, max_iter=100, random_state=None):
        self.n_clusters = n_clusters      # step 1: k is given to us
        self.max_iter = max_iter          # at most this many assign/move rounds
        self.random_state = random_state  # fixes the random start
        self.centroids = None

    def fit_predict(self, X):
        # Step 2: pick k different rows at random as the starting centroids
        rng = np.random.default_rng(self.random_state)
        random_index = rng.choice(X.shape[0], size=self.n_clusters, replace=False)
        self.centroids = X[random_index].astype(float)

        for i in range(self.max_iter):
            cluster_group = self.assign_clusters(X)                 # step 3
            old_centroids = self.centroids
            self.centroids = self.move_centroids(X, cluster_group)  # step 4
            if np.allclose(old_centroids, self.centroids):          # step 5
                break
        self.n_iter_ = i + 1
        # WCSS of the final clusters (scikit-learn's inertia_)
        self.inertia_ = ((X - self.centroids[cluster_group]) ** 2).sum()
        return cluster_group

    def assign_clusters(self, X):
        cluster_group = []
        for row in X:
            # Euclidean distance from this row to every centroid
            distances = [np.sqrt(np.dot(row - c, row - c)) for c in self.centroids]
            cluster_group.append(int(np.argmin(distances)))  # index of the nearest one
        return np.array(cluster_group)

    def move_centroids(self, X, cluster_group):
        new_centroids = []
        for k in range(self.n_clusters):
            members = X[cluster_group == k]
            # mean of each column; an empty cluster keeps its old centroid
            new_centroids.append(members.mean(axis=0) if len(members) else self.centroids[k])
        return np.array(new_centroids)


if __name__ == "__main__":
    from sklearn.cluster import KMeans as SkKMeans
    from sklearn.datasets import make_blobs
    from sklearn.metrics import adjusted_rand_score

    X, _ = make_blobs(n_samples=300, centers=[(-5, -5), (5, 5), (-2.5, 2.5)], cluster_std=1, random_state=2)
    ours = KMeans(n_clusters=3, random_state=1).fit_predict(X)
    theirs = SkKMeans(n_clusters=3, random_state=0).fit_predict(X)
    assert adjusted_rand_score(ours, theirs) == 1.0, "different clusters from scikit-learn"
    print("self-check passed: same clusters as scikit-learn")
