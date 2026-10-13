"""Animation: one motion-plan request for the transfer of the cup, followed through MoveIt's planning pipeline
(MoveIt docs, "Motion Planning" and "The move_group node"). The request (start, goal, planner) goes through the
request adapters, then to a planner from OMPL (such as PRM), which asks MoveIt's planning scene to check every
configuration it tries (the robot, the world and the attached cup); the adapters after it add timing; the result is
a trajectory for the controllers. One box is highlighted per frame. Run -> moveit.gif, moveit_frames.png"""
from pathlib import Path

import plotly.graph_objects as go

from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, make_gif

here = Path(__file__).parent
# (key, label, x0, y0, x1, y1, colour)
BOXES = [("req", "motion plan request", 0.04, 0.80, 0.42, 0.93, BLUE),
         ("pre", "request adapters (before)", 0.04, 0.60, 0.42, 0.73, GREY),
         ("ompl", "planner from OMPL, e.g. PRM", 0.04, 0.40, 0.42, 0.53, ORANGE),
         ("post", "request adapters (after)", 0.04, 0.20, 0.42, 0.33, GREY),
         ("traj", "trajectory to the controllers", 0.04, 0.00, 0.42, 0.13, GREEN),
         ("scene", "planning scene:<br>robot, world, attached cup", 0.50, 0.40, 0.92, 0.53, PURPLE)]
TEXT = {
    "req": ["the request for the transfer:", "start: the grasp configuration", "goal: above the holder at B",
            "which joints: the arm", "which planner: PRM"],
    "pre": ["adapters fix small problems", "before planning, such as a start", "slightly outside a joint limit"],
    "ompl": ["OMPL holds the planners:", "PRM, RRT and others", "", "it has no collision checker;", "for every configuration it",
             "tries, it asks MoveIt"],
    "scene": ["the planning scene answers:", "robot's links (self-collision),", "the table, the bottle, the holder,",
              "and the cup, attached to the", "hand after the grasp: transfer", "", "free or not, every time"],
    "post": ["the planner returns a path:", "configurations, no timing", "", "an adapter adds the timing,",
             "keeping each joint within its", "speed and acceleration limits"],
    "traj": ["a trajectory: the path with", "a time for every configuration,", "sent to the arm's controllers"],
}
ORDER = ["req", "pre", "ompl", "scene", "ompl", "post", "traj"]


def frame(active, step):
    fig = go.Figure()
    for key, label, x0, y0, x1, y1, col in BOXES:
        on = key == active
        fig.add_shape(type="rect", xref="x", yref="y", x0=x0, y0=y0, x1=x1, y1=y1,
                      line=dict(color=col, width=5 if on else 2), fillcolor=col if on else "white", opacity=1,
                      layer="below")
        fig.add_annotation(xref="x", yref="y", x=(x0 + x1) / 2, y=(y0 + y1) / 2, text=label, showarrow=False,
                           font=dict(size=19, color="white" if on else "black"))
    for y0, y1 in ((0.80, 0.73), (0.60, 0.53), (0.40, 0.33), (0.20, 0.13)):
        fig.add_annotation(xref="x", yref="y", x=0.23, y=y1, ax=0.23, ay=y0, axref="x", ayref="y",
                           showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=2.5, arrowcolor=GREY, text="")
    fig.add_annotation(xref="x", yref="y", x=0.50, y=0.49, ax=0.42, ay=0.49, axref="x", ayref="y",
                       showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=2.5, arrowcolor=GREY, text="")
    fig.add_annotation(xref="x", yref="y", x=0.42, y=0.44, ax=0.50, ay=0.44, axref="x", ayref="y",
                       showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=2.5, arrowcolor=GREY, text="")
    fig.add_annotation(xref="x", yref="y", x=0.46, y=0.555, text="free?", showarrow=False, font=dict(size=16))
    for k, s in enumerate(TEXT[active] if active else []):
        fig.add_annotation(xref="x", yref="y", x=0.50, y=0.98 - 0.055 * k, xanchor="left", yanchor="top",
                           text=s, showarrow=False, font=dict(size=19))
    fig.update_xaxes(visible=False, range=[0, 1])
    fig.update_yaxes(visible=False, range=[0, 1])
    title = f"step {step} of 7: " + {"req": "the request", "pre": "adapters before planning",
                                     "ompl": "the planner", "scene": "collision checks in the planning scene",
                                     "post": "adapters after planning", "traj": "the trajectory"}[active]
    fig.update_layout(template="simple_white", width=1300, height=720, font=FONT, showlegend=False,
                      title=dict(text=title, x=0.5, font=dict(size=22)), margin=dict(l=20, r=20, t=70, b=20))
    return fig


figs = [frame(a, i + 1) for i, a in enumerate(ORDER)]
holds = [8] * len(figs)
holds[-1] = 16
make_gif(figs, here / "moveit", fps=2, holds=holds, keys=[0, 2, 3, 5], cols=2, width=1000)
