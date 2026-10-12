"""Smoothing the Hybrid A* path (Nav2's weights: data 0.2, smoothing 0.3, plus Dolgov's push away from obstacles),
sweep by sweep, on the forward drive up to the switch to reverse. Left: the drive round the end of the middle row,
the path as found (grey) and after the sweep (green); black dots: points held where Hybrid A* put them, because
smoothing them would turn tighter than the 5 m circle. Right: the steering angle along the drive, as found (grey)
and after the sweep (green): the left-straight-right swerve flattens. Run -> smooth_anim.gif, smooth_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from carkit import dense_clearance, hybrid_astar, pieces, smooth_path, steering
from gifkit import GREEN, GREY, make_gif
from lotdraw import FONT, axes, lot, path
from plotly.subplots import make_subplots

here = Path(__file__).parent
R = hybrid_astar("max", shot=True)
X, D = pieces(R)[0]
KEEP = [1, 2, 3, 5, 8, 12, 20, 30]
SM, SN, RERUNS = smooth_path(R, keep=KEEP)
Y = SM[0][0]
REC = SN[0]
ITS = REC["iters"]
FIX = REC["fixed"]
S0, S1 = steering(X, D), steering(Y, D)
DIST = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(X, axis=0).T))])[1:-1]
TOT0, TOT1 = np.abs(np.diff(S0)).sum(), np.abs(np.diff(S1)).sum()
C0, C1 = dense_clearance(X, D), dense_clearance(Y, D)
assert ITS == 49 and round(TOT0) == 133 and round(TOT1) == 100 and round(C0, 2) == 0.16 and round(C1, 2) == 0.19
assert np.abs(S1).max() <= 26.57 + 0.01


def frame(k):
    y = REC["final"] if k == ITS else REC.get(k, REC[0])
    fig = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5], horizontal_spacing=0.1,
                        subplot_titles=["round the end of the middle row", "steering angle along the drive (deg)"])
    lot(fig, (1, 1), xr=(8, 20), yr=(2, 18))
    path(fig, X, (1, 1), colour=GREY, width=3)
    path(fig, y, (1, 1), colour=GREEN, width=4)
    path(fig, X[FIX], (1, 1), colour="black", mode="markers", size=6)
    axes(fig, (1, 1), xr=(8, 20), yr=(2, 18))
    s = steering(y, D)
    fig.add_trace(go.Scatter(x=DIST, y=S0, mode="lines", line=dict(color=GREY, width=3),
                             hoverinfo="skip"), row=1, col=2)
    fig.add_trace(go.Scatter(x=DIST, y=s, mode="lines+markers", line=dict(color=GREEN, width=3),
                             marker=dict(size=5), hoverinfo="skip"), row=1, col=2)
    fig.update_xaxes(title_text="distance along the drive (m)", range=[0, 32], row=1, col=2,
                     tickfont=dict(size=15))
    fig.update_yaxes(range=[-30, 30], tickvals=[-26.6, 0, 26.6], ticktext=["-26.6", "0", "26.6"], row=1, col=2,
                     tickfont=dict(size=15))
    tot = np.abs(np.diff(s)).sum()
    title = "the forward drive as found" if k == 0 else f"smoothing, sweep {k}"
    if k == ITS:
        title = f"settled after {ITS} sweeps"
    fig.update_layout(template="simple_white", width=1100, height=640, showlegend=False, font=FONT,
                      title=dict(text=title, x=0.5, xanchor="center", font_size=23), margin=dict(l=40, r=30, t=120, b=60))
    fig.add_annotation(x=0.5, y=1.12, xref="paper", yref="paper", showarrow=False, font=dict(size=18),
                       text=f"total steering movement {tot:.0f} deg (was {TOT0:.0f}); black: points held")
    for a in fig.layout.annotations[:2]:
        a.font = dict(size=17, family=FONT["family"])
    return fig


ks = [0] + KEEP + [ITS]
figs = [frame(k) for k in ks]
make_gif(figs, here / "smooth_anim", fps=3, holds=[6] + [3] * len(KEEP) + [20], keys=[0, 3, len(figs) - 1],
         cols=1, width=900)
