"""More Plotly figures for the XGBoost maths Note, all on the four students of the XGBoost regression Note
(residuals -2.875, 3.625, -1.375, 0.625 from the mean 7.375):
additive.png  - the model is a sum of functions: the constant f1, the tree f2, and their sum, a staircase;
objective.png - loss + gamma*T + lambda/2 * sum w^2 for trees with 1, 2 and 3 leaves (gamma = lambda = 1);
parabolas.png - each leaf's own parabola G w + (H + lambda) w^2 / 2 and its minimum w* = -G / (H + lambda);
structure.png - the best objective -1/2 sum G^2 / (H + lambda) of each candidate root split (lower is better)."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
BLUE, RED, GREEN, GREY, PURPLE, ORANGE = "#4C78A8", "#E45756", "#54A24B", "#6B6B6B", "#B279A2", "#F58518"
cgpa = np.array([6.7, 9.0, 7.5, 5.0])
y = np.array([4.5, 11.0, 6.0, 8.0])
f1 = y.mean()
r = y - f1
g = -r                                                     # squared error: g = -r, h = 1
assert np.isclose(f1, 7.375) and np.allclose(r, [-2.875, 3.625, -1.375, 0.625])


def save(fig, name):
    fig.write_image(HERE / f"{name}.png", scale=2)
    fig.write_image(HERE / f"{name}.pdf")


# 1. a sum of functions
tree = lambda v: np.where(v < 5.85, 0.625, np.where(v < 8.25, -2.125, 3.625))
grid = np.linspace(4.6, 9.4, 800)
fig = make_subplots(1, 3, subplot_titles=["f1(x) = 7.375", "f2(x): the first tree", "f1(x) + f2(x)"],
                    horizontal_spacing=0.07)
for col, curve in [(1, np.full_like(grid, f1)), (2, tree(grid)), (3, f1 + tree(grid))]:
    fig.add_trace(go.Scatter(x=grid, y=curve, mode="lines", line=dict(color=[BLUE, ORANGE, RED][col - 1], width=4,
                             shape="hv"), showlegend=False), 1, col)
fig.add_trace(go.Scatter(x=cgpa, y=y, mode="markers", marker=dict(color="black", size=12), name="students"), 1, 3)
fig.add_trace(go.Scatter(x=cgpa, y=r, mode="markers", marker=dict(color=GREY, size=12, symbol="diamond"),
                         name="residuals (what f2 aims at)"), 1, 2)
fig.update_xaxes(title_text="CGPA", range=[4.6, 9.4])
fig.update_yaxes(range=[3.5, 12], row=1, col=1, title_text="output")
fig.update_yaxes(range=[-3.5, 4.5], row=1, col=2)
fig.update_yaxes(range=[3.5, 12], row=1, col=3)
fig.update_annotations(font=dict(family="Latin Modern Roman", size=24))
fig.update_layout(template="simple_white", width=1400, height=520, font=FONT, margin=dict(l=80, r=20, t=50, b=70),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.25))
save(fig, "additive")

# 2. the objective for trees of growing size, gamma = lambda = 1, leaf outputs = the residual means (lambda = 0)
GAMMA = LAM = 1
trees = {"1 leaf<br>(no split)": [np.ones(4, bool)],
         "2 leaves<br>(CGPA < 8.25)": [cgpa < 8.25, cgpa >= 8.25],
         "3 leaves<br>(the first tree)": [cgpa < 5.85, (cgpa >= 5.85) & (cgpa < 8.25), cgpa >= 8.25]}
rows = {}
for name, leaves in trees.items():
    w = [r[m].mean() for m in leaves]
    loss = sum(0.5 * ((r[m] - wj) ** 2).sum() for m, wj in zip(leaves, w))
    rows[name] = (loss, GAMMA * len(leaves), 0.5 * LAM * sum(wj ** 2 for wj in w))
loss3, gT3, l3 = rows["3 leaves<br>(the first tree)"]
assert np.isclose(gT3 + l3, 12.02, atol=0.005)
totals = {k: sum(v) for k, v in rows.items()}
print("objective:", {k.split("<")[0]: round(v, 2) for k, v in totals.items()})
fig = go.Figure()
for i, (part, c) in enumerate([("loss", BLUE), ("gamma x T", ORANGE), ("lambda/2 x sum of w squared", GREEN)]):
    fig.add_trace(go.Bar(x=list(rows), y=[v[i] for v in rows.values()], name=part, marker_color=c,
                         text=[f"{v[i]:.4f}" if v[i] > 0.8 else "" for v in rows.values()], textposition="inside",
                         textfont=dict(size=22)))
fig.add_annotation(x=list(rows)[2], y=loss3 / 2, text=f"{loss3:.4f}", showarrow=False, font=dict(size=19, color="white"))
for k, v in totals.items():
    fig.add_annotation(x=k, y=v, text=f"<b>{v:.4f}</b>", showarrow=False, yshift=18, font=dict(size=24))
fig.update_layout(barmode="stack", template="simple_white", width=1100, height=560, font=FONT,
                  yaxis=dict(title="objective", range=[0, 14]), margin=dict(l=80, r=20, t=20, b=60),
                  uniformtext=dict(minsize=20, mode="show"),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2, traceorder="normal"))
save(fig, "objective")

# 3. one parabola per leaf
leaves = {"leaf CGPA < 5.85": (cgpa < 5.85, GREEN), "leaf 5.85 to 8.25": ((cgpa >= 5.85) & (cgpa < 8.25), BLUE),
          "leaf CGPA ≥ 8.25": (cgpa >= 8.25, ORANGE)}
wg = np.linspace(-4.5, 4.5, 600)
fig = go.Figure()
wstar = {}
for name, (m, c) in leaves.items():
    G, H = g[m].sum(), m.sum()
    for lam, dash in [(0, None), (1, "dot")]:
        ws = -G / (H + lam)
        wstar[(name, lam)] = ws
        fig.add_trace(go.Scatter(x=wg, y=G * wg + 0.5 * (H + lam) * wg ** 2, mode="lines",
                                 line=dict(color=c, width=4 if lam == 0 else 3, dash=dash),
                                 name=f"{name}: G = {G:g}, H = {H}" if lam == 0 else None, showlegend=lam == 0))
        fig.add_trace(go.Scatter(x=[ws], y=[-0.5 * G ** 2 / (H + lam)], mode="markers+text" if lam == 0 else "markers",
                                 marker=dict(size=15 if lam == 0 else 11, color=c, symbol="star" if lam == 0 else "circle"),
                                 text=[f"w* = {ws:g}"], textposition="bottom center", textfont=dict(size=21, color=c),
                                 showlegend=False))
assert np.allclose([wstar[(n, 0)] for n in leaves], [0.625, -2.125, 3.625])
assert np.isclose(wstar[("leaf 5.85 to 8.25", 1)], -1.4167, atol=1e-4)
fig.add_hline(y=0, line=dict(color="black", width=1))
for label, dash in [("solid: lambda = 0 (star = minimum)", None), ("dotted: lambda = 1", "dot")]:
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", line=dict(color=GREY, width=3, dash=dash), name=label))
fig.update_xaxes(title="leaf output w", range=[-4.5, 4.5], dtick=1)
fig.update_yaxes(title="the leaf's part of the objective", range=[-8, 13])
fig.update_layout(template="simple_white", width=1100, height=620, font=FONT, margin=dict(l=90, r=20, t=20, b=70),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18, font=dict(size=20)))
save(fig, "parabolas")

# 4. structure score of each candidate root split (lambda = gamma = 0)
S = lambda m: g[m].sum() ** 2 / m.sum()
score = {"no split": abs(-0.5 * S(np.ones(4, bool)))}           # 0: the residuals sum to 0
for t in (5.85, 7.1, 8.25):
    score[f"CGPA < {t:g}"] = -0.5 * (S(cgpa < t) + S(cgpa >= t))
assert np.isclose(score["CGPA < 8.25"], -8.76, atol=0.005)
best = min(score, key=score.get)
fig = go.Figure(go.Bar(x=list(score), y=list(score.values()), width=0.6,
                       marker_color=[GREEN if k == best else GREY for k in score],
                       text=[f"{v:.2f}" for v in score.values()], textposition="outside", textfont=dict(size=24)))
fig.add_hline(y=0, line=dict(color="black", width=1))
fig.update_yaxes(title="best objective (lower is better)", range=[-10.5, 1])
fig.update_layout(template="simple_white", width=1000, height=520, font=FONT, margin=dict(l=90, r=20, t=20, b=60))
save(fig, "structure")
