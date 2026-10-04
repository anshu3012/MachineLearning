"""Scaling: the vector v = [2, 3] multiplied by s = 1, 2, 0.5, -1 and -2. The direction stays on the same line; the
length is |s| times sqrt(13) = 3.61, and a negative s flips the arrow. The strip below shows the same s acting on the
number 1 on a number line: stretch, shrink, flip. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from anim import save_gif, FONT, BLUE, ORANGE

here = Path(__file__).parent
v = np.array([2, 3.0])
assert np.isclose(np.linalg.norm(2 * v), 2 * np.linalg.norm(v)) and np.isclose(np.linalg.norm(-v), np.linalg.norm(v))
assert np.isclose(np.linalg.norm(-2 * v), 2 * np.linalg.norm(v))


def arrow(fig, x, y, color, width, opacity, ref):
    fig.add_annotation(x=x, y=y, ax=0, ay=0, xref=f"x{ref}", yref=f"y{ref}", axref=f"x{ref}", ayref=f"y{ref}",
                       arrowhead=3, arrowwidth=width, arrowcolor=color, opacity=opacity, text="")


def frame(s):
    w = s * v
    fig = make_subplots(rows=2, cols=1, row_heights=[0.84, 0.16], vertical_spacing=0.11)
    fig.add_scatter(x=[-6, 6], y=[-9, 9], mode="lines", line=dict(color="#dddddd", width=2, dash="dot"), row=1, col=1)
    arrow(fig, v[0], v[1], BLUE, 3, 0.5, "")
    arrow(fig, w[0], w[1], ORANGE, 5, 1, "")
    fig.add_annotation(x=w[0], y=w[1], text=f"{s:g} × [2, 3] = [{w[0]:g}, {w[1]:g}]", showarrow=False,
                       xshift=120 if s > 0 else -120, font=dict(size=20, color="#c55a00"))
    # number line: the same scalar acting on the number 1
    fig.add_scatter(x=[1, s], y=[0, 0], mode="markers", marker=dict(size=[12, 16], color=[BLUE, ORANGE],
                                                                    opacity=[0.5, 1]), row=2, col=1)
    arrow(fig, 1, 0, BLUE, 3, 0.5, "2")
    arrow(fig, s, 0, ORANGE, 5, 1, "2")
    fig.add_annotation(x=-4.2, y=0.9, xref="x2", yref="y2", showarrow=False, xanchor="left",
                       text=f"on a number line: {s:g} × 1 = {s:g}", font=dict(size=20, color="#c55a00"))
    fig.update_layout(template="simple_white", width=900, height=940, font=FONT, showlegend=False,
                      title=dict(text=f"s = {s:g}: length {abs(s):g} × 3.61 = {abs(s) * np.linalg.norm(v):.2f}"
                                      + ("  (direction flipped)" if s < 0 else ""), x=0.5),
                      xaxis=dict(range=[-6, 6], zeroline=True, zerolinewidth=2),
                      yaxis=dict(range=[-7, 7], zeroline=True, zerolinewidth=2, scaleanchor="x"),
                      xaxis2=dict(range=[-4.4, 4.4], dtick=1, zeroline=True, zerolinewidth=2),
                      yaxis2=dict(range=[-0.6, 1.5], visible=False),
                      margin=dict(l=60, r=30, t=80, b=50))
    return fig


if __name__ == "__main__":
    save_gif([frame(s) for s in (1, 2, 0.5, -1, -2)], "scaling", here, keys=[1, 2, 3, 4], fps=1, holds=[3, 3, 3, 3, 6])
