"""The timed elastic band being optimised, one solver step per frame, in the cycle the person is first seen
(t = 2.4 s). The first frame is the warm start: last cycle's band, its first pose moved to the robot, its last to
the local goal (cross); it runs through the person. Then 4 passes of TEB's optimiser: each pass first inserts or
removes poses so neighbours stay about 0.3 s apart, then takes 5 Levenberg-Marquardt steps; the obstacle weight
starts at 50 and doubles after each pass. The text gives the pass, the step, the number of poses, the cost (with
that pass's weight) and the closest the robot's disk comes to the person along the band (negative: overlap).
Run -> band_anim.gif, band_anim_frames.png"""
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
from gifkit import BLUE, FONT, ORANGE, RED, make_gif

here = Path(__file__).parent
c = bk.results()["loop"][24]
H = c["hist"]
assert round(c["t"], 1) == 2.4 and len(H) == 4 * 6


def closest(P):
    seg = np.concatenate([np.linspace(P[k, :2], P[k + 1, :2], 20) for k in range(len(P) - 1)])
    return float(bk.gap(seg[:, 0], seg[:, 1], bk.PERSON).min())


g0, gN = closest(H[0][0]), closest(H[-1][0])
assert round(g0, 2) == -0.22 and round(gN, 2) == 0.15 and len(H[0][0]) == 9 and len(H[-1][0]) == 10


OBS = bk.obstacles(bk.PERSON)


def frame(i):
    P, DT, _ = H[i]
    cost = bk.cost(P, DT, c["v"], c["final"], OBS)                # with TEB's set weights (obstacle 50)
    p, s = divmod(i, 6)
    fig = go.Figure()
    rd.room(fig)
    rd.route(fig, bk.ROUTE)
    rd.person(fig, bk.PERSON, bk.PERSON_R)
    if i > 0:
        rd.band(fig, H[0][0], "#F9D2A8", size=6, width=1.5, ticks=False)
    rd.band(fig, P, ORANGE)
    g = c["goal"]
    fig.add_trace(go.Scatter(x=[g[0]], y=[g[1]], mode="markers", marker=dict(symbol="x", size=18, color=ORANGE)))
    rd.robot(fig, *c["x"], BLUE, fill="rgba(255,255,255,0)")
    head = "<b>warm start</b>: last cycle's band" if i == 0 else (
        f"<b>pass {p + 1} of 4</b>, " + ("poses resized" if s == 0 else f"step {s} of 5"))
    gp = closest(P)
    lines = [head, f"{len(P)} poses, {DT.sum():.2f} s", f"solver's clearance weight {50 * 2 ** p}", f"cost {cost:.2f}",
             f"<span style='color:{RED if gp < 0 else BLUE}'>disk to person: {gp:.2f} m</span>"]
    fig.add_annotation(x=1.75, y=3.55, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=20), bgcolor="rgba(255,255,255,0.9)")
    rd.zoom(fig, (1.7, 3.75), (1.65, 3.6))
    fig.update_layout(template="simple_white", font=FONT, width=820, height=800, showlegend=False,
                      margin=dict(l=10, r=10, t=10, b=10))
    return fig


figs = [frame(i) for i in range(len(H))]
make_gif(figs, here / "band_anim", fps=2, holds=[6] + [2] * (len(figs) - 2) + [12], keys=[0, 1, 5, 11, 17, 23],
         cols=3, width=620)
print("closest", round(g0, 3), "->", round(gN, 3), "costs", [round(bk.cost(h[0], h[1], c["v"], c["final"], OBS), 2) for h in H])
