"""Why a sine stays a sine: the speed loop's PI controller of RO-060, Kp = 20 N per m/s and Ki = 10 N per m, is fed a
speed error that swings 0.1 m/s at 0.5 rad/s, e(t) = 0.1 sin(0.5 t) (right axis, m/s). Stage 1: the error. Stage 2: the
proportional part 20 e = 2 sin(0.5 t) N, same timing. Stage 3: the integral part, 10 N per m times the running total of
e, whose swing is -2 cos(0.5 t) N, a quarter period later. Stage 4: their sum 2.83 sin(0.5 t - 45 deg) N: a sine of the
same rate, 45 degrees (1.57 s) later. Run: python ops_anim.py -> ops_anim.gif, ops_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, RED, make_gif

here = Path(__file__).parent
KP, KI, w, E = 20.0, 10.0, 0.5, 0.1
t = np.linspace(0, 4 * np.pi / w, 801)            # two periods, 25.1 s
e = E * np.sin(w * t)
p = KP * e
i = KI * (-E / w) * np.cos(w * t)                  # Ki times the swing of the running total of e
out = p + i
C = KP + KI / (1j * w)
amp, sh = abs(C) * E, np.angle(C)
assert abs(KP * E - 2) < 1e-12 and abs(KI * E / w - 2) < 1e-12
assert abs(amp - 2.83) < 5e-3 and abs(np.degrees(sh) + 45) < 1e-9 and abs(-sh / w - 1.57) < 5e-3
assert np.allclose(out, amp * np.sin(w * t + sh))
dt = t[1] - t[0]
assert np.allclose(np.gradient(i / KI, dt)[5:-5], e[5:-5], atol=2e-4)   # i / Ki really is the running total of e
FADE_B, FADE_O = "rgba(76,120,168,0.35)", "rgba(245,133,24,0.35)"
STAGES = [("the speed error e = 0.1 sin(0.5 t) m/s (right axis)", [("speed error e (m/s, right axis)", e, GREY, "dash", True)]),
          ("proportional part 20e = 2 sin(0.5 t) N: same timing",
           [("speed error e (m/s, right axis)", e, GREY, "dash", True), ("20 e (N)", p, BLUE, "solid", False)]),
          ("integral part: swing −2 cos(0.5 t) N, a quarter period later",
           [("speed error e (m/s, right axis)", e, GREY, "dash", True), ("20 e (N)", p, BLUE, "solid", False),
            ("10 × swing of running total of e (N)", i, ORANGE, "solid", False)]),
          ("PI output = 2.83 sin(0.5 t − 45°) N: a sine of the same rate",
           [("speed error e (m/s, right axis)", e, GREY, "dash", True), ("20 e (N)", p, FADE_B, "solid", False),
            ("10 × swing of running total of e (N)", i, FADE_O, "solid", False), ("PI output u (N)", out, PURPLE, "solid", False)])]


def frame(si, frac):
    title, curves = STAGES[si]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    n = int(frac * (len(t) - 1)) + 1
    for j, (name, y, col, dash, right) in enumerate(curves):
        upto = n if j == len(curves) - 1 else len(t)
        fig.add_trace(go.Scatter(x=t[:upto], y=y[:upto], mode="lines", name=name,
                                 line=dict(color=col, width=5 if j == len(curves) - 1 else 3, dash=dash)),
                      secondary_y=right)
    if si == 3 and frac >= 1:
        tc = np.pi / 2 / w                          # first crest of the error
        tp = (np.pi / 2 - sh) / w                   # first crest of the output
        fig.add_trace(go.Scatter(x=[tc], y=[E], mode="markers", showlegend=False, marker=dict(color=GREY, size=14)),
                      secondary_y=True)
        fig.add_trace(go.Scatter(x=[tp], y=[amp], mode="markers", showlegend=False, marker=dict(color=RED, size=14)),
                      secondary_y=False)
        fig.add_annotation(x=tp, y=amp, text="crest 2.83 N", ax=-90, ay=-25, arrowcolor=RED, font=dict(color=RED, size=20))
        fig.add_annotation(x=tp + 1.6, y=3.3, text="← 1.57 s later = 45° of a 12.57 s period", xanchor="left",
                           showarrow=False, font=dict(color=RED, size=19))
        fig.add_shape(type="line", x0=tc, x1=tc, y0=-2.3, y1=1, line=dict(color=GREY, dash="dot", width=2))
        fig.add_shape(type="line", x0=tp, x1=tp, y0=-2.3, y1=amp, line=dict(color=RED, dash="dot", width=2))
    fig.update_xaxes(title="time t (s)", range=[0, t[-1]])
    fig.update_yaxes(title="force (N)", range=[-3.2, 3.6], secondary_y=False)
    fig.update_yaxes(title="speed error (m/s)", range=[-0.32, 0.36], secondary_y=True, showgrid=False)
    fig.update_layout(template="simple_white", font=FONT, width=1100, height=720,
                      legend=dict(orientation="h", x=0, y=1.02, yanchor="bottom", font=dict(size=17)),
                      margin=dict(l=80, r=90, t=190, b=70), title=dict(x=0.5, y=0.96, text=title))
    return fig


figs, holds, keys = [], [], []
for si in range(4):
    for frac in np.linspace(0.1, 1, 10):
        figs.append(frame(si, frac))
        holds.append(1)
    holds[-1] = 10 if si < 3 else 30
    keys.append(len(figs) - 1)
make_gif(figs, here / "ops_anim", fps=8, holds=holds, keys=keys, cols=2, width=900)
