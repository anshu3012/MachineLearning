"""Weighing five particles by the first reading z = 1.46 m. A particle in front of a door expects 1.5 m, one beside
plain wall expects 1.0 m. Its weight is the height of the sensor's normal curve (sd 0.15 m), centred on the reading
it expects, at the reading we got: 2.567 for a door particle, 0.024 for a wall particle.
Run: python weight_by_hand.py -> weight_by_hand.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, RED
from pfsim import DOORS, SIGMA_Z, h, likelihood

here = Path(__file__).parent
P = np.array([0.7, 1.6, 2.4, 3.3, 6.9])
Z1 = 1.46
lik = likelihood(Z1, P)
w = lik / lik.sum()
assert np.allclose(lik.round(3), [0.024, 2.567, 2.567, 0.024, 2.567]) and np.allclose(w.round(4), [0.0031, 0.3313, 0.3313, 0.0031, 0.3313])

fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45], horizontal_spacing=0.1,
                    subplot_titles=["five particles on the corridor (doors shaded)",
                                    "sensor curve centred on the expected reading"])
for a, b in DOORS:
    fig.add_shape(type="rect", x0=a, x1=b, y0=0, y1=1, fillcolor=ORANGE, opacity=0.2, line_width=0, layer="below", row=1, col=1)
cols = [BLUE if h(np.array([p]))[0] == 1.5 else GREY for p in P]
fig.add_trace(go.Scatter(x=P, y=[0.5] * 5, mode="markers+text", marker=dict(size=22, color=cols),
                         text=[str(i + 1) for i in range(5)], textposition="top center",
                         textfont=dict(size=20)), row=1, col=1)
fig.add_annotation(x=5, y=0.15, text="blue: in front of a door, expects 1.5 m<br>grey: beside plain wall, expects 1.0 m",
                   showarrow=False, font=dict(size=17), row=1, col=1)
zz = np.linspace(0.4, 2.1, 400)
for mu, c, name in ((1.5, BLUE, "door particle"), (1.0, GREY, "wall particle")):
    fig.add_trace(go.Scatter(x=zz, y=np.exp(-0.5 * ((zz - mu) / SIGMA_Z) ** 2) / (SIGMA_Z * np.sqrt(2 * np.pi)),
                             mode="lines", line=dict(color=c, width=4)), row=1, col=2)
    val = np.exp(-0.5 * ((Z1 - mu) / SIGMA_Z) ** 2) / (SIGMA_Z * np.sqrt(2 * np.pi))
    fig.add_trace(go.Scatter(x=[Z1, Z1], y=[0, val], mode="lines", line=dict(color=c, width=6)), row=1, col=2)
    fig.add_annotation(x=Z1, y=val, text=f"{name}: height {val:.3f}", showarrow=True, ax=-150 if mu == 1.5 else 120,
                       ay=-10 if mu == 1.5 else -60, font=dict(size=16, color=c), row=1, col=2)
fig.add_vline(x=Z1, line=dict(color=RED, width=2, dash="dash"), row=1, col=2)
fig.add_annotation(x=Z1 + 0.03, y=2.95, xanchor="left", text="reading z = 1.46 m", showarrow=False, font=dict(size=16, color=RED), row=1, col=2)
fig.update_xaxes(title="position x (m)", range=[0, 10], dtick=2, row=1, col=1)
fig.update_yaxes(visible=False, range=[0, 1], row=1, col=1)
fig.update_xaxes(title="reading (m)", range=[0.4, 2.1], row=1, col=2)
fig.update_yaxes(title="density p(z | x)", range=[0, 3.1], row=1, col=2)
fig.update_layout(template="simple_white", font=FONT, width=1250, height=520, showlegend=False,
                  margin=dict(l=40, r=30, t=70, b=60))
fig.update_annotations(selector=dict(yref="paper"), font_size=19)
fig.write_image(here / "weight_by_hand.png")
