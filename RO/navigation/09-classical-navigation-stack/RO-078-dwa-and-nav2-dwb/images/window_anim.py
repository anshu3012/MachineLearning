"""The dynamic window in the plane of speed v and turn rate omega, built up stage by stage, at the person's cycle
(t = 2.4 s, the robot at 0.568 m/s and 0.263 rad/s): 1 one point = one command; 2 the robot's limits (v from 0 to
0.6 m/s, |omega| at most 1 rad/s, each wheel at most 0.6 m/s); 3 now; 4 DWA's window, reachable in one 0.05 s cycle;
5 DWB's window, reachable in sim_time = 1.7 s, which covers every limit; 6 the 20 x 21 samples; 7 the 44 that ask a
wheel for more than 0.6 m/s dropped, 375 left. Run -> window_anim.gif, window_anim_frames.png"""
import dwbkit as d
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, RED, make_gif

R = d.results()
o = [c for c in R["replan"]["cycles"] if abs(c["t"] - d.T_PERSON) < 1e-9][0]
rec = o["rec"]
v0, w0 = o["v"], o["w"]
dt = 1 / d.PARAMS["controller_frequency"]
dwa = (v0 - 0.5 * dt, min(0.6, v0 + 0.5 * dt), w0 - 3.2 * dt, w0 + 3.2 * dt)
assert [round(a, 3) for a in dwa] == [0.543, 0.593, 0.103, 0.423]
vs, ws = rec["vs"], rec["ws"]
grid = [(v, w) for v in vs for w in ws]
drop = [(v, w) for v, w in grid if (v == 0 and w == 0) or not d.wheel_ok(v, w)]
assert len(grid) == 420 and len(drop) == 45 and len(grid) - len(drop) == 375
TITLES = ["1  each point is one command: speed v, turn rate ω",
          "2  the robot's limits (grey)",
          "3  the command now, at t = 2.4 s",
          "4  DWA: reachable in one cycle, 0.05 s",
          "5  DWB: reachable in sim_time, 1.7 s",
          "6  20 speeds × 21 turn rates = 420 pairs",
          "7  drop (0, 0) and 44 over the wheel limit: 375"]


def frame(stage):
    fig = go.Figure()
    w = np.linspace(-1, 1, 201)
    if stage >= 1:
        fig.add_trace(go.Scatter(x=np.r_[w, w[::-1]], y=np.r_[0.6 - 0.1 * np.abs(w), np.zeros_like(w)], fill="toself",
                                 fillcolor="rgba(150,150,150,0.15)", line=dict(color=GREY, width=3)))
        fig.add_annotation(x=-0.55, y=0.69, text="each wheel at most 0.6 m/s: v + 0.1 |ω| ≤ 0.6", showarrow=False,
                           font=dict(size=17, color=GREY))
        fig.add_annotation(x=-1, y=0.25, text="|ω| ≤ 1", showarrow=False, xanchor="right", font=dict(size=17, color=GREY))
    if stage >= 4:
        fig.add_shape(type="rect", x0=-1.0, x1=1.0, y0=0.0, y1=0.6, line=dict(color=PURPLE, width=3, dash="dash"),
                      fillcolor="rgba(0,0,0,0)")
        fig.add_annotation(x=-0.97, y=0.03, text="DWB window, clipped to the limits", showarrow=False,
                           xanchor="left", yanchor="bottom", font=dict(size=17, color=PURPLE),
                           bgcolor="rgba(255,255,255,0.85)")
    if stage >= 5:
        pts = [p for p in grid if stage == 5 or p not in drop]
        fig.add_trace(go.Scatter(x=[p[1] for p in pts], y=[p[0] for p in pts], mode="markers",
                                 marker=dict(size=7, color="#7F7F7F")))
    if stage >= 6:
        fig.add_trace(go.Scatter(x=[p[1] for p in drop], y=[p[0] for p in drop], mode="markers",
                                 marker=dict(size=10, color=RED, symbol="x")))
    if stage == 0:
        fig.add_trace(go.Scatter(x=[0.5], y=[0.4], mode="markers", marker=dict(size=14, color=BLUE)))
        fig.add_annotation(x=0.5, y=0.4, text="drive 0.4 m/s while turning<br>0.5 rad/s: one arc",
                           ax=-120, ay=-60, font=dict(size=18, color=BLUE), arrowcolor=BLUE, align="left")
    if stage >= 3:
        fig.add_shape(type="rect", x0=dwa[2], x1=dwa[3], y0=dwa[0], y1=dwa[1], line=dict(color=ORANGE, width=3),
                      fillcolor="rgba(245,133,24,0.25)")
        fig.add_annotation(x=dwa[3], y=dwa[0], text="DWA window: ±0.025 m/s, ±0.16 rad/s", ax=0, ay=110,
                           font=dict(size=17, color=ORANGE), arrowcolor=ORANGE, bgcolor="rgba(255,255,255,0.85)")
    if stage >= 2:
        fig.add_trace(go.Scatter(x=[w0], y=[v0], mode="markers",
                                 marker=dict(size=15, color="white", line=dict(color=BLUE, width=3))))
    if stage >= 2:
        fig.add_annotation(x=w0, y=v0, text="now: 0.568 m/s, 0.263 rad/s", ax=190, ay=-55,
                           font=dict(size=17, color=BLUE), arrowcolor=BLUE)
    fig.add_annotation(x=0.5, y=1.0, xref="paper", yref="paper", text=f"<b>{TITLES[stage]}</b>", showarrow=False,
                       yanchor="bottom", font=dict(size=21))
    fig.update_xaxes(title_text="turn rate ω (rad/s)", range=[-1.25, 1.25], showgrid=False, zeroline=True,
                     zerolinecolor="#DDDDDD")
    fig.update_yaxes(title_text="speed v (m/s)", range=[-0.05, 0.75], showgrid=False)
    fig.update_layout(template="simple_white", font=FONT, width=900, height=760, showlegend=False,
                      margin=dict(l=90, r=30, t=60, b=80))
    return fig


figs = [frame(k) for k in range(7)]
make_gif(figs, "window_anim", fps=1, holds=[3, 3, 2, 3, 3, 3, 6], keys=[0, 3, 4, 6], cols=2)
