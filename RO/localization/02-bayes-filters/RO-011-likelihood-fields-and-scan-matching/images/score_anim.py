"""Scoring the scan at pose A with the likelihood field, beam by beam (Section 3.3 table as an animation). The room
of Figure 1, the robot at pose A (2, 2, 0) and its 12 beams, one every 30 degrees, taken one at a time: the beam
(dashed, not used by the model) and its end point (red dot); d, the end point's distance to the nearest obstacle
(purple arrow when it is long enough to see); the density 0.9 N(d; 0, 0.1^2) + 0.02 per m; and its natural log,
added to a running sum. The person's beam ends 1.01 m from the box corner (density 0.020), the 90-degree beam
0.03 m from the top wall (3.452), the 270-degree beam 0.02 m from the bottom wall (3.539), the other nine inside a
wall or the box (3.610). The logs, to 3 decimals, add up to 10.147: the log-likelihood 10.15 of the Note's table.
Run -> score_anim.gif"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from scipy.ndimage import distance_transform_edt
from fieldmodel import ANGLES, BOX, POSE_A, RES, cell, endpoints, field, field_loglik, make_map, scan_A
from gifkit import FONT, GREY, ORANGE, PURPLE, RED, make_gif
from roomdraw import robot_marker, room_shapes

here = Path(__file__).parent
occ, XS, YS = make_map()
DIST, IDX = distance_transform_edt(~occ, return_indices=True)
DIST = DIST * RES
F = field(DIST)
Z = scan_A()
PX, PY = endpoints(POSE_A, Z)
ANG = np.round(np.degrees(ANGLES)).astype(int)
D, DENS, NEAR = [], [], []
for x, y in zip(PX, PY):
    r, c = cell(x, y)
    D.append(DIST[r, c])
    DENS.append(F[r, c])
    nx, ny = XS[IDX[1][r, c]], YS[IDX[0][r, c]]
    NEAR.append("the box" if BOX[0] < nx < BOX[1] and BOX[2] < ny < BOX[3] else
                "the left wall" if nx < 0 else "the right wall" if nx > 5 else
                "the bottom wall" if ny < 0 else "the top wall")
NEAR[0] = "the box corner"
PEAK = float(field(0.0))                                  # 3.6105 per m, 3.610 to three decimals
SHOWN = [f"{p:.3f}" for p in DENS]
LOG = [round(float(np.log(p)), 3) for p in DENS]          # the logs as shown, to 3 decimals


def num(v, k=3):
    s = f"{v:.{k}f}"
    return s.lstrip("-") if float(s) == 0 else s.replace("-", "−")
RUN = np.round(np.cumsum(LOG), 3)                         # running sum of the shown logs
COLS = [0.585, 0.68, 0.78, 0.895]
CORNER = (BOX[0], BOX[2] + 0.6)                           # the box's top-left corner (3.6, 1.2)


def text(fig, x, y, s, color="black", size=19, anchor="left", ref=("paper", "paper")):
    fig.add_annotation(x=x, y=y, xref=ref[0], yref=ref[1], text=s, showarrow=False, xanchor=anchor,
                       yanchor="middle", font=dict(color=color, size=size), bgcolor="rgba(0,0,0,0)")


def room(fig, upto, cur):
    room_shapes(fig)
    text(fig, 3.9, 0.9, "box", size=19, anchor="center", ref=("x", "y"))
    fig.add_trace(go.Scatter(x=[3.12], y=[2], mode="markers", marker=dict(color=ORANGE, size=22)))
    text(fig, 3.12, 2.22, "person", ORANGE, size=18, anchor="center", ref=("x", "y"))
    for j in range(upto + 1):
        now = j == cur
        fig.add_trace(go.Scatter(x=[2, PX[j]], y=[2, PY[j]], mode="lines",
                                 line=dict(color=RED, width=3.5 if now else 1.5, dash="dash")))
        fig.add_trace(go.Scatter(x=[PX[j]], y=[PY[j]], mode="markers", cliponaxis=False,
                                 marker=dict(color=RED, size=16 if now else 10, line=dict(color="white", width=1.5))))
    if upto >= 0:                                         # the person's end point, 1.01 m from the box corner
        fig.add_annotation(x=CORNER[0], y=CORNER[1], ax=PX[0], ay=PY[0], xref="x", yref="y", axref="x", ayref="y",
                           text="", showarrow=True, arrowhead=2, arrowside="end+start", arrowwidth=3,
                           arrowcolor=PURPLE)
        text(fig, 3.38, 1.62, f"d = {D[0]:.2f} m", PURPLE, ref=("x", "y"))
    fig.add_trace(robot_marker(POSE_A, size=0.2))
    fig.update_xaxes(range=[-0.3, 5.3], dtick=1, domain=[0, 0.53], constrain="domain", title="x (m)")
    fig.update_yaxes(range=[-0.3, 4.3], dtick=1, domain=[0.14, 1.0], scaleanchor="x", constrain="domain",
                     constraintoward="top", title="y (m)")


def table(fig, upto, cur):
    for c, h in zip(COLS, ["beam", "d (m)", "density", "log"]):
        text(fig, c, 0.97, h, GREY)
    for j in range(12):
        got = j <= upto
        cells = [f"{ANG[j]}°"] + ([f"{D[j]:.2f}", SHOWN[j], num(LOG[j])] if got else ["…"] * 3)
        for i, (c, s) in enumerate(zip(COLS, cells)):
            text(fig, c, 0.905 - 0.06 * j, s, RED if (j == cur and i > 0) else ("black" if got else GREY))
    if upto >= 0:
        last = upto == 11 and cur is None
        text(fig, COLS[0], 0.15, ("sum of the 12 logs: " if last else "running sum of the logs: ") + num(RUN[upto]),
             RED if not last else "black", size=21)
    text(fig, COLS[0], 0.07, "density = 0.9 × Gaussian of d + 0.02", GREY, size=17)
    text(fig, COLS[0], 0.01, "log: natural logarithm of the density", GREY, size=17)


def legend(fig):
    text(fig, 0.265, 0.07, "dashed: the beam (not used by the model)", GREY, size=17, anchor="center")
    text(fig, 0.265, 0.01, "dot: its end point; purple: d to the nearest obstacle", GREY, size=17, anchor="center")


def frame(upto, cur, title):
    fig = go.Figure()
    room(fig, upto, cur)
    table(fig, upto, cur)
    legend(fig)
    fig.update_layout(template="simple_white", width=1150, height=780, font=FONT, showlegend=False,
                      margin=dict(l=70, r=20, t=110, b=30), title=dict(text=title, x=0.5, font_size=21))
    return fig


def beam_title(j):
    where = (f"d = {D[j]:.2f} m from {NEAR[j]}" if D[j] > 0 else f"inside {NEAR[j]}, so d = 0")
    head = f"beam {ANG[j]}°: reads {Z[j]:.2f} m, end point ({num(PX[j], 2)}, {num(PY[j], 2)})"
    if j == 0:
        head += ", at the person"
    return f"{head}<br>{where}: density {SHOWN[j]} per m, log {num(LOG[j])}"


figs = [frame(-1, None, "pose A (2, 2, 0): score the scan one beam at a time<br>"
                        "each end point's distance d to the nearest obstacle sets its density")]
holds = [5]
for j in range(12):
    figs.append(frame(j, j, beam_title(j)))
    holds.append({0: 8, 3: 6, 9: 5}.get(j, 3))
figs.append(frame(11, None, "the scan at pose A: 11 end points on a wall or the box, the person's 1.01 m away<br>"
                            f"sum of the 12 logs = {RUN[-1]:.3f}: the log-likelihood of the scan, 10.15"))
holds.append(20)
make_gif(figs, here / "score_anim", fps=2, holds=holds, keys=[1, len(figs) - 1], cols=2, width=950)

# the numbers of the Note's Section 3.3 tables and Section 3.1 worked example
assert [f"{d:.2f}" for d in D[:1]] == ["1.01"] and [round(D[j], 2) for j in (3, 9)] == [0.03, 0.02]
assert [SHOWN[j] for j in (0, 3, 9, 11)] == ["0.020", "3.452", "3.539", "3.610"] and round(PEAK, 4) == 3.6105
assert LOG[11] == round(float(np.log(PEAK)), 3) == 1.284
assert sum(D[j] == 0 for j in range(12)) == 9
assert round(field_loglik(F, POSE_A, Z), 2) == 10.15 and f"{RUN[-1]:.3f}" == "10.147" and round(RUN[-1], 2) == 10.15
assert (round(PX[3], 2), round(PY[3], 2)) == (2.0, 3.97) and (PX[0], PY[0]) == (3.0, 2.0)
