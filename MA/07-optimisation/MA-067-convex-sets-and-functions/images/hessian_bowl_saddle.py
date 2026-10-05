"""Second-order test on two quadratics (Plotly: the 3-D surfaces on top, the same surfaces seen from above as contour maps below). Left: x^2 + xy + y^2, Hessian eigenvalues 1 and 3, both
positive: closed ellipses, a bowl. Right: x^2 + 3xy + y^2, eigenvalues 5 and -1: hyperbolas, a saddle. Arrows: the
eigenvector directions, labelled with the curvature along them. On the saddle, the chord from (1, -1) to (-1, 1) (both
value -1) has midpoint chord value -1, below the function's value 0 at (0, 0): not convex."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
funs = [(lambda x, y: x ** 2 + x * y + y ** 2, np.array([[2, 1], [1, 2]]), GREEN),
        (lambda x, y: x ** 2 + 3 * x * y + y ** 2, np.array([[2, 3], [3, 2]]), RED)]
assert np.allclose(np.linalg.eigvalsh(funs[0][1]), [1, 3]) and np.allclose(np.linalg.eigvalsh(funs[1][1]), [-1, 5])
assert funs[0][0](1, -1) == 1 and funs[1][0](1, -1) == funs[1][0](-1, 1) == -1 and funs[1][0](0, 0) == 0

g = np.linspace(-2, 2, 201)
X, Y = np.meshgrid(g, g)
fig = make_subplots(rows=2, cols=2, horizontal_spacing=0.08, vertical_spacing=0.05,
                    specs=[[{"type": "scene"}, {"type": "scene"}], [{"type": "xy"}, {"type": "xy"}]],
                    subplot_titles=("x² + xy + y²: the surface, a bowl", "x² + 3xy + y²: the surface, a saddle",
                                    "the same surface from above: eigenvalues 1, 3", "the same surface from above: eigenvalues 5, −1"))
LINES = dict(show=True, usecolormap=False, color="#444444", width=2, start=-8, end=12, size=1, project=dict(z=True))
for c, (f, H, col) in enumerate(funs, start=1):
    D = float(np.abs(f(X, Y)).max())
    fig.add_trace(go.Surface(x=g[::3], y=g[::3], z=np.minimum(f(X, Y), 8)[::3, ::3], colorscale="RdBu", reversescale=True, cmin=-D, cmax=D, showscale=False,
                             contours=dict(z=LINES), lighting=dict(ambient=1, diffuse=0.1, specular=0)), 1, c)
    e = f(1, -1)
    fig.add_trace(go.Scatter3d(x=[1, -1], y=[-1, 1], z=[e, e], mode="lines+markers", line=dict(color="black", width=6),
                               marker=dict(size=4, color="black")), 1, c)
    fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0.05], mode="markers", marker=dict(size=6, color=col)), 1, c)
    fig.add_trace(go.Contour(x=g, y=g, z=f(X, Y), colorscale="RdBu", reversescale=True, zmin=-D, zmax=D, showscale=False,
                             contours=dict(start=-8, end=12, size=1), line=dict(width=0.6), opacity=0.8), 2, c)
    vals, vecs = np.linalg.eigh(H)
    for lam, v in zip(vals, vecs.T):
        v = v * np.sign(v[0] + 1e-9) * 1.6
        fig.add_annotation(x=v[0], y=v[1], ax=0, ay=0, axref=f"x{c}", ayref=f"y{c}", xref=f"x{c}", yref=f"y{c}",
                           showarrow=True, arrowhead=2, arrowwidth=3, arrowcolor="black", text="")
        fig.add_annotation(x=1.22 * v[0], y=1.22 * v[1], xref=f"x{c}", yref=f"y{c}", showarrow=False, bgcolor="white",
                           text=f"<b>{'+' if lam > 0 else '−'}{abs(lam):g}</b>", font=dict(size=22, color="black"))
    end = f(1, -1)
    fig.add_trace(go.Scatter(x=[1, -1], y=[-1, 1], mode="markers+text", text=[f"{end:g}".replace("-", "−")] * 2,
                             textposition="bottom center", textfont=dict(size=20, color="black"),
                             marker=dict(size=12, color="black")), 2, c)
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers+text", text=["0"], textposition="middle left",
                             textfont=dict(size=20, color=col), marker=dict(size=12, color=col)), 2, c)
    fig.update_layout({"scene" if c == 1 else "scene2": dict(
        xaxis=dict(title="x", showbackground=False, tickfont=dict(size=13)), yaxis=dict(title="y", showbackground=False, tickfont=dict(size=13)),
        zaxis=dict(title="f", range=[-5, 9], showbackground=False, tickfont=dict(size=13)),
        camera=dict(eye=dict(x=-1.5, y=1.5, z=0.8), projection=dict(type="orthographic")),
        aspectmode="manual", aspectratio=dict(x=1, y=1, z=0.7))})
fig.add_annotation(x=0, y=-1.75, text="chord midpoint −1 < value 0 at (0, 0)", showarrow=False, bgcolor="white",
                   font=dict(color=RED, size=20), xref="x2", yref="y2")
fig.add_annotation(x=0, y=-1.75, text="chord midpoint 1 ≥ value 0 at (0, 0)", showarrow=False, bgcolor="white",
                   font=dict(color=GREEN, size=20), xref="x1", yref="y1")
fig.update_xaxes(title_text="x", range=[-2, 2], row=2)
fig.update_yaxes(range=[-2, 2], row=2)
fig.update_yaxes(title_text="y", row=2, col=1)
fig.update_yaxes(scaleanchor="x", row=2, col=1)
fig.update_yaxes(scaleanchor="x2", row=2, col=2)
fig.update_layout(template="simple_white", width=1150, height=1150, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=60, r=20, t=50, b=60))
fig.update_annotations(font_size=21)
fig.write_image(HERE / "hessian_bowl_saddle.png", scale=2)
fig.write_image(HERE / "hessian_bowl_saddle.pdf")
