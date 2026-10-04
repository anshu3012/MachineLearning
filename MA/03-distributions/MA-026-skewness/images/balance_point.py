"""The mean as the balance point of a density, the median as its equal-area line. A right-skewed shape (gamma, k = 2:
mode 1, median 1.68, mean 2, skewness 1.41) sits on a beam. With the support under the mode, or under the median
(50 percent of the area on each side), the long right tail tips the beam; it balances only under the mean.
Plotly frames -> GIF. Idea after Khan Academy, "Median, mean and skew from density curves"."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from anim import save_gif, FONT, BLUE, ORANGE, RED, GREY

here = Path(__file__).parent
dist = stats.gamma(2)
MODE, MEDIAN, MEAN = 1.0, dist.median(), dist.mean()
assert abs(MEDIAN - 1.678) < 1e-3 and MEAN == 2 and MODE < MEDIAN < MEAN
S, XMAX, MAXTILT = 8, 9, np.radians(6)          # height scale, right end of the beam, tilt with the support at the mode
x = np.linspace(0, XMAX, 400)


def rot(px, py, f, a):
    """rotate points about the support (f, 0) by angle a."""
    return f + (px - f) * np.cos(a) - py * np.sin(a), (px - f) * np.sin(a) + py * np.cos(a)


def frame(f, title):
    a = -MAXTILT * (MEAN - f) / (MEAN - MODE)   # net turning effect is proportional to (mean - support)
    fig = go.Figure()
    for lo, hi, col in ((0, f, BLUE), (f, XMAX, ORANGE)):
        m = (x >= lo) & (x <= hi)
        px, py = rot(np.r_[lo, x[m], hi], np.r_[0, S * dist.pdf(x[m]), 0], f, a)
        fig.add_scatter(x=px, y=py, fill="toself", fillcolor=col, opacity=0.6, line=dict(width=0), mode="lines")
    bx, by = rot(np.array([-0.3, XMAX + 0.3]), np.zeros(2), f, a)
    fig.add_scatter(x=bx, y=by, mode="lines", line=dict(color="black", width=6))
    fig.add_scatter(x=[f - 0.35, f, f + 0.35, f - 0.35], y=[-1.0, -0.05, -1.0, -1.0], fill="toself", fillcolor=RED,
                    line=dict(color=RED), mode="lines")
    fig.add_shape(type="line", x0=-0.6, x1=XMAX + 0.6, y0=-1.0, y1=-1.0, line=dict(color=GREY, width=2))
    left = 100 * dist.cdf(f)
    fig.add_annotation(x=0.2, y=3.9, text=f"<b>{left:.0f} percent</b><br>of the area", showarrow=False, xanchor="left",
                       font=dict(size=24, color=BLUE))
    fig.add_annotation(x=5.5, y=3.9, text=f"<b>{100 - left:.0f} percent</b><br>of the area", showarrow=False,
                       font=dict(size=24, color="#C96A00"))
    fig.add_annotation(x=f, y=-1.45, text=f"support at {f:.2f}", showarrow=False, font=dict(size=22, color=RED))
    fig.update_layout(template="simple_white", width=1000, height=640, font=FONT, showlegend=False,
                      title=dict(text=title, x=0.5), margin=dict(l=20, r=20, t=90, b=20),
                      xaxis=dict(visible=False, range=[-0.8, XMAX + 0.8]),
                      yaxis=dict(visible=False, range=[-1.9, 4.6], scaleanchor="x"))
    return fig


if __name__ == "__main__":
    tip = "the long right tail tips the beam"
    steps = [(MODE, f"<b>Support under the mode</b>: {tip}"), (1.2, "Move the support towards the tail"),
             (1.45, "Move the support towards the tail"),
             (MEDIAN, "<b>Support under the median</b>: equal areas, but it still tips"),
             (1.8, "Move the support a little further"), (1.9, "Move the support a little further"),
             (MEAN, "<b>Support under the mean</b>: the shape balances")]
    save_gif([frame(f, t) for f, t in steps], "balance_point", here, keys=[0, 3, 6], fps=2,
             holds=[6, 1, 1, 7, 1, 1, 10], cols=2)
