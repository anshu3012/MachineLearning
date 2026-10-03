"""Heavy part, run once: MNIST, KNN with and without PCA, accuracy by number of components, explained variance.
Writes small CSV files into data/ that the figure scripts read. Run: python compute_results.py (a few minutes)."""
import time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_openml
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

out = Path(__file__).parent / "data"
X, y = fetch_openml("mnist_784", version=1, return_X_y=True, as_frame=False)
idx = np.random.default_rng(0).choice(len(X), 42000, replace=False)     # same size as the Kaggle train.csv
X, y = X[idx], y[idx].astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

def knn(a, b):
    t = time.perf_counter()
    acc = accuracy_score(y_test, KNeighborsClassifier(n_neighbors=5).fit(a, y_train).predict(b))
    return acc, time.perf_counter() - t

rows = [("raw pixels", 784, *knn(X_train, X_test))]
sc = StandardScaler().fit(X_train)
Xs_train, Xs_test = sc.transform(X_train), sc.transform(X_test)
rows.append(("standardised", 784, *knn(Xs_train, Xs_test)))
full = PCA().fit(Xs_train)
pd.DataFrame({"component": np.arange(1, len(full.explained_variance_ratio_) + 1),
              "ratio": full.explained_variance_ratio_}).to_csv(out / "explained_variance.csv", index=False)
for k in [1, 2, 3, 5, 10, 20, 30, 50, 75, 100, 150, 200, 300]:
    p = PCA(n_components=k).fit(Xs_train)
    rows.append((f"PCA {k}", k, *knn(p.transform(Xs_train), p.transform(Xs_test))))
    print(rows[-1], flush=True)
pd.DataFrame(rows, columns=["setup", "columns", "accuracy", "seconds"]).to_csv(out / "knn_results.csv", index=False)
p3 = PCA(n_components=3).fit(Xs_train)
Z = p3.transform(Xs_test)
pd.DataFrame({"PC1": Z[:, 0], "PC2": Z[:, 1], "PC3": Z[:, 2], "label": y_test}).round(3).to_csv(out / "test_pca3.csv", index=False)
print(pd.read_csv(out / "knn_results.csv"))
cum = np.cumsum(full.explained_variance_ratio_)
print("components for 90%:", int(np.searchsorted(cum, 0.90) + 1), " 95%:", int(np.searchsorted(cum, 0.95) + 1),
      " first 3:", full.explained_variance_ratio_[:3].round(4))
