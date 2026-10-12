"""Why a tracker needs both errors, one frame per 0.3 s, all three cars at 2 m/s from 1.0 m left of the course.
Blue: the line rule on both errors, w = -0.5 e - 2 th_e. Red: lateral error only (heading gain 0): nothing damps the
swing, so the car weaves across the course at s = 3.16, 9.62, 14.56, 24.50 and 30.79 m, up to 2.09 m off. Purple:
heading error only (lateral gain 0): nothing pulls it back, so it stays 1.00 m off along the whole first straight.
Lower panel: the lateral error e of each against the distance s along the course.
Run -> two_errors.gif, two_errors_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from coursedraw import axes, car, course, label, minus, trail
from gifkit import BLUE, FONT, PURPLE, RED, make_gif
from plotly.subplots import make_subplots
from trackkit import L1, L_ARC, S_END, line_rule, run

here = Path(__file__).parent
CASES = [((0.5, 2.0), BLUE, "both errors"), ((0.5, 0.0), RED, "lateral error only"),
         ((0.0, 2.0), PURPLE, "heading error only")]
R = [run(lambda q, t, k=k: line_rule(q, k_d=k[0], k_h=k[1]), t_max=25) for k, _, _ in CASES]
red, pur = R[1], R[2]
zc = red["s"][np.where(np.diff(np.sign(red["e"])) != 0)[0]]
assert np.allclose(np.round(zc, 2), [3.16, 9.62, 14.56, 24.50, 30.79])
assert round(np.abs(red["e"]).max(), 2) == 2.09
assert round(np.interp(L1, pur["s"], pur["e"]), 2) == 1.00
T_END = max(r["t"][-1] for r in R)


def frame(t):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3], vertical_spacing=0.08)
    course(fig, (1, 1))
    for (k, col, name), r in zip(CASES, R):
        i = min(int(round(t / 0.01)), len(r["t"]) - 1)
        trail(fig, r["x"][:i + 1], r["y"][:i + 1], col, (1, 1))
        car(fig, (r["x"][i], r["y"][i], r["th"][i]), r["delta"][i], col, (1, 1), wheels=False,
            fill="rgba(255,255,255,0.3)")
        fig.add_trace(go.Scatter(x=r["s"][:i + 1], y=r["e"][:i + 1], mode="lines", line=dict(color=col, width=3),
                                 showlegend=False), row=2, col=1)
    fig.add_vrect(x0=L1, x1=L1 + L_ARC, fillcolor="#F2F2F2", line_width=0, layer="below", row=2, col=1)
    label(fig, -1.5, 22.3, "blue: both errors, ω = −0.5 e − 2 θ<sub>e</sub>", BLUE, (1, 1), size=17, anchor="left")
    label(fig, -1.5, 20.6, "red: lateral error only, ω = −0.5 e", RED, (1, 1), size=17, anchor="left")
    label(fig, -1.5, 18.9, "purple: heading error only, ω = −2 θ<sub>e</sub>", PURPLE, (1, 1), size=17, anchor="left")
    title = (f"t = {t:.1f} s<br><span style='font-size:19px'>the same start, 1.0 m left of the course, at 2 m/s</span>")
    if t >= T_END:
        title = ("lateral error only weaves; heading error only stays off<br><span style='font-size:19px'>"
                 "both errors together settle onto the course</span>")
    axes(fig, (1, 1))
    fig.update_xaxes(title=dict(text="s, distance along the course (m)", standoff=2), range=[0, S_END + 0.5], dtick=5,
                     row=2, col=1)
    fig.update_yaxes(title=dict(text="lateral error e (m)", standoff=2), range=[-2.3, 1.3], dtick=1, row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1250, showlegend=False,
                      margin=dict(l=100, r=30, t=120, b=60), title=dict(x=0.5, y=0.975, yanchor="top", text=minus(title)))
    return fig


ts = list(np.arange(0, T_END, 0.3)) + [T_END]
figs = [frame(t) for t in ts]
holds = [4] + [1] * (len(ts) - 2) + [14]
make_gif(figs, here / "two_errors", fps=5, holds=holds, keys=[0, 13, 33, len(ts) - 1], cols=2, width=800)
