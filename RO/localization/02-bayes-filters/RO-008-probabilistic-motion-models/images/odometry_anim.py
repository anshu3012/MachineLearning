"""Odometry from (2, 1, 30 deg) to (2.249, 1.409, 87.3 deg) as turn, drive, turn, played. First a faint robot drives
the arc the robot really drove (v = 0.5 m/s, omega = 1 rad/s for 1 s); odometry keeps only its start and end pose.
Then the robot redoes the move as the odometry model describes it: turn on the spot by rot1 = 0.500 rad to face the
end point, drive trans = 0.479 m straight to it, turn by rot2 = 0.500 rad to the end heading. It lands on the same
pose.
Run: python odometry_anim.py -> odometry_anim.gif, odometry_anim_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, make_gif
from motion import ODO_END, START, arc_end, odo_deltas
from robotdraw import robot

here = Path(__file__).parent
X0, Y0, TH0 = START
X1, Y1, TH1 = ODO_END
ROT1, TRANS, ROT2 = odo_deltas(START, ODO_END)
CHORD = TH0 + ROT1                                        # direction of the straight line, atan2(0.409, 0.249)
assert [round(v, 3) for v in (ROT1, TRANS, ROT2)] == [0.500, 0.479, 0.500]
assert round(CHORD, 3) == 1.024 and round(np.degrees(TH1), 1) == 87.3 and round(np.degrees(TH0)) == 30
assert np.allclose(arc_end(X0, Y0, TH0, 0.5, 1.0, 1.0), ODO_END, atol=5e-4)   # the arc ends on odometry's end pose
SC = 0.3                                                  # robot drawn at 0.3 of RO-001's size
GHOST = dict(scale=SC, color=GREY, opacity=0.35, arrow=False, fill="rgba(107,107,107,0.15)")


def arc_xy(f):
    """Points of the true arc driven so far (fraction f of the 1 s drive), and the pose reached."""
    x, y, th = arc_end(X0, Y0, TH0, 0.5, 1.0, np.linspace(0, f, 40))
    return x, y, (x[-1], y[-1], th[-1])


def wedge(fig, cx, cy, a0, a1, r):
    t = np.linspace(a0, a1, 30)
    fig.add_trace(go.Scatter(x=cx + r * np.cos(t), y=cy + r * np.sin(t), mode="lines+markers",
                             line=dict(color=PURPLE, width=3),
                             marker=dict(symbol="arrow", size=[0] * 29 + [13], angleref="previous", color=PURPLE)))


def label(fig, x, y, s, col, anchor="center", size=21):
    fig.add_annotation(x=x, y=y, text=s, showarrow=False, xanchor=anchor, font=dict(color=col, size=size))


def arrow(fig, x, y, th, n, col=ORANGE):
    fig.add_trace(go.Scatter(x=[x, x + n * np.cos(th)], y=[y, y + n * np.sin(th)], mode="lines+markers",
                             line=dict(color=col, width=4), marker=dict(symbol="arrow", size=[0, 15],
                                                                         angleref="previous", color=col)))


def frame(title, sub, ghost_f, r1=0.0, d=0.0, r2=0.0):
    """ghost_f: fraction of the arc the faint robot has driven (None: not shown). r1, d, r2: how far the robot has
    got through the first turn (rad), the drive (m) and the second turn (rad)."""
    fig = go.Figure()
    if ghost_f is not None:                                # the arc the robot really drove
        ax, ay, gq = arc_xy(ghost_f)
        fig.add_trace(go.Scatter(x=ax, y=ay, mode="lines", line=dict(color=GREY, dash="dash", width=3)))
        if ghost_f == 1:
            label(fig, 2.245, 1.17, "path driven (arc)", GREY, "left", 19)
    started = r1 > 0
    if started:                                            # the start heading stays behind as a fixed arrow
        arrow(fig, X0, Y0, TH0, 0.14)
        label(fig, 2.13, 1.045, "start heading 30°", ORANGE, "left", 19)
        wedge(fig, X0, Y0, TH0, TH0 + r1, 0.08)
        label(fig, 2.028, 1.088, f"δ<sub>rot1</sub> = {r1:.3f} rad", PURPLE, "right")
    if d > 0:
        px, py = X0 + d * np.cos(CHORD), Y0 + d * np.sin(CHORD)
        fig.add_trace(go.Scatter(x=[X0, px], y=[Y0, py], mode="lines", line=dict(color=BLUE, width=6)))
        label(fig, 2.075, 1.25, f"δ<sub>trans</sub> = {d:.3f} m", BLUE, "right")
    if r2 > 0:
        fig.add_trace(go.Scatter(x=[X1, X1 + 0.09 * np.cos(CHORD)], y=[Y1, Y1 + 0.09 * np.sin(CHORD)], mode="lines",
                                 line=dict(color="rgba(76,120,168,0.4)", dash="dash", width=2)))
        wedge(fig, X1, Y1, CHORD, CHORD + r2, 0.06)
        label(fig, 2.305, 1.455, f"δ<sub>rot2</sub> = {r2:.3f} rad", PURPLE, "left")
    if ghost_f is not None:
        for tr in robot(gq, **GHOST):
            fig.add_trace(tr)
    fig.add_trace(go.Scatter(x=[X0, X1], y=[Y0, Y1], mode="markers", marker=dict(size=13, color="black")))
    label(fig, 1.935, 0.95, "(2, 1)", "black", "right")
    label(fig, 2.18, 1.409, "(2.249, 1.409)", "black", "right")
    if r2 > 0 and abs(r2 - ROT2) < 1e-9:                   # the end heading
        arrow(fig, X1, Y1, TH1, 0.12)
        label(fig, X1 + 0.006, 1.565, "end heading 87.3°", ORANGE, "center", 19)
    q = (X0, Y0, TH0 + r1) if d == 0 else (X0 + d * np.cos(CHORD), Y0 + d * np.sin(CHORD), CHORD + r2)
    for tr in robot(q, scale=SC):
        fig.add_trace(tr)
    fig.update_xaxes(range=[1.86, 2.52], dtick=0.1, showgrid=True, gridcolor="#e4e4e4", title="x (m)")
    fig.update_yaxes(range=[0.91, 1.6], dtick=0.1, showgrid=True, gridcolor="#e4e4e4", title="y (m)",
                     scaleanchor="x")
    fig.update_layout(template="simple_white", width=900, height=1000, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=150, b=70),
                      title=dict(x=0.5, y=0.97, font=dict(size=23), text=f"{title}<br><span style='font-size:20px;"
                                 f"color:{GREY}'>{sub}</span>"))
    return fig


figs, holds = [], []
add = lambda f, h: (figs.append(f), holds.append(h))
add(frame("odometry reports two poses: start and end", "start (2, 1), heading 30°;  end (2.249, 1.409), heading 87.3°",
          None), 8)
for f in (0.25, 0.5, 0.75, 1.0):
    add(frame("the robot really drove an arc (faint robot)", "odometry keeps only where it started and ended", f),
        2 if f < 1 else 6)
SUB1, SUB2, SUB3 = ("1. turn on the spot to face the end point", "2. drive straight to it",
                    "3. turn on the spot to the end heading")
for k in (1, 2, 3, 4):
    add(frame("the odometry model: turn, drive, turn", SUB1, 1.0, r1=ROT1 * k / 4), 2 if k < 4 else 5)
for k in (1, 2, 3, 4):
    add(frame("the odometry model: turn, drive, turn", SUB2, 1.0, r1=ROT1, d=TRANS * k / 4), 2 if k < 4 else 5)
for k in (1, 2, 3, 4):
    add(frame("the odometry model: turn, drive, turn", SUB3, 1.0, r1=ROT1, d=TRANS, r2=ROT2 * k / 4),
        2 if k < 4 else 3)
add(frame("turn, drive, turn: the same end pose as the arc", "three numbers: 0.500 rad, 0.479 m, 0.500 rad", 1.0,
          r1=ROT1, d=TRANS, r2=ROT2), 20)
make_gif(figs, here / "odometry_anim", fps=4, holds=holds, keys=[4, 8, 11, len(figs) - 1], cols=2, width=850)
