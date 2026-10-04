"""Why a table stops working: the exact distribution of the sum of 1, 2, 3, 5 and 10 dice. The number of sums and
of equally likely combinations grows fast (10 dice: 51 sums from 6^10 = 60,466,176 combinations), while the graph
shows the shape at a glance. Exact counts by repeated convolution. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE

here = Path(__file__).parent
die = np.ones(6, dtype=np.int64)


def counts(n):
    c = np.array([1], dtype=np.int64)
    for _ in range(n):
        c = np.convolve(c, die)
    return c                                               # c[k] = ways to get sum n + k


c10 = counts(10)
assert len(c10) == 51 and c10.sum() == 6 ** 10 == 60_466_176


def frame(n):
    c = counts(n)
    x = np.arange(n, 6 * n + 1)
    fig = go.Figure(go.Bar(x=x, y=c / c.sum(), marker_color=BLUE, width=0.8 if n < 10 else 0.7))
    fig.update_layout(template="simple_white", width=1100, height=600, font=FONT,
                      title=dict(text=f"<b>{n} {'die' if n == 1 else 'dice'}</b>: {len(x)} possible sums,"
                                      f" {6 ** n:,} equally likely combinations", x=0.5),
                      xaxis=dict(title="sum x", range=[0, 61]), yaxis=dict(title="P(X = x)", range=[0, 0.18]),
                      margin=dict(l=90, r=30, t=80, b=80))
    return fig


if __name__ == "__main__":
    save_gif([frame(n) for n in (1, 2, 3, 5, 10)], "many_dice", here, keys=[0, 1, 3, 4], fps=1, holds=[3, 3, 3, 3, 6])
