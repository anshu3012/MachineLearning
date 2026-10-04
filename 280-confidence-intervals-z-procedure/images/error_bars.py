"""Mean Titanic fare per passenger class with 95% bootstrap confidence intervals as error bars (the interval seaborn
draws by default for an estimated mean: 10000 resamples, seed 0, middle 95% of the resampled means).
Training file, 891 passengers."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "titanic_train.csv")
names = {1: "first", 2: "second", 3: "third"}


def bootstrap_ci(x, n_boot=10000, seed=0):
    """Resample with replacement n_boot times, take each mean, keep the 2.5th to 97.5th percentile."""
    rng = np.random.default_rng(seed)
    boots = [x[rng.integers(0, len(x), len(x))].mean() for _ in range(n_boot)]
    return np.percentile(boots, [2.5, 97.5])


fig = go.Figure()
for cls, name in names.items():
    fare = df.loc[df.Pclass == cls, "Fare"].to_numpy(float)
    lo, hi = bootstrap_ci(fare)
    print(f"{name}: mean {fare.mean():.1f}, 95% CI {lo:.1f} to {hi:.1f}")
    fig.add_bar(x=[name], y=[fare.mean()], marker=dict(color="#4C78A8", opacity=0.6), width=0.8)
    fig.add_scatter(x=[name, name], y=[lo, hi], mode="lines", line=dict(color="black", width=3.5))
fig.update_xaxes(title="passenger class")
fig.update_yaxes(title="mean fare (pounds)", showgrid=True)
fig.update_layout(template="simple_white", width=600, height=400, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=19), margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(here / "error_bars.png", scale=2)
fig.write_image(here / "error_bars.pdf")
