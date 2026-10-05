"""The loss surface behind the contour maps of this Note: mean squared error of the 100-point example over (m, b).
Left: the surface with contour lines on it and on the floor. Right: the same surface seen from above (contour map).
Same colours, same start (grey square) and same minimum (black cross) on both (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import make_regression
from gifkit import FONT
from surface_tilt import surface_traces, scene

HERE = Path(__file__).parent
X, y = make_regression(n_samples=100, n_features=1, n_informative=1, n_targets=1, noise=20, random_state=13)
x = X.ravel()
bm, bb = np.polyfit(x, y, 1)
mg, bg = np.linspace(-150, 150, 90), np.linspace(-150, 170, 90)
Z = np.array([[np.mean((y - m * x - b) ** 2) for m in mg] for b in bg])
lv = (float(Z.min()), float(Z.max()), (float(Z.max()) - float(Z.min())) / 20)
tr, zf = surface_traces(mg, bg, Z, lv, mark=(bm, bb), start=(-127.82, 150.0))
fig = make_subplots(1, 2, specs=[[{"type": "scene"}, {}]], column_widths=[0.5, 0.5], horizontal_spacing=0.08,
                    subplot_titles=("the surface: height = loss", "the same surface seen from above"))
for t in tr:
    fig.add_trace(t, 1, 1)
fig.update_scenes(scene(mg, bg, Z, zf, "m", "b", "loss", (1.5, -1.5, 1.1), 3), row=1, col=1)
fig.add_trace(go.Contour(x=mg, y=bg, z=Z, colorscale="Blues", reversescale=True, showscale=False,
                         contours=dict(start=lv[0], end=lv[1], size=lv[2]), line=dict(width=0.5)), 1, 2)
fig.add_trace(go.Scatter(x=[bm], y=[bb], mode="markers", marker=dict(size=14, color="black", symbol="x")), 1, 2)
fig.add_trace(go.Scatter(x=[-127.82], y=[150], mode="markers", marker=dict(size=11, color="#6B6B6B", symbol="square")), 1, 2)
fig.update_xaxes(title="m (slope)", row=1, col=2)
fig.update_yaxes(title="b (intercept)", row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=500, showlegend=False, font=dict(FONT, size=16),
                  margin=dict(l=10, r=20, t=50, b=60))
fig.update_annotations(font_size=18)
fig.write_image(HERE / "surface_panel.png", scale=2)
fig.write_image(HERE / "surface_panel.pdf")
