"""Learning rate in online learning: how fast a model follows a value that changes.
Simulation: each step the model moves a fraction (the learning rate) of the way towards the newest data point."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"


def simulate(rate, steps=300, seed=0):
    rng = np.random.default_rng(seed)
    truth = np.where(np.arange(steps) < 120, 20.0, 60.0)          # the real-world value jumps at step 120
    data = truth + rng.normal(0, 8, steps)                          # what we observe: noisy
    estimate = np.empty(steps)
    m = data[0]
    for t, x in enumerate(data):
        m = m + rate * (x - m)                                      # online update
        estimate[t] = m
    return truth, data, estimate


if __name__ == "__main__":
    fig = go.Figure()
    truth, data, _ = simulate(0.1)
    t = np.arange(len(truth))
    fig.add_trace(go.Scatter(x=t, y=data, mode="markers", marker=dict(color=GREY, size=4, opacity=0.35), name="incoming data"))
    fig.add_trace(go.Scatter(x=t, y=truth, mode="lines", line=dict(color="black", width=2, dash="dash"), name="true value"))
    for rate, colour, label in [(0.01, BLUE, "learning rate 0.01: too slow"),
                                (0.1, GREEN, "learning rate 0.1: balanced"),
                                (0.7, RED, "learning rate 0.7: too jumpy")]:
        fig.add_trace(go.Scatter(x=t, y=simulate(rate)[2], mode="lines", line=dict(color=colour, width=3), name=label))
    fig.add_vline(x=120, line=dict(color=GREY, width=2, dash="dot"))
    fig.add_annotation(x=122, y=82, xanchor="left", text="the world changes", showarrow=False, font=dict(size=16, color=GREY))
    fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=17),
                      title=dict(text="How the learning rate changes what an online model learns", x=0.5),
                      xaxis_title="Time (new data points)", yaxis_title="Value", yaxis_range=[-5, 85],
                      legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.85)"), margin=dict(l=70, r=30, t=70, b=60))
    fig.write_image(here / "learning_rate.png", scale=2)
    fig.write_image(here / "learning_rate.pdf")
