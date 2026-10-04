"""IMDB, last 50 words per review: train and test accuracy per epoch for integer encoding vs a learned
embedding, same SimpleRNN(32). Mean of 3 seeds (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import GREY, GREEN, FONT

here = Path(__file__).parent
c = pd.read_csv(here.parent / "data" / "imdb_curves.csv").groupby(["approach", "epoch"]).mean(numeric_only=True).reset_index()
fig = go.Figure()
for name, col in (("integer encoding", GREY), ("embedding", GREEN)):
    d = c[c.approach == name]
    fig.add_trace(go.Scatter(x=d.epoch, y=d.accuracy, name=f"{name}: training", line=dict(color=col, width=4, dash="dash")))
    fig.add_trace(go.Scatter(x=d.epoch, y=d.val_accuracy, name=f"{name}: test", line=dict(color=col, width=4)))
fig.update_layout(template="simple_white", width=950, height=450, font=FONT, xaxis=dict(title="epoch", dtick=1),
                  yaxis=dict(title="accuracy (mean of 3 runs)", range=[0.45, 1.0]),
                  legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.8)"), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "imdb_curves.png", scale=2)
fig.write_image(here / "imdb_curves.pdf")
