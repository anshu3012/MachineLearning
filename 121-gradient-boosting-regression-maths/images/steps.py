"""Gradient boosting maths on the three startups, steps 2(a), 2(c) and 2(d) drawn (Plotly):
gradients.png   - each startup's loss against its prediction; the slope at F0 = 142.41 is minus the pseudo-residual;
leaf_values.png - region R11 (startup 3): the best leaf value for squared error (= the tree's mean) and for
                  absolute error (the tree's mean of signs, -1, is replaced by -53.55);
update.png      - the predictions after one tree, learning rate 1 and 0.1."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import GradientBoostingRegressor

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=20)
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
d = pd.read_csv(HERE.parent / "data" / "startups3.csv")
X, y = d[["rd", "admin", "marketing"]].to_numpy(), d.profit.to_numpy()
F0 = y.mean()
r = y - F0
assert np.allclose(r, [49.85, 1.85, -51.70], atol=0.005)


def save(fig, name):
    fig.write_image(HERE / f"{name}.png", scale=2)
    fig.write_image(HERE / f"{name}.pdf")


# ---- 2(a): pseudo-residual = minus the slope of the loss at the current prediction ----
fig = make_subplots(1, 3, horizontal_spacing=0.06, subplot_titles=[
    f"startup {i + 1}: y = {y[i]:.2f}<br>slope {-r[i]:+.2f}, so r = {r[i]:+.2f}" for i in range(3)])
F = np.linspace(60, 220, 300)
for i in range(3):
    slope = -(y[i] - F0)                                  # dL/dF for L = 1/2 (y - F)^2
    num = (0.5 * (y[i] - (F0 + 1e-4)) ** 2 - 0.5 * (y[i] - (F0 - 1e-4)) ** 2) / 2e-4
    assert np.isclose(num, slope, atol=1e-4)
    L0 = 0.5 * (y[i] - F0) ** 2
    fig.add_trace(go.Scatter(x=F, y=0.5 * (y[i] - F) ** 2, mode="lines", line=dict(color=GREY, width=3),
                             name="loss ½ (y − F)²", showlegend=i == 0), 1, i + 1)
    T = np.linspace(F0 - 30, F0 + 30, 2)
    fig.add_trace(go.Scatter(x=T, y=L0 + slope * (T - F0), mode="lines", line=dict(color=RED, width=4),
                             name="slope at F₀ = 142.41", showlegend=i == 0), 1, i + 1)
    fig.add_trace(go.Scatter(x=[F0], y=[L0], mode="markers", marker=dict(color="black", size=13), showlegend=False),
                  1, i + 1)
    if abs(r[i]) > 5:                                      # arrow: the downhill direction, minus the slope
        fig.add_annotation(x=F0 + np.sign(r[i]) * 45, y=L0, ax=F0, ay=L0, axref=f"x{i + 1 if i else ''}",
                           ayref=f"y{i + 1 if i else ''}", xref=f"x{i + 1 if i else ''}", yref=f"y{i + 1 if i else ''}",
                           showarrow=True, arrowhead=2, arrowwidth=3, arrowcolor=GREEN, text="")
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", line=dict(color=GREEN, width=3),
                             name="downhill: the way r points", showlegend=i == 0), 1, i + 1)
fig.update_xaxes(title_text="prediction F", range=[60, 220])
fig.update_yaxes(range=[-300, 4000])
fig.update_annotations(font_size=20)
fig.update_layout(template="simple_white", width=1400, height=560, font=FONT, margin=dict(l=60, r=20, t=90, b=60),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2))
save(fig, "gradients")

# ---- 2(c): best leaf value in region R11 (startup 3), squared against absolute error ----
g = np.linspace(-80, 20, 1001)
F0_abs = np.median(y)
assert np.isclose(F0_abs, 144.26)
# (leaf loss, the tree's own leaf value = mean of the pseudo-residuals in the leaf, best value = argmin of the loss)
cases = {"squared error": (lambda gg: 0.5 * (y[2] - F0 - gg) ** 2, r[2], r[2]),
         "absolute error": (lambda gg: np.abs(y[2] - F0_abs - gg), np.sign(y[2] - F0_abs), y[2] - F0_abs)}
fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=[
    f"{k}<br>tree says {v[1]:.2f}, best γ = {v[2]:.2f}" for k, v in cases.items()])
for c, (k, (f, tree_val, best_val)) in enumerate(cases.items(), start=1):
    assert abs(g[np.argmin(f(g))] - best_val) < 0.1
    fig.add_trace(go.Scatter(x=g, y=f(g), mode="lines", line=dict(color=GREY, width=3), showlegend=False), 1, c)
    fig.add_trace(go.Scatter(x=[best_val], y=[f(best_val)], mode="markers", marker=dict(color=GREEN, size=16),
                             name="best leaf value (step 2(c))", showlegend=c == 1), 1, c)
    fig.add_trace(go.Scatter(x=[tree_val], y=[f(tree_val)], mode="markers",
                             marker=dict(color=RED, size=16, symbol="x"), name="the tree's own leaf value",
                             showlegend=c == 1), 1, c)
assert np.isclose(cases["absolute error"][2], -53.55) and cases["absolute error"][1] == -1
fig.update_xaxes(title_text="leaf value γ for startup 3")
fig.update_yaxes(title_text="loss in the leaf", row=1, col=1)
fig.update_annotations(font_size=21)
fig.update_layout(template="simple_white", width=1200, height=560, font=FONT, margin=dict(l=80, r=20, t=90, b=60),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2))
save(fig, "leaf_values")

# ---- 2(d): the update, learning rate 1 and 0.1 ----
preds = {}
for lr in (1.0, 0.1):
    gbr = GradientBoostingRegressor(n_estimators=1, max_depth=1, learning_rate=lr).fit(X, y)
    preds[lr] = gbr.predict(X)
assert np.allclose(preds[1.0], [168.26, 168.26, 90.71], atol=0.005)
assert np.allclose(preds[0.1], [144.995, 144.995, 137.24], atol=0.005)
names = ["startup 1", "startup 2", "startup 3"]
fig = go.Figure()
for name, vals, col in (("F₀ = 142.41 (the mean)", np.full(3, F0), "#BDBDBD"), ("F₁, learning rate 1", preds[1.0], RED),
                        ("F₁, learning rate 0.1", preds[0.1], BLUE)):
    fig.add_trace(go.Bar(x=names, y=vals, name=name, marker_color=col, text=[f"{v:.3f}".rstrip("0") for v in vals],
                         textposition="outside", textfont=dict(size=18)))
fig.add_trace(go.Scatter(x=names, y=y, mode="markers", name="actual profit",
                         marker=dict(symbol="line-ew", size=70, line=dict(color="black", width=4))))
fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, barmode="group",
                  yaxis=dict(title="profit (thousands)", range=[0, 215]), margin=dict(l=80, r=20, t=90, b=50),
                  legend=dict(orientation="h", x=0, y=1.02, yanchor="bottom", font_size=19))
save(fig, "update")
print("ok")
