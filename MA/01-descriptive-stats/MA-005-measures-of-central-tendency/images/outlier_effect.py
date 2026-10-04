"""Mean, median and 10% trimmed mean of a class's monthly salaries, before and after one very high earner joins."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
nine = np.array([28, 30, 31, 32, 33, 35, 36, 38, 40])      # thousand rupees a month
ten = np.append(nine, 2000)                                 # plus a founder earning 20 lakh a month
groups = ["9 students", "9 students + founder"]
measures = {"mean": ([nine.mean(), ten.mean()], "#E45756"),
            "median": ([np.median(nine), np.median(ten)], "#4C78A8"),
            "10% trimmed mean": ([stats.trim_mean(nine, 0.1), stats.trim_mean(ten, 0.1)], "#54A24B")}
fig = go.Figure()
for name, (vals, colour) in measures.items():
    fig.add_bar(name=name, x=groups, y=vals, marker_color=colour, text=[f"{v:.1f}" for v in vals],
                textposition="outside", textfont=dict(size=17))
fig.update_layout(barmode="group", template="simple_white", width=900, height=480,
                  font=dict(family="Latin Modern Roman", size=17),
                  yaxis=dict(title="thousand rupees a month", range=[0, 265]),
                  legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"), margin=dict(l=70, r=20, t=50, b=50))
fig.write_image(here / "outlier_effect.png", scale=2)
fig.write_image(here / "outlier_effect.pdf")
