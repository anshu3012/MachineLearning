"""Note ML-087 figures (Plotly): scaling.png - multiplying w and b by a factor moves pi+ and pi- (the margin changes);
constraints.png - y_i (w.x_i + b) for every training point; outlier.png - one outlier makes the hard margin impossible."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.svm import SVC

here = Path(__file__).parent
font = dict(family="Latin Modern Roman", size=18)
GREEN, RED, BLUE, GREY = "#54A24B", "#E45756", "#4C78A8", "#6B6B6B"

# 1. scaling the equation of 2x + 3y + 3 = 0 by k: same line, different pi+ and pi-
w0, b0 = np.array([2.0, 3.0]), 3.0
xs = np.array([-8.0, 8.0])
cases = [(10, "multiply by 10"), (1, "original"), (0.1, "divide by 10")]
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.05,
                    subplot_titles=[f"{t}: d = {2 / np.linalg.norm(k * w0):.3g}" for k, t in cases])
for c, (k, _) in enumerate(cases, start=1):
    w, b = k * w0, k * b0
    for rhs, colour, dash in ((0, "black", "solid"), (1, GREEN, "dash"), (-1, RED, "dash")):
        fig.add_trace(go.Scatter(x=xs, y=(rhs - b - w[0] * xs) / w[1], mode="lines", showlegend=c == 1,
                                 name={0: "wᵀx + b = 0", 1: "wᵀx + b = +1", -1: "wᵀx + b = −1"}[rhs],
                                 line=dict(color=colour, width=4 if rhs == 0 else 3, dash=dash)), 1, c)
    eq = f"{k * 2:g}x + {k * 3:g}y + {k * 3:g}"
    fig.add_annotation(x=-7.6, y=7.2, xanchor="left", text=eq + " = 0, ±1", showarrow=False, font=dict(size=16),
                       bgcolor="rgba(255,255,255,0.9)", row=1, col=c)
fig.update_xaxes(range=[-8, 8], title="x")
fig.update_yaxes(range=[-8, 8])
fig.update_yaxes(title="y", row=1, col=1)
for c in (1, 2, 3):
    fig.update_yaxes(scaleanchor=f"x{'' if c == 1 else c}", row=1, col=c)
fig.update_layout(template="simple_white", width=1000, height=460, font=font, margin=dict(l=60, r=20, t=50, b=100),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.22))
fig.write_image(here / "scaling.png", scale=2); fig.write_image(here / "scaling.pdf")

# 2. the constraint y_i (w.x_i + b) >= 1 on the data of the SVM intuition Note
G = np.array([(2, 6), (3.5, 7.5), (4.5, 6), (6, 7.5), (2.5, 8.5), (5, 9), (7, 9), (7.5, 6.8)])
R = np.array([(1, 1.5), (2.5, 3), (3.5, 1), (5, 2.5), (6.5, 1.5), (7, 3.5), (1.5, 3.8), (4, 3.5)])
X, y = np.r_[G, R], np.r_[np.ones(len(G)), -np.ones(len(R))]
svm = SVC(kernel="linear", C=1e6).fit(X, y)
w, b = svm.coef_[0], svm.intercept_[0]
print("w", w.round(3), "b", round(b, 3), "|w|", round(np.linalg.norm(w), 3), "2/|w|", round(2 / np.linalg.norm(w), 3))
xs = np.array([0, 8.5])


def lines(fig, w, b, **rc):
    for rhs, colour, dash, name in ((0, "black", "solid", "wᵀx + b = 0"), (1, GREEN, "dash", "wᵀx + b = +1"),
                                    (-1, RED, "dash", "wᵀx + b = −1")):
        fig.add_trace(go.Scatter(x=xs, y=(rhs - b - w[0] * xs) / w[1], mode="lines", name=name,
                                 line=dict(color=colour, width=4 if rhs == 0 else 3, dash=dash)), **rc)


def dots(fig, P, colour, **rc):
    fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="markers", showlegend=False,
                             marker=dict(color=colour, size=13, line=dict(color="black", width=1))), **rc)


fig = go.Figure()
lines(fig, w, b)
dots(fig, G, GREEN); dots(fig, R, RED)
vals = y * (X @ w + b)
fig.add_trace(go.Scatter(x=X[:, 0] + 0.22, y=X[:, 1], mode="text", text=[f"{v:.2f}" for v in vals], textposition="middle right",
                         textfont=dict(size=15, color=["black" if abs(v - 1) < 1e-3 else GREY for v in vals]), showlegend=False))
fig.update_layout(template="simple_white", width=580, height=620, font=font, margin=dict(l=60, r=20, t=60, b=110),
                  title=dict(text="Label × (wᵀx + b) for every point: 1 on π+ and π−, above 1 elsewhere", x=0.5, font=dict(size=17)),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.14),
                  xaxis=dict(title="x₁", range=[0, 9.5]), yaxis=dict(title="x₂", range=[0, 10], scaleanchor="x"))
fig.write_image(here / "constraints.png", scale=2); fig.write_image(here / "constraints.pdf")

# 3. one green outlier among the red points: no line can keep every constraint
out = np.array([4.5, 2.0])
fig = go.Figure()
lines(fig, w, b)
dots(fig, G, GREEN); dots(fig, R, RED); dots(fig, out[None], GREEN)
v = 1 * (out @ w + b)
fig.add_trace(go.Scatter(x=[out[0]], y=[out[1]], mode="markers", showlegend=False,
                         marker=dict(size=30, color="rgba(0,0,0,0)", line=dict(color="black", width=2.5))))
fig.add_annotation(x=out[0] + 0.35, y=out[1] - 0.2, ax=7.0, ay=0.2, axref="x", ayref="y", xanchor="left",
                   text=f"green outlier:<br>y(wᵀx + b) = {v:.2f}".replace("-", "−"),
                   font=dict(size=16), bgcolor="rgba(255,255,255,0.9)")
print("outlier value", round(v, 3))
fig.update_layout(template="simple_white", width=580, height=620, font=font, margin=dict(l=60, r=20, t=40, b=110),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.14),
                  xaxis=dict(title="x₁", range=[0, 9.5]), yaxis=dict(title="x₂", range=[-0.5, 10], scaleanchor="x"))
fig.write_image(here / "outlier.png", scale=2); fig.write_image(here / "outlier.pdf")
