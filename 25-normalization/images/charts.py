"""Still charts for Note 25 (Plotly; replaces an earlier seaborn version): wine data before vs after MinMaxScaler
(training set), and all scalers on one small column with an outlier."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler, RobustScaler, StandardScaler

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED = "#4C78A8", "#F58518", "#54A24B", "#E45756"
FONT = dict(family="Latin Modern Roman", size=18)
df = pd.read_csv(here.parent / "data" / "wine_data.csv", header=None, usecols=[0, 1, 2])
df.columns = ["Class", "Alcohol", "Malic acid"]
X_train, _, y_train, _ = train_test_split(df.drop(columns="Class"), df["Class"], test_size=0.3, random_state=0)
scaled = pd.DataFrame(MinMaxScaler().fit_transform(X_train), columns=X_train.columns, index=X_train.index)
assert len(X_train) == 124 and round(X_train.Alcohol.min(), 2) == 11.03

# 1. scatter: same cloud, now inside the unit square
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=["Before scaling", "After min-max scaling"])
for j, d in enumerate((X_train, scaled), start=1):
    for c, col in ((1, BLUE), (2, ORANGE), (3, GREEN)):
        m = y_train == c
        fig.add_scatter(x=d.Alcohol[m], y=d["Malic acid"][m], mode="markers", name=f"class {c}", showlegend=j == 1,
                        marker=dict(color=col, size=9, opacity=0.85), row=1, col=j)
    fig.update_xaxes(title_text="Alcohol", row=1, col=j)
    fig.update_yaxes(title_text="Malic acid", row=1, col=j)
fig.update_annotations(font_size=20)
fig.update_layout(template="simple_white", width=1300, height=540, font=FONT, margin=dict(l=70, r=20, t=60, b=70),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18))
fig.write_image(here / "scatter_before_after.png", scale=2)
fig.write_image(here / "scatter_before_after.pdf")

# 2. one small column with an outlier (130), scaled five ways, all on one shared axis
w = np.array([[32.0], [54], [60], [67], [130]])
methods = {
    "Standardization": StandardScaler().fit_transform(w),
    "Min-max": MinMaxScaler().fit_transform(w),
    "Mean normalization": (w - w.mean()) / (w.max() - w.min()),
    "Max-abs": MaxAbsScaler().fit_transform(w),
    "Robust": RobustScaler().fit_transform(w),
}
assert np.allclose(methods["Robust"].ravel(), [-2.1538, -0.4615, 0, 0.5385, 5.3846], atol=1e-3)
fig = go.Figure()
for i, (m, v) in enumerate(methods.items()):
    v = v.ravel()
    fig.add_scatter(x=v[:4], y=[m] * 4, mode="markers", name="other values", showlegend=i == 0,
                    marker=dict(color=BLUE, size=16, opacity=0.85))
    fig.add_scatter(x=v[4:], y=[m], mode="markers", name="outlier (130)", showlegend=i == 0,
                    marker=dict(color=RED, size=16, opacity=0.85))
fig.update_layout(template="simple_white", width=1200, height=520, font=FONT,
                  xaxis=dict(title="scaled value", range=[-2.5, 5.8], showgrid=True),
                  yaxis=dict(categoryorder="array", categoryarray=list(methods)[::-1], showgrid=True),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=190, r=20, t=30, b=80))
fig.write_image(here / "scalers_outlier.png", scale=2)
fig.write_image(here / "scalers_outlier.pdf")
