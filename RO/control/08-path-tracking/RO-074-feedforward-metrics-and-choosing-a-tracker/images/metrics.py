"""How the three metrics read one finished run: pure pursuit (4 m look-ahead) on the plan's car at 2 m/s, starting on
the line. Top: the lateral error at the rear axle; the RMS lateral error, 0.086 m, drawn as dashed lines either side of 0;
the peak, 0.167 m, as a dot. Bottom: the steering command; its steering travel, 30 degrees, is the sum of all its
rises and falls: up to 14.7 degrees into the arc and back down out of it.
Run: python metrics.py -> metrics.png (and metrics.html)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import ffkit as fk
import trackkit as tk
from gifkit import BLUE, FONT, GREY, RED

here = Path(__file__).parent
run = tk.simulate(tk.law("pp"), v=2.0, start=(0.0, 0.0, 0.0))
m = fk.scores(run)
s, e, d = run["s"], run["e"], np.degrees(run["delta"])
ip = int(np.argmax(np.abs(e)))
assert abs(m["rms"] - 0.086) < 5e-4 and abs(m["peak"] - 0.167) < 5e-4 and abs(m["travel"] - 30.1) < 0.05
assert abs(d.max() - 14.7) < 0.05

fig = make_subplots(rows=2, cols=1, row_heights=[0.55, 0.45], vertical_spacing=0.12)
for y0 in (-m["rms"], m["rms"]):
    fig.add_trace(go.Scatter(x=[0, 36.5], y=[y0, y0], mode="lines", line=dict(color=BLUE, width=2, dash="dash"),
                             showlegend=False), row=1, col=1)
fig.add_trace(go.Scatter(x=s, y=e, mode="lines", line=dict(color=BLUE, width=4), name="lateral error"), row=1, col=1)
fig.add_trace(go.Scatter(x=[s[ip]], y=[e[ip]], mode="markers", marker=dict(color=RED, size=16), showlegend=False),
              row=1, col=1)
fig.add_annotation(x=s[ip], y=e[ip], ax=60, ay=-10, text=f"peak {abs(e[ip]):.3f} m", font=dict(size=20, color=RED),
                   arrowcolor=RED, xanchor="left", row=1, col=1)
fig.add_annotation(x=1, y=-m["rms"], yanchor="top", xanchor="left", showarrow=False,
                   text=f"dashed: ± the RMS, {m['rms']:.3f} m", font=dict(size=19, color=BLUE), row=1, col=1)
fig.add_trace(go.Scatter(x=s, y=d, mode="lines", line=dict(color=BLUE, width=4), name="steering"), row=2, col=1)
fig.add_annotation(x=17.9, y=d.max(), yanchor="bottom", showarrow=False, text=f"up to {d.max():.1f}°",
                   font=dict(size=19), row=2, col=1)
fig.add_annotation(x=27.5, y=14, xanchor="left", showarrow=False, align="left",
                   text=f"steering travel: all rises<br>and falls added up, {m['travel']:.0f}°",
                   font=dict(size=19), row=2, col=1)
for row in (1, 2):
    for s0 in (tk.S1, tk.S2):
        fig.add_vline(x=s0, line=dict(color=GREY, dash="dot", width=1.5), row=row, col=1)
fig.add_annotation(x=(tk.S1 + tk.S2) / 2, y=0.21, text="arc", showarrow=False, font=dict(size=18, color=GREY),
                   row=1, col=1)
fig.add_hline(y=0, line=dict(color="black", width=1), row=1, col=1)
fig.update_layout(template="simple_white", font=FONT, width=1000, height=820, showlegend=False,
                  margin=dict(l=110, r=30, t=40, b=70))
fig.update_xaxes(range=[0, 36.5], dtick=5, row=1, col=1)
fig.update_yaxes(title_text="lateral error (m)<br>+ = left", range=[-0.22, 0.24], row=1, col=1)
fig.update_xaxes(title_text="distance along the course (m)", range=[0, 36.5], dtick=5, row=2, col=1)
fig.update_yaxes(title_text="steering (°)", range=[-2, 18], row=2, col=1)
fig.write_image(here / "metrics.png", scale=2)
