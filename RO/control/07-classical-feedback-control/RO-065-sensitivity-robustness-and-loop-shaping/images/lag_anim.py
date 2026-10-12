"""A lag compensator (s + 0.25)/(s + b2) added to the lead raises the heading loop's gain at low frequencies. Its
zero-to-pole ratio 0.25/b2 grows 1, 2, 4, 6, 10. Top: |L| in dB, lifted below 0.25 rad/s. Middle: |S| in dB, pushed
down at low frequencies while its peak creeps up (1.30 to 1.35). Bottom: the heading error after the 0.02 N m drag
starts at t = 1 s; the final offset falls from 0.096 rad (lead alone) to 0.0096 rad. Grey: the lead alone (from the second frame on).
Run: python lag_anim.py -> lag_anim.gif, lag_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT, GREEN, GREY, RED, make_gif
from loopkit import C_lead, P_head, db, margins, sens_peak
from shapekit import A_LAG, DRAG, sim

here = Path(__file__).parent
rs = [1, 2, 4, 6, 10]
w = np.logspace(-2, 2, 1500)
t = np.arange(0, 30.001, 1e-3)


def loop(r):
    b2 = A_LAG / r
    return b2, (lambda s: C_lead(s) * (s + A_LAG) / (s + b2) * P_head(s))


runs = {r: sim("leadlag", t, dist=DRAG, b_lag=A_LAG / r)[0] for r in rs}
assert abs(runs[1][-1] - 0.096) < 2e-4 and abs(runs[10][-1] - 0.0096) < 3e-4
_, L10 = loop(10)
assert abs(margins(L10)["pm"] - 48.0) < 0.05 and abs(sens_peak(L10)[2] - 1.352) < 2e-3


def frame(r):
    b2, L = loop(r)
    _, Lref = loop(1)
    pm = margins(L)["pm"]
    wms, _, Ms = sens_peak(L)
    off = DRAG * b2 / A_LAG / abs(C_lead(1e-9j))
    fig = make_subplots(rows=3, cols=1, row_heights=[0.3, 0.3, 0.4], vertical_spacing=0.1)
    pairs = [(L, runs[1], GREEN, 5, "the lead alone")] if r == 1 else \
        [(Lref, runs[1], GREY, 3, "lead alone"), (L, runs[r], GREEN, 5, "lead with the lag")]
    for f, th, col, wd, name in pairs:
        fig.add_trace(go.Scatter(x=w, y=db(f(1j * w)), line=dict(color=col, width=wd), name=name), 1, 1)
        fig.add_trace(go.Scatter(x=w, y=db(1 / (1 + f(1j * w))), line=dict(color=col, width=wd), showlegend=False), 2, 1)
        fig.add_trace(go.Scatter(x=t[::20], y=th[::20], line=dict(color=col, width=wd), showlegend=False), 3, 1)
    fig.add_trace(go.Scatter(x=[wms], y=[db(Ms)], mode="markers", marker=dict(color=RED, size=12), showlegend=False),
                  2, 1)
    fig.add_annotation(x=np.log10(wms), y=db(Ms), text=f"Ms = {Ms:.3f}", ax=80, ay=-25, font=dict(size=18, color=RED),
                       arrowcolor=RED, row=2, col=1)
    fig.add_annotation(x=30, y=off, text=f"offset {off:.4f} rad", ax=-90, ay=-45, font=dict(size=18, color=GREEN),
                       arrowcolor=GREEN, row=3, col=1)
    fig.add_hline(y=0, line=dict(color=GREY, width=1.5, dash="dash"), row=1, col=1)
    fig.add_hline(y=0, line=dict(color=GREY, width=1.5, dash="dash"), row=2, col=1)
    for row in (1, 2):
        fig.update_xaxes(type="log", range=[-2, 2], title_text="ω (rad/s)", row=row, col=1)
    fig.update_yaxes(title_text="|L| (dB)", range=[-20, 100], row=1, col=1)
    fig.update_yaxes(title_text="|S| (dB)", range=[-90, 10], row=2, col=1)
    fig.update_xaxes(title_text="time (s)", range=[0, 30], row=3, col=1)
    fig.update_yaxes(title_text="heading error (rad)", range=[-0.01, 0.12], row=3, col=1)
    head = "no lag (ratio 1): the lead alone" if r == 1 else f"lag ratio {r}: zero 0.25, pole {b2:.4g} rad/s"
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1250, margin=dict(l=100, r=30, t=170, b=70),
                      legend=dict(x=0.0, y=1.0, yanchor="bottom", orientation="h", font=dict(size=17)),
                      title=dict(x=0.5, y=0.975, text=f"{head}<br>drag offset {off:.4f} rad, PM {pm:.1f}°, Ms = {Ms:.3f}"))
    return fig


figs = [frame(r) for r in rs]
make_gif(figs, here / "lag_anim", fps=1, holds=[3, 1, 1, 1, 10], keys=[0, 4], cols=2, width=800)
