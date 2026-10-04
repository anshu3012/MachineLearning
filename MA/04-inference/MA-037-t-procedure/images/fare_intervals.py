"""Section 8: the case study's intervals for the mean Titanic fare against the true mean 33.30 (Notebook seed 42):
one sample of 30 at 95% and 50%, ten samples of 30 combined the wrong way (average s, n = 30) and pooled (n = 300)."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import stats

here = Path(__file__).parent
data = here.parent / "data"
df = pd.concat([pd.read_csv(data / "titanic_train.csv").drop(columns="Survived"),
                pd.read_csv(data / "titanic_test.csv")])
fares = df["Fare"].dropna().to_numpy()
true = fares.mean()
sample = np.random.default_rng(42).choice(fares, 30, replace=False)
xb, s = sample.mean(), sample.std(ddof=1)
rows = [("one sample of 30, 95%", stats.t.interval(0.95, 29, loc=xb, scale=s / np.sqrt(30)), "#4C78A8"),
        ("one sample of 30, 50%", stats.t.interval(0.50, 29, loc=xb, scale=s / np.sqrt(30)), "#B279A2")]
rng = np.random.default_rng(42)
ten = np.array([rng.choice(fares, 30, replace=False) for _ in range(10)])
am, as_ = ten.mean(axis=1).mean(), ten.std(axis=1, ddof=1).mean()
pooled = ten.ravel()
rows += [("10 samples, averaged s, n = 30 (wrong)", (am - 2.045 * as_ / np.sqrt(30), am + 2.045 * as_ / np.sqrt(30)),
          "#E45756"),
         ("10 samples pooled, n = 300", stats.t.interval(0.95, 299, loc=pooled.mean(),
                                                         scale=pooled.std(ddof=1) / np.sqrt(300)), "#54A24B")]
got = [f"{a:.2f} to {b:.2f}" for _, (a, b), _ in rows]
assert got == ["18.57 to 55.72", "30.94 to 43.35", "14.29 to 48.55", "26.20 to 36.64"], got
assert round(true, 2) == 33.30
fig = go.Figure()
for i, (name, (a, b), c) in enumerate(rows):
    y = len(rows) - i
    fig.add_scatter(x=[a, b], y=[y, y], mode="lines+markers", line=dict(color=c, width=10), showlegend=False,
                    marker=dict(symbol="line-ns", size=24, line=dict(width=3, color=c)))
    fig.add_annotation(x=(a + b) / 2, y=y + 0.33, text=f"{name}: {a:.2f} to {b:.2f}", showarrow=False,
                       font=dict(size=19, color=c), bgcolor="white")
fig.add_vline(x=true, line=dict(color="black", width=2.5, dash="dash"))
fig.add_annotation(x=true, y=4.75, text="true mean 33.30", showarrow=False, xanchor="left", xshift=6,
                   font=dict(size=19))
fig.update_layout(template="simple_white", width=1000, height=560, font=dict(family="Latin Modern Roman", size=19),
                  xaxis=dict(title="mean fare (pounds)", range=[10, 60]), yaxis=dict(visible=False, range=[0.5, 4.95]),
                  margin=dict(l=30, r=20, t=20, b=60))
fig.write_image(here / "fare_intervals.png", scale=2)
fig.write_image(here / "fare_intervals.pdf")
