"""AdaBoost hyperparameters on the circles data (Plotly):
surfaces.png  - decision surfaces for n_estimators 1 to 1500, and 1500 with learning_rate 0.1 (the app's code);
staged.png    - training and test accuracy after each added stump, for three learning rates."""
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import X_test, X_train, figure, fit, y_test, y_train  # noqa: E402

from sklearn.ensemble import AdaBoostClassifier  # noqa: E402

FONT = dict(family="Latin Modern Roman", size=19)
panels = []
for n, lr in [(1, 1.0), (50, 1.0), (150, 1.0), (500, 1.0), (1500, 1.0), (1500, 0.1)]:
    model, acc = fit(n, lr)
    panels.append((f"n_estimators={n}, learning_rate={lr}<br>{acc}", model))
    print(panels[-1][0])
fig = figure(panels, cols=3)
fig.update_annotations(font_size=19)
fig.update_layout(width=1500, height=1000, font=FONT, margin=dict(t=90), legend=dict(font_size=20))
fig.write_image(HERE / "surfaces.png", scale=2)
fig.write_image(HERE / "surfaces.pdf")

fig = go.Figure()
colours = {1.0: "#E45756", 0.1: "#4C78A8", 0.01: "#54A24B"}
n = np.arange(1, 1501)
for lr, c in colours.items():
    m = AdaBoostClassifier(n_estimators=1500, learning_rate=lr, random_state=42).fit(X_train, y_train)
    tr = list(m.staged_score(X_train, y_train))
    te = list(m.staged_score(X_test, y_test))
    k = len(te)
    fig.add_trace(go.Scatter(x=n[:k], y=te, name=f"learning_rate={lr}: test", line=dict(color=c, width=3)))
    fig.add_trace(go.Scatter(x=n[:k], y=tr, name=f"learning_rate={lr}: train", line=dict(color=c, width=2, dash="dot")))
    print(lr, "stumps", k, "best test", max(te), "at", int(np.argmax(te)) + 1, "final train/test", tr[-1], te[-1])
fig.update_xaxes(title="n_estimators (stumps added so far)", type="log")
fig.update_yaxes(title="accuracy", range=[0.5, 0.92])
fig.update_layout(template="simple_white", width=1100, height=700, font=FONT, margin=dict(l=70, r=20, t=20, b=70),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18, yanchor="top", font_size=17))
fig.write_image(HERE / "staged.png", scale=2)
fig.write_image(HERE / "staged.pdf")
