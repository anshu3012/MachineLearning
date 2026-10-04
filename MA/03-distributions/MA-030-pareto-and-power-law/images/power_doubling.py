"""The power law y = x^-2 of section 2: each doubling of x divides y by 4, wherever we start; on log-log axes the
same points lie on a straight line with slope -2. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from anim import save_gif, FONT, BLUE, ORANGE

here = Path(__file__).parent
xs = np.array([1, 2, 4, 8])
ys = xs ** -2.0
assert np.allclose(ys[:-1] / ys[1:], 4) and np.isclose(10.0 ** -2, 0.01)
grid = np.linspace(0.8, 9, 300)


def frame(k):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                        subplot_titles=["ordinary axes: a curve with a long tail", "log-log axes: a straight line, slope −2"])
    for c in (1, 2):
        fig.add_scatter(x=grid, y=grid ** -2.0, mode="lines", line=dict(color="#cccccc", width=3), row=1, col=c)
        fig.add_scatter(x=xs[:k], y=ys[:k], mode="markers+text", marker=dict(size=16, color=ORANGE),
                        text=[f"({x}, {y:.4g})" for x, y in zip(xs[:k], ys[:k])], textposition="top right",
                        textfont=dict(size=18), row=1, col=c)
    fig.update_xaxes(title_text="x", range=[0, 11], row=1, col=1)
    fig.update_yaxes(title_text="y", range=[0, 1.15], row=1, col=1)
    fig.update_xaxes(title_text="x (log)", type="log", range=[-0.15, 1.2], tickvals=[1, 2, 4, 8], row=1, col=2)
    fig.update_yaxes(title_text="y (log)", type="log", range=[-2.2, 0.3], tickvals=[1, 0.25, 0.0625, 0.015625], ticktext=["1", "0.25", "0.0625", "0.0156"], row=1, col=2)
    head = "y = x<sup>−2</sup>" if k == 1 else f"x doubled to {xs[k - 1]}: y = {ys[k - 2]:g} / 4 = <b>{ys[k - 1]:g}</b>"
    fig.update_annotations(font_size=20)
    fig.update_layout(template="simple_white", width=1300, height=560, font=FONT, showlegend=False,
                      title=dict(text=head, x=0.5), margin=dict(l=80, r=30, t=110, b=70))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(1, 5)], "power_doubling", here, keys=[1, 3], fps=1, holds=[3, 3, 3, 6], cols=1)
