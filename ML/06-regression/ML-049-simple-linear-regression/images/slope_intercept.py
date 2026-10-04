"""What m and b mean: +1 CGPA adds m to the package; b is where the line meets CGPA = 0 (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import df, M, B

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
xs = np.array([0, 10])
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.cgpa, y=df.package, mode="markers", marker=dict(size=6, color=BLUE, opacity=0.35)))
fig.add_trace(go.Scatter(x=[4.2, 10], y=[M * 4.2 + B, M * 10 + B], mode="lines", line=dict(color=ORANGE, width=4)))
fig.add_trace(go.Scatter(x=[0, 4.2], y=[B, M * 4.2 + B], mode="lines", line=dict(color=ORANGE, width=3, dash="dot")))
# slope triangle from CGPA 7 to 8
y7, y8 = M * 7 + B, M * 8 + B
fig.add_trace(go.Scatter(x=[7, 8, 8], y=[y7, y7, y8], mode="lines", line=dict(color=GREEN, width=3)))
fig.add_annotation(x=7.5, y=y7, yshift=-16, text="+1 CGPA", showarrow=False, bgcolor="white", font=dict(color=GREEN, size=16))
fig.add_annotation(x=8, y=(y7 + y8) / 2, xshift=8, xanchor="left", text=f"+{M:.2f} LPA = m", showarrow=False, bgcolor="white",
                   font=dict(color=GREEN, size=16))
fig.add_trace(go.Scatter(x=[0], y=[B], mode="markers", marker=dict(size=13, color=RED)))
fig.add_annotation(x=0, y=B, xshift=10, xanchor="left", yshift=-4, text=f"b = −{abs(B):.2f}: the line's value at CGPA 0",
                   showarrow=False, font=dict(color=RED, size=16))
fig.add_trace(go.Scatter(x=[10], y=[M * 10 + B], mode="markers", marker=dict(size=11, color=ORANGE)))
fig.add_annotation(x=10, y=M * 10 + B, xshift=-8, yshift=14, xanchor="right",
                   text=f"CGPA 10: {M * 10 + B:.2f} LPA", showarrow=False, font=dict(size=15))
fig.update_layout(template="simple_white", width=950, height=560, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=80, r=30, t=60, b=60),
                  title=dict(text=f"package = {M:.3f} × CGPA − {abs(B):.3f}", x=0.5),
                  xaxis=dict(title="CGPA", range=[-0.3, 10.4], zeroline=True, zerolinecolor="#BBBBBB"),
                  yaxis=dict(title="Package (LPA)", range=[-1.5, 5.5], zeroline=True, zerolinecolor="#BBBBBB"))
fig.write_image(here / "slope_intercept.png", scale=2)
fig.write_image(here / "slope_intercept.pdf")
