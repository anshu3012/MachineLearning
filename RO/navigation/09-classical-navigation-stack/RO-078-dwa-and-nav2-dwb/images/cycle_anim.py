"""The person's cycle (t = 2.4 s, main run), one frame per sampled speed. Top: the room near the robot; every pair
(speed, turn rate) of the window is rolled out for 1.7 s; red: illegal (a pose inside the robot-radius band of the
person or the table); legal rollouts coloured by their total score, darker = lower = better. Bottom: the same pairs
as dots in the plane of speed v and turn rate omega, inside our robot's wheel limit (grey line). Last frame: the
lowest total, 26.0, is a braking pair, (0.158 m/s, 0.263 rad/s). Our Python version of DWB's algorithm.
Run -> cycle_anim.gif, cycle_anim_frames.png"""
import math

import dwbkit as d
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from plotly.subplots import make_subplots

R = d.results()
C = R["replan"]["cycles"]
o = [c for c in C if abs(c["t"] - d.T_PERSON) < 1e-9][0]
rec = o["rec"]
pairs = np.array(rec["pairs"])
tot = np.array([t if t is not None else np.nan for t in rec["totals"]])
legal = ~np.isnan(tot)
best = int(np.nanargmin(tot))
assert len(pairs) == 375 and legal.sum() == 242 and round(tot[best], 1) == 26.0
assert np.allclose(pairs[best], (0.15789, 0.26316), atol=1e-4)
lo, hi = np.nanmin(tot), np.nanpercentile(tot, 95)
SHADES = ["#08306B", "#08519C", "#2171B5", "#4292C6", "#6BAED6", "#9ECAE1", "#C6DBEF"]


def shade(t):
    k = int(np.clip((t - lo) / (hi - lo) * len(SHADES), 0, len(SHADES) - 1))
    return SHADES[k]


ILL = "#F28B82"
vs = rec["vs"]
x = o["x"]


def frame(n_done, final=False):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.62, 0.38], vertical_spacing=0.07)
    rd.room(fig, rc=(1, 1))
    rd.plan(fig, o["local"], rc=(1, 1))
    rd.person(fig, d.PERSON, d.PERSON_R, rc=(1, 1))
    tt = np.linspace(0, 2 * math.pi, 80)
    fig.add_trace(go.Scatter(x=d.PERSON[0] + (d.PERSON_R + d.R_BODY) * np.cos(tt),
                             y=d.PERSON[1] + (d.PERSON_R + d.R_BODY) * np.sin(tt), mode="lines",
                             line=dict(color="#C2185B", width=1.5, dash="dot")), row=1, col=1)
    done = [i for i, (v, w) in enumerate(pairs) if v <= vs[n_done - 1] + 1e-9] if n_done else []
    ill = [rec["trajs"][i] for i in done if not legal[i]]
    rd.arcs(fig, ill, ILL, rc=(1, 1), width=1.2)
    groups = {}
    for i in done:
        if legal[i]:
            groups.setdefault(shade(tot[i]), []).append(rec["trajs"][i])
    for col in SHADES[::-1]:
        rd.arcs(fig, groups.get(col, []), col, rc=(1, 1), width=1.6)
    rd.robot(fig, x[0], x[1], x[2], BLUE, rc=(1, 1), fill="rgba(0,0,0,0)")
    if final:
        tb = rec["trajs"][best]
        rd.arcs(fig, [tb], ORANGE, rc=(1, 1), width=7)
        fig.add_trace(go.Scatter(x=[tb[-1, 0]], y=[tb[-1, 1]], mode="markers",
                                 marker=dict(size=16, color=ORANGE, line=dict(color="black", width=1.5))),
                      row=1, col=1)
    n_leg = int(sum(legal[i] for i in done))
    lines = [f"<b>t = 2.4 s</b>, speed {o['v']:.3f} m/s, turn {o['w']:.3f} rad/s",
             f"pairs rolled out: {len(done)} of 375" if not final else "all 375 pairs rolled out",
             f"<span style='color:{RED}'>illegal (hits a dotted band): {len(done) - n_leg}</span>",
             f"<span style='color:{SHADES[1]}'>legal: {n_leg}, darker = lower total = better</span>"]
    if final:
        lines.append(f"<span style='color:{ORANGE}'><b>lowest total 26.0: brake to 0.158 m/s</b></span>")
    fig.add_annotation(x=1.88, y=3.33, xref="x", yref="y", text="<br>".join(lines), showarrow=False,
                       xanchor="left", yanchor="top", align="left", font=dict(size=19),
                       bgcolor="rgba(255,255,255,0.9)")
    fig.add_annotation(x=2.75, y=3.42, xref="x", yref="y", text="local plan", showarrow=False,
                       font=dict(size=16, color=GREY), xanchor="left", yanchor="top")
    # the velocity plane
    w = np.linspace(-1, 1, 201)
    fig.add_trace(go.Scatter(x=w, y=d.V_WHEEL - np.abs(w) * d.L_AXLE / 2, mode="lines",
                             line=dict(color=GREY, width=2.5)), row=2, col=1)
    fig.add_annotation(x=0.0, y=0.66, xref="x2", yref="y2", text="wheel limit: v + 0.1 |ω| = 0.6",
                       showarrow=False, font=dict(size=16, color=GREY))
    cols = []
    for i in range(len(pairs)):
        if i not in set(done):
            cols.append("#DDDDDD")
        elif not legal[i]:
            cols.append(RED)
        else:
            cols.append(shade(tot[i]))
    fig.add_trace(go.Scatter(x=pairs[:, 1], y=pairs[:, 0], mode="markers",
                             marker=dict(size=8, color=cols, symbol=["x" if (i in done and not legal[i]) else "circle"
                                                                     for i in range(len(pairs))])),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=[o["w"]], y=[o["v"]], mode="markers",
                             marker=dict(size=16, color="white", line=dict(color=BLUE, width=3))), row=2, col=1)
    fig.add_annotation(x=o["w"], y=o["v"], xref="x2", yref="y2", text="now", ax=55, ay=-30,
                       font=dict(size=16, color=BLUE), arrowcolor=BLUE)
    if final:
        fig.add_trace(go.Scatter(x=[pairs[best, 1]], y=[pairs[best, 0]], mode="markers",
                                 marker=dict(size=18, color=ORANGE, line=dict(color="black", width=1.5))),
                      row=2, col=1)
    rd.zoom(fig, (1.85, 3.65), (1.35, 3.45), rc=(1, 1))
    fig.update_xaxes(title_text="turn rate ω (rad/s)", range=[-1.12, 1.12], row=2, col=1, showgrid=False)
    fig.update_yaxes(title_text="speed v (m/s)", range=[-0.04, 0.72], row=2, col=1, showgrid=False)
    fig.update_layout(template="simple_white", font=FONT, width=800, height=1300, showlegend=False,
                      margin=dict(l=90, r=20, t=10, b=70))
    return fig


figs = [frame(0)] + [frame(k) for k in range(1, len(vs) + 1)] + [frame(len(vs), final=True)]
holds = [6] + [2] * len(vs) + [16]
make_gif(figs, "cycle_anim", fps=4, holds=holds, keys=[0, 6, 14, len(figs) - 1], cols=2)
