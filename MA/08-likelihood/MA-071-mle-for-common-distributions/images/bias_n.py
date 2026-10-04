"""Biased but consistent (Plotly). For each sample size n from 2 to 20, draw 100,000 samples of n mice from
N(32, 2^2) (true variance 4) and average the two variance estimates. The sample variance (divide by n - 1) averages 4
for every n; the MLE variance (divide by n) averages (n - 1)/n x 4: 3.2 at n = 5, closing on 4 as n grows."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
rng = np.random.default_rng(0)
ns = np.arange(2, 21)
mle, s2 = [], []
for n in ns:
    x = rng.normal(32, 2, size=(100_000, n))
    mle.append(x.var(axis=1).mean())
    s2.append(x.var(axis=1, ddof=1).mean())
mle, s2 = np.array(mle), np.array(s2)
i5 = list(ns).index(5)
assert abs(mle[i5] - 3.2) < 0.03 and abs(s2[i5] - 4) < 0.03
assert np.allclose(mle, (ns - 1) / ns * 4, atol=0.04) and np.allclose(s2, 4, atol=0.05)

fig = go.Figure()
fig.add_hline(y=4, line=dict(color=GREY, width=2, dash="dash"))
fig.add_annotation(x=20, y=4, text="true variance 4", xanchor="right", yshift=16, showarrow=False,
                   font=dict(color=GREY, size=20))
nn = np.linspace(2, 20, 200)
fig.add_trace(go.Scatter(x=nn, y=(nn - 1) / nn * 4, mode="lines", line=dict(color=ORANGE, width=2, dash="dot"),
                         name="theory (n − 1)/n × 4"))
fig.add_trace(go.Scatter(x=ns, y=s2, mode="markers", marker=dict(size=12, color=BLUE),
                         name="sample variance s² (divide by n − 1)"))
fig.add_trace(go.Scatter(x=ns, y=mle, mode="markers", marker=dict(size=12, color=ORANGE),
                         name="MLE variance (divide by n)"))
fig.add_annotation(x=5, y=mle[i5], text="n = 5: about 3.2", ax=40, ay=40, arrowhead=2, font=dict(size=20, color=ORANGE))
fig.update_layout(template="simple_white", width=950, height=580, font=dict(family="Latin Modern Roman", size=20),
                  xaxis=dict(title="sample size n", dtick=2), yaxis=dict(title="average over 100,000 samples", range=[1.5, 4.5]),
                  legend=dict(x=0.3, y=0.05, yanchor="bottom"), margin=dict(l=70, r=20, t=30, b=60))
fig.write_image(HERE / "bias_n.png", scale=2)
fig.write_image(HERE / "bias_n.pdf")
