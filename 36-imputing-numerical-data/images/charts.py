"""Plotly charts for Note 36: mean/median, arbitrary value and end-of-distribution imputation on the Titanic training set."""
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


def save(fig, name, width, height, top=80, bottom=70):
    fig.update_layout(template="simple_white", width=width, height=height, font=FONT, bargap=0.05,
                      margin=dict(l=80, r=20, t=top, b=bottom))
    fig.update_annotations(font_size=21)
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


def kde(fig, data, lo, hi, colour, name, col, dash="solid", show=True):
    grid = np.linspace(lo, hi, 600)
    fig.add_trace(go.Scatter(x=grid, y=gaussian_kde(data.dropna())(grid), mode="lines", name=name,
                             line=dict(color=colour, width=3, dash=dash), showlegend=show), 1, col)


# the training set, exactly as in the Notebook (imputation values come from it only)
df = pd.read_csv(here.parent / "data" / "titanic_toy.csv")
X_train, X_test, y_train, y_test = train_test_split(df.drop(columns="Survived"), df["Survived"],
                                                    test_size=0.2, random_state=2)
age, fare = X_train["Age"], X_train["Fare"]
legend_below = dict(orientation="h", x=0.5, xanchor="center", y=-0.25)

# 1. where the mean and median sit: Age is nearly symmetric, Fare is right-skewed
fig = make_subplots(1, 2, horizontal_spacing=0.08, subplot_titles=["Age", "Fare"])
for j, (s, size) in enumerate([(age, 2.5), (fare, 10)], start=1):
    fig.add_trace(go.Histogram(x=s, xbins=dict(start=0, end=s.max() + size, size=size), marker_color=BLUE,
                               opacity=0.6, showlegend=False), 1, j)
    for v, colour, name in [(s.mean(), GREEN, "mean"), (s.median(), ORANGE, "median")]:
        fig.add_vline(x=v, line=dict(color=colour, width=3, dash="dash" if name == "mean" else "solid"), opacity=1, layer="above", row=1, col=j)
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", name=name, showlegend=(j == 1),
                                 line=dict(color=colour, width=3, dash="dash" if name == "mean" else "solid")), 1, j)
    fig.update_xaxes(title=s.name, row=1, col=j)
fig.add_annotation(text=f"mean {age.mean():.2f}, median {age.median():.2f}", x=0.22, y=0.98, xref="paper",
                   yref="paper", showarrow=False, font_size=18)
fig.add_annotation(text=f"mean {fare.mean():.2f}, median {fare.median():.2f}", x=0.8, y=0.98, xref="paper",
                   yref="paper", showarrow=False, font_size=18)
fig.update_xaxes(range=[0, 300], row=1, col=2)
fig.update_yaxes(title="passengers", col=1)
fig.update_layout(legend=legend_below)
save(fig, "mean_median_position", 1300, 520, top=60, bottom=120)

# 2. KDE before and after mean/median imputation
fig = make_subplots(1, 2, horizontal_spacing=0.08, subplot_titles=["Age (20.8% missing)", "Fare (5.1% missing)"])
for j, (s, lo, hi) in enumerate([(age, -10, 85), (fare, -50, 300)], start=1):
    kde(fig, s, lo, hi, BLUE, "original (gaps skipped)", j, show=(j == 1))
    kde(fig, s.fillna(s.median()), lo, hi, ORANGE, "median imputed", j, show=(j == 1))
    kde(fig, s.fillna(s.mean()), lo, hi, GREEN, "mean imputed", j, dash="dash", show=(j == 1))
    fig.update_xaxes(title=s.name, row=1, col=j)
fig.update_yaxes(title="density", col=1)
fig.update_layout(legend=legend_below)
save(fig, "mean_median_kde", 1300, 520, top=60, bottom=120)

# 3. box plots before and after: the box of Age shrinks, so more points count as outliers
fig = make_subplots(1, 2, horizontal_spacing=0.08, subplot_titles=["Age", "Fare"])
for j, s in enumerate([age, fare], start=1):
    for data, colour, name in [(s, BLUE, "original"), (s.fillna(s.median()), ORANGE, "median"),
                               (s.fillna(s.mean()), GREEN, "mean")]:
        fig.add_trace(go.Box(y=data.dropna(), name=name, marker_color=colour, boxpoints="outliers",
                             showlegend=False), 1, j)
fig.update_yaxes(title="Age (years)", col=1)
fig.update_yaxes(title="Fare", col=2)
save(fig, "mean_median_box", 1300, 560, top=60)

# 4. arbitrary value imputation: a spike appears at the chosen value
fig = make_subplots(1, 2, horizontal_spacing=0.08, subplot_titles=["Age: 99 and -1", "Fare: 999 and -1"])
for j, (s, big, lo, hi) in enumerate([(age, 99, -20, 120), (fare, 999, -100, 1100)], start=1):
    kde(fig, s, lo, hi, BLUE, "original (gaps skipped)", j, show=(j == 1))
    kde(fig, s.fillna(big), lo, hi, RED, "large value (99 / 999)", j, show=(j == 1))
    kde(fig, s.fillna(-1), lo, hi, PURPLE, "-1", j, dash="dash", show=(j == 1))
    fig.update_xaxes(title=s.name, row=1, col=j)
fig.update_yaxes(title="density", col=1)
fig.update_layout(legend=legend_below)
save(fig, "arbitrary_kde", 1300, 520, top=60, bottom=120)

# 5. end of distribution: mean + 3 std for Age, Q3 + 1.5 IQR for Fare
q1, q3 = fare.quantile([0.25, 0.75])
ends = [(age, age.mean() + 3 * age.std(), "mean + 3 std", -10, 90),
        (fare, q3 + 1.5 * (q3 - q1), "Q3 + 1.5 IQR", -50, 300)]
fig = make_subplots(1, 2, horizontal_spacing=0.08,
                    subplot_titles=[f"Age: {name} = {v:.2f}" for s, v, name, *_ in ends[:1]]
                    + [f"Fare: {name} = {v:.2f}" for s, v, name, *_ in ends[1:]])
for j, (s, v, name, lo, hi) in enumerate(ends, start=1):
    kde(fig, s, lo, hi, BLUE, "original (gaps skipped)", j, show=(j == 1))
    kde(fig, s.fillna(v), lo, hi, RED, "end-of-distribution imputed", j, show=(j == 1))
    fig.add_vline(x=v, line=dict(color=GREY, width=2, dash="dot"), opacity=1, row=1, col=j)
    fig.update_xaxes(title=s.name, row=1, col=j)
fig.update_yaxes(title="density", col=1)
fig.update_layout(legend=legend_below)
save(fig, "end_of_distribution", 1300, 520, top=60, bottom=120)
