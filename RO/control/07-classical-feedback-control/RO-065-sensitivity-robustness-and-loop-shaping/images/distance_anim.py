"""The sensitivity function read off the Nyquist plot. The PD heading loop L(s) = (0.8 s + 4)/s^2; as the frequency w
rises, the point L(jw) runs along the Nyquist curve. Top: the red line from the critical point -1 to L(jw); its length
is |1 + L(jw)|. Bottom left: that distance against w. Bottom right: its reciprocal, the gain |S(jw)| of the sensitivity
function. The last frame marks the closest approach, 0.392 at 2.085 rad/s, so the peak Ms = 1/0.392 = 2.55.
Run: python distance_anim.py -> distance_anim.gif, distance_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, RED, make_gif
from loopkit import L_head, sens_peak

here = Path(__file__).parent
wms, dmin, Ms = sens_peak(L_head)
assert abs(wms - 2.085) < 1e-3 and abs(dmin - 0.392) < 5e-4 and abs(Ms - 2.55) < 5e-3
wc = np.logspace(np.log10(1.1), np.log10(15), 600)          # the curve drawn
Lc = L_head(1j * wc)
ws = list(np.round(np.geomspace(1.2, 12, 16), 2))
ws.insert(int(np.searchsorted(ws, wms)), round(wms, 3))
ang = np.linspace(0, 2 * np.pi, 200)


def lab(w):
    return "2.085" if abs(w - wms) < 1e-3 else f"{w:.2f}"


def frame(w, last=False):
    fig = make_subplots(rows=2, cols=2, specs=[[{"colspan": 2}, None], [{}, {}]], row_heights=[0.55, 0.45],
                        vertical_spacing=0.16, horizontal_spacing=0.14)
    fig.add_trace(go.Scatter(x=Lc.real, y=Lc.imag, mode="lines", line=dict(color=BLUE, width=4),
                             name="Nyquist curve L(jω), ω > 0"), 1, 1)
    fig.add_trace(go.Scatter(x=[-1], y=[0], mode="markers", marker=dict(color=RED, size=16, symbol="x"),
                             name="critical point −1"), 1, 1)
    if last:
        fig.add_trace(go.Scatter(x=-1 + dmin * np.cos(ang), y=dmin * np.sin(ang), mode="lines",
                                 line=dict(color=RED, width=2, dash="dot"), showlegend=False), 1, 1)
    Lw = L_head(1j * w)
    fig.add_trace(go.Scatter(x=[-1, Lw.real], y=[0, Lw.imag], mode="lines", line=dict(color=RED, width=4),
                             showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=[Lw.real], y=[Lw.imag], mode="markers", marker=dict(color=BLUE, size=16),
                             showlegend=False), 1, 1)
    fig.add_annotation(x=Lw.real, y=Lw.imag, text=f"ω = {lab(w)} rad/s<br>distance {abs(1 + Lw):.3f}",
                       ax=60 if Lw.real < -1.5 else 90, ay=60, font=dict(size=18, color=RED), arrowcolor=RED, row=1, col=1)
    k = np.ones(len(ws), bool) if last else np.array(ws) <= w + 1e-9
    wk = np.array(ws)[k]
    dk = np.abs(1 + L_head(1j * wk))
    fig.add_trace(go.Scatter(x=wk, y=dk, mode="lines+markers", line=dict(color=RED, width=3), marker=dict(size=9),
                             showlegend=False), 2, 1)
    fig.add_trace(go.Scatter(x=wk, y=1 / dk, mode="lines+markers", line=dict(color=BLUE, width=3), marker=dict(size=9),
                             showlegend=False), 2, 2)
    if last:
        fig.add_annotation(x=np.log10(wms), y=dmin, text="closest: 0.392", ax=70, ay=-90, font=dict(size=18, color=RED),
                           arrowcolor=RED, row=2, col=1)
        fig.add_annotation(x=np.log10(wms), y=Ms, text="Ms = 1/0.392 = 2.55", ax=120, ay=-25,
                           font=dict(size=18, color=BLUE), arrowcolor=BLUE, row=2, col=2)
    fig.update_xaxes(title_text="real part", range=[-3.2, 0.4], row=1, col=1)
    fig.update_yaxes(title_text="imaginary part", range=[-1.2, 0.5], scaleanchor="x", scaleratio=1, row=1, col=1)
    for c, ttl, rng in ((1, "distance |1 + L|", [0, 2.2]), (2, "|S| = 1 / distance", [0, 3])):
        fig.update_xaxes(type="log", range=[0, np.log10(15)], title_text="ω (rad/s)", row=2, col=c)
        fig.update_yaxes(title_text=ttl, range=rng, row=2, col=c)
    title = ("the closest approach sets the peak of |S|" if last else
             f"ω = {lab(w)} rad/s: distance from −1 = {abs(1 + Lw):.3f}, |S| = {1 / abs(1 + Lw):.2f}")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1050, margin=dict(l=90, r=30, t=150, b=70),
                      legend=dict(x=0.0, y=1.02, yanchor="bottom", orientation="h", font=dict(size=17)),
                      title=dict(x=0.5, y=0.975, text=title))
    return fig


figs = [frame(w) for w in ws] + [frame(wms, last=True)]
make_gif(figs, here / "distance_anim", fps=2, holds=[3] + [1] * (len(ws) - 1) + [12],
         keys=[3, len(ws)], cols=2, width=800)
