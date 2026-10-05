"""The squared-error surface behind circle.tex: a bowl over two coefficients (beta1, beta2) whose contours are the
ellipses of the TikZ figure (centre = OLS answer (3, 2.2), tilted 30 degrees, axes ratio 2:1). Height = squared error
above its minimum, f = u^2 + 4 v^2 in the tilted coordinates (u, v). Left: surface; right: seen from above, with
the penalty circle and the two marked answers on both (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT
from surface_tilt import surface_traces, scene

here = Path(__file__).parent
C, A = np.array([3.0, 2.2]), np.radians(30)
def f(b1, b2):
    dx, dy = b1 - C[0], b2 - C[1]
    u, v = dx * np.cos(A) + dy * np.sin(A), -dx * np.sin(A) + dy * np.cos(A)
    return u ** 2 + 4 * v ** 2
x1, x2 = np.linspace(-2.2, 5, 90), np.linspace(-2.2, 4.2, 90)
Z = f(*np.meshgrid(x1, x2))
ridge = (1.127, 0.990)
print("f(0, 0) =", round(float(f(0, 0)), 1), " f(ridge) =", round(float(f(*ridge)), 2))
lv = (5.0, float(Z.max()), 5.0)
tr, zf = surface_traces(x1, x2, Z, lv, mark=tuple(C))
th = np.linspace(0, 2 * np.pi, 120)
circ = (1.5 * np.cos(th), 1.5 * np.sin(th))
tr.append(go.Scatter3d(x=circ[0], y=circ[1], z=[zf] * 120, mode="lines", line=dict(color="#F58518", width=6)))
tr.append(go.Scatter3d(x=[ridge[0]] * 2, y=[ridge[1]] * 2, z=[float(f(*ridge)), zf], mode="lines+markers",
                       line=dict(color="#E45756", width=4), marker=dict(size=4, color="#E45756")))
fig = make_subplots(1, 2, specs=[[{"type": "scene"}, {}]], horizontal_spacing=0.08,
                    subplot_titles=("the surface: height = squared error", "the same surface seen from above"))
for t in tr:
    fig.add_trace(t, 1, 1)
fig.update_scenes(scene(x1, x2, Z, zf, "β1", "β2", "squared error", (1.6, -1.5, 1.0), 4), row=1, col=1)
fig.add_trace(go.Contour(x=x1, y=x2, z=Z, showscale=False, colorscale="Blues", reversescale=True,
                         contours=dict(start=lv[0], end=lv[1], size=lv[2]), line=dict(width=0.8)), 1, 2)
fig.add_trace(go.Scatter(x=circ[0], y=circ[1], mode="lines", line=dict(color="#F58518", width=4)), 1, 2)
fig.add_trace(go.Scatter(x=[C[0]], y=[C[1]], mode="markers", marker=dict(size=11, color="black", symbol="x")), 1, 2)
fig.add_trace(go.Scatter(x=[ridge[0]], y=[ridge[1]], mode="markers", marker=dict(size=11, color="#E45756")), 1, 2)
fig.update_xaxes(title="β1", range=[-2.2, 5], row=1, col=2)
fig.update_yaxes(title="β2", range=[-2.2, 4.2], scaleanchor="x2", row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=520, showlegend=False, font=dict(FONT, size=16),
                  margin=dict(l=10, r=20, t=50, b=60))
fig.update_annotations(font_size=18)
fig.write_image(here / "circle_surface.png", scale=2)
fig.write_image(here / "circle_surface.pdf")
