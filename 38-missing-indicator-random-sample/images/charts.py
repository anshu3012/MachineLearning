"""Plotly charts for Note 38: random sample imputation on Titanic Age and on two house-quality columns."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import gaussian_kde
from sklearn.model_selection import train_test_split

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, PURPLE, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)
legend_below = dict(orientation="h", x=0.5, xanchor="center", y=-0.25)


def save(fig, name, width, height, top=60, bottom=120):
    fig.update_layout(template="simple_white", width=width, height=height, font=FONT,
                      margin=dict(l=80, r=20, t=top, b=bottom))
    fig.update_annotations(font_size=21)
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


def random_fill(col, pool, seed=42):
    # same rule and seed as the Notebook
    out = col.copy()
    gaps = out.isnull()
    out[gaps] = pool.sample(gaps.sum(), random_state=seed).values
    return out


# 1. Titanic Age: random sample imputation keeps the shape, mean imputation does not
df = pd.read_csv(here.parent / "data" / "titanic.csv", usecols=["Age", "Fare", "Survived"])
X_train, *_ = train_test_split(df[["Age", "Fare"]], df["Survived"], test_size=0.2, random_state=2)
age = X_train["Age"]
rand = random_fill(age, age.dropna())
mean = age.fillna(age.mean())
fig = make_subplots(1, 2, column_widths=[0.62, 0.38], horizontal_spacing=0.1,
                    subplot_titles=["Density of Age", "Box plots"])
grid = np.linspace(-10, 85, 600)
for s, colour, name, dash in [(age, BLUE, "original (gaps skipped)", "solid"),
                              (rand, ORANGE, "random sample imputed", "solid"),
                              (mean, GREEN, "mean imputed (Note 36)", "dash")]:
    fig.add_trace(go.Scatter(x=grid, y=gaussian_kde(s.dropna())(grid), mode="lines", name=name,
                             line=dict(color=colour, width=3, dash=dash)), 1, 1)
for s, colour, name in [(age, BLUE, "original"), (rand, ORANGE, "random"), (mean, GREEN, "mean")]:
    fig.add_trace(go.Box(y=s.dropna(), name=name, marker_color=colour, showlegend=False), 1, 2)
fig.update_xaxes(title="Age (years)", row=1, col=1)
fig.update_yaxes(title="density", row=1, col=1)
fig.update_yaxes(title="Age (years)", row=1, col=2)
fig.update_layout(legend=legend_below)
save(fig, "random_age", 1300, 540)

# 2. house data: category shares before and after random sample imputation
house = pd.read_csv(here.parent / "data" / "house_prices.csv")
H_train, _ = train_test_split(house, test_size=0.2, random_state=2)
H_train = H_train.copy()
order = ["Ex", "Gd", "TA", "Fa", "Po"]
for c in ["GarageQual", "FireplaceQu"]:
    H_train[c + "_imputed"] = random_fill(H_train[c], H_train[c].dropna())
fig = make_subplots(1, 2, horizontal_spacing=0.1,
                    subplot_titles=["GarageQual (5.6% missing)", "FireplaceQu (47.7% missing)"])
for j, c in enumerate(["GarageQual", "FireplaceQu"], start=1):
    for col, colour, name in [(c, BLUE, "before (known values)"), (c + "_imputed", ORANGE, "after random sample")]:
        share = H_train[col].value_counts(normalize=True).reindex(order) * 100
        fig.add_trace(go.Bar(x=order, y=share, name=name, marker_color=colour, showlegend=(j == 1),
                             text=[f"{v:.1f}" for v in share], textposition="outside"), 1, j)
    fig.update_xaxes(title="category", row=1, col=j)
fig.update_yaxes(title="share of rows (%)", range=[0, 110], col=1)
fig.update_yaxes(range=[0, 62], col=2)
fig.update_layout(legend=legend_below, barmode="group", bargap=0.25)
save(fig, "category_shares", 1300, 540)

# 3. FireplaceQu: sale price per category, before and after
colours = dict(Ex=PURPLE, Gd=BLUE, TA=ORANGE, Fa=GREEN, Po=RED)
fig = make_subplots(1, 2, horizontal_spacing=0.08, shared_yaxes=True,
                    subplot_titles=["before imputation", "after random sample imputation"])
grid = np.linspace(0, 600_000, 600)
for j, col in enumerate(["FireplaceQu", "FireplaceQu_imputed"], start=1):
    for cat in order:
        prices = H_train.loc[H_train[col] == cat, "SalePrice"]
        fig.add_trace(go.Scatter(x=grid / 1000, y=gaussian_kde(prices)(grid) * 1000, mode="lines", name=cat,
                                 line=dict(color=colours[cat], width=3), showlegend=(j == 1)), 1, j)
    fig.update_xaxes(title="sale price (thousand dollars)", row=1, col=j)
fig.update_yaxes(title="density", col=1)
fig.update_layout(legend=legend_below)
save(fig, "fireplace_price", 1300, 540)
