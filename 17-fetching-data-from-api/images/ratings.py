"""The dataset built from the TVmaze API: how the 1,208 shows are rated."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "shows.csv")
rated = df.dropna(subset=["rating.average"])
r = rated["rating.average"]
fig = go.Figure(go.Histogram(x=r, xbins=dict(start=0, end=10.2, size=0.2), marker=dict(color="#4C78A8", opacity=0.85,
                                                                                    line=dict(color="white", width=1))))
fig.update_layout(template="simple_white", width=900, height=520, font=dict(family="Latin Modern Roman", size=18),
                  title=dict(text=f"{len(df):,} shows fetched, {len(rated):,} with a rating", x=0.5),
                  xaxis=dict(title="Average viewer rating (out of 10)", range=[r.min() - 0.3, r.max() + 0.3], dtick=1),
                  yaxis=dict(title="Number of shows", showgrid=True), margin=dict(l=80, r=20, t=70, b=70))
fig.write_image(here / "ratings.png", scale=2)
fig.write_image(here / "ratings.pdf")
