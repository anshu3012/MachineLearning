"""Animation: AMCL in the main run, one frame per filter update (our Python version of nav2_amcl with the bring-up's
sensor parameters and the tuning guide's odometry alphas 0.005; not Nav2 running). Black: where the robot truly is;
grey dashed: where odometry alone puts it (its left wheel is 1 percent smaller than the odometry assumes); blue: AMCL's
estimate, with up to 400 of its particles (dots). The filter updates only after 0.25 m or 0.2 rad of odometry.
Run -> amcl.gif, amcl_frames.png"""
import math
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import nav2sim as N
import roomdraw as rd
from gifkit import BLUE, FONT, GREY, make_gif

here = Path(__file__).parent
R = N.results()
m = R["main"]
L = m["log"]
U = m["amcl"]
assert len(U) == 21
times = np.array([x["t"] for x in L])


def frame(j, title):
    u = U[j]
    k = int(np.argmin(abs(times - u["t"])))
    fig = go.Figure()
    rd.room(fig)
    tr = np.array([x["true"][:2] for x in L[:k + 1]])
    od = np.array([x["odom"][:2] for x in L[:k + 1]])
    es = np.array([x["map"][:2] for x in L[:k + 1]])
    fig.add_trace(go.Scatter(x=od[:, 0], y=od[:, 1], mode="lines", line=dict(color=GREY, width=3, dash="dash"),
                             hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=tr[:, 0], y=tr[:, 1], mode="lines", line=dict(color="black", width=3),
                             hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=es[:, 0], y=es[:, 1], mode="lines", line=dict(color=BLUE, width=2.5),
                             hoverinfo="skip"))
    p = u["particles"]
    fig.add_trace(go.Scatter(x=p[:, 0], y=p[:, 1], mode="markers", marker=dict(size=4, color=BLUE, opacity=0.5),
                             hoverinfo="skip"))
    x = L[k]
    eo = math.hypot(*(x["odom"][:2] - x["true"][:2]))
    ea = math.hypot(*(x["map"][:2] - x["true"][:2]))
    fig.add_annotation(x=0.02, y=0.02, xref="paper", yref="paper", xanchor="left", yanchor="bottom", align="left",
                       text=f"update {j + 1} of 21, {u['t']:.1f} s<br>particles: {u['n_after']}<br>"
                            f"odometry off by {eo:.3f} m<br>AMCL off by {ea:.3f} m",
                       showarrow=False, font=dict(size=18), bgcolor="rgba(255,255,255,0.85)")
    rd.axes(fig)
    fig.update_layout(template="simple_white", width=820, height=920, showlegend=False, font=FONT,
                      margin=dict(l=10, r=10, t=70, b=10), title=dict(text=title, x=0.5, y=0.975, font=dict(size=20)))
    return fig


figs, holds, keys = [], [], []
for j, u in enumerate(U):
    figs.append(frame(j, "black: true; grey dashed: odometry alone; blue: AMCL"))
    holds.append(3)
    if j in (0, 2, 10):
        keys.append(j)
holds[0] = 6
holds[-1] = 16
keys.append(len(figs) - 1)
make_gif(figs, here / "amcl", fps=4, holds=holds, keys=keys, cols=2, width=700)
