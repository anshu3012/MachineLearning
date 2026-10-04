"""Where the chi-square distribution comes from. Left: draws z from the standard normal. Right: the histogram of z^2
(k = 1), then of the sum of 2, 3 and 5 squared draws, each against the chi-square density with k degrees of freedom.
Seeded simulation, 20,000 sums per frame.
Tool: Plotly frames -> GIF (histograms changing). Idea after Khan Academy, "Chi-square distribution introduction"."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from gifkit import make_gif, FONT, BLUE, ORANGE, RED, GREY

here = Path(__file__).parent
rng = np.random.default_rng(0)
Z = rng.standard_normal((20000, 5))
for k_ in (1, 2, 3, 5):                                   # the simulated sums behave like chi-square with k df
    assert abs((Z[:, :k_] ** 2).sum(axis=1).mean() - k_) < 0.05
assert abs((np.abs(Z[:, 0]) < 1).mean() - 0.683) < 0.01    # 68 percent of draws are within 1 of zero
BINS = dict(start=0, end=14, size=0.25)


def frame(k, n, head, curve=True):
    q = (Z[:n, :k] ** 2).sum(axis=1)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.4, 0.6], horizontal_spacing=0.12,
                        subplot_titles=("draws z from the standard normal",
                                        "z²" if k == 1 else "sum of " + str(k) + " squared draws"))
    fig.update_annotations(font_size=22)
    fig.add_histogram(x=Z[:n, 0], histnorm="probability density", xbins=dict(start=-4, end=4, size=0.25),
                      marker_color=GREY, opacity=0.6, row=1, col=1)
    fig.add_histogram(x=q, histnorm="probability density", xbins=BINS, marker_color=BLUE, opacity=0.75, row=1, col=2)
    if curve:
        x = np.linspace(0.02 if k > 1 else 0.13, 14, 500)
        fig.add_scatter(x=x, y=stats.chi2.pdf(x, k), mode="lines", line=dict(color=RED, width=4), row=1, col=2)
        fig.add_annotation(x=8.5, y=0.5, xref="x2", yref="y2", showarrow=False, font=dict(size=24, color=RED),
                           text=f"chi-square curve, df = {k}")
    fig.update_xaxes(title="z", range=[-4, 4], row=1, col=1)
    fig.update_yaxes(range=[0, 0.5], row=1, col=1)
    fig.update_xaxes(title="value", range=[0, 14], row=1, col=2)
    fig.update_yaxes(range=[0, 0.75], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=560, font=FONT, showlegend=False,
                      title=dict(text=head, x=0.5), margin=dict(l=60, r=30, t=110, b=70))
    return fig


if __name__ == "__main__":
    figs = [frame(1, 200, "200 draws, each one squared", curve=False),
            frame(1, 20000, "20,000 squared draws: most are near 0"),
            frame(2, 20000, "add 2 squared draws"),
            frame(3, 20000, "add 3 squared draws: the peak leaves 0"),
            frame(5, 20000, "add 5 squared draws: the curve moves right")]
    make_gif(figs, here / "squared_normals", fps=1, holds=[3, 3, 3, 3, 6], keys=[1, 2, 3, 4], cols=2)
