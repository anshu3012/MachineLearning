"""The two Gaussians of the pink pole's reading at pose A. Left: the range error, sigma_r = 0.1 m; the error 0.10 m
lands at 2.420 per m. Right: the bearing error, sigma_phi = 5 deg; the error 3.13 deg lands at 3.758 per rad.
The density of the reading is the product of the two heights, 9.09. Run -> two_gauss.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE
from lmmodel import LM, POSE_A, READ, SIG_PHI, SIG_R, expected, gauss, landmark_density, wrap
from plotly.subplots import make_subplots

here = Path(__file__).parent
r, phi = READ["pink"]
r_hat, phi_hat = expected(POSE_A, LM["pink"])
e_r, e_phi = r - r_hat, wrap(phi - phi_hat)
h_r, h_phi = gauss(e_r, SIG_R), gauss(e_phi, SIG_PHI)
assert round(e_r, 2) == 0.10 and round(np.degrees(e_phi), 2) == 3.13
assert round(h_r, 3) == 2.420 and round(h_phi, 3) == 3.758
assert round(h_r * h_phi, 2) == round(landmark_density(POSE_A, "pink"), 2) == 9.09

panels = [  # (x values, density, error, height, x label, unit, colour, x tick step = sigma)
    (np.linspace(-0.35, 0.35, 401), lambda v: gauss(v, SIG_R), e_r, h_r, "range error (m)", "per m", BLUE, 0.1,
     f"error 0.10 m<br>height {h_r:.3f} per m"),
    (np.linspace(-17.5, 17.5, 401), lambda v: gauss(np.radians(v), SIG_PHI), np.degrees(e_phi), h_phi,
     "bearing error (degrees)", "per rad", ORANGE, 5, f"error 3.13°<br>height {h_phi:.3f} per rad"),
]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=["range: σ<sub>r</sub> = 0.1 m", "bearing: σ<sub>φ</sub> = 5° = 0.0873 rad"])
for k, (xs, f, e, h, xlab, unit, col, step, txt) in enumerate(panels, start=1):
    fig.add_trace(go.Scatter(x=xs, y=f(xs), mode="lines", line=dict(color=col, width=4, simplify=False)), 1, k)
    fig.add_trace(go.Scatter(x=[e, e], y=[0, h], mode="lines", line=dict(color=GREY, width=2, dash="dash")), 1, k)
    fig.add_trace(go.Scatter(x=[e], y=[h], mode="markers", marker=dict(size=16, color="black")), 1, k)
    fig.add_annotation(x=e, y=h, text=txt, showarrow=False, xanchor="left", yanchor="bottom", xshift=12, yshift=4,
                       align="left", font=dict(size=20), row=1, col=k)
    fig.update_xaxes(title=xlab, dtick=step, row=1, col=k)
    fig.update_yaxes(title=f"density ({unit})", range=[0, 5.3], dtick=1, row=1, col=k)
fig.update_layout(template="simple_white", width=1200, height=520, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=70, b=80))
fig.update_annotations(font_size=21)
fig.write_image(here / "two_gauss.png")
print(f"range error {e_r:.2f} m -> {h_r:.3f} per m; bearing error {np.degrees(e_phi):.2f} deg -> {h_phi:.3f} per rad;"
      f" product {h_r * h_phi:.2f}")
