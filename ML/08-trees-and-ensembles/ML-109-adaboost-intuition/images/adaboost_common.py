"""The Note's 10 students and their three AdaBoost stumps, shared by the Plotly figures (no output when run).
Same data and algorithm as boosting_stages.py."""
import numpy as np
from sklearn.tree import DecisionTreeClassifier

BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=18)
CGPA = np.array([2, 3, 1.5, 7, 8.5, 3.5, 6, 8, 8.5, 5.5])
IQ = np.array([120, 90, 78, 125, 120, 55, 90, 70, 100, 62])
Y = np.array([1, 1, 1, 1, 1, -1, -1, -1, -1, -1])
X = np.c_[CGPA, IQ]


def adaboost(rounds=3):
    """Stumps trained on weighted rows; alpha = 1/2 ln((1 - error) / error); w * e^(-alpha y h)."""
    w = np.full(len(Y), 1 / len(Y))
    out = []
    for _ in range(rounds):
        stump = DecisionTreeClassifier(max_depth=1, random_state=0).fit(X, Y, sample_weight=w)
        pred = stump.predict(X)
        err = w[pred != Y].sum()
        alpha = 0.5 * np.log((1 - err) / err)
        out.append(dict(stump=stump, pred=pred, err=err, alpha=alpha))
        w = w * np.exp(-alpha * Y * pred)
        w = w / w.sum()
    return out


STAGES = adaboost()
assert [round(s["alpha"], 2) for s in STAGES] == [0.69, 0.97, 1.28]      # the Note's table


def score(points, upto=3):
    return sum(s["alpha"] * s["stump"].predict(points) for s in STAGES[:upto])
