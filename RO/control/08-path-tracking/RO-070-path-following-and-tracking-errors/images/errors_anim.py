"""Path coordinates live, one frame per 0.25 s: the car at 2 m/s steered by RO-069's line rule on the course's tangent
at the nearest course point. Top left: the whole course with the distance s along it so far (green). Top right: a
10 m x 8 m window that follows the car: the nearest course point (orange dot), the course's tangent there (orange
dotted, and a copy at the car), the lateral error e from that point to the rear axle (purple) and the heading error
th_e from the course's direction to the car's heading (red arc). Lower panels: e and th_e against s. Measured: the
error starts at 1.000 m, first falls within 0.1 m at s = 7.70 m, settles near -0.39 m on the arc (at most 0.388 m outside it)
and is back within 0.1 m from s = 30.92 m. Run -> errors_anim.gif, errors_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from coursedraw import axes, car, course, frenet_marks, label, minus, trail
from gifkit import BLUE, FONT, GREEN, ORANGE, PURPLE, RED, make_gif
from plotly.subplots import make_subplots
from trackkit import L1, L_ARC, S_END, course_point, line_rule, run

here = Path(__file__).parent
deg = np.degrees
R = run(lambda q, t: line_rule(q))
E, TH, S = R["e"], deg(R["the"]), R["s"]
i_in = int(np.argmax(np.abs(E) < 0.1))
on_arc = (S > L1 + 5) & (S <= L1 + L_ARC)
j_out = np.where((S > L1 + L_ARC) & (np.abs(E) > 0.1))[0][-1]
assert E[0] == 1.0 and round(S[i_in], 2) == 7.70 and round(S[j_out], 2) == 30.92
assert round(E[on_arc].min(), 3) == -0.388 and round(R["t"][-1], 2) == 18.15


def frame(t):
    fig = make_subplots(rows=2, cols=2, row_heights=[0.62, 0.38], vertical_spacing=0.1, horizontal_spacing=0.1)
    k = min(int(round(t / 0.01)), len(R["t"]) - 1)
    q = (R["x"][k], R["y"][k], R["th"][k])
    for c in (1, 2):
        course(fig, (1, c), upto=S[k])
        trail(fig, R["x"][:k + 1], R["y"][:k + 1], BLUE, (1, c), width=2)
        car(fig, q, R["delta"][k], BLUE, (1, c), wheels=(c == 2), fill="rgba(76,120,168,0.10)" if c == 2 else "rgba(76,120,168,0.25)")
    frenet_marks(fig, q, S[k], E[k], R["the"][k], (1, 2))
    px, py, pth, _ = course_point(S[k])
    cx, cy = q[0] + 1.5 * np.cos(q[2]), q[1] + 1.5 * np.sin(q[2])
    nx, ny = -np.sin(pth), np.cos(pth)
    label(fig, cx - 4.8, cy + 3.4, f"s = {S[k]:.2f} m", GREEN, (1, 2), size=19, anchor="left")
    label(fig, cx - 4.8, cy + 2.5, f"e = {E[k]:.3f} m", PURPLE, (1, 2), size=19, anchor="left")
    label(fig, cx - 4.8, cy + 1.6, f"θ<sub>e</sub> = {TH[k]:.2f}°", RED, (1, 2), size=19, anchor="left")
    fig.add_trace(go.Scatter(x=S[:k + 1], y=E[:k + 1], mode="lines", line=dict(color=PURPLE, width=3),
                             showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=S[:k + 1], y=TH[:k + 1], mode="lines", line=dict(color=RED, width=3),
                             showlegend=False), row=2, col=2)
    for c in (1, 2):
        fig.add_vrect(x0=L1, x1=L1 + L_ARC, fillcolor="#F2F2F2", line_width=0, layer="below", row=2, col=c)
    label(fig, L1 + L_ARC / 2, 0.85, "arc", "#757575", (2, 1), size=16)
    label(fig, L1 + L_ARC / 2, 10.5, "arc", "#757575", (2, 2), size=16)
    axes(fig, (1, 1))
    fig.update_xaxes(range=[cx - 5, cx + 5], dtick=2, row=1, col=2, showgrid=True, gridcolor="#EEEEEE",
                     zeroline=False, title=dict(text="x (m)", standoff=2))
    fig.update_yaxes(range=[cy - 4, cy + 4], dtick=2, row=1, col=2, showgrid=True, gridcolor="#EEEEEE",
                     zeroline=False, scaleanchor="x2", scaleratio=1, title=dict(text="y (m)", standoff=2))
    fig.update_xaxes(title=dict(text="s, distance along the course (m)", standoff=2), range=[0, S_END + 0.5], dtick=10,
                     row=2)
    fig.update_yaxes(title=dict(text="lateral error e (m)", standoff=2), range=[-0.5, 1.05], dtick=0.5, row=2, col=1)
    fig.update_yaxes(title=dict(text="heading error θ<sub>e</sub> (°)", standoff=2), range=[-13, 13], dtick=5,
                     row=2, col=2)
    if k == len(R["t"]) - 1:
        title = ("at the end of the course, 18.15 s<br><span style='font-size:19px'>"
                 "the error settled at −0.39 m on the arc: the car ran outside it</span>")
    else:
        title = (f"t = {R['t'][k]:.2f} s: the car in path coordinates<br><span style='font-size:19px'>"
                 "nearest course point (orange), lateral error (purple), heading error (red)</span>")
    fig.update_layout(template="simple_white", font=FONT, width=1100, height=1050, showlegend=False,
                      margin=dict(l=90, r=30, t=120, b=60), title=dict(x=0.5, y=0.975, yanchor="top", text=minus(title)))
    return fig


ts = list(np.arange(0, 18.15, 0.25)) + [18.15]
figs = [frame(t) for t in ts]
holds = [4] + [1] * (len(ts) - 2) + [14]
make_gif(figs, here / "errors_anim", fps=5, holds=holds, keys=[0, 8, 40, len(ts) - 1], cols=2, width=850)
