"""Gradient boosting classification on the eight students, the worked numbers drawn (Plotly; trees as in the
Notebook: 3 leaves, random_state=0):
sigmoid_points.png - log-odds to probability: F0 = 0.51 -> 0.625, and the stage-2 log-odds of each leaf (section 5);
tree1_regions.png  - tree 1's three leaves as bands of CGPA over the students, with each residual (section 7);
lr_step.png        - stage-2 probabilities with learning rate 1 against 0.1 (section 9.1);
new_student.png    - the log-odds of a new student built up tree by tree, then the sigmoid (section 11)."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.tree import DecisionTreeRegressor

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=20)
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
df = pd.read_csv(HERE.parent / "data" / "placement8.csv")
X, y = df[["cgpa", "iq"]].values, df["placed"].values
sig = lambda z: 1 / (1 + np.exp(-z))
F0 = np.log(y.sum() / (1 - y).sum())
trees, F = [], np.full(len(y), F0)
for _ in range(2):
    p = sig(F)
    r = y - p
    tree = DecisionTreeRegressor(max_leaf_nodes=3, random_state=0).fit(X, r)
    leaf = tree.apply(X)
    gamma = {j: r[leaf == j].sum() / (p[leaf == j] * (1 - p[leaf == j])).sum() for j in np.unique(leaf)}
    trees.append((tree, gamma, leaf, r))
    F = F + np.array([gamma[j] for j in leaf])
t1, g1, leaf1, r1 = trees[0]
F1 = F0 + np.array([g1[j] for j in leaf1])
assert np.isclose(F0, 0.51, atol=0.005) and np.isclose(sig(F0), 0.625)
assert np.allclose(sorted(g1.values()), [-2.67, 0.18, 1.60], atol=0.005)
assert np.allclose(sig(F1), [0.10, 0.10, 0.67, 0.67, 0.67, 0.89, 0.89, 0.89], atol=0.005)


def save(fig, name):
    fig.write_image(HERE / f"{name}.png", scale=2)
    fig.write_image(HERE / f"{name}.pdf")


# ---- section 5: the sigmoid maps log-odds to probability ----
z = np.linspace(-4, 4, 400)
fig = go.Figure(go.Scatter(x=z, y=sig(z), mode="lines", line=dict(color=GREY, width=3), showlegend=False))
pts = [(F0, "F₀ = 0.51 → p = 0.625", BLUE, "bottom right")] + [
    (v, f"{v:+.2f} → p = {sig(v):.2f}", RED if v < 0 else GREEN, "bottom right" if v < 0 else "top left")
    for v in sorted(set(np.round(F1, 4)))]
for v, t, c, pos in pts:
    fig.add_trace(go.Scatter(x=[v, v, -4], y=[0, sig(v), sig(v)], mode="lines", showlegend=False,
                             line=dict(color=c, width=2, dash="dot")))
    fig.add_trace(go.Scatter(x=[v], y=[sig(v)], mode="markers+text", text=[t], textposition=pos, showlegend=False,
                             marker=dict(color=c, size=14), textfont=dict(size=20, color=c)))
fig.add_hline(y=0.5, line=dict(color="black", width=1, dash="dash"))
fig.update_layout(template="simple_white", width=1000, height=560, font=FONT, margin=dict(l=80, r=30, t=20, b=70),
                  xaxis=dict(title="log-odds F", range=[-4, 4]), yaxis=dict(title="probability p = σ(F)", range=[0, 1]))
save(fig, "sigmoid_points")

# ---- section 7: tree 1's leaves as bands of CGPA ----
thr = sorted(t for t, f in zip(t1.tree_.threshold, t1.tree_.feature) if f == 0)
assert np.allclose(thr, [6.8, 7.85]) and set(t1.tree_.feature[t1.tree_.feature >= 0]) == {0}
fig = go.Figure()
edges = [5.2, *thr, 9.2]
for k in range(3):
    fig.add_vrect(x0=edges[k], x1=edges[k + 1], fillcolor=[ORANGE, GREY, BLUE][k], opacity=0.10, line_width=0)
    fig.add_annotation(x=(edges[k] + edges[k + 1]) / 2, y=158, showarrow=False, font=dict(size=20),
                       text=f"leaf {k + 1}")
for t in thr:
    fig.add_vline(x=t, line=dict(color=GREY, dash="dash", width=2))
for cls, col, name in ((0, ORANGE, "not placed: r = −0.625"), (1, BLUE, "placed: r = +0.375")):
    k = y == cls
    fig.add_trace(go.Scatter(x=X[k, 0], y=X[k, 1], mode="markers+text", name=name,
                             marker=dict(color=col, size=18, line=dict(color="white", width=1)),
                             text=[f"{i + 1}" for i in np.where(k)[0]], textposition="top center",
                             textfont=dict(size=18)))
fig.update_layout(template="simple_white", width=1000, height=560, font=FONT, margin=dict(l=80, r=20, t=20, b=60),
                  xaxis=dict(title="CGPA", range=[5.2, 9.2]), yaxis=dict(title="IQ", range=[75, 165]),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.15))
save(fig, "tree1_regions")

# ---- section 9.1: learning rate 1 against 0.1 at stage 2 ----
F_small = F0 + 0.1 * np.array([g1[j] for j in leaf1])
assert np.isclose(F_small[0], 0.24, atol=0.005) and np.isclose(sig(F_small[0]), 0.56, atol=0.005)
students = [f"{i + 1}" for i in range(8)]
fig = go.Figure()
fig.add_trace(go.Scatter(x=students, y=np.full(8, sig(F0)), mode="markers", name="stage 1: 0.625",
                         marker=dict(color=GREY, size=14)))
for vals, name, col, sym in ((sig(F1), "stage 2, learning rate 1", RED, "circle"),
                             (sig(F_small), "stage 2, learning rate 0.1", BLUE, "diamond")):
    fig.add_trace(go.Scatter(x=students, y=vals, mode="markers", name=name, marker=dict(color=col, size=16, symbol=sym)))
for i in range(8):
    fig.add_trace(go.Scatter(x=[students[i]] * 2, y=[sig(F0), sig(F1[i])], mode="lines", showlegend=False,
                             line=dict(color=RED, width=2)))
    fig.add_trace(go.Scatter(x=[students[i], students[i]], y=[y[i], y[i]], mode="markers", showlegend=i == 0,
                             name="true class", marker=dict(symbol="circle-open", size=22, color="black",
                                                            line=dict(width=2))))
fig.add_hline(y=0.5, line=dict(color="black", width=1, dash="dash"))
fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, margin=dict(l=80, r=20, t=90, b=60),
                  xaxis=dict(title="student"), yaxis=dict(title="probability of placement", range=[-0.08, 1.08]),
                  legend=dict(orientation="h", x=0, y=1.02, yanchor="bottom", font_size=19))
save(fig, "lr_step")

# ---- section 11: a new student ----
new = np.array([[7.2, 100]])
t2, g2 = trees[1][0], trees[1][1]
v1, v2 = g1[t1.apply(new)[0]], g2[t2.apply(new)[0]]
Fn = F0 + v1 + v2
assert np.isclose(v1, 0.18, atol=0.005) and np.isclose(v2, 0.82, atol=0.005)
assert np.isclose(Fn, 1.51, atol=0.01) and np.isclose(sig(Fn), 0.82, atol=0.005)
fig = make_subplots(1, 2, column_widths=[0.6, 0.4], horizontal_spacing=0.12,
                    subplot_titles=["log-odds, added up", "then the sigmoid"])
fig.add_trace(go.Waterfall(x=["F₀", "tree 1, leaf 2", "tree 2, leaf A", "total"],
                           measure=["absolute", "relative", "relative", "total"], y=[F0, v1, v2, Fn],
                           text=[f"{F0:.2f}", f"{v1:+.2f}", f"{v2:+.2f}", f"{Fn:.2f}"], textposition="outside",
                           increasing=dict(marker_color=GREEN), totals=dict(marker_color=BLUE),
                           connector=dict(line=dict(color=GREY, dash="dot")), showlegend=False), 1, 1)
fig.add_trace(go.Scatter(x=z, y=sig(z), mode="lines", line=dict(color=GREY, width=3), showlegend=False), 1, 2)
fig.add_trace(go.Scatter(x=[Fn], y=[sig(Fn)], mode="markers+text", text=[f"p = {sig(Fn):.2f}: placed"],
                         textposition="middle left", marker=dict(color=BLUE, size=16), textfont=dict(size=20),
                         showlegend=False), 1, 2)
fig.add_hline(y=0.5, line=dict(color="black", width=1, dash="dash"), row=1, col=2)
fig.update_yaxes(title_text="log-odds", range=[0, 1.9], row=1, col=1)
fig.update_yaxes(title_text="probability", range=[0, 1], row=1, col=2)
fig.update_xaxes(title_text="log-odds F", row=1, col=2)
fig.update_annotations(font_size=21)
fig.update_layout(template="simple_white", width=1200, height=540, font=FONT, margin=dict(l=80, r=20, t=50, b=60))
save(fig, "new_student")
print("ok")
