"""Transcription: the controls of the 8 s least-effort drive as a list of numbers. The 8 s are cut into 30
intervals of 0.267 s, and in each the acceleration a (top) and the turn rate omega (bottom) are held constant: 60
numbers in all, found by single shooting. Run -> transcription.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import trajkit as tk
from gifkit import BLUE, FONT, ORANGE
from plotly.subplots import make_subplots

here = Path(__file__).parent
U = tk.solutions()["single"]["U"]
N, T = len(U), 8.0
assert N == 30
t = np.linspace(0, T, N + 1)
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                    subplot_titles=["acceleration a (m/s²): 30 numbers", "turn rate ω (rad/s): 30 numbers"])
for r, (k, col) in enumerate(((0, BLUE), (1, ORANGE)), start=1):
    fig.add_trace(go.Scatter(x=np.repeat(t, 2)[1:-1], y=np.repeat(U[:, k], 2), mode="lines",
                             line=dict(color=col, width=3)), row=r, col=1)
    fig.add_trace(go.Scatter(x=(t[:-1] + t[1:]) / 2, y=U[:, k], mode="markers", marker=dict(size=8, color=col)),
                  row=r, col=1)
    fig.add_hline(y=0, line=dict(color="#BBBBBB", width=1), row=r, col=1)
fig.update_xaxes(title="time (s), 30 intervals of 0.267 s", row=2, col=1)
fig.update_layout(template="simple_white", font=FONT, width=1100, height=720, showlegend=False,
                  margin=dict(l=70, r=20, t=50, b=60))
fig.write_image(here / "transcription.png", scale=2)
