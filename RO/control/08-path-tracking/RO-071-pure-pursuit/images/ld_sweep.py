"""The look-ahead distance swept: 2 m (red), 4 m (blue) and 8 m (purple), all three cars starting 1.0 m left of the
course. Two animations, one frame per 0.5 s or 0.2 s:
- ld_sweep: the plan's car at 2 m/s, its wheels turning the instant they are told. The 2 m car is back within 0.1 m
  after 4.0 m but steers at full lock (26.6 deg) at the start; the 8 m car returns slowly and cuts 0.85 m inside the arc.
- ld_sweep_lag: 5 m/s, and the wheels follow the command with a first-order lag of 0.4 s (Stanford's steering model,
  Hoffmann et al. 2007). The 2 m car weaves: 0.83 m past the line, then 1.25 m off on the arc; the 4 m car swings
  0.26 m past the line; the 8 m car does not weave but cuts 0.56 m inside the arc.
Run: python ld_sweep.py -> ld_sweep.gif, ld_sweep_frames.png, ld_sweep_lag.gif, ld_sweep_lag_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import trackkit as tk
from cardraw import car_traces, course_trace
from gifkit import BLUE, FONT, GREY, PURPLE, RED, make_gif

here = Path(__file__).parent
LDS, COLS = (2.0, 4.0, 8.0), (RED, BLUE, PURPLE)


def runs(v, tau):
    out = [tk.simulate(tk.law("pp", ld=ld), v=v, tau=tau) for ld in LDS]
    return out, [tk.metrics(r) for r in out]


def label(ld, m, lag):
    if not lag:
        return {2.0: f"2 m: within 0.1 m after {m['reach']:.1f} m; full lock at the start",
                4.0: f"4 m: within 0.1 m after {m['reach']:.1f} m",
                8.0: f"8 m: cuts {m['arc_peak']:.2f} m inside the arc"}[ld]
    return {2.0: f"2 m: {m['over']:.2f} m past the line, {abs(m['arc_peak']):.2f} m off on the arc",
            4.0: f"4 m: {m['over']:.2f} m past the line",
            8.0: f"8 m: no swing; cuts {m['arc_peak']:.2f} m inside the arc"}[ld]


def frame(rs, ms, t, lag, v, last=False):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.62, 0.38], vertical_spacing=0.09)
    fig.add_trace(course_trace(), row=1, col=1)
    for ld, r, m, c in zip(LDS, rs, ms, COLS):
        i = min(int(round(t / tk.DT)), len(r["t"]) - 1)
        fig.add_trace(go.Scatter(x=r["x"][:i + 1], y=r["y"][:i + 1], mode="lines", line=dict(color=c, width=3),
                                 showlegend=False), row=1, col=1)
        for tr in car_traces(r["x"][i], r["y"][i], r["th"][i], r["delta"][i], c, body=False):
            fig.add_trace(tr, row=1, col=1)
        name = label(ld, m, lag) if last else f"look-ahead {ld:.0f} m"
        fig.add_trace(go.Scatter(x=r["s"][:i + 1], y=r["e"][:i + 1], mode="lines", line=dict(color=c, width=3),
                                 name=name), row=2, col=1)
    for s0 in (tk.S1, tk.S2):
        fig.add_vline(x=s0, line=dict(color=GREY, dash="dot", width=1.5), row=2, col=1)
    fig.add_hline(y=0, line=dict(color="black", width=1), row=2, col=1)
    small = "<span style='font-size:19px'>"
    head = (f"look-ahead 2, 4 and 8 m at {v:.0f} m/s, " + ("steering lags 0.4 s" if lag else "no steering lag"))
    sub = "the whole course" if last else f"t = {t:.1f} s"
    fig.update_layout(template="simple_white", font=FONT, width=900, height=1150, margin=dict(l=90, r=30, t=110, b=70),
                      title=dict(x=0.5, y=0.975, yanchor="top", text=f"{head}<br>{small}{sub}</span>"),
                      legend=dict(x=0.02, y=0.985, font=dict(size=18), bgcolor="rgba(255,255,255,0.9)"))
    fig.update_xaxes(title_text="x (m)", range=[-2, 24], dtick=5, row=1, col=1)
    fig.update_yaxes(title_text="y (m)", range=[-3, 23], dtick=5, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(title_text="distance along the course (m)", range=[0, 36.5], dtick=5, row=2, col=1)
    fig.update_yaxes(title_text="lateral error (m)", range=[-1.4, 1.1], dtick=0.25, row=2, col=1)
    return fig


for lag, v, dt_frame, out in ((False, tk.V_BASE, 0.5, "ld_sweep"), (True, tk.V_FAST, 0.2, "ld_sweep_lag")):
    rs, ms = runs(v, 0.4 if lag else 0.0)
    if lag:
        assert abs(ms[0]["over"] - 0.832) < 0.001 and abs(ms[0]["arc_peak"] + 1.254) < 0.001
        assert abs(ms[1]["over"] - 0.256) < 0.001 and ms[2]["over"] == 0 and abs(ms[2]["arc_peak"] - 0.559) < 0.001
    else:
        assert abs(ms[0]["reach"] - 4.02) < 0.01 and abs(ms[0]["steer_max"] - 26.57) < 0.01
        assert abs(ms[1]["reach"] - 7.36) < 0.01 and abs(ms[2]["arc_peak"] - 0.850) < 0.001
    t_end = max(r["t"][-1] for r in rs)
    ts = list(np.arange(0, t_end, dt_frame)) + [t_end]
    figs = [frame(rs, ms, t, lag, v) for t in ts] + [frame(rs, ms, t_end, lag, v, last=True)]
    n = len(figs)
    make_gif(figs, here / out, fps=4, holds=[6] + [1] * (n - 2) + [16], keys=[0, n // 3, 2 * n // 3, n - 1], cols=2,
             width=850)
