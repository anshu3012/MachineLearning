"""Asymptotes built from pieces, on the speed plant P(s) = 1/(8 s + 2) = 0.5 x 1/(4 s + 1). Stage 1: the constant 0.5
is -6.02 dB at every rate, phase 0. Stage 2: the lag 1/(4 s + 1) is flat at 0 dB up to its corner 1/4 = 0.25 rad/s,
then falls 20 dB per decade; its phase goes from 0 to -90 deg in a straight line over the two decades 0.025 to
2.5 rad/s. Stage 3: in decibels and degrees the pieces add. Stage 4: the exact curve: 3.01 dB below the asymptotes'
corner (-9.03 dB) and -45 deg at the corner. Run: python asym_anim.py -> asym_anim.gif, asym_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, RED, make_gif
from loopkit import P_speed, db, deg

here = Path(__file__).parent
wl = np.logspace(np.log10(0.0025), np.log10(25), 600)
wc = 0.25
K_DB = db(0.5)
lag_db = np.where(wl < wc, 0, -20 * np.log10(wl / wc))
lag_ph = np.clip(-45 - 45 * np.log10(wl / wc), -90, 0)
exact = P_speed(1j * wl)
assert abs(K_DB + 6.02) < 5e-3 and abs(db(P_speed(1j * wc)) + 9.03) < 5e-3 and abs(deg(P_speed(1j * wc)) + 45) < 1e-9
assert abs(db(P_speed(1j * wc)) - K_DB + 3.01) < 5e-3 and abs(deg(P_speed(0.025j)) + 5.7) < 0.05
assert np.max(np.abs(db(exact) - (K_DB + lag_db))) < 3.02          # the largest error is at the corner
STAGES = ["piece 1: the constant 0.5 = −6.02 dB, phase 0°",
          "piece 2: the lag 1/(4s + 1): corner at 0.25 rad/s, then −20 dB per decade",
          "add the pieces (decibels add, degrees add)",
          "the exact curve: 3.01 dB below the corner, −45° there"]


def frame(si):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.08)
    if si in (0, 2, 3):
        c = GREY if si else ORANGE
        fig.add_trace(go.Scatter(x=wl, y=np.full_like(wl, K_DB), mode="lines", line=dict(color=c, width=3,
                                 dash="dot" if si else "solid")), 1, 1)
        fig.add_trace(go.Scatter(x=wl, y=np.zeros_like(wl), mode="lines", line=dict(color=c, width=3,
                                 dash="dot" if si else "solid")), 2, 1)
    if si in (1, 2, 3):
        c = GREY if si > 1 else PURPLE
        fig.add_trace(go.Scatter(x=wl, y=lag_db, mode="lines", line=dict(color=c, width=3, dash="dot" if si > 1 else "solid")),
                      1, 1)
        fig.add_trace(go.Scatter(x=wl, y=lag_ph, mode="lines", line=dict(color=c, width=3, dash="dot" if si > 1 else "solid")),
                      2, 1)
    if si == 1:
        fig.add_annotation(x=np.log10(wc), y=0, text="corner 0.25 rad/s", ax=-90, ay=45, arrowcolor=PURPLE,
                           font=dict(color=PURPLE, size=18), row=1, col=1)
        fig.add_annotation(x=np.log10(2.5), y=-20, text="−20 dB at 2.5 rad/s:<br>one decade, one fall of 20 dB",
                           ax=70, ay=-60, arrowcolor=PURPLE, font=dict(color=PURPLE, size=18), row=1, col=1)
    if si >= 2:
        fig.add_annotation(x=0.01, y=0.03, xref="x domain", yref="y domain", xanchor="left", yanchor="bottom",
                           showarrow=False, align="left", font=dict(size=17),
                           text=("<span style='color:#6B6B6B'>dotted grey: the two pieces</span><br>"
                                 "<span style='color:#F58518'>dashed orange: their sum, the asymptotes</span>"
                                 + ("<br><span style='color:#4C78A8'>blue: the exact curve</span>" if si == 3 else "")))
        fig.add_trace(go.Scatter(x=wl, y=K_DB + lag_db, mode="lines", line=dict(color=ORANGE, width=4, dash="dash")), 1, 1)
        fig.add_trace(go.Scatter(x=wl, y=lag_ph, mode="lines", line=dict(color=ORANGE, width=4, dash="dash")), 2, 1)
    if si == 3:
        fig.add_trace(go.Scatter(x=wl, y=db(exact), mode="lines", line=dict(color=BLUE, width=4)), 1, 1)
        fig.add_trace(go.Scatter(x=wl, y=deg(exact), mode="lines", line=dict(color=BLUE, width=4)), 2, 1)
        fig.add_trace(go.Scatter(x=[wc, wc], y=[K_DB, db(P_speed(1j * wc))], mode="markers",
                                 marker=dict(color=[ORANGE, RED], size=12)), 1, 1)
        fig.add_annotation(x=np.log10(wc), y=db(P_speed(1j * wc)), text="exact −9.03 dB:<br>3.01 dB below",
                           ax=-120, ay=55, arrowcolor=RED, font=dict(color=RED, size=18), row=1, col=1)
        fig.add_trace(go.Scatter(x=[wc], y=[-45], mode="markers", marker=dict(color=RED, size=12)), 2, 1)
        fig.add_annotation(x=np.log10(wc), y=-45, text="−45° at the corner", ax=110, ay=-30, arrowcolor=RED,
                           font=dict(color=RED, size=18), row=2, col=1)
    for r in (1, 2):
        fig.update_xaxes(type="log", range=[np.log10(0.0025), np.log10(25)],
                         title="frequency ω (rad/s), log scale" if r == 2 else None, row=r, col=1)
    fig.update_yaxes(range=[-48, 6], dtick=10, title="gain (dB)", row=1, col=1)
    fig.update_yaxes(range=[-100, 10], dtick=45, title="phase (°)", row=2, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1050, showlegend=False,
                      margin=dict(l=90, r=30, t=130, b=70),
                      title=dict(x=0.5, y=0.97, text=f"speed plant 1/(8s + 2)<br><span style='font-size:20px'>{STAGES[si]}</span>"))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=20)
    return fig


figs = [frame(i) for i in range(4)]
make_gif(figs, here / "asym_anim", fps=1, holds=[4, 4, 4, 12], keys=[0, 1, 2, 3], cols=2, width=800)
