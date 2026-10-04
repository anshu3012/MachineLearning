"""The noise distribution decides the loss (Plotly). Left: normal noise N(0, 1) and Laplace noise with b = 1. Right:
minus the log of each density, shifted so both start at 0 at residual 0: the normal gives r^2/2 (squared error), the
Laplace gives |r| (absolute error). At an outlier with residual 3 the normal NLL adds 4.5, the Laplace NLL only 3."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
r = np.linspace(-4, 4, 401)
nll_n = -stats.norm(0, 1).logpdf(r) + stats.norm(0, 1).logpdf(0)
nll_l = -stats.laplace(0, 1).logpdf(r) + stats.laplace(0, 1).logpdf(0)
assert np.allclose(nll_n, r ** 2 / 2) and np.allclose(nll_l, np.abs(r))
assert abs(-stats.norm.logpdf(3) + stats.norm.logpdf(0) - 4.5) < 1e-9

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=("noise density", "−log density (shifted to 0) = loss"))
for y, col, name in ((stats.norm(0, 1).pdf(r), BLUE, "normal"), (stats.laplace(0, 1).pdf(r), ORANGE, "Laplace")):
    fig.add_trace(go.Scatter(x=r, y=y, mode="lines", line=dict(color=col, width=4), name=name), 1, 1)
fig.add_trace(go.Scatter(x=r, y=nll_n, mode="lines", line=dict(color=BLUE, width=4), showlegend=False), 1, 2)
fig.add_trace(go.Scatter(x=r, y=nll_l, mode="lines", line=dict(color=ORANGE, width=4), showlegend=False), 1, 2)
fig.add_trace(go.Scatter(x=[3, 3], y=[4.5, 3], mode="markers+text", marker=dict(size=13, color=[BLUE, ORANGE]),
                         text=["r²/2 = 4.5", "|r| = 3"], textposition=["top left", "bottom right"],
                         textfont=dict(size=20, color=[BLUE, ORANGE]), showlegend=False), 1, 2)
fig.add_annotation(x=3, y=0.2, text="outlier, residual 3", showarrow=False, font=dict(size=19, color=GREY), xref="x2", yref="y2")
fig.add_vline(x=3, line=dict(color=GREY, width=1.5, dash="dot"), row=1, col=2)
fig.update_xaxes(title_text="residual y − ŷ")
fig.update_yaxes(title_text="density", row=1, col=1)
fig.update_yaxes(title_text="loss", range=[0, 6], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=520, font=dict(family="Latin Modern Roman", size=20),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font_size=21)
fig.write_image(HERE / "gauss_vs_laplace.png", scale=2)
fig.write_image(HERE / "gauss_vs_laplace.pdf")
