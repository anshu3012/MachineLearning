"""Shapiro-Wilk depends on n. Normal Q-Q plots of our random sample of 25 Titanic ages (random_state=0, p = 0.299)
and of all 1046 known ages (p = 6e-11): the bend in the tails is similar, but only the large sample is rejected."""
from pathlib import Path

import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
data = here.parent / "data"
ages = pd.concat([pd.read_csv(data / "titanic_train.csv"), pd.read_csv(data / "titanic_test.csv")]).Age.dropna() \
    .reset_index(drop=True)
sample = ages.sample(25, random_state=0)
p_s, p_all = stats.shapiro(sample).pvalue, stats.shapiro(ages).pvalue
assert len(ages) == 1046 and round(p_s, 3) == 0.299 and round(p_all * 1e11) == 6, (p_s, p_all)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=[f"sample of 25: p = {p_s:.3f}<br>fail to reject normality",
                                    "all 1046: p = 6 × 10⁻¹¹<br>reject normality"])
for col, (v, c) in enumerate(((sample, "#F58518"), (ages, "#4C78A8")), start=1):
    (q, y), (slope, icpt, _) = stats.probplot(v, dist="norm")
    fig.add_scatter(x=q, y=y, mode="markers", marker=dict(size=9 if col == 1 else 5, color=c), row=1, col=col)
    fig.add_scatter(x=q[[0, -1]], y=icpt + slope * q[[0, -1]], mode="lines", line=dict(color="black", width=2.5),
                    row=1, col=col)
fig.update_xaxes(title_text="normal quantile")
fig.update_yaxes(title_text="age (years)", row=1, col=1)
fig.update_layout(template="simple_white", width=1000, height=480, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=70, r=20, t=90, b=60))
for a in fig.layout.annotations:
    a.font.size = 22
fig.write_image(here / "qq_two_sizes.png", scale=2)
fig.write_image(here / "qq_two_sizes.pdf")
