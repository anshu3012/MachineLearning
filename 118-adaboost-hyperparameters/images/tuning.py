"""AdaBoost hyperparameters, two more pictures (Plotly):
weights.png - the observation weights after 50 stages, learning_rate 1.0 against 0.1 (marker area = weight);
              the weights are replayed from scikit-learn's own stumps and alphas (SAMME), section 4.2;
grid.png    - the 10-fold cross-validated accuracy of every pair in the grid search, section 5."""
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import GridSearchCV

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import COLOURS, X, X_train, y, y_train  # noqa: E402

FONT = dict(family="Latin Modern Roman", size=20)


def save(fig, name):
    fig.write_image(HERE / f"{name}.png", scale=2)
    fig.write_image(HERE / f"{name}.pdf")


# ---- weights after 50 stages ----
STAGES = 50
fig = make_subplots(1, 2, horizontal_spacing=0.04)
titles, largest = [], {}
for c, lr in enumerate((1.0, 0.1), start=1):
    m = AdaBoostClassifier(n_estimators=STAGES, learning_rate=lr, random_state=42).fit(X_train, y_train)
    w = np.full(len(y_train), 1 / len(y_train))
    for stump, alpha in zip(m.estimators_, m.estimator_weights_):
        wrong = stump.predict(X_train) != y_train
        err = w[wrong].sum()
        assert np.isclose(alpha, lr * np.log((1 - err) / err))   # SAMME alpha, two classes
        w = w * np.exp(alpha * wrong)
        w = w / w.sum()
    largest[lr] = w.max() * len(w)
    titles.append(f"learning_rate {lr}: largest weight {largest[lr]:.1f} × the start")
    for cls in (0, 1):
        k = y_train == cls
        fig.add_trace(go.Scatter(x=X_train[k, 0], y=X_train[k, 1], mode="markers", name=f"class {cls}",
                                 showlegend=c == 1, marker=dict(color=COLOURS[cls], size=4 + 9 * np.sqrt(w[k] * len(w)),
                                                                opacity=0.75, line=dict(color="white", width=0.5))),
                      1, c)
first = {lr: AdaBoostClassifier(n_estimators=1, learning_rate=lr, random_state=42).fit(X_train, y_train).estimator_weights_[0]
         for lr in (1.0, 0.1)}
assert np.allclose([first[1.0], first[0.1]], [0.5322, 0.0532], atol=1e-4)    # the Note, section 4.1
assert largest[1.0] > 2 * largest[0.1]
print("largest weight / start:", {k: round(v, 2) for k, v in largest.items()})
for i, t in enumerate(titles):
    fig.layout.annotations += (go.layout.Annotation(text=t, x=[0.24, 0.76][i], y=1.0, xref="paper", yref="paper",
                                                    xanchor="center", yanchor="bottom", showarrow=False,
                                                    font=dict(size=21)),)
fig.update_xaxes(showticklabels=False)
fig.update_yaxes(showticklabels=False, scaleanchor="x")
fig.update_layout(template="simple_white", width=1300, height=680, font=FONT, margin=dict(l=10, r=10, t=50, b=50),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.02, yanchor="top", itemsizing="constant"))
save(fig, "weights")

# ---- the grid search ----
grid = {"n_estimators": [10, 50, 100, 500], "learning_rate": [0.0001, 0.001, 0.01, 0.1, 1.0]}
gs = GridSearchCV(AdaBoostClassifier(random_state=42), param_grid=grid, n_jobs=-1, cv=10, scoring="accuracy").fit(X, y)
assert gs.best_params_ == {"learning_rate": 0.1, "n_estimators": 500} and f"{gs.best_score_:.3f}" == "0.832"
res = gs.cv_results_
Z = np.zeros((len(grid["learning_rate"]), len(grid["n_estimators"])))
for p, s in zip(res["params"], res["mean_test_score"]):
    Z[grid["learning_rate"].index(p["learning_rate"]), grid["n_estimators"].index(p["n_estimators"])] = s
assert f"{Z[-1, 1]:.3f}" == "0.812"                                       # the defaults: 50 stumps, rate 1.0
assert np.all(np.abs(Z[:2] - 0.57) < 0.02) and f"{Z[-1, 1]:.3f}" == "0.812"           # rates 0.001 and below: about 0.57
fig = go.Figure(go.Heatmap(z=Z, x=list(range(4)), y=list(range(5)),
                           colorscale="Blues", colorbar=dict(title="accuracy")))
for (r, c), v in np.ndenumerate(Z):
    fig.add_annotation(x=c, y=r, text=f"{v:.3f}", showarrow=False, font=dict(size=24, color="white" if v > 0.7 else "black"))
best = (grid["n_estimators"].index(gs.best_params_["n_estimators"]), grid["learning_rate"].index(gs.best_params_["learning_rate"]))
fig.add_shape(type="rect", x0=best[0] - 0.5, x1=best[0] + 0.5, y0=best[1] - 0.5, y1=best[1] + 0.5, line=dict(color="#E45756", width=5))
fig.add_annotation(x=best[0], y=best[1], text="best", yshift=-32, showarrow=False, font=dict(color="white", size=20))
fig.add_annotation(x=1, y=4, text="default", yshift=-32, showarrow=False, font=dict(color="white", size=20))
fig.update_xaxes(title="n_estimators", tickvals=list(range(4)), ticktext=[str(n) for n in grid["n_estimators"]])
fig.update_yaxes(title="learning_rate", tickvals=list(range(5)), ticktext=[str(l) for l in grid["learning_rate"]])
fig.update_layout(template="simple_white", width=1000, height=640, font=FONT, margin=dict(l=90, r=20, t=20, b=70))
save(fig, "grid")
print("ok")
