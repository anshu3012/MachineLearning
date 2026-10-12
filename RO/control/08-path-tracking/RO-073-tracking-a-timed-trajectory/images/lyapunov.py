"""Kanayama's Lyapunov function on the run of Figure 5, one frame per 0.2 s for the first 6 s. Top: V = (x_e^2 + y_e^2)/2
+ (1 - cos th_e)/K_y and its two parts. Bottom: its rate from the formula, -K_x x_e^2 - v_r K_th sin^2 th_e / K_y,
never above zero. Start: V = 0.025 m^2, rate -0.040 m^2/s; V below 0.0001 m^2 from 3.15 s.
Run: python lyapunov.py -> lyapunov.gif, lyapunov_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, PURPLE, make_gif
from trackkit import DT, KTH, KX, KY, V_R, errors, kanayama, lyap, simulate

here = Path(__file__).parent
run = simulate(kanayama)
t = run["t"]
xe, ye, the, _ = errors(run)
V = lyap(xe, ye, the)
part_d = 0.5 * (xe ** 2 + ye ** 2)
part_h = (1 - np.cos(the)) / KY
rate = -KX * xe ** 2 - V_R * KTH * np.sin(the) ** 2 / KY
assert abs(V[0] - 0.025) < 1e-12 and abs(rate[0] + 0.04) < 1e-12 and np.all(rate <= 0)
assert abs(t[np.argmax(V < 1e-4)] - 3.15) < 1e-9 and abs(V[int(round(1 / DT))] - 0.0046) < 5e-5

steps = [int(round(s / DT)) for s in np.arange(0, 6.01, 0.2)]


def frame(k):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.6, 0.4], vertical_spacing=0.12)
    tt = t[:k + 1]
    fig.add_trace(go.Scatter(x=tt, y=V[:k + 1], mode="lines", line=dict(color=BLUE, width=5), name="V, the total"),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=tt, y=part_d[:k + 1], mode="lines", line=dict(color=GREEN, width=3, dash="dash"),
                             name="distance part (x<sub>e</sub>² + y<sub>e</sub>²) / 2"), row=1, col=1)
    fig.add_trace(go.Scatter(x=tt, y=part_h[:k + 1], mode="lines", line=dict(color=PURPLE, width=3, dash="dot"),
                             name="heading part (1 − cos θ<sub>e</sub>) / K<sub>y</sub>"), row=1, col=1)
    fig.add_trace(go.Scatter(x=[t[k]], y=[V[k]], mode="markers", marker=dict(color=BLUE, size=14), showlegend=False),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=tt, y=rate[:k + 1], mode="lines", line=dict(color="black", width=4),
                             name="rate of V (m² per s)"), row=2, col=1)
    fig.add_trace(go.Scatter(x=[0, 6], y=[0, 0], mode="lines", line=dict(color="#999999", width=2, dash="dash"),
                             showlegend=False), row=2, col=1)
    small = "<span style='font-size:19px'>"
    title = (f"t = {t[k]:.1f} s: V = {V[k]:.4f} m²<br>{small}falling at {-rate[k]:.4f} m² per s;"
             " the rate is never above zero</span>")
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1000, margin=dict(l=110, r=30, t=130, b=70),
                      title=dict(text=title, x=0.5, y=0.97, yanchor="top"),
                      legend=dict(x=0.42, y=0.98, font=dict(size=19), bgcolor="rgba(255,255,255,0.85)"))
    fig.update_xaxes(range=[0, 6], title="time (s)", row=1, col=1)
    fig.update_yaxes(range=[0, 0.027], title="V (m²)", row=1, col=1)
    fig.update_xaxes(range=[0, 6], title="time (s)", row=2, col=1)
    fig.update_yaxes(range=[-0.045, 0.005], title="rate of V (m²/s)", row=2, col=1)
    return fig


figs = [frame(k) for k in steps]
make_gif(figs, here / "lyapunov", fps=5, holds=[8] + [1] * (len(steps) - 2) + [16],
         keys=[0, 5, 15, len(steps) - 1], cols=2, width=800)
