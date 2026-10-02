"""Data vs performance: ML levels off, DL keeps improving. Concept curves, not measurements."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
x = np.linspace(0, 10, 200)
ml = 0.62 * (1 - np.exp(-1.1 * x)) + 0.1     # rises fast, then flattens
dl = 0.9 / (1 + np.exp(-0.9 * (x - 5.2))) + 0.04  # weak on small data, keeps climbing

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=ml, name="Machine Learning", line=dict(color="#F58518", width=5)))
fig.add_trace(go.Scatter(x=x, y=dl, name="Deep Learning", line=dict(color="#54A24B", width=5)))
fig.add_annotation(x=8.6, y=0.76, text="ML stops improving", showarrow=False, font=dict(color="#F58518", size=18))
fig.add_annotation(x=8.2, y=0.98, text="DL keeps improving", showarrow=False, font=dict(color="#54A24B", size=18))
fig.add_vrect(x0=0, x1=3, fillcolor="#6B6B6B", opacity=0.08, line_width=0)
fig.add_annotation(x=1.5, y=0.97, text="small data:<br>ML wins", showarrow=False, font=dict(size=16, color="#6B6B6B"))
fig.update_layout(
    template="simple_white", width=900, height=540, font=dict(family="Roboto, Arial", size=18),
    title=dict(text="More data helps DL much more than ML", x=0.5),
    xaxis=dict(title="Amount of data", showticklabels=False, ticks=""),
    yaxis=dict(title="Performance", showticklabels=False, ticks="", range=[0, 1.05]),
    legend=dict(x=0.62, y=0.3), margin=dict(l=70, r=30, t=70, b=60),
)
fig.add_annotation(x=10, y=0.02, xanchor="right", text="illustration, not real measurements", showarrow=False,
                   font=dict(size=13, color="#6B6B6B"))
fig.write_image(here / "data_vs_performance.png", scale=2)
fig.write_image(here / "data_vs_performance.pdf")
