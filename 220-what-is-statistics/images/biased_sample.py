"""Section 4.1: why a sample must be random. Population: the 891 Titanic fares, mean 32.2. Grey: the means of 1,000
random samples of 50 passengers (seed 0), which centre on 32.2. Red: one biased sample of 50 passengers drawn only from
first class, whose mean is far too high. Plotly."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=18)
d = pd.read_csv(here.parent / "data" / "titanic_train.csv")
fare = d.Fare.to_numpy()
rng = np.random.default_rng(0)
means = np.array([rng.choice(fare, 50, replace=False).mean() for _ in range(1000)])
first = d.loc[d.Pclass == 1, "Fare"].to_numpy()
biased = rng.choice(first, 50, replace=False).mean()
mu = fare.mean()
assert round(mu, 1) == 32.2 and abs(means.mean() - mu) < 1 and biased > 60
fig = go.Figure(go.Histogram(x=means, xbins=dict(size=2), marker_color="#BBBBBB", name="1,000 random samples of 50"))
fig.add_vline(x=mu, line=dict(color="#4C78A8", width=3), opacity=1)
fig.add_annotation(x=mu, y=1, yref="paper", text=f"population mean μ = {mu:.1f}", showarrow=False, xanchor="left", xshift=6,
                   font=dict(color="#4C78A8", size=17))
fig.add_vline(x=biased, line=dict(color="#E45756", width=3, dash="dash"), opacity=1)
fig.add_annotation(x=biased, y=0.85, yref="paper", text=f"first-class-only sample: {biased:.1f}", showarrow=False, xanchor="right",
                   xshift=-6, font=dict(color="#E45756", size=17))
fig.update_layout(template="simple_white", width=1000, height=440, font=FONT, showlegend=False,
                  xaxis=dict(title="sample mean of 50 fares", range=[0, 110]), yaxis=dict(title="number of samples"),
                  margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "biased_sample.png", scale=2)
fig.write_image(here / "biased_sample.pdf")
print(round(biased, 1), round(means.std(), 1))
