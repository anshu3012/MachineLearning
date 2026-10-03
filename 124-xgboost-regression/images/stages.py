"""The 4-student data: stage 1 (the mean and its residuals) and stage 2 (mean + 0.3 x first XGBoost tree), Plotly."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
x = np.array([6.7, 9.0, 7.5, 5.0])
y = np.array([4.5, 11.0, 6.0, 8.0])
f0 = y.mean()
tree = lambda v: np.where(v < 5.85, 0.625, np.where(v < 8.25, -2.125, 3.625))   # the tree of Figure 4
pred2 = f0 + 0.3 * tree(x)
grid = np.linspace(4.6, 9.4, 1000)

fig = make_subplots(1, 2, subplot_titles=["stage 1: the mean, 7.375", "stage 2: mean + 0.3 x tree 1"],
                    horizontal_spacing=0.08)
for col, pred, line_y in [(1, np.full(4, f0), np.full_like(grid, f0)), (2, pred2, f0 + 0.3 * tree(grid))]:
    for xi, yi, pi in zip(x, y, pred):
        fig.add_trace(go.Scatter(x=[xi, xi], y=[yi, pi], mode="lines", line=dict(color="#6B6B6B", width=2, dash="dot"),
                                 showlegend=False), 1, col)
    fig.add_trace(go.Scatter(x=grid, y=line_y, mode="lines", line=dict(color="#E45756", width=3, shape="hv"),
                             name="model prediction", showlegend=(col == 1)), 1, col)
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(color="#4C78A8", size=13), name="students",
                             showlegend=(col == 1)), 1, col)
    for xi, yi, pi in zip(x, y, pred):
        fig.add_annotation(x=xi + 0.08, y=(yi + pi) / 2, text=f"{yi - pi:+.2f}", showarrow=False, xanchor="left",
                           font=dict(size=20, color="#6B6B6B"), row=1, col=col)
    print(col, np.round(y - pred, 4))
fig.update_xaxes(title="CGPA", range=[4.6, 9.4])
fig.update_yaxes(title="package (LPA)", range=[3.5, 12], col=1)
fig.update_yaxes(range=[3.5, 12], col=2)
fig.update_annotations(font_family="Latin Modern Roman")
for a in fig.layout.annotations[:2]:
    a.font.size = 24
fig.update_layout(template="simple_white", width=1300, height=560, font=FONT, margin=dict(l=70, r=20, t=50, b=70),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2))
fig.write_image(HERE / "stages.png", scale=2)
fig.write_image(HERE / "stages.pdf")
