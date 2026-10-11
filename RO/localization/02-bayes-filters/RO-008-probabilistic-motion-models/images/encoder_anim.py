"""Wheel odometry from encoder ticks, played. Top left: the right and the left wheel's encoder discs (slots drawn as 24;
the Note's discs have 1000 per turn) turn for one step of 0.1 s while their counters run up to 191 and 127 ticks (the
wheel spin rates 12 and 8 rad/s of RO-001). Right: the three steps of wheel odometry fill in: ticks to wheel distances
(60.0 and 39.9 mm), to the robot's move (forward 49.95 mm, turn 0.1005 rad), to the new pose (2.0433, 1.0250, 0.6241).
Bottom left: the robot moves to that pose. The step then repeats four times, each from the last pose, with the same
counts. The last frame holds the numbers and the five poses.
Run: python encoder_anim.py -> encoder_anim.gif, encoder_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, RED, make_gif
from motion import START
from robotdraw import L, R_WHEEL, robot, step

here = Path(__file__).parent
N = 1000                                                   # ticks per wheel turn
TR, TL = 191, 127                                          # ticks in one step of 0.1 s
TICK = 2 * np.pi * R_WHEEL / N
dR, dL = TR * TICK, TL * TICK
DS, DTH = (dR + dL) / 2, (dR - dL) / L
POSES = [START]
for _ in range(5):
    POSES.append(step(POSES[-1], DS, DTH, 1.0))            # Euler step: move along the old heading, then turn
POSES = np.array(POSES)
assert round(TICK * 1000, 3) == 0.314 and round(dR * 1000, 1) == 60.0 and round(dL * 1000, 1) == 39.9
assert round(DS * 1000, 2) == 49.95 and round(DTH, 4) == 0.1005
assert [round(v, 4) for v in POSES[1]] == [2.0433, 1.0250, 0.6241]
assert [round(v, 4) for v in POSES[5]] == [2.1851, 1.1639, 1.0263]                 # after 0.5 s, in the caption
assert round(TR / N * 2 * np.pi, 1) == 1.2 and round(TL / N * 2 * np.pi, 1) == 0.8     # 12 and 8 rad/s for 0.1 s
DISCS = [("right wheel", 0.0, RED), ("left wheel", 5.8, PURPLE)]
BOXES = [("1. ticks to wheel distances", BLUE, "rgba(76,120,168,0.10)", 0.985, 0.745),
         ("2. wheel distances to robot motion", GREEN, "rgba(84,162,75,0.10)", 0.66, 0.46),
         ("3. robot motion to the world frame", PURPLE, "rgba(178,121,162,0.10)", 0.375, 0.0)]
fmt = lambda q: f"({q[0]:.4f}, {q[1]:.4f}, {q[2]:.4f})"


def disc(fig, cx, ang, col):
    """One encoder disc centred at (cx, 0), turned by ang (rad, anticlockwise), drawn with 24 slots."""
    t = np.linspace(0, 2 * np.pi, 120)
    fig.add_trace(go.Scatter(x=cx + 2 * np.cos(t), y=2 * np.sin(t), mode="lines", fill="toself", fillcolor="#e0e0e0",
                             line=dict(color="black", width=3)))
    sx, sy = [], []
    for a in np.radians(np.arange(0, 360, 15)) + ang:
        c, s = np.cos(a), np.sin(a)
        for r, w in ((1.45, -0.06), (1.9, -0.06), (1.9, 0.06), (1.45, 0.06), (1.45, -0.06)):
            sx.append(cx + r * c - w * s)
            sy.append(r * s + w * c)
        sx.append(None)
        sy.append(None)
    fig.add_trace(go.Scatter(x=sx, y=sy, mode="lines", fill="toself", fillcolor="white", line=dict(width=0)))
    fig.add_trace(go.Scatter(x=[cx, cx + 1.1 * np.cos(np.pi / 2 + ang)], y=[0, 1.1 * np.sin(np.pi / 2 + ang)],
                             mode="lines+markers", line=dict(color=col, width=4), marker=dict(size=[0, 14], color=col)))
    fig.add_trace(go.Scatter(x=[cx], y=[0], mode="markers", marker=dict(size=22, color="black")))
    fig.add_shape(type="rect", x0=cx + 1.45, x1=cx + 1.95, y0=2.3, y1=2.6, fillcolor=ORANGE, line_width=0, opacity=1)
    fig.add_shape(type="line", x0=cx + 1.7, x1=cx + 1.7, y0=2.3, y1=0.8, line=dict(color=ORANGE, dash="dash", width=2), opacity=1)
    fig.add_shape(type="rect", x0=cx + 1.45, x1=cx + 1.95, y0=0.55, y1=0.8, fillcolor=BLUE, line_width=0, opacity=1)


def text(x, y, s, col="black", size=21, anchor="center", ref="paper"):
    return dict(x=x, y=y, xref=ref if ref == "paper" else "x", yref=ref if ref == "paper" else "y", text=s,
                showarrow=False, xanchor=anchor, yanchor="middle", font=dict(color=col, size=size))


def frame(title, f, k, nbox, done):
    """f: fraction of this step's ticks counted; k: step number (1 to 5); nbox: boxes filled (0 to 3);
    done: steps finished so far (0 to 5)."""
    fig = go.Figure()
    nr, nl = round(TR * f), round(TL * f)
    for (name, cx, col), n in zip(DISCS, (nr, nl)):
        disc(fig, cx, ((k - 1) * (TR if cx == 0 else TL) + n) * 2 * np.pi / N, col)
        fig.add_annotation(**text(cx, 2.95, f"<b>{name}</b>", col, 22, ref="x"))
        fig.add_annotation(**text(cx, -2.55, f"in this 0.1 s: {n} ticks", col, 22, ref="x"))
    fig.add_annotation(**text(2.0, 2.45, "light", ORANGE, 18, "left", ref="x"))
    fig.add_annotation(**text(2.0, 0.67, "sensor", BLUE, 18, "left", ref="x"))
    fig.add_annotation(**text(2.9, -3.3, "one tick per slot that passes the light (24 slots drawn; the real disc has "
                                         "1000)", GREY, 18, ref="x"))
    # the three boxes
    lines = [["one tick = 2π × 0.05 / 1000 = 0.314 mm", f"right: {TR} ticks = {dR * 1000:.1f} mm",
              f"left: {TL} ticks = {dL * 1000:.1f} mm"],
             [f"forward Δs = {DS * 1000:.2f} mm", f"turn Δθ = {DTH:.4f} rad"],
             [f"start: {fmt(POSES[0]).replace('2.0000', '2').replace('1.0000', '1')}"]
             + [f"after {j / 10:.1f} s: {fmt(POSES[j])}" for j in range(1, done + 1)]]
    for i, (head, col, fill, y1, y0) in enumerate(BOXES):
        fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.55, x1=1.0, y0=y0, y1=y1, fillcolor=fill,
                      line=dict(color=col, width=2.5), opacity=1)
        fig.add_annotation(**text(0.775, y1 - 0.035, f"<b>{head}</b>", "black", 21))
        if i < nbox:
            for j, s in enumerate(lines[i]):
                fig.add_annotation(**text(0.775, y1 - 0.09 - 0.05 * j, s, "black", 20))
        if i < 2:
            gap = (y0 - BOXES[i + 1][3]) * 760                 # px between the boxes (plot height 760 px)
            fig.add_annotation(x=0.775, y=BOXES[i + 1][3], ax=0, ay=-gap, xref="paper", yref="paper", text="",
                               showarrow=True, arrowhead=2, arrowwidth=2.5, arrowcolor=GREY)
    # the robot in the world frame
    path = POSES[:done + 1]
    fig.add_trace(go.Scatter(x=path[:, 0], y=path[:, 1], mode="lines+markers", line=dict(color=PURPLE, width=2),
                             marker=dict(size=10, color=PURPLE), xaxis="x2", yaxis="y2"))
    for tr in robot(tuple(path[-1]), scale=0.25):
        tr.update(xaxis="x2", yaxis="y2")
        fig.add_trace(tr)
    fig.update_layout(
        xaxis=dict(domain=[0, 0.5], range=[-2.6, 8.4], visible=False),
        yaxis=dict(domain=[0.5, 1.0], range=[-3.5, 3.2], visible=False, scaleanchor="x"),
        xaxis2=dict(domain=[0.07, 0.47], range=[1.95, 2.24], dtick=0.1, title="x (m)", anchor="y2", showgrid=True,
                    gridcolor="#eee"),
        yaxis2=dict(domain=[0.0, 0.4], range=[0.95, 1.24], dtick=0.1, title="y (m)", anchor="x2", showgrid=True,
                    gridcolor="#eee", scaleanchor="x2"),
        template="simple_white", width=1200, height=900, font=FONT, showlegend=False,
        margin=dict(l=40, r=20, t=80, b=60), title=dict(text=title, x=0.5, y=0.975, font=dict(size=23)))
    return fig


figs, holds = [], []
add = lambda f, h: (figs.append(f), holds.append(h))
add(frame("the first 0.1 s: each encoder counts the slots that pass its light", 0, 1, 0, 0), 8)
for i in range(1, 6):
    add(frame("the first 0.1 s: each encoder counts the slots that pass its light", i / 5, 1, 0, 0),
        2 if i < 5 else 6)
add(frame("1. ticks to wheel distances", 1, 1, 1, 0), 8)
add(frame("2. wheel distances to the robot's move", 1, 1, 2, 0), 8)
add(frame("3. the move added to the pose (2, 1, 0.5236)", 1, 1, 3, 1), 12)
key = [len(figs) - 1]
for k in range(2, 6):
    t = f"t = {k / 10:.1f} s: the next 0.1 s, the same counts, added to the last pose"
    add(frame(t, 0.5, k, 3, k - 1), 2)
    add(frame(t, 1, k, 3, k), 4 if k < 5 else 24)
key.append(len(figs) - 1)
make_gif(figs, here / "encoder_anim", fps=4, holds=holds, keys=key, cols=2, width=950)
