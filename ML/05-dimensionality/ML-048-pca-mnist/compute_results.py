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
# main run: PCA on the raw pixels (PCA centres them itself; all pixels share one unit, 0-255)
full = PCA().fit(X_train)
pd.DataFrame({"component": np.arange(1, len(full.explained_variance_ratio_) + 1),
              "ratio": full.explained_variance_ratio_}).to_csv(out / "explained_variance.csv", index=False)
for k in [1, 2, 3, 5, 10, 20, 30, 50, 75, 100, 150, 200, 300]:
    p = PCA(n_components=k).fit(X_train)
    rows.append((f"PCA {k}", k, *knn(p.transform(X_train), p.transform(X_test))))
    print(rows[-1], flush=True)
# comparison for the Extra: standardise every pixel first
sc = StandardScaler().fit(X_train)
Xs_train, Xs_test = sc.transform(X_train), sc.transform(X_test)
rows.append(("standardised", 784, *knn(Xs_train, Xs_test)))
for k in [50, 100]:
    p = PCA(n_components=k).fit(Xs_train)
    rows.append((f"std PCA {k}", k, *knn(p.transform(Xs_train), p.transform(Xs_test))))
pd.DataFrame(rows, columns=["setup", "columns", "accuracy", "seconds"]).to_csv(out / "knn_results.csv", index=False)
p3 = PCA(n_components=3).fit(X_train)
Z = p3.transform(X_test)
print("first 3 eigenvalues:", p3.explained_variance_.round(1), "sum all:", full.explained_variance_.sum().round(1))
print("PC1 vs ink:", np.corrcoef(Z[:, 0], (X_test > 0).sum(axis=1))[0, 1].round(2))
pd.DataFrame({"PC1": Z[:, 0], "PC2": Z[:, 1], "PC3": Z[:, 2], "label": y_test}).round(3).to_csv(out / "test_pca3.csv", index=False)
print(pd.read_csv(out / "knn_results.csv"))
cum = np.cumsum(full.explained_variance_ratio_)
print("components for 90%:", int(np.searchsorted(cum, 0.90) + 1), " 95%:", int(np.searchsorted(cum, 0.95) + 1),
      " first 3:", full.explained_variance_ratio_[:3].round(4))
