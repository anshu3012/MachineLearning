"""Animation: the integral gain swept, with the dragging gearbox. Kp 0.2 and Kd 0.283 stay; Ki grows from 0 to 0.6, one
value per frame, the heading drawn over 30 s. Ki = 0 stops at 39.27 degrees; 0.05 peaks at 51.78 and is within 1
degree after 10.63 s; 0.2 peaks at 68.73 and needs 14.77 s; 0.4 peaks at 81.28 and needs 38.51 s; at 0.6 every swing is
bigger than the last until the robot spins round. The last frame holds 0, 0.05, 0.2 and 0.6.
Run -> ki_sweep.gif, ki_sweep_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import headkit as h
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
T = 30
KIS = [0.0, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
RUNS = {ki: h.run(40, kd=h.KD, ki=ki, tau_d=h.TAU_DRAG) for ki in KIS}
MARK = {0.0: BLUE, 0.05: GREEN, 0.2: ORANGE, 0.6: RED}
for ki, top, w in ((0.05, 51.78, 10.63), (0.2, 68.73, 14.77), (0.4, 81.28, 38.51)):
    assert round(np.degrees(RUNS[ki]["th"].max()), 2) == top and abs(h.within(RUNS[ki]) - w) < 1e-9
assert np.all(np.diff(h.peaks(RUNS[0.6])[1][:4]) > 0)


def frame(i, final=False):
    fig = go.Figure()
    shown = [ki for ki in KIS if ki in MARK] if final else KIS[:i + 1]
    for ki in shown:
        a = RUNS[ki]
        bold = final or ki == KIS[i]
        col = MARK.get(ki, GREEN) if final else (GREEN if bold else GREY)
        n = int(round(T / h.DT)) + 1
        fig.add_trace(go.Scatter(x=a["t"][:n], y=np.degrees(a["th"][:n]), mode="lines", opacity=1 if bold else 0.35,
                                 line=dict(color=col, width=4 if bold else 2), name=f"Ki = {ki:g}", showlegend=final))
    fig.add_hline(y=45, line=dict(color=GREY, width=2, dash="dash"))
    if not final:
        a = RUNS[KIS[i]]
        w1 = h.within(a)
        msg = (f"Ki = {KIS[i]:g}: highest {np.degrees(a['th'][:3001].max()):.1f}° in 30 s, " +
               (f"within 1° of 45° after {w1:.2f} s" if w1 is not None else
                ("never reaches 45°" if KIS[i] == 0 else "the swings grow")))
        fig.add_annotation(x=29.5, y=132, xanchor="right", text=msg, showarrow=False, font=dict(size=19, color=GREEN),
                           bgcolor="rgba(255,255,255,0.85)")
    fig.update_xaxes(range=[0, T], dtick=5, title="time after the corner (s)")
    fig.update_yaxes(range=[-20, 140], dtick=15, title="heading (°)")
    title = ("a small Ki removes the 5.73° error; larger values swing more; at 0.6 each swing is bigger" if final
             else f"with the dragging gearbox: Kp 0.2, Kd 0.283, Ki = {KIS[i]:g} N m per rad s")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=740, margin=dict(l=90, r=30, t=100, b=120),
                      title=dict(text=title, x=0.5, y=0.96, font=dict(size=20)),
                      legend=dict(orientation="h", x=0.0, y=-0.17, font=dict(size=18)))
    return fig


figs = [frame(i) for i in range(len(KIS))] + [frame(len(KIS) - 1, final=True)]
make_gif(figs, here / "ki_sweep", fps=2, holds=[4] + [3] * (len(KIS) - 1) + [12],
         keys=[0, 2, 8, len(figs) - 1], cols=2, width=900)
