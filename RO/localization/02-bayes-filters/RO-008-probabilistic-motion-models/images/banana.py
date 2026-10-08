"""500 samples of the odometry motion model from (2, 1, 30 deg) with u = (0.500, 0.479, 0.500) under three noise
settings: the Note's (alpha = 0.1, 0.1, 0.1, 0.01), mostly turning noise, mostly driving noise. Seeded.
Run: python banana.py -> banana.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, RED
from motion import START, sample_odometry
from plotly.subplots import make_subplots

here = Path(__file__).parent
u = (0.500, 0.479, 0.500)
cases = [("the Note's noise", (0.1, 0.1, 0.1, 0.01)), ("mostly turning noise", (0.4, 0.1, 0.02, 0.0)),
         ("mostly driving noise", (0.02, 0.0, 0.4, 0.0))]
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.05, subplot_titles=[c[0] for c in cases])
t = np.linspace(START[2], START[2] + 1, 50)
for c, (_, a) in enumerate(cases, start=1):
    xs, ys, _ = sample_odometry(u, START, np.random.default_rng(5), 500, a)
    fig.add_trace(go.Scatter(x=1.75 + 0.5 * np.sin(t), y=1.433 - 0.5 * np.cos(t), mode="lines",
                             line=dict(color=GREY, dash="dash", width=2)), 1, c)
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="markers", marker=dict(size=4, color=BLUE, opacity=0.6)), 1, c)
    fig.add_trace(go.Scatter(x=[2.0], y=[1.0], mode="markers", marker=dict(size=12, color="black")), 1, c)
    fig.add_trace(go.Scatter(x=[2.249], y=[1.409], mode="markers", marker=dict(size=12, color=RED, symbol="x")), 1, c)
    fig.update_xaxes(range=[1.7, 2.6], dtick=0.2, title="x (m)", row=1, col=c)
    fig.update_yaxes(range=[0.9, 1.85], dtick=0.2, scaleanchor=f"x{c if c > 1 else ''}", row=1, col=c)
fig.update_yaxes(title="y (m)", row=1, col=1)
fig.update_layout(template="simple_white", width=1200, height=520, font=FONT, showlegend=False,
                  margin=dict(l=80, r=30, t=110, b=70),
                  title=dict(text="500 sampled end positions for the same odometry reading", x=0.5, y=0.95,
                             font=dict(size=22)))
fig.update_annotations(font_size=20)
fig.write_image(here / "banana.png")
