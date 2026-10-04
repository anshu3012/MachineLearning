"""200 students, CGPA vs package: guessing the average for everyone vs the fitted line (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import df, M, B

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
xs = np.array([4.2, 9.7])
mean = df.package.mean()
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.cgpa, y=df.package, mode="markers", marker=dict(size=8, color=BLUE, opacity=0.6),
                         name="students"))
fig.add_trace(go.Scatter(x=xs, y=[mean, mean], mode="lines", line=dict(color=RED, width=3, dash="dash"),
                         name=f"same guess for all: average {mean:.2f} LPA"))
fig.add_trace(go.Scatter(x=xs, y=M * xs + B, mode="lines", line=dict(color=ORANGE, width=4),
                         name=f"best-fit line: package = {M:.3f} × CGPA − {abs(B):.3f}"))
fig.update_layout(template="simple_white", width=950, height=540, font=dict(family="Latin Modern Roman", size=17),
                  title=dict(text="Placement data: package rises with CGPA, roughly along a line", x=0.5),
                  xaxis=dict(title="CGPA"), yaxis=dict(title="Package (lakh rupees per year, LPA)"),
                  legend=dict(x=0.01, y=0.99), margin=dict(l=80, r=30, t=60, b=60))
fig.write_image(here / "baseline_vs_line.png", scale=2)
fig.write_image(here / "baseline_vs_line.pdf")
