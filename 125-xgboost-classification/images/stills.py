"""Still figures for the XGBoost classification Note (Plotly):
residuals.png - stage 1 predicts p = 0.6 for every student; the residuals y - p are -0.6 or +0.4;
hessian.png   - the weight p(1 - p) each observation brings to a denominator, against p: 0.24 at p = 0.6;
lambda_compare.png - lambda = 1 shrinks the classification leaves far more than the regression leaves,
                     because their denominators sum p(1-p) are small next to 1."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
x = np.array([5.70, 6.25, 7.10, 8.15, 9.60])
y = np.array([0, 1, 0, 1, 1])
p0 = 0.6
assert np.isclose(1 / (1 + np.exp(-np.log(1.5))), p0)
r = y - p0
assert np.allclose(r, [-0.6, 0.4, -0.6, 0.4, 0.4]) and np.isclose(r.sum(), 0)


def save(fig, name):
    fig.write_image(HERE / f"{name}.png", scale=2)
    fig.write_image(HERE / f"{name}.pdf")


# 1. residuals in probability
fig = go.Figure()
fig.add_trace(go.Scatter(x=[5.3, 10], y=[p0, p0], mode="lines", line=dict(color=GREY, width=3, dash="dash"),
                         name="stage 1: p = 0.6 for everyone"))
for xi, yi, ri in zip(x, y, r):
    c = BLUE if yi else ORANGE
    fig.add_trace(go.Scatter(x=[xi, xi], y=[p0, yi], mode="lines", line=dict(color=c, width=4), showlegend=False))
    fig.add_annotation(x=xi, y=(p0 + yi) / 2, text=f"{ri:+.1f}", showarrow=False, xanchor="left", xshift=10,
                       font=dict(size=24, color=c), bgcolor="white")
for cls, name, c in [(0, "not placed (0)", ORANGE), (1, "placed (1)", BLUE)]:
    m = y == cls
    fig.add_trace(go.Scatter(x=x[m], y=y[m], mode="markers", marker=dict(color=c, size=16), name=name))
fig.update_xaxes(title="CGPA", range=[5.3, 10.0])
fig.update_yaxes(title="placed / probability", range=[-0.1, 1.1], dtick=0.2)
fig.update_layout(template="simple_white", width=1100, height=520, font=FONT, margin=dict(l=80, r=20, t=20, b=70),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.22))
save(fig, "residuals")

# 2. p(1 - p): what each observation adds to the denominator
pg = np.linspace(0, 1, 401)
pts = {"stage 1, every student: p = 0.6": (0.6, GREY), "stage 2, right leaf: p = 0.712": (0.712, BLUE)}
assert np.isclose(0.6 * 0.4, 0.24) and np.isclose(0.518 * 0.482, 0.250, atol=1e-3) and np.isclose(0.712 * 0.288, 0.205, atol=1e-3)
fig = go.Figure(go.Scatter(x=pg, y=pg * (1 - pg), mode="lines", line=dict(color=RED, width=4), name="p(1 - p)"))
fig.add_trace(go.Scatter(x=[0, 1], y=[1, 1], mode="lines", line=dict(color=GREEN, width=4, dash="dash"),
                         name="regression: every observation counts 1"))
for name, (p, c) in pts.items():
    fig.add_trace(go.Scatter(x=[p], y=[p * (1 - p)], mode="markers+text", marker=dict(size=16, color=c),
                             text=[f"{p * (1 - p):.3f}"], textposition="top right", textfont=dict(size=22, color=c),
                             name=name))
fig.add_annotation(x=0.5, y=0.25, text="largest: 0.25 at p = 0.5", showarrow=True, ay=-60, ax=-120,
                   font=dict(size=22, color=RED), arrowcolor=RED)
fig.update_xaxes(title="the observation's previous probability p", range=[0, 1], dtick=0.1)
fig.update_yaxes(title="weight in the denominator", range=[0, 1.08], dtick=0.25)
fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, margin=dict(l=80, r=20, t=20, b=70),
                  legend=dict(x=0.99, xanchor="right", y=0.85, bgcolor="rgba(255,255,255,0.9)"))
save(fig, "hessian")

# 3. lambda = 1 in regression versus classification: the share of each leaf output that survives
reg = {"CGPA < 5.85 (n = 1)": (0.625, 1), "5.85 to 8.25 (n = 2)": (-4.25, 2), "8.25 or more (n = 1)": (3.625, 1)}
cls = {"CGPA < 7.625 (sum p(1-p) = 0.72)": (-0.8, 0.72), "7.625 or more (sum p(1-p) = 0.48)": (0.8, 0.48)}
kept = lambda d: {k: d / (d + 1) for k, (_, d) in d.items()}
assert np.allclose([s / (h + 1) for s, h in cls.values()], [-0.47, 0.54], atol=0.005)
assert np.allclose([s / h for s, h in cls.values()], [-1.11, 1.67], atol=0.005)
fig = make_subplots(1, 2, subplot_titles=["regression leaves", "classification leaves"], horizontal_spacing=0.1)
for col, d, c in [(1, reg, GREEN), (2, cls, BLUE)]:
    names = [k.replace(" (", "<br>(") for k in d]
    share = [h / (h + 1) for _, h in d.values()]
    fig.add_trace(go.Bar(x=names, y=share, marker_color=c, width=0.55, showlegend=False,
                         text=[f"{s:.0%}" for s in share], textposition="outside", textfont=dict(size=24)), 1, col)
fig.add_hline(y=1, line=dict(color=GREY, width=2, dash="dot"))
fig.update_yaxes(range=[0, 1.1], tickformat=".0%", title_text="output kept when lambda = 1", col=1)
fig.update_yaxes(range=[0, 1.1], tickformat=".0%", col=2)
fig.update_xaxes(tickfont=dict(size=17))
fig.update_annotations(font=dict(family="Latin Modern Roman", size=24))
fig.update_layout(template="simple_white", width=1200, height=560, font=FONT, margin=dict(l=90, r=20, t=50, b=40))
save(fig, "lambda_compare")
