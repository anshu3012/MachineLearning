"""Choosing the versicolor/virginica cut-off on petal width with the two ECDFs: for each cut-off c, the share of
versicolor right is F_versicolor(c) and the share of virginica right is 1 - F_virginica(c). At c = 1.7: 0.98 and 0.90,
144 of 150 right in total (with all 50 setosa below 0.7). Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_iris
from anim import save_gif, FONT, ORANGE, GREEN

here = Path(__file__).parent
iris = load_iris()
pw, t = iris.data[:, 3], iris.target
ve, vi = np.sort(pw[t == 1]), np.sort(pw[t == 2])
F = lambda v, c: np.mean(v <= c + 1e-9)
assert F(ve, 1.7) == 0.98 and round(F(vi, 1.7), 2) == 0.10 and pw[t == 0].max() <= 0.6
assert 50 + round(50 * F(ve, 1.7)) + round(50 * (1 - F(vi, 1.7))) == 144


def frame(c):
    fig = go.Figure()
    e = np.arange(1, 51) / 50
    fig.add_scatter(x=np.r_[0.8, ve, 2.6], y=np.r_[0, e, 1], mode="lines", line=dict(color=ORANGE, width=4, shape="hv"),
                    name="versicolor CDF")
    fig.add_scatter(x=np.r_[0.8, vi, 2.6], y=np.r_[0, e, 1], mode="lines", line=dict(color=GREEN, width=4, shape="hv"),
                    name="virginica CDF")
    a, b = F(ve, c), F(vi, c)
    fig.add_vline(x=c, line=dict(color="black", width=2, dash="dash"))
    fig.add_scatter(x=[c, c], y=[a, b], mode="markers", marker=dict(size=16, color=[ORANGE, GREEN]), showlegend=False)
    total = 50 + round(50 * a) + round(50 * (1 - b))
    fig.update_layout(template="simple_white", width=1000, height=620, font=FONT,
                      title=dict(text=f"cut-off {c:.1f} cm: versicolor right F = <b>{a:.2f}</b>, virginica right 1 − F = <b>{1 - b:.2f}</b>"
                                      f"<br>{total} of 150 flowers right", x=0.5, y=0.94),
                      xaxis=dict(title="petal width (cm)", range=[0.8, 2.6]), yaxis=dict(title="share at or below", range=[0, 1.05]),
                      legend=dict(x=0.72, y=0.15), margin=dict(l=90, r=30, t=110, b=80))
    return fig


if __name__ == "__main__":
    cs = [1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
    save_gif([frame(c) for c in cs], "cutoff_sweep", here, keys=[0, 2, 4, 6], fps=1, holds=[2, 2, 2, 2, 4, 2, 4])
