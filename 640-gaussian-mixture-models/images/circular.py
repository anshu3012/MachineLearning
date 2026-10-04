"""The circular dependence, step by step (Plotly frames -> GIF), on MML's seven points and starting mixture
N(-4, 1), N(0, 0.2), N(8, 3), weights 1/3. Frame 1: the start; point -1 belongs 0.057 to component 1. Frame 2: the
slope-zero formula moves mu1 to the responsibility-weighted mean, -2.70. Frame 3: with mu1 = -2.70 the
responsibilities change; point -1 now belongs 0.56 to component 1. Frame 4: the same formula now gives -2.34, so
-2.70 did not satisfy its own equation."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import norm
from common import COLS, FONT
from gifkit import make_gif

here = Path(__file__).parent
x = np.array([-3, -2.5, -1, 0, 2, 4, 5.0])
VAR, PI = np.array([1, 0.2, 3]), np.ones(3) / 3


def resp(mu):
    d = PI * norm.pdf(x[:, None], mu, np.sqrt(VAR))
    return d / d.sum(1, keepdims=True)


mu0 = np.array([-4.0, 0, 8])
r0 = resp(mu0)
m1 = (r0[:, 0] * x).sum() / r0[:, 0].sum()
mu1 = mu0.copy(); mu1[0] = m1
r1 = resp(mu1)
m2 = (r1[:, 0] * x).sum() / r1[:, 0].sum()
assert round(r0[2, 0], 3) == 0.057 and round(m1, 2) == -2.70 and round(r1[2, 0], 2) == 0.56 and round(m2, 2) == -2.34
g = np.linspace(-7, 10, 600)
STEPS = [(mu0, r0, "1. start: μ₁ = −4; point −1 belongs 0.057 to component 1"),
         (mu1, r0, f"2. slope = 0 gives μ₁ = Σ r x / Σ r = {m1:.2f} (old responsibilities)"),
         (mu1, r1, f"3. with μ₁ = {m1:.2f} the responsibilities change: point −1 now {r1[2, 0]:.2f}"),
         (np.array([m2, 0, 8]), r1, f"4. the same formula now gives μ₁ = {m2:.2f}: not the {m1:.2f} we had")]


def frame(mu, r, title):
    fig = make_subplots(2, 1, vertical_spacing=0.14, row_heights=[0.55, 0.45],
                        subplot_titles=["the mixture and the seven points", "responsibility of component 1 for each point"])
    fig.update_annotations(font_size=20)
    for k in range(3):
        fig.add_trace(go.Scatter(x=g, y=PI[k] * norm.pdf(g, mu[k], np.sqrt(VAR[k])), mode="lines",
                                 line=dict(color=COLS[k], width=3)), 1, 1)
    fig.add_trace(go.Scatter(x=x, y=np.zeros_like(x), mode="markers", marker=dict(size=12, color="black")), 1, 1)
    fig.add_trace(go.Bar(x=x, y=r[:, 0], marker_color=COLS[0], width=0.35, text=[f"{v:.2f}" for v in r[:, 0]],
                         textposition="outside", textfont=dict(size=16)), 2, 1)
    fig.update_xaxes(range=[-7, 10], row=1, col=1)
    fig.update_yaxes(range=[0, 0.32], row=1, col=1)
    fig.update_xaxes(title="x", range=[-7, 10], row=2, col=1)
    fig.update_yaxes(range=[0, 1.25], row=2, col=1)
    fig.update_layout(template="simple_white", width=1100, height=680, font=FONT, showlegend=False,
                      title=dict(text=title, x=0.5, font=dict(size=22)), margin=dict(l=60, r=30, t=100, b=60))
    return fig


if __name__ == "__main__":
    make_gif([frame(*s) for s in STEPS], here / "circular", fps=1, holds=[3, 3, 3, 4], keys=[2, 3], cols=1)
