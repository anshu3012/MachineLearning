"""Building the empirical CDF of the 50 versicolor petal widths: a cut-off x sweeps right; the flowers at or below x
turn orange and the ECDF value is their share. At x = 1.7 it reaches 49/50 = 0.98. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_iris
from anim import save_gif, FONT, ORANGE

here = Path(__file__).parent
iris = load_iris()
v = np.sort(iris.data[iris.target == 1, 3])
assert len(v) == 50 and np.mean(v <= 1.7) == 0.98
# jitter-free dot strip: stack equal values
vals, counts = np.unique(v, return_counts=True)
xs = np.repeat(vals, counts)
ys = np.concatenate([np.arange(c) for c in counts]) + 1


def frame(x0):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08, row_heights=[0.45, 0.55],
                        subplot_titles=["50 versicolor flowers (one dot each)", "Empirical CDF: share at or below x"])
    on = xs <= x0 + 1e-9
    fig.add_scatter(x=xs, y=ys, mode="markers", marker=dict(size=13, color=np.where(on, ORANGE, "#cccccc")), row=1, col=1)
    e = np.arange(1, 51) / 50
    m = v <= x0 + 1e-9
    fig.add_scatter(x=np.r_[0.8, v[m], x0], y=np.r_[0, e[m], e[m][-1] if m.any() else 0], mode="lines",
                    line=dict(color=ORANGE, width=4, shape="hv"), row=2, col=1)
    share = m.mean()
    for r in (1, 2):
        fig.add_vline(x=x0, line=dict(color="black", width=2, dash="dash"), row=r, col=1)
    fig.update_yaxes(visible=False, range=[0, ys.max() + 1.5], row=1, col=1)
    fig.update_yaxes(title_text="F(x)", range=[0, 1.05], row=2, col=1)
    fig.update_xaxes(range=[0.8, 2.0], row=1, col=1)
    fig.update_xaxes(title_text="petal width x (cm)", range=[0.8, 2.0], row=2, col=1)
    fig.update_annotations(font_size=21)
    fig.update_layout(template="simple_white", width=1000, height=760, font=FONT, showlegend=False,
                      title=dict(text=f"x = {x0:.1f} cm: {int(m.sum())} of 50 at or below → <b>F(x) = {share:.2f}</b>", x=0.5),
                      margin=dict(l=90, r=30, t=110, b=80))
    return fig


if __name__ == "__main__":
    xs_ = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
    save_gif([frame(x) for x in xs_], "ecdf_build", here, keys=[0, 3, 5, 7], fps=1, holds=[2] * 7 + [6])
