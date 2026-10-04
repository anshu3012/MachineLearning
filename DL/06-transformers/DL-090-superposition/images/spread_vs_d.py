"""Section 4: the measured spread of the angle between random directions (20,000 pairs per dimension) against the
prediction 57.3 / sqrt(d) degrees, and the share of pairs within 5 degrees of perpendicular
(data/random_angles_summary.csv, Notebook). Plotly, log axis for d."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, RED, GREY, FONT

here = Path(__file__).parent
R = pd.read_csv(here.parent / "data" / "random_angles_summary.csv")
assert R.set_index("d").loc[100, "angle_std_deg"].round(2) == 5.75 and R.set_index("d").loc[1000, "share_85_95"].round(2) == 0.99
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=("spread of the angle (degrees)", "pairs within 5 degrees of 90"))
dd = np.logspace(np.log10(2), np.log10(12288), 100)
fig.add_scatter(x=dd, y=57.3 / np.sqrt(dd), mode="lines", line=dict(color=GREY, dash="dash", width=3), name="57.3 / √d", row=1, col=1)
fig.add_scatter(x=R.d, y=R.angle_std_deg, mode="markers", marker=dict(size=12, color=BLUE), name="measured", row=1, col=1)
fig.add_scatter(x=R.d, y=100 * R.share_85_95, mode="lines+markers", line=dict(color=RED, width=3), marker=dict(size=10),
                showlegend=False, text=[f"{100 * v:.0f}%" for v in R.share_85_95], textposition="top left", row=1, col=2)
for c in (1, 2):
    fig.update_xaxes(type="log", title="dimension d", tickvals=[2, 10, 100, 1000, 12288], ticktext=["2", "10", "100", "1,000", "12,288"], row=1, col=c)
fig.update_yaxes(title="percent of pairs", range=[0, 105], row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=430, font=dict(FONT, size=18),
                  legend=dict(x=0.25, y=0.95), margin=dict(l=60, r=20, t=50, b=70))
fig.write_image(here / "spread_vs_d.png", scale=2)
fig.write_image(here / "spread_vs_d.pdf")
