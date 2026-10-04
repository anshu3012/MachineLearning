"""Angles between 3,000 rows of GPT-2 small's token-embedding table (768 numbers each), raw and after subtracting
the table's mean vector, against 3,000 random directions in 768 dimensions.
Data: data/gpt2_angles_hist.csv (Notebook). Run: python gpt2_angles.py"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREY, FONT

HERE = Path(__file__).parent
h = pd.read_csv(HERE.parent / "data" / "gpt2_angles_hist.csv")
fig = go.Figure()
for col, name, c in (("random", "random directions, 768 dims", GREY), ("raw", "GPT-2 rows, as stored", ORANGE),
                     ("centred", "GPT-2 rows, mean vector removed", BLUE)):
    fig.add_trace(go.Scatter(x=h.angle, y=h[col] * 100, mode="lines", name=name, line=dict(color=c, width=3),
                             fill="tozeroy", opacity=0.6))
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(FONT, size=18),
                  xaxis=dict(title="angle between two token vectors (degrees)", range=[55, 110]),
                  yaxis=dict(title="share of pairs (%)"), legend=dict(x=0.01, y=0.98),
                  margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(HERE / "gpt2_angles.png", scale=2)
fig.write_image(HERE / "gpt2_angles.pdf")
