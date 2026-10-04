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

# ---- Round 2 figures ----
import warnings
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
warnings.filterwarnings("ignore")


def save_plain(fig, name, width, height, top=50, bottom=80, legend=False):
    fig.update_layout(template="simple_white", width=width, height=height, showlegend=legend, font={**FONT, "size": 22},
                      margin=dict(l=90, r=30, t=top, b=bottom))
    fig.update_annotations(font_size=23)
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


pool = age.dropna()

# 4. Section 4: the same input asked 8 times; a fresh draw each time vs a draw seeded by the row's fare
new_fare = 56.4958
seeded = [pool.sample(1, random_state=int(new_fare)).iloc[0] for _ in range(8)]
fresh = [pool.sample(1, random_state=s).iloc[0] for s in range(100, 108)]   # 8 different seeds stand in for "no seed"
assert seeded == [34.0] * 8 and len(set(fresh)) > 4
fig = go.Figure()
presses = list(range(1, 9))
fig.add_trace(go.Scatter(x=presses, y=fresh, mode="lines+markers+text", name="no fixed seed: a new draw each time",
                         line=dict(color=RED, width=3), marker=dict(size=14), text=[f"{a:g}" for a in fresh],
                         textposition=["bottom center" if 25 <= a <= 42 else "top center" for a in fresh],
                         textfont=dict(size=20, color=RED)))
fig.add_trace(go.Scatter(x=presses, y=seeded, mode="lines+markers", name="seed = int(Fare) = 56: always 34",
                         line=dict(color=GREEN, width=4), marker=dict(size=14)))
fig.update_xaxes(title="press of the button, same input (Age empty, Fare 56.50)", dtick=1)
fig.update_yaxes(title="age filled in", range=[0, max(fresh) + 12])
fig.update_layout(legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.25))
save_plain(fig, "same_fill", 1000, 520, top=20, bottom=150, legend=True)

# 5. Section 6.2: survival of passengers with and without a recorded age (Titanic training set)
y_tr = df.loc[X_train.index, "Survived"]
rates = [y_tr[X_train["Age"].isnull()].mean() * 100, y_tr[X_train["Age"].notnull()].mean() * 100]
assert [round(r, 1) for r in rates] == [28.4, 39.2]
fig = go.Figure(go.Bar(x=["Age missing<br>(Age_NA = True)", "Age recorded<br>(Age_NA = False)"], y=rates,
                       marker_color=[ORANGE, BLUE], width=0.5, text=[f"{r:.1f}%" for r in rates],
                       textposition="outside", textfont=dict(size=26)))
fig.update_yaxes(title="survived (%)", range=[0, 50])
save_plain(fig, "indicator_survival", 800, 460, top=20)

# 6. Section 6.3: the indicator's weight moves the predicted chance of survival down for a missing age
X_tr, X_te, y_tr2, y_te = train_test_split(df[["Age", "Fare"]], df["Survived"], test_size=0.2, random_state=2)
si = SimpleImputer(add_indicator=True).fit(X_tr)
clf = LogisticRegression().fit(si.transform(X_tr), y_tr2)
base = LogisticRegression().fit(SimpleImputer().fit_transform(X_tr), y_tr2)
correct = int((clf.predict(si.transform(X_te)) == y_te).sum())
correct0 = int((base.predict(SimpleImputer().fit(X_tr).transform(X_te)) == y_te).sum())
assert (correct0, correct, len(y_te)) == (110, 113, 179) and round(clf.coef_[0][2], 2) == -0.30
fares = np.linspace(0, 150, 200)
mean_age = si.statistics_[0]
fig = go.Figure()
for na, colour, name in [(0, BLUE, "Age recorded as 29.79 (Age_NA = 0)"), (1, ORANGE, "Age missing, filled with 29.79 (Age_NA = 1)")]:
    p = clf.predict_proba(np.column_stack([np.full_like(fares, mean_age), fares, np.full_like(fares, na)]))[:, 1]
    fig.add_trace(go.Scatter(x=fares, y=p * 100, mode="lines", line=dict(color=colour, width=4), name=name))
