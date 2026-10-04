"""Where LeNet-5's 61,706 parameters sit, layer by layer (model.summary() in the Notebook) (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREEN, GREY, FONT

here = Path(__file__).parent
s = pd.read_csv(here.parent / "data" / "lenet_summary.csv")
assert s.params.sum() == 61_706 and s.params.max() == 48_120
assert (5 * 5 * 1 + 1) * 6 == 156 and (5 * 5 * 6 + 1) * 16 == 2_416 and (400 + 1) * 120 == 48_120
names = ["conv 1 (6 @ 5×5)", "avg pool 1", "conv 2 (16 @ 5×5)", "avg pool 2", "flatten", "dense 120", "dense 84",
         "dense 10 (output)"]
col = [BLUE, ORANGE, BLUE, ORANGE, GREY, GREEN, GREEN, GREEN]
fig = go.Figure(go.Bar(y=names[::-1], x=s.params[::-1], orientation="h", marker_color=col[::-1],
                       text=[f"{p:,} ({p / s.params.sum():.1%})" for p in s.params[::-1]], textposition="outside",
                       textfont=dict(size=18)))
fig.update_layout(template="simple_white", width=950, height=500, font=dict(FONT, size=18),
                  xaxis=dict(title="parameters", range=[0, 62000]), margin=dict(l=20, r=20, t=20, b=60))
fig.write_image(here / "param_share.png", scale=2)
fig.write_image(here / "param_share.pdf")
