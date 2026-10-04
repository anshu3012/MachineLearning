"""Estimated PMFs from 10,000 simulated rolls (bars) against the exact PMFs (dots); same seed as the Notebook."""
from pathlib import Path
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots

here = Path(__file__).parent
rng = np.random.default_rng(42)
one = pd.Series(rng.integers(1, 7, 10_000)).value_counts(normalize=True).sort_index()
two = pd.Series(rng.integers(1, 7, 10_000) + rng.integers(1, 7, 10_000)).value_counts(normalize=True).sort_index()
x2 = np.arange(2, 13)
fig = make_subplots(rows=1, cols=2, column_widths=[0.38, 0.62], horizontal_spacing=0.09,
                    subplot_titles=["One die", "Sum of two dice"])
fig.add_bar(x=one.index, y=one.values, marker_color="#4C78A8", name="simulated (10,000 rolls)", row=1, col=1)
fig.add_scatter(x=np.arange(1, 7), y=np.full(6, 1 / 6), mode="markers", name="exact",
                marker=dict(color="#F58518", size=13, symbol="diamond"), row=1, col=1)
fig.add_bar(x=two.index, y=two.values, marker_color="#4C78A8", showlegend=False, row=1, col=2)
fig.add_scatter(x=x2, y=(6 - np.abs(x2 - 7)) / 36, mode="markers", showlegend=False,
                marker=dict(color="#F58518", size=13, symbol="diamond"), row=1, col=2)
fig.update_xaxes(dtick=1)
fig.update_xaxes(title_text="face x", row=1, col=1)
fig.update_xaxes(title_text="sum x", row=1, col=2)
fig.update_yaxes(title_text="probability", range=[0, 0.2], row=1, col=1)
fig.update_yaxes(range=[0, 0.2], row=1, col=2)
fig.update_annotations(font_size=20)
fig.update_layout(template="simple_white", width=1100, height=480, bargap=0.3,
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.22),
                  font=dict(family="Latin Modern Roman", size=18), margin=dict(l=60, r=20, t=50, b=40))
fig.write_image(here / "pmf_simulated.png", scale=2)
fig.write_image(here / "pmf_simulated.pdf")
