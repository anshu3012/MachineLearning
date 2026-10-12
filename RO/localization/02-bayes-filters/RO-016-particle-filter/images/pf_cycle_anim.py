"""One round of the particle filter, as an animation of the loop. Top: the three boxes (move, weigh,
resample, same labels and colours); the box of the step being done is lit. Bottom: 100 particles on the corridor,
the first round of the run of pf_loop.gif (seed 2): start spread evenly; weigh by reading 1 (z = 1.46 m), so the
particles at doors grow; resample, so the light ones are dropped and the door ones copied 3 or 4 times; move 2.5 m,
first the command, then each particle's own slip, so the copies spread apart. Reading 1 comes before any move, so
this round starts at step 2 and ends at step 1. Last frame held.
Run: python pf_cycle_anim.py -> pf_cycle_anim.gif, pf_cycle_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif
from pfsim import DOOR, DOORS, LOOP, U, X_TRUE, Z, h, likelihood, low_variance, move, run

here = Path(__file__).parent
M = 100

# the first round of the Figure 8 run, step by step (same seed, same random draws as pfsim.run)
rng = np.random.default_rng(2)
x0 = rng.uniform(0, LOOP, M)
w1 = likelihood(Z[0], x0)
w1 = w1 / w1.sum()
idx = low_variance(w1, rng)
xr = x0[idx]
xm = move(xr, U, rng)
st = run(M, np.random.default_rng(2))
assert [s[0] for s in st[:4]] == ["start", "weigh 1", "resample 1", "move 1"]
assert all(np.allclose(a, s[1]) for a, s in zip((x0, x0, xr, xm), st[:4])) and np.allclose(w1, st[1][2])

# numbers quoted in the frames and the caption
door = h(x0) == DOOR
kept = np.bincount(idx, minlength=M)
dropped = kept == 0
assert door.sum() == 30 and dropped.sum() == 69 and np.all(kept[door] >= 3) and np.all(kept[door] <= 4)
assert (~door & ~dropped).sum() == 1 and round(float(x0[~door & ~dropped][0]), 2) == 1.05   # one light one survives
assert round(float(likelihood(1.46, np.array([2.0]))[0]), 3) == 2.567
assert round(float(likelihood(1.46, np.array([3.0]))[0]), 3) == 0.024
assert np.all(np.diff(np.sort(xr + U)) >= 0) and xm.max() < LOOP and (xr + U).max() < LOOP      # no wrap round
near = np.any([(xm > a + U - 0.4) & (xm < b + U + 0.4) for a, b in DOORS], axis=0)
assert near[door[idx]].all() and near.sum() == 99    # three clusters after the move, each 2.5 m past a door
assert abs(X_TRUE[1] - X_TRUE[0] - 2.52) < 1e-9

jitter = np.random.default_rng(7).uniform(0.15, 0.85, M)       # the heights of pf_loop.gif


def size(w):
    return np.clip(4 + 16 * np.sqrt(w * M), 3, 60)


# the loop, in cm: box centre, half width, half height, colour, text
BOX = {
    "move": (0.0, 0.0, 2.95, 1.35, BLUE, "<b>1. move (predict)</b><br>each particle moves by the command<br>"
             "plus its own random slip<br>(motion model)"),
    "weigh": (8.6, 0.0, 2.95, 1.35, ORANGE, "<b>2. weigh (update)</b><br>weight = <i>p</i>(<i>z</i> | <i>x</i>):<br>"
              "how well the particle explains<br>the reading (sensor model)"),
    "resample": (4.3, -4.2, 2.95, 1.05, GREEN, "<b>3. resample</b><br>draw <i>M</i> new particles,<br>"
                 "each in proportion to its weight"),
}


def rgba(hex_, a):
    return f"rgba({int(hex_[1:3], 16)},{int(hex_[3:5], 16)},{int(hex_[5:7], 16)},{a})"


def rbox(cx, cy, hw, hh, r=0.2):
    x0_, x1, y0, y1 = cx - hw, cx + hw, cy - hh, cy + hh
    return (f"M{x0_ + r},{y0} L{x1 - r},{y0} Q{x1},{y0} {x1},{y0 + r} L{x1},{y1 - r} Q{x1},{y1} {x1 - r},{y1} "
            f"L{x0_ + r},{y1} Q{x0_},{y1} {x0_},{y1 - r} L{x0_},{y0 + r} Q{x0_},{y0} {x0_ + r},{y0} Z")


def arrow(fig, x, y, ax, ay):
    fig.add_annotation(x=x, y=y, ax=ax, ay=ay, xref="x", yref="y", axref="x", ayref="y", text="", showarrow=True,
                       arrowhead=2, arrowsize=1.1, arrowwidth=2.6, arrowcolor=GREY)


def frame(title, lit, cloud_text, pts, robot, dead=None):
    """lit: the box being done (or None). pts: list of (x, y, marker size) arrays for the blue particles.
    dead: (x, y) of particles just dropped, drawn as grey crosses."""
    fig = make_subplots(rows=2, cols=1, row_heights=[0.6, 0.4], vertical_spacing=0.13)
    # the loop
    for name, (cx, cy, hw, hh, col, txt) in BOX.items():
        on = name == lit
        fig.add_shape(type="path", path=rbox(cx, cy, hw, hh), xref="x", yref="y", opacity=1,
                      fillcolor=rgba(col, 0.38 if on else 0.1), line=dict(color=col, width=7 if on else 2.5))
        fig.add_annotation(x=cx, y=cy, xref="x", yref="y", text=txt, showarrow=False, font=dict(size=21),
                           align="center")
    arrow(fig, 5.6, 0, 3.0, 0)
    fig.add_annotation(x=4.3, y=0.25, xref="x", yref="y", yanchor="bottom", text="predicted<br>cloud", showarrow=False,
                       font=dict(size=18))
    fig.add_shape(type="line", x0=8.6, y0=-1.35, x1=8.6, y1=-4.2, xref="x", yref="y",
                  line=dict(color=GREY, width=2.6), opacity=1)
    arrow(fig, 7.3, -4.2, 8.6, -4.2)
    fig.add_annotation(x=8.75, y=-2.75, xref="x", yref="y", xanchor="left", text="weighted cloud", showarrow=False,
                       font=dict(size=18))
    fig.add_shape(type="line", x0=1.35, y0=-4.2, x1=0, y1=-4.2, xref="x", yref="y",
                  line=dict(color=GREY, width=2.6), opacity=1)
    arrow(fig, 0, -1.4, 0, -4.2)
    fig.add_annotation(x=-0.15, y=-2.75, xref="x", yref="y", xanchor="right", text="new cloud,<br>equal weights",
                       showarrow=False, font=dict(size=18), align="right")
    fig.add_annotation(x=4.3, y=1.75, xref="x", yref="y", text="the set of <i>M</i> particles is the belief; one round "
                       "per command and reading", showarrow=False, font=dict(size=18, color=GREY))
    fig.update_xaxes(visible=False, range=[-3.2, 11.8], row=1, col=1)
    fig.update_yaxes(visible=False, range=[-5.4, 2.05], row=1, col=1)
    # the cloud on the corridor
    for a, b in DOORS:
        fig.add_shape(type="rect", x0=a, x1=b, y0=0, y1=1, xref="x2", yref="y2 domain", fillcolor=ORANGE, opacity=0.18,
                      line_width=0, layer="below")
    if dead is not None:
        fig.add_trace(go.Scatter(x=dead[0], y=dead[1], mode="markers", marker=dict(symbol="x-thin", size=11,
                                 line=dict(width=2.5, color=GREY))), row=2, col=1)
    for px, py, ps in pts:
        fig.add_trace(go.Scatter(x=px, y=py, mode="markers", marker=dict(size=ps, color=BLUE, opacity=0.55,
                                 line=dict(width=0))), row=2, col=1)
    fig.add_trace(go.Scatter(x=[robot], y=[1.0], mode="markers+text", marker=dict(symbol="triangle-down", size=22,
                             color=RED), text=["robot"], textposition="middle right",
                             textfont=dict(size=17, color=RED)), row=2, col=1)
    fig.add_annotation(xref="x2 domain", yref="y2 domain", x=0, y=1.1, xanchor="left", yanchor="bottom",
                       text=cloud_text, showarrow=False, font=dict(size=19))
    fig.update_xaxes(title="position x (m)", range=[0, LOOP], dtick=1, row=2, col=1)
    fig.update_yaxes(visible=False, range=[0.05, 1.12], row=2, col=1)
    fig.add_annotation(xref="paper", yref="paper", x=0.5, y=-0.1, yanchor="top", showarrow=False,
                       font=dict(size=16, color=GREY),
                       text="orange: doors; marker size grows with a particle's weight; red triangle: the true robot;<br>"
                            "the heights only spread the particles apart, position is left to right")
    fig.update_layout(template="simple_white", font=FONT, width=1100, height=1080, showlegend=False,
                      margin=dict(l=40, r=40, t=80, b=175),
                      title=dict(x=0.5, y=0.975, font=dict(size=23), text=title))
    return fig


figs, holds, keys = [], [], []
eq = size(np.full(M, 1 / M))
# start
keys.append(len(figs))
figs.append(frame("start: 100 particles spread evenly, weight 1/100 = 0.01 each", None,
                  "reading 1 comes before the first move, so this round starts at step 2, weigh",
                  [(x0, jitter, eq)], X_TRUE[0]))
holds.append(12)
# weigh: the sizes change with the reading
for f in (0.5, 1.0):
    s = size((1 - f) / M + f * w1)
    if f == 1.0:
        keys.append(len(figs))
    figs.append(frame("2. weigh by reading 1, z = 1.46 m: particles at doors grow, the rest shrink", "weigh",
                      "density of the reading: 2.567 at a door particle, 0.024 at a wall particle",
                      [(x0, jitter, s)], X_TRUE[0]))
    holds.append(2 if f < 1 else 12)
# resample: drop the light ones, then the copies fan out from their parent
keys.append(len(figs))
figs.append(frame("3. resample: the 69 light particles are dropped (grey crosses)", "resample",
                  "one light particle, at 1.05 m (blue ring), is picked once by chance",
                  [(x0[~dropped], jitter[~dropped], size(w1[~dropped]))], X_TRUE[0],
                  dead=(x0[dropped], jitter[dropped])))
lucky = np.flatnonzero(~door & ~dropped)[0]
figs[-1].add_trace(go.Scatter(x=[x0[lucky]], y=[jitter[lucky]], mode="markers", marker=dict(symbol="circle-open",
                              size=26, color=BLUE, line=dict(width=3))), row=2, col=1)
holds.append(10)
for f in (1 / 3, 2 / 3, 1.0):
    y = (1 - f) * jitter[idx] + f * jitter
    s = (1 - f) * size(w1[idx]) + f * eq
    if f == 1.0:
        keys.append(len(figs))
    figs.append(frame("3. resample: each door particle is copied 3 or 4 times, all weights equal again", "resample",
                      "each copy sits at its parent's position: one column of dots per door particle",
                      [(xr, y, s)], X_TRUE[0]))
    holds.append(1 if f < 1 else 12)
# move: first the command for all, then each particle's own slip
for f in (0.25, 0.5, 0.75, 1.0):
    if f == 1.0:
        keys.append(len(figs))
    figs.append(frame("1. move: every particle shifts by the command, 2.5 m", "move",
                      "the copies still share their parent's position",
                      [(xr + f * U, jitter, eq)], X_TRUE[0] + f * 2.52))
    holds.append(1 if f < 1 else 8)
for f in (0.5, 1.0):
    if f == 1.0:
        keys.append(len(figs))
    figs.append(frame("1. move: each particle adds its own slip, so the copies spread apart", "move",
                      "one turn done: three clusters, each 2.5 m past a door, ready for reading 2",
                      [(xr + U + f * (xm - xr - U), jitter, eq)], X_TRUE[1]))
    holds.append(1 if f < 1 else 28)

make_gif(figs, here / "pf_cycle_anim", fps=4, holds=holds, keys=keys, cols=2, width=900)
