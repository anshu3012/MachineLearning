"""The Bode plot built point by point: the heading command is a sine of 0.1 rad at rising weave rates w, from 0.2 to
10 rad/s. Top: two periods of the settled command (dashed) and heading (blue). Middle: the gain in decibels, one dot
per rate. Bottom: the phase in degrees. The dots come from fitting a sine to the simulated heading; the last frame
draws the exact curves of G(jw) = 4/(4 - w^2 + 0.8 j w) through them and the straight-line asymptotes: 0 dB up to
w_n = 2 rad/s, then -40 dB per decade; phase 0, then -180 deg. Run: python sweep_anim.py -> sweep_anim.gif,
sweep_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from loopkit import G_yr, db, deg, simulate_heading, sine_fit

here = Path(__file__).parent
A = 0.1
WS = [0.2, 0.3, 0.5, 0.7, 1.0, 1.4, 1.92, 2.5, 3.0, 4.0, 6.0, 10.0]
meas = {}
for w in WS:                                      # simulate the loop from rest, fit the settled sine
    T = 2 * np.pi / w
    t = np.arange(0, max(60, 30 * T), 1e-3)
    th, _, tq = simulate_heading(t, A * np.sin(w * t))
    k = t > t[-1] - 10 * T
    amp, ph = sine_fit(t[k], th[k], w)
    g = G_yr(1j * w)
    assert abs(amp / A - abs(g)) < 0.006 * abs(g) and abs(np.degrees(ph) - deg(g)) < 0.6 and abs(tq).max() < 0.2
    meas[w] = (20 * np.log10(amp / A), np.degrees(ph))
assert abs(meas[1.0][0] - 2.20) < 0.01 and abs(meas[1.92][0] - 8.13) < 0.02 and abs(meas[10.0][0] + 27.7) < 0.1
wl = np.logspace(-1, np.log10(20), 600)


def frame(n, last=False):
    w = WS[min(n, len(WS) - 1)]
    T = 2 * np.pi / w
    ts = np.linspace(0, 2 * T, 300)
    g = G_yr(1j * w)
    fig = make_subplots(rows=3, cols=1, row_heights=[0.28, 0.36, 0.36], vertical_spacing=0.1,
                        subplot_titles=[f"ω = {w:g} rad/s: heading swing {A * abs(g):.4f} rad, {-deg(g):.1f}° late",
                                        "", ""])
    fig.add_trace(go.Scatter(x=ts / T, y=A * np.sin(w * ts), mode="lines", line=dict(color=GREY, width=3, dash="dash")),
                  1, 1)
    fig.add_trace(go.Scatter(x=ts / T, y=A * abs(g) * np.sin(w * ts + np.angle(g)), mode="lines",
                             line=dict(color=BLUE, width=4)), 1, 1)
    done = WS[:n + 1]
    if last:
        gl = G_yr(1j * wl)
        fig.add_trace(go.Scatter(x=wl, y=db(gl), mode="lines", line=dict(color=BLUE, width=3)), 2, 1)
        fig.add_trace(go.Scatter(x=wl, y=deg(gl), mode="lines", line=dict(color=BLUE, width=3)), 3, 1)
        fig.add_trace(go.Scatter(x=[0.1, 2, 20], y=[0, 0, -40], mode="lines", line=dict(color=ORANGE, width=3, dash="dash")),
                      2, 1)
        fig.add_trace(go.Scatter(x=[0.1, 2, 2, 20], y=[0, 0, -180, -180], mode="lines",
                                 line=dict(color=ORANGE, width=3, dash="dash")), 3, 1)
        fig.add_annotation(x=np.log10(8), y=-40 * np.log10(4), text="asymptote: −40 dB per decade", ax=-200, ay=45,
                           arrowcolor=ORANGE, font=dict(color=ORANGE, size=18), row=2, col=1)
        fig.add_annotation(x=np.log10(0.15), y=-6, text="asymptote: 0 dB", showarrow=False,
                           font=dict(color=ORANGE, size=18), xanchor="left", row=2, col=1)
    fig.add_trace(go.Scatter(x=done, y=[meas[x][0] for x in done], mode="markers",
                             marker=dict(color=[RED if x == w and not last else BLUE for x in done], size=13)), 2, 1)
    fig.add_trace(go.Scatter(x=done, y=[meas[x][1] for x in done], mode="markers",
                             marker=dict(color=[RED if x == w and not last else BLUE for x in done], size=13)), 3, 1)
    fig.update_xaxes(title="time ÷ one weave period", range=[0, 2], row=1, col=1)
    fig.update_yaxes(title="angle (rad)", range=[-0.3, 0.3], row=1, col=1)
    for r in (2, 3):
        fig.update_xaxes(type="log", range=[-1, np.log10(20)], title="weave rate ω (rad/s), log scale" if r == 3 else None,
                         row=r, col=1)
    fig.update_yaxes(range=[-48, 14], dtick=10, title="gain (dB)", row=2, col=1)
    fig.update_yaxes(range=[-190, 10], dtick=45, title="phase (°)", row=3, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1350, showlegend=False,
                      margin=dict(l=90, r=30, t=130, b=70),
                      title=dict(x=0.5, y=0.975, text="the Bode plot of the heading loop" if last else
                                 "one weave rate at a time: measure, then plot"))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=20)
    return fig


figs = [frame(n) for n in range(len(WS))] + [frame(len(WS) - 1, last=True)]
make_gif(figs, here / "sweep_anim", fps=2, holds=[3] + [2] * (len(WS) - 1) + [16],
         keys=[4, 6, len(WS) - 1, len(figs) - 1], cols=2, width=760)
