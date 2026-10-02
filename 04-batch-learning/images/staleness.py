"""A batch model gets stale between retrains: performance drifts down, jumps back at each retrain.
Concept curve, not measurements."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
BLUE, GREEN, GREY = "#4C78A8", "#54A24B", "#6B6B6B"


def performance(days, retrain_every, decay=0.012, start=0.92):
    """Performance drops a little each day since the last retrain, then resets."""
    since = np.mod(days, retrain_every)
    return start - decay * since


def staleness_figure(retrain_every=7):
    days = np.linspace(0, 28, 2000)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=performance(days, retrain_every), mode="lines",
                             line=dict(color=BLUE, width=4), name="model performance"))
    for d in np.arange(retrain_every, 28, retrain_every):
        fig.add_vline(x=d, line=dict(color=GREEN, width=2, dash="dot"))
    fig.add_annotation(x=retrain_every, y=0.95, text="retrain", showarrow=False, font=dict(color=GREEN, size=16))
    fig.update_layout(template="simple_white", width=950, height=450, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=18),
                      title=dict(text=f"A batch model gets stale between retrains (retrain every {retrain_every} days)", x=0.5),
                      xaxis=dict(title="Days since deployment"), yaxis=dict(title="Performance", range=[0.78, 0.97],
                                                                            showticklabels=False, ticks=""),
                      margin=dict(l=70, r=30, t=70, b=60))
    fig.add_annotation(x=28, y=0.785, xanchor="right", showarrow=False, text="illustration, not real measurements",
                       font=dict(size=13, color=GREY))
    return fig


if __name__ == "__main__":
    fig = staleness_figure(7)
    fig.write_image(here / "staleness.png", scale=2)
    fig.write_image(here / "staleness.pdf")
