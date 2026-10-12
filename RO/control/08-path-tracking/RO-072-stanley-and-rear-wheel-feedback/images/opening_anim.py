"""What still breaks after pure pursuit: the car of RO-071 with its 4 m look-ahead at 2 m/s (grey) on the course,
one frame per 0.5 s, with its rear axle's lateral error below. It runs 0.12 m inside the arc and 0.17 m wide after it.
The last frame adds Stanley (orange; error at its front axle) and rear-wheel feedback (blue; error at its rear axle),
which follow the arc: in its middle 0.004 m and 0.000 m, after it 0.005 m and 0.005 m.
Run: python opening_anim.py -> opening_anim.gif, opening_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import trackkit as tk
from cardraw import car_traces, course_trace
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif

here = Path(__file__).parent
pp = tk.simulate(tk.law("pp", ld=4.0), v=tk.V_BASE)
st = tk.simulate(tk.law("stanley"), v=tk.V_BASE)
rw = tk.simulate(tk.law("rear"), v=tk.V_BASE)
mp, ms, mr = tk.metrics(pp), tk.metrics(st, "front"), tk.metrics(rw)
assert abs(mp["arc_peak"] - 0.120) < 1e-3 and abs(mp["exit_peak"] + 0.166) < 1e-3
assert abs(ms["arc_mid"] - 0.0040) < 1e-4 and abs(ms["exit_peak"] - 0.005) < 1e-3
assert abs(mr["arc_mid"]) < 5e-4 and abs(mr["exit_peak"] - 0.005) < 1e-3
DARK = "#4D4D4D"


def frame(i, last=False):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.66, 0.34], vertical_spacing=0.09)
    fig.add_trace(course_trace(), row=1, col=1)
    fig.add_trace(go.Scatter(x=pp["x"][:i + 1], y=pp["y"][:i + 1], mode="lines", line=dict(color=DARK, width=3),
                             showlegend=False), row=1, col=1)
    for t in car_traces(pp["x"][i], pp["y"][i], pp["th"][i], pp["delta"][i], DARK):
        fig.add_trace(t, row=1, col=1)
    name = (f"pure pursuit, rear axle: {mp['arc_peak']:.2f} m inside the arc, {-mp['exit_peak']:.2f} m wide after"
            if last else "pure pursuit, 4 m look-ahead (rear axle)")
    fig.add_trace(go.Scatter(x=pp["s"][:i + 1], y=pp["e"][:i + 1], mode="lines", line=dict(color=DARK, width=3),
                             name=name), row=2, col=1)
    if last:
        for r, c, s_, e_, lab in ((st, ORANGE, st["sf"], st["ef"],
                                   f"Stanley, front axle: {ms['arc_mid']:.3f} m in the middle of the arc"),
                                  (rw, BLUE, rw["s"], rw["e"],
                                   f"rear-wheel feedback, rear axle: {abs(mr['arc_mid']):.3f} m in the middle")):
            fig.add_trace(go.Scatter(x=r["x"], y=r["y"], mode="lines", line=dict(color=c, width=3), showlegend=False),
                          row=1, col=1)
            fig.add_trace(go.Scatter(x=s_, y=e_, mode="lines", line=dict(color=c, width=3), name=lab), row=2, col=1)
    for s0 in (tk.S1, tk.S2):
        fig.add_vline(x=s0, line=dict(color=GREY, dash="dot", width=1.5), row=2, col=1)
    fig.add_annotation(x=(tk.S1 + tk.S2) / 2, y=0.95, text="arc", showarrow=False, font=dict(size=18, color=GREY),
                       row=2, col=1)
    fig.add_hline(y=0, line=dict(color="black", width=1), row=2, col=1)
    small = "<span style='font-size:19px'>"
    if last:
        title = f"steering from the errors at the car's own axles<br>{small}Stanley and rear-wheel feedback follow the arc</span>"
    else:
        title = (f"pure pursuit, 4 m look-ahead, t = {pp['t'][i]:.1f} s<br>{small}course distance {pp['s'][i]:.1f} m, "
                 f"lateral error {pp['e'][i]:+.2f} m (+ = left)</span>")
    fig.update_layout(template="simple_white", font=FONT, width=900, height=1150, margin=dict(l=90, r=30, t=120, b=70),
                      title=dict(x=0.5, y=0.975, yanchor="top", text=title),
                      legend=dict(x=0.01, y=0.985, font=dict(size=16), bgcolor="rgba(255,255,255,0.9)"))
    fig.update_xaxes(title_text="x (m)", range=[-2, 24], dtick=5, row=1, col=1)
    fig.update_yaxes(title_text="y (m)", range=[-3, 24], dtick=5, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(title_text="distance along the course (m)", range=[0, 36.5], dtick=5, row=2, col=1)
    fig.update_yaxes(title_text="lateral error (m)", range=[-0.3, 1.05], dtick=0.25, row=2, col=1)
    return fig


idx = list(range(0, len(pp["t"]), 50)) + [len(pp["t"]) - 1]
figs = [frame(i) for i in idx] + [frame(idx[-1], last=True)]
make_gif(figs, here / "opening_anim", fps=4, holds=[6] + [1] * (len(idx) - 1) + [16], keys=[0, 12, 28, len(figs) - 1],
         cols=2, width=850)
