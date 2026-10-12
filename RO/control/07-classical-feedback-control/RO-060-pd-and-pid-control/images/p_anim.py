"""Animation: why proportional control swings. The torque is 0.2 N m per rad of heading error (also 0.1, faint). Top:
the heading. Middle: the turn rate. Bottom: the torque. At 1.11 s the heading reaches 45 degrees: the error and so the
torque are 0, but the robot is turning at 1.12 rad/s, so it carries on to 90.5 degrees; the torque, now negative,
slows it and sends it back. The smaller gain swings more slowly (peak at 3.14 s instead of 2.22 s), not less far.
One frame per 0.2 s for 6.6 s; the last frame holds. Run -> p_anim.gif, p_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import headkit as h
from gifkit import FONT, GREY, PURPLE, RED, make_gif

here = Path(__file__).parent
T = 6.6
A, B = h.run(T, kp=0.2), h.run(T, kp=0.1)
kc = int(np.argmax(A["th"] >= h.TH_REF))
assert abs(A["t"][kc] - 1.11) < 1e-9 and round(A["w"][kc], 2) == 1.12 and abs(A["tau"][kc]) < 1e-3
assert abs(h.peaks(B)[0][0] - 3.14) < 1e-9 and abs(h.peaks(A)[0][0] - 2.22) < 1e-9


def frame(t, final=False):
    k = int(round(t / h.DT))
    fig = make_subplots(rows=3, cols=1, vertical_spacing=0.07, shared_xaxes=True,
                        subplot_titles=["heading θ", "turn rate ω", "torque τ = Kp × error"])
    for run, op, name in ((B, 0.35, "Kp = 0.1 N m per rad"), (A, 1.0, "Kp = 0.2 N m per rad")):
        tt = run["t"][:k + 1]
        for row, y, show in ((1, np.degrees(run["th"][:k + 1]), True), (2, run["w"][:k + 1], False),
                             (3, run["tau"][:k + 1], False)):
            fig.add_trace(go.Scatter(x=tt, y=y, mode="lines", opacity=op, showlegend=show, name=name,
                                     line=dict(color=RED if row != 2 else PURPLE, width=4)), row=row, col=1)
    fig.add_hline(y=45, line=dict(color=GREY, width=2, dash="dash"), row=1, col=1)
    for row in (2, 3):
        fig.add_hline(y=0, line=dict(color=GREY, width=1), row=row, col=1)
    if t >= 1.11:
        tc = A["t"][kc]
        fig.add_vline(x=tc, line=dict(color=GREY, width=1.5, dash="dot"))
        fig.add_annotation(x=tc + 0.1, y=20, xanchor="left", showarrow=False, text="at 45°: error 0", font=dict(
            size=17, color=GREY), row=1, col=1)
        fig.add_annotation(x=tc, y=A["w"][kc], text="still turning at 1.12 rad/s", showarrow=True, ax=95, ay=-12,
                           arrowhead=2, font=dict(size=17, color=PURPLE), bgcolor="rgba(255,255,255,0.85)", row=2, col=1)
        fig.add_annotation(x=tc, y=0, text="torque 0", showarrow=True, ax=50, ay=-30, arrowhead=2,
                           font=dict(size=17, color=RED), row=3, col=1)
    if t >= 2.22:
        fig.add_annotation(x=2.22, y=90.5, text="90.5°", showarrow=True, ax=35, ay=-18, arrowhead=2,
                           font=dict(size=17, color=RED), row=1, col=1)
    fig.update_yaxes(range=[-10, 105], dtick=45, title="degrees", row=1, col=1)
    fig.update_yaxes(range=[-1.4, 1.4], dtick=0.5, title="rad/s", row=2, col=1)
    fig.update_yaxes(range=[-0.2, 0.2], dtick=0.1, title="N m", row=3, col=1)
    fig.update_xaxes(range=[0, T], dtick=1, title="time after the corner (s)", row=3, col=1)
    title = ("proportional control swings: at 45° the torque is 0 but the robot is still turning" if final else
             f"t = {t:.1f} s")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1050, margin=dict(l=90, r=30, t=110, b=70),
                      title=dict(text=title, x=0.5, y=0.975, font=dict(size=21)),
                      legend=dict(x=0.62, y=0.99, font=dict(size=17), bgcolor="rgba(255,255,255,0.85)"))
    for a in fig.layout.annotations[:3]:
        a.font.size = 19
    return fig


times = list(np.round(np.arange(0, T + 0.001, 0.2), 1))
figs = [frame(t) for t in times] + [frame(T, final=True)]
make_gif(figs, here / "p_anim", fps=5, holds=[8] + [2] * (len(times) - 1) + [26],
         keys=[0, 6, 11, len(figs) - 1], cols=2, width=900)
