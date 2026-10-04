"""Section 7: 2000 one-sample ranges x_bar +- 2 s / sqrt(50) on the Titanic fares (seeds 5000 + r, as in the
Notebook). Each sample is a point (x_bar, s). The range catches the true mean exactly when the point lies above the
V-shaped line s = |x_bar - mu| sqrt(50) / 2. Misses pile up low and to the left: samples without the rare expensive
tickets have both x_bar and s too small."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
data = here.parent / "data"
df = pd.concat([pd.read_csv(data / "titanic_train.csv").drop(columns="Survived"),
                pd.read_csv(data / "titanic_test.csv")]).sample(frac=1, random_state=42)
F = df["Fare"].dropna().to_numpy()
mu = F.mean()
xs, ss, big = [], [], []
for r in range(2000):
    one = np.random.default_rng(5000 + r).choice(F, 50, replace=False)
    xs.append(one.mean()); ss.append(one.std(ddof=1)); big.append((one > 200).any())
xs, ss, big = np.array(xs), np.array(ss), np.array(big)
miss = abs(xs - mu) > 2 * ss / np.sqrt(50)
assert miss.sum() == 221 and (miss & (xs < mu)).sum() == 218
assert round(100 * miss[~big].mean(), 1) == 44.6 and round(100 * miss[big].mean(), 1) == 1.2
assert round(np.corrcoef(xs, ss)[0, 1], 2) == 0.86
fig = go.Figure()
groups = [(~miss & ~big, "#4C78A8", "circle-open", "caught, no fare above 200"),
          (~miss & big, "#4C78A8", "circle", "caught, a fare above 200"),
          (miss & ~big, "#E45756", "circle-open", "missed, no fare above 200"),
          (miss & big, "#E45756", "circle", "missed, a fare above 200")]
for m, c, sym, name in groups:
    fig.add_scatter(x=xs[m], y=ss[m], mode="markers", name=f"{name} ({m.sum()})",
                    marker=dict(color=c, symbol=sym, size=7, line=dict(width=1.3, color=c)), opacity=0.75)
vx = np.linspace(0, 100, 400)
fig.add_scatter(x=vx, y=np.abs(vx - mu) * np.sqrt(50) / 2, mode="lines", name="edge: range just reaches μ",
                line=dict(color="black", width=3, dash="dash"))
fig.add_vline(x=mu, line=dict(color="#6B6B6B", width=1.5, dash="dot"))
fig.add_annotation(x=mu, y=150, text="true mean 33.30", showarrow=False, xanchor="left", font=dict(size=18))
fig.update_layout(template="simple_white", width=1000, height=680, font=dict(family="Latin Modern Roman", size=19),
                  xaxis=dict(title="sample mean x̄ (pounds)", range=[5, 75]),
                  yaxis=dict(title="sample standard deviation s (pounds)", range=[0, 160]),
                  legend=dict(x=0.6, y=0.0, yanchor="bottom", font=dict(size=16), bgcolor="rgba(255,255,255,0.85)"),
                  title=dict(text=f"{miss.sum()} of 2000 ranges miss; {(miss & (xs < mu)).sum()} of them lie left of μ",
                             x=0.5), margin=dict(l=80, r=20, t=60, b=60))
fig.write_image(here / "one_sample_wedge.png", scale=2)
fig.write_image(here / "one_sample_wedge.pdf")
