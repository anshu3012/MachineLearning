"""Training and test accuracy against the number of base models, for bagging (fully grown trees) and AdaBoost
(stumps), on the noisy concentric circles of the Notebook. Averaged over 20 fresh draws of the data (350 training,
150 test points each). Bagging starts near 0.9 on the training data (low bias) and its test accuracy rises as the
variance averages away; AdaBoost starts near 0.6 on both (high bias) and both rise as the bias falls. Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_circles
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=20)
GREY, RED = "#6B6B6B", "#E45756"
N, DRAWS = 100, 20


def curves():
    """Mean accuracy after 1..N models: dict[(method, split)] -> array of length N."""
    out = {(m, s): np.zeros(N) for m in ("bagging", "boosting") for s in ("train", "test")}
    for seed in range(DRAWS):
        X, y = make_circles(n_samples=500, factor=0.1, noise=0.35, random_state=seed)
        Xa, Xb, ya, yb = train_test_split(X, y, test_size=150, random_state=seed)
        bag = BaggingClassifier(DecisionTreeClassifier(random_state=seed), n_estimators=N, random_state=seed).fit(Xa, ya)
        ada = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), n_estimators=N, random_state=seed).fit(Xa, ya)
        for split, XX, yy in (("train", Xa, ya), ("test", Xb, yb)):
            votes = np.cumsum([t.predict(XX) for t in bag.estimators_], axis=0) / np.arange(1, N + 1)[:, None]
            out["bagging", split] += ((votes > 0.5) == yy).mean(axis=1) / DRAWS
            out["boosting", split] += np.array([(p == yy).mean() for p in ada.staged_predict(XX)]) / DRAWS
    return out


if __name__ == "__main__":
    C = curves()
    r = {k: (round(v[0], 2), round(v[-1], 2)) for k, v in C.items()}
    print(r)
    assert r["bagging", "train"][0] > 0.85 and r["boosting", "train"][0] < 0.65          # low bias against high bias
    assert r["bagging", "test"][1] > r["bagging", "test"][0] and r["boosting", "test"][1] > r["boosting", "test"][0]
    fig = make_subplots(1, 2, shared_yaxes=True, horizontal_spacing=0.06,
                        subplot_titles=["bagging: fully grown trees", "boosting: AdaBoost with stumps"])
    fig.update_annotations(font_size=22)
    n = np.arange(1, N + 1)
    for col, m in enumerate(("bagging", "boosting"), 1):
        for split, colr in (("train", GREY), ("test", RED)):
            fig.add_trace(go.Scatter(x=n, y=C[m, split], mode="lines", name=f"{split}ing accuracy" if split == "train" else "test accuracy",
                                     line=dict(color=colr, width=4), showlegend=col == 1), 1, col)
        fig.update_xaxes(title="number of base models", row=1, col=col)
    fig.update_yaxes(title="accuracy (mean of 20 draws)", range=[0.55, 1.02], row=1, col=1)
    fig.update_yaxes(range=[0.55, 1.02], row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=480, font=FONT,
                      legend=dict(x=0.99, xanchor="right", y=0.08), margin=dict(l=80, r=20, t=60, b=70))
    fig.write_image(here / "error_curves.png", scale=2)
    fig.write_image(here / "error_curves.pdf")
