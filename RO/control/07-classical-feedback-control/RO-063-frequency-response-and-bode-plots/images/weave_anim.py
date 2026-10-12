"""The opening problem: the planner asks the robot to weave, its heading command a sine of 0.1 rad at three weave
rates, 0.5, 1.92 and 5 rad/s. The PD heading loop (Kp = 0.4, Kd = 0.08) follows the slow weave (1.06 times the command,
6 degrees late), over-turns at 1.92 rad/s (2.55 times, 78 degrees late) and barely turns at 5 rad/s (0.19 times,
169 degrees late). Each stage shows two weave periods after the start-up swing has died away; the last frame sums up
the three. Run: python weave_anim.py -> weave_anim.gif, weave_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif
from loopkit import G_yr, deg, simulate_heading, sine_fit
from robotdraw import robot

here = Path(__file__).parent
A = 0.1                                   # command amplitude (rad)
RATES = [0.5, 1.92, 5.0]
G = {w: G_yr(1j * w) for w in RATES}
gain = {w: abs(G[w]) for w in RATES}
lag = {w: -deg(G[w]) for w in RATES}
assert [round(gain[w], 2) for w in RATES] == [1.06, 2.55, 0.19] and [round(lag[w]) for w in RATES] == [6, 78, 169]
for w in RATES:                           # the simulated loop, started from rest, settles on the same sine
    t = np.arange(0, max(80, 40 * 2 * np.pi / w), 1e-3)
    th, _, tq = simulate_heading(t, A * np.sin(w * t))
    k = t > t[-1] / 2
    amp, ph = sine_fit(t[k], th[k], w)
    assert abs(amp / A - gain[w]) < 0.005 and abs(-np.degrees(ph) - lag[w]) < 0.5 and abs(tq).max() < 0.2


def ray(ang, r=0.66):
    return [0, r * np.cos(ang)], [0, r * np.sin(ang)]


def frame(w, tk):
    T = 2 * np.pi / w
    ts = np.linspace(0, 2 * T, 400)
    cmd = A * np.sin(w * ts)
    head = A * gain[w] * np.sin(w * ts - np.radians(lag[w]))
    k = np.searchsorted(ts, tk)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.4, 0.6], horizontal_spacing=0.08,
                        subplot_titles=["the robot from above", "heading θ (blue), command θ<sub>r</sub> (dashed)"])
    x, y = ray(A * np.sin(w * tk))
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=GREY, width=4, dash="dash")), 1, 1)
    for tr in robot((0, 0, head[min(k, len(ts) - 1)]), scale=1.6):
        fig.add_trace(tr, 1, 1)
    fig.add_annotation(x=0.0, y=-0.42, text="dashed: command θ<sub>r</sub><br>orange arrow: heading θ", showarrow=False,
                       font=dict(size=18, color=GREY), row=1, col=1)
    fig.add_trace(go.Scatter(x=ts, y=cmd, mode="lines", line=dict(color=GREY, width=3, dash="dash")), 1, 2)
    fig.add_trace(go.Scatter(x=ts[:k + 1], y=head[:k + 1], mode="lines", line=dict(color=BLUE, width=4)), 1, 2)
    fig.add_trace(go.Scatter(x=[ts[min(k, len(ts) - 1)]], y=[head[min(k, len(ts) - 1)]], mode="markers",
                             marker=dict(color=ORANGE, size=14)), 1, 2)
    sub = (f"<br><span style='color:{RED}'>heading swings ±{A * gain[w]:.3f} rad = {gain[w]:.2f} × the command,"
           f" {lag[w]:.0f}° late</span>" if tk >= 2 * T - 1e-9 else "<br> ")
    fig.update_xaxes(range=[-0.75, 0.75], visible=False, row=1, col=1)
    fig.update_yaxes(range=[-0.55, 0.75], visible=False, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(title="time t (s)", range=[0, 2 * T], row=1, col=2)
    fig.update_yaxes(title="angle (rad)", range=[-0.3, 0.3], row=1, col=2)
    fig.update_layout(template="simple_white", font=FONT, width=1150, height=620, showlegend=False,
                      margin=dict(l=40, r=30, t=160, b=70),
                      title=dict(x=0.5, y=0.96, text=f"weave rate ω = {w} rad/s (one weave every {T:.2f} s){sub}"))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=20)
    return fig


def summary():
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.16,
                        subplot_titles=["heading swing ÷ command swing", "how late the heading is (degrees)"])
    names = [f"{w} rad/s" for w in RATES]
    cols = [BLUE, RED, GREY]
    fig.add_trace(go.Bar(x=names, y=[gain[w] for w in RATES], marker_color=cols,
                         text=[f"{gain[w]:.2f}" for w in RATES], textposition="outside"), 1, 1)
    fig.add_trace(go.Bar(x=names, y=[lag[w] for w in RATES], marker_color=cols,
                         text=[f"{lag[w]:.0f}°" for w in RATES], textposition="outside"), 1, 2)
    fig.add_trace(go.Scatter(x=names, y=[1, 1, 1], mode="lines", line=dict(color=GREY, dash="dash", width=2)), 1, 1)
    fig.add_annotation(x=names[2], y=1, text="1: follows exactly", showarrow=False, yanchor="bottom", xanchor="left",
                       xshift=-20, font=dict(size=17, color=GREY), row=1, col=1)
    fig.update_yaxes(range=[0, 3.1], row=1, col=1)
    fig.update_yaxes(range=[0, 200], row=1, col=2)
    fig.update_xaxes(title="weave rate ω", row=1, col=1)
    fig.update_xaxes(title="weave rate ω", row=1, col=2)
    fig.update_layout(template="simple_white", font=FONT, width=1150, height=620, showlegend=False,
                      margin=dict(l=70, r=30, t=140, b=80),
                      title=dict(x=0.5, y=0.96, text="slow: follows · 1.92 rad/s: over-turns · fast: barely turns"))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=20)
    return fig


figs, holds, keys = [], [], []
for w in RATES:
    T = 2 * np.pi / w
    tks = np.linspace(0, 2 * T, 25)
    figs += [frame(w, tk) for tk in tks]
    holds += [4] + [1] * 23 + [12]
    keys.append(len(figs) - 1)
figs.append(summary())
holds.append(30)
keys.append(len(figs) - 1)
make_gif(figs, here / "weave_anim", fps=8, holds=holds, keys=keys, cols=2, width=900)
