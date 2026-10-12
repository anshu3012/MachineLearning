"""Rear-wheel feedback on the course at 2 m/s from 1.0 m left of the line; one frame per 0.5 s. Top: the car and its
rear-axle path. Middle: the turn rate it asks for, as its three parts at the latest tick: the path-curvature part
(v kappa cos(th_e) / (1 - kappa e)), the heading part (-k_th |v| th_e) and the lateral part
(-k_e v (sin(th_e)/th_e) e), and their sum. Bottom: the rear axle's lateral error. Last frame: within 0.1 m after
4.1 m, 0.04 m past the line, 0.000 m in the middle of the arc.
Run: python rear_anim.py -> rear_anim.gif, rear_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import trackkit as tk
from cardraw import car_traces, course_trace
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, make_gif

here = Path(__file__).parent
run = tk.simulate(tk.law("rear"), v=tk.V_BASE)
m = tk.metrics(run)
assert abs(m["reach"] - 4.09) < 0.01 and abs(m["over"] - 0.039) < 1e-3 and abs(m["arc_mid"]) < 5e-4
ticks = run["ticks"]
PARTS = (("path curvature", "ff", GREEN), ("heading", "fb_h", PURPLE), ("lateral", "fb_e", ORANGE),
         ("total", "omega", BLUE))


def frame(k, last=False):
    tick = ticks[k]
    i = int(round(tick["t"] / tk.DT))
    fig = make_subplots(rows=3, cols=1, row_heights=[0.55, 0.17, 0.28], vertical_spacing=0.07)
    fig.add_trace(course_trace(), row=1, col=1)
    fig.add_trace(go.Scatter(x=run["x"][:i + 1], y=run["y"][:i + 1], mode="lines", line=dict(color=BLUE, width=3),
                             showlegend=False), row=1, col=1)
    for tr in car_traces(run["x"][i], run["y"][i], run["th"][i], run["delta"][i], BLUE):
        fig.add_trace(tr, row=1, col=1)
    names = [p[0] for p in PARTS]
    vals = [tick[p[1]] for p in PARTS]
    fig.add_trace(go.Bar(x=vals, y=names, orientation="h", marker=dict(color=[p[2] for p in PARTS]),
                         text=[f"{v:+.2f}" if abs(v) >= 0.005 else "0.00" for v in vals], textposition="outside", textfont=dict(size=17),
                         showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=run["s"][:i + 1], y=run["e"][:i + 1], mode="lines", line=dict(color=BLUE, width=3),
                             showlegend=False), row=3, col=1)
    for s0 in (tk.S1, tk.S2):
        fig.add_vline(x=s0, line=dict(color=GREY, dash="dot", width=1.5), row=3, col=1)
    fig.add_hline(y=0, line=dict(color="black", width=1), row=3, col=1)
    small = "<span style='font-size:19px'>"
    asked = np.degrees(np.arctan(tk.L * tick["omega"] / tk.V_BASE))
    if last:
        title = (f"rear-wheel feedback, the whole course<br>{small}within 0.1 m after {m['reach']:.1f} m, "
                 f"{m['over']:.2f} m past the line, {abs(m['arc_mid']):.3f} m in the middle of the arc</span>")
    else:
        title = (f"rear-wheel feedback at 2 m/s, t = {tick['t']:.1f} s<br>{small}turn rate {tick['omega']:+.2f} rad/s: "
                 f"steering {asked:+.1f}° asked, {np.degrees(tick['delta_cmd']):+.1f}° given</span>")
    fig.update_layout(template="simple_white", font=FONT, width=900, height=1250, margin=dict(l=150, r=30, t=110, b=70),
                      title=dict(x=0.5, y=0.98, yanchor="top", text=title))
    fig.update_xaxes(title_text="x (m)", range=[-2, 24], dtick=5, row=1, col=1)
    fig.update_yaxes(title_text="y (m)", range=[-3, 23], dtick=5, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(title_text="turn rate asked (rad/s)", range=[-1.4, 1.4], dtick=0.5, row=2, col=1)
    fig.update_yaxes(autorange="reversed", row=2, col=1)
    fig.update_xaxes(title_text="distance along the course (m)", range=[0, 36.5], dtick=5, row=3, col=1)
    fig.update_yaxes(title_text="lateral error (m)", range=[-0.2, 1.05], dtick=0.25, row=3, col=1)
    return fig


ks = list(range(0, len(ticks), 10)) + [len(ticks) - 1]
figs = [frame(k) for k in ks] + [frame(ks[-1], last=True)]
n = len(figs)
make_gif(figs, here / "rear_anim", fps=4, holds=[6] + [1] * (n - 2) + [16], keys=[0, 2, 14, n - 1], cols=2, width=850)
