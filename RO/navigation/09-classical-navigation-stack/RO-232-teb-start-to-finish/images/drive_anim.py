"""Animation for the Overview: the whole drive with our Python version of teb_local_planner's algorithm (tebkit.py),
one frame per 0.2 s. Grey dashed: the global plan (RO-034's A* route, its ends moved to the robot and the door
pose). Orange: the band TEB picks, its poses with
headings; pale purple: the other candidate bands; orange cross: the local goal. At 2.4 s the person (pink) steps in.
The last frame holds at the arrival (RO-058's test: within 0.02 m and 0.05 rad of the door pose, stopped).
Run -> drive_anim.gif, drive_anim_frames.png"""
from pathlib import Path

import bandkit as bk
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
import tebkit as tk
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, make_gif

here = Path(__file__).parent
run = tk.results()["person"]
xs = np.array([o["x"] for o in run])
T_end = tk.arrival(run)
gp = np.hypot(*(xs[:, :2] - bk.PERSON).T) - bk.PERSON_R - bk.R_BODY
assert round(T_end, 1) == 9.8 and round(tk.arrival(tk.results()["clear"]), 1) == 7.9
assert round(float(gp[24:].min()), 3) == 0.137
PLAN = tk.global_plan()


def frame(k):
    o = run[k]
    fig = go.Figure()
    rd.room(fig)
    fig.add_trace(go.Scatter(x=PLAN[:, 0], y=PLAN[:, 1], mode="lines", line=dict(color=GREY, width=2.5, dash="dash")))
    if o["person"] is not None:
        rd.person(fig, bk.PERSON, bk.PERSON_R)
    fig.add_trace(go.Scatter(x=xs[:k + 1, 0], y=xs[:k + 1, 1], mode="lines", line=dict(color=BLUE, width=5)))
    n_c = 0
    if "planner" in o:
        pl = o["planner"]
        n_c = len(pl["candidates"])
        for i, b in enumerate(pl["candidates"]):
            if i != pl["best"]:
                rd.band(fig, b.P, PURPLE, size=5, width=1.5, ticks=False)
        rd.band(fig, pl["candidates"][pl["best"]].P, ORANGE, size=8)
        g = o["goal"]
        fig.add_trace(go.Scatter(x=[g[0]], y=[g[1]], mode="markers", marker=dict(symbol="x", size=16, color=ORANGE)))
    rd.robot(fig, *tuple(bk.GOAL[:3]), "#BBBBBB", width=2, fill="rgba(0,0,0,0)")
    rd.robot(fig, o["x"][0], o["x"][1], o["x"][2], BLUE)
    done = o.get("arrived", False)
    lines = [f"<b>t = {o['t']:.1f} s</b>" + (", arrived" if done else ""), f"speed {abs(o['v']) if abs(o['v']) < 0.005 else o['v']:.2f} m/s",
             "<span style='color:#888888'>our Python version of TEB</span>"]
    if not done:
        lines.append(f"<span style='color:{ORANGE}'>picked band</span>" +
                     (f", <span style='color:{PURPLE}'>{n_c - 1} other</span>" if n_c > 1 else ""))
    if o["person"] is not None:
        lines.append("<span style='color:#C2185B'>person seen at 2.4 s</span>")
    fig.add_annotation(x=1.35, y=3.85, text="<br>".join(lines), showarrow=False, xanchor="left", yanchor="top",
                       align="left", font=dict(size=20), bgcolor="rgba(255,255,255,0.9)")
    fig.add_annotation(x=2.0, y=0.62, text="start", showarrow=False, font=dict(size=18, color="#555555"))
    rd.axes(fig)
    fig.update_layout(template="simple_white", font=FONT, width=760, height=1000, showlegend=False,
                      margin=dict(l=10, r=10, t=10, b=10))
    return fig


ks = list(range(0, len(run), 2))
if ks[-1] != len(run) - 1:
    ks.append(len(run) - 1)
k_person = ks.index(24)
figs = [frame(k) for k in ks]
holds = [4] + [1] * (len(figs) - 2) + [14]
holds[k_person] = 6
make_gif(figs, here / "drive_anim", fps=5, holds=holds, keys=[0, k_person, k_person + 4, ks.index(40),
                                                               ks.index(78), len(figs) - 1], cols=3, width=560)
print("arrival", T_end, "closest to the person", round(float(gp[24:].min()), 3))
