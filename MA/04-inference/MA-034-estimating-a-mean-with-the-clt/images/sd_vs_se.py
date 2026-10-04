"""Standard deviation against standard error, on the Titanic fares (same samples as the Notebook, seed 42).
Row 1: the 50 fares of sample 1, with mean +- SD: the spread of single fares.
Row 2: the 100 sample means, with mean +- their SD: the spread of means, the standard error.
Row 3: 10,000 bootstrap means of sample 1 alone (resampled with replacement), with mean +- their SD.
Run: python sd_vs_se.py -> sd_vs_se.png, .pdf"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
data = HERE.parent / "data"
df = pd.concat([pd.read_csv(data / "titanic_train.csv").drop(columns="Survived"),
                pd.read_csv(data / "titanic_test.csv")]).sample(frac=1, random_state=42)
fare = df["Fare"].dropna()
rng = np.random.default_rng(42)
samples = np.array([fare.sample(50, random_state=rng).to_numpy() for _ in range(100)])
means = samples.mean(axis=1)
one = samples[0]
boot = np.random.default_rng(0).choice(one, size=(10_000, 50), replace=True).mean(axis=1)
sd, sem, sboot = one.std(ddof=1), means.std(ddof=1), boot.std(ddof=1)
assert round(one.mean(), 2) == 37.27 and round(sd, 2) == 51.34 and round(sem, 2) == 7.56
print(f"sample 1 SD {sd:.2f}; SD of 100 means {sem:.2f}; s/sqrt(50) {sd / np.sqrt(50):.2f}; "
      f"sigma/sqrt(50) {fare.std(ddof=0) / np.sqrt(50):.2f}; bootstrap SE {sboot:.2f}")

jit = np.random.default_rng(1)
rows = [(one, one.mean(), sd, BLUE, f"50 fares of one sample<br>SD = {sd:.2f}"),
        (means, means.mean(), sem, ORANGE, f"100 sample means<br>SD = SE = {sem:.2f}"),
        (boot[:400], boot.mean(), sboot, GREEN, f"bootstrap means of one sample<br>SD = {sboot:.2f}")]
fig = go.Figure()
for i, (vals, c, s, col, label) in enumerate(rows):
    y = 2 - i
    fig.add_scatter(x=vals, y=y + jit.uniform(-0.18, 0.18, len(vals)), mode="markers",
                    marker=dict(color=col, size=7, opacity=0.6), showlegend=False)
    fig.add_scatter(x=[c - s, c + s], y=[y - 0.32] * 2, mode="lines+markers", line=dict(color="black", width=4),
                    marker=dict(symbol="line-ns-open", size=16, color="black"), showlegend=False)
    fig.add_scatter(x=[c], y=[y - 0.32], mode="markers", marker=dict(color="black", size=11), showlegend=False)
fig.update_yaxes(tickvals=[2, 1, 0], ticktext=[r[4] for r in rows], range=[-0.6, 2.4], showline=False, ticks="")
fig.update_xaxes(range=[-20, 160], title_text="fare (pounds)", dtick=20)
fig.add_annotation(x=150, y=2, text=f"{int((one > 160).sum())} fares above 160<br>not shown", showarrow=False, font=dict(size=17, color=GREY))
fig.update_layout(template="simple_white", width=1050, height=480, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=20, r=20, t=20, b=55))
print("fares above 160 in sample 1:", int((one > 160).sum()))
fig.write_image(HERE / "sd_vs_se.png", scale=2)
fig.write_image(HERE / "sd_vs_se.pdf")
