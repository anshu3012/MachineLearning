"""Running share of heads over 100,000 tosses, three runs (seeds 0, 1, 2 as in the Notebook), log x axis (Plotly)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
n = 100_000
steps = np.arange(1, n + 1)
keep = np.unique(np.logspace(0, 5, 600).astype(int)) - 1
colours = ["#4C78A8", "#F58518", "#54A24B"]
fig = go.Figure()
for seed, c in zip([0, 1, 2], colours):
    running = np.random.default_rng(seed).integers(0, 2, n).cumsum() / steps
    fig.add_scatter(x=steps[keep], y=running[keep], mode="lines", line=dict(color=c, width=2.5), name=f"run {seed + 1}")
    print(seed, [round(running[k - 1], 3) for k in (10, 100, 1000, 100_000)])
fig.add_hline(y=0.5, line_dash="dash", line_color="#6B6B6B",
              annotation_text="theoretical 0.5", annotation_position="top right", annotation_font_size=22)
fig.update_xaxes(type="log", range=[0, 5.08], title="number of tosses (log scale)", tickvals=[1, 10, 100, 1000, 10_000, 100_000],
                 ticktext=["1", "10", "100", "1,000", "10,000", "100,000"])
fig.update_yaxes(range=[0, 1], title="share of heads so far", dtick=0.25)
fig.update_layout(template="simple_white", width=950, height=480, font=dict(family="Latin Modern Roman", size=22),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=1.12),
                  margin=dict(l=70, r=50, t=60, b=60))
fig.write_image(here / "convergence.png", scale=2)
fig.write_image(here / "convergence.pdf")
