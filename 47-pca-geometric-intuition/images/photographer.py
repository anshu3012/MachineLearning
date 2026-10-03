"""A photo turns the 3D match into 2D. Top view of 10 players, and what two cameras see (Plotly).
Camera A looks along the pitch: players bunch up. Camera B looks across it: players stay apart."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
rng = np.random.default_rng(3)
x = np.sort(rng.uniform(8, 92, 10))          # along the pitch (long side, 100 m)
y = 30 + rng.normal(0, 4, 10)                 # across the pitch (short side, 60 m)
fig = make_subplots(2, 2, column_widths=[0.55, 0.45], horizontal_spacing=0.08, vertical_spacing=0.3,
                    specs=[[{"rowspan": 2}, {}], [None, {}]],
                    subplot_titles=("Top view of the pitch", "Camera A's photo: players overlap",
                                    "Camera B's photo: players stay apart"))
fig.add_shape(type="rect", x0=0, y0=0, x1=100, y1=60, line=dict(color=GREEN, width=3),
              fillcolor="rgba(84,162,75,0.10)", row=1, col=1)
fig.add_shape(type="line", x0=50, y0=0, x1=50, y1=60, line=dict(color=GREEN, width=2), row=1, col=1)
fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(size=14, color=BLUE)), 1, 1)
fig.add_annotation(x=-2, y=30, ax=-50, ay=0, text="A", showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor=RED,
                   font=dict(color=RED, size=20), row=1, col=1)
fig.add_annotation(x=50, y=-3, ax=0, ay=50, text="B", showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor=ORANGE,
                   font=dict(color=ORANGE, size=20), row=1, col=1)
# camera A looks along x, so its photo shows only y; camera B looks along y, so its photo shows only x
fig.add_trace(go.Scatter(x=y, y=np.zeros(10), mode="markers", marker=dict(size=16, color=BLUE, opacity=0.55)), 1, 2)
fig.add_trace(go.Scatter(x=x, y=np.zeros(10), mode="markers", marker=dict(size=16, color=BLUE, opacity=0.55)), 2, 2)
fig.update_xaxes(range=[-22, 104], visible=False, row=1, col=1)
fig.update_yaxes(range=[-22, 64], visible=False, scaleanchor="x", row=1, col=1)
for r, lim in ((1, 60), (2, 100)):
    fig.update_xaxes(range=[-3, lim + 3], title="position in the photo", showticklabels=False, ticks="", row=r, col=2)
    fig.update_yaxes(visible=False, range=[-1, 1], row=r, col=2)
print("spread seen by A (std):", y.std().round(1), " by B:", x.std().round(1))
fig.update_layout(template="simple_white", width=1000, height=440, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=20, r=20, t=50, b=20))
fig.update_annotations(font_size=17)
fig.write_image(here / "photographer.png", scale=2)
fig.write_image(here / "photographer.pdf")
