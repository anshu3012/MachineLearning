"""More data gives better parameter estimates: samples of 10, 30, 100 and 1,000 values from a normal distribution
with mean 50 and standard deviation 5, each with its fitted normal PDF (orange) against the true PDF (dashed).
The 1,000-value sample is the Note's (seed 42); smaller samples are its first n values. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from anim import save_gif, FONT, BLUE, ORANGE

here = Path(__file__).parent
sample = np.random.default_rng(42).normal(50, 5, 1000)
assert round(sample.mean(), 2) == 49.86 and round(sample.std(), 2) == 4.94      # the Note's estimates
x = np.linspace(30, 70, 300)
true = stats.norm(50, 5).pdf(x)


def frame(n):
    s = sample[:n]
    m, sd = s.mean(), s.std()
    fig = go.Figure()
    fig.add_histogram(x=s, histnorm="probability density", xbins=dict(start=30, end=70, size=2.5),
                      marker_color="rgba(76,120,168,0.4)", name="sample (density histogram)")
    fig.add_scatter(x=x, y=true, mode="lines", line=dict(color="black", dash="dash", width=3), name="true PDF: μ = 50, σ = 5")
    fig.add_scatter(x=x, y=stats.norm(m, sd).pdf(x), mode="lines", line=dict(color=ORANGE, width=4),
                    name=f"fitted PDF: x̄ = {m:.2f}, s = {sd:.2f}")
    fig.update_layout(template="simple_white", width=1000, height=640, font=FONT, bargap=0.05,
                      title=dict(text=f"<b>n = {n:,}</b> values: estimates x̄ = {m:.2f}, s = {sd:.2f}", x=0.5),
                      xaxis=dict(title="value", range=[30, 70]), yaxis=dict(title="density", range=[0, 0.16]),
                      legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.8)"), margin=dict(l=90, r=30, t=80, b=80))
    return fig


if __name__ == "__main__":
    save_gif([frame(n) for n in (10, 30, 100, 1000)], "more_data", here, keys=[0, 1, 2, 3], fps=1, holds=[3, 3, 3, 6])
