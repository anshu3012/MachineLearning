"""Binomial versus Poisson (Plotly). Top: a binomial count is built from a fixed number of trials, here 10 trials
with success probability 0.6, each a box that is a success or not; the count cannot pass 10. Bottom: a Poisson
count has no trials, only events at random moments on a time line; we know the average, 4 a day, and count the
events that fall in each day. One simulated example of each, seeded."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, ORANGE

here = Path(__file__).parent
rng = np.random.default_rng(3)
trials = rng.random(10) < 0.6
days = 5
times = np.sort(rng.uniform(0, days, rng.poisson(4 * days)))     # 4 per day on average, at random moments
counts = np.histogram(times, bins=np.arange(days + 1))[0]
fig = make_subplots(2, 1, vertical_spacing=0.24,
                    subplot_titles=[f"binomial B(10, 0.6): 10 trials, {trials.sum()} successes (at most 10)",
                                    f"Poisson Po(4): no trials, events at random moments; counts per day {', '.join(map(str, counts))}"])
fig.update_annotations(font_size=22)
for i, ok in enumerate(trials):
    fig.add_shape(type="rect", x0=i + 0.1, x1=i + 0.9, y0=0, y1=1, row=1, col=1, line=dict(color=GREY, width=2),
                  fillcolor=ORANGE if ok else "white")
    fig.add_annotation(x=i + 0.5, y=0.5, text="✓" if ok else "✗", showarrow=False, font=dict(size=26), row=1, col=1)
    fig.add_annotation(x=i + 0.5, y=-0.35, text=f"trial {i + 1}", showarrow=False, font=dict(size=16), row=1, col=1)
fig.add_trace(go.Scatter(x=[None], y=[None]), 1, 1)
fig.add_trace(go.Scatter(x=times, y=np.full_like(times, 0.5), mode="markers",
                         marker=dict(symbol="line-ns", size=36, line=dict(width=4, color=BLUE))), 2, 1)
for d in range(days + 1):
    fig.add_vline(x=d, line=dict(color=GREY, width=2, dash="dot"), row=2, col=1)
for d in range(days):
    fig.add_annotation(x=d + 0.5, y=1.25, text=f"day {d + 1}: <b>{counts[d]}</b>", showarrow=False, font=dict(size=20),
                       row=2, col=1)
fig.update_xaxes(visible=False, range=[0, 10], row=1, col=1)
fig.update_yaxes(visible=False, range=[-0.6, 1.1], row=1, col=1)
fig.update_xaxes(title="time (days)", range=[0, days], row=2, col=1)
fig.update_yaxes(visible=False, range=[0, 1.5], row=2, col=1)
fig.update_layout(template="simple_white", width=1200, height=500, font=FONT, showlegend=False,
                  margin=dict(l=30, r=30, t=60, b=70))
fig.write_image(here / "trials_vs_rate.png", scale=2)
