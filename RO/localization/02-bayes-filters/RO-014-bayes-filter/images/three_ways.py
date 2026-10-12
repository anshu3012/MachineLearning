"""Figure 8: one belief stored three ways, the predicted belief of Figure 6 (three bumps, at 3.5, 5.5 and 9.5 m).
Top, histogram filter (RO-015): one probability per 1 m cell, drawn as bars. Middle, particle filter (RO-016): 500
samples drawn from the belief; a dot's height is random, only to keep the dots apart. Bottom, Kalman filter (RO-017):
one Gaussian with the belief's mean 5.22 m and standard deviation 2.83 m (taken along the line from 0 to 10 m), one
wide hump. The grey line in the top and bottom panels is the belief itself.
Run: python three_ways.py -> three_ways.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from gifkit import FONT, GREY, ORANGE
from hallcont import BROWN, DOORS, LOOP, X, predicted

here = Path(__file__).parent
pred = predicted()
cells = np.array([np.trapezoid(pred[(X >= k) & (X <= k + 1)], X[(X >= k) & (X <= k + 1)]) for k in range(10)])
assert np.isclose(cells.sum(), 1, atol=1e-6) and set(np.argsort(cells)[-3:]) == {3, 5, 9}   # tallest bars: 3, 5, 9
M = 500
rng = np.random.default_rng(14)
cdf = np.cumsum(pred) / pred.sum()
particles = np.interp(rng.uniform(0, 1, M), cdf, X)                     # M samples from the belief (m)
jitter = np.random.default_rng(15).uniform(0.22, 0.97, M)
mean = np.trapezoid(X * pred, X)
sd = np.sqrt(np.trapezoid((X - mean) ** 2 * pred, X))
assert round(mean, 2) == 5.22 and round(sd, 2) == 2.83 and len(particles) == 500
gauss = np.exp(-0.5 * ((X - mean) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))

fig = make_subplots(rows=3, cols=1, vertical_spacing=0.13, subplot_titles=[
    "histogram filter (RO-015): one probability per 1 m cell",
    "particle filter (RO-016): 500 samples, crowded where the belief is high",
    f"Kalman filter (RO-017): one Gaussian, mean {mean:.2f} m, standard deviation {sd:.2f} m"])
fig.add_trace(go.Bar(x=np.arange(10) + 0.5, y=cells, width=0.85, marker_color=ORANGE), row=1, col=1)
fig.add_trace(go.Scatter(x=particles, y=jitter, mode="markers",
                         marker=dict(size=7, color=ORANGE, opacity=0.7, line=dict(width=0))), row=2, col=1)
fig.add_trace(go.Scatter(x=X, y=gauss, mode="lines", line=dict(color=ORANGE, width=5, simplify=False)), row=3, col=1)
for r in (1, 3):
    fig.add_trace(go.Scatter(x=X, y=pred, mode="lines", line=dict(color=GREY, width=2.5, simplify=False)), row=r, col=1)
for a, b in DOORS:                       # after the traces: Plotly skips shapes on a still-empty subplot
    for r in (1, 2, 3):
        fig.add_vrect(x0=a, x1=b, fillcolor=BROWN, opacity=0.13, line_width=0, layer="below", row=r, col=1)
fig.add_annotation(xref="x2 domain", yref="y2 domain", x=1, y=0.02, xanchor="right", yanchor="bottom", showarrow=False,
                   text="a dot's height is random, only to keep the dots apart", font=dict(size=17, color=GREY))
fig.add_annotation(xref="x3 domain", yref="y3 domain", x=1, y=0.98, xanchor="right", yanchor="top", showarrow=False,
                   text="mean and spread taken along the line 0 to 10 m", font=dict(size=17, color=GREY))
fig.add_annotation(xref="paper", yref="paper", x=0.5, y=1.09, showarrow=False, font=dict(size=19),
                   text=f"<span style='color:{GREY}'>grey line: the predicted belief of Figure 6</span>   "
                        f"<span style='color:{BROWN}'>shaded: doors</span>")
for r in (1, 2, 3):
    fig.update_xaxes(range=[0, LOOP], dtick=1, showticklabels=True, row=r, col=1)
fig.update_xaxes(title="position (m)", row=3, col=1)
fig.update_yaxes(range=[0, 0.2], dtick=0.05, title="per m", row=1, col=1)
fig.update_yaxes(range=[0, 1], visible=False, row=2, col=1)
fig.update_yaxes(range=[0, 0.2], dtick=0.05, title="per m", row=3, col=1)
fig.update_layout(template="simple_white", width=1100, height=1050, font=FONT, showlegend=False, bargap=0,
                  margin=dict(l=90, r=30, t=150, b=70),
                  title=dict(text="one belief, stored three ways", x=0.5, y=0.985, yanchor="top", font=dict(size=24)))
for ann in fig.layout.annotations[:3]:   # the subplot titles
    ann.font.size = 21
fig.write_image(here / "three_ways.png")
