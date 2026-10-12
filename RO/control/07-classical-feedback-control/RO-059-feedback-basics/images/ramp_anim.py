"""Opening animation: two copies of the robot cruise at 0.5 m/s on the flat and reach a ramp (1 cm rise per metre) at
x = 2 m, t = 4 s. Top: open loop, the fixed 1 N of the flat-floor test. Middle: closed loop, 1 N plus 20 N for every
m/s of measured error. Bottom: their speeds over time. One frame per second for 30 s; the last frame holds:
open loop 0.108 m/s, closed loop 0.464 m/s. No sensor noise in this run. The slope is drawn 20 times steeper than it
is and the robots 2 times larger, so that both can be seen. Run -> ramp_anim.gif, ramp_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import speedkit as s
from gifkit import BLUE, FONT, GREY, RED, make_gif

here = Path(__file__).parent
T = 30
OL, CL = s.run(T, closed=False), s.run(T, closed=True)
assert round(OL["v"][-1], 3) == 0.108 and round(CL["v"][-1], 3) == 0.464
assert abs(OL["t"][np.argmax(OL["d"] > 0)] - 4.0) < 1e-9
EXAG = 20                                            # drawn slope = 20 x true slope
X_END = 15.0


def ground_y(x):
    return np.where(x < s.X_RAMP, 0.0, (x - s.X_RAMP) * s.RISE * EXAG)


def robot(fig, x, color, row):
    """A side view of the robot at x: a box on two wheels, tilted with the drawn ground."""
    ang = 0.0 if x < s.X_RAMP else np.arctan(s.RISE * EXAG)
    c, si = np.cos(ang), np.sin(ang)
    gx, gy = x, float(ground_y(np.array(x)))
    def tr(px, py):
        return gx + c * px - si * py, gy + si * px + c * py
    body = [(-0.5, 0.2), (0.5, 0.2), (0.5, 0.75), (-0.5, 0.75), (-0.5, 0.2)]          # 1 m long: 2 x true size
    bx, by = zip(*[tr(*p) for p in body])
    fig.add_trace(go.Scatter(x=bx, y=by, mode="lines", fill="toself", line=dict(color=color, width=2),
                             fillcolor=color, opacity=0.85, showlegend=False, hoverinfo="skip"), row=row, col=1)
    for wx in (-0.3, 0.3):
        th = np.linspace(0, 2 * np.pi, 30)
        cx, cy = zip(*[tr(wx + 0.17 * np.cos(a), 0.17 + 0.17 * np.sin(a)) for a in th])
        fig.add_trace(go.Scatter(x=cx, y=cy, mode="lines", fill="toself", line=dict(color="black", width=1),
                                 fillcolor="black", showlegend=False, hoverinfo="skip"), row=row, col=1)


def frame(t, final=False):
    k = int(round(t / s.DT))
    fig = make_subplots(rows=3, cols=1, row_heights=[0.25, 0.25, 0.5], vertical_spacing=0.07,
                        subplot_titles=["open loop: always the 1 N of the flat-floor test",
                                        "closed loop: 1 N + 20 N for every m/s too slow",
                                        ""])
    xs = np.linspace(-0.5, X_END, 200)
    for row, run, col in ((1, OL, RED), (2, CL, BLUE)):
        fig.add_trace(go.Scatter(x=xs, y=ground_y(xs), mode="lines", line=dict(color=GREY, width=3),
                                 showlegend=False, hoverinfo="skip"), row=row, col=1)
        robot(fig, run["x"][k], col, row)
        x = run["x"][k]
        fig.add_annotation(x=x, y=float(ground_y(np.array(x))) + 1.2, text=f"<b>{run['v'][k]:.3f} m/s</b>",
                           showarrow=False, font=dict(size=19, color=col), row=row, col=1)
        fig.update_xaxes(range=[-0.6, X_END + 0.2], constrain="domain", showticklabels=row == 2,
                         ticksuffix=" m" if row == 2 else None, row=row, col=1)
        fig.update_yaxes(range=[-0.25, 4.0], visible=False, scaleanchor="x" if row == 1 else "x2", scaleratio=1,
                         constrain="domain", row=row, col=1)
    fig.add_annotation(x=6.5, y=3.7, text="ramp: rises 1 cm per metre (drawn 20 times steeper; robots 2 times larger)", showarrow=False,
                       font=dict(size=16, color=GREY), row=1, col=1)
    # speeds
    for run, col, name in ((OL, RED, "open loop"), (CL, BLUE, "closed loop")):
        fig.add_trace(go.Scatter(x=run["t"][:k + 1], y=run["v"][:k + 1], mode="lines", line=dict(color=col, width=4,
                                 dash="dash" if col == RED else None), name=name), row=3, col=1)
        fig.add_trace(go.Scatter(x=[run["t"][k]], y=[run["v"][k]], mode="markers", marker=dict(color=col, size=12),
                                 showlegend=False), row=3, col=1)
    fig.add_hline(y=0.5, line=dict(color=GREY, width=2, dash="dot"), row=3, col=1)
    fig.add_vline(x=4, line=dict(color=GREY, width=1.5, dash="dash"), row=3, col=1)
    fig.add_annotation(x=4.2, y=0.06, text="both reach the ramp at 4 s", xanchor="left", showarrow=False,
                       font=dict(size=17, color=GREY), row=3, col=1)
    fig.add_annotation(x=0.2, y=0.535, text="wanted 0.5 m/s", xanchor="left", showarrow=False,
                       font=dict(size=17, color=GREY), row=3, col=1)
    if final:
        fig.add_annotation(x=29.5, y=OL["v"][-1] + 0.05, text="open loop: 0.108 m/s", xanchor="right",
                           showarrow=False, font=dict(size=19, color=RED), row=3, col=1)
        fig.add_annotation(x=29.5, y=CL["v"][-1] - 0.06, text="closed loop: 0.464 m/s", xanchor="right",
                           showarrow=False, font=dict(size=19, color=BLUE), row=3, col=1)
    fig.update_xaxes(range=[0, T], dtick=5, title="time (s)", row=3, col=1)
    fig.update_yaxes(range=[0, 0.6], dtick=0.1, title="speed (m/s)", row=3, col=1)
    title = ("after 30 s: the ramp cut the open-loop speed to 0.108 m/s, the closed loop holds 0.464 m/s" if final
             else f"t = {t:.0f} s")
    fig.update_layout(template="simple_white", font=FONT, width=1100, height=1150,
                      margin=dict(l=90, r=30, t=110, b=70), title=dict(text=title, x=0.5, y=0.975, font=dict(size=21)),
                      legend=dict(x=0.72, y=0.40, font=dict(size=18), bgcolor="rgba(255,255,255,0.85)"))
    for a in fig.layout.annotations[:2]:
        a.font.size = 19
    return fig


times = list(range(0, T + 1))
figs = [frame(t) for t in times] + [frame(T, final=True)]
make_gif(figs, here / "ramp_anim", fps=4, holds=[8] + [2] * (len(times) - 1) + [24], keys=[0, 4, 8, len(figs) - 1],
         cols=2, width=900)
