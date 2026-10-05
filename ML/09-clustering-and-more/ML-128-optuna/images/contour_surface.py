"""The surface behind contour.png: score of the TPE study's trials (n_estimators across, max_depth up), filled in
between the trials by straight-line interpolation. Left: surface (height = 3-fold CV accuracy); right: the same
surface seen from above with the trials as dots (Plotly)."""
from pathlib import Path
import numpy as np
import optuna
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.interpolate import griddata
from gifkit import FONT
from surface_tilt import scene

here = Path(__file__).parent
optuna.logging.set_verbosity(optuna.logging.WARNING)
tpe = optuna.load_study(study_name="tpe", storage=f"sqlite:///{here.parent / 'data' / 'optuna.db'}")
T = [(t.params["n_estimators"], t.params["max_depth"], t.value) for t in tpe.trials if t.value is not None]
n, d, v = (np.array(a, float) for a in zip(*T))
gx, gy = np.linspace(n.min(), n.max(), 80), np.linspace(d.min(), d.max(), 80)
GX, GY = np.meshgrid(gx, gy)
Z = griddata((n, d), v, (GX, GY), method="linear")
zmin, zmax = float(np.nanmin(Z)), float(np.nanmax(Z))
zf = zmin - 0.25 * (zmax - zmin)
i = int(np.argmax(v))
print("trials", len(v), "best", round(v[i], 4), "at n_estimators", n[i], "max_depth", d[i], "range", round(zmin, 3), round(zmax, 3))
lv = dict(start=round(zmin, 2), end=zmax, size=round((zmax - zmin) / 8, 3))
fig = make_subplots(1, 2, specs=[[{"type": "scene"}, {}]], horizontal_spacing=0.08,
                    subplot_titles=("the surface: height = accuracy", "the same surface seen from above"))
fig.add_trace(go.Surface(x=gx, y=gy, z=Z, colorscale="Blues", showscale=False, cmin=zmin, cmax=zmax,
                         contours=dict(z=dict(show=True, color="#1F3B5C", width=2, usecolormap=False,
                                              project=dict(z=True), **lv))), 1, 1)
fig.add_trace(go.Scatter3d(x=n, y=d, z=v, mode="markers", marker=dict(size=3, color="black")), 1, 1)
fig.add_trace(go.Scatter3d(x=[n[i]] * 2, y=[d[i]] * 2, z=[v[i], zf], mode="lines+markers",
                           line=dict(color="#E45756", width=5), marker=dict(size=5, color="#E45756")), 1, 1)
sc = scene(gx, gy, Z, zf, "n_estimators", "max_depth", "accuracy", (1.7, -1.6, 1.0), 4)
sc["zaxis"]["range"] = [zf, zmax]
fig.update_scenes(sc, row=1, col=1)
fig.add_trace(go.Contour(x=gx, y=gy, z=Z, colorscale="Blues", showscale=False, zmin=zmin, zmax=zmax,
                         contours=lv, line=dict(width=0.8)), 1, 2)
fig.add_trace(go.Scatter(x=n, y=d, mode="markers", marker=dict(size=6, color="black")), 1, 2)
fig.add_trace(go.Scatter(x=[n[i]], y=[d[i]], mode="markers", marker=dict(size=12, color="#E45756")), 1, 2)
fig.update_xaxes(title="n_estimators", row=1, col=2)
fig.update_yaxes(title="max_depth", row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=500, showlegend=False, font=dict(FONT, size=16),
                  margin=dict(l=10, r=20, t=50, b=60))
fig.update_annotations(font_size=18)
fig.write_image(here / "contour_surface.png", scale=2)
fig.write_image(here / "contour_surface.pdf")
