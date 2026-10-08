"""Control sets in the (v, omega) plane (MR 13.3.1; LaValle 13.1.2.1). Differential drive with wheel top speed 0.6 m/s
and L = 0.2 m: diamond with corners (+-0.6, 0) and (0, +-6). Simple car with rho_min = 5 m, top speed 1 m/s:
bowtie |omega| <= |v| / 5. Reeds-Shepp: v in {-1, 0, 1}. Dubins: v in {0, 1}.
Run: python control_sets.py -> control_sets.png, control_sets.pdf"""
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, ORANGE, PURPLE

here = Path(__file__).parent
fig = make_subplots(rows=1, cols=4, horizontal_spacing=0.07,
                    subplot_titles=["<b>differential drive</b><br>diamond", "<b>simple car</b><br>bowtie",
                                    "<b>Reeds-Shepp car</b><br>forward or reverse", "<b>Dubins car</b><br>forward only"])
fill = lambda c: c.replace("#", "rgba(") if False else c
fig.add_trace(go.Scatter(x=[0.6, 0, -0.6, 0, 0.6], y=[0, 6, 0, -6, 0], fill="toself", mode="lines",
                         line=dict(color=BLUE, width=3), fillcolor="rgba(76,120,168,0.25)"), row=1, col=1)
fig.add_trace(go.Scatter(x=[0, 1, 1, 0, -1, -1, 0], y=[0, 0.2, -0.2, 0, 0.2, -0.2, 0], fill="toself", mode="lines",
                         line=dict(color=ORANGE, width=3), fillcolor="rgba(245,133,24,0.25)"), row=1, col=2)
for vv in (1, -1):
    fig.add_trace(go.Scatter(x=[vv, vv], y=[-0.2, 0.2], mode="lines", line=dict(color=PURPLE, width=7)), row=1, col=3)
fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=12, color=PURPLE)), row=1, col=3)
fig.add_trace(go.Scatter(x=[1, 1], y=[-0.2, 0.2], mode="lines", line=dict(color=GREEN, width=7)), row=1, col=4)
fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=12, color=GREEN)), row=1, col=4)
fig.update_xaxes(title="v (m/s)", zeroline=True, zerolinecolor="#999", showgrid=True, gridcolor="#eee")
fig.update_yaxes(zeroline=True, zerolinecolor="#999", showgrid=True, gridcolor="#eee")
fig.update_xaxes(range=[-0.8, 0.8], dtick=0.3, row=1, col=1)
fig.update_yaxes(range=[-7, 7], dtick=2, title="ω (rad/s)", row=1, col=1)
for c in (2, 3, 4):
    fig.update_xaxes(range=[-1.3, 1.3], dtick=1, row=1, col=c)
    fig.update_yaxes(range=[-0.3, 0.3], dtick=0.1, row=1, col=c)
fig.add_annotation(x=0.5, y=-0.45, xref="paper", yref="paper", showarrow=False, font=dict(size=19),
                   text="note the different ω scale: the robot can turn up to 6 rad/s, the cars only up to 0.2 rad/s "
                        "(ρ<sub>min</sub> = 5 m)")
fig.update_layout(template="simple_white", width=1400, height=540, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=100, b=160))
fig.update_annotations(selector=dict(yref="paper", y=1.0), font_size=21)
fig.write_image(here / "control_sets.png", scale=1)
fig.write_image(here / "control_sets.pdf")
