"""Resampling the five particles of the worked example, step by step. Their normalised weights 0.0031, 0.3313,
0.3313, 0.0031, 0.3313 are laid end to end from 0 to 1, one stretch per particle. Top: plain (multinomial)
resampling, five independent random numbers 0.33, 0.99, 0.32, 0.79, 0.87 land one at a time: copies 0, 2, 0, 0, 3,
so particle 3 is lost. Bottom: the low-variance sampler, one random start r = 0.12, then a pointer every
1/M = 0.2: copies 0, 2, 1, 0, 2. The last frame shows both, plain resampling on top.
Run: python resample_anim.py -> resample_anim.gif, resample_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, PURPLE, RED, make_gif
from pfsim import likelihood, low_variance

here = Path(__file__).parent
P = np.array([0.7, 1.6, 2.4, 3.3, 6.9])                     # the five particles of Section 4.2 (m)
w = likelihood(1.46, P)
w = w / w.sum()
ends = np.cumsum(w)
DARTS = [0.33, 0.99, 0.32, 0.79, 0.87]
R, M = 0.12, len(w)
POINTERS = [R + k / M for k in range(M)]
plain = np.searchsorted(ends, DARTS, side="right")
lowvar = low_variance(w, None, r=R)
assert np.allclose(w.round(4), [0.0031, 0.3313, 0.3313, 0.0031, 0.3313])
assert np.allclose(ends.round(4), [0.0031, 0.3344, 0.6656, 0.6687, 1.0])
assert list(np.bincount(plain, minlength=M)) == [0, 2, 0, 0, 3]
assert list(np.bincount(lowvar, minlength=M)) == [0, 2, 1, 0, 2]
assert np.allclose(POINTERS, [0.12, 0.32, 0.52, 0.72, 0.92])

LIGHT, MID, SLIVER = "#C3D2E4", "#9DB4D2", "#B9B9B9"         # cblue!35, cblue!55, cgrey!60 of the TikZ still
FILL = [SLIVER, LIGHT, MID, SLIVER, LIGHT]
BARS = {"plain": 5.0, "lv": 0.8}                            # bottom edge of each bar (data units); bars are 0.6 high
starts = np.concatenate([[0], ends[:-1]])


def text(fig, x, y, s, color="black", size=20, anchor="left", **kw):
    fig.add_annotation(x=x, y=y, text=s, showarrow=False, xanchor=anchor, font=dict(size=size, color=color), **kw)


def bar(fig, y0, shown, hit=None):
    """The five stretches (the first `shown` of them filled); `hit`: the stretch outlined as just picked."""
    fig.add_shape(type="rect", x0=0, x1=1, y0=y0, y1=y0 + 0.6, line=dict(color="black", width=2), opacity=1,
                  fillcolor="rgba(0,0,0,0)")
    for i in range(shown):
        fig.add_shape(type="rect", x0=starts[i], x1=ends[i], y0=y0, y1=y0 + 0.6, fillcolor=FILL[i],
                      line=dict(color="black", width=2), layer="below", opacity=1)
        if i in (1, 2, 4):
            text(fig, (starts[i] + ends[i]) / 2, y0 + 0.3, str(i + 1), size=24, anchor="center")
    if hit is not None:
        fig.add_shape(type="rect", x0=starts[hit], x1=ends[hit], y0=y0 - 0.06, y1=y0 + 0.66,
                      line=dict(color="black", width=6), opacity=1, fillcolor="rgba(0,0,0,0)")
    text(fig, 0, y0 - 0.3, "0", size=19, anchor="center")
    text(fig, 1, y0 - 0.3, "1", size=19, anchor="center")


def arrows(fig, y0, xs, color, gap=None):
    """Arrows dropping onto the bar at the values xs, each labelled with its value."""
    for x in xs:
        fig.add_annotation(x=x, y=y0 + 0.66, ax=x, ay=y0 + 1.45, xref="x", yref="y", axref="x", ayref="y", text="",
                           showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=4, arrowcolor=color)
        anchor = "right" if x == 0.32 and 0.33 in xs else "left" if x == 0.33 and 0.32 in xs else "center"
        dx = {"right": -0.003, "left": 0.003, "center": 0}[anchor]
        text(fig, x + dx, y0 + 1.68, f"{x:.2f}", color, size=20, anchor=anchor)
    if gap is not None:                                      # the spacing just added: from a to b
        a, b, label = gap
        fig.add_annotation(x=b, y=y0 + 1.05, ax=a, ay=y0 + 1.05, xref="x", yref="y", axref="x", ayref="y", text="",
                           showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2.5, arrowcolor=GREY)
        text(fig, (a + b) / 2, y0 + 1.25, label, GREY, size=19, anchor="center")


def copies(idx):
    c = np.bincount(np.asarray(idx, dtype=int), minlength=M)
    return ",  ".join(str(v) for v in c)


def frame(title, shown=5, nd=0, npt=0, hit=None, gap=None, plain_note="", lv_note=""):
    fig = go.Figure()
    y = BARS["plain"]
    text(fig, 0, y + 2.35, "<b>plain (multinomial) resampling: five independent random numbers</b>", size=22)
    bar(fig, y, shown, hit if nd and hit is not None and npt == 0 else None)
    arrows(fig, y, DARTS[:nd], PURPLE)
    if shown == 5:
        text(fig, 0, y - 0.75, f"copies of particles 1 to 5:   {copies(plain[:nd])}" + plain_note, size=20)
    y = BARS["lv"]
    text(fig, 0, y + 2.35, "<b>low-variance sampler: one random start r = 0.12, then a pointer every 1/M = 0.2</b>",
         size=22)
    bar(fig, y, shown, hit if npt and hit is not None else None)
    arrows(fig, y, POINTERS[:npt], RED, gap)
    if shown == 5:
        text(fig, 0, y - 0.75, f"copies of particles 1 to 5:   {copies(lowvar[:npt])}" + lv_note, size=20)
    if shown < 5:
        text(fig, 0, 4.25, "weights of particles 1 to 5:   0.0031,  0.3313,  0.3313,  0.0031,  0.3313", size=20)
    text(fig, 0, -1.25, "grey slivers: particles 1 and 4 (weight 0.0031 each); blue: particles 2, 3 and 5 "
         "(weight 0.3313 each)", GREY, size=18)
    fig.update_xaxes(range=[-0.03, 1.03], visible=False)
    fig.update_yaxes(range=[-1.5, 7.6], visible=False)
    fig.update_layout(template="simple_white", font=FONT, width=1100, height=760, showlegend=False,
                      margin=dict(l=30, r=30, t=80, b=20), title=dict(x=0.5, y=0.975, font=dict(size=23), text=title))
    return fig


name = lambda i: f"particle {i + 1}"
figs, holds, keys = [], [], []


def add(fig, hold, key=False):
    figs.append(fig)
    holds.append(hold)
    if key:
        keys.append(len(figs) - 1)


add(frame("1. lay the five weights end to end along the line from 0 to 1", shown=0), 5)
for i in range(M):
    add(frame(f"particle {i + 1}: weight {w[i]:.4f}, its stretch ends at {ends[i]:.4f}", shown=i + 1), 3)
add(frame("2. each particle owns a stretch as long as its weight"), 5)
for k in range(M):
    add(frame(f"plain: random number {DARTS[k]:.2f} lands in {name(plain[k])}'s stretch, one copy for it",
              nd=k + 1, hit=plain[k]), 4, key=k == 0)
add(frame("plain: particle 3 carries a third of the weight but got no copy", nd=M,
          plain_note="     particle 3 is lost"), 8, key=True)
for k in range(M):
    gap = (0, R, "r = 0.12") if k == 0 else (POINTERS[k - 1], POINTERS[k], "+ 0.2")
    what = "one random start r = 0.12" if k == 0 else f"next pointer 0.2 further, at {POINTERS[k]:.2f}"
    add(frame(f"low-variance: {what}, lands in {name(lowvar[k])}", nd=M, npt=k + 1, hit=lowvar[k], gap=gap,
              plain_note="     particle 3 is lost"), 4, key=k == 0)
add(frame("3. plain loses particle 3 by chance; the evenly spaced pointers keep 2, 3 and 5", nd=M, npt=M,
          plain_note="     particle 3 (weight 0.33) is lost",
          lv_note="     every particle with weight ≥ 0.2 is kept"), 14, key=True)
make_gif(figs, here / "resample_anim", fps=2, holds=holds, keys=keys, cols=2, width=900)
