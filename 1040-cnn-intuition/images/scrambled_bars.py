"""Test accuracy on normal and on scrambled MNIST for the ANN (data/scramble_results.csv, from the Notebook) and for
the small CNN (data/scramble_cnn.csv, from experiments/scrambled_cnn.py); means of 3 seeds. Plotly grouped bars,
the natural chart for four numbers in two groups.  Run: python scrambled_bars.py -> scrambled_bars.png"""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
ann = pd.read_csv(here.parent / "data" / "scramble_results.csv").groupby("images").test_acc.mean() * 100
cnn = pd.read_csv(here.parent / "data" / "scramble_cnn.csv").groupby("images").test_acc.mean() * 100
print(ann.round(2).to_dict(), cnn.round(2).to_dict())
assert abs(ann["normal"] - ann["scrambled"]) < 0.2 and cnn["normal"] - cnn["scrambled"] > 5
fig = go.Figure()
for key, color, name in (("normal", BLUE, "normal images"), ("scrambled", ORANGE, "scrambled images")):
    vals = [ann[key], cnn[key]]
    fig.add_trace(go.Bar(x=["ANN (Flatten + Dense)", "small CNN (2 convolution layers)"], y=vals, name=name, marker_color=color,
                         text=[f"{v:.2f}%" for v in vals], textposition="outside", textfont=dict(size=22)))
fig.update_layout(template="simple_white", width=1000, height=560, font=dict(FONT, size=22), barmode="group",
                  yaxis=dict(title="test accuracy (percent)", range=[80, 100]),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=1.02, yanchor="bottom"),
                  margin=dict(l=90, r=20, t=60, b=60))
fig.write_image(here / "scrambled_bars.png", scale=2)
