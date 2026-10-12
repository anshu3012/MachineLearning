"""G(jw) as an arrow: for the heading loop G(s) = 4/(s^2 + 0.8 s + 4), the complex number G(jw) is drawn as an arrow
from 0 while the weave rate w rises from 0.1 to 10 rad/s. Its length is the gain and its angle from the positive real
axis is the phase: 1.288 and -14.9 deg at 1 rad/s, 2.55 and -78.5 deg at 1.92 rad/s, 0.187 and -169.2 deg at 5 rad/s.
The tip leaves a trail; the last frame shows the whole curve with those rates marked.
Run: python arrow_anim.py -> arrow_anim.gif, arrow_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from loopkit import G_yr, deg

here = Path(__file__).parent
MARK = [0.5, 1.0, 1.92, 5.0]
G = {w: G_yr(1j * w) for w in MARK}
assert abs(abs(G[1.0]) - 1.288) < 5e-4 and abs(deg(G[1.0]) + 14.9) < 0.05
assert abs(abs(G[1.92]) - 2.55) < 5e-3 and abs(deg(G[1.92]) + 78.5) < 0.05
assert abs(abs(G[5.0]) - 0.187) < 5e-4 and abs(deg(G[5.0]) + 169.2) < 0.05
wall = np.logspace(-1, 1, 1500)
gall = G_yr(1j * wall)
WS = sorted(set(np.round(np.logspace(-1, 1, 22), 3)) | set(MARK))


def frame(w, last=False):
    g = G_yr(1j * w)
    trail = gall[wall <= w]
    fig = go.Figure()
    fig.add_shape(type="line", x0=-1.7, x1=1.7, y0=0, y1=0, line=dict(color=GREY, width=1))
    fig.add_shape(type="line", x0=0, x1=0, y0=-2.85, y1=0.5, line=dict(color=GREY, width=1))
    fig.add_trace(go.Scatter(x=(gall if last else trail).real, y=(gall if last else trail).imag, mode="lines",
                             line=dict(color=BLUE, width=3)))
    if not last:
        fig.add_annotation(x=g.real, y=g.imag, ax=0, ay=0, axref="x", ayref="y", xref="x", yref="y", showarrow=True,
                           arrowhead=3, arrowsize=1.4, arrowwidth=4, arrowcolor=ORANGE, text="")
        r = min(0.45, 0.8 * abs(g))
        a = np.linspace(0, np.angle(g), 60)
        fig.add_trace(go.Scatter(x=r * np.cos(a), y=r * np.sin(a), mode="lines", line=dict(color=RED, width=3)))
        title = (f"ω = {w:g} rad/s:   length (gain) {abs(g):.3f},   angle (phase) {deg(g):.1f}°").replace("-", "−")
    else:
        for wm in MARK:
            gm = G[wm]
            fig.add_trace(go.Scatter(x=[gm.real], y=[gm.imag], mode="markers", marker=dict(color=RED, size=13)))
            ax, ay = {0.5: (-150, 10), 1.0: (-150, 25), 1.92: (-40, -70), 5.0: (-40, -60)}[wm]
            fig.add_annotation(x=gm.real, y=gm.imag, text=f"{wm:g} rad/s: {abs(gm):.3g}, {deg(gm):.1f}°".replace("-", "−"),
                               ax=ax, ay=ay, arrowcolor=RED, font=dict(color=RED, size=18))
        fig.add_annotation(x=1, y=0, text="ω → 0: G = 1", ax=40, ay=-50, font=dict(size=18, color=GREY))
        title = "the tip's path as ω rises from 0.1 to 10 rad/s"
    fig.update_xaxes(title="real part", range=[-1.7, 1.7], zeroline=False)
    fig.update_yaxes(title="imaginary part", range=[-2.85, 0.5], zeroline=False, scaleanchor="x", scaleratio=1)
    fig.update_layout(template="simple_white", font=FONT, width=900, height=1000, showlegend=False,
                      margin=dict(l=90, r=30, t=110, b=70), title=dict(x=0.5, y=0.96, text=title, font=dict(size=22)))
    return fig


figs = [frame(w) for w in WS] + [frame(10, last=True)]
holds = [4] + [2 if w in MARK else 1 for w in WS[1:]] + [30]
i1 = WS.index(1.0)
make_gif(figs, here / "arrow_anim", fps=4, holds=holds, keys=[i1, WS.index(1.92), WS.index(5.0), len(figs) - 1], cols=2,
         width=760)
