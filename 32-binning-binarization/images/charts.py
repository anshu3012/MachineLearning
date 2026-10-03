"""Plotly charts for Note 32: the three KBinsDiscretizer strategies on Age and Fare, and binarizing an image."""
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
