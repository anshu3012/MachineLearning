"""Gradient boosting intuition, the worked numbers drawn (Plotly):
full_vs_small.png - five students: the mean plus all of tree 1 (learning rate 1) against one tenth of it (section 8);
new_student.png   - the prediction for a new student built up tree by tree (section 10);
stump_vs_tree.png - the first residuals of the curve data fitted by a stump and by an 8-leaf tree (section 13)."""
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.tree import DecisionTreeRegressor

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import GRID, X as Xc, y as yc  # noqa: E402

FONT = dict(family="Latin Modern Roman", size=20)
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
X = np.array([[90, 8], [100, 7], [110, 6], [120, 9], [80, 5]])
y = np.array([3, 4, 8, 6, 3], dtype=float)
F0 = y.mean()
tree1 = DecisionTreeRegressor(random_state=0).fit(X, y - F0)
pred_full = F0 + tree1.predict(X)
pred_small = F0 + 0.1 * tree1.predict(X)
tree2 = DecisionTreeRegressor(random_state=0).fit(X, y - pred_small)
assert F0 == 4.8 and np.allclose(pred_full, y) and np.allclose(pred_small, [4.62, 4.72, 5.12, 4.92, 4.62])


def save(fig, name):
    fig.write_image(HERE / f"{name}.png", scale=2)
    fig.write_image(HERE / f"{name}.pdf")


# ---- section 8: all of tree 1, or a tenth of it ----
students = [f"student {i}" for i in range(1, 6)]
fig = go.Figure()
fig.add_trace(go.Bar(x=students, y=pred_full, name="4.8 + tree 1 (no learning rate)", marker_color=RED,
                     text=[f"{p:.2f}" for p in pred_full], textposition="outside"))
fig.add_trace(go.Bar(x=students, y=pred_small, name="4.8 + 0.1 × tree 1", marker_color=BLUE,
                     text=[f"{p:.2f}" for p in pred_small], textposition="outside"))
fig.add_trace(go.Scatter(x=students, y=y, mode="markers", name="actual package",
                         marker=dict(symbol="line-ew", size=60, line=dict(color="black", width=4))))
fig.add_hline(y=F0, line=dict(color=GREY, dash="dash", width=2), annotation_text="mean 4.8",
              annotation_position="top left", annotation_font_size=19)
fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, barmode="group",
                  yaxis=dict(title="package (LPA)", range=[0, 9.5]), margin=dict(l=80, r=20, t=90, b=50),
                  legend=dict(orientation="h", x=0, y=1.02, yanchor="bottom", font_size=19))
save(fig, "full_vs_small")

# ---- section 10: a new student, tree by tree ----
new = np.array([[60, 4.9]])
h1, h2 = tree1.predict(new)[0], tree2.predict(new)[0]
total = F0 + 0.1 * h1 + 0.1 * h2
assert np.isclose(h1, -1.8) and np.isclose(h2, -1.62) and np.isclose(total, 4.458)
fig = go.Figure(go.Waterfall(x=["the mean", "0.1 × tree 1", "0.1 × tree 2", "prediction"],
                             measure=["absolute", "relative", "relative", "total"], y=[F0, 0.1 * h1, 0.1 * h2, total],
                             text=["4.8", f"{0.1 * h1:+.2f}", f"{0.1 * h2:+.3f}", f"{total:.3f}"],
                             textposition="outside", textfont=dict(size=22),
                             decreasing=dict(marker_color=RED), totals=dict(marker_color=BLUE),
                             increasing=dict(marker_color=GREY), connector=dict(line=dict(color=GREY, dash="dot"))))
fig.update_layout(template="simple_white", width=1000, height=520, font=FONT, showlegend=False,
                  yaxis=dict(title="package (LPA)", range=[4.3, 4.9]), margin=dict(l=80, r=20, t=30, b=50))
save(fig, "new_student")

# ---- section 13: a stump against an 8-leaf tree, on the first residuals of the curve ----
res = yc - yc.mean()
assert np.isclose(yc.mean(), 0.265, atol=5e-4)                         # the Note, section 11
fits = {n: DecisionTreeRegressor(max_leaf_nodes=n, random_state=42).fit(Xc, res) for n in (2, 8)}
err = {n: float(np.mean((res - t.predict(Xc)) ** 2)) for n, t in fits.items()}
assert err[8] < err[2] / 3
names = {2: "AdaBoost-size stump: 2 leaves", 8: "gradient boosting tree: 8 leaves"}
fig = make_subplots(1, 2, horizontal_spacing=0.06,
                    subplot_titles=[f"{names[n]}<br>error left over {err[n]:.4f}" for n in fits])
for c, (n, t) in enumerate(fits.items(), start=1):
    fig.add_trace(go.Scatter(x=Xc[:, 0], y=res, mode="markers", marker=dict(color=GREY, size=7),
                             name="residuals of the mean", showlegend=c == 1), 1, c)
    fig.add_trace(go.Scatter(x=GRID[:, 0], y=t.predict(GRID), mode="lines", line=dict(color=GREEN, width=4),
                             name="tree fitted to them", showlegend=c == 1), 1, c)
fig.update_xaxes(title_text="x")
fig.update_yaxes(title_text="residual", row=1, col=1)
fig.update_annotations(font_size=21)
fig.update_layout(template="simple_white", width=1200, height=560, font=FONT, margin=dict(l=80, r=20, t=90, b=60),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18))
save(fig, "stump_vs_tree")
print("ok", err)
