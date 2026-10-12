"""What a transfer function is: feed the speed plant 8 v' + 2 v = u an exponential force u = e^(s t) and the speed comes
out as the same exponential times one number, G(s) = 1 / (8 s + 2). Left: s = -0.1, a fading push; the speed is 0.833
times the force at every instant. Right: s = 0.1, a growing push; the speed is 0.357 times the force. Each robot starts
at the matching speed, G(s) times 1 N. Run: python expo_anim.py -> expo_anim.gif, expo_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, ORANGE, PURPLE, make_gif
from tfkit import B, M

here = Path(__file__).parent
t = np.linspace(0, 5, 5001)
CASES = []
for s in (-0.1, 0.1):
    g = 1 / (M * s + B)
    u = np.exp(s * t)
    v = np.zeros_like(t)                         # simulate the plant from v(0) = G(s): Euler steps of 1 ms
    v[0] = g
    for k in range(len(t) - 1):
        v[k + 1] = v[k] + (t[1] - t[0]) * (u[k] - B * v[k]) / M
    assert np.max(np.abs(v / u - g)) < 1e-3     # the speed is G(s) times the force at every instant
    CASES.append((s, g, u, v))
assert abs(CASES[0][1] - 0.8333) < 1e-4 and abs(CASES[1][1] - 0.3571) < 1e-4
TK = np.round(np.arange(0, 5.01, 0.125), 3)


def frame(tk):
    k = int(round(tk * 1000))
    titles = [f"s = {s:g}: G(s) = 1 / (8 s + 2) = {g:.3f}" for s, g, _, _ in CASES]
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=titles)
    for c, (s, g, u, v) in enumerate(CASES, start=1):
        fig.add_trace(go.Scatter(x=t[:k + 1], y=u[:k + 1], mode="lines", line=dict(color=ORANGE, width=4),
                                 name="force u (N)", showlegend=c == 1), 1, c)
        fig.add_trace(go.Scatter(x=t[:k + 1], y=v[:k + 1], mode="lines", line=dict(color=BLUE, width=4),
                                 name="speed v (m/s)", showlegend=c == 1), 1, c)
        fig.add_trace(go.Scatter(x=[t[k], t[k]], y=[v[k], u[k]], mode="lines+markers",
                                 line=dict(color=PURPLE, width=2, dash="dot"), marker=dict(size=9, color=PURPLE),
                                 showlegend=False), 1, c)
        fig.add_annotation(x=t[k], y=max(u[k], v[k]) + 0.12, text=f"v / u = {v[k] / u[k]:.3f}", showarrow=False,
                           xanchor="right" if tk > 2.5 else "left", xshift=-8 if tk > 2.5 else 8,
                           font=dict(color=PURPLE, size=19), bgcolor="rgba(255,255,255,0.85)", row=1, col=c)
        fig.update_yaxes(range=[0, 1.8], row=1, col=c)
    fig.update_xaxes(title="time t (s)", range=[0, 5])
    fig.update_layout(template="simple_white", font=FONT, width=1250, height=600,
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=1.2, font=dict(size=20)),
                      margin=dict(l=60, r=30, t=170, b=70),
                      title=dict(x=0.5, y=0.97, text=f"an exponential force in, the same exponential out:   t = {tk:.2f} s"))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=21)
    return fig


figs = [frame(tk) for tk in TK]
make_gif(figs, here / "expo_anim", fps=8, holds=[8] + [1] * (len(TK) - 2) + [30], keys=[8, len(TK) - 1], cols=1,
         width=900)
