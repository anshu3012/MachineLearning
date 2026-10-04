"""Training loss of the small CNN trained with the hand-derived gradients only (NumPy), 1 against 7 (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, FONT

here = Path(__file__).parent
d = pd.read_csv(here.parent / "data" / "numpy_training.csv")
fig = go.Figure(go.Scatter(x=d.step, y=d.loss, mode="lines+markers", line=dict(color=BLUE, width=3), marker=dict(size=6)))
fig.update_layout(template="simple_white", width=900, height=420, font=FONT, xaxis=dict(title="mini-batch (32 images each)"),
                  yaxis=dict(title="log loss of the batch", rangemode="tozero"), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "numpy_training.png", scale=2)
fig.write_image(here / "numpy_training.pdf")
