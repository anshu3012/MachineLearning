"""Maximising 2/||w|| is minimising ||w||/2 (Plotly): both curves against ||w||. The margin 2/||w|| falls as ||w||
grows and the term ||w||/2 rises, so the smallest feasible ||w|| is best for both. Marked: ||w|| = 0.899, the SVM of
the intuition Note, with margin 2.22 and term 0.45."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, ORANGE

here = Path(__file__).parent
n = np.linspace(0.3, 3, 300)
assert round(2 / 0.899, 2) == 2.22 and round(0.899 / 2, 2) == 0.45
fig = go.Figure([go.Scatter(x=n, y=2 / n, mode="lines", line=dict(color=BLUE, width=4), name="margin 2/‖w‖ (maximise)"),
                 go.Scatter(x=n, y=n / 2, mode="lines", line=dict(color=ORANGE, width=4), name="‖w‖/2 (minimise)")])
fig.add_scatter(x=[0.899, 0.899], y=[0, 7], mode="lines", line=dict(color="black", dash="dash", width=2), showlegend=False)
fig.add_scatter(x=[0.899, 0.899], y=[2.22, 0.45], mode="markers+text", text=["2.22", "0.45"], textposition="middle right",
                textfont=dict(size=20), marker=dict(size=12, color=[BLUE, ORANGE]), showlegend=False)
fig.add_annotation(x=0.899, y=6.3, text="‖w‖ = 0.899", showarrow=False, xanchor="left", xshift=6, font=dict(size=19))
fig.update_layout(template="simple_white", width=900, height=520, font=FONT,
                  xaxis=dict(title="length of w, ‖w‖"), yaxis=dict(range=[0, 7]), legend=dict(x=0.5, y=0.98),
                  margin=dict(l=70, r=30, t=20, b=70))
fig.write_image(here / "max_min.png", scale=2)