b0, (wa, wf, wn) = clf.intercept_[0], clf.coef_[0]
cross = [-(b0 + wa * mean_age + wn * na) / wf for na in (0, 1)]     # fare where the chance reaches 50%
assert round(cross[0], -1) == 60 and round(cross[1], -1) == 80, cross
fig.add_hline(y=50, line=dict(color=GREY, width=1.5, dash="dot"), opacity=1)
fig.add_annotation(x=150, y=50, text="predicts 'survived' above 50%", showarrow=False, xanchor="right", yanchor="bottom",
                   font=dict(size=20, color=GREY))
fig.update_xaxes(title="Fare")
fig.update_yaxes(title="predicted chance of survival (%)", range=[20, 80])
fig.update_layout(legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.25))
save_plain(fig, "indicator_effect", 1000, 540, top=20, bottom=160, legend=True)

# 7. Section 7.4: what grid search found, where the fill matters (houses) and where it does not (Titanic)
house = pd.read_csv(here.parent / "data" / "house_prices.csv")
Xh_tr, _, yh_tr, _ = train_test_split(house[["GarageQual", "FireplaceQu"]], house["SalePrice"], test_size=0.2, random_state=2)
hp = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("ohe", OneHotEncoder(handle_unknown="ignore")),
               ("model", LinearRegression())])
hs = GridSearchCV(hp, {"imputer__strategy": ["most_frequent", "constant"]}, cv=10,
                  scoring="neg_mean_absolute_error").fit(Xh_tr, yh_tr)
mae = -hs.cv_results_["mean_test_score"]
assert np.round(mae).tolist() == [53447, 46382]
t = pd.read_csv(here.parent / "data" / "titanic.csv").drop(columns=["PassengerId", "Name", "Ticket", "Cabin"])
Xt_tr, _, yt_tr, _ = train_test_split(t.drop(columns=["Survived"]), t["Survived"], test_size=0.2, random_state=2)
num = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])
cat = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("ohe", OneHotEncoder(handle_unknown="ignore"))])
pre = ColumnTransformer([("num", num, ["Age", "Fare"]), ("cat", cat, ["Embarked", "Sex"])])
grid = {"preprocessor__num__imputer__strategy": ["mean", "median"],
        "preprocessor__cat__imputer__strategy": ["most_frequent", "constant"], "classifier__C": [0.1, 1.0, 10, 100]}
gs = GridSearchCV(Pipeline([("preprocessor", pre), ("classifier", LogisticRegression())]), grid, cv=10).fit(Xt_tr, yt_tr)
res = pd.DataFrame(gs.cv_results_)
res["imputers"] = res["param_preprocessor__num__imputer__strategy"] + " + " + res["param_preprocessor__cat__imputer__strategy"]
table = res.pivot(index="imputers", columns="param_classifier__C", values="mean_test_score") * 100
assert set(table.round(1).loc[:, 0.1]) == {78.6} and set(table.round(1).loc[:, [1.0, 10, 100]].values.ravel()) == {78.8}
fig = make_subplots(1, 2, column_widths=[0.38, 0.62], horizontal_spacing=0.2,
                    subplot_titles=["House prices: error (dollars)", "Titanic: CV accuracy (%)"])
fig.add_trace(go.Bar(x=["most_frequent", "constant"], y=mae, marker_color=[GREY, GREEN], width=0.55,
                     text=[f"{v:,.0f}" for v in mae], textposition="outside", textfont=dict(size=22)), 1, 1)
fig.add_trace(go.Heatmap(z=table.values, x=[f"C = {c:g}" for c in table.columns], y=list(table.index),
                         colorscale="Greens", zmin=78, zmax=79.2, showscale=False,
                         text=table.round(1).values, texttemplate="%{text}", textfont=dict(size=22)), 1, 2)
fig.update_yaxes(title="mean CV error", range=[0, 62000], row=1, col=1)
fig.update_xaxes(title="imputer strategy", row=1, col=1)
fig.update_xaxes(title="C of logistic regression", row=1, col=2)
save_plain(fig, "grid_results", 1300, 560, top=60, bottom=90)
print("round 2 charts done")
