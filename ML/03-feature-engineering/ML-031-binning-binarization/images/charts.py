"""Plotly charts for Note ML-031: the three KBinsDiscretizer strategies on Age and Fare, and binarizing an image."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_sample_image
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Binarizer, KBinsDiscretizer

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)


def save(fig, name, width, height, top=80):
    fig.update_layout(template="simple_white", width=width, height=height, showlegend=False, font=FONT,
                      bargap=0.05, margin=dict(l=70, r=20, t=top, b=60 if top > 50 else 10))
    fig.update_annotations(font_size=21)
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


# Titanic training set, exactly as in the Notebook
df = pd.read_csv(here.parent / "data" / "titanic_train.csv", usecols=["Age", "Fare", "Survived"]).dropna()
X_train, _, _, _ = train_test_split(df[["Age", "Fare"]], df["Survived"], test_size=0.2, random_state=42)

# 1. one column, three strategies, 5 bins: histogram with the bin edges (top), rows per bin (bottom)
strategies = {"uniform": "Equal width (uniform)", "quantile": "Equal frequency (quantile)", "kmeans": "k-means"}
for col, xmax in [("Age", 80), ("Fare", 520)]:
    x = X_train[[col]]
    titles = []
    for s, name in strategies.items():
        e = KBinsDiscretizer(n_bins=5, encode="ordinal", strategy=s).fit(x).bin_edges_[0][1:-1]
        titles.append(f"{name}<br><span style='color:{RED}'>inner edges: {', '.join(f'{v:g}' for v in np.round(e, 1))}</span>")
    fig = make_subplots(2, 3, vertical_spacing=0.2, horizontal_spacing=0.06, row_heights=[0.55, 0.45],
                        subplot_titles=titles + [""] * 3)
    for j, s in enumerate(strategies, start=1):
        kb = KBinsDiscretizer(n_bins=5, encode="ordinal", strategy=s).fit(x)
        edges = kb.bin_edges_[0]
        counts = np.bincount(kb.transform(x)[:, 0].astype(int), minlength=5)
        fig.add_trace(go.Histogram(x=x[col], xbins=dict(start=0, end=xmax, size=xmax / 40),
                                   marker_color=BLUE, opacity=0.55), 1, j)
        for e in edges[1:-1]:
            fig.add_vline(x=e, line=dict(color=RED, width=2.5), opacity=1, layer="above", row=1, col=j)
        fig.update_xaxes(title=col, range=[0, xmax], row=1, col=j)
        fig.add_trace(go.Bar(x=[f"bin {i}" for i in range(5)], y=counts, marker_color=GREEN,
                             text=counts, textposition="outside", textfont=dict(size=17)), 2, j)
        fig.update_yaxes(range=[0, 600 if col == "Fare" else 320], row=2, col=j)
        fig.update_xaxes(title="bin number", row=2, col=j)
    fig.update_yaxes(title="passengers", col=1)
    save(fig, f"{col.lower()}_strategies", 1300, 740, top=120)

# 2. binarizing an image: grey levels 0 to 255, threshold 127.5
grey = load_sample_image("china.jpg").mean(axis=2)          # 427 x 640 grey levels
bw = Binarizer(threshold=127.5).fit_transform(grey) * 255   # every pixel becomes 0 or 255
fig = make_subplots(1, 2, horizontal_spacing=0.03,
                    subplot_titles=["Grey levels 0 to 255", "After Binarizer(threshold=127.5)"])
for j, img in enumerate([grey, bw], start=1):
    fig.add_trace(go.Heatmap(z=img[::-1], colorscale="gray", showscale=False, zmin=0, zmax=255), 1, j)
    fig.update_xaxes(visible=False, row=1, col=j)
    fig.update_yaxes(visible=False, scaleanchor=f"x{j}", row=1, col=j)
save(fig, "binarize_image", 1100, 400, top=50)

# ---- Round 2 figures ----
import warnings
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeClassifier
warnings.filterwarnings("ignore")


def save_plain(fig, name, width, height, top=40, bottom=80, legend=False):
    fig.update_layout(template="simple_white", width=width, height=height, showlegend=legend, font={**FONT, "size": 22},
                      margin=dict(l=90, r=30, t=top, b=bottom))
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


# 3. equal frequency: sort the ages, cut the sorted list into 5 equal piles; the cut heights are the quantile edges
age = np.sort(X_train["Age"].to_numpy())
kb = KBinsDiscretizer(n_bins=5, encode="ordinal", strategy="quantile").fit(X_train[["Age"]])
q_edges = kb.bin_edges_[0]
q_counts = np.bincount(kb.transform(X_train[["Age"]])[:, 0].astype(int))
assert np.allclose(q_edges[1:-1], [19, 25, 32, 42]) and q_counts.tolist() == [108, 112, 118, 115, 118]
rank = np.arange(1, len(age) + 1)
colours = [BLUE, ORANGE, GREEN, RED, "#B279A2"]
fig = go.Figure()
bin_of = np.digitize(age, q_edges[1:-1])
for b in range(5):
    m = bin_of == b
    fig.add_trace(go.Scatter(x=rank[m], y=age[m], mode="markers", marker=dict(color=colours[b], size=6),
                             name=f"bin {b}: {m.sum()} passengers"))
for k, e in enumerate(q_edges[1:-1], start=1):
    fig.add_hline(y=e, line=dict(color=GREY, width=1.5, dash="dot"))
    fig.add_vline(x=k * len(age) / 5, line=dict(color=GREY, width=1.5, dash="dot"))
    fig.add_annotation(x=8, y=e, text=f"Q({k / 5:.1f}) = {e:g}", showarrow=False, xanchor="left", yanchor="bottom",
                       font=dict(size=22))
fig.update_xaxes(title="passengers sorted by age (1 = youngest, 571 = oldest)", tickvals=[1, 114, 228, 343, 457, 571])
fig.update_yaxes(title="Age (years)", range=[0, 82])
fig.update_layout(legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2, font_size=19))
save_plain(fig, "quantile_edges", 1100, 620, bottom=150, legend=True)

# 4. Section 10.4: cross-validated accuracy for every strategy and number of bins, against no binning
full = pd.read_csv(here.parent / "data" / "titanic_train.csv", usecols=["Age", "Fare", "Survived"]).dropna()
X, y = full[["Age", "Fare"]], full["Survived"]
base = cross_val_score(DecisionTreeClassifier(random_state=0), X, y, cv=10).mean()
names = {"uniform": "Equal width", "quantile": "Equal frequency", "kmeans": "k-means"}
acc = {}
for s in names:
    for b in (5, 10, 15):
        kb_ = lambda: KBinsDiscretizer(n_bins=b, encode="ordinal", strategy=s)
        trf = ColumnTransformer([("age", kb_(), ["Age"]), ("fare", kb_(), ["Fare"])])
        acc[s, b] = cross_val_score(make_pipeline(trf, DecisionTreeClassifier(random_state=0)), X, y, cv=10).mean()
expected = {("uniform", 5): 63.2, ("uniform", 10): 68.6, ("uniform", 15): 65.3, ("quantile", 5): 67.7,
            ("quantile", 10): 67.5, ("quantile", 15): 67.5, ("kmeans", 5): 67.8, ("kmeans", 10): 66.5,
            ("kmeans", 15): 66.3}
assert all(round(acc[k] * 100, 1) == v for k, v in expected.items()) and round(base * 100, 1) == 63.0
fig = go.Figure()
for (s, colour, dash) in [("uniform", BLUE, "solid"), ("quantile", GREEN, "solid"), ("kmeans", ORANGE, "solid")]:
    ys = [acc[s, b] * 100 for b in (5, 10, 15)]
    fig.add_trace(go.Scatter(x=[5, 10, 15], y=ys, mode="lines+markers+text", name=names[s],
                             line=dict(color=colour, width=4), marker=dict(size=14),
                             text=[f"{v:.1f}" for v in ys], textposition={"uniform": ["top center"] * 3, "quantile": ["bottom center", "top center", "top center"],
                                           "kmeans": ["top center", "bottom center", "bottom center"]}[s],
                             textfont=dict(size=20, color=colour)))
fig.add_hline(y=base * 100, line=dict(color=RED, width=3, dash="dash"))
fig.add_annotation(x=15.4, y=base * 100, text="no binning: 63.0", showarrow=False, xanchor="right", yanchor="bottom",
                   font=dict(size=22, color=RED))
fig.update_xaxes(title="number of bins", tickvals=[5, 10, 15], range=[4, 16])
fig.update_yaxes(title="10-fold CV accuracy (%)", range=[62, 70])
fig.update_layout(legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2))
save_plain(fig, "strategy_grid", 1000, 600, bottom=140, legend=True)

# 5. Section 11: survival rate of the custom age groups (all 714 passengers with an age)
groups = pd.cut(full["Age"], bins=[0, 18, 60, np.inf], right=False, labels=["child (0-17)", "adult (18-59)", "senior (60+)"])
surv = full.groupby(groups, observed=True)["Survived"].agg(["size", "mean"])
assert surv["size"].tolist() == [113, 575, 26] and (surv["mean"] * 100).round().tolist() == [54, 39, 27]
fig = go.Figure(go.Bar(x=surv.index.astype(str), y=surv["mean"] * 100, marker_color=[GREEN, BLUE, ORANGE],
                       text=[f"{m * 100:.0f}% of {n}" for n, m in zip(surv["size"], surv["mean"])],
                       textposition="outside", textfont=dict(size=24)))
fig.update_yaxes(title="survived (%)", range=[0, 65])
save_plain(fig, "custom_groups", 900, 480)

# 6. Section 13: survival by family size; binarizing at 0 keeps the big jump (alone vs with family)
fam = (full_fam := pd.read_csv(here.parent / "data" / "titanic_train.csv").dropna(subset=["Age"]))["SibSp"] + full_fam["Parch"]
by = full_fam.groupby(fam)["Survived"].agg(["size", "mean"])
alone, with_fam = full_fam["Survived"][fam == 0].mean(), full_fam["Survived"][fam > 0].mean()
assert len(full_fam) == 714 and round(alone * 100) == 32 and round(with_fam * 100) == 52
assert round(full_fam["Survived"][fam >= 4].mean() * 100) == 20
fig = go.Figure(go.Bar(x=by.index, y=by["mean"] * 100, marker_color=[GREY if f == 0 else ORANGE for f in by.index],
                       text=[f"n={n}" for n in by["size"]], textposition="outside", textfont=dict(size=18)))
fig.add_shape(type="line", x0=-0.45, x1=0.45, y0=alone * 100, y1=alone * 100, line=dict(color=BLUE, width=5, dash="dash"), layer="above", opacity=1)
fig.add_shape(type="line", x0=0.55, x1=7.45, y0=with_fam * 100, y1=with_fam * 100, line=dict(color=BLUE, width=5, dash="dash"), layer="above", opacity=1)
fig.add_annotation(x=0, y=88, text=f"binarized 0<br>alone: {alone * 100:.0f}%", showarrow=False, yanchor="top",
                   font=dict(size=22, color=BLUE))
fig.add_annotation(x=5.5, y=88, text=f"binarized 1<br>with family: {with_fam * 100:.0f}%", showarrow=False,
                   yanchor="top", font=dict(size=22, color=BLUE))
fig.update_xaxes(title="family = SibSp + Parch", dtick=1)
fig.update_yaxes(title="survived (%)", range=[0, 92])
save_plain(fig, "family_survival", 1000, 540)
print("round 2 charts done")
