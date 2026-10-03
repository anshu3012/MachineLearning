"""Assumption 1: each input against the target (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import df, BLUE, FONT

here = Path(__file__).parent
cols = ["feature1", "feature2", "feature3"]
r = [np.corrcoef(df[c], df["target"])[0, 1] for c in cols]
fig = make_subplots(1, 3, shared_yaxes=True, horizontal_spacing=0.04,
                    subplot_titles=[f"{c}: correlation {v:+.2f}" for c, v in zip(cols, r)])
for i, c in enumerate(cols, start=1):
    fig.add_trace(go.Scatter(x=df[c], y=df["target"], mode="markers", marker=dict(size=6, color=BLUE, opacity=0.6)), 1, i)
    fig.update_xaxes(title=c, row=1, col=i)
fig.update_yaxes(title="target", row=1, col=1)
fig.update_layout(template="simple_white", width=1100, height=400, showlegend=False, font=FONT,
                  margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font_size=16)
print([round(v, 3) for v in r])
fig.write_image(here / "linearity.png", scale=2)
fig.write_image(here / "linearity.pdf")
