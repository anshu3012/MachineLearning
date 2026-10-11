"""Figures 6 and 7 of the Note as one animation: sampling poses from one reading of the pink pole.
Part 1, one pose, step by step, from the noise-free reading of A (range 3.0 m, bearing 36.87 deg): the angle gamma
swings round the pole to 216.87 deg, the robot steps out 3.0 m along it to (2, 2), and the heading turns until the
pole sits 36.87 deg to its left, which leaves theta = 216.87 + 180 - 36.87 = 360 = 0 deg: pose A.
Part 2, the real reading (3.10 m, 40 deg) with noise (0.1 m, 5 deg): pose 1 with its numbers,
then 200 poses fill a ring around the pole. Run -> sample_anim.gif, sample_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif
from lmmodel import LM, POSE_A, READ, SIG_PHI, SIG_R, sample_poses, wrap

here = Path(__file__).parent
PINK = "#E377C2"
MX, MY = LM["pink"]
G_A = np.degrees(np.arctan2(POSE_A[1] - MY, POSE_A[0] - MX)) % 360        # direction from the pole to A
R_A, PHI_A = np.hypot(MX - 2, MY - 2), np.degrees(np.arctan2(MY - 2, MX - 2))
rng = np.random.default_rng(4)                                           # the notebook's seed
XS, YS, TS = sample_poses("pink", 200, rng)
rng = np.random.default_rng(4)                                           # same draws again, to show pose 1's numbers
G1 = np.degrees(rng.uniform(0, 2 * np.pi, 200))[0]
R1 = (READ["pink"][0] + rng.normal(0, SIG_R, 200))[0]
P1 = np.degrees(READ["pink"][1] + rng.normal(0, SIG_PHI, 200))[0]
INSIDE = (XS > 0) & (XS < 5) & (YS > 0) & (YS < 4)
r_back = np.hypot(MX - XS, MY - YS)
phi_back = np.degrees(wrap(np.arctan2(MY - YS, MX - XS) - TS))

assert (round(G_A, 2), round(R_A, 1), round(PHI_A, 2)) == (216.87, 3.0, 36.87)
assert (round(G1, 2), round(R1, 3), round(P1, 2)) == (339.50, 3.008, 37.37)
assert (round(XS[0], 2), round(YS[0], 2), round(np.degrees(TS[0]), 2)) == (7.22, 2.75, 122.13)
assert round(339.50 + 180 - 37.37, 2) == 482.13 and round(482.13 - 360, 2) == 122.13
assert INSIDE.sum() == 64 and (round(r_back.mean(), 2), round(r_back.std(), 2)) == (3.10, 0.10)
assert (round(phi_back.mean(), 1), round(phi_back.std(), 1)) == (39.8, 4.9)


def arc(fig, cx, cy, rad, a0, a1, col, width=3, head=True):
    """Arc from angle a0 to a1 (degrees) around (cx, cy), with an arrowhead at a1."""
    t = np.radians(np.linspace(a0, a1, 60))
    fig.add_trace(go.Scatter(x=cx + rad * np.cos(t), y=cy + rad * np.sin(t), mode="lines",
                             line=dict(color=col, width=width)))
    if head and abs(a1 - a0) > 8:
        s = np.sign(a1 - a0)
        fig.add_annotation(x=cx + rad * np.cos(t[-1]), y=cy + rad * np.sin(t[-1]), ax=cx + rad * np.cos(t[-6]),
                           ay=cy + rad * np.sin(t[-6]), xref="x", yref="y", axref="x", ayref="y", text="",
                           showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=s * 0 + width, arrowcolor=col)


def label(fig, x, y, s, col, anchor="left", size=20):
    fig.add_annotation(x=x, y=y, text=s, showarrow=False, xanchor=anchor, font=dict(size=size, color=col),
                       bgcolor="rgba(255,255,255,0.85)")


def base(title, lines):
    fig = go.Figure()
    fig.add_shape(type="rect", x0=0, x1=5, y0=0, y1=4, line=dict(color=GREY, width=4), fillcolor="rgba(0,0,0,0)",
                  layer="below")
    label(fig, 0.15, 0.3, "room", GREY, size=18)
    for j, (s, col) in enumerate(lines):
        fig.add_annotation(x=0.0, y=0.165 - 0.045 * j, xref="paper", yref="paper", xanchor="left", showarrow=False,
                           text=s, font=dict(size=20, color=col))
    fig.update_xaxes(title="x (m)", range=[-0.4, 8.0], dtick=1)
    fig.update_yaxes(title="y (m)", range=[-0.4, 7.2], dtick=1, scaleanchor="x", domain=[0.3, 1])
    fig.update_layout(template="simple_white", width=900, height=1060, font=FONT, showlegend=False,
                      margin=dict(l=70, r=20, t=80, b=20), title=dict(text=title, x=0.5, font=dict(size=22)))
    return fig


def pole(fig, name=True):
    fig.add_trace(go.Scatter(x=[MX], y=[MY], mode="markers", marker=dict(size=18, color=PINK,
                                                                           line=dict(color="black", width=2))))
    if name:
        label(fig, MX + 0.2, MY - 0.35, "pink pole (4.4, 3.8)", PINK)


def one_pose(title, lines, g=None, d=None, th=None, ring=False, note=False):
    """Part 1. g: angle gamma so far (degrees); d: distance stepped out along it; th: heading of the robot."""
    fig = base(title, lines)
    if ring:
        t = np.linspace(0, 2 * np.pi, 200)
        fig.add_trace(go.Scatter(x=MX + R_A * np.cos(t), y=MY + R_A * np.sin(t), mode="lines",
                                 line=dict(color=PINK, width=2, dash="dash"), opacity=0.5))
    fig.add_trace(go.Scatter(x=[MX, MX + 1.2], y=[MY, MY], mode="lines", line=dict(color=GREY, width=2)))
    if g is not None:
        arc(fig, MX, MY, 0.6, 0, g, BLUE)
        label(fig, MX + 1.2, MY + 0.8, f"γ = {g:.2f}°" if g == G_A else f"γ = {g:.0f}°", BLUE)
        c, s = np.cos(np.radians(g)), np.sin(np.radians(g))
        fig.add_trace(go.Scatter(x=[MX, MX + R_A * c], y=[MY, MY + R_A * s], mode="lines",
                                 line=dict(color=BLUE, width=2, dash="dot")))
        if d:
            fig.add_trace(go.Scatter(x=[MX, MX + d * c], y=[MY, MY + d * s], mode="lines",
                                     line=dict(color=BLUE, width=5), opacity=0.35 if th is not None else 1))
            fig.add_trace(go.Scatter(x=[MX + d * c], y=[MY + d * s], mode="markers",
                                     marker=dict(size=10, color=BLUE)))
            if abs(d - R_A) < 1e-9:
                label(fig, 3.0, 3.15, f"r = {d:.1f} m", BLUE, anchor="right")
    if th is not None:
        x, y = POSE_A[:2]
        fig.add_trace(go.Scatter(x=[x, MX], y=[y, MY], mode="lines", line=dict(color=PINK, width=3, dash="dash")))
        fig.add_shape(type="rect", x0=x - 0.15, x1=x + 0.15, y0=y - 0.15, y1=y + 0.15, line=dict(color=GREY, width=2),
                      fillcolor="#DDDDDD")
        a = np.radians(th)
        fig.add_annotation(x=x + 0.9 * np.cos(a), y=y + 0.9 * np.sin(a), ax=x, ay=y, xref="x", yref="y", axref="x",
                           ayref="y", text="", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=4, arrowcolor=ORANGE)
        label(fig, x + 0.9 * np.cos(a) + 0.1, y + 0.9 * np.sin(a) - 0.25, f"heading θ = {th:.2f}°".replace(".00°", "°"),
              ORANGE)
        if PHI_A - th > 1:
            arc(fig, x, y, 0.7, th, PHI_A, PINK)
            label(fig, 3.05, 2.45, f"φ = {PHI_A - th:.2f}°", PINK)
        label(fig, x - 0.25, y - 0.05, "robot", "black", anchor="right")
    pole(fig)
    return fig


def many(n, title, lines, show_one=False):
    """Part 2: the first n of the 200 poses drawn from the real reading (3.10 m, 40 deg) with noise."""
    fig = base(title, lines)
    L = 0.25
    sx = np.column_stack([XS[:n], XS[:n] + L * np.cos(TS[:n]), np.full(n, np.nan)]).ravel()
    sy = np.column_stack([YS[:n], YS[:n] + L * np.sin(TS[:n]), np.full(n, np.nan)]).ravel()
    fig.add_trace(go.Scatter(x=sx, y=sy, mode="lines", line=dict(color=PINK, width=1.5)))
    fig.add_trace(go.Scatter(x=XS[:n], y=YS[:n], mode="markers", marker=dict(color=PINK, size=5)))
    if show_one:
        fig.add_trace(go.Scatter(x=[MX, XS[0]], y=[MY, YS[0]], mode="lines", line=dict(color=BLUE, width=3)))
        arc(fig, MX, MY, 0.6, 0, G1, BLUE)
        fig.add_trace(go.Scatter(x=[MX, MX + 1.2], y=[MY, MY], mode="lines", line=dict(color=GREY, width=2)))
        fig.add_annotation(x=XS[0] + 0.7 * np.cos(TS[0]), y=YS[0] + 0.7 * np.sin(TS[0]), ax=XS[0], ay=YS[0], xref="x",
                           yref="y", axref="x", ayref="y", text="", showarrow=True, arrowhead=2, arrowwidth=4,
                           arrowcolor=ORANGE)
        label(fig, XS[0] + 0.15, YS[0] - 0.35, "pose 1", "black")
        label(fig, MX + 1.2, MY + 0.8, f"γ = {G1:.2f}°", BLUE)
    fig.add_trace(go.Scatter(x=[POSE_A[0], POSE_A[0] + 0.5], y=[POSE_A[1]] * 2, mode="lines+markers",
                             line=dict(color="black", width=4), marker=dict(size=[12, 1], color="black")))
    pole(fig, name=not show_one)
    return fig


figs, holds, keys = [], [], []


def add(fig, hold, key=False):
    figs.append(fig)
    holds.append(hold)
    if key:
        keys.append(len(figs) - 1)


A_LINES = [("the reading, noise-free as from A: range r = 3.0 m, bearing φ = 36.87°", "black"),
           ("for this check the recipe's step 2 (noise) is left out", GREY)]
add(one_pose("one pose from one reading of the pink pole", A_LINES
             + [("grey line: the direction 0° from the pole, where γ starts", GREY)]), 8)
for g in (45, 90, 135, 180, G_A):
    last = g == G_A
    add(one_pose("step 1: pick an angle γ around the pole", A_LINES[:1] + [
        (f"γ = {G_A:.2f}°: drawn at random; here the angle that leads back to A" if last
         else f"γ = {g:.0f}°, turning from the grey line", BLUE),
        ("the robot will sit somewhere along the dotted ray", GREY)], g=g), 8 if last else 2)
for d in (1.0, 2.0, 3.0):
    last = d == 3.0
    lines = A_LINES[:1] + ([(f"x = 4.4 + 3.0 cos {G_A:.2f}° = 4.4 − 2.4 = 2.0", BLUE),
                            (f"y = 3.8 + 3.0 sin {G_A:.2f}° = 3.8 − 1.8 = 2.0", BLUE),
                            ("dashed ring: every γ lands on this circle of radius 3.0 m", PINK)] if last
                           else [(f"distance from the pole so far: {d:.1f} m", BLUE)])
    add(one_pose("step 3: step out the range, 3.0 m, along γ", lines, g=G_A, d=d, ring=last), 10 if last else 2,
        key=last)
add(one_pose(f"step 4: seen from the robot, the pole lies at γ − 180° = {PHI_A:.2f}°",
             A_LINES[:1] + [(f"{G_A:.2f}° − 180° = {PHI_A:.2f}° (pink dashes: from the robot to the pole)", PINK),
                            ("facing that way, the robot would see the pole straight ahead", "black")],
             g=G_A, d=3.0, th=PHI_A, ring=True), 8)
for th in (PHI_A * 2 / 3, PHI_A / 3):
    add(one_pose("step 4: turn the heading until the pole is 36.87° to the left",
                 A_LINES[:1] + [(f"heading θ = {th:.2f}°; the pole now appears {PHI_A - th:.2f}° to the left", ORANGE),
                                ("φ (pink arc): the angle from the heading to the pole", PINK)],
                 g=G_A, d=3.0, th=th, ring=True), 2)
add(one_pose("step 4: the heading θ = γ + 180° − φ",
             [(f"θ = {G_A:.2f}° + 180° − {PHI_A:.2f}° = 360°", ORANGE),
              ("= 0° after wrapping: the recipe gives back pose A = (2, 2, 0)", ORANGE),
              ("the bearing φ = 36.87° is the direction to the pole minus θ", PINK)],
             g=G_A, d=3.0, th=0.0, ring=True), 16, key=True)
assert round(G_A + 180 - PHI_A, 6) == 360 and round(4.4 + 3.0 * np.cos(np.radians(G_A)), 6) == 2.0

add(many(1, "the real reading, with noise: pose 1 of 200",
         [("reading 3.10 m, 40°; noise of standard deviation 0.1 m and 5°", "black"),
          (f"pose 1: γ = {G1:.2f}°, noisy range {R1:.3f} m, noisy bearing {P1:.2f}°", BLUE),
          (f"(x, y) = ({XS[0]:.2f}, {YS[0]:.2f}); θ = {G1:.2f}° + 180° − {P1:.2f}° = 482.13° = 122.13°", ORANGE),
          ("black: the true pose A = (2, 2, 0)", "black")], show_one=True), 14, key=True)
for n in (5, 20, 50, 100):
    add(many(n, f"the same four steps, again and again: {n} poses",
             [(f"poses drawn: {n}; inside the room: {INSIDE[:n].sum()}", PINK),
              ("black: the true pose A = (2, 2, 0)", "black")]), 3)
add(many(200, "200 poses drawn from the pink reading (3.10 m, 40°)",
         [("a ring of radius about 3.1 m; each arrow turned so the pole appears about 40° to its left", PINK),
          (f"seen from the samples: range {r_back.mean():.2f} m (sd {r_back.std():.2f} m), "
           f"bearing {phi_back.mean():.1f}° (sd {phi_back.std():.1f}°)", "black"),
          (f"{INSIDE.sum()} of the 200 lie inside the room", GREY),
          ("black: the true pose A = (2, 2, 0)", "black")]), 28, key=True)
make_gif(figs, here / "sample_anim", fps=4, holds=holds, keys=keys, cols=2, width=800)
