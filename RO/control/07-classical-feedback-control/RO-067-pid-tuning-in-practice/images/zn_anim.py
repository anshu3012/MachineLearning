"""The Ziegler-Nichols experiment on the speed loop: P control only (the drive force is 1 N, the force that holds
0.5 m/s, plus kp times the error), the reference steps up by 0.01 m/s at t = 0.2 s, and the gain is raised run by run:
50, 100, 150, 200 N per m/s. Each run plays in steps; earlier runs stay faint. At 200 the ringing neither grows nor
dies: the critical gain kc = 200, and two neighbouring peaks are Tc = 0.40 s apart. The force stays inside +-4 N.
Run: python zn_anim.py -> zn_anim.gif, zn_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif
from tunekit import KC, TC, U_MAX, speed_run

here = Path(__file__).parent
T = 3.0
STEP = lambda t: 0.51 if t >= 0.2 else 0.5
GAINS = [50, 100, 150, 200]
COL = {50: GREEN, 100: BLUE, 150: ORANGE, 200: RED}
runs = {kp: speed_run(T, kp, 0, r=STEP, bias=1.0) for kp in GAINS}


def peaks(t, y):
    return [i for i in range(1, len(y) - 1) if y[i] > y[i - 1] and y[i] >= y[i + 1] and t[i] > 1.0]


t, _, y200, u200 = runs[200]
pk = peaks(t, y200)
per = np.diff(t[pk])
amp = y200[pk] - 0.5
assert np.allclose(per, TC, atol=0.011) and amp.max() - amp.min() < 0.0005      # steady swings, 0.39 to 0.40 s
assert u200.min() > -U_MAX and u200.max() < U_MAX and abs(u200.max() - 3.0) < 0.01
t220, _, y220, _ = speed_run(T, 220, 0, r=STEP, bias=1.0)
a220 = y220[peaks(t220, y220)]
assert np.all(np.diff(a220) > 0)                                                   # past kc the swings grow
_, _, y150, _ = runs[150]
a150 = y150[peaks(t, y150)]
assert np.all(np.diff(a150) < 0)                                                   # below kc they die out
p0, p1 = pk[1], pk[2]


def frame(kp, upto, final=False):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08, row_heights=[0.62, 0.38])
    for g in GAINS:
        if g > kp:
            break
        tt, _, y, u = runs[g]
        n = len(tt) if g < kp else int(upto / (tt[1] - tt[0])) + 1
        thick = g == kp
        fig.add_trace(go.Scatter(x=tt[:n], y=y[:n], mode="lines", name=f"kp = {g}",
                                 line=dict(color=COL[g], width=4 if thick else 2),
                                 opacity=1 if thick else 0.35), row=1, col=1)
        if thick:
            fig.add_trace(go.Scatter(x=tt[:n], y=u[:n], mode="lines", showlegend=False,
                                     line=dict(color=COL[g], width=3)), row=2, col=1)
    fig.add_hline(y=0.51, line=dict(color="black", width=1, dash="dash"), row=1, col=1)
    for lim in (U_MAX, -U_MAX):
        fig.add_hline(y=lim, line=dict(color=GREY, width=2, dash="dot"), row=2, col=1)
    fig.add_annotation(x=2.95, y=U_MAX, text="force limit 4 N", showarrow=False, xanchor="right", yanchor="bottom",
                       font=dict(size=17, color=GREY), row=2, col=1)
    if final:
        ytop = y200[p0] + 0.004
        fig.add_trace(go.Scatter(x=[t[p0], t[p1]], y=[ytop, ytop], mode="lines+markers", showlegend=False,
                                 line=dict(color="black", width=3), marker=dict(symbol="line-ns", size=14,
                                 line=dict(width=3, color="black"))), row=1, col=1)
        fig.add_annotation(x=(t[p0] + t[p1]) / 2, y=ytop + 0.0015, text=f"Tc = {TC:.2f} s", showarrow=False,
                           yanchor="bottom", font=dict(size=21), row=1, col=1)
        title = f"kp = {KC:.0f}: the swings neither grow nor decay, so kc = {KC:.0f}"
    else:
        msg = {50: "settles", 100: "rings, then settles", 150: "rings longer", 200: "keeps ringing"}
        title = f"run {GAINS.index(kp) + 1}: kp = {kp} N per m/s, the speed {msg[kp]}"
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=760,
                      margin=dict(l=110, r=30, t=150, b=80), title=dict(text=title, x=0.5, y=0.97),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=1.02, yanchor="bottom",
                                  font=dict(size=18)))
    fig.update_yaxes(title_text="measured speed (m/s)", range=[0.495, 0.535], row=1, col=1)
    fig.update_yaxes(title_text="force (N)", range=[-4.6, 4.6], row=2, col=1)
    fig.update_xaxes(range=[0, T], row=1, col=1)
    fig.update_xaxes(title_text="time t (s)", range=[0, T], row=2, col=1)
    return fig


figs, holds, keys = [], [], []
for kp in GAINS:
    for j, upto in enumerate(np.linspace(0.5, T, 6)):
        figs.append(frame(kp, upto))
        holds.append(5 if j == 5 else 1)
    keys.append(len(figs) - 1)
figs.append(frame(200, T, final=True))
holds.append(16)
keys = [keys[0], keys[2], len(figs) - 1]
make_gif(figs, here / "zn_anim", fps=5, holds=holds, keys=keys, cols=1, width=850)
