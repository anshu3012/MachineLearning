"""The missing indicator's weight being learned: logistic regression on Age (mean filled), Fare and Age_NA, the model
of Section 6.3, stopped after 0, 1, 2, ... solver iterations (lbfgs, started from all-zero weights). Each frame draws
the predicted chance of survival against Fare for Age_NA = 0 and Age_NA = 1 at the same filled age; the two curves
start as one and move apart as the weight on Age_NA grows to -0.30. Our own design; no source to credit.
Plotly frames -> ffmpeg GIF + _frames.png grid. Run: python indicator_training.py"""
import shutil
import subprocess
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=22)

df = pd.read_csv(HERE.parent / "data" / "titanic.csv", usecols=["Age", "Fare", "Survived"])
X_tr, X_te, y_tr, y_te = train_test_split(df[["Age", "Fare"]], df["Survived"], test_size=0.2, random_state=2)
si = SimpleImputer(add_indicator=True).fit(X_tr)
Xt = si.transform(X_tr)
mean_age = si.statistics_[0]
fares = np.linspace(0, 150, 200)
ITERS = [0, 1, 2, 3, 4, 6, 8, 10, 14, 20, 100]


def model(k):
    """Weights (intercept, age, fare, Age_NA) after k solver iterations."""
    if k == 0:
        return 0.0, np.zeros(3)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")                       # stopping early is the point
        m = LogisticRegression(max_iter=k).fit(Xt, y_tr)
    return m.intercept_[0], m.coef_[0]


def frame(k):
    b0, w = model(k)
    fig = go.Figure()
    for na, colour, name in [(0, BLUE, "Age recorded (Age_NA = 0)"), (1, ORANGE, "Age missing (Age_NA = 1)")]:
        z = b0 + w[0] * mean_age + w[1] * fares + w[2] * na
        fig.add_trace(go.Scatter(x=fares, y=100 / (1 + np.exp(-z)), mode="lines", name=name,
                                 line=dict(color=colour, width=5, dash="solid" if na == 0 else "dash")))
    fig.add_hline(y=50, line=dict(color=GREY, width=1.5, dash="dot"))
    fig.add_annotation(x=0.03, y=0.95, xref="paper", yref="paper", xanchor="left", showarrow=False,
                       text=f"weight on Age_NA: {w[2]:+.2f}", font=dict(size=28, color=ORANGE))
    done = " (training finished)" if k == ITERS[-1] else ""
    fig.update_layout(template="simple_white", width=1000, height=580, font=FONT,
                      title=dict(text=f"after {k} training iterations{done}", x=0.5),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.22),
                      margin=dict(l=90, r=20, t=70, b=140))
    fig.update_xaxes(title="Fare")
    fig.update_yaxes(title="predicted chance of survival (%)", range=[20, 80])
    return fig, w


if __name__ == "__main__":
    tmp = HERE / ".ind_frames"
    tmp.mkdir(exist_ok=True)
    for i, k in enumerate(ITERS):
        fig, w = frame(k)
        fig.write_image(tmp / f"{i:03d}.png")
        print(k, np.round(w, 3))
    assert round(w[2], 2) == -0.30, w                         # the Note's final weight on Age_NA
    last = len(ITERS) - 1
    for i in range(last + 1, last + 6):                       # hold the final frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "indicator_training.gif")], check=True)
    keys = [Image.open(tmp / f"{i:03d}.png").convert("RGB") for i in (0, 3, 6, last)]
    w_, h_ = keys[0].size
    sheet = Image.new("RGB", (2 * w_ + 16, 2 * h_ + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w_ + 16), (i // 2) * (h_ + 16)))
    sheet.save(HERE / "indicator_training_frames.png")
    shutil.rmtree(tmp)
