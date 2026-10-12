"""The PI controller as code, one tick per frame at 10 Hz: read the speed (A/D), compute the error and the force,
send the force out (D/A, held for 0.1 s), then update the integral. Top: the four lines of the tick with this tick's
numbers. Middle: the true speed (line) and the readings (dots). Bottom: the force staircase. Ticks 0 to 10.
Run: python pi_code_anim.py -> pi_code_anim.gif, pi_code_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from digikit import R1, sampled_loop
from robotctl import KI, KP
from gifkit import FONT, GREEN, ORANGE, make_gif

here = Path(__file__).parent
TS, N = 0.1, 10
r = sampled_loop(10, T=1.1, digits=4)          # the A/D reads to 0.0001 m/s
tk, yk, ek, uk, ik = r["tk"], r["yk"], r["ek"], r["uk"], r["ik"]
assert abs(uk[0] - 2.8) < 1e-9 and abs(ik[1] - 0.9) < 1e-9 and abs(yk[1] - 0.4247) < 1e-12 and abs(uk[1] - 2.406) < 1e-12


def ex(x):
    """An exact decimal with at most 5 places, trailing zeros dropped."""
    return f"{x:.5f}".rstrip("0").rstrip(".")


def lines(k):
    v, e, I = yk[k], ek[k], ik[k]
    u, Inext = KP * e + I, I + KI * TS * e
    # every number is shown exactly (the reading has 4 decimals), so the shown arithmetic reproduces the results
    assert abs(u - uk[k]) < 1e-12 and abs(round(Inext, 5) - Inext) < 1e-12 and abs(round(u, 5) - u) < 1e-12
    es = f"{e:.4f}".replace("-", "−")
    ep = f"({es})" if e < 0 else es                      # a negative factor in brackets
    return [f"<b>tick k = {k}, t = {tk[k]:.1f} s</b>",
            f"1. read the speed:  v = {v:.4f} m/s",
            f"2. error:  e = 0.5 − {v:.4f} = {es} m/s",
            f"3. force:  u = {KP:g} × {ep} + {ex(I)} = {ex(u)} N, sent to the D/A",
            f"4. integral:  I = {ex(I)} + {KI:g} × 0.1 × {ep} = {ex(Inext)} N"]


def frame(k):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08,
                        subplot_titles=["speed: true (line) and readings (dots)", "force sent out, held 0.1 s"])
    m = r["t"] <= tk[k] + TS - 1e-9
    fig.add_trace(go.Scatter(x=r["t"][m], y=r["v"][m], mode="lines", line=dict(color=GREEN, width=4)), row=1, col=1)
    fig.add_trace(go.Scatter(x=tk[:k + 1], y=yk[:k + 1], mode="markers",
                             marker=dict(color=GREEN, size=13, line=dict(color="white", width=2))), row=1, col=1)
    xs, ys = [], []
    for j in range(k + 1):
        xs += [tk[j], tk[j] + TS]
        ys += [uk[j], uk[j]]
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=ORANGE, width=5)), row=2, col=1)
    fig.add_trace(go.Scatter(x=[tk[k]], y=[uk[k]], mode="markers",
                             marker=dict(color=ORANGE, size=14, line=dict(color="white", width=2))), row=2, col=1)
    fig.update_yaxes(range=[0.395, 0.51], title="speed (m/s)", row=1, col=1)
    fig.update_yaxes(range=[0.9, 2.9], title="force (N)", row=2, col=1)
    fig.update_xaxes(range=[-0.03, 1.13], dtick=0.1, title="time since the command (s)", row=2, col=1)
    fig.add_annotation(xref="paper", yref="paper", x=0.0, y=1.33, xanchor="left", yanchor="top", align="left",
                       showarrow=False, text="<br>".join(lines(k)), font=dict(size=21),
                       bgcolor="rgba(240,240,240,0.9)", borderpad=8)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1000, showlegend=False,
                      margin=dict(l=100, r=30, t=290, b=80))
    fig.update_annotations(font=dict(size=21))
    return fig


figs = [frame(k) for k in range(N + 1)]
make_gif(figs, here / "pi_code_anim", fps=1, holds=[3] + [1] * (N - 1) + [5], keys=[1, N], cols=2, width=760)
