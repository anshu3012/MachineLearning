"""The loss of the network as a function of b21 alone, and 10 updates of b21 from -5 with four learning rates
(paths from the Notebook) (Plotly)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, GREEN, RED, GREY, FONT

here = Path(__file__).parent
paths = pd.read_csv(here.parent / "data" / "b21_paths.csv")
panels = [(0.01, "η = 0.01: tiny steps, slow", ORANGE, (-7, 9)), (0.1, "η = 0.1: steps shrink, converges", GREEN, (-7, 9)),
          (1.0, "η = 1: jumps between −5 and 12.36", BLUE, (-7, 15)), (1.1, "η = 1.1: each jump bigger, diverges", RED, (-55, 30))]
fig = make_subplots(rows=2, cols=2, subplot_titles=[p[1] for p in panels], vertical_spacing=0.16, horizontal_spacing=0.1)
for k, (lr, _, c, (lo, hi)) in enumerate(panels):
    r, col = k // 2 + 1, k % 2 + 1
    b = np.linspace(lo, hi, 400)
    fig.add_trace(go.Scatter(x=b, y=(3.68 - b) ** 2, mode="lines", line=dict(color=GREY, width=3), showlegend=False),
                  row=r, col=col)
    p = paths[paths.lr == lr]
    p = p[(p.b21 >= lo) & (p.b21 <= hi)]
    fig.add_trace(go.Scatter(x=p.b21, y=p.loss, mode="lines+markers", line=dict(color=c, width=2),
                             marker=dict(size=10, color=c), showlegend=False), row=r, col=col)
    fig.add_trace(go.Scatter(x=[p.b21.iloc[0]], y=[p.loss.iloc[0]], mode="markers+text", text=["start"],
                             textposition="top right", marker=dict(size=14, color="black", symbol="x"),
                             showlegend=False), row=r, col=col)
    fig.update_xaxes(title_text="b21", range=[lo, hi], row=r, col=col)
    fig.update_yaxes(title_text="loss", row=r, col=col)
fig.update_layout(template="simple_white", width=1100, height=820, font=FONT, margin=dict(l=70, r=30, t=60, b=60))
fig.update_annotations(font=dict(family="Latin Modern Roman", size=18))
fig.write_image(here / "lr_paths.png", scale=2)
fig.write_image(here / "lr_paths.pdf")
