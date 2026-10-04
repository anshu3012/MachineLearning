"""Still charts for Note ML-023 (Social Network Ads, training set): scatter, KDE and outliers, before vs after StandardScaler.
Plotly; KDE curves are scipy's gaussian_kde (Scott's bandwidth), drawn 3 bandwidths past the data on each side."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

here = Path(__file__).parent
BLUE, ORANGE, RED = "#4C78A8", "#F58518", "#E45756"
STAGES = ["Before scaling", "After scaling"]
COLOUR = {"Age": BLUE, "Salary": ORANGE}
FONT = dict(family="Latin Modern Roman", size=20)


def before_after(df):
    """Training set before and after StandardScaler, stacked into one long table with a 'stage' column."""
    X = df.drop(columns="Purchased")
    X_train, _, _, _ = train_test_split(X, df["Purchased"], test_size=0.3, random_state=0)
    scaled = pd.DataFrame(StandardScaler().fit_transform(X_train), columns=X.columns, index=X_train.index)
    return pd.concat([X_train.assign(stage=STAGES[0]), scaled.assign(stage=STAGES[1])])


def kde(x):
    """Density curve on its own grid, from min - 3 bandwidths to max + 3 bandwidths."""
    k = stats.gaussian_kde(x)
    bw = np.sqrt(k.covariance[0, 0])
    grid = np.linspace(x.min() - 3 * bw, x.max() + 3 * bw, 400)
    return grid, k(grid)


def save(fig, name, width, height, legend=True):
    fig.update_layout(template="simple_white", width=width, height=height, font=FONT, showlegend=legend,
                      legend=dict(x=1.02, y=0.5, yanchor="middle"), margin=dict(l=90, r=20, t=50, b=70))
    fig.update_annotations(font_size=22)
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


df = pd.read_csv(here.parent / "data" / "Social_Network_Ads.csv").iloc[:, 2:]
both = before_after(df).rename(columns={"EstimatedSalary": "Salary"})

# 1. scatter: same cloud, new numbers on the axes
fig = make_subplots(1, 2, subplot_titles=STAGES, horizontal_spacing=0.1)
for c, stage in enumerate(STAGES, start=1):
    d = both[both.stage == stage]
    fig.add_scatter(x=d.Age, y=d.Salary, mode="markers", marker=dict(color=BLUE, size=6, opacity=0.6), row=1, col=c)
    fig.update_xaxes(title="Age", row=1, col=c)
fig.update_yaxes(title="Estimated salary", row=1, col=1)
save(fig, "scatter_before_after", 1000, 420, legend=False)

# 2. KDE of both columns on one axis: before, salary is a flat line; after, the two curves overlap
fig = make_subplots(1, 2, subplot_titles=STAGES, horizontal_spacing=0.1)
for c, stage in enumerate(STAGES, start=1):
    d = both[both.stage == stage]
    for col in ("Age", "Salary"):
        x, y = kde(d[col].to_numpy(float))
        fig.add_scatter(x=x, y=y, mode="lines", name=col, legendgroup=col, showlegend=c == 1,
                        line=dict(color=COLOUR[col], width=3, shape="spline"), row=1, col=c)
    fig.update_xaxes(title="value", row=1, col=c)
fig.update_yaxes(title="Density", row=1, col=1)
save(fig, "kde_before_after", 1000, 420)

# 3. each column alone: the shape of the curve does not change, only the numbers on the x axis
fig = make_subplots(2, 2, subplot_titles=[f"{s}: {col}" for col in ("Age", "Salary") for s in STAGES],
                    horizontal_spacing=0.1, vertical_spacing=0.17)
for r, col in enumerate(("Age", "Salary"), start=1):
    for c, stage in enumerate(STAGES, start=1):
        x, y = kde(both.loc[both.stage == stage, col].to_numpy(float))
        fig.add_scatter(x=x, y=y, mode="lines", name=col, showlegend=c == 1,
                        line=dict(color=COLOUR[col], width=3, shape="spline"), row=r, col=c)
    fig.update_yaxes(title="Density", row=r, col=1)
for c in (1, 2):
    fig.update_xaxes(title="value", row=2, col=c)
fig.update_yaxes(tickformat=".1e", row=2, col=1)   # salary densities are around 0.00001
save(fig, "shape_unchanged", 1000, 640)

# 4. three made-up extreme users: after scaling they are just as far from the rest
extra = pd.DataFrame({"Age": [5, 90, 95], "EstimatedSalary": [1000, 250000, 350000], "Purchased": [0, 1, 1]})
out = before_after(pd.concat([df, extra], ignore_index=True)).rename(columns={"EstimatedSalary": "Salary"})
out["point"] = np.where(out.index >= len(df), "added outlier", "normal user")
fig = make_subplots(1, 2, subplot_titles=STAGES, horizontal_spacing=0.1)
for c, stage in enumerate(STAGES, start=1):
    for point, colour in (("normal user", BLUE), ("added outlier", RED)):
        d = out[(out.stage == stage) & (out.point == point)]
        fig.add_scatter(x=d.Age, y=d.Salary, mode="markers", name=point, showlegend=c == 1,
                        marker=dict(color=colour, size=8 if point == "normal user" else 11, opacity=0.8),
                        row=1, col=c)
    fig.update_xaxes(title="Age", row=1, col=c)
fig.update_yaxes(title="Estimated salary", row=1, col=1)
save(fig, "outliers", 1100, 420)
