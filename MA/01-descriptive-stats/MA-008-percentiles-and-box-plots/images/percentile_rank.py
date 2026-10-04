"""Percentile rank of a mark, step by step: count the marks below it, add half of the marks equal to it, divide by
10. Each mark sits in the middle of its own tenth of the data. Data: the Note's ten marks. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from anim import save_gif, FONT, BLUE, ORANGE, GREY

here = Path(__file__).parent
marks = [78, 82, 84, 88, 91, 93, 94, 96, 98, 99]
assert stats.percentileofscore(marks, 88, kind="mean") == 35 and stats.percentileofscore(marks, 99, kind="mean") == 95


def frame(v):
    X = sum(m < v for m in marks)
    Y = sum(m == v for m in marks)
    rank = (X + 0.5 * Y) / len(marks) * 100
    assert np.isclose(rank, stats.percentileofscore(marks, v, kind="mean"))
    fig = go.Figure()
    for i, m in enumerate(marks):                       # each mark owns one tenth of the 0-100 scale
        c = BLUE if m < v else (ORANGE if m == v else "#e6e6e6")
        fig.add_shape(type="rect", x0=10 * i, x1=10 * i + 10, y0=0, y1=1, fillcolor=c, opacity=1, layer="below", line=dict(color="white", width=3))
        fig.add_annotation(x=10 * i + 5, y=0.5, text=f"<b>{m}</b>", showarrow=False, font=dict(size=24,
                           color="white" if m <= v else "#555"))
    fig.add_shape(type="line", x0=rank, x1=rank, y0=-0.25, y1=1.25, opacity=1, line=dict(color="black", width=4))
    fig.add_annotation(x=rank, y=1.45, text=f"<b>{rank:g}th percentile</b>", showarrow=False, font=dict(size=24))
    fig.update_layout(template="simple_white", width=1100, height=500, font=FONT,
                      title=dict(text=f"<b>Mark {v}</b>: {X} below (blue) + half of {Y} equal (orange)"
                                      f"<br>({X} + 0.5 × {Y}) / 10 × 100 = <b>{rank:g}</b>", x=0.5, y=0.95),
                      xaxis=dict(range=[-2, 102], title="share of the data (percent)", tickvals=list(range(0, 101, 10))),
                      yaxis=dict(visible=False, range=[-0.4, 1.7]), margin=dict(l=30, r=30, t=110, b=80))
    return fig


if __name__ == "__main__":
    vals = [78, 84, 88, 93, 99]
    save_gif([frame(v) for v in vals], "percentile_rank", here, keys=[0, 2, 4], fps=1, holds=[3, 3, 3, 3, 6], cols=1, width=900)
