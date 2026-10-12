"""What the normalizer eta does. The Gaussian part for a wall 4.98 m away (sigma 0.05 m) is cut at the maximum range
z_max = 5 m: the area inside 0 to 5 m is 0.655, the 0.345 beyond 5 m is cut off. Multiplying every height inside by
eta = 1 / 0.655 = 1.53 gives the black curve, whose area is 1 again (peak 7.98 -> 12.2 per m). Run -> eta_cut.png"""
from math import erf, sqrt
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from beammodel import SIG_HIT, ZMAX, gauss, p_hit
from gifkit import BLUE, FONT, GREY

here = Path(__file__).parent
ZW = 4.98                                                   # the wall, 0.4 sigma in front of z_max
inside = 0.5 * (erf((ZMAX - ZW) / (SIG_HIT * sqrt(2))) + erf(ZW / (SIG_HIT * sqrt(2))))
eta = 1 / inside
peak = float(gauss(ZW, ZW, SIG_HIT))
zi = np.linspace(4.7, ZMAX, 600)
zo = np.linspace(ZMAX, 5.25, 300)
fig = go.Figure()
fig.add_trace(go.Scatter(x=zi, y=gauss(zi, ZW, SIG_HIT), mode="lines", fill="tozeroy", fillcolor="rgba(76,120,168,0.25)",
                         line=dict(color=BLUE, width=3, simplify=False)))
fig.add_trace(go.Scatter(x=zo, y=gauss(zo, ZW, SIG_HIT), mode="lines", fill="tozeroy", fillcolor="rgba(107,107,107,0.35)",
                         line=dict(color=BLUE, width=3, dash="dash")))
fig.add_trace(go.Scatter(x=np.concatenate([zi, [ZMAX]]), y=np.concatenate([p_hit(zi, ZW), [0]]), mode="lines",
                         line=dict(color="black", width=4, simplify=False)))
fig.add_vline(x=ZMAX, line=dict(color=GREY, dash="dot", width=2))
fig.add_annotation(x=ZMAX, y=13.8, text="z<sub>max</sub> = 5 m", showarrow=False, xanchor="left", font=dict(color=GREY, size=20))
fig.add_annotation(x=ZW, y=12.5, ax=-20, ay=-38, text="wall z* = 4.98 m", xanchor="right", font=dict(color=BLUE, size=20),
                   arrowcolor=BLUE, arrowwidth=2)
for y, txt, col in [(11.6, f"black: inside part × η = {eta:.2f}", "black"),
                    (10.7, f"peak {peak * eta:.1f} per m, area 1", "black"),
                    (9.0, "blue: Gaussian around 4.98 m,", BLUE),
                    (8.1, f"σ = {SIG_HIT} m, peak {peak:.2f} per m", BLUE),
                    (6.4, "light blue: area inside 5 m", BLUE)]:
    fig.add_annotation(x=4.705, y=y, text=txt, showarrow=False, xanchor="left", font=dict(color=col, size=20))
for y, txt in [(8.0, "grey: area beyond 5 m,"), (7.1, "cut off")]:
    fig.add_annotation(x=5.065, y=y, text=txt, showarrow=False, xanchor="left", font=dict(color=GREY, size=20))
fig.add_annotation(x=4.963, y=1.3, text=f"{inside:.3f}", showarrow=False, font=dict(color=BLUE, size=20))
fig.add_annotation(x=5.024, y=1.1, text=f"{1 - inside:.3f}", showarrow=False, font=dict(color="black", size=20))
fig.update_layout(template="simple_white", width=900, height=520, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=30, b=70))
fig.update_xaxes(title="reading z (m)", range=[4.7, 5.25], dtick=0.05)
fig.update_yaxes(title="density (per m)", range=[0, 14.5])
fig.write_image(here / "eta_cut.png", scale=1)
assert round(inside, 3) == 0.655 and round(1 - inside, 3) == 0.345 and round(eta, 2) == 1.53 and round(1 / 0.655, 2) == 1.53
assert round(peak, 2) == 7.98 and round(peak * eta, 1) == 12.2 and round(7.98 * 1.53, 1) == 12.2
area = np.trapezoid(p_hit(np.linspace(0, ZMAX, 200001), ZW), dx=ZMAX / 200000)
assert abs(area - 1) < 1e-3                               # the rescaled curve has area 1
