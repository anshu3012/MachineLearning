"""Step 4 on numbers (homotopy classes), with the person 0.25 m further left, in the cycle at 2.5 s, stage by stage:
the two bands kept from the last cycle; the right one dropped because it sets off 97.3 degrees away from the picked
band's direction (more than 90 degrees); the band from the global plan, whose class is now free; 15 random samples in
a rectangle 6 m wide from the robot to the local goal; the edges that head forward and pass no obstacle point closer
than 0.1 m; the 4 paths depth-first search finds, each checked against the classes TEB has; the new band built on
the one path in a new class. Run -> roadmap_anim.gif, roadmap_anim_frames.png"""
import math
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import tebkit as tk
from gifkit import BLUE, FONT, GREEN, ORANGE, PURPLE, RED, make_gif

here = Path(__file__).parent
c = tk.results()["left"][25]
pl, rm = c["planner"], c["planner"]["roadmap"]
V, E, verdicts = rm["V"], rm["E"], rm["verdicts"]
w = pl["warm"]
ang = abs(math.degrees(tk.wrap(tk._start_dir(w[1], 0.4) - tk._start_dir(w[0], 0.4))))
assert pl["dropped_detours"] == 1 and pl["plan_band_added"] and round(ang, 1) == 97.3
assert len(V) == 17 and len(E) == 20 and [v for _, v in verdicts] == ["taken", "new", "taken", "taken"]
x, g = c["x"], c["goal"]
u = (g[:2] - x[:2]) / np.hypot(*(g[:2] - x[:2]))
nrm = np.array([-u[1], u[0]])
Lg = float(np.hypot(*(g[:2] - x[:2])))
rect = np.array([x[:2] - 3 * nrm, x[:2] + 3 * nrm, x[:2] + Lg * u + 3 * nrm, x[:2] + Lg * u - 3 * nrm, x[:2] - 3 * nrm])
cells = tk.costmap(x, bk.PERSON_LEFT)["cells"]

STAGES = ["kept from the last cycle: two bands", "dropped: the right band sets off 97° from the picked one",
          "added: the band from the global plan (its class is free)", "15 random samples, 6 m wide",
          "20 edges: forward, clear of obstacles by 0.1 m"] + \
         [f"depth-first path {i + 1} of 4: " + ("class taken" if v == "taken" else "<b>new class</b>")
          for i, (_, v) in enumerate(verdicts)] + ["the candidates: 3 bands, one per class"]


def frame(k):
    fig = go.Figure()
    rd.room(fig, band=False)
    fig.add_trace(go.Scatter(x=cells[:, 0], y=cells[:, 1], mode="markers", marker=dict(symbol="square", size=4,
                                                                                         color="#AAAAAA")))
    rd.person(fig, bk.PERSON_LEFT, bk.PERSON_R, label=False)
    if k <= 2:
        rd.band(fig, w[0].P, ORANGE, size=6, width=2, ticks=False)
        if k == 0:
            rd.band(fig, w[1].P, PURPLE, size=6, width=2, ticks=False)
        if k == 1:
            rd.band(fig, w[1].P, "#DDDDDD", size=5, width=2, ticks=False)
        if k == 2:
            rd.band(fig, pl["plan_band"].P, PURPLE, size=5, width=2, ticks=False)
    if 3 <= k < len(STAGES) - 1:
        fig.add_trace(go.Scatter(x=rect[:, 0], y=rect[:, 1], mode="lines", line=dict(color="#999999", dash="dot")))
        if k >= 4:
            xs, ys = [], []
            for a, b in E:
                xs += [V[a, 0], V[b, 0], None]
                ys += [V[a, 1], V[b, 1], None]
            fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color="#BBBBBB", width=1.5)))
        if k >= 5:
            path, v = verdicts[k - 5]
            fig.add_trace(go.Scatter(x=V[path, 0], y=V[path, 1], mode="lines", line=dict(
                color=GREEN if v == "new" else RED, width=5)))
        fig.add_trace(go.Scatter(x=V[1:-1, 0], y=V[1:-1, 1], mode="markers", marker=dict(size=11, color="#333333")))
    if k == len(STAGES) - 1:
        rd.band(fig, w[0].P, ORANGE, size=6, width=2, ticks=False)
        rd.band(fig, pl["plan_band"].P, PURPLE, size=5, width=2, ticks=False)
        rd.band(fig, rm["new"][0][1].P, GREEN, size=6, width=2, ticks=False)
    rd.robot(fig, *x, BLUE)
    fig.add_trace(go.Scatter(x=[g[0]], y=[g[1]], mode="markers", marker=dict(symbol="x", size=16, color="#333333")))
    fig.add_annotation(x=0.1, y=4.55, text=f"<b>t = 2.5 s</b>, stage {k + 1} of {len(STAGES)}<br>{STAGES[k]}",
                       showarrow=False, xanchor="left", yanchor="top", align="left", font=dict(size=20),
                       bgcolor="rgba(255,255,255,0.92)")
    fig.update_xaxes(range=[0.0, 5.6], visible=False)
    fig.update_yaxes(range=[-0.1, 4.6], visible=False, scaleanchor="x")
    fig.update_layout(template="simple_white", font=FONT, width=900, height=780, showlegend=False,
                      margin=dict(l=10, r=10, t=10, b=10))
    return fig


figs = [frame(k) for k in range(len(STAGES))]
make_gif(figs, here / "roadmap_anim", fps=1, holds=[3, 2, 2, 2, 2, 2, 3, 2, 2, 6], keys=[0, 2, 4, 6, 7, 9], cols=2,
         width=640)
