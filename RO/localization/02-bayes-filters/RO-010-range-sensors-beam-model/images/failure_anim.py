"""Failures as an animation. The forward beam of pose A faces the wall 3 m away. Now and then its pulse is lost at the
wall (a black, light-absorbing spot or a shiny surface hit at a slant) and no echo comes back. The clock runs past
20.0 ns, when an echo from 3 m would be back, and on to 33.4 ns, the time a 5 m echo needs (light covers about
0.3 m per ns); with no echo by then the sensor reports its maximum range, 5 m. Every failure reading lands on 5 m,
so their histogram (counts per 0.05 m bin) is one bar at 5 m. Run -> failure_anim.gif"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from beammodel import ZMAX
from gifkit import FONT, GREY, PURPLE, RED, make_gif
from histkit import EDGES
from roomkit import C_NS, beam_view, text

here = Path(__file__).parent
MID = (EDGES[:-1] + EDGES[1:]) / 2


def frame(title, n=0, s=None, lost=False, t=None):
    """n failure readings so far; s: the pulse has travelled s metres out; lost: it vanished at the wall;
    t: the clock in ns."""
    fig = go.Figure()
    beam_view(fig)
    if s is not None:
        fig.add_trace(go.Scatter(x=[2, 2 + s], y=[2, 2], mode="lines", line=dict(color=RED, width=4)))
        if not lost:
            fig.add_trace(go.Scatter(x=[2 + s], y=[2], mode="markers",
                                     marker=dict(size=17, color=RED, symbol="circle-open", line=dict(width=4))))
    if lost:
        fig.add_trace(go.Scatter(x=[5], y=[2], mode="markers", marker=dict(size=20, color=PURPLE, symbol="x")))
        text(fig, 5.1, 1.45, "lost: no echo", PURPLE, size=18, ref=("x", "y"))
    if t is not None:
        text(fig, 3.6, 4.55, f"clock: {t:.1f} ns", size=24, ref=("x", "y"), anchor="center")
    if n:
        fig.add_trace(go.Scatter(x=[2, 2 + ZMAX], y=[2, 2], mode="lines", line=dict(color=PURPLE, width=3, dash="dash")))
        fig.add_trace(go.Scatter(x=[2 + ZMAX], y=[2], mode="markers", marker=dict(size=15, color=PURPLE)))
        text(fig, 6.9, 2.4, "reported: 5 m", PURPLE, size=18, ref=("x", "y"), anchor="right")
    counts = np.histogram(np.full(n, ZMAX), bins=EDGES)[0]
    fig.add_trace(go.Bar(x=MID, y=counts, width=0.05, marker=dict(color=PURPLE, line=dict(width=0)),
                         xaxis="x2", yaxis="y2"))
    top = max(5, 1.15 * n)
    fig.add_trace(go.Scatter(x=[3, 3], y=[0, top], mode="lines", line=dict(color=GREY, width=2, dash="dot"),
                             xaxis="x2", yaxis="y2"))
    fig.update_layout(xaxis2=dict(domain=[0.58, 1.0], anchor="y2", range=[0, 5.15], dtick=1, title="reading z (m)"),
                      yaxis2=dict(domain=[0.0, 0.86], anchor="x2", range=[0, top], title="number of readings"))
    text(fig, 0.79, 0.96, "histogram of the failure readings", size=20, anchor="center")
    text(fig, 3.05, 0.93 * top, "wall at 3 m", GREY, size=18, ref=("x2", "y2"))
    fig.update_layout(template="simple_white", width=1150, height=540, font=FONT, showlegend=False, bargap=0,
                      margin=dict(l=20, r=30, t=70, b=70), title=dict(text=title, x=0.5, font_size=22))
    return fig


figs = [frame("a failure: the pulse travels out", s=1.5, t=1.5 / C_NS),
        frame("the pulse is lost at the wall", s=3.0, lost=True, t=3.0 / C_NS),
        frame("an echo from the wall would be back by now: nothing", s=3.0, lost=True, t=6.0 / C_NS),
        frame("no echo by 33.4 ns, the time a 5 m echo needs: the sensor reports 5 m", n=1, s=3.0, lost=True,
              t=2 * ZMAX / C_NS)]
holds = [3, 4, 4, 8]
for n in (2, 3, 5, 10, 20, 50):
    figs.append(frame(f"{n} failures: every one reads exactly 5 m", n=n))
    holds.append(12 if n == 50 else 2)
make_gif(figs, here / "failure_anim", fps=2, holds=holds, keys=[3, len(figs) - 1], cols=2, width=950)
assert round(2 * ZMAX / C_NS, 1) == 33.4 and round(6.0 / C_NS, 1) == 20.0   # the clock limit and a 3 m echo
assert np.histogram([ZMAX], bins=EDGES)[0][-1] == 1                          # a 5 m reading lands in the last bin
