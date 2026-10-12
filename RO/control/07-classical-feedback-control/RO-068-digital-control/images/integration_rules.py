"""Three ways to add up the area under the speed error with one sample every 0.5 s, one strip per frame: forward
Euler (each strip as tall as its left sample), backward Euler (as tall as its right sample) and Tustin (a trapezoid
joining both). The grey curve is the error of the continuous loop after the speed step. The titles keep the running
area; the last frame compares the three with the exact area under the curve from 0 to 2.5 s.
Run: python integration_rules.py -> integration_rules.gif, integration_rules_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from digikit import continuous_loop
from gifkit import BLUE, FONT, GREY, PURPLE, RED, make_gif

here = Path(__file__).parent
T, N = 0.5, 5
c = continuous_loop(3.0)
t, e = c["t"], 0.5 - c["v"]
tk = np.arange(N + 1) * T
ek = np.interp(tk, t, e)
m = t <= N * T + 1e-9
exact = np.trapezoid(e[m], t[m])
area = {"fwd": np.cumsum(T * ek[:-1]), "bwd": np.cumsum(T * ek[1:]), "tus": np.cumsum(T * (ek[:-1] + ek[1:]) / 2)}
RULES = [("fwd", "forward Euler: height of the left sample", RED),
         ("bwd", "backward Euler: height of the right sample", BLUE),
         ("tus", "Tustin: a trapezoid joining both samples", PURPLE)]
assert area["fwd"][-1] > exact > area["bwd"][-1] and abs(area["tus"][-1] - exact) < abs(area["fwd"][-1] - exact)


def frame(j, last=False):
    titles = [f"{name}<br>area so far {area[key][j - 1]:.4f} m" if j else f"{name}" for key, name, _ in RULES]
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.11, subplot_titles=titles)
    for i, (key, _, col) in enumerate(RULES, start=1):
        for s in range(j):
            a, b = tk[s], tk[s + 1]
            h0 = ek[s] if key == "fwd" else ek[s + 1] if key == "bwd" else ek[s]
            h1 = ek[s] if key == "fwd" else ek[s + 1] if key == "bwd" else ek[s + 1]
            fig.add_trace(go.Scatter(x=[a, a, b, b, a], y=[0, h0, h1, 0, 0], fill="toself", mode="lines",
                                     line=dict(color=col, width=2), fillcolor=col, opacity=0.35), row=i, col=1)
        fig.add_trace(go.Scatter(x=t[m], y=e[m], mode="lines", line=dict(color=GREY, width=3)), row=i, col=1)
        fig.add_trace(go.Scatter(x=tk, y=ek, mode="markers", marker=dict(color="black", size=10)), row=i, col=1)
        fig.update_yaxes(range=[-0.012, 0.105], dtick=0.05, title="error (m/s)" if i == 2 else None, row=i, col=1)
    fig.update_xaxes(range=[-0.05, N * T + 0.05], dtick=0.5, title="time since the command (s)", row=3, col=1)
    top = (f"exact area under the curve: {exact:.4f} m" if last else
           f"{j} of {N} strips, one sample every 0.5 s")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1150, showlegend=False,
                      margin=dict(l=100, r=30, t=150, b=80), title=dict(x=0.5, y=0.975, text=top))
    fig.update_annotations(font=dict(size=21))
    return fig


figs = [frame(j) for j in range(N + 1)] + [frame(N, last=True)]
make_gif(figs, here / "integration_rules", fps=1, holds=[2] + [1] * N + [5], keys=[2, N + 1], cols=2, width=760)
