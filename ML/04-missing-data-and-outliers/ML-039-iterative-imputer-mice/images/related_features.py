"""Plotly charts for Note ML-039, Sections 2 and 8.4: why MICE needs related features.
1. related_features: R&D vs Marketing for the 50 startups. A mean fill ignores R&D (flat line); a regression fill reads
   the gap off the sloped line, which follows the points (correlation 0.72).
2. imputer_error: the Notebook's 100-split test, real columns vs columns shuffled one by one (links broken).
Run: python related_features.py -> related_features.png/.pdf, imputer_error.png/.pdf"""
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer, KNNImputer, SimpleImputer
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")
here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=22)


def save(fig, name, width, height, bottom=70):
    fig.update_layout(template="simple_white", width=width, height=height, font=FONT,
                      margin=dict(l=90, r=30, t=40, b=bottom))
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


full = pd.read_csv(here.parent / "data" / "50_Startups.csv")
data = full[["R&D Spend", "Administration", "Marketing Spend"]] / 10000
x, y = data["R&D Spend"], data["Marketing Spend"]
r = x.corr(y)
assert round(r, 2) == 0.72

# 1. two ways to fill a Marketing gap: the mean (ignores R&D) or a line through the other startups
slope, intercept = np.polyfit(x, y, 1)
grid = np.array([0, x.max() * 1.02])
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(color=BLUE, size=11, opacity=0.75),
                         name="the 50 startups"))
fig.add_trace(go.Scatter(x=grid, y=[y.mean()] * 2, mode="lines", line=dict(color=ORANGE, width=4, dash="dash"),
                         name=f"mean fill: always {y.mean():.1f}"))
fig.add_trace(go.Scatter(x=grid, y=intercept + slope * grid, mode="lines", line=dict(color=GREEN, width=4),
                         name="regression fill: read off the line"))
fig.add_annotation(x=0.02, y=0.98, xref="paper", yref="paper", showarrow=False, xanchor="left",
                   text=f"correlation {r:.2f}", font=dict(size=26))
fig.update_xaxes(title="R&D spend (tens of thousands of dollars)")
fig.update_yaxes(title="Marketing spend (tens of thousands)")
fig.update_layout(legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.22))
save(fig, "related_features", 1000, 640, bottom=150)


# 2. the Notebook's test: 100 splits, 20% of values hidden, error of each imputer on real and on shuffled columns
def compare(d):
    imputers = {"Mean": SimpleImputer(), "KNN, k = 5": KNNImputer(), "Iterative": IterativeImputer(random_state=0)}
    sq_err = {name: [] for name in imputers}
    for seed in range(100):
        train, test = train_test_split(d, test_size=0.3, random_state=seed)
        rng = np.random.default_rng(seed)
        train_gaps = train.mask(rng.random(train.shape) < 0.2)
        test_gaps = test.mask(rng.random(test.shape) < 0.2)
        hidden = test_gaps.isna().values
        for name, imp in imputers.items():
            imp.fit(train_gaps)
            sq_err[name] += list((imp.transform(test_gaps) - test.values)[hidden] ** 2)
    return {name: round(np.sqrt(np.mean(e)), 2) for name, e in sq_err.items()}


real = compare(data)
rng = np.random.default_rng(0)
shuffled = compare(data.apply(lambda c: rng.permutation(c.values)))
assert list(real.values()) == [7.54, 6.69, 5.88], real
assert list(shuffled.values()) == [7.78, 8.64, 8.10], shuffled
fig = go.Figure()
for res, colour, name in [(real, BLUE, "real data (features related)"), (shuffled, GREY, "columns shuffled (links broken)")]:
    fig.add_trace(go.Bar(x=list(res), y=list(res.values()), marker_color=colour, name=name,
                         text=[f"{v:.2f}" for v in res.values()], textposition="outside", textfont=dict(size=22)))
fig.update_yaxes(title="error of the fills (lower is better)", range=[0, 10])
fig.update_layout(barmode="group", bargap=0.3, legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.15))
save(fig, "imputer_error", 1000, 560, bottom=130)
print("real", real, "shuffled", shuffled)
