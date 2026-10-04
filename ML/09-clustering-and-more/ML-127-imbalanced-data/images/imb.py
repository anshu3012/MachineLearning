"""Shared data and resamplers for the figures of this Note (the Notebook builds the same steps one by one)."""
import numpy as np
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

BLUE, RED, ORANGE, GREY = "#4C78A8", "#E45756", "#F58518", "#6B6B6B"   # majority, minority, synthetic, neutral
FONT = dict(family="Latin Modern Roman", size=17)


def data():
    """400 rows, 2 inputs, about 7% in class 0 (the minority); 80/20 split -> 299 + 21 training rows."""
    X, y = make_classification(n_samples=400, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=2,
                               weights=[0.07], class_sep=0.8, flip_y=0, random_state=59)
    return train_test_split(X, y, test_size=0.2, random_state=42)


def undersample(X, y):
    return RandomUnderSampler(random_state=42).fit_resample(X, y)


def oversample(X, y):
    return RandomOverSampler(random_state=42).fit_resample(X, y)


def smote(X, y):
    """imblearn returns the original rows first, then the synthetic ones."""
    Xs, ys = SMOTE(k_neighbors=5, random_state=42).fit_resample(X, y)
    return Xs, ys, Xs[len(X):]


if __name__ == "__main__":
    Xtr, Xte, ytr, yte = data()
    assert ((ytr == 0).sum(), (ytr == 1).sum()) == (21, 299)
    assert np.bincount(undersample(Xtr, ytr)[1]).tolist() == [21, 21]
    assert np.bincount(oversample(Xtr, ytr)[1]).tolist() == [299, 299]
    Xs, ys, new = smote(Xtr, ytr)
    assert np.bincount(ys).tolist() == [299, 299] and len(new) == 278 and np.allclose(Xs[:len(Xtr)], Xtr)
