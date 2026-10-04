"""Note 76 (Plotly).
accuracy_count.gif + _frames.png (Section 2): the 61 heart-disease test patients are ticked one batch at a time,
  right (green) or wrong (red), for logistic regression and the decision tree; the running count becomes the accuracy.
imbalance.png (Section 6): the always-'not a threat' model on 100,000 passengers: accuracy 0.9999, threats caught 0 of 10.
Run: python accuracy_count.py"""
import shutil
import subprocess
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

warnings.simplefilter("ignore")
HERE = Path(__file__).parent
GREEN, RED, GREY, BLUE = "#54A24B", "#E45756", "#BBBBBB", "#4C78A8"
FONT = dict(family="Latin Modern Roman", size=22)
df = pd.read_csv(HERE.parent / "data" / "heart.csv")
Xtr, Xte, ytr, yte = train_test_split(df.iloc[:, :-1], df.iloc[:, -1], test_size=0.2, random_state=2)
models = [("Logistic regression", make_pipeline(StandardScaler(), LogisticRegression())),
          ("Decision tree", DecisionTreeClassifier(random_state=1))]
right = {n: (m.fit(Xtr, ytr).predict(Xte) == yte.values) for n, m in models}
N = len(yte)
assert N == 61 and right["Logistic regression"].sum() == 53 and right["Decision tree"].sum() == 51
COLS = 16
gx, gy = np.arange(N) % COLS, -(np.arange(N) // COLS)


def frame(k):
    f = make_subplots(rows=2, cols=1, vertical_spacing=0.16, subplot_titles=[
        f"{n}: {r[:k].sum()} right of {k}" + (f"  →  accuracy {r.sum() / N:.3f}" if k == N else "") for n, r in right.items()])
    for i, r in enumerate(right.values()):
        col = [GREY if j >= k else (GREEN if r[j] else RED) for j in range(N)]
        sym = ["circle" if j >= k or r[j] else "x" for j in range(N)]
        f.add_trace(go.Scatter(x=gx, y=gy, mode="markers", marker=dict(size=26, color=col, symbol=sym,
                                                                       line=dict(color="white", width=1))), i + 1, 1)
    f.update_xaxes(visible=False, range=[-0.7, COLS - 0.3])
    f.update_yaxes(visible=False, range=[-3.7, 0.7])
    f.update_layout(template="simple_white", width=1000, height=560, font=FONT, showlegend=False,
                    margin=dict(l=20, r=20, t=60, b=20))
    f.update_annotations(font_size=26)
    return f


ims = HERE / "imbalance.png"
cm = np.array([[99990, 0], [10, 0]])
acc = np.trace(cm) / cm.sum()
assert acc == 0.9999 and cm[1, 1] == 0
fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45], horizontal_spacing=0.18,
                    subplot_titles=("The 'always not a threat' model", "Two scores for the same model"))
fig.add_trace(go.Heatmap(z=[[1, 0], [0, 1]], x=["predicted 0", "predicted 1"], y=["actual 0", "actual 1"], showscale=False,
                         colorscale=[[0, "#F8D3D3"], [1, "#D6ECD2"]], text=[[f"{v:,}" for v in row] for row in cm],
                         texttemplate="%{text}", textfont=dict(size=28)), 1, 1)
fig.add_trace(go.Bar(x=["accuracy", "threats caught"], y=[acc * 100, 0], marker_color=[BLUE, RED], width=0.55,
                     text=["99.99%", "0 of 10 (0%)"], textposition="outside", textfont=dict(size=24)), 1, 2)
fig.update_yaxes(autorange="reversed", row=1, col=1)
fig.update_yaxes(range=[0, 115], title="percent", row=1, col=2)
fig.update_layout(template="simple_white", width=1100, height=500, font=FONT, showlegend=False,
                  margin=dict(l=110, r=20, t=60, b=50))
fig.update_annotations(font_size=24)
fig.write_image(ims, scale=2)

if __name__ == "__main__":
    tmp = HERE / ".acc_frames"
    tmp.mkdir(exist_ok=True)
    ks = list(range(0, N, 4)) + [N]
    for i, k in enumerate(ks):
        frame(k).write_image(tmp / f"{i:03d}.png")
    n = len(ks)
    for i in range(n, n + 8):                                     # hold the last frame
        shutil.copy(tmp / f"{n - 1:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "accuracy_count.gif")], check=True)
    keys = [Image.open(tmp / f"{ks.index(k):03d}.png").convert("RGB") for k in (24, N)]
    w, h = keys[0].size                                           # one column, so the counts stay readable in the PDF
    sheet = Image.new("RGB", (w, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, (0, i * (h + 16)))
    sheet.save(HERE / "accuracy_count_frames.png")
    shutil.rmtree(tmp)
