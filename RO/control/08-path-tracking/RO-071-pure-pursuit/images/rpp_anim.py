"""Regulated pure pursuit against plain pure pursuit at 5 m/s, both with the look-ahead that grows with speed
(speed x 2 s, from 2 to 10 m) and steering that lags 0.4 s, from the start 1.0 m left of the course. One frame per 0.25 s.
Orange: always 5 m/s. Blue: regulated (Nav2's curvature rule, r_min = 25 m, speed changes of at most 2.5 m/s^2); its
look-ahead circle is drawn, and shrinks as it slows. Panels: the course, the speed, the offset.
Last frame: middle of the arc 0.60 m (orange) against 0.27 m (blue); after the exit 0.76 m against 0.14 m; 7.0 s
against 11.4 s for the whole course.
Run: python rpp_anim.py -> rpp_anim.gif, rpp_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import trackkit as tk
from cardraw import car_traces, circle_points, course_trace
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif

here = Path(__file__).parent
fast = tk.simulate(tk.law("pp", ld_time=2.0), v=tk.V_FAST, tau=0.4)
reg = tk.simulate(tk.law("rpp", r_min=25.0, ld_time=2.0), v=tk.V_FAST, tau=0.4, a_max=2.5)
mf, mr = tk.metrics(fast), tk.metrics(reg)
assert abs(mf["arc_mid"] - 0.604) < 0.001 and abs(mr["arc_mid"] - 0.271) < 0.001
assert abs(mf["exit_peak"] + 0.755) < 0.001 and abs(mr["exit_peak"] + 0.142) < 0.001
assert abs(fast["t"][-1] - 7.01) < 0.01 and abs(reg["t"][-1] - 11.36) < 0.01 and abs(reg["v"].min() - 1.41) < 0.005
RUNS = ((fast, ORANGE, "always 5 m/s"), (reg, BLUE, "regulated"))


def frame(t, last=False):
    fig = make_subplots(rows=3, cols=1, row_heights=[0.56, 0.18, 0.26], vertical_spacing=0.07)
    fig.add_trace(course_trace(), row=1, col=1)
    for r, c, name in RUNS:
        i = min(int(round(t / tk.DT)), len(r["t"]) - 1)
        fig.add_trace(go.Scatter(x=r["x"][:i + 1], y=r["y"][:i + 1], mode="lines", line=dict(color=c, width=3),
                                 showlegend=False), row=1, col=1)
        for tr in car_traces(r["x"][i], r["y"][i], r["th"][i], r["delta"][i], c, body=False):
            fig.add_trace(tr, row=1, col=1)
        if r is reg and not last:
            ld = float(np.clip(r["v"][i] * 2.0, 2.0, 10.0))
            cx, cy = circle_points(r["x"][i], r["y"][i], ld)
            fig.add_trace(go.Scatter(x=cx, y=cy, mode="lines", line=dict(color=BLUE, width=2, dash="dash"),
                                     name=f"regulated car's look-ahead: {ld:.1f} m"), row=1, col=1)
        m = tk.metrics(r)
        lab = (f"{name}: arc middle {abs(m['arc_mid']):.2f} m, after exit {abs(m['exit_peak']):.2f} m, "
               f"{r['t'][-1]:.1f} s") if last else name
        fig.add_trace(go.Scatter(x=r["s"][:i + 1], y=r["v"][:i + 1], mode="lines", line=dict(color=c, width=3),
                                 showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=r["s"][:i + 1], y=r["e"][:i + 1], mode="lines", line=dict(color=c, width=3),
                                 name=lab), row=3, col=1)
    for row in (2, 3):
        for s0 in (tk.S1, tk.S2):
            fig.add_vline(x=s0, line=dict(color=GREY, dash="dot", width=1.5), row=row, col=1)
    fig.add_hline(y=0, line=dict(color="black", width=1), row=3, col=1)
    small = "<span style='font-size:19px'>"
    sub = "the whole course" if last else f"t = {t:.2f} s"
    fig.update_layout(template="simple_white", font=FONT, width=900, height=1300, margin=dict(l=90, r=30, t=110, b=70),
                      title=dict(x=0.5, y=0.98, yanchor="top",
                                 text=f"slow down where the arc is tight: regulated pure pursuit<br>{small}{sub}</span>"),
                      legend=dict(x=0.02, y=0.99, font=dict(size=17), bgcolor="rgba(255,255,255,0.9)"))
    fig.update_xaxes(title_text="x (m)", range=[-2, 24], dtick=5, row=1, col=1)
    fig.update_yaxes(title_text="y (m)", range=[-3, 23], dtick=5, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(range=[0, 36.5], dtick=5, row=2, col=1)
    fig.update_yaxes(title_text="speed (m/s)", range=[0, 5.6], dtick=1, row=2, col=1)
    fig.update_xaxes(title_text="distance along the course (m)", range=[0, 36.5], dtick=5, row=3, col=1)
    fig.update_yaxes(title_text="lateral error (m)", range=[-0.9, 1.1], dtick=0.25, row=3, col=1)
    return fig


t_end = reg["t"][-1]
ts = list(np.arange(0, t_end, 0.25)) + [t_end]
figs = [frame(t) for t in ts] + [frame(t_end, last=True)]
n = len(figs)
make_gif(figs, here / "rpp_anim", fps=4, holds=[6] + [1] * (n - 2) + [16], keys=[0, 12, 24, n - 1], cols=2, width=850)
