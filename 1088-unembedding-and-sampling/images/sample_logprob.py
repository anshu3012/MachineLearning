"""Section 6.2: 10 sampled continuations of 12 tokens at each temperature (seeds 0 to 9) on "Once upon a time there
was a". Dots: the mean log-probability (at T = 1) of each sample's chosen tokens; line: the mean over the 10 samples.
The higher T, the less likely the chosen tokens (data/samples.csv, Notebook). Plotly."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, GREY, RED, FONT

here = Path(__file__).parent
S = pd.read_csv(here.parent / "data" / "samples.csv")
m = S.groupby("T").mean_logprob.mean()
assert np.allclose(m.round(2).tolist(), [-1.95, -2.17, -2.97, -5.19, -8.42])
fig = go.Figure()
fig.add_scatter(x=S["T"], y=S.mean_logprob, mode="markers", marker=dict(size=9, color=GREY, opacity=0.6), name="one sample")
fig.add_scatter(x=m.index, y=m.values, mode="lines+markers+text", line=dict(color=BLUE, width=4), marker=dict(size=12),
                text=[f"{v:.2f}" for v in m.values], textposition="top right", name="mean of 10")
fig.add_annotation(x=1.5, y=m[1.5], text=f"chosen token's probability<br>about e<sup>{m[1.5]:.2f}</sup> ≈ {np.exp(m[1.5]):.4f}",
                   showarrow=True, ax=-150, ay=30, font=dict(size=16, color=RED))
fig.update_layout(template="simple_white", width=1000, height=450, font=dict(FONT, size=19),
                  xaxis=dict(title="temperature T (0 = greedy)", tickvals=[0, 0.3, 0.7, 1.0, 1.5]),
                  yaxis=dict(title="mean log-prob of chosen tokens"),
                  legend=dict(x=0.02, y=0.08), margin=dict(l=90, r=20, t=20, b=70))
fig.write_image(here / "sample_logprob.png", scale=2)
fig.write_image(here / "sample_logprob.pdf")
