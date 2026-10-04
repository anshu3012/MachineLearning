"""The ML stage of loan screening on real data. Data: the German credit dataset (Hofmann 1994; UCI Statlog, OpenML
31), 1,000 past borrowers, 300 of whom did not repay ("bad"). A logistic regression learns from 700 of them and
scores the other 300 with a chance of not repaying, out of 100. Applications above a cut-off are rejected; the rest
go to a loan officer. The animation lowers the cut-off from 90 to 20.
Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.compose import make_column_transformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
GREEN, RED, GREY = "#54A24B", "#E45756", "#6B6B6B"

df = pd.read_csv(HERE.parent / "data" / "credit_g.csv")
y = (df.pop("class") == "bad").astype(int).values
assert len(df) == 1000 and y.sum() == 300
cat = df.select_dtypes("object").columns.tolist()
num = [c for c in df.columns if c not in cat]
Xtr, Xte, ytr, yte = train_test_split(df, y, test_size=300, stratify=y, random_state=0)
model = make_pipeline(make_column_transformer((OneHotEncoder(handle_unknown="ignore"), cat), (StandardScaler(), num)),
                      LogisticRegression(max_iter=2000)).fit(Xtr, ytr)
score = 100 * model.predict_proba(Xte)[:, 1]
CUTS = [90, 80, 70, 60, 50, 40, 30, 20]


def counts(c):
    rej = score > c
    return int((rej & (yte == 1)).sum()), int((rej & (yte == 0)).sum()), int((~rej).sum())


assert [counts(c) for c in (80, 50, 20)] == [(9, 3, 288), (38, 20, 242), (72, 82, 146)]
jit = np.random.default_rng(0).uniform(-0.3, 0.3, len(score))


def frame(c):
    caught, wrong, passed = counts(c)
    fig = go.Figure()
    for lab, col, name, yy in ((0, GREEN, "repaid", 0), (1, RED, "did not repay", 1)):
        m = yte == lab
        fig.add_scatter(x=score[m], y=yy + jit[m], mode="markers", name=name,
                        marker=dict(size=9, color=col, opacity=0.75))
    fig.add_vrect(x0=c, x1=100, fillcolor=RED, opacity=0.08, line_width=0)
    fig.add_vline(x=c, line=dict(color="black", width=3))
    fig.add_annotation(x=c + 1, y=1.62, text="rejected →", showarrow=False, xanchor="left", font=dict(size=18))
    fig.add_annotation(x=c - 1, y=1.62, text="← to the loan officer", showarrow=False, xanchor="right",
                       font=dict(size=18))
    fig.update_layout(template="simple_white", width=1100, height=640, font=FONT,
                      title=dict(text=f"Cut-off {c}: rejects <b>{caught}</b> of 90 who did not repay and "
                                      f"<b>{wrong}</b> of 210 who did; {passed} go to the officer",
                                 x=0.5, y=0.95, font=dict(size=20)),
                      xaxis=dict(title="model's chance of not repaying (out of 100)", range=[0, 100]),
                      yaxis=dict(tickvals=[0, 1], ticktext=["repaid", "did not<br>repay"], range=[-0.6, 1.8]),
                      showlegend=False, margin=dict(l=110, r=30, t=80, b=80))
    return fig


if __name__ == "__main__":
    for c in CUTS:
        print(c, counts(c))
    tmp = HERE / ".lt_frames"
    tmp.mkdir(exist_ok=True)
    keys = {}
    for c in CUTS:
        keys[c] = tmp / f"c{c}.png"
        frame(c).write_image(keys[c])
    seq = [c for c in CUTS for _ in range(2)] + [CUTS[-1]] * 3
    for j, c in enumerate(seq):
        shutil.copy(keys[c], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=820:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "loan_threshold.gif")], check=True)
    shutil.copy(keys[50], HERE / "loan_threshold_frames.png")     # one readable frame for the PDF
    shutil.rmtree(tmp)
