"""Plotly chart for Note 40: the three fill values after each iteration (linear regression and BayesianRidge),
with the true hidden values. Run: python convergence.py -> convergence.png, convergence.pdf"""
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer
from sklearn.linear_model import LinearRegression

warnings.filterwarnings("ignore")   # "early stopping criterion not reached": we stop on purpose at each max_iter
here = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"

# the 5-row toy table, built exactly as in the Notebook
df = np.round(pd.read_csv(here.parent / "data" / "50_Startups.csv")
              [["R&D Spend", "Administration", "Marketing Spend"]] / 10000)
df = df.sample(5, random_state=np.random.RandomState(9)).reset_index(drop=True)
truth = [df.iloc[1, 0], df.iloc[3, 1], df.iloc[4, 2]]
df.iloc[1, 0] = df.iloc[3, 1] = df.iloc[4, 2] = np.nan
rows, cols = [1, 3, 4], [0, 1, 2]


def fills(estimator, n):
    out = [df.fillna(df.mean()).values[rows, cols]]
    for m in range(1, n + 1):
        imp = IterativeImputer(estimator=estimator, max_iter=m, tol=0, random_state=0)
        out.append(imp.fit_transform(df)[rows, cols])
    return np.array(out)


its = list(range(11))
lin, bay = fills(LinearRegression(), 10), fills(None, 10)
names = ["R&D Spend (row 2)", "Administration (row 4)", "Marketing Spend (row 5)"]
fig = make_subplots(rows=1, cols=3, subplot_titles=names, horizontal_spacing=0.08)
for j in range(3):
    first = j == 0
    fig.add_trace(go.Scatter(x=its, y=lin[:, j], name="linear regression", showlegend=first, mode="lines+markers",
                             line=dict(color=BLUE, width=3), marker_size=8), row=1, col=j + 1)
    fig.add_trace(go.Scatter(x=its, y=bay[:, j], name="BayesianRidge (default)", showlegend=first,
                             mode="lines+markers", line=dict(color=ORANGE, width=3, dash="dash"), marker_size=8),
                  row=1, col=j + 1)
    fig.add_trace(go.Scatter(x=[0, 10], y=[truth[j]] * 2, name="true value", showlegend=first, mode="lines",
                             line=dict(color=GREY, width=2, dash="dot")), row=1, col=j + 1)
    fig.update_xaxes(title_text="iteration", dtick=2, row=1, col=j + 1)
fig.update_yaxes(title_text="filled value (tens of thousands)", row=1, col=1)
fig.update_annotations(font_size=20)
fig.update_layout(template="simple_white", width=1200, height=520, font=dict(family="Latin Modern Roman", size=18),
                  margin=dict(l=80, r=20, t=50, b=120),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2))
fig.write_image(here / "convergence.png", scale=2)
fig.write_image(here / "convergence.pdf")
print("LR", lin.round(2).tolist(), "\nBR", bay.round(2).tolist(), "\ntruth", truth)
