"""The Gang of Four of the PD heading loop (kp = 0.4, kd = 0.08, plant 1/(0.1 s^2)): the gains of S (output
disturbance to heading), T (noise to heading), PS (drag torque to heading) and CS (noise to motor torque) against
frequency. PS starts at 1/kp = 2.5 rad per N m, so a 0.02 N m drag leaves 0.05 rad; CS keeps rising with frequency,
8.0 N m per rad at 100 rad/s. Run: python gang_of_four.py -> gang_of_four.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE, PURPLE, RED
from loopkit import C_pd
from shapekit import gang_of_four

here = Path(__file__).parent
w = np.logspace(-1, np.log10(300), 2000)
g = gang_of_four(C_pd, w)
g0 = gang_of_four(C_pd, np.array([1e-4, 100.0]))
assert abs(abs(g0["PS"][0]) - 2.5) < 1e-3 and abs(abs(g0["CS"][1]) - 8.01) < 1e-2

panels = [("S", "S: output disturbance d → heading", BLUE, "", 0.0),
          ("T", "T: sensor noise n → heading", PURPLE, "", 0.0),
          ("PS", "PS: drag torque v → heading", ORANGE, "rad per N·m", 0.0),
          ("CS", "CS: sensor noise n → motor torque", RED, "N·m per rad", 0.0)]
fig = make_subplots(rows=2, cols=2, subplot_titles=[p[1] for p in panels], vertical_spacing=0.2,
                    horizontal_spacing=0.13)
for i, (key, _, col, unit, _) in enumerate(panels):
    r, c = i // 2 + 1, i % 2 + 1
    fig.add_trace(go.Scatter(x=w, y=np.abs(g[key]), line=dict(color=col, width=4), showlegend=False), r, c)
    fig.add_trace(go.Scatter(x=[0.1, 300], y=[1, 1], mode="lines", line=dict(color=GREY, width=1.5, dash="dash"),
                             showlegend=False), r, c)
    fig.update_xaxes(type="log", range=[-1, np.log10(300)], title_text="ω (rad/s)", row=r, col=c)
    fig.update_yaxes(type="log", title_text=("gain " + (f"({unit})" if unit else "")).strip(), row=r, col=c)
fig.update_yaxes(range=[-3, 1], row=1, col=1)
fig.update_yaxes(range=[-3, 1], row=1, col=2)
fig.update_yaxes(range=[-3, 1], row=2, col=1)
fig.update_yaxes(range=[-3, 1.5], row=2, col=2)
fig.add_annotation(x=-0.9, y=np.log10(2.5), text="2.5 = 1/Kp", ax=60, ay=40, font=dict(size=18, color=ORANGE),
                   arrowcolor=ORANGE, xanchor="left", row=2, col=1)
fig.add_annotation(x=2, y=np.log10(8.0), text="8.0 at 100 rad/s", ax=-90, ay=-35, font=dict(size=18, color=RED),
                   arrowcolor=RED, row=2, col=2)
fig.add_annotation(x=np.log10(2.085), y=np.log10(2.55), text="Ms = 2.55", ax=60, ay=-30, font=dict(size=18, color=BLUE),
                   arrowcolor=BLUE, row=1, col=1)
fig.add_annotation(x=np.log10(1.93), y=np.log10(2.73), text="Mt = 2.73", ax=60, ay=-30, font=dict(size=18, color=PURPLE),
                   arrowcolor=PURPLE, row=1, col=2)
for a in fig.layout.annotations[:4]:
    a.font = dict(size=19)
fig.update_layout(template="simple_white", font=FONT, width=1050, height=900, margin=dict(l=90, r=30, t=120, b=70),
                  title=dict(x=0.5, y=0.97, text="the Gang of Four of the PD heading loop (dashed: gain 1)"))
fig.write_image(here / "gang_of_four.png", scale=1)
