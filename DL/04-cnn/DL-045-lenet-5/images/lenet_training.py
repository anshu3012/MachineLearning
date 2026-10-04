"""LeNet-5 on MNIST: training and validation accuracy per epoch, mean of the Notebook's 3 seeds, against the
MNIST ANN's 97.63% test accuracy (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREY, FONT

here = Path(__file__).parent
h = pd.read_csv(here.parent / "data" / "lenet_history.csv")
assert sorted(h.seed.unique()) == [1, 2, 3] and h.epoch.max() == 10
m = h.groupby("epoch")[["accuracy", "val_accuracy"]].mean()
fig = go.Figure()
fig.add_trace(go.Scatter(x=m.index, y=m.accuracy, name="training", line=dict(color=BLUE, width=3), mode="lines+markers"))
fig.add_trace(go.Scatter(x=m.index, y=m.val_accuracy, name="validation", line=dict(color=ORANGE, width=3),
                         mode="lines+markers"))
fig.add_hline(y=0.9763, line=dict(color=GREY, dash="dash", width=2))
fig.add_annotation(x=10, y=0.9763, xanchor="right", yshift=-14, showarrow=False, font=dict(color=GREY, size=17),
                   text="ANN of the MNIST ANN Note: 97.63% test")
fig.update_layout(template="simple_white", width=900, height=470, font=dict(FONT, size=18),
                  xaxis=dict(title="epoch", dtick=1), yaxis=dict(title="accuracy (mean of 3 seeds)", tickformat=".1%"),
                  legend=dict(x=0.6, y=0.3), margin=dict(l=90, r=20, t=20, b=60))
fig.write_image(here / "lenet_training.png", scale=2)
fig.write_image(here / "lenet_training.pdf")
