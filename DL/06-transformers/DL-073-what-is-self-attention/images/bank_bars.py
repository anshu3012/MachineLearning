"""Section 6's table as bars: the cosine similarity of the vector for "bank" with "money" and with "river", for the
static vector and after self-attention in each phrase (data/bank_similarity.csv, from the Notebook). Plotly."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, GREEN, FONT

here = Path(__file__).parent
S = pd.read_csv(here.parent / "data" / "bank_similarity.csv")
assert S.sim_money.tolist() == [0.4, 0.68, 0.21] and S.sim_river.tolist() == [0.24, 0.13, 0.71]
labels = ["static vector<br>(any sentence)", 'after self-attention<br>"money bank grows"', 'after self-attention<br>"river bank flows"']
fig = go.Figure()
fig.add_bar(x=labels, y=S.sim_money, name='similarity to "money"', marker_color=GREEN, text=S.sim_money, textposition="outside")
fig.add_bar(x=labels, y=S.sim_river, name='similarity to "river"', marker_color=BLUE, text=S.sim_river, textposition="outside")
fig.update_layout(template="simple_white", width=1000, height=440, font=dict(FONT, size=20), barmode="group",
                  yaxis=dict(title='cosine similarity of "bank"', range=[0, 0.85]),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=1.12), margin=dict(l=80, r=20, t=50, b=80))
fig.write_image(here / "bank_bars.png", scale=2)
fig.write_image(here / "bank_bars.pdf")
