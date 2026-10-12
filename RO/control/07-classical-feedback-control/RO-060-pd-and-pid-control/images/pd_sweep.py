"""Animation: the derivative gain swept. Kp stays 0.2 N m per rad; Kd grows from 0 to 0.6 N m per rad/s, one value per
frame. Top: the heading over 12 s for this Kd (bold) and the earlier ones (faint). Bottom: the two parts of the torque
for this Kd: the P part (red) pushes towards 45 degrees, the D part (purple) pushes against the turning. Kd = 0 swings
to 92.6 degrees within 12 s; 0.1 overshoots to 58.8; 0.283 reaches 45.0 without passing it and stays within 1 degree
after 4.07 s (near 0.28 the swing past 45 degrees disappears); 0.6 creeps up and needs 10.94 s. The last frame holds those four. Run -> pd_sweep.gif, pd_sweep_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import headkit as h
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, RED, make_gif

here = Path(__file__).parent
T = 12
KDS = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, h.KD, 0.4, 0.5, 0.6]
RUNS = {kd: h.run(T, kd=kd) for kd in KDS}
MARK = {0.0: RED, 0.1: ORANGE, h.KD: BLUE, 0.6: GREEN}
assert round(np.degrees(RUNS[0.0]["th"].max()), 1) == 92.6 and round(np.degrees(RUNS[0.1]["th"].max()), 1) == 58.8
assert round(np.degrees(RUNS[h.KD]["th"].max()), 1) == 45.0 and abs(h.within(RUNS[h.KD]) - 4.07) < 1e-9
assert abs(h.within(h.run(15, kd=0.6)) - 10.94) < 1e-9


def frame(i, final=False):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.62, 0.38], vertical_spacing=0.12,
                        subplot_titles=["heading θ", "the two parts of the torque, for the bold Kd"])
    shown = [kd for kd in KDS if kd in MARK] if final else KDS[:i + 1]
    for kd in shown:
        a = RUNS[kd]
        bold = final or kd == KDS[i]
        col = MARK.get(kd, BLUE) if final else (BLUE if bold else GREY)
        fig.add_trace(go.Scatter(x=a["t"], y=np.degrees(a["th"]), mode="lines", opacity=1 if bold else 0.35,
                                 line=dict(color=col, width=4 if bold else 2), name=f"Kd = {kd:g}",
                                 showlegend=final), row=1, col=1)
    cur = RUNS[h.KD] if final else RUNS[KDS[i]]
    fig.add_trace(go.Scatter(x=cur["t"], y=cur["p"], mode="lines", line=dict(color=RED, width=3),
                             name="P part: Kp × error", showlegend=not final), row=2, col=1)
    fig.add_trace(go.Scatter(x=cur["t"], y=cur["d"], mode="lines", line=dict(color=PURPLE, width=3),
                             name="D part: Kd × rate of change of the error", showlegend=not final), row=2, col=1)
    fig.add_hline(y=45, line=dict(color=GREY, width=2, dash="dash"), row=1, col=1)
    fig.add_hline(y=0, line=dict(color=GREY, width=1), row=2, col=1)
    if not final:
        a = RUNS[KDS[i]]
        w1 = h.within(a)
        msg = (f"Kd = {KDS[i]:g}: highest {np.degrees(a['th'].max()):.1f}°, " +
               (f"within 1° of 45° after {w1:.2f} s" if w1 is not None else "never settles"))
        fig.add_annotation(x=11.8, y=100, xanchor="right", text=msg, showarrow=False, font=dict(size=19, color=BLUE),
                           bgcolor="rgba(255,255,255,0.85)", row=1, col=1)
    fig.update_yaxes(range=[-5, 105], dtick=15, title="heading (°)", row=1, col=1)
    fig.update_yaxes(range=[-0.17, 0.17], dtick=0.05, title="torque (N m)", row=2, col=1)
    fig.update_xaxes(range=[0, T], dtick=1, row=1, col=1)
    fig.update_xaxes(range=[0, T], dtick=1, title="time after the corner (s)", row=2, col=1)
    title = ("near Kd = 0.28 the swing past 45° disappears; more Kd only slows the turn" if final else
             f"Kp = 0.2 N m per rad, Kd = {KDS[i]:g} N m per rad/s")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1050, margin=dict(l=90, r=30, t=110, b=110),
                      title=dict(text=title, x=0.5, y=0.975, font=dict(size=21)),
                      legend=dict(orientation="h", x=0.0, y=-0.1, font=dict(size=17)))
    for a in fig.layout.annotations[:2]:
        a.font.size = 19
    return fig


figs = [frame(i) for i in range(len(KDS))] + [frame(len(KDS) - 1, final=True)]
make_gif(figs, here / "pd_sweep", fps=2, holds=[4] + [3] * (len(KDS) - 1) + [12],
         keys=[0, 2, 6, len(figs) - 1], cols=2, width=900)
