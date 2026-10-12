"""Animation: the obstacle region of the room for the robot carrying the 1.4 m x 0.3 m board, one heading per frame
from 0 to 180 degrees in steps of 10. Orange: centres that put the board on an obstacle at that heading (one slice of
C-space); white: free centres. The small panel shows the board's heading. The doorway's free stretch for the centre is
0 at 0 degrees (the 1.4 m board lies across the 1.2 m doorway) and 0.90 m at 90 degrees (only its 0.3 m width
crosses). At 180 degrees the slice is the same as at 0. Run -> slices.gif, slices_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import cspace as c
import drawkit as k
from gifkit import GREEN, ORANGE, RED, make_gif

here = Path(__file__).parent
ROOM = c.box(0, 0, c.W, c.H + 0.12)
gaps = {d: c.door_gap(c.cobs_board(np.radians(d))) for d in range(0, 181, 10)}
assert gaps[0] == 0 and abs(gaps[90] - 0.9) < 1e-3 and gaps[180] == 0


def frame(d):
    th = np.radians(d)
    C = c.cobs_board(th)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.8, 0.2], horizontal_spacing=0.04,
                        subplot_titles=["slice of C-space at this heading", "the board"])
    fig.add_trace(k.geom_trace(C.intersection(ROOM).difference(c.obstacles()), k.COBS_FILL, ORANGE, 1), row=1, col=1)
    k.room(fig, 1, 1, walls=False)
    g = gaps[d]
    if g > 0:
        x0 = 3.6 - g / 2
        fig.add_trace(go.Scatter(x=[x0, x0 + g], y=[4.0, 4.0], mode="lines", line=dict(color=GREEN, width=7),
                                 hoverinfo="skip"), row=1, col=1)
    fig.add_annotation(x=3.6, y=4.42, text=f"doorway free for the centre: {g:.2f} m" if g > 0 else
                       "doorway closed: no free centre", showarrow=False,
                       font=dict(size=19, color=GREEN if g > 0 else RED), row=1, col=1)
    fig.add_trace(k.board_trace(0, 0, th), row=1, col=2)
    fig.add_trace(go.Scatter(x=[0, 0.8 * np.cos(th)], y=[0, 0.8 * np.sin(th)], mode="lines+markers",
                             line=dict(color=ORANGE, width=4), marker=dict(symbol="arrow", size=[0, 16],
                             angleref="previous", color=ORANGE), hoverinfo="skip"), row=1, col=2)
    fig.update_xaxes(range=[-0.15, 7.15], dtick=1, title="x (m)", row=1, col=1)
    fig.update_yaxes(range=[-0.15, 4.65], dtick=1, title="y (m)", scaleanchor="x", constrain="domain", row=1, col=1)
    fig.update_xaxes(constrain="domain", row=1, col=1)
    fig.update_xaxes(range=[-0.95, 0.95], visible=False, row=1, col=2)
    fig.update_yaxes(range=[-0.95, 0.95], visible=False, scaleanchor="x2", row=1, col=2)
    k.layout(fig, 1250, 640, f"heading θ = {d}°", margin=dict(l=70, r=20, t=100, b=60))
    fig.update_annotations(font_size=20, selector=dict(text="slice of C-space at this heading"))
    fig.update_annotations(font_size=20, selector=dict(text="the board"))
    return fig


ds = list(range(0, 181, 10))
figs = [frame(d) for d in ds]
holds = [6] + [2] * (len(ds) - 2) + [12]
holds[ds.index(90)] = 8
make_gif(figs, here / "slices", fps=3, holds=holds, keys=[0, 3, 6, 9, 12, 18], cols=2, width=1000)
