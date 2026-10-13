"""Animation: the sense-plan-act loop of the opening, looking once a second, step by step from 1.9 s to 3.22 s.
Top: the three steps, the one running lit. Bottom: a time line with the loop's looks (2.0 and 3.0 s), the moment the
person steps in (2.4 s) and the moment the robot touches them (3.22 s). At 2.0 s the loop senses and plans with no
person there, then acts on that plan for a whole second; the person steps in at 2.4 s, 0.465 m ahead, while the loop
is not looking; at 3.0 s it senses them 0.113 m ahead and plans to brake at 0.5 m/s^2, too late: it touches them at
3.22 s. Run -> spa_anim.gif, spa_anim_frames.png"""
from pathlib import Path

import netdraw as nd
import stackkit as sk
from gifkit import BLUE, GREEN, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
S = sk.spa(1.0)
gap = lambda t: float(S["gap"][int(round(t / sk.DT))])
assert round(gap(2.4), 3) == 0.465 and round(gap(3.0), 3) == 0.113 and gap(3.22) < 0 < gap(3.2)
BOX = {"sense": (0.17, 0.72), "plan": (0.50, 0.72), "act": (0.83, 0.72)}
COL = {"sense": GREEN, "plan": ORANGE, "act": BLUE}
SUB = {"sense": "read every sensor", "plan": "map, pose, whole route", "act": "drive the plan"}
T0, T1, X0, X1 = 1.85, 3.35, 0.06, 0.96
X = lambda t: X0 + (t - T0) / (T1 - T0) * (X1 - X0)
YL = 0.30


def frame(t, step, note):
    fig = nd.blank()
    for name, p in BOX.items():
        nd.box(fig, *p, name, COL[name], lit=name == step, w=0.24, h=0.14, size=24, sub=SUB[name])
    nd.arrow(fig, (0.29, 0.72), (0.38, 0.72), GREY, width=3)
    nd.arrow(fig, (0.62, 0.72), (0.71, 0.72), GREY, width=3)
    fig.add_shape(type="path", opacity=1, xref="paper", yref="paper",
                  path="M 0.83 0.65 L 0.83 0.57 L 0.17 0.57", line=dict(color=GREY, width=3), fillcolor="rgba(0,0,0,0)")
    nd.arrow(fig, (0.17, 0.57), (0.17, 0.648), GREY, width=3)
    nd.text(fig, 0.5, 0.555, "next pass: one second later", size=18, color=GREY, anchor="center", valign="top")
    fig.add_shape(type="line", opacity=1, xref="paper", yref="paper", x0=X0, x1=X1, y0=YL, y1=YL,
                  line=dict(color="#BBBBBB", width=3))
    for tt in (2.0, 2.5, 3.0):
        nd.text(fig, X(tt), YL - 0.045, f"{tt:.1f} s", size=17, color=GREY, anchor="center", valign="top")
    for tt in (2.0, 3.0):
        if t >= tt - 1e-9:
            nd.dot(fig, (X(tt), YL), GREEN)
            nd.text(fig, X(tt), YL + 0.035, "look", size=17, color=GREEN, anchor="center", valign="bottom")
    if t >= 2.4 - 1e-9:
        nd.dot(fig, (X(2.4), YL), "#C2185B")
        nd.text(fig, X(2.4), YL + 0.035, "person<br>steps in", size=17, color="#C2185B", anchor="center",
                valign="bottom")
    if t >= 3.22 - 1e-9:
        nd.dot(fig, (X(3.22), YL), RED)
        nd.text(fig, X(3.22) + 0.012, YL + 0.035, "touches", size=17, color=RED, anchor="left", valign="bottom")
    fig.add_shape(type="line", opacity=1, xref="paper", yref="paper", x0=X(t), x1=X(t), y0=YL - 0.03,
                  y1=YL + 0.03, line=dict(color="black", width=4))
    stamp = f"{t:.2f}" if abs(t * 10 - round(t * 10)) > 1e-6 else f"{t:.1f}"
    nd.text(fig, 0.02, 0.98, f"<b>t = {stamp} s</b>: {note}", size=22)
    if t >= 2.4 - 1e-9:
        g = gap(t)
        nd.text(fig, 0.02, 0.12, f"gap to the person: {max(g, 0):.3f} m" + ("" if g >= 0 else ", touching"), size=20,
                color=RED if g < 0 else "black")
    return fig


FR = [(1.9, "act", "acting on the plan made at 1.0 s"),
      (2.0, "sense", "the loop looks: nobody on the route"),
      (2.0, "plan", "plan from that look: drive on"),
      (2.2, "act", "acting; the loop is not looking"),
      (2.4, "act", "the person steps in; the loop is not looking"),
      (2.6, "act", "acting on the old plan"),
      (2.8, "act", "acting on the old plan"),
      (3.0, "sense", "the loop looks: the person, 0.113 m ahead"),
      (3.0, "plan", "plan: brake at 0.5 m/s²"),
      (3.1, "act", "braking"),
      (3.22, "act", "too late: the robot touches the person")]
figs = [frame(*f) for f in FR]
holds = [4, 4, 4, 3, 6, 3, 3, 5, 4, 3, 12]
make_gif(figs, here / "spa_anim", fps=2, holds=holds, keys=[1, 4, 7, len(figs) - 1], cols=2, width=900)
