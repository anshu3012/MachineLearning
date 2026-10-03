"""Why the sample variance divides by n - 1: average of many sample variances, dividing by n or by n - 1,
against the true variance of a population (the 714 known Titanic ages)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
ages = pd.read_csv(here.parent / "data" / "titanic_train.csv")["Age"].dropna().to_numpy()
true_var = ages.var()                                   # population variance: divide by N
rng = np.random.default_rng(0)
sizes = np.arange(2, 21)
by_n, by_n1 = [], []
for n in sizes:
    samples = rng.choice(ages, size=(20_000, n))       # 20,000 random samples of size n
    by_n.append(samples.var(axis=1, ddof=0).mean())    # divide by n
    by_n1.append(samples.var(axis=1, ddof=1).mean())   # divide by n - 1
fig = go.Figure()
fig.add_hline(y=true_var, line=dict(color="#6B6B6B", dash="dash", width=2))
fig.add_annotation(x=2, y=true_var, text=f"true population variance = {true_var:.0f}", showarrow=False,
                   xanchor="left", yshift=20, font=dict(size=17, color="#6B6B6B"))
fig.add_scatter(x=sizes, y=by_n1, name="divide by n - 1", mode="lines+markers",
                line=dict(color="#54A24B", width=3), marker=dict(size=8))
fig.add_scatter(x=sizes, y=by_n, name="divide by n", mode="lines+markers",
                line=dict(color="#E45756", width=3), marker=dict(size=8))
fig.update_layout(template="simple_white", width=950, height=480, font=dict(family="Latin Modern Roman", size=17),
                  xaxis=dict(title="sample size n", dtick=2), yaxis=dict(title="average sample variance (years²)",
                  range=[0, 250]), legend=dict(x=0.62, y=0.25), margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(here / "bessel.png", scale=2)
fig.write_image(here / "bessel.pdf")
