"""Resonance and the damping ratio: the heading loop's gain curve G(jw) = 4/(4 - w^2 + j 0.8 zeta/0.2 w), that is
Kp = 0.4 with Kd = 0.4 zeta, redrawn as the damping ratio zeta falls from 1 (RO-061's fix, Kd = 0.4) to 0.1. While
zeta >= 0.707 the curve never rises above 0 dB. Below it a peak grows near w_n = 2 rad/s: at w_n itself the gain is
exactly 1/(2 zeta); the peak is a little higher and a little to the left. The last frame returns to our loop,
zeta = 0.2: peak 2.55 (8.14 dB) at 1.918 rad/s, against 2.5 at 2 rad/s, with RO-060's tuned loop (Kp 0.2, Kd 0.283,
zeta = 1) in grey. Run: python zeta_anim.py -> zeta_anim.gif,
zeta_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from loopkit import G_yr, KP, db, deg, peak, wn_zeta

here = Path(__file__).parent
ZS = [1.0, 0.85, 0.707, 0.6, 0.5, 0.4, 0.3, 0.2, 0.15, 0.1]
wl = np.logspace(-1, np.log10(20), 800)


def G(z):
    return lambda s: G_yr(s, KP, 0.4 * z)


for z in ZS:
    assert abs(wn_zeta(KP, 0.4 * z)[1] - z) < 1e-12 and abs(abs(G(z)(2j)) - 1 / (2 * z)) < 1e-9
    wp, mp = peak(G(z))
    if z < 0.707:
        assert abs(mp - 1 / (2 * z * np.sqrt(1 - z * z))) < 1e-6 and abs(wp - 2 * np.sqrt(1 - 2 * z * z)) < 1e-3
    else:
        assert mp < 1 + 1e-6
wp02, mp02 = peak(G(0.2))
assert abs(wn_zeta(0.2, 0.283)[1] - 1) < 1e-3 and peak(lambda s: G_yr(s, 0.2, 0.283))[1] < 1 + 1e-6
assert abs(mp02 - 2.55) < 5e-3 and abs(20 * np.log10(mp02) - 8.14) < 5e-3 and abs(wp02 - 1.918) < 5e-4


def frame(z, last=False):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.6, 0.4], vertical_spacing=0.08)
    for zo in ZS:
        if zo > z and not last:
            fig.add_trace(go.Scatter(x=wl, y=db(G(zo)(1j * wl)), mode="lines", line=dict(color="#C9C9C9", width=2)), 1, 1)
    if last:
        gt = G_yr(1j * wl, 0.2, 0.283)              # RO-060's tuned gains: Kp 0.2, Kd 0.283, zeta 1
        fig.add_trace(go.Scatter(x=wl, y=db(gt), mode="lines", line=dict(color=GREY, width=3)), 1, 1)
        fig.add_trace(go.Scatter(x=wl, y=deg(gt), mode="lines", line=dict(color=GREY, width=3)), 2, 1)
        fig.add_annotation(x=np.log10(0.45), y=-8, text="RO-060's tuned loop (Kp 0.2, Kd 0.283, ζ = 1): no peak",
                           showarrow=False, font=dict(color=GREY, size=18), row=1, col=1)
    fig.add_trace(go.Scatter(x=[0.1, 2, 20], y=[0, 0, -40], mode="lines", line=dict(color=ORANGE, width=3, dash="dash")),
                  1, 1)
    g = G(z)(1j * wl)
    fig.add_trace(go.Scatter(x=wl, y=db(g), mode="lines", line=dict(color=BLUE, width=4)), 1, 1)
    fig.add_trace(go.Scatter(x=wl, y=deg(g), mode="lines", line=dict(color=BLUE, width=4)), 2, 1)
    fig.add_trace(go.Scatter(x=[2], y=[db(1 / (2 * z))], mode="markers", marker=dict(color=ORANGE, size=12)), 1, 1)
    fig.add_annotation(x=np.log10(2), y=db(1 / (2 * z)), text=f"at ω<sub>n</sub> = 2: 1/(2ζ) = {1 / (2 * z):.2f}",
                       ax=190, ay=60 if z < 0.5 else -40, arrowcolor=ORANGE, font=dict(color=ORANGE, size=18), row=1, col=1)
    if z < 0.707:
        wp, mp = peak(G(z))
        fig.add_trace(go.Scatter(x=[wp], y=[db(mp)], mode="markers", marker=dict(color=RED, size=13)), 1, 1)
        fig.add_annotation(x=np.log10(wp), y=db(mp), text=f"peak {mp:.2f} ({db(mp):.2f} dB)<br>at {wp:.3f} rad/s",
                           ax=-150, ay=-20, arrowcolor=RED, font=dict(color=RED, size=18), row=1, col=1)
    else:
        fig.add_annotation(x=np.log10(0.3), y=9, text="no peak above 0 dB", showarrow=False,
                           font=dict(color=RED, size=19), row=1, col=1)
    for r in (1, 2):
        fig.update_xaxes(type="log", range=[-1, np.log10(20)], title="weave rate ω (rad/s), log scale" if r == 2 else None,
                         row=r, col=1)
    fig.update_yaxes(range=[-42, 16], dtick=10, title="gain (dB)", row=1, col=1)
    fig.update_yaxes(range=[-190, 10], dtick=45, title="phase (°)", row=2, col=1)
    kd = 0.4 * z
    head = "our loop again" if last else "damping falls"
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1150, showlegend=False,
                      margin=dict(l=90, r=30, t=130, b=70),
                      title=dict(x=0.5, y=0.97, text=f"{head}: ζ = {z:g}  (Kd = {kd:.3g}, Kp = 0.4)"))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=20)
    return fig


figs = [frame(z) for z in ZS] + [frame(0.2, last=True)]
make_gif(figs, here / "zeta_anim", fps=1, holds=[3] + [1] * (len(ZS) - 1) + [12], keys=[0, 2, 7, len(figs) - 1],
         cols=2, width=760)
