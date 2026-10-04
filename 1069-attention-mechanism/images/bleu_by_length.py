"""Test BLEU by English sentence length, encoder-decoder without and with attention, mean of 3 seeds (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import GREY, ORANGE, FONT

here = Path(__file__).parent
a = pd.read_csv(here.parent / "data" / "bleu_by_length.csv")
a = a[a.words != "all"]
order = ["1-4", "5-7", "8-10", "11-13", "14-16"]
fig = go.Figure()
for att, name, c in ((False, "without attention", GREY), (True, "with attention (Bahdanau)", ORANGE)):
    s = a[a.attention == att].groupby("words").bleu.agg(["mean", "min", "max"]).reindex(order)
    fig.add_trace(go.Scatter(x=order, y=s["mean"], name=name, mode="lines+markers", line=dict(color=c, width=4),
                             marker=dict(size=10), error_y=dict(type="data", symmetric=False, array=s["max"] - s["mean"],
                                                                arrayminus=s["mean"] - s["min"], thickness=1.5)))
fig.update_layout(template="simple_white", width=900, height=450, font=FONT,
                  xaxis=dict(title="number of words in the English sentence"),
                  yaxis=dict(title="test BLEU (mean of 3 seeds)", rangemode="tozero"),
                  legend=dict(x=0.6, y=0.98, bgcolor="rgba(255,255,255,0.8)"), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "bleu_by_length.png", scale=2)
fig.write_image(here / "bleu_by_length.pdf")
