"""Still: what two real sensors would see from the robot at 2.4 s, when the person steps in. Left: a 2D laser
scanner like the Hokuyo URG-04LX-UG01 at the robot's centre, facing forward: 240 degrees in 0.352 degree steps
(682 readings), out to 5.6 m; red dots are where its readings stop; the grey wedge behind is the 120 degrees it never
sees, where Nav2's default back-up recovery (0.30 m) drives. Right: a depth camera like the RealSense D435: 87 degrees
wide, from 0.3 m to 3 m. The dashed circle is the distance the robot needs to see an obstacle in, 0.67 m from its
centre (0.42 m from its rim at 0.6 m/s with a 0.1 s loop). Run -> coverage.png"""
import math
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import stackkit as sk
from gifkit import BLUE, FONT, GREY, ORANGE, RED
from plotly.subplots import make_subplots

here = Path(__file__).parent
o = bk.results()["loop"][24]
x, y, h = o["x"][:3]
NEED = round(0.6 * 0.1 + 0.6 ** 2 / (2 * 0.5) + 0.25, 2)
assert NEED == 0.67
n = round(240 / 0.352)
assert n == 682
b360, r360 = sk.ranges((x, y, h), bk.PERSON, n=1024, rmax=5.6, origin=0.0)      # 1024 steps a turn, as the scanner
keep = np.abs(b360) <= math.radians(120)
assert keep.sum() in (682, 683)


def wedge(c, r0, r1, a0, a1, m=60):
    a = np.linspace(a0, a1, m)
    xs = np.concatenate([c[0] + r1 * np.cos(a), c[0] + r0 * np.cos(a[::-1])])
    ys = np.concatenate([c[1] + r1 * np.sin(a), c[1] + r0 * np.sin(a[::-1])])
    return np.append(xs, xs[0]), np.append(ys, ys[0])


fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.03,
                    subplot_titles=["laser scanner: 240°, to 5.6 m", "depth camera: 87°, 0.3 to 3 m"])
fig.update_annotations(font_size=22)
for col in (1, 2):
    rc = (1, col)
    rd.room(fig, rc=rc)
    rd.person(fig, bk.PERSON, bk.PERSON_R, rc=rc)
    if col == 1:
        wx, wy = wedge((x, y), 0, 0.8, h + math.radians(120), h + math.radians(240))
        fig.add_trace(go.Scatter(x=wx, y=wy, fill="toself", fillcolor="rgba(107,107,107,0.25)", mode="lines",
                                 line=dict(color=GREY, width=1)), row=1, col=1)
        px = x + r360[keep] * np.cos(h + b360[keep])
        py = y + r360[keep] * np.sin(h + b360[keep])
        fig.add_trace(go.Scatter(x=px, y=py, mode="markers", marker=dict(size=3, color=RED)), row=1, col=1)
        bx, by = x - 0.30 * math.cos(h), y - 0.30 * math.sin(h)
        fig.add_annotation(x=bx, y=by, ax=x, ay=y, xref="x", yref="y", axref="x", ayref="y", showarrow=True,
                           arrowhead=2, arrowwidth=3, arrowcolor=GREY, text="", row=1, col=1)
        fig.add_annotation(x=x - 1.25 * math.cos(h) - 0.25, y=y - 1.25 * math.sin(h), text="blind 120\u00b0:<br>"
                           "the back-up recovery<br>drives 0.30 m here", showarrow=False, font=dict(size=17, color=GREY),
                           row=1, col=1)
    else:
        bc, rc_ = sk.ranges((x, y, h), bk.PERSON, n=1440, rmax=3.0, origin=0.0)
        m = np.abs(bc) <= math.radians(43.5)
        order = np.argsort(bc[m])
        a, r = bc[m][order], np.maximum(rc_[m][order], 0.3)
        a0 = np.linspace(a[-1], a[0], 30)
        wx = np.concatenate([x + r * np.cos(h + a), x + 0.3 * np.cos(h + a0)])
        wy = np.concatenate([y + r * np.sin(h + a), y + 0.3 * np.sin(h + a0)])
        fig.add_trace(go.Scatter(x=np.append(wx, wx[0]), y=np.append(wy, wy[0]), fill="toself",
                                 fillcolor="rgba(245,133,24,0.20)", mode="lines", line=dict(color=ORANGE, width=2)),
                      row=1, col=2)
        fig.add_annotation(x=x + 1.5 * math.cos(h + math.radians(28)), y=y + 1.5 * math.sin(h + math.radians(28)),
                           text="what the<br>camera sees", showarrow=False, font=dict(size=17, color=ORANGE),
                           row=1, col=2)
    t = np.linspace(0, 2 * math.pi, 120)
    fig.add_trace(go.Scatter(x=x + NEED * np.cos(t), y=y + NEED * np.sin(t), mode="lines",
                             line=dict(color=BLUE, width=2.5, dash="dash")), row=1, col=col)
    rd.robot(fig, x, y, h, BLUE, rc=rc)
    fig.add_annotation(x=x - NEED * 0.72, y=y + NEED * 0.72, text="needed: 0.67 m", showarrow=False, xanchor="right",
                       yanchor="bottom", font=dict(size=17, color=BLUE), row=1, col=col)
    rd.axes(fig, rc=rc)
fig.update_layout(template="simple_white", font=FONT, width=1300, height=900, showlegend=False,
                  margin=dict(l=10, r=10, t=50, b=10))
fig.write_image(here / "coverage.png", scale=2)
