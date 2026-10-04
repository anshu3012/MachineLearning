"""One-input Lasso vs Ridge with toy sums S = sum((x - x_bar)(y - y_bar)) = 100 and D = sum((x - x_bar)^2) = 50 (Plotly).
Figure 1: slope against lambda. Figure 2: slope against S for lambda = 100 (the dead zone)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
S, D = 100.0, 50.0
font = dict(family="Latin Modern Roman", size=16)


def lasso(s, lam):
    return np.where(s > lam, (s - lam) / D, np.where(s < -lam, (s + lam) / D, 0.0))


lam = np.linspace(0, 200, 401)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=("Lasso: m = (S − λ) / D, stops at 0", "Ridge: m = S / (D + λ), never 0"))
fig.add_trace(go.Scatter(x=lam[lam >= 100], y=(S - lam[lam >= 100]) / D, mode="lines",
                         line=dict(color="#BBBBBB", width=3, dash="dash"), name="m > 0 formula: gives m < 0, not allowed"), 1, 1)
fig.add_trace(go.Scatter(x=lam[lam >= 100], y=(S + lam[lam >= 100]) / D, mode="lines",
                         line=dict(color="#BBBBBB", width=3, dash="dot"), name="m < 0 formula: gives m > 0, not allowed"), 1, 1)
fig.add_trace(go.Scatter(x=lam, y=lasso(S, lam), mode="lines", line=dict(color="#E45756", width=5), name="Lasso slope"), 1, 1)
pts = [0, 25, 50, 100, 150]
fig.add_trace(go.Scatter(x=pts, y=lasso(S, np.array(pts, float)), mode="markers+text", marker=dict(size=11, color="#E45756"),
                         text=[f"{v:g}" for v in lasso(S, np.array(pts, float))], textposition="top right",
                         textfont=dict(color="#E45756"), showlegend=False), 1, 1)
fig.add_trace(go.Scatter(x=lam, y=S / (D + lam), mode="lines", line=dict(color="#4C78A8", width=5), name="Ridge slope"), 1, 2)
fig.add_trace(go.Scatter(x=pts, y=S / (D + np.array(pts, float)), mode="markers+text", marker=dict(size=11, color="#4C78A8"),
                         text=[f"{v:.2g}" for v in S / (D + np.array(pts, float))], textposition="top right",
                         textfont=dict(color="#4C78A8"), showlegend=False), 1, 2)
fig.update_xaxes(title="λ")
fig.update_yaxes(title="slope m", range=[-2.5, 5.5])
fig.update_layout(template="simple_white", width=1100, height=480, font=font, margin=dict(l=70, r=30, t=60, b=60),
                  legend=dict(x=0.01, y=0.99, font=dict(size=13), bgcolor="rgba(255,255,255,0.85)"))
fig.write_image(here / "slope_vs_lambda.png", scale=2)
fig.write_image(here / "slope_vs_lambda.pdf")

s = np.linspace(-300, 300, 601)
fig = go.Figure()
fig.add_shape(type="rect", x0=-100, x1=100, y0=-4.5, y1=4.5, fillcolor="#E45756", opacity=0.08, line_width=0)
fig.add_trace(go.Scatter(x=s, y=s / D, mode="lines", line=dict(color="#BBBBBB", width=3, dash="dash"), name="linear regression: S / D"))
fig.add_trace(go.Scatter(x=s, y=s / (D + 100), mode="lines", line=dict(color="#4C78A8", width=5), name="Ridge: S / (D + λ)"))
fig.add_trace(go.Scatter(x=s, y=lasso(s, 100), mode="lines", line=dict(color="#E45756", width=5), name="Lasso"))
fig.add_annotation(x=0, y=3.6, text="−λ ≤ S ≤ λ: Lasso slope is exactly 0", showarrow=False, font=dict(color="#E45756", size=16))
fig.update_layout(template="simple_white", width=1000, height=480, font=font, margin=dict(l=70, r=30, t=50, b=60),
                  legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.85)"),
                  xaxis=dict(title="S = Σ(x − x̄)(y − ȳ)   (D = 50, λ = 100)"), yaxis=dict(title="slope m", range=[-4.5, 4.5]))
fig.write_image(here / "dead_zone.png", scale=2)
fig.write_image(here / "dead_zone.pdf")
