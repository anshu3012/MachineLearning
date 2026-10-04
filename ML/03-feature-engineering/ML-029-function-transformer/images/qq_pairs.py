"""A Q-Q plot built one pair at a time from the Note's five values 1, 2, 3, 4, 10. Top: the normal curve cut into five
slices of equal probability, with the z-value at the middle of each slice. Bottom: the k-th smallest value against the
k-th z-value; dotted lines meet at each dot. Construction after StatQuest, "Quantile-Quantile Plots (QQ plots)"
(00:30-03:30), on our own values. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from anim import save_gif, FONT, BLUE, RED, GREY, ORANGE

here = Path(__file__).parent
vals = np.array([1, 2, 3, 4, 10])
n = len(vals)
z = stats.norm.ppf((np.arange(1, n + 1) - 0.5) / n)
assert np.allclose(z, [-1.28, -0.52, 0, 0.52, 1.28], atol=0.005)
edges = np.concatenate([[-2.6], stats.norm.ppf(np.arange(1, n) / n), [2.6]])
slope, intercept = np.polyfit(z, vals, 1)
grid = np.linspace(-2.6, 2.6, 300)


def frame(k, head, line=False):
    """k pairs are plotted; pair k is the one being added (dotted lines)."""
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.36, 0.64], vertical_spacing=0.06)
    fig.add_scatter(x=grid, y=stats.norm.pdf(grid), mode="lines", line=dict(color=GREY, width=3), row=1, col=1)
    for e in edges[1:-1]:
        fig.add_scatter(x=[e, e], y=[0, stats.norm.pdf(e)], mode="lines", line=dict(color=GREY, width=2), row=1, col=1)
    if k and not line:
        g = np.linspace(edges[k - 1], edges[k], 60)
        fig.add_scatter(x=np.r_[g, g[::-1]], y=np.r_[stats.norm.pdf(g), np.zeros(60)], fill="toself", mode="none",
                        fillcolor="rgba(245,133,24,0.45)", row=1, col=1)
    fig.add_scatter(x=z[:max(k, 0)] if k else [], y=[0] * k, mode="markers", marker=dict(color=ORANGE, size=13, symbol="diamond"),
                    row=1, col=1)
    if line:
        fig.add_scatter(x=z[[0, -1]], y=slope * z[[0, -1]] + intercept, mode="lines", line=dict(color=RED, width=3), row=2, col=1)
    if k and not line:
        fig.add_scatter(x=[z[k - 1], z[k - 1]], y=[-1, vals[k - 1]], mode="lines", line=dict(color=ORANGE, width=3, dash="dot"),
                        row=2, col=1)
        fig.add_scatter(x=[-2.6, z[k - 1]], y=[vals[k - 1]] * 2, mode="lines", line=dict(color=BLUE, width=3, dash="dot"),
                        row=2, col=1)
    fig.add_scatter(x=z[:k], y=vals[:k], mode="markers+text", marker=dict(color=BLUE, size=17),
                    text=[f"({a:.2f}, {b})" for a, b in zip(z[:k], vals[:k])], textposition="middle right",
                    textfont=dict(size=20), row=2, col=1)
    fig.update_xaxes(range=[-2.6, 2.6])
    fig.update_xaxes(title="normal quantile z (middle of each slice)", row=2, col=1)
    fig.update_yaxes(visible=False, row=1, col=1)
    fig.update_yaxes(title="sorted value", range=[-1, 11.5], tickvals=vals, row=2, col=1)
    fig.update_layout(template="simple_white", width=1000, height=820, font=FONT, showlegend=False,
                      title=dict(text=head, x=0.5), margin=dict(l=80, r=30, t=90, b=70))
    return fig


if __name__ == "__main__":
    figs = [frame(0, "<b>The normal curve in 5 slices of equal probability</b>")]
    figs += [frame(k, f"<b>Pair {k}:</b> value {vals[k - 1]} with the z of slice {k}, {z[k - 1]:.2f}") for k in range(1, n + 1)]
    figs += [frame(n, "<b>Four dots lie near a line; the value 10 jumps above it</b>", line=True)]
    save_gif(figs, "qq_pairs", here, keys=[1, 3, 5, 6], fps=1, holds=[3, 2, 2, 2, 2, 3, 6], cols=2)
