"""Each next-token logit of GPT-2 small (after "Steve Jobs was the founder of") against the cosine between the final
vector and that token's embedding row, after removing the mean row that all rows share. 3,000 random tokens plus
the 300 most likely; the top 10 labelled. Data: data/logit_vs_cosine.csv (Notebook).
Run: python logit_cosine.py -> logit_cosine.png"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

from common import FONT, GREY, ORANGE, DATA

HERE = Path(__file__).parent
d = pd.read_csv(DATA / "logit_vs_cosine.csv", keep_default_na=False)
top = d[d.top10].sort_values("logit", ascending=False).head(2)
fig = go.Figure(go.Scattergl(x=d.centred_cosine, y=d.logit, mode="markers", marker=dict(size=4, color=GREY, opacity=0.4),
                             showlegend=False))
fig.add_trace(go.Scatter(x=d[d.top10].centred_cosine, y=d[d.top10].logit, mode="markers",
                         marker=dict(size=9, color=ORANGE), showlegend=False))
for k, (_, r) in enumerate(top.iterrows()):
    fig.add_annotation(x=r.centred_cosine, y=r.logit, text=r.token.strip() or repr(r.token), showarrow=True,
                       ax=-80, ay=-20 + 30 * k, font=dict(size=18, color=ORANGE))
fig.update_layout(template="simple_white", width=860, height=520, font=FONT,
                  xaxis=dict(title="cosine between the final vector and the token's row (mean row removed)"),
                  yaxis=dict(title="logit"), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(HERE / "logit_cosine.png", scale=2)
