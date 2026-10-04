"""Section 5.1: the estimate 31.87 follows a normal curve with standard error 0.756; ranges of 1, 2 and 3 standard
errors around it, against the true mean fare 33.30. Same sampling as the Notebook (seed 42)."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
data = here.parent / "data"
df = pd.concat([pd.read_csv(data / "titanic_train.csv").drop(columns="Survived"),
                pd.read_csv(data / "titanic_test.csv")]).sample(frac=1, random_state=42)
fare = df["Fare"].dropna()
rng = np.random.default_rng(42)
means = np.array([fare.sample(50, random_state=rng).to_numpy() for _ in range(100)]).mean(axis=1)
est, se, true = means.mean(), means.std(ddof=1) / 10, fare.mean()
R = {k: (est - k * se, est + k * se) for k in (1, 2, 3)}
assert [f"{a:.2f} to {b:.2f}" for a, b in R.values()] == ["31.11 to 32.62", "30.35 to 33.38", "29.60 to 34.13"]
assert round(se, 3) == 0.756 and round(true, 2) == 33.30
COL = {1: "#E45756", 2: "#4C78A8", 3: "#54A24B"}
x = np.linspace(28.8, 35, 600)
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.06, row_heights=[0.55, 0.45])
d = stats.norm(est, se)
for k, alpha in [(3, 0.15), (2, 0.28), (1, 0.42)]:
    xs = x[np.abs(x - est) <= k * se]
    fig.add_scatter(x=xs, y=d.pdf(xs), fill="tozeroy", fillcolor=f"rgba(76,120,168,{alpha})", mode="lines",
                    line=dict(width=0), showlegend=False, row=1, col=1)
fig.add_scatter(x=x, y=d.pdf(x), mode="lines", line=dict(color="black", width=3), showlegend=False, row=1, col=1)
fig.add_annotation(x=est, y=0.6, text="where the estimate lands:<br>normal, centre 31.87, SE 0.756", showarrow=False,
                   font=dict(size=18), bgcolor="rgba(255,255,255,0.8)", row=1, col=1)
for k, share, y in [(1, "68%", 3), (2, "95%", 2), (3, "99.7%", 1)]:
    a, b = R[k]
    hit = a <= true <= b
    fig.add_scatter(x=[a, b], y=[y, y], mode="lines+markers", line=dict(color=COL[k], width=9),
                    marker=dict(symbol="line-ns", size=22, line=dict(width=3, color=COL[k])), showlegend=False,
                    row=2, col=1)
    fig.add_annotation(x=b + 0.06, y=y, xanchor="left", showarrow=False, font=dict(size=18, color=COL[k]),
                       text=f"±{k} SE ({share})", row=2, col=1)
    fig.add_annotation(x=(a + b) / 2, y=y + 0.42, showarrow=False, font=dict(size=18, color=COL[k]),
                       text=f"{a:.2f} to {b:.2f}: {'contains' if hit else 'misses'} 33.30", row=2, col=1)
for row in (1, 2):
    fig.add_vline(x=true, line=dict(color="black", width=2.5, dash="dash"), row=row, col=1)
fig.add_annotation(x=true, y=0.98, yref="paper", text="true mean 33.30", showarrow=False, xanchor="left",
                   font=dict(size=18))
fig.update_yaxes(title_text="density", row=1, col=1)
fig.update_yaxes(visible=False, range=[0.5, 3.75], row=2, col=1)
fig.update_xaxes(title_text="mean fare (pounds)", range=[28.8, 35], row=2, col=1)
fig.update_layout(template="simple_white", width=1000, height=640, font=dict(family="Latin Modern Roman", size=18),
                  margin=dict(l=70, r=20, t=30, b=55))
fig.write_image(here / "ranges.png", scale=2)
fig.write_image(here / "ranges.pdf")
