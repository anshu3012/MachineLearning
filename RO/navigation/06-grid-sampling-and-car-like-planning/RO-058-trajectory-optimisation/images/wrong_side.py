"""The same optimiser from two first guesses, one solver step per frame, with the person standing 0.25 m further left
than in the Overview, at (2.65, 2.75). Left: started from last cycle's band (the warm start), which runs just right
of the person's centre: the steps push it right, into the gap between the person and the table, where it settles
with the robot's disk overlapping them by 0.02 m (cost 5.82). Right: started from a search, A* on a local costmap of
0.1 m cells (green dotted, 78 cells expanded), which goes left of the person: the same steps give a band that passes
0.15 m clear (cost 1.49). Both runs: TEB's 4 passes of 5 Levenberg-Marquardt steps. Run -> wrong_side.gif,
wrong_side_frames.png"""
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
from gifkit import BLUE, FONT, GREEN, ORANGE, RED, make_gif
from plotly.subplots import make_subplots

here = Path(__file__).parent
W = bk.results()["wrong"]
c = W["cycle"]
Hw, Ha = W["hist_w"], W["hist_a"]
assert len(Hw) == len(Ha) == 24 and W["expanded"] == 78


def closest(P):
    seg = np.concatenate([np.linspace(P[k, :2], P[k + 1, :2], 20) for k in range(len(P) - 1)])
    return float(bk.gap(seg[:, 0], seg[:, 1], bk.PERSON_LEFT).min())


assert round(W["res_w"][2], 2) == 5.82 and round(W["res_a"][2], 2) == 1.49
assert round(closest(W["res_w"][0]), 2) == -0.02 and round(closest(W["res_a"][0]), 2) == 0.15


OBS = bk.obstacles(bk.PERSON_LEFT)


def frame(i):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.03,
                        subplot_titles=["first guess: last cycle's band", "first guess: a search (A*)"])
    fig.update_annotations(font_size=22)
    for col, H in ((1, Hw), (2, Ha)):
        rc = (1, col)
        P, DT, _ = H[i]
        cost = bk.cost(P, DT, c["v"], c["final"], OBS)            # with TEB's set weights (obstacle 50)
        rd.room(fig, rc=rc)
        rd.person(fig, bk.PERSON_LEFT, bk.PERSON_R, rc=rc)
        if col == 2:
            fig.add_trace(go.Scatter(x=W["route"][:, 0], y=W["route"][:, 1], mode="lines",
                                     line=dict(color=GREEN, width=3, dash="dot")), row=1, col=2)
        rd.band(fig, P, ORANGE, rc=rc)
        g = c["goal"]
        fig.add_trace(go.Scatter(x=[g[0]], y=[g[1]], mode="markers", marker=dict(symbol="x", size=16, color=ORANGE)),
                      row=1, col=col)
        rd.robot(fig, *c["x"], BLUE, rc=rc, fill="rgba(255,255,255,0)")
        gp = closest(P)
        p, s = divmod(i, 6)
        head = "start" if i == 0 else f"pass {p + 1}, " + ("resized" if s == 0 else f"step {s}")
        lines = [f"<b>{head}</b>", f"cost {cost:.2f}",
                 f"<span style='color:{RED if gp < 0 else BLUE}'>gap to person or table: {gp:.2f} m</span>"]
        fig.add_annotation(x=1.72, y=3.62, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                           align="left", font=dict(size=19), bgcolor="rgba(255,255,255,0.9)", row=1, col=col)
        rd.zoom(fig, (1.7, 3.7), (1.65, 3.65), rc=rc)
    fig.update_layout(template="simple_white", font=FONT, width=1400, height=760, showlegend=False,
                      margin=dict(l=10, r=10, t=50, b=10))
    return fig


figs = [frame(i) for i in range(24)]
make_gif(figs, here / "wrong_side", fps=2, holds=[6] + [2] * 22 + [12], keys=[0, 5, 11, 23], cols=2, width=900)
