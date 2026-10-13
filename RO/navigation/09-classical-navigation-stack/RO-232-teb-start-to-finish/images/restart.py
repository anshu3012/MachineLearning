"""Step 3 on numbers. Top, 2.4 s: the two first guesses of the cycle, before any optimising. Orange: last cycle's band,
its passed poses dropped, its first pose moved to the robot and its last to the new local goal (the warm start);
purple: the band built from the global plan, a pose at every plan point. Both run through the person, who was not
there when they were made. Bottom, 4.7 s: the local goal (cross) has turned from -35.5 degrees to 90 degrees, more
than force_reinit_new_goal_angular (90 degrees), so the bands are dropped and a new one is built from the plan.
Orange: the band of 4.6 s; purple: the new band of 4.7 s after optimising. Run -> restart.png"""
import math
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import tebkit as tk
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE
from plotly.subplots import make_subplots

here = Path(__file__).parent
P = tk.results()["person"]
c24, c46, c47 = P[24], P[46], P[47]
w, pb = c24["planner"]["warm"][0], c24["planner"]["plan_band"]
old = c46["planner"]["candidates"][c46["planner"]["best"]]
new = c47["planner"]["candidates"][c47["planner"]["best"]]
assert c47["planner"].get("reinit") and len(w.P) == 12 and len(pb.P) == 32
assert round(math.degrees(c46["goal"][2]), 1) == -35.5 and round(math.degrees(c47["goal"][2])) == 90

fig = make_subplots(rows=2, cols=1, vertical_spacing=0.04)
PLAN = tk.global_plan()


def arrow(g, rc):
    fig.add_annotation(x=g[0] + 0.3 * math.cos(g[2]), y=g[1] + 0.3 * math.sin(g[2]), ax=g[0], ay=g[1], xref=f"x{rc}",
                       yref=f"y{rc}", axref=f"x{rc}", ayref=f"y{rc}", showarrow=True, arrowhead=2, arrowwidth=3,
                       arrowcolor=ORANGE, text="")


for r, (c, a, b, la, lb) in enumerate(((c24, w, pb, "warm start: last band, moved", "band from the plan"),
                                       (c46, old, new, "4.6 s: local goal faces −35.5°",
                                        "4.7 s: goal faces 90°, new band")), start=1):
    rc = (r, 1)
    rd.room(fig, rc)
    fig.add_trace(go.Scatter(x=PLAN[:, 0], y=PLAN[:, 1], mode="lines", line=dict(color=GREY, width=2, dash="dash")),
                  row=r, col=1)
    if c["person"] is not None:
        rd.person(fig, bk.PERSON, bk.PERSON_R, rc, label=False)
    rd.band(fig, a.P, ORANGE, rc, size=8)
    rd.band(fig, b.P, PURPLE, rc, size=6)
    rd.robot(fig, *(c["x"] if r == 1 else c47["x"]), BLUE, rc)
    for g in ((c["goal"],) if r == 1 else (c46["goal"], c47["goal"])):
        fig.add_trace(go.Scatter(x=[g[0]], y=[g[1]], mode="markers", marker=dict(symbol="x", size=18, color=ORANGE)),
                      row=r, col=1)
        arrow(g, "" if r == 1 else "2")
    fig.add_annotation(x=1.4, y=3.85, xref=f"x{'' if r == 1 else 2}", yref=f"y{'' if r == 1 else 2}",
                       text=f"<b>t = {c['t'] if r == 1 else 4.7:.1f} s</b><br><span style='color:{ORANGE}'>{la}</span>"
                            f"<br><span style='color:{PURPLE}'>{lb}</span>", showarrow=False, xanchor="left",
                       yanchor="top", align="left", font=dict(size=19), bgcolor="rgba(255,255,255,0.9)")
    rd.zoom(fig, (1.35, 4.2), (1.5, 3.95), rc)
fig.update_layout(template="simple_white", font=FONT, width=760, height=1300, showlegend=False,
                  margin=dict(l=10, r=10, t=10, b=10))
fig.write_image(here / "restart.png")
