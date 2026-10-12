"""Animation: the preimage of the cup holder for the command "move down", in the cup's C-space (orange: the grown
posts, bottle and table; the cup is the point at the middle of its bottom). The motion's direction may be off by up
to 10 degrees; five possible directions (260 to 280 degrees) are drawn from one start, 0.8 cm right of the slot's
centre and 2 cm above the posts. Without sliding, a touch anywhere but the slot's bottom is a failure: the preimage
(the starts from which every direction ends in the holder) is a sliver in the slot, at most 1 cm wide, up to 0.8 cm
above the posts. With sliding along the chamfers (friction coefficient 0.4), the preimage is a triangle 3 cm wide at
the mouth and 8.5 cm tall. A start known only to within 1 cm either side fits inside it up to 2.8 cm above the posts.
Run -> preimage.gif, preimage_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

import armdraw as ad
import holder as H
import manip as m
from gifkit import BLUE, FONT, GREEN, ORANGE, RED, make_gif

here = Path(__file__).parent
S = (H.B + 0.008, H.MOUTH + 0.02)
FAN = [260, 265, 270, 275, 280]
xs, ys, G0 = H.preimage_grid(False, h=0.001)
_, _, G1 = H.preimage_grid(True, h=0.001)
top0 = ys[G0.any(1)].max() - H.MOUTH
top1 = ys[G1.any(1)].max() - H.MOUTH
assert round(top0, 3) == 0.008 and round(top1, 3) == 0.085
j = np.argmin(abs(ys - H.MOUTH))
assert round(xs[G1[j]].max() - xs[G1[j]].min() + 0.001, 3) == 0.029
h_ok = (0.015 - 0.01) / np.tan(np.radians(10))
assert round(h_ok, 4) == 0.0284
fans = {slide: [H.run(S, a, slide, log := []) + (log,) for a in FAN] for slide in (False, True)}
assert sum(ok for _, ok, _ in fans[False]) == 1 and all(ok for _, ok, _ in fans[True])
assert all(H.MOUTH - 0.0101 < e[1] < H.MOUTH + 1e-9 and e[0] > H.B for e, ok, _ in fans[False] if not ok)


def frame(title, shade=None, fan=None, bands=(), lines=()):
    fig = go.Figure()
    O = H.O.intersection(m.box(0.36, -0.12, 0.48, 0.012))
    for g in getattr(O, "geoms", [O]):
        ad.poly(fig, g, "rgba(245,133,24,0.28)", ORANGE)
    if shade is not None:
        Gs, col = shade
        X, Y = np.meshgrid(xs, ys)
        fig.add_trace(go.Scatter(x=X[Gs], y=Y[Gs], mode="markers", hoverinfo="skip",
                                 marker=dict(color=col, size=5, symbol="square")))
    if fan is not None:
        for end, ok, log in fans[fan]:
            L = np.array(log)
            fig.add_trace(go.Scatter(x=L[:, 0], y=L[:, 1], mode="lines", line=dict(color=GREEN if ok else RED, width=3)))
            fig.add_trace(go.Scatter(x=[end[0]], y=[end[1]], mode="markers",
                                     marker=dict(color=GREEN if ok else RED, size=11, symbol="circle" if ok else "x")))
        fig.add_trace(go.Scatter(x=[S[0]], y=[S[1]], mode="markers", marker=dict(color="black", size=12)))
    for (y, ok) in bands:
        fig.add_trace(go.Scatter(x=[H.B - 0.01, H.B + 0.01], y=[y, y], mode="lines+markers",
                                 line=dict(color=GREEN if ok else RED, width=6), marker=dict(size=10, symbol="line-ns",
                                                                                              line=dict(width=3))))
    for k, (s, c) in enumerate(lines):
        fig.add_annotation(x=0.63, y=0.95 - 0.07 * k, xref="paper", yref="paper", xanchor="left", yanchor="top",
                           text=s, showarrow=False, font=dict(size=19, color=c))
    fig.update_xaxes(range=[0.37, 0.47], dtick=0.02, title="x of the cup's bottom (m)", showgrid=False,
                     domain=[0, 0.58], constrain="domain")
    fig.update_yaxes(range=[-0.105, 0.012], dtick=0.02, title="y (m)", showgrid=False, scaleanchor="x",
                     constrain="domain")
    fig.update_layout(template="simple_white", width=1300, height=700, font=FONT, showlegend=False,
                      title=dict(text=title, x=0.5, font=dict(size=22)), margin=dict(l=80, r=20, t=80, b=60))
    return fig


figs, holds = [], []
figs.append(frame("move down: the direction may be off by up to 10 degrees", fan=None,
                  lines=[("the cup's C-space near B:", "black"), ("orange: grown posts, bottle", ORANGE),
                         ("and table; slot 1 cm wide", ORANGE), ("", "black"), ("command: move down until", "black"),
                         ("stopped; the real direction", "black"), ("is within 10 degrees of down", "black")]))
holds.append(8)
figs.append(frame("without sliding: a touch outside the slot's bottom fails", fan=False,
                  lines=[("five possible directions from", "black"), ("the start (black dot):", "black"),
                         ("1 of 5 reaches the bottom", GREEN), ("4 of 5 stop on the chamfer", RED), ("", "black"),
                         ("not guaranteed", RED)]))
holds.append(10)
figs.append(frame("without sliding: the preimage is a sliver inside the slot", shade=(G0, "rgba(84,162,75,0.6)"),
                  lines=[("green: every start from which", "black"), ("all directions end in the", "black"),
                         ("holder: the preimage", "black"), ("", "black"), ("at most 1 cm wide,", "black"),
                         ("up to 0.8 cm above the posts", "black")]))
holds.append(10)
figs.append(frame("with sliding: the chamfers guide the cup into the slot", fan=True,
                  lines=[("the same five directions:", "black"), ("a touch on a chamfer slides", "black"),
                         ("down it into the slot", "black"), ("all 5 reach the bottom", GREEN), ("", "black"),
                         ("guaranteed", GREEN)]))
holds.append(10)
figs.append(frame("with sliding: the preimage is 3 cm wide and 8.5 cm tall", shade=(G1, "rgba(84,162,75,0.6)"),
                  lines=[("green: the preimage", "black"), ("with sliding", "black"), ("", "black"),
                         ("3 cm wide at the posts' top,", "black"), ("up to 8.5 cm above them", "black")]))
holds.append(10)
figs.append(frame("the hand is known to 1 cm either side: where does a 2 cm band fit?", shade=(G1, "rgba(84,162,75,0.4)"),
                  bands=[(H.MOUTH + 0.014, True), (H.MOUTH + 0.05, False)],
                  lines=[("bands: every start the hand", "black"), ("could be at, 1 cm either side", "black"), ("", "black"),
                         ("1.4 cm above the posts:", "black"), ("inside: guaranteed", GREEN), ("", "black"),
                         ("5 cm above the posts:", "black"), ("sticks out: not guaranteed", RED), ("", "black"),
                         ("fits up to 2.8 cm above", "black")]))
holds.append(16)
make_gif(figs, here / "preimage", fps=2, holds=holds, keys=[1, 2, 3, 5], cols=2, width=1000)
