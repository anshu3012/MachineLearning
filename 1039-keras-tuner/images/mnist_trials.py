"""MNIST: validation accuracy of the 20 trials, best first, against the hand-made baseline's 5 runs (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, RED, FONT

here = Path(__file__).parent
t = pd.read_csv(here.parent / "data" / "mnist_trials.csv").sort_values("val_accuracy", ascending=False, kind="stable")
r = pd.read_csv(here.parent / "data" / "mnist_retrain.csv")
b = r[r.model == "baseline"].val_accuracy
base, lo, hi = b.mean(), b.min(), b.max()
x = list(range(1, len(t) + 1))
fig = go.Figure()
fig.add_hrect(y0=lo, y1=hi, fillcolor=RED, opacity=0.25, line_width=0, layer="below")
fig.add_hline(y=base, line=dict(color=RED, width=3, dash="dash"))
fig.add_trace(go.Scatter(x=x, y=t.val_accuracy, mode="markers", marker=dict(color=BLUE, size=16)))
fig.add_annotation(x=0.99, y=0.02, xref="paper", yref="paper", xanchor="right", yanchor="bottom", showarrow=False,
                   font=dict(color=RED, size=17), bgcolor="white",
                   text=f"red line and band: baseline, 5 runs (mean {base:.3f}, range {lo:.3f} to {hi:.3f})")
ymin = min(t.val_accuracy.min(), lo) - 0.03
fig.update_layout(template="simple_white", width=1000, height=470, font=FONT, showlegend=False,
                  xaxis=dict(title="trial, ranked by its score (number of layers, optimizer)", tickmode="array",
                             tickvals=x, tickfont=dict(size=12),
                             ticktext=[f"{n}<br>{o}" for n, o in zip(t.num_layers, t.optimizer)]),
                  yaxis=dict(title="validation accuracy", range=[ymin, 1.0]),
                  margin=dict(l=80, r=20, t=20, b=90))
fig.write_image(here / "mnist_trials.png", scale=2)
fig.write_image(here / "mnist_trials.pdf")
