"""Moving mean of node 1 in the first batch normalisation layer, after every batch of training (seed 0, from the
Notebook), against the node's actual mean over all 500 observations at the end of training (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import GREEN, GREY, FONT

here = Path(__file__).parent
m = pd.read_csv(here.parent / "data" / "moving_mean.csv")
ACTUAL = 0.2255                                    # Notebook: actual mean of node 1 over all 500 rows after training
per_epoch = len(m) / 200
fig = go.Figure(go.Scatter(x=m.step / per_epoch, y=m.moving_mean, mode="lines", line=dict(color=GREEN, width=2.5),
                           name="moving mean, updated after every batch"))
fig.add_hline(y=ACTUAL, line=dict(color=GREY, width=2, dash="dash"),
              annotation_text=f"actual mean after training: {ACTUAL:.3f}", annotation_position="top left",
              annotation_font=dict(size=18, color=GREY))
fig.add_annotation(x=200, y=m.moving_mean.iloc[-1], text=f"{m.moving_mean.iloc[-1]:.3f}", xanchor="left", xshift=6,
                   showarrow=False, font=dict(size=18, color=GREEN))
fig.update_layout(template="simple_white", width=950, height=420, font=dict(family=FONT["family"], size=18),
                  xaxis=dict(title="epoch", range=[0, 212]), yaxis=dict(title="node 1: mean"),
                  legend=dict(x=0.35, y=1.0, bgcolor="rgba(255,255,255,0.8)"), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "moving_mean.png", scale=2)
fig.write_image(here / "moving_mean.pdf")
