"""Six encoder blocks trained on IMDB, with and without residual connections: validation accuracy per epoch,
3 seeds (thin) and their mean (thick) (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import RED, GREY, FONT

here = Path(__file__).parent
t = pd.read_csv(here.parent / "data" / "training.csv")
fig = go.Figure()
for res, name, col in ((True, "with residual connections", RED), (False, "without", GREY)):
    d = t[t.residual == res]
    for s, g in d.groupby("seed"):
        fig.add_trace(go.Scatter(x=g.epoch, y=g.val, showlegend=False, opacity=0.4, line=dict(color=col, width=1.5)))
    m = d.groupby("epoch").val.mean()
    fig.add_trace(go.Scatter(x=m.index, y=m.values, name=name + " (mean of 3)", mode="lines+markers",
                             line=dict(color=col, width=5), marker=dict(size=9)))
fig.add_hline(y=0.5, line=dict(color=GREY, dash="dot", width=1.5))
fig.add_annotation(x=3, y=0.5, text="guessing", showarrow=False, yshift=12, xanchor="right")
fig.update_layout(template="simple_white", width=900, height=430, font=FONT, margin=dict(l=70, r=20, t=20, b=60),
                  xaxis=dict(title="epoch", tickvals=[1, 2, 3]), yaxis=dict(title="validation accuracy", range=[0.4, 0.95]),
                  legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.85)"))
fig.write_image(here / "training.png", scale=2)
fig.write_image(here / "training.pdf")
