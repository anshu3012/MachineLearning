"""How one reading is made and how a scan forms, in the room of Figure 1.
Part 1: the forward beam's pulse goes out to the person 1.00 m ahead and comes back; the clock stops at 6.67 ns;
light covers about 0.3 m per ns, so the pulse travelled 2.00 m, and half of that, 1.00 m, is the reading.
Part 2: the head turns and fires every 0.5 degrees; the readings (with noise of 0.05 m) outline the room and the
person. A glass pane in the top wall lets beams out; they meet nothing within 5 m, no echo returns in time, and
the sensor reports its longest distance, 5 m. Run -> pulse_scan.gif"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from beammodel import POSE, ROOM, SIG_HIT, ZMAX
from gifkit import FONT, GREY, PURPLE, RED, make_gif
from roomkit import C_NS, PERSON, axes, person, robot, room, text

here = Path(__file__).parent
X0, Y0, _ = POSE
GLASS = (3.5, 4.5)                              # the glass pane: top wall (y = 4) from x = 3.5 to 4.5 m
FIG1 = {0: 1.00, 180: 1.97, 360: 2.04, 540: 1.99}  # beam index (0.5 degree steps) -> reading of Figure 1


def cast(a):
    """Distance along direction a to the person or a wall; ZMAX when the beam leaves through the glass."""
    c, s = np.cos(a), np.sin(a)
    ts = [t for t in ((ROOM[0] - X0) / c if c > 1e-12 else np.inf, -X0 / c if c < -1e-12 else np.inf,
                      (ROOM[1] - Y0) / s if s > 1e-12 else np.inf, -Y0 / s if s < -1e-12 else np.inf)]
    t = min(ts)
    hx, hy = X0 + t * c, Y0 + t * s
    glass = abs(hy - ROOM[1]) < 1e-9 and GLASS[0] < hx < GLASS[1]
    dx, dy = PERSON[0] - X0, PERSON[1] - Y0
    tc = dx * c + dy * s
    h2 = dx * dx + dy * dy - tc * tc
    if tc > 0 and h2 <= PERSON[2] ** 2:
        return tc - np.sqrt(PERSON[2] ** 2 - h2), False
    return (ZMAX, True) if glass else (t, False)


rng = np.random.default_rng(1)
ANG = np.radians(np.arange(720) * 0.5)
z, lost = np.empty(720), np.zeros(720, bool)
for i, a in enumerate(ANG):
    d, lost[i] = cast(a)
    z[i] = d if lost[i] else np.round(d + rng.normal(0, SIG_HIT), 2)
for i, v in FIG1.items():
    z[i] = v
EX, EY = X0 + z * np.cos(ANG), Y0 + z * np.sin(ANG)


def base(title):
    fig = go.Figure()
    axes(fig, xr=(-0.35, 6.15), yr=(-0.35, 6.25), dom=(0.0, 0.56))
    room(fig)
    fig.add_shape(type="line", x0=GLASS[0], x1=GLASS[1], y0=4, y1=4, line=dict(color="#A6CEE3", width=7), opacity=1)
    text(fig, 4.0, 4.28, "glass", GREY, size=18, ref=("x", "y"), anchor="center")
    person(fig)
    fig.update_layout(template="simple_white", width=1100, height=640, font=FONT, showlegend=False,
                      margin=dict(l=30, r=20, t=70, b=20), title=dict(text=title, x=0.5, font_size=22))
    return fig


def pulse(s, title, lines):
    """Part 1: the pulse has travelled s metres (out to the person at 1.00 m, then back)."""
    fig = base(title)
    d = s if s <= 1 else 2 - s
    if s > 0:
        fig.add_trace(go.Scatter(x=[X0, X0 + min(s, 1.0)], y=[Y0, Y0], mode="lines", line=dict(color=RED, width=3)))
        fig.add_trace(go.Scatter(x=[X0 + d], y=[Y0], mode="markers",
                                 marker=dict(size=17, color=RED, symbol="circle-open", line=dict(width=4))))
    robot(fig, X0, Y0)
    for j, (s_, col, size) in enumerate(lines):
        text(fig, 0.62, 0.86 - 0.11 * j, s_, col, size=size)
    return fig


def sweep(n, title, lines):
    """Part 2: the first n beams (0.5 degrees apart) have been fired."""
    fig = base(title)
    hit, out = ~lost[:n], lost[:n]
    for m, col in ((hit, RED), (out, PURPLE)):
        xs = np.column_stack([np.full(m.sum(), X0), EX[:n][m], np.full(m.sum(), np.nan)]).ravel()
        ys = np.column_stack([np.full(m.sum(), Y0), EY[:n][m], np.full(m.sum(), np.nan)]).ravel()
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=col, width=1), opacity=0.18))
        fig.add_trace(go.Scatter(x=EX[:n][m], y=EY[:n][m], mode="markers", marker=dict(size=5, color=col)))
    k = n - 1
    fig.add_trace(go.Scatter(x=[X0, EX[k]], y=[Y0, EY[k]], mode="lines", line=dict(color=PURPLE if lost[k] else RED, width=4)))
    robot(fig, X0, Y0)
    for j, (s_, col, size) in enumerate(lines):
        text(fig, 0.62, 0.86 - 0.11 * j, s_, col, size=size)
    return fig


def clock(s):
    return f"clock: {s / C_NS:.2f} ns"


figs, holds = [], []
steps = [(0.0, "one reading: the laser sends a pulse and starts its clock"),
         (0.5, "the pulse travels out"), (1.0, "the pulse reaches the person"),
         (1.5, "the echo travels back"), (2.0, "the echo is back at the laser")]
for s, title in steps:
    figs.append(pulse(s, title, [(clock(s), "black", 26), (f"path so far: {s:.2f} m", GREY, 20)]))
    holds.append(4 if s in (0.0, 1.0, 2.0) else 2)
figs.append(pulse(2.0, "the reading is half the round trip: 1.00 m",
                  [(clock(2.0), "black", 26), ("light covers 0.3 m per ns", GREY, 20),
                   ("0.3 × 6.67 = 2.00 m, out and back", GREY, 20), ("half of 2.00 m = 1.00 m", RED, 24)]))
holds.append(12)
key = [len(figs) - 1]
for deg in (45, 90, 135, 180, 225, 270, 315, 360):
    n = deg * 2
    last = n == 720
    lines = [("the laser head turns and fires", "black", 22), ("one beam every 0.5°", "black", 22),
             (f"readings so far: {n}", GREY, 20), ("red dot: where a beam stopped", RED, 20)]
    if lost[:n].any():
        lines += [("purple: through the glass, no echo", PURPLE, 20), ("in time, so it reports 5 m", PURPLE, 20)]
    title = "one sweep is one scan: 720 readings" if last else f"the head has turned {deg}°"
    figs.append(sweep(n, title, lines))
    holds.append(20 if last else 3)
key.append(len(figs) - 1)
make_gif(figs, here / "pulse_scan", fps=4, holds=holds, keys=key, cols=2, width=950)
assert round(2.0 / C_NS, 2) == 6.67 and round(0.3 * 6.67, 2) == 2.00   # the clock and the halving
assert lost.sum() > 0 and np.all(z[lost] == ZMAX) and len(z) == 720
assert [z[i] for i in FIG1] == [1.00, 1.97, 2.04, 1.99]                # the four beams of Figure 1
