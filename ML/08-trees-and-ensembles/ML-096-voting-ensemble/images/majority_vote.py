"""Majority-vote accuracy: (a) against the number of independent models, for several single-model accuracies
(exact binomial lines, simulation dots for p = 0.6); (b) against how correlated the models are (Plotly)."""
from math import comb
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
COL = {0.3: "#E45756", 0.5: "#6B6B6B", 0.6: "#4C78A8", 0.7: "#54A24B"}
rng = np.random.default_rng(0)


def exact(p, n):
    """P(more than half of n independent models are right), each right with probability p (n odd)."""
    return sum(comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(n // 2 + 1, n + 1))


def simulate(p, n, rho=0.0, trials=20_000):
    """Simulated majority accuracy. With probability rho a model copies one shared answer, else answers on its own;
    either way each model is right with probability p."""
    shared = rng.random(trials) < p
    own = rng.random((trials, n)) < p
    copy = rng.random((trials, n)) < rho
    right = np.where(copy, shared[:, None], own)
    return (right.sum(1) > n // 2).mean()


ns = list(range(1, 102, 2))
fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=(
    "(a) independent models: accuracy of the vote", "(b) 11 models of accuracy 0.7: effect of correlation"))
for p, c in COL.items():
    fig.add_trace(go.Scatter(x=ns, y=[exact(p, n) for n in ns], mode="lines", line=dict(color=c, width=3),
                             name=f"each model {p}"), 1, 1)
sim_n = [1, 3, 5, 11, 21, 41, 61, 81, 101]
fig.add_trace(go.Scatter(x=sim_n, y=[simulate(0.6, n) for n in sim_n], mode="markers", name="simulation (0.6)",
                         marker=dict(color="white", size=10, line=dict(color="#4C78A8", width=2.5))), 1, 1)
for n in (3, 11, 101):
    print(f"n={n}: p=0.7 -> {exact(0.7, n):.3f}, p=0.6 -> {exact(0.6, n):.3f}, p=0.3 -> {exact(0.3, n):.3f}")

rhos = np.linspace(0, 1, 21)
acc = [simulate(0.7, 11, r) for r in rhos]
print("correlation 0 ->", round(acc[0], 3), " 0.5 ->", round(acc[10], 3), " 1 ->", round(acc[-1], 3))
fig.add_trace(go.Scatter(x=rhos, y=acc, mode="lines+markers", line=dict(color="#54A24B", width=3),
                         marker=dict(size=7), showlegend=False), 1, 2)
fig.add_trace(go.Scatter(x=[0, 1], y=[0.7, 0.7], mode="lines", line=dict(color="#6B6B6B", dash="dash"), showlegend=False), 1, 2)
fig.add_annotation(x=0.25, y=0.715, xref="x2", yref="y2", text="one model alone: 0.7", showarrow=False,
                   yanchor="bottom", font=dict(size=16, color="#6B6B6B"))
fig.update_xaxes(title="number of models (odd)", row=1, col=1)
fig.update_xaxes(title="share of answers copied from a common source", row=1, col=2)
fig.update_yaxes(title="accuracy of the majority vote", range=[0, 1.02], row=1, col=1)
fig.update_yaxes(range=[0.6, 1.0], row=1, col=2)
fig.update_annotations(font_size=19)
fig.update_layout(template="simple_white", width=1300, height=560, font=dict(family="Latin Modern Roman", size=16),
                  legend=dict(x=0.22, y=0.44, yanchor="top", bordercolor="#999", borderwidth=1), margin=dict(l=70, r=20, t=60, b=60))
fig.write_image(HERE / "majority_vote.png", scale=2)
fig.write_image(HERE / "majority_vote.pdf")
