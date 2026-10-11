"""Random readings as an animation. The forward beam of pose A faces the wall 3 m away, but now and then a stray echo
(cross-talk from another sensor, a reflection that comes back by an odd path) gives a reading with no relation to
the wall, anywhere from 0 to 5 m. We simulate 5000 such readings from the uniform part (1 cm steps); beside the
room, their histogram (density per m, 0.25 m bins) fills in evenly and settles on the flat line at
1 / 5 = 0.2 per m. Run -> random_anim.gif"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from beammodel import ZMAX, p_rand
from gifkit import FONT, GREEN, RED, make_gif
from roomkit import beam_view, text

here = Path(__file__).parent
N = 5000
z = np.random.default_rng(1).uniform(0, ZMAX, N).round(2)
EDGES = np.linspace(0, ZMAX, 21)
MID = (EDGES[:-1] + EDGES[1:]) / 2
SHOW = [1, 2, 3, 10, 50, 200, 1000, 5000]


def frame(n):
    fig = go.Figure()
    beam_view(fig)
    fig.add_trace(go.Scatter(x=[2, 5], y=[2, 2], mode="lines", line=dict(color=RED, width=2), opacity=0.35))
    past = z[max(0, n - 40):n - 1]
    fig.add_trace(go.Scatter(x=2 + past, y=np.full(len(past), 2.0), mode="markers",
                             marker=dict(size=8, color=GREEN, opacity=0.5)))
    fig.add_trace(go.Scatter(x=[2 + z[n - 1]], y=[2], mode="markers", marker=dict(size=17, color=GREEN)))
    text(fig, min(2 + z[n - 1], 6.35), 1.55, f"{z[n - 1]:.2f} m", GREEN, size=18, ref=("x", "y"), anchor="center")
    dens = np.histogram(z[:n], bins=EDGES)[0] / (n * 0.25)
    fig.add_trace(go.Bar(x=MID, y=dens, width=0.25, marker=dict(color=GREEN, line=dict(color="white", width=1)),
                         xaxis="x2", yaxis="y2"))
    fig.add_trace(go.Scatter(x=[0, ZMAX], y=[0.2, 0.2], mode="lines", line=dict(color="black", width=3),
                             xaxis="x2", yaxis="y2"))
    top = max(0.5, 1.1 * dens.max())
    fig.update_layout(xaxis2=dict(domain=[0.58, 1.0], anchor="y2", range=[0, 5.15], dtick=1, title="reading z (m)"),
                      yaxis2=dict(domain=[0.0, 0.8], anchor="x2", range=[0, top], title="density (per m)"))
    text(fig, 0.79, 0.96, "histogram of the random readings", size=20, anchor="center")
    text(fig, 0.79, 0.88, "black line: uniform part, 1 / 5 = 0.2 per m", size=18, anchor="center")
    title = (f"random reading {n}: a stray echo gives {z[n - 1]:.2f} m" if n <= 3 else
             f"{n} random readings: spread evenly from 0 to 5 m")
    fig.update_layout(template="simple_white", width=1150, height=540, font=FONT, showlegend=False, bargap=0,
                      margin=dict(l=20, r=30, t=70, b=70), title=dict(text=title, x=0.5, font_size=22))
    return fig


figs = [frame(n) for n in SHOW]
make_gif(figs, here / "random_anim", fps=2, holds=[4, 3, 3, 2, 2, 2, 2, 12], keys=[4, len(SHOW) - 1], cols=2,
         width=950)
dens = np.histogram(z, bins=EDGES)[0] / (N * 0.25)
assert float(p_rand(1.0)) == 0.2 and np.all(np.abs(dens - 0.2) < 0.03)   # the flat floor at 0.2 per m
