"""The partial derivative as the slope of a slice. Left: E(m, b) along b with m fixed at 0.558; right: along m with
b fixed at -0.896. A tangent line slides along each slice; its slope is the partial derivative, negative before the
bottom, 0 at the bottom (the OLS values) and positive after. Data: the 160 training students.
Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from common import B, M, X_train, y_train
from gifkit import BLUE, FONT, GREEN, ORANGE, RED, make_gif

HERE = Path(__file__).parent
x, y = X_train["cgpa"].to_numpy(), y_train.to_numpy()
E = lambda m, b: float(((y - m * x - b) ** 2).sum())
dEdb = lambda m, b: float(-2 * (y - m * x - b).sum())
dEdm = lambda m, b: float(-2 * ((y - m * x - b) * x).sum())

# Worked numbers quoted in the Note.
assert round(dEdb(M, -1.9)) == -321 and round(dEdb(M, 0.1)) == 319 and abs(dEdb(M, B)) < 1e-6
assert round(dEdm(0.45, B)) == -1727 and round(dEdm(0.65, B)) == 1473

bs_path = list(np.linspace(-1.9, B, 10)) + [B] * 4 + list(np.linspace(B, 0.1, 10))[1:]
ms_path = list(np.linspace(0.45, M, 10)) + [M] * 4 + list(np.linspace(M, 0.65, 10))[1:]
bb, mm = np.linspace(-2.0, 0.2, 200), np.linspace(0.44, 0.66, 200)
TOP = 1.05 * max(E(M, -2.0), E(0.44, B), E(0.66, B))


def word(s):
    if abs(s) < 1e-6:
        return "= 0: flat, the bottom", GREEN
    return ("< 0: E falls if we increase it", RED) if s < 0 else ("> 0: E rises if we increase it", ORANGE)


def frame(i):
    b, m = bs_path[i], ms_path[i]
    sb, sm = dEdb(M, b), dEdm(m, B)
    fig = make_subplots(1, 2, horizontal_spacing=0.12,
                        subplot_titles=[f"slice with m = {M:.3f}: E against b", f"slice with b = {B:.3f}: E against m"])
    fig.update_annotations(font_size=22)
    for col, grid, f, v, s, half in ((1, bb, lambda t: E(M, t), b, sb, 0.35), (2, mm, lambda t: E(t, B), m, sm, 0.035)):
        fig.add_trace(go.Scatter(x=grid, y=[f(t) for t in grid], mode="lines", line=dict(color=BLUE, width=4)), 1, col)
        w, colr = word(s)
        tx = np.array([v - half, v + half])
        fig.add_trace(go.Scatter(x=tx, y=f(v) + s * (tx - v), mode="lines", line=dict(color=colr, width=5)), 1, col)
        fig.add_trace(go.Scatter(x=[v], y=[f(v)], mode="markers",
                                 marker=dict(size=16, color=colr, line=dict(color="white", width=2))), 1, col)
        name = "∂E/∂b" if col == 1 else "∂E/∂m"
        fig.add_annotation(x=0.5, y=1.0, xref=f"x{col if col > 1 else ''} domain", yref=f"y{col if col > 1 else ''} domain", showarrow=False,
                           yanchor="top", font=dict(size=22, color=colr), text=f"{name} = {0 if abs(s) < 1e-6 else s:,.0f}<br>{w}")
    fig.update_xaxes(title="b (intercept)", range=[-2.0, 0.2], row=1, col=1)
    fig.update_xaxes(title="m (slope)", range=[0.44, 0.66], row=1, col=2)
    fig.update_yaxes(title="E", range=[0, TOP], row=1, col=1)
    fig.update_yaxes(range=[0, TOP], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=560, showlegend=False, font=FONT,
                      margin=dict(l=70, r=30, t=60, b=70))
    return fig


if __name__ == "__main__":
    figs = [frame(i) for i in range(len(bs_path))]
    holds = [1] * len(figs)
    holds[10] = holds[-1] = 8
    make_gif(figs, HERE / "tangent_slice", fps=5, holds=holds, keys=[0, 10, len(figs) - 1], cols=1, width=900)
