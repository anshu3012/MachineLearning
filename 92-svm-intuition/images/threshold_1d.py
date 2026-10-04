"""The margin in one dimension (Plotly frames -> GIF), on the iris petal lengths of setosa and versicolor (50 flowers
each). A threshold slides across the empty gap between the longest setosa petal (1.9 cm) and the shortest versicolor
petal (3.0 cm). Top: the flowers on a number line, the threshold and its distance to the nearest flower of each
species. Bottom: the smaller of the two distances against the threshold position; it peaks at the midpoint, 2.45 cm."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_iris
from gifkit import BLUE, FONT, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
iris = load_iris()
pl = iris.data[:, 2]
se, ve = pl[iris.target == 0], pl[iris.target == 1]
lo, hi = se.max(), ve.min()
mid = (lo + hi) / 2
assert (lo, hi, round(mid, 2), round((hi - lo) / 2, 2)) == (1.9, 3.0, 2.45, 0.55)
rng = np.random.default_rng(0)
js, jv = rng.uniform(-0.25, 0.25, len(se)), rng.uniform(-0.25, 0.25, len(ve))     # vertical jitter, display only
grid = np.linspace(lo, hi, 111)
small = np.minimum(grid - lo, hi - grid)


def frame(t):
    dl, dr = t - lo, hi - t
    fig = make_subplots(2, 1, row_heights=[0.5, 0.5], vertical_spacing=0.2, shared_xaxes=True,
                        subplot_titles=[f"threshold at {t:.2f} cm: gaps {dl:.2f} and {dr:.2f}", "the smaller gap"])
    fig.update_annotations(font_size=22)
    fig.add_trace(go.Scatter(x=se, y=js, mode="markers", marker=dict(size=11, color=BLUE, opacity=0.7), name="setosa"), 1, 1)
    fig.add_trace(go.Scatter(x=ve, y=jv, mode="markers", marker=dict(size=11, color=ORANGE, opacity=0.7), name="versicolor"), 1, 1)
    fig.add_trace(go.Scatter(x=[t, t], y=[-0.6, 0.6], mode="lines", line=dict(color="black", width=4), showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=[lo, t], y=[0.45, 0.45], mode="lines+markers", line=dict(color=BLUE, width=5), showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=[t, hi], y=[-0.45, -0.45], mode="lines+markers", line=dict(color=ORANGE, width=5), showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=grid, y=small, mode="lines", line=dict(color=GREY, width=3), showlegend=False), 2, 1)
    fig.add_trace(go.Scatter(x=[t], y=[min(dl, dr)], mode="markers+text", text=[f"{min(dl, dr):.2f}"], textposition="top center", textfont=dict(size=22),
                             marker=dict(size=17, color=RED, line=dict(color="black", width=2)), showlegend=False), 2, 1)
    fig.update_yaxes(visible=False, range=[-0.7, 0.7], row=1, col=1)
    fig.update_yaxes(range=[0, 0.72], title="cm", row=2, col=1)
    fig.update_xaxes(range=[0.8, 5.3], row=1, col=1)
    fig.update_xaxes(title="petal length (cm)", row=2, col=1)
    fig.update_layout(template="simple_white", width=1100, height=680, font=FONT, margin=dict(l=70, r=30, t=60, b=70),
                      legend=dict(orientation="h", x=0.99, xanchor="right", y=1.0, yanchor="bottom"))
    return fig


if __name__ == "__main__":
    ts = [2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 2.45]
    make_gif([frame(t) for t in ts], here / "threshold_1d", fps=2, holds=[4] + [1] * 9 + [8], keys=[0, 10], cols=1)
