"""Section 3's idea as bars: the new "bank" as a mix of the words of its phrase, with the real weights of the simple
self-attention (data/weights_simple.csv, from the Notebook). Plotly."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREEN, PURPLE, GREY, FONT

here = Path(__file__).parent
W = pd.read_csv(here.parent / "data" / "weights_simple.csv", index_col=[0, 1])
m = W.loc[("money bank grows", "bank")]
r = W.loc[("river bank flows", "bank")]
assert (m.money, m.bank, m.grows) == (0.287, 0.524, 0.189) and (r.river, r.bank, r.flows) == (0.251, 0.539, 0.21)
fig = go.Figure()
rows = ['"bank" in "money bank grows"', '"bank" in "river bank flows"']
for word, col in (("money", GREEN), ("river", BLUE), ("bank", GREY), ("grows", ORANGE), ("flows", PURPLE)):
    vals = [m.get(word, float("nan")), r.get(word, float("nan"))]
    fig.add_bar(y=rows, x=vals, orientation="h", name=word, marker_color=col,
                text=[f"{word} {v:.2f}" if v == v else "" for v in vals], textposition="inside", insidetextanchor="middle")
fig.update_layout(barmode="stack", template="simple_white", width=1000, height=320, font=dict(FONT, size=20), showlegend=False,
                  xaxis=dict(title="share of the new vector (the weights sum to 1)", range=[0, 1]),
                  yaxis=dict(autorange="reversed"), margin=dict(l=20, r=20, t=20, b=70))
fig.update_traces(textfont=dict(color="white", size=19))
fig.write_image(here / "bank_mix.png", scale=2)
fig.write_image(here / "bank_mix.pdf")
