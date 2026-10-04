"""32 real IMDB reviews padded to the longest one (888 words): which positions hold a word and which hold padding (Plotly)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from common import FONT

here = Path(__file__).parent
lengths = pd.read_csv(here.parent / "data" / "imdb_batch_lengths.csv").length.to_numpy()
T = lengths.max()
real = (np.arange(T)[None, :] < lengths[:, None]).astype(int)
fig = go.Figure(go.Heatmap(z=real, colorscale=[[0, "#E8E8E8"], [1, "#4C78A8"]], showscale=False))
fig.add_annotation(x=T * 0.72, y=8, text=f"padding: {1 - real.mean():.0%} of all positions", showarrow=False,
                   font=dict(size=22), bgcolor="white")
fig.update_layout(template="simple_white", width=950, height=430, font=FONT,
                  xaxis=dict(title="position in the review (blue: a real word, grey: padding)"),
                  yaxis=dict(title="review", autorange="reversed"), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "imdb_padding.png", scale=2)
fig.write_image(here / "imdb_padding.pdf")
