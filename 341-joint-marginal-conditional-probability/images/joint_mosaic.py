"""The joint distribution of class and survival (891 Titanic passengers, data/titanic_train.csv) as a unit square
cut into six tiles: each column's width is P(class), each tile's height within it is P(died or survived | class),
so each tile's area is the joint probability. The six areas fill the square: they sum to 1."""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
BLUE, RED = "#4C78A8", "#E45756"
df = pd.read_csv(here.parent / "data" / "titanic_train.csv")
counts = pd.crosstab(df["Pclass"], df["Survived"])
assert counts.values.tolist() == [[80, 136], [97, 87], [372, 119]]
joint = counts / counts.values.sum()
px = joint.sum(axis=1)
assert abs(joint.values.sum() - 1) < 1e-12
fig = go.Figure()
x0 = 0.0
for c in (1, 2, 3):
    w = px[c]
    died = joint.loc[c, 0] / w                                # height of the died tile = P(died | class)
    for y0, y1, col, s in ((0, died, RED, 0), (died, 1, BLUE, 1)):
        fig.add_shape(type="rect", x0=x0, x1=x0 + w, y0=y0, y1=y1, fillcolor=col, opacity=0.75,
                      line=dict(color="white", width=4))
        fig.add_annotation(x=x0 + w / 2, y=(y0 + y1) / 2, showarrow=False, font=dict(size=24, color="white"),
                           text=f"<b>{joint.loc[c, s]:.3f}</b>")
    fig.add_annotation(x=x0 + w / 2, y=-0.07, showarrow=False, font=dict(size=22),
                       text=f"class {c}<br>width {w:.3f}")
    x0 += w
fig.add_annotation(x=1.02, y=0.15, xanchor="left", showarrow=False, text="died", font=dict(size=22, color=RED))
fig.add_annotation(x=1.02, y=0.85, xanchor="left", showarrow=False, text="survived", font=dict(size=22, color=BLUE))
fig.update_xaxes(visible=False, range=[-0.01, 1.16])
fig.update_yaxes(visible=False, range=[-0.15, 1.01], scaleanchor="x", scaleratio=0.75)
fig.update_layout(template="simple_white", width=900, height=640, showlegend=False,
                  title=dict(text="six tiles, total area 1", x=0.5), font=dict(family="Latin Modern Roman", size=22),
                  margin=dict(l=10, r=10, t=60, b=10))
fig.write_image(here / "joint_mosaic.png", scale=2)
fig.write_image(here / "joint_mosaic.pdf")
