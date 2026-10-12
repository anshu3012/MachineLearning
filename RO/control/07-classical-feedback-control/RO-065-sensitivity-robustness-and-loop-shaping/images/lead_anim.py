"""A lead compensator reshapes the heading loop. The lead C = k (s + a)/(s + b) is centred on 2.5 rad/s (sqrt(ab) = 2.5)
and its gain k keeps the crossover there; the pole-to-zero ratio b/a grows 1, 1.5, 2, 3, 4.5, 6, 9. Top: |L| in dB.
Middle: the phase of L, whose bump is the lead's phase; the phase margin is the bar from -180 degrees at 2.5 rad/s.
Bottom: the Nyquist curve bends away from -1. At b/a = 1 the controller is a plain gain 0.625: phase margin 0 and the
curve runs through -1. At b/a = 9 (zero 0.833, pole 7.5 rad/s, k = 1.875): phase margin 53.1 degrees, Ms = 1.30.
Grey: the PD loop. Run: python lead_anim.py -> lead_anim.gif, lead_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, PURPLE, RED, make_gif
from loopkit import L_head, P_head, db, deg, margins, sens_peak
from shapekit import W_C, lead_family

here = Path(__file__).parent
rs = [1.0, 1.5, 2, 3, 4.5, 6, 9]
w = np.logspace(-1, 2, 1500)
wn = np.logspace(np.log10(0.9), np.log10(60), 1200)
ang = np.linspace(0, 2 * np.pi, 200)


def loop(r):
    k, a, b = lead_family(r)
    return k, a, b, (lambda s: k * (s + a) / (s + b) * P_head(s))


k9, a9, b9, L9 = loop(9)
assert abs(k9 - 1.875) < 1e-3 and abs(a9 - 0.8333) < 1e-3 and abs(b9 - 7.5) < 1e-9
assert abs(margins(L9)["pm"] - 53.13) < 0.01 and abs(sens_peak(L9)[2] - 1.30) < 5e-3


def frame(r):
    k, a, b, L = loop(r)
    lead = np.degrees(np.arctan(W_C / a) - np.arctan(W_C / b))
    pm = 180 + deg(L(1j * W_C))
    fig = make_subplots(rows=3, cols=1, row_heights=[0.28, 0.28, 0.44], vertical_spacing=0.08)
    for f, col, wd, name in ((L_head, GREY, 3, "PD loop (Kd = 0.08)"), (L, PURPLE, 5, "with the lead")):
        fig.add_trace(go.Scatter(x=w, y=db(f(1j * w)), line=dict(color=col, width=wd), name=name), 1, 1)
        fig.add_trace(go.Scatter(x=w, y=np.unwrap(np.angle(f(1j * w))) * 180 / np.pi, line=dict(color=col, width=wd),
                                 showlegend=False), 2, 1)
        Lc = f(1j * wn)
        fig.add_trace(go.Scatter(x=Lc.real, y=Lc.imag, mode="lines", line=dict(color=col, width=wd), showlegend=False),
                      3, 1)
    fig.add_trace(go.Scatter(x=[W_C, W_C], y=[-180, -180 + pm], mode="lines+markers", line=dict(color=RED, width=5),
                             marker=dict(size=8), showlegend=False), 2, 1)
    fig.add_annotation(x=np.log10(W_C), y=-180 + pm, text=f"PM {pm:.1f}°", ax=80, ay=-25, font=dict(size=18, color=RED),
                       arrowcolor=RED, row=2, col=1)
    fig.add_trace(go.Scatter(x=[-1], y=[0], mode="markers", marker=dict(color=RED, size=16, symbol="x"),
                             showlegend=False), 3, 1)
    if r > 1:
        _, d, Ms = sens_peak(L)
        fig.add_trace(go.Scatter(x=-1 + d * np.cos(ang), y=d * np.sin(ang), mode="lines",
                                 line=dict(color=RED, width=2, dash="dot"), showlegend=False), 3, 1)
        tail = f"PM {pm:.1f}°, Ms = {Ms:.2f}"
        head = f"lead b/a = {r:g}: zero {a:.3f}, pole {b:.3f} rad/s, k = {k:.3f}"
    else:
        tail = "PM 0°: the curve runs through −1"
        head = f"no lead (b/a = 1): a plain gain {k:.3f} N·m/rad"
    fig.add_hline(y=0, line=dict(color=GREY, width=1.5, dash="dash"), row=1, col=1)
    fig.add_hline(y=-180, line=dict(color=GREY, width=1.5, dash="dash"), row=2, col=1)
    fig.update_xaxes(type="log", range=[-1, 2], row=1, col=1)
    fig.update_xaxes(type="log", range=[-1, 2], title_text="ω (rad/s)", row=2, col=1)
    fig.update_yaxes(title_text="|L| (dB)", range=[-50, 60], row=1, col=1)
    fig.update_yaxes(title_text="phase of L (°)", range=[-185, -100], row=2, col=1)
    fig.update_xaxes(title_text="real part", range=[-3.0, 0.6], row=3, col=1)
    fig.update_yaxes(title_text="imaginary part", range=[-1.5, 0.9], scaleanchor="x3", scaleratio=1, row=3, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1250, margin=dict(l=100, r=30, t=170, b=70),
                      legend=dict(x=0.0, y=1.0, yanchor="bottom", orientation="h", font=dict(size=17)),
                      title=dict(x=0.5, y=0.975, text=f"{head}<br>phase lead {lead:.1f}° at 2.5 rad/s, {tail}"))
    return fig


figs = [frame(r) for r in rs]
make_gif(figs, here / "lead_anim", fps=1, holds=[3, 1, 1, 1, 1, 1, 10], keys=[0, 3, 6], cols=3, width=800)
