"""The particle filter on the corridor, one stage per frame: 100 particles start spread evenly; each reading weighs
them (marker size grows with weight), resampling copies the heavy ones, each move shifts every particle by 2.5 m plus
its own slip. Top: particles on the corridor (doors shaded), the true robot (red triangle) and the weighted mean
(black diamond). Bottom: the particles' histogram against the exact belief from a fine grid (blue line).
Run: python pf_loop.py -> pf_loop.gif, pf_loop_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from pfsim import DOORS, LOOP, X_TRUE, Z, grid_belief, run

here = Path(__file__).parent
M = 100
stages = run(M, np.random.default_rng(2))
xs, preds, bels = grid_belief()
final = stages[-2]                                     # weigh 3
assert abs(np.sum(final[1] * final[2]) - 7.0) < 0.15

TITLES = {"start": "start: 100 particles spread evenly (the robot has no idea)",
          "weigh 1": "weigh by reading 1, z = 1.46 m: particles at the doors grow",
          "resample 1": "resample: heavy particles copied, light ones dropped",
          "move 1": "move 2.5 m: every particle shifts, each with its own slip",
          "weigh 2": "weigh by reading 2, z = 1.58 m: two clusters stay heavy",
          "resample 2": "resample: the cloud now has two clusters",
          "move 2": "move 2.5 m again",
          "weigh 3": "weigh by reading 3, z = 1.41 m: one cluster stays heavy",
          "resample 3": "resample: the cloud sits at door 3, around the robot"}
jitter = np.random.default_rng(7).uniform(0.15, 0.85, M)


def truth(name):
    k = 0 if name in ("start", "weigh 1", "resample 1") else 1 if name in ("move 1", "weigh 2", "resample 2") else 2
    return X_TRUE[k]


def exact(name):
    if name == "start":
        return np.full_like(xs, 1 / LOOP)
    kind, k = name.split()
    return preds[int(k)] if kind == "move" else bels[int(k) - 1]


def frame(i, name, x, w):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.42, 0.58], vertical_spacing=0.12)
    for a, b in DOORS:
        for r in (1, 2):
            fig.add_shape(type="rect", x0=a, x1=b, y0=0, y1=1, yref="y domain" if r == 1 else "y2 domain",
                          xref="x" if r == 1 else "x2", fillcolor=ORANGE, opacity=0.18, line_width=0, layer="below")
    size = 4 + 16 * np.sqrt(w * M)
    fig.add_trace(go.Scatter(x=x, y=jitter, mode="markers", marker=dict(size=np.clip(size, 3, 60), color=BLUE,
                             opacity=0.55, line=dict(width=0))), row=1, col=1)
    fig.add_trace(go.Scatter(x=[truth(name)], y=[1.08], mode="markers+text", marker=dict(symbol="triangle-down",
                             size=22, color=RED), text=["robot"], textposition="middle right",
                             textfont=dict(size=17, color=RED)), row=1, col=1)
    mean = np.sum(w * x)
    fig.add_trace(go.Scatter(x=[mean], y=[-0.1], mode="markers+text", marker=dict(symbol="diamond", size=16,
                             color="black"), text=[f"weighted mean {mean:.2f} m"], textposition="middle right",
                             textfont=dict(size=16)), row=1, col=1)
    hist, edges = np.histogram(x, bins=40, range=(0, LOOP), weights=w)
    fig.add_trace(go.Bar(x=(edges[:-1] + edges[1:]) / 2, y=hist / (edges[1] - edges[0]), marker_color=GREY,
                         opacity=0.6, width=edges[1] - edges[0]), row=2, col=1)
    fig.add_trace(go.Scatter(x=xs, y=exact(name), mode="lines", line=dict(color=BLUE, width=3)), row=2, col=1)
    fig.update_xaxes(range=[0, LOOP], dtick=1, row=1, col=1, showticklabels=False)
    fig.update_yaxes(visible=False, range=[-0.25, 1.2], row=1, col=1)
    fig.update_xaxes(title="position x (m)", range=[0, LOOP], dtick=1, row=2, col=1)
    fig.update_yaxes(title="belief (per m)", range=[0, 2.4], row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1100, height=820, showlegend=False, bargap=0,
                      margin=dict(l=90, r=40, t=110, b=70),
                      title=dict(x=0.5, y=0.97, font=dict(size=23), text=f"{i + 1}. {TITLES[name]}"))
    fig.add_annotation(xref="paper", yref="paper", x=1, y=0.555, xanchor="right", showarrow=False, font=dict(size=16),
                       text="grey bars: share of particle weight per 0.25 m; blue line: exact belief")
    return fig


figs = [frame(i, *s) for i, s in enumerate(stages)]
names = [s[0] for s in stages]
make_gif(figs, here / "pf_loop", fps=2, holds=[4] * (len(figs) - 1) + [8],
         keys=[names.index(n) for n in ("start", "weigh 1", "move 1", "weigh 2", "move 2", "weigh 3")], cols=2, width=900)
