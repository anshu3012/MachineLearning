"""Scoring the opening scan with the beam model, as an animation. For pose A (2, 2, 0), then pose B (3, 2, 0), each
beam in turn: its beam model is drawn around the beam's expected range z* (from ray casting), its reading is marked
on the curve, the density is read off, and a running product is updated. Pose A ends at 6.26 per m^4, pose B at
0.0291; the last frame shows the backward beam that decides it and the ratio 6.26 / 0.0291 = 215.
Right: the room with the guessed pose; red = what each beam read, drawn from that pose; dashed = where the map says
it should end. Run -> score_anim.gif"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from beammodel import mixture, raycast
from gifkit import BLUE, FONT, GREEN, GREY, RED, make_gif
from roomkit import axes, robot, room, text

here = Path(__file__).parent
READ = [1.00, 1.97, 2.04, 1.99]
ANG = [0, 90, 180, 270]
POSES = [("A", (2.0, 2.0, 0.0), BLUE), ("B", (3.0, 2.0, 0.0), GREEN)]
ZS = {n: [raycast(p, np.radians(a)) for a in ANG] for n, p, _ in POSES}
DENS = {n: [float(mixture(r, e)) for r, e in zip(READ, ZS[n])] for n, _, _ in POSES}
PROD = {n: np.cumprod(DENS[n]) for n in DENS}
G = np.concatenate([np.linspace(0, 4.99, 3000), [4.9949, 4.995, 5.0]])
COLS = [0.625, 0.72, 0.82, 0.90]


def fmt(p):
    """A scan density to three significant figures, as the Note's Section 5.2 table writes it: 6.26, 0.0291."""
    return f"{p:.3g}"


def curve_axes(fig, title):
    fig.update_layout(xaxis=dict(domain=[0, 0.54], anchor="y", range=[0, 5.1], dtick=1, title="reading z (m)"),
                      yaxis=dict(domain=[0, 0.84], anchor="x", range=[0, 6.6], title="density (per m)"))
    text(fig, 0.27, 0.93, title, size=20, anchor="center")


def mark(fig, r, d, col, label_up=True, ax=None):
    fig.add_trace(go.Scatter(x=[r, r], y=[0, 6.6], mode="lines", line=dict(color=RED, width=2, dash="dot")))
    fig.add_annotation(x=r, y=d, ax=ax or (60 if r < 2.5 else -60), ay=-55 if label_up else -110, text=f"{d:.3f} per m",
                       font=dict(color=col, size=20), arrowcolor=col, arrowwidth=2, bgcolor="white")
    fig.add_trace(go.Scatter(x=[r], y=[d], mode="markers", marker=dict(size=13, color=col)))


def room_view(fig, name, pose, col, k):
    axes(fig, ax="3", dom=(0.62, 0.98), ydom=(0.5, 0.97), ticks=False, titles=False)
    room(fig, ax="3")
    px, py, _ = pose
    for j in range(k + 1):
        a = np.radians(ANG[j])
        fig.add_trace(go.Scatter(x=[px, px + READ[j] * np.cos(a)], y=[py, py + READ[j] * np.sin(a)],
                                 mode="lines+markers", line=dict(color=RED, width=4 if j == k else 2),
                                 marker=dict(size=[0, 10 if j == k else 6], color=RED), xaxis="x3", yaxis="y3"))
    a = np.radians(ANG[k])
    e = ZS[name][k]
    fig.add_trace(go.Scatter(x=[px, px + e * np.cos(a)], y=[py, py + e * np.sin(a)], mode="lines",
                             line=dict(color=col, width=3, dash="dash"), xaxis="x3", yaxis="y3"))
    robot(fig, px, py, ax="3", arrow=0.3)
    text(fig, 0.80, 0.465, "red: the reading; dashed: z* from the map", GREY, size=16, anchor="center")


