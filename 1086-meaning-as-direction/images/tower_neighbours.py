"""Section 3: the 8 GloVe words with the highest cosine similarity to "tower" (data/tower_neighbours.csv, Notebook).
Plotly."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, FONT

here = Path(__file__).parent
T = pd.read_csv(here.parent / "data" / "tower_neighbours.csv")
assert T.word.tolist()[:3] == ["towers", "building", "dome"] and T.cosine.iloc[0] == 0.847
fig = go.Figure(go.Bar(y=T.word, x=T.cosine, orientation="h", marker_color=BLUE, text=[f"{c:.2f}" for c in T.cosine],
                       textposition="outside"))
fig.update_layout(template="simple_white", width=900, height=420, font=dict(FONT, size=20), showlegend=False,
                  xaxis=dict(title='cosine similarity with "tower"', range=[0, 1]), yaxis=dict(autorange="reversed"),
                  margin=dict(l=20, r=20, t=20, b=60))
fig.write_image(here / "tower_neighbours.png", scale=2)
fig.write_image(here / "tower_neighbours.pdf")
