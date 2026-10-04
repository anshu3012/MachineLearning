"""The Taylor polynomials of f(x, y) = x^3 + xy + y^2 around (1, 1), watched along the path to (1.5, 0.5)
(Plotly frames -> GIF). Left: the contour map with the moving point. Right: f along the path and T1, T2, T3; at
(1.1, 0.9) they read 3.1, 3.13, 3.131 and at (1.5, 0.5) 3.5, 4.25, 4.375; T3 always equals f."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, ORANGE, PURPLE, make_gif

here = Path(__file__).parent
f = lambda x, y: x ** 3 + x * y + y ** 2
T1 = lambda x, y: 3 + 4 * (x - 1) + 3 * (y - 1)
T2 = lambda x, y: T1(x, y) + 3 * (x - 1) ** 2 + (x - 1) * (y - 1) + (y - 1) ** 2
T3 = lambda x, y: T2(x, y) + (x - 1) ** 3
for (x, y), want in (((1.1, 0.9), (3.1, 3.13, 3.131)), ((1.5, 0.5), (3.5, 4.25, 4.375))):
    assert np.allclose([T1(x, y), T2(x, y), T3(x, y)], want) and np.isclose(T3(x, y), f(x, y))
ts = np.linspace(0, 0.5, 101)
path = [(1 + t, 1 - t) for t in ts]
g = np.linspace(0.3, 1.7, 141)
X, Y = np.meshgrid(g, g)
SHOW = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]


def frame(k):
    t = ts[k]
    x, y = path[k]
    fig = make_subplots(1, 2, column_widths=[0.42, 0.58], horizontal_spacing=0.1,
                        subplot_titles=[f"the point ({x:.2f}, {y:.2f})", "f and its Taylor polynomials along the path"])
    fig.update_annotations(font_size=21)
    fig.add_trace(go.Contour(x=g, y=g, z=f(X, Y), colorscale="Blues", reversescale=True, showscale=False, opacity=0.6,
                             contours=dict(size=0.5), line=dict(width=0.5)), 1, 1)
    fig.add_trace(go.Scatter(x=[1, 1.5], y=[1, 0.5], mode="lines", line=dict(color="black", dash="dot", width=2)), 1, 1)
    fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(size=16, color=ORANGE, line=dict(color="white", width=2))), 1, 1)
    for fn, c, name, w, dash in ((f, BLUE, "f (true)", 7, None), (T1, ORANGE, "T₁ (plane)", 3, "dash"),
                                 (T2, GREEN, "T₂", 3, "dash"), (T3, PURPLE, "T₃ = f", 3, "dot")):
        fig.add_trace(go.Scatter(x=ts, y=[fn(*p) for p in path], mode="lines", name=name,
                                 line=dict(color=c, width=w, dash=dash)), 1, 2)
        fig.add_trace(go.Scatter(x=[t], y=[fn(x, y)], mode="markers", marker=dict(size=11, color=c), showlegend=False), 1, 2)
    fig.add_annotation(x=0.02, y=4.5, xref="x2", yref="y2", xanchor="left", showarrow=False, align="left", font=dict(size=19),
                       text=f"T₁ = {T1(x, y):.3f}<br>T₂ = {T2(x, y):.3f}<br>T₃ = f = {f(x, y):.3f}")
    fig.update_xaxes(title="x", range=[0.3, 1.7], row=1, col=1)
    fig.update_yaxes(title="y", range=[0.3, 1.7], scaleanchor="x", row=1, col=1)
    fig.update_xaxes(title="distance t along the path: (1 + t, 1 − t)", row=1, col=2)
    fig.update_yaxes(range=[2.8, 4.9], row=1, col=2)
    fig.update_layout(template="simple_white", width=1250, height=560, font=FONT,
                      legend=dict(orientation="h", x=0.72, xanchor="center", y=-0.2), margin=dict(l=70, r=30, t=60, b=120))
    for tr in fig.data[:3]:
        tr.showlegend = False
    return fig


if __name__ == "__main__":
    make_gif([frame(k) for k in SHOW], here / "taylor_path", fps=2, holds=[3] + [1] * (len(SHOW) - 2) + [6],
             keys=[2, len(SHOW) - 1], cols=1, width=950)
