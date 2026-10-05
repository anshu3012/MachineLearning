"""The squared-error surface behind the contour maps of this Note (100-point example, log of the sum of squared
errors over slope m and intercept b). Left: the surface; right: the same surface seen from above, with the two arrows
of the Ridge step (old w -> shrink -> new w) on both (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ridge_race import ms, bs, Z, paths
from gifkit import FONT
from surface_tilt import surface_traces, scene

here = Path(__file__).parent
eta, lam = 0.005, 100
old, new = paths[100][0], paths[100][1]
shr = np.array([(1 - eta * lam) * old[0], old[1]])
lv = (float(Z.min()) + 0.05, float(Z.max()), 0.25)
route = np.array([old, shr, new])
tr, zf = surface_traces(ms, bs, Z, lv, path=route, lift=0.1)
fig = make_subplots(1, 2, specs=[[{"type": "scene"}, {}]], horizontal_spacing=0.08,
                    subplot_titles=("the surface: height = log of the squared error", "the same surface seen from above"))
for t in tr:
    fig.add_trace(t, 1, 1)
fig.update_scenes(scene(ms, bs, Z, zf, "m", "b", "log error", (1.5, -1.6, 1.0), 3), row=1, col=1)
fig.add_trace(go.Contour(x=ms, y=bs, z=Z, showscale=False, colorscale="Blues", reversescale=True,
                         contours=dict(start=lv[0], end=lv[1], size=lv[2]), line=dict(width=0.8)), 1, 2)
fig.add_trace(go.Scatter(x=route[:, 0], y=route[:, 1], mode="lines+markers", line=dict(color="#F58518", width=4),
                         marker=dict(size=9, color="#F58518")), 1, 2)
fig.update_xaxes(title="slope m", range=[ms[0], ms[-1]], row=1, col=2)
fig.update_yaxes(title="intercept b", range=[bs[0], bs[-1]], row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=500, showlegend=False, font=dict(FONT, size=16),
                  margin=dict(l=10, r=20, t=50, b=60))
fig.update_annotations(font_size=17)
fig.write_image(here / "surface_panel.png", scale=2)
fig.write_image(here / "surface_panel.pdf")
