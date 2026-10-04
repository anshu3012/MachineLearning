"""Three ranges for the mean Titanic fare against the true population mean, with how often each method caught
the true mean in 1000 repetitions (numbers from the Notebook)."""
from pathlib import Path
import plotly.graph_objects as go

here = Path(__file__).parent
TRUE = 33.30
rows = [  # label, centre, low, high, colour
    ("one sample of 50: x̄ ± 2s/√50<br>caught the mean 87.9% of the time", 37.27, 22.74, 51.79, "#4C78A8"),
    ("100 samples, ± 2 SE with √50 (wrong)<br>caught the mean 99.5% of the time", 31.87, 29.73, 34.00, "#E45756"),
    ("100 samples, ± 2 SE with √100<br>caught the mean 95.0% of the time", 31.87, 30.35, 33.38, "#54A24B"),
]
fig = go.Figure()
for i, (label, c, lo, hi, colour) in enumerate(rows):
    fig.add_scatter(x=[lo, hi], y=[i, i], mode="lines", line=dict(color=colour, width=8))
    fig.add_scatter(x=[c], y=[i], mode="markers", marker=dict(color="black", size=12))
    fig.add_annotation(x=hi, y=i, text=f"{lo:.2f} to {hi:.2f}", xanchor="left", xshift=10, showarrow=False,
                       font_size=20)
fig.add_vline(x=TRUE, line=dict(color="black", dash="dash", width=2))
fig.add_annotation(x=TRUE, y=2.55, text=f"true mean {TRUE}", showarrow=False, font_size=20, bgcolor="white")
fig.update_yaxes(tickvals=[0, 1, 2], ticktext=[r[0] for r in rows], range=[-0.5, 2.8])
fig.update_xaxes(range=[20, 60], title_text="mean fare (pounds)")
fig.update_layout(template="simple_white", width=1000, height=420, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=21), margin=dict(l=20, r=20, t=20, b=50))
fig.write_image(here / "fare_intervals.png", scale=2)
fig.write_image(here / "fare_intervals.pdf")
