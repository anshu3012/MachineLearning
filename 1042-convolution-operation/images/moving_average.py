"""A window of five weights of 1/5 slides along one row of the Note's photo (row 100, the first 40 pixels) and
writes the average of the five pixels under it: a moving average, the 1-D version of the sliding window.
Plotly frames because a curve is drawn step by step. Our own design; the moving-average idea is the one in
3Blue1Brown, "But what is a convolution?" (07:30-08:30).
Run: python moving_average.py -> moving_average.gif, moving_average_frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from PIL import Image
from anim import save_gif
from common import BLUE, ORANGE, GREEN, GREY, FONT

HERE = Path(__file__).parent
row = np.array(Image.open(HERE.parent / "data" / "photo.png"), dtype=float)[100, :40]
F = 5
avg = np.array([row[k:k + F].mean() for k in range(len(row) - F + 1)])
assert np.allclose(avg, np.convolve(row, np.ones(F) / F, mode="valid"))      # the same thing as a convolution
assert row[:5].tolist() == [215, 211, 204, 190, 170] and avg[0] == 198        # the Note's worked example
assert np.convolve([1, 2, 3], [4, 5, 6]).tolist() == [4, 13, 28, 27, 18]          # true convolution flips (the Note's Extra)
print("first windows:", row[:7].astype(int).tolist(), "->", avg[:3].round(1).tolist())
print("largest jump between neighbours: pixels", np.abs(np.diff(row)).max(), "averages", np.abs(np.diff(avg)).max())
x = np.arange(len(row))


def frame(k):
    fig = go.Figure()
    fig.add_vrect(x0=k - 0.5, x1=k + F - 0.5, fillcolor=ORANGE, opacity=0.25, line_width=0)
    fig.add_trace(go.Scatter(x=x, y=row, mode="lines+markers", name="pixel values of the row",
                             line=dict(color=GREY, width=2), marker=dict(size=8, color=BLUE)))
    fig.add_trace(go.Scatter(x=x[2:2 + k + 1], y=avg[:k + 1], mode="lines+markers", name="moving average (window of 5)",
                             line=dict(color=GREEN, width=5), marker=dict(size=9)))
    fig.add_trace(go.Scatter(x=[k + 2], y=[avg[k]], mode="markers", showlegend=False,
                             marker=dict(size=18, color=ORANGE, line=dict(color="black", width=1.5))))
    terms = " + ".join(f"{int(v)}" for v in row[k:k + F])
    fig.update_layout(template="simple_white", width=1100, height=560, font=dict(FONT, size=22),
                      title=dict(text=f"window on pixels {k} to {k + F - 1}:  ({terms}) / 5 = {avg[k]:.0f}", x=0.5, y=0.96),
                      xaxis=dict(title="pixel position in the row", range=[-1, len(row)]),
                      yaxis=dict(title="pixel value (0 black, 255 white)", range=[0, 275]),
                      legend=dict(orientation="h", x=0, y=1.0, yanchor="bottom"), margin=dict(l=90, r=20, t=110, b=70))
    return fig


if __name__ == "__main__":
    n = len(avg)
    save_gif([frame(k) for k in range(n)], "moving_average", HERE, fps=4, hold=10, keys=(0, 8, 20, -1), height=560)
