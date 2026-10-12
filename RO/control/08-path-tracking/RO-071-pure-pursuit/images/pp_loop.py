"""Pure pursuit as a loop: the car at 2 m/s with a 4 m look-ahead, one frame every 0.5 s (every tenth tick of the
20 Hz loop). Each frame draws the look-ahead circle around the rear axle, the look-ahead point where it meets the
course ahead, and the arc to that point, tangent to the heading, that the car is told to drive until the next tick.
Below: the offset along the course. Last frame: within 0.1 m after 7.4 m; 0.12 m inside on the arc; 0.17 m wide after
the exit.
Run: python pp_loop.py -> pp_loop.gif, pp_loop_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import trackkit as tk
from cardraw import arc_length_to, arc_points, car_traces, circle_points, course_trace
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, make_gif

here = Path(__file__).parent
run = tk.simulate(tk.law("pp", ld=4.0), v=tk.V_BASE)
m = tk.metrics(run)
ticks = run["ticks"]
assert abs(m["reach"] - 7.36) < 0.01 and abs(m["arc_peak"] - 0.120) < 0.001 and abs(m["exit_peak"] + 0.166) < 0.001
assert abs(np.degrees(ticks[0]["delta_cmd"]) + 17.35) < 0.01 and abs(1 / ticks[0]["kappa"] + 8.0) < 1e-3


def frame(k, last=False):
    tk_ = ticks[k]
    i = int(round(tk_["t"] / tk.DT))
    fig = make_subplots(rows=2, cols=1, row_heights=[0.68, 0.32], vertical_spacing=0.09)
    fig.add_trace(course_trace(), row=1, col=1)
    fig.add_trace(go.Scatter(x=run["x"][:i + 1], y=run["y"][:i + 1], mode="lines", line=dict(color=BLUE, width=3),
                             name="path of the rear axle"), row=1, col=1)
    if not last:
        cx, cy = circle_points(tk_["x"], tk_["y"], tk_["ld"])
        fig.add_trace(go.Scatter(x=cx, y=cy, mode="lines", line=dict(color=ORANGE, width=2, dash="dash"),
                                 name="look-ahead circle, 4 m"), row=1, col=1)
        fig.add_trace(go.Scatter(x=[tk_["gx"]], y=[tk_["gy"]], mode="markers",
                                 marker=dict(color=ORANGE, size=15, line=dict(color="black", width=1)),
                                 name="look-ahead point"), row=1, col=1)
    for t in car_traces(run["x"][i], run["y"][i], run["th"][i], run["delta"][i], BLUE):
        fig.add_trace(t, row=1, col=1)
    if not last:
        ax, ay = arc_points(tk_["x"], tk_["y"], tk_["th"], tk_["kappa"], arc_length_to(tk_["kappa"], tk_["ld"]))
        fig.add_trace(go.Scatter(x=ax, y=ay, mode="lines", line=dict(color=GREEN, width=5),
                                 name="arc to the look-ahead point"), row=1, col=1)
        fig.add_trace(go.Scatter(x=[tk_["gx"]], y=[tk_["gy"]], mode="markers", showlegend=False,
                                 marker=dict(color=ORANGE, size=15, line=dict(color="black", width=1))), row=1, col=1)
    fig.add_trace(go.Scatter(x=run["s"][:i + 1], y=run["e"][:i + 1], mode="lines", line=dict(color=BLUE, width=3),
                             showlegend=False), row=2, col=1)
    for s0 in (tk.S1, tk.S2):
        fig.add_vline(x=s0, line=dict(color=GREY, dash="dot", width=1.5), row=2, col=1)
    fig.add_annotation(x=(tk.S1 + tk.S2) / 2, y=1.05, text="arc", showarrow=False, font=dict(size=18, color=GREY),
                       row=2, col=1)
    fig.add_hline(y=0, line=dict(color="black", width=1), row=2, col=1)
    small = "<span style='font-size:19px'>"
    if last:
        title = (f"pure pursuit, 4 m look-ahead, the whole course<br>{small}within 0.1 m after {m['reach']:.1f} m; "
                 f"on the arc at most {m['arc_peak']:.2f} m inside; {-m['exit_peak']:.2f} m wide after it</span>")
    else:
        R = 1 / tk_["kappa"]
        side = "left" if R > 0 else "right"
        rtxt = f"arc radius {abs(R):.1f} m, centre to the {side}" if abs(R) < 200 else "arc nearly straight"
        title = (f"t = {tk_['t']:.1f} s: chase the point 4 m ahead<br>{small}{rtxt}; steering "
                 f"{np.degrees(tk_['delta_cmd']):+.1f}°; lateral error {run['e'][i]:+.2f} m</span>")
    fig.update_layout(template="simple_white", font=FONT, width=900, height=1150, margin=dict(l=90, r=30, t=120, b=70),
                      title=dict(x=0.5, y=0.975, yanchor="top", text=title),
                      legend=dict(x=0.02, y=0.985, font=dict(size=18), bgcolor="rgba(255,255,255,0.85)"))
    fig.update_xaxes(title_text="x (m)", range=[-2, 24], dtick=5, row=1, col=1)
    fig.update_yaxes(title_text="y (m)", range=[-3, 24], dtick=5, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(title_text="distance along the course (m)", range=[0, 36.5], dtick=5, row=2, col=1)
    fig.update_yaxes(title_text="lateral error (m)", range=[-0.4, 1.15], dtick=0.25, row=2, col=1)
    return fig


ks = list(range(0, len(ticks), 10)) + [len(ticks) - 1]
figs = [frame(k) for k in ks] + [frame(ks[-1], last=True)]
make_gif(figs, here / "pp_loop", fps=4, holds=[6] + [1] * (len(ks) - 1) + [16], keys=[0, 6, 20, len(figs) - 1],
         cols=2, width=850)
