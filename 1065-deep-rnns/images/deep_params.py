"""Section 10: parameters of each recurrent layer in the two-layer model of section 6 (5 nodes per layer, 32-number
embeddings), for SimpleRNN, LSTM and GRU layers. Counts from data/imdb_params.csv (Keras model.summary() in the
Notebook), checked against the formulas: one, four and three copies of a simple layer (GRU: Keras' extra biases).
Run: python deep_params.py  -> deep_params.png (Plotly grouped bars)"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

from common import BLUE, ORANGE

HERE = Path(__file__).parent
p = pd.read_csv(HERE.parent / "data" / "imdb_params.csv").set_index("model")
simple = lambda d, u: d * u + u * u + u
assert list(p.loc["deep SimpleRNN", ["layer_1", "layer_2"]]) == [simple(32, 5), simple(5, 5)] == [190, 55]
assert list(p.loc["deep LSTM", ["layer_1", "layer_2"]]) == [4 * simple(32, 5), 4 * simple(5, 5)]
assert list(p.loc["deep GRU", ["layer_1", "layer_2"]]) == [3 * (simple(32, 5) + 5), 3 * (simple(5, 5) + 5)]

fig = go.Figure()
for col, name, colour in (("layer_1", "layer 1 (input: 32 numbers)", BLUE), ("layer_2", "layer 2 (input: 5 numbers)", ORANGE)):
    fig.add_trace(go.Bar(x=["SimpleRNN", "LSTM", "GRU"], y=p[col], name=name, marker_color=colour,
                         text=p[col], textposition="outside"))
fig.update_layout(template="simple_white", width=1000, height=500, font=dict(family="Latin Modern Roman", size=22),
                  title=dict(text="parameters per recurrent layer, 5 nodes each", x=0.5, y=0.97), barmode="group",
                  yaxis=dict(title="parameters", range=[0, 900]), legend=dict(orientation="h", x=0.5, xanchor="center", y=1.0, yanchor="bottom"),
                  margin=dict(l=80, r=20, t=110, b=50))

if __name__ == "__main__":
    fig.write_image(HERE / "deep_params.png", scale=2)
