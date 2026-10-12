"""Stanley's gain k swept at 5 m/s with steering that lags 0.4 s (RO-071's real steering motor), from 1.0 m left of the
course; one frame per 0.2 s. k = 0.5 (purple), 1 (blue), 2.5 (orange) and 5 per s (red). Top: the paths of the front
axles. Bottom: the front axle's lateral error against time. On the first straight a small gain returns slowly; a
large one returns sooner but swings past the line: 0.24 m for k = 2.5 and 0.46 m for k = 5. On the arc every gain
swings, by 0.13 to 0.48 m.
Run: python k_sweep.py -> k_sweep.gif, k_sweep_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import trackkit as tk
from cardraw import course_trace
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, RED, make_gif

here = Path(__file__).parent
KS, COLS = (0.5, 1.0, 2.5, 5.0), (PURPLE, BLUE, ORANGE, RED)
runs = [tk.simulate(tk.law("stanley", k=k), v=tk.V_FAST, tau=0.4) for k in KS]
ms = [tk.metrics(r, "front") for r in runs]
assert abs(ms[0]["reach"] - 13.06) < 0.01 and abs(ms[1]["reach"] - 10.66) < 0.01
assert abs(ms[2]["over"] - 0.237) < 1e-3 and abs(ms[3]["over"] - 0.458) < 1e-3 and ms[1]["over"] == 0


def label(k, m):
    past = f"{m['over']:.2f} m past" if m["over"] > 0 else "none past"
    return f"k = {k} per s: within 0.1 m after {m['reach']:.1f} m, {past}"


def frame(t, last=False):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.58, 0.42], vertical_spacing=0.09)
    fig.add_trace(course_trace(), row=1, col=1)
    for k, r, m, c in zip(KS, runs, ms, COLS):
        i = min(int(round(t / tk.DT)), len(r["t"]) - 1)
        fig.add_trace(go.Scatter(x=r["fx"][:i + 1], y=r["fy"][:i + 1], mode="lines", line=dict(color=c, width=3),
                                 showlegend=False), row=1, col=1)
        fig.add_trace(go.Scatter(x=[r["fx"][i]], y=[r["fy"][i]], mode="markers",
                                 marker=dict(color=c, size=11, line=dict(color="black", width=1)), showlegend=False),
                      row=1, col=1)
        fig.add_trace(go.Scatter(x=r["t"][:i + 1], y=r["ef"][:i + 1], mode="lines", line=dict(color=c, width=3),
                                 name=label(k, m) if last else f"k = {k} per s"), row=2, col=1)
    fig.add_hline(y=0, line=dict(color="black", width=1), row=2, col=1)
    small = "<span style='font-size:19px'>"
    sub = "the whole course" if last else f"t = {t:.1f} s"
    fig.update_layout(template="simple_white", font=FONT, width=900, height=1150, margin=dict(l=90, r=30, t=110, b=70),
                      title=dict(x=0.5, y=0.975, yanchor="top",
                                 text=f"Stanley's gain k at 5 m/s, steering lagging 0.4 s<br>{small}{sub}</span>"),
                      legend=dict(x=0.02, y=0.93, font=dict(size=17), bgcolor="rgba(255,255,255,0.9)"))
    fig.update_xaxes(title_text="x (m)", range=[-1, 25], dtick=5, row=1, col=1)
    fig.update_yaxes(title_text="y (m)", range=[-2, 24], dtick=5, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(title_text="time (s)", range=[0, 7.2], dtick=1, row=2, col=1)
    fig.update_yaxes(title_text="front-axle lateral error (m)", range=[-0.6, 1.05], dtick=0.25, row=2, col=1)
    return fig


t_end = max(r["t"][-1] for r in runs)
ts = list(np.round(np.arange(0, t_end, 0.2), 2)) + [t_end]
figs = [frame(t) for t in ts] + [frame(t_end, last=True)]
n = len(figs)
make_gif(figs, here / "k_sweep", fps=4, holds=[6] + [1] * (n - 2) + [16], keys=[0, 6, 14, n - 1], cols=2, width=850)
