"""Animation: the integral at work. The right gearbox drags, a steady torque of 0.02 N m turning the robot right. Two
copies take the corner: PD (Kp 0.2, Kd 0.283; blue) and PID (the same plus Ki 0.05; green). Top: the floor, seen from
above. Middle: the heading. Bottom: the PID's integral part, Ki times the running sum of the error, built up one 10 ms
step at a time, against the 0.02 N m it must cancel. PD stops at 39.27 degrees (5.73 degrees short); PID passes 45 to
51.78 degrees at 4.74 s (its sum has grown to 0.98 rad s, more than the 0.4 it needs), then settles at 45 degrees with
the integral part at exactly 0.02 N m. One frame per 0.25 s for 15 s; the last frame holds.
Run -> pid_anim.gif, pid_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import headkit as h
from gifkit import BLUE, FONT, GREEN, GREY, make_gif
from robotdraw import robot

here = Path(__file__).parent
T = 15
PD = h.run(T, kd=h.KD, tau_d=h.TAU_DRAG)
PID = h.run(T, kd=h.KD, ki=h.KI, tau_d=h.TAU_DRAG)
LONG = h.run(30, kd=h.KD, ki=h.KI, tau_d=h.TAU_DRAG)
tp, pk = h.peaks(PID)
assert round(np.degrees(PD["th"][-1]), 2) == 39.27 and round(np.degrees(pk[0]), 2) == 51.78 and abs(tp[0] - 4.74) < 1e-9
assert round(PID["integ"][int(round(3 / h.DT))], 2) == 0.98 and round(LONG["i"][-1], 4) == 0.02


def frame(t, final=False):
    k = int(round(t / h.DT))
    fig = make_subplots(rows=3, cols=1, row_heights=[0.42, 0.32, 0.26], vertical_spacing=0.08,
                        subplot_titles=["the floor, seen from above", "heading θ",
                                        "PID's integral part: Ki × (sum of error × 0.01 s)"])
    L = np.array([0, 7])
    fig.add_trace(go.Scatter(x=L * np.cos(h.TH_REF), y=L * np.sin(h.TH_REF), mode="lines", showlegend=False,
                             line=dict(color=GREY, width=3, dash="dash")), row=1, col=1)
    fig.add_trace(go.Scatter(x=[-0.7, 0], y=[0, 0], mode="lines", line=dict(color=GREY, width=3), showlegend=False),
                  row=1, col=1)
    for run, col, name in ((PD, BLUE, "PD"), (PID, GREEN, "PID")):
        fig.add_trace(go.Scatter(x=run["x"][:k + 1], y=run["y"][:k + 1], mode="lines", line=dict(color=col, width=4),
                                 name=f"{name}: {np.degrees(run['th'][k]):.2f}°"), row=1, col=1)
        for tr in robot((run["x"][k], run["y"][k], run["th"][k]), scale=1.6, color=col):
            fig.add_trace(tr.update(showlegend=False), row=1, col=1)
        fig.add_trace(go.Scatter(x=run["t"][:k + 1], y=np.degrees(run["th"][:k + 1]), mode="lines",
                                 line=dict(color=col, width=4), showlegend=False), row=2, col=1)
    fig.add_hline(y=45, line=dict(color=GREY, width=2, dash="dash"), row=2, col=1)
    fig.add_trace(go.Scatter(x=PID["t"][:k + 1], y=PID["i"][:k + 1], mode="lines", fill="tozeroy",
                             fillcolor="rgba(84,162,75,0.25)", line=dict(color=GREEN, width=3), showlegend=False),
                  row=3, col=1)
    fig.add_hline(y=0.02, line=dict(color=GREY, width=2, dash="dash"), row=3, col=1)
    fig.add_annotation(x=14.8, y=0.008, xanchor="right", text="needed to cancel the drag: 0.02 N m", showarrow=False,
                       font=dict(size=16, color=GREY), row=3, col=1)
    fig.add_annotation(x=PID["t"][k], y=PID["i"][k], text=f"sum {PID['integ'][k]:.2f} rad s → {PID['i'][k]:.4f} N m",
                       showarrow=True, ax=-10 if t > 8 else 60, ay=-28, arrowhead=2, xanchor="right" if t > 8 else "left",
                       font=dict(size=17, color=GREEN), bgcolor="rgba(255,255,255,0.85)", row=3, col=1)
    fig.update_xaxes(range=[-0.8, 6.2], dtick=1, ticksuffix=" m", constrain="domain", row=1, col=1)
    fig.update_yaxes(range=[-0.5, 5.4], dtick=1, ticksuffix=" m", scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(range=[0, T], dtick=1, row=2, col=1)
    fig.update_yaxes(range=[0, 60], dtick=15, title="heading (°)", row=2, col=1)
    fig.update_xaxes(range=[0, T], dtick=1, title="time after the corner (s)", row=3, col=1)
    fig.update_yaxes(range=[0, 0.06], dtick=0.02, title="torque (N m)", row=3, col=1)
    title = ("PD stops 5.73° short; the integral grows until it cancels the drag, and PID settles at 45°" if final else
             f"a dragging gearbox (0.02 N m to the right): t = {t:.2f} s")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1300, margin=dict(l=90, r=30, t=110, b=70),
                      title=dict(text=title, x=0.5, y=0.98, font=dict(size=21)),
                      legend=dict(x=0.02, y=0.99, font=dict(size=18), bgcolor="rgba(255,255,255,0.85)"))
    for a in fig.layout.annotations[:3]:
        a.font.size = 19
    return fig


times = list(np.round(np.arange(0, T + 0.001, 0.25), 2))
figs = [frame(t) for t in times] + [frame(T, final=True)]
make_gif(figs, here / "pid_anim", fps=6, holds=[8] + [2] * (len(times) - 1) + [30],
         keys=[0, 12, 19, len(figs) - 1], cols=2, width=900)
