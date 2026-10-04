"""Second-order test on two quadratics (Plotly contour maps). Left: x^2 + xy + y^2, Hessian eigenvalues 1 and 3, both
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
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                    subplot_titles=("x² + xy + y²: eigenvalues 1, 3 → bowl", "x² + 3xy + y²: eigenvalues 5, −1 → saddle"))
for c, (f, H, col) in enumerate(funs, start=1):
    fig.add_trace(go.Contour(x=g, y=g, z=f(X, Y), colorscale="RdBu", reversescale=True, zmid=0, showscale=False,
                             contours=dict(start=-8, end=12, size=1), line=dict(width=0.6), opacity=0.8), 1, c)
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
                             marker=dict(size=12, color="black")), 1, c)
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers+text", text=["0"], textposition="middle left",
                             textfont=dict(size=20, color=col), marker=dict(size=12, color=col)), 1, c)
fig.add_annotation(x=0, y=-1.75, text="chord midpoint −1 < value 0 at (0, 0)", showarrow=False, bgcolor="white",
                   font=dict(color=RED, size=20), xref="x2", yref="y2")
fig.add_annotation(x=0, y=-1.75, text="chord midpoint 1 ≥ value 0 at (0, 0)", showarrow=False, bgcolor="white",
                   font=dict(color=GREEN, size=20), xref="x1", yref="y1")
fig.update_xaxes(title_text="x", range=[-2, 2])
fig.update_yaxes(title_text="y", range=[-2, 2])
fig.update_yaxes(scaleanchor="x", row=1, col=1)
fig.update_yaxes(scaleanchor="x2", row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=600, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=60, r=20, t=50, b=60))
fig.update_annotations(font_size=21)
fig.write_image(HERE / "hessian_bowl_saddle.png", scale=2)
fig.write_image(HERE / "hessian_bowl_saddle.pdf")
