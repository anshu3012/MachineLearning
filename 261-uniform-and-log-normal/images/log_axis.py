"""Why the log makes a right-skewed feature symmetric. Seven comment lengths around the Note's median of 20 words:
20 divided and multiplied by 2, 4 and 8. On an ordinary axis 8 times longer (160) is far from 20 and 8 times
shorter (2.5) is close; as the axis turns into a log axis the two distances become equal.
Plotly frames (positions of points changing) -> log_axis.gif, _frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, ORANGE, GREY

here = Path(__file__).parent
FOLD = np.array([1 / 8, 1 / 4, 1 / 2, 1, 2, 4, 8])
X = 20 * FOLD
NAMES = ["8 times shorter", "4 times shorter", "half", "median", "double", "4 times longer", "8 times longer"]
LAMS = [1, 0.6, 0.35, 0.2, 0.1, 0]


def t(x, lam):
    y = np.log(x) if lam == 0 else (x ** lam - 1) / lam
    lo, hi = (np.log(2.5), np.log(160)) if lam == 0 else ((2.5 ** lam - 1) / lam, (160 ** lam - 1) / lam)
    return (y - lo) / (hi - lo)                       # 2.5 words -> 0, 160 words -> 1


assert np.allclose(np.diff(t(X, 0)), 1 / 6)           # log axis: equal steps


def frame(lam):
    p, mid = t(X, lam), t(20, lam)
    fig = go.Figure()
    for i in range(7):
        c = GREY if i == 3 else (ORANGE if i > 3 else BLUE)
        fig.add_scatter(x=[mid, p[i]], y=[i, i], mode="lines", line=dict(color=c, width=10))
        fig.add_scatter(x=[p[i]], y=[i], mode="markers", marker=dict(color=c, size=20))
        fig.add_annotation(x=1.04, y=i, text=f"{NAMES[i]}: {X[i]:g}", showarrow=False, xanchor="left", font_size=22)
    fig.add_vline(x=mid, line=dict(color=GREY, dash="dot", width=2))
    left, right = mid - p[0], p[-1] - mid
    ticks, last = [], -1
    for v in X:                                       # label a tick only when there is room for it
        if t(v, lam) - last > 0.07:
            ticks.append(v)
            last = t(v, lam)
    name = "ordinary axis" if lam == 1 else ("log axis" if lam == 0 else "turning into a log axis")
    fig.update_layout(template="simple_white", width=1100, height=640, font=FONT, showlegend=False,
                      title=dict(text=f"<b>{name}</b><br><sup>distance from the median: 8 times shorter "
                                      f"{left:.2f}, 8 times longer {right:.2f} of the axis</sup>", x=0.5),
                      xaxis=dict(title="comment length (words)", range=[-0.03, 1.42], tickvals=[t(v, lam) for v in ticks],
                                 ticktext=[f"{v:g}" for v in ticks]),
                      yaxis=dict(visible=False, range=[-0.7, 6.7]), margin=dict(l=30, r=30, t=110, b=80))
    return fig


if __name__ == "__main__":
    save_gif([frame(l) for l in LAMS], "log_axis", here, keys=[0, 5], fps=1, holds=[4, 1, 1, 1, 1, 6], cols=1)
    print(t(X, 1), t(20, 1))
