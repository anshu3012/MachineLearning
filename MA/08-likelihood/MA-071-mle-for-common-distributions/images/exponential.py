"""Exponential distribution: left, the PDF for rates 0.5, 1 and 2; right, the likelihood of the rate for the three
waiting times 2, 2.5 and 1.5 seconds, highest at lambda = 3 / 6 = 0.5."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
data = np.array([2, 2.5, 1.5])
lik = lambda lam: (lam * np.exp(-lam * data)).prod()
lam = np.linspace(0.02, 2.2, 400)
L = np.array([lik(l) for l in lam])
assert abs(lam[L.argmax()] - 0.5) < 0.01

fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.14,
                    subplot_titles=("PDF f(x) = λe<sup>−λx</sup>", "likelihood of λ for x = 2, 2.5, 1.5"))
x = np.linspace(0, 6, 300)
for l, c in ((0.5, GREEN), (1, BLUE), (2, RED)):
    fig.add_trace(go.Scatter(x=x, y=l * np.exp(-l * x), mode="lines", line=dict(color=c, width=4), name=f"λ = {l}"), 1, 1)
    fig.add_trace(go.Scatter(x=[l], y=[lik(l)], mode="markers", marker=dict(size=14, color=c), showlegend=False), 1, 2)
fig.add_trace(go.Scatter(x=data, y=np.zeros(3), mode="markers", marker=dict(size=13, color="black"), name="data"), 1, 1)
fig.add_trace(go.Scatter(x=lam, y=L, mode="lines", line=dict(color=GREY, width=3), showlegend=False), 1, 2)
fig.add_vline(x=0.5, line=dict(color=GREEN, dash="dash", width=2), row=1, col=2)
fig.add_annotation(x=0.5, y=0.0066, text="MLE: λ = 0.5", showarrow=False, xanchor="left", xshift=8, row=1, col=2)
fig.update_xaxes(title_text="waiting time x (seconds)", row=1, col=1)
fig.update_yaxes(title_text="density", range=[0, 2.05], row=1, col=1)
fig.update_xaxes(title_text="rate λ (events per second)", row=1, col=2)
fig.update_yaxes(title_text="likelihood", range=[0, 0.0072], row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=500, font=dict(family="Latin Modern Roman", size=20),
                  legend=dict(x=0.2, y=0.98), margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font_size=21)
fig.write_image(HERE / "exponential.png", scale=2)
fig.write_image(HERE / "exponential.pdf")
