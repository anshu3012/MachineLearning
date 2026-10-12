"""The opening problem: the car starts 1.0 m left of the course, heading 0 deg, at 2 m/s. RO-069's line rule given
one line, the first straight (y = 0), joins it and drives straight on past the corner at x = 10 m: after 11.0 s it is
at (21.94, 0.00), 5.57 m from the course. The last frame adds the same rule applied to the course's tangent at the
nearest course point, which follows the course to its end in 18.15 s, 0.388 m outside the arc at most.
Run -> opening.gif, opening_frames.png"""
from pathlib import Path

import numpy as np
from coursedraw import axes, car, course, label, minus, trail
from gifkit import BLUE, FONT, RED, make_gif
from plotly.subplots import make_subplots
from trackkit import START, first_line_rule, line_rule, nearest_s, course_point, run

here = Path(__file__).parent
deg = np.degrees
T_RED = 11.0
A = run(lambda q, t: first_line_rule(q), stop=lambda q: False, t_max=T_RED)
B = run(lambda q, t: line_rule(q))
K_RED = int(round(T_RED / 0.01))
xa, ya = A["x"][K_RED], A["y"][K_RED]
pa = course_point(nearest_s(xa, ya))
D_RED = np.hypot(xa - pa[0], ya - pa[1])
assert round(xa, 2) == 21.94 and abs(ya) < 0.005 and round(D_RED, 2) == 5.57
assert round(B["t"][-1], 2) == 18.15 and round(B["e"].min(), 3) == -0.388


def frame(t, last=False):
    fig = make_subplots(rows=1, cols=1)
    course(fig, (1, 1))
    label(fig, -1.5, 21.5, "course: 10 m straight, 90° left arc<br>of radius 10 m, 10 m straight", "#757575", (1, 1), size=16, anchor="left")
    k = min(int(round(t / 0.01)), K_RED)
    trail(fig, A["x"][:k + 1], A["y"][:k + 1], RED, (1, 1))
    car(fig, (A["x"][k], A["y"][k], A["th"][k]), A["delta"][k], RED, (1, 1), fill="rgba(228,87,86,0.25)")
    if last:
        trail(fig, B["x"], B["y"], BLUE, (1, 1))
        car(fig, (B["x"][-1], B["y"][-1], B["th"][-1]), B["delta"][-1], BLUE, (1, 1))
        label(fig, 10.5, 15.0, "tangent at the nearest<br>course point: follows<br>the course", BLUE, (1, 1), size=17)
        title = ("the line has to move with the car<br><span style='font-size:19px'>"
                 "the tangent at the nearest course point keeps the car on the course</span>")
    else:
        if t >= 5.0:
            label(fig, 17.5, -2.0, "one line, y = 0: straight on past the corner", RED, (1, 1), size=17)
        title = (f"one line (the first straight): t = {A['t'][k]:.1f} s<br><span style='font-size:19px'>"
                 f"rear axle at ({A['x'][k]:.1f}, {A['y'][k]:.2f}), heading {deg(A['th'][k]):.1f}°</span>")
        if k == K_RED:
            title = (f"one line: at {T_RED:.1f} s the car is {D_RED:.2f} m from the course<br>"
                     "<span style='font-size:19px'>and still heading 0°: the course turned, the line did not</span>")
    axes(fig, (1, 1))
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=980, showlegend=False,
                      margin=dict(l=90, r=30, t=120, b=60), title=dict(x=0.5, y=0.97, yanchor="top", text=minus(title)))
    return fig


ts = list(np.arange(0, T_RED, 0.5)) + [T_RED]
figs = [frame(t) for t in ts] + [frame(T_RED, last=True)]
holds = [4] + [1] * (len(ts) - 2) + [8, 14]
make_gif(figs, here / "opening", fps=4, holds=holds, keys=[0, 10, len(ts) - 1, len(figs) - 1], cols=2, width=800)
