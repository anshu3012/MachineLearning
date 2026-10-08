"""The four parts of the beam model for the beam whose expected range is 3 m (z_max = 5 m):
measurement noise (Gaussian, sigma 0.05), unexpected objects (exponential, lambda 2, stops at 3 m),
failures (spike at 5 m, drawn one 1 cm step wide), random readings (uniform 1/5). Run -> four_parts.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from beammodel import ZMAX, ZSTAR, p_hit, p_max, p_rand, p_short
from gifkit import BLUE, FONT, GREEN, ORANGE, PURPLE, GREY

here = Path(__file__).parent
z = np.concatenate([np.linspace(0, 4.99, 5000), [4.9949, 4.995, 5.0]])
parts = [("1. measurement noise p<sub>hit</sub>", p_hit(z, ZSTAR), BLUE, [0, 9]),
         ("2. unexpected objects p<sub>short</sub>", p_short(z, ZSTAR), ORANGE, [0, 2.3]),
         ("3. failures p<sub>max</sub> (spike at z<sub>max</sub>)", p_max(z), PURPLE, [0, 110]),
         ("4. random readings p<sub>rand</sub>", p_rand(z), GREEN, [0, 0.3])]
fig = make_subplots(rows=2, cols=2, subplot_titles=[p[0] for p in parts], horizontal_spacing=0.1, vertical_spacing=0.2)
for i, (name, y, c, yr) in enumerate(parts):
    r, cc = i // 2 + 1, i % 2 + 1
    fig.add_trace(go.Scatter(x=z, y=y, mode="lines", line=dict(color=c, width=3), fill="tozeroy"), row=r, col=cc)
    for x0, lab in ((ZSTAR, "z*"), (ZMAX, "z<sub>max</sub>")):
        fig.add_vline(x=x0, line=dict(color=GREY, dash="dot", width=1.5), row=r, col=cc)
    fig.update_yaxes(range=yr, title="density (per m)" if cc == 1 else None, row=r, col=cc)
    fig.update_xaxes(range=[0, 5.1], dtick=1, title="reading z (m)" if r == 2 else None, row=r, col=cc)
fig.update_layout(template="simple_white", width=1100, height=750, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=60, b=70))
fig.update_annotations(selector=dict(yref="paper"), font_size=21)
fig.add_annotation(x=3.0, y=8.5, xref="x", yref="y", text="z* = 3 m", showarrow=False, xanchor="left", font_size=17)
fig.add_annotation(x=5.0, y=105, xref="x3", yref="y3", text="height 100, width 0.01 m: area 1", showarrow=False,
                   xanchor="right", font_size=17)
fig.write_image(here / "four_parts.png", scale=1)
