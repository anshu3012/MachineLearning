"""Plotly charts for Note ML-036: category shares and sale prices before and after imputing two categorical columns."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import gaussian_kde
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)
COLS = ["GarageQual", "FireplaceQu"]


def save(fig, name, width, height, top=80, legend=False):
    fig.update_layout(template="simple_white", width=width, height=height, showlegend=legend, font=FONT,
                      margin=dict(l=90, r=20, t=top, b=70))
    fig.update_annotations(font_size=21)
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


# the house data, split exactly as in the Notebook; every number comes from the training set
df = pd.read_csv(here.parent / "data" / "house_prices.csv")
X_train, X_test, y_train, y_test = train_test_split(df[COLS], df["SalePrice"], test_size=0.2, random_state=42)
mode = SimpleImputer(strategy="most_frequent").set_output(transform="pandas").fit(X_train)
X_mode = mode.transform(X_train)
X_miss = SimpleImputer(strategy="constant", fill_value="Missing").set_output(transform="pandas").fit_transform(X_train)

# 1. category shares before and after mode imputation
fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=COLS)
for j, c in enumerate(COLS, start=1):
    before = X_train[c].value_counts(normalize=True) * 100
    after = X_mode[c].value_counts(normalize=True)[before.index] * 100
    for data, col, name in [(before, RED, "before imputation"), (after, GREEN, "after mode imputation")]:
        fig.add_trace(go.Bar(x=data.index, y=data.values, marker_color=col, name=name, legendgroup=name,
                             showlegend=(j == 1), text=[f"{v:.1f}" for v in data], textposition="outside",
                             textfont=dict(size=15)), 1, j)
    fig.update_xaxes(title="category", row=1, col=j)
fig.update_layout(barmode="group", bargroupgap=0.05, legend=dict(orientation="h", x=0.5, xanchor="center", y=1.2))
fig.update_yaxes(title="share of training rows (%)", range=[0, 108], col=1)
fig.update_yaxes(range=[0, 85], col=2)
save(fig, "mode_shares", 1300, 560, top=120, legend=True)

# 2. sale price of houses in the most frequent category, of houses with a gap, and of the category after imputation
grid = np.linspace(0, 500_000, 400)
titles = []
for c, m in zip(COLS, mode.statistics_):
    titles += [f"{c}: houses with {m} vs houses with NaN", f"{c}: houses with {m}, before vs after"]
fig = make_subplots(2, 2, vertical_spacing=0.2, horizontal_spacing=0.08, subplot_titles=titles)
for i, (c, m) in enumerate(zip(COLS, mode.statistics_), start=1):
    pairs = [[(y_train[X_train[c] == m], BLUE, "solid", f"{m}"), (y_train[X_train[c].isnull()], ORANGE, "solid", "NaN")],
             [(y_train[X_train[c] == m], RED, "solid", f"{m} before"), (y_train[X_mode[c] == m], GREEN, "dash", f"{m} after")]]
    for j, pair in enumerate(pairs, start=1):
        for k, (data, col, dash, name) in enumerate(pair):
            fig.add_trace(go.Scatter(x=grid / 1000, y=gaussian_kde(data)(grid) * 1000, mode="lines",
                                     line=dict(color=col, width=3, dash=dash), showlegend=False), i, j)
            # label each curve at the right, instead of a shared legend
            fig.add_annotation(x=1.0, y=0.85 - 0.15 * k, xref="x domain", yref="y domain", row=i, col=j,
                               text=f"<b>{name}</b> (mean {data.mean() / 1000:.0f}k)", showarrow=False, xanchor="right",
                               font=dict(color=col, size=18))
        fig.update_xaxes(title="SalePrice (thousand dollars)", row=i, col=j)
fig.update_yaxes(title="density", col=1)
save(fig, "price_kde", 1300, 820, top=70)

# 3. category counts after adding the category "Missing"
fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=COLS)
for j, c in enumerate(COLS, start=1):
    n = X_miss[c].value_counts()
    fig.add_trace(go.Bar(x=n.index, y=n.values, marker_color=[ORANGE if k == "Missing" else BLUE for k in n.index],
                         text=[f"{v} ({v / len(X_miss) * 100:.1f}%)" if k == "Missing" else str(v) for k, v in n.items()],
                         textposition="outside", textfont=dict(size=15)), 1, j)
    fig.update_xaxes(title="category", row=1, col=j)
fig.update_yaxes(title="number of training rows", range=[0, 1180], col=1)
fig.update_yaxes(range=[0, 620], col=2)
save(fig, "missing_category", 1300, 520, top=60)

# 4. Section 4: share of missing values in each column (all 1,460 houses), against the 5% rule of thumb
miss = df[COLS].isnull().mean() * 100
assert miss.round(1).tolist() == [5.5, 47.3] and df[COLS].isnull().sum().tolist() == [81, 690]
fig = go.Figure(go.Bar(x=miss.values, y=COLS, orientation="h", marker_color=[BLUE, ORANGE], width=0.55,
                       text=[f"{v:.1f}% ({n} of 1,460)" for v, n in zip(miss, df[COLS].isnull().sum())],
                       textposition="outside", textfont=dict(size=22)))
fig.add_vline(x=5, line=dict(color=RED, width=3, dash="dash"), opacity=1)
fig.add_annotation(x=5, y=1.45, text="5% rule of thumb", showarrow=False, xanchor="left", xshift=6,
                   font=dict(size=22, color=RED))
fig.update_xaxes(title="share of values missing (%)", range=[0, 70])
fig.update_yaxes(range=[-0.6, 1.7])
save(fig, "missing_share", 1000, 360, top=20)
