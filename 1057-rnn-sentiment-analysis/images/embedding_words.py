"""The 2-number embedding learned on IMDB: a few positive, negative and neutral words (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import GREEN, RED, GREY, FONT

here = Path(__file__).parent
e = pd.read_csv(here.parent / "data" / "embedding_words.csv")
# label placement, so close points do not overlap
POS = {"waste": "bottom center", "terrible": "bottom center", "loved": "bottom center", "perfect": "middle right",
       "wonderful": "middle left", "the": "middle right", "and": "bottom right", "of": "middle left", "film": "top right",
       "story": "bottom center", "amazing": "top center"}
e["pos"] = e.word.map(POS).fillna("top center")
fig = go.Figure()
for g, col in (("positive", GREEN), ("negative", RED), ("neutral", GREY)):
    d = e[e.group == g]
    fig.add_trace(go.Scatter(x=d.e1, y=d.e2, mode="markers+text", text=d.word, textposition=list(d.pos), name=g,
                             marker=dict(size=11, color=col), textfont=dict(color=col, size=15)))
fig.update_layout(template="simple_white", width=900, height=560, font=FONT,
                  xaxis=dict(title="embedding number 1"), yaxis=dict(title="embedding number 2"),
                  legend=dict(x=1.0, y=1.0, xanchor="right", bgcolor="rgba(255,255,255,0.8)"), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "embedding_words.png", scale=2)
fig.write_image(here / "embedding_words.pdf")
