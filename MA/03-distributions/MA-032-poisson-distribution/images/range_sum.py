"""Probability of a range, added up bar by bar (Plotly frames -> GIF). Po(4): the bars for 0 to 6 questions are
stacked one at a time into a running total, P(Y <= 6) = 0.8893; the rest of the column, 1 - 0.8893 = 0.111, is
P(Y >= 7)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from gifkit import BLUE, FONT, GREEN, GREY, RED, make_gif

here = Path(__file__).parent
y = np.arange(0, 15)
pmf = stats.poisson.pmf(y, 4)
assert [round(p, 4) for p in pmf[:7]] == [0.0183, 0.0733, 0.1465, 0.1954, 0.1954, 0.1563, 0.1042]
assert round(pmf[:7].sum(), 4) == 0.8893 and round(1 - pmf[:7].sum(), 3) == 0.111
COLS = ["#4C78A8", "#72B7B2", "#54A24B", "#EECA3B", "#B279A2", "#FF9DA6", "#9D755D"]


def frame(k, done=False):
    fig = make_subplots(1, 2, column_widths=[0.72, 0.28], horizontal_spacing=0.08,
                        subplot_titles=["Po(4): one bar per count", "running total"])
    fig.update_annotations(font_size=22)
    cols = [COLS[i] if i < k else (RED if done and i >= 7 else GREY) for i in y]
    fig.add_trace(go.Bar(x=y, y=pmf, marker_color=cols), 1, 1)
    base = 0
    for i in range(k):
        fig.add_trace(go.Bar(x=["P(Y ≤ 6)"], y=[pmf[i]], base=[base], marker_color=COLS[i], width=0.6,
                             text=[f"P({i}) = {pmf[i]:.4f}"], textposition="inside", textfont=dict(size=15)), 1, 2)
        base += pmf[i]
    if done:
        fig.add_trace(go.Bar(x=["P(Y ≤ 6)"], y=[1 - base], base=[base], marker_color=RED, width=0.6,
                             text=[f"P(Y ≥ 7) = {1 - base:.3f}"], textposition="outside", textfont=dict(size=18)), 1, 2)
    fig.add_hline(y=1, line=dict(color="black", dash="dash"), row=1, col=2)
    title = (f"adding bars 0 to {k - 1}: total {base:.4f}" if not done else
             f"P(Y ≤ 6) = {base:.4f}, so P(Y ≥ 7) = 1 − {base:.4f} = {1 - base:.3f}")
    fig.update_xaxes(title="questions in one day, y", row=1, col=1)
    fig.update_yaxes(title="P(Y = y)", range=[0, 0.22], row=1, col=1)
    fig.update_yaxes(range=[0, 1.08], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=580, font=FONT, showlegend=False, barmode="overlay",
                      title=dict(text=title, x=0.5), margin=dict(l=70, r=30, t=100, b=70))
    return fig


if __name__ == "__main__":
    figs = [frame(k) for k in range(1, 8)] + [frame(7, done=True)]
    make_gif(figs, here / "range_sum", fps=1, holds=[1] * 7 + [5], keys=[len(figs) - 1], cols=1)