def table(fig, name, col, k):
    text(fig, COLS[0], 0.42, f"pose {name}", col, size=21)
    for c, h in zip(COLS, ["beam", "reading", "z*", "density"]):
        text(fig, c, 0.355, h, GREY, size=18)
    for j in range(4):
        cells = [f"{ANG[j]}°", f"{READ[j]:.2f}", f"{ZS[name][j]:.1f}", f"{DENS[name][j]:.3f}" if j <= k else "…"]
        for c, s in zip(COLS, cells):
            text(fig, c, 0.29 - 0.065 * j, s, RED if (j == k and c == COLS[3]) else "black", size=19)
    p = PROD[name][k]
    text(fig, COLS[0], 0.0, f"running product: {fmt(p)}" if k < 3 else f"product: {fmt(p)} per m⁴", col, size=21)


def frame(name, pose, col, k):
    fig = go.Figure()
    curve_axes(fig, f"beam model of this beam: expected range z* = {ZS[name][k]:.1f} m")
    fig.add_trace(go.Scatter(x=G, y=mixture(G, ZS[name][k]), mode="lines", line=dict(color="black", width=2.5)))
    fig.add_trace(go.Scatter(x=[ZS[name][k]] * 2, y=[0, 6.6], mode="lines", line=dict(color=col, width=2, dash="dash")))
    mark(fig, READ[k], DENS[name][k], RED)
    room_view(fig, name, pose, col, k)
    table(fig, name, col, k)
    title = f"pose {name} ({pose[0]:g}, {pose[1]:g}, 0), beam {ANG[k]}°: reading {READ[k]:.2f} m, expected {ZS[name][k]:.1f} m"
    fig.update_layout(template="simple_white", width=1150, height=720, font=FONT, showlegend=False,
                      margin=dict(l=80, r=20, t=70, b=70), title=dict(text=title, x=0.5))
    return fig


def final():
    fig = go.Figure()
    curve_axes(fig, "the backward beam (180°) decides: reading 2.04 m")
    for (name, _, col), up, side in zip(POSES, (True, False), ("right", "left")):
        e = ZS[name][2]
        fig.add_trace(go.Scatter(x=G, y=mixture(G, e), mode="lines", line=dict(color=col, width=2.5)))
        mark(fig, READ[2], DENS[name][2], col, label_up=up, ax=None if up else -100)
        text(fig, e - 0.1 if side == "right" else e + 0.1, 6.25, f"pose {name}: z* = {e:.1f} m", col, size=19,
             ref=("x", "y"), anchor=side)
    for i, (name, _, col) in enumerate(POSES):
        y0 = 0.9 - 0.36 * i
        text(fig, COLS[0], y0, f"pose {name}", col, size=22)
        text(fig, COLS[0], y0 - 0.07, " × ".join(f"{d:.3f}" for d in DENS[name]), "black", size=18)
        text(fig, COLS[0], y0 - 0.14, f"= {fmt(PROD[name][-1])} per m⁴", col, size=22)
    ratio = PROD["A"][-1] / PROD["B"][-1]
    text(fig, COLS[0], 0.12, f"ratio: {fmt(PROD['A'][-1])} / {fmt(PROD['B'][-1])} = {ratio:.0f}", "black", size=22)
    text(fig, COLS[0], 0.05, f"pose A is about {ratio:.0f} times more likely", "black", size=19)
    fig.update_layout(template="simple_white", width=1150, height=720, font=FONT, showlegend=False,
                      margin=dict(l=80, r=20, t=70, b=70),
                      title=dict(text="the scan scores pose A 6.26 and pose B 0.0291", x=0.5))
    return fig


figs, holds = [], []
for name, pose, col in POSES:
    for k in range(4):
        figs.append(frame(name, pose, col, k))
        holds.append(5 if k < 3 else 8)
figs.append(final())
holds.append(16)
make_gif(figs, here / "score_anim", fps=2, holds=holds, keys=[3, 8], cols=2, width=950)
assert ZS == {"A": [3.0, 2.0, 2.0, 2.0], "B": [2.0, 2.0, 3.0, 2.0]}                 # the z* table of Section 5.2
assert [round(d, 3) for d in DENS["A"]] == [0.049, 5.019, 4.361, 5.886]
assert [round(d, 3) for d in DENS["B"]] == [0.049, 5.019, 0.020, 5.886]
assert round(PROD["A"][-1], 2) == 6.26 and round(PROD["B"][-1], 4) == 0.0291
assert round(PROD["A"][-1] / PROD["B"][-1]) == 215
