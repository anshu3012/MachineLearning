"""One sigmoid perceptron as a probability map: perceptron 1 of Figure 2, p = s(3 x1 + 3 x2). Contours every 0.1;
the 0.5 contour is its hyperplane (here a line). Plotly."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
s = lambda z: 1 / (1 + np.exp(-z))
xs = np.linspace(-3, 3, 301)
X1, X2 = np.meshgrid(xs, xs)
P = s(3 * X1 + 3 * X2)
assert abs(s(0) - 0.5) < 1e-12 and round(s(3 * 0.5 + 3 * 0.5), 3) == 0.953
fig = go.Figure(go.Contour(x=xs, y=xs, z=P, zmin=0, zmax=1, showscale=False, hoverinfo="skip",
                           colorscale=[[0, "#F6C9C9"], [0.5, "#FFFFFF"], [1, "#CBE5C5"]],
                           contours=dict(start=0.1, end=0.9, size=0.1, showlabels=True,
                                         labelfont=dict(size=18, color="#444")),
                           line=dict(width=1, color="#999")))
fig.add_trace(go.Contour(x=xs, y=xs, z=P, showscale=False, hoverinfo="skip", contours_coloring="none",
                         contours=dict(start=0.5, end=0.5, size=1), line=dict(width=5, color="black")))
fig.add_annotation(x=-0.6, y=0.6, ax=-150, ay=-60, text="hyperplane:<br>3x₁ + 3x₂ = 0, p = 0.5", showarrow=True, arrowwidth=2, font=dict(size=20),
                   bgcolor="rgba(255,255,255,0.85)")
fig.add_annotation(x=2.1, y=2.5, text="p → 1", showarrow=False, font=dict(size=24, color="#2E7D32"))
fig.add_annotation(x=-2.2, y=-2.5, text="p → 0", showarrow=False, font=dict(size=24, color="#C62828"))
fig.update_layout(template="simple_white", width=760, height=720, font=dict(family="Latin Modern Roman", size=22),
                  title=dict(text="One sigmoid perceptron: p = σ(3x₁ + 3x₂)", x=0.5),
                  xaxis=dict(title="x₁", range=[-3, 3]), yaxis=dict(title="x₂", range=[-3, 3], scaleanchor="x"),
                  margin=dict(l=70, r=20, t=70, b=70))
fig.write_image(HERE / "sigmoid_map.png", scale=2)
