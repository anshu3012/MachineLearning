"""The mixed term can turn a bowl into a saddle (Plotly frames: a 3-D surface plus a chart of its slices).
f = x^2 + y^2 + p x y for p from 0 to 4. The slices along x and along y always curve up (second derivative 2), but the
diagonal slice has second derivative 2 - p: it flattens at p = 2 and curves down after. Readouts: the Hessian
[[2, p], [p, 2]], its eigenvalues 2 - p and 2 + p, and the test value f_xx f_yy - f_xy^2 = 4 - p^2.
Idea after Khan Academy, "Second partial derivative test". Run: python saddle_slider.py -> saddle_slider.gif, _frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT, GREEN, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
g = np.linspace(-1.5, 1.5, 50)
X, Y = np.meshgrid(g, g)
s = np.linspace(-1.5, 1.5, 80)
r2 = np.sqrt(2)


def frame(p):
    lam = np.linalg.eigvalsh(np.array([[2, p], [p, 2]]))
    assert np.allclose(lam, [2 - p, 2 + p]) and np.isclose(np.linalg.det([[2, p], [p, 2]]), 4 - p * p)
    f = lambda x, y: x ** 2 + y ** 2 + p * x * y
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "scene"}, {"type": "xy"}]], column_widths=[0.56, 0.44],
                        horizontal_spacing=0.06)
    fig.add_trace(go.Surface(x=X, y=Y, z=f(X, Y), colorscale="Blues", reversescale=True, showscale=False, opacity=0.55,
                             cmin=-3, cmax=12), row=1, col=1)
    z0 = 0 * s
    for xs, ys, col in ((s, z0, ORANGE), (z0, s, GREEN), (s / r2, -s / r2, RED)):
        fig.add_trace(go.Scatter3d(x=xs, y=ys, z=f(xs, ys), mode="lines", line=dict(color=col, width=9)), row=1, col=1)
    fig.add_trace(go.Scatter(x=s, y=s ** 2, line=dict(color=ORANGE, width=7)), row=1, col=2)
    fig.add_trace(go.Scatter(x=s, y=s ** 2, line=dict(color=GREEN, width=3, dash="dash")), row=1, col=2)
    fig.add_trace(go.Scatter(x=s, y=(1 - p / 2) * s ** 2, line=dict(color=RED, width=5)), row=1, col=2)
    fig.add_annotation(x=0, y=3.75, xref="x", yref="y", showarrow=False, font=dict(size=20, color=ORANGE),
                       text="slices along x and along y:<br>always curve up (2)")
    fig.add_annotation(x=0, y=2.85, xref="x", yref="y", showarrow=False, font=dict(size=20, color=RED),
                       text=f"diagonal slice: second derivative 2 − p = {2 - p:.1f}")
    fig.update_xaxes(title="distance along the slice", range=[-1.5, 1.5], row=1, col=2)
    fig.update_yaxes(title="height f", range=[-2.4, 4.3], zeroline=True, zerolinecolor="#CCCCCC", row=1, col=2)
    tick = dict(tickfont=dict(size=14))
    fig.update_scenes(xaxis=dict(title="x", nticks=4, **tick), yaxis=dict(title="y", nticks=4, **tick),
                      zaxis=dict(title="f", range=[-5, 13], nticks=4, **tick), aspectmode="manual",
                      aspectratio=dict(x=1, y=1, z=0.85), camera=dict(eye=dict(x=1.5, y=-1.35, z=0.7), center=dict(x=0, y=0, z=-0.12)))
    kind = "a bowl: minimum" if p < 2 else "flat along one diagonal: the test cannot tell" if p == 2 else "a saddle"
    fig.update_layout(template="simple_white", width=1100, height=640, font=FONT, showlegend=False,
                      margin=dict(l=0, r=20, t=135, b=65),
                      title=dict(x=0.5, y=0.95, font=dict(size=22),
                                 text=f"f = x² + y² + p·xy with <b>p = {p:.2f}</b>:  {kind}<br>"
                                      f"test value  f<sub>xx</sub>·f<sub>yy</sub> − f<sub>xy</sub>² = 4 − p² = <b>{4 - p * p:.2f}</b>"
                                      f"     Hessian eigenvalues: {2 - p:.2f} and {2 + p:.2f}"))
    return fig


ps = [0.25 * k for k in range(17)]
figs = [frame(p) for p in ps]
holds = [10 if p in (0, 2) else 14 if p == 4 else 2 for p in ps]
make_gif(figs, here / "saddle_slider", fps=6, holds=holds, keys=[0, ps.index(1.5), ps.index(2), len(ps) - 1], width=1000)
