"""Still: the numbers inside one skill, "pick up the bottle" in the final plan. The bottle stands at x = 0.42 m; the one
grasp puts the hand on the centre of its cap, (0.42, 0.04) m; the joint angles that put the hand there without
hitting anything are q = (31.2, -66.4) degrees; the motion from home to q is 88.7 degrees of joint motion (the dotted
track of the hand). Plotly, because it is drawn from the same model as the animations.
Run -> params.png"""
from pathlib import Path

import plotly.graph_objects as go

import tabledraw as td
import tampkit as t
from gifkit import GREEN, GREY

here = Path(__file__).parent
w = t.World({"cup": t.A_X, "bottle": t.B_X})
g = t.grasp_conf(w, "bottle", t.B_X)
path, L = t.motion(w, t.HOME, g)
assert [round(v, 1) for v in g] == [31.2, -66.4] and round(L, 1) == 88.7
cap = t.top("bottle", t.B_X)
assert [round(v, 2) for v in cap] == [0.42, 0.04]

fig = go.Figure()
td.scene(fig, w)
td.arm(fig, t.HOME, opacity=0.25)
td.hand_trace(fig, path)
td.arm(fig, g)
notes = [
    (0.42, -0.06, 0.53, -0.04, "x = 0.42 m: where the bottle stands"),
    (0.42, 0.04, 0.53, 0.10, "grasp: the cap's centre, (0.42, 0.04) m"),
    (0.26, 0.15, 0.47, 0.26, "q = (31.2, -66.4) degrees: the joint angles"),
    (0.20, 0.47, 0.30, 0.46, "motion: 88.7 degrees of joint motion from home"),
]
for x, y, ax, ay, s in notes:
    fig.add_annotation(x=x, y=y, ax=ax, ay=ay, axref="x", ayref="y", text=s, showarrow=True, arrowhead=2,
                       arrowwidth=1.5, arrowcolor=GREY, xanchor="left", font=dict(size=18, color="black"))
fig.add_annotation(x=0.0, y=0.53, text="home", showarrow=False, font=dict(size=16, color=GREY))
td.axes(fig, xr=(-0.2, 1.0), yr=(-0.17, 0.56))
fig.update_yaxes(scaleanchor="x")
td.layout(fig, 1300, 640, "the skill 'pick up the bottle' and its numbers")
fig.write_image(here / "params.png", scale=1)
