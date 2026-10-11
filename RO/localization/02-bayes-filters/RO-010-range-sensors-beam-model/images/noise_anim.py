"""Measurement noise as an animation. With nobody in the way, the forward beam of pose A hits the wall 3 m away
again and again. Each reading is 3 m plus a Gaussian error with standard deviation 0.05 m, reported in 1 cm steps
(simulated; the first reading is the 3.02 m of the Note's worked example). Beside the room, the histogram of the
readings so far (density per m, one bar per 1 cm step, zoomed to 2.75 to 3.25 m) settles onto the Gaussian part
p_hit, whose peak is 7.98 per m. Run -> noise_anim.gif"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from beammodel import POSE, SIG_HIT, ZSTAR, p_hit
from gifkit import BLUE, FONT, GREY, RED, make_gif
from roomkit import axes, robot, room, text

here = Path(__file__).parent
X0, Y0, _ = POSE
N = 2000
z = np.random.default_rng(33).normal(ZSTAR, SIG_HIT, N).round(2)
EDGES = np.arange(2.745, 3.2551, 0.01)          # one bin per 1 cm step, centred on 2.75, 2.76, ..., 3.25
MID = (EDGES[:-1] + EDGES[1:]) / 2
G = np.linspace(2.75, 3.25, 400)
SHOW = [1, 2, 3, 4, 5, 10, 30, 100, 300, 1000, 2000]
near = np.mean(np.abs(z - ZSTAR) <= 0.10 + 1e-9)


def frame(n):
    fig = go.Figure()
    axes(fig, dom=(0.0, 0.36), titles=False)
    room(fig)
    fig.add_trace(go.Scatter(x=[X0, X0 + z[n - 1]], y=[Y0, Y0], mode="lines+markers", line=dict(color=RED, width=4),
                             marker=dict(size=[0, 12], color=RED)))
    robot(fig, X0, Y0)
    text(fig, 3.6, 2.45, "wall 3 m away", GREY, size=18, ref=("x", "y"), anchor="center")
    dens = np.histogram(z[:n], bins=EDGES)[0] / (n * 0.01)
    fig.add_trace(go.Bar(x=MID, y=dens, width=0.0095, marker=dict(color=BLUE, line=dict(width=0)),
                         xaxis="x2", yaxis="y2"))
    fig.add_trace(go.Scatter(x=G, y=p_hit(G, ZSTAR), mode="lines", line=dict(color="black", width=3),
                             xaxis="x2", yaxis="y2"))
    fig.update_layout(xaxis2=dict(domain=[0.47, 1.0], anchor="y2", range=[2.745, 3.255], dtick=0.05,
                                  title="reading z (m), zoom: 2.75 to 3.25 m"),
                      yaxis2=dict(domain=[0.0, 0.88], anchor="x2", range=[0, max(10, 1.1 * dens.max())],
                                  title="density (per m)"))
    text(fig, 0.735, 0.97, "histogram of the readings so far", size=20, anchor="center")
    text(fig, 0.49, 0.84, "black: Gaussian around 3 m,", size=18)
    text(fig, 0.49, 0.77, "σ = 0.05 m, peak 7.98 per m", size=18)
    title = (f"reading {n}: {z[n - 1]:.2f} m" if n <= 5 else
             f"{n} readings: {near:.0%} lie within 0.1 m of 3 m" if n == N else f"{n} readings of the same beam")
    fig.update_layout(template="simple_white", width=1150, height=560, font=FONT, showlegend=False, bargap=0,
                      margin=dict(l=30, r=30, t=70, b=70), title=dict(text=title, x=0.5, font_size=22))
    return fig


figs = [frame(n) for n in SHOW]
make_gif(figs, here / "noise_anim", fps=2, holds=[3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 12], keys=[6, len(SHOW) - 1],
         cols=2, width=950)
assert z[0] == 3.02 and round(float(p_hit(ZSTAR, ZSTAR)), 2) == 7.98 and round(float(p_hit(3.02, ZSTAR)), 2) == 7.37
assert abs(z.std() - SIG_HIT) < 0.003 and 0.94 < near < 0.98
