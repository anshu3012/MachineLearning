"""The 61 heart-disease test patients dropped one by one into the 2 x 2 confusion matrix (scikit-learn layout: rows
actual, columns predicted) of logistic regression and of the decision tree. Green cells are the diagonal (correct),
red cells the two kinds of mistake. The last frame gives accuracy = diagonal / total for each model.
Then: the always-'no threat' model while the share of threats grows from 0.01 percent to 50 percent.
Run: python matrix_fill.py -> matrix_fill.gif/_frames.png, imbalance_sweep.gif/_frames.png (Plotly frames + ffmpeg)"""
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
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

warnings.simplefilter("ignore")
HERE = Path(__file__).parent
GREEN, RED, BLUE = "#54A24B", "#E45756", "#4C78A8"
FONT = dict(family="Latin Modern Roman", size=22)
df = pd.read_csv(HERE.parent / "data" / "heart.csv")
Xtr, Xte, ytr, yte = train_test_split(df.iloc[:, :-1], df.iloc[:, -1], test_size=0.2, random_state=2)
models = [("Logistic regression", make_pipeline(StandardScaler(), LogisticRegression())),
          ("Decision tree", DecisionTreeClassifier(random_state=1))]
yt = yte.to_numpy()
pred = {n: m.fit(Xtr, ytr).predict(Xte) for n, m in models}
N = len(yt)
assert confusion_matrix(yt, pred["Logistic regression"]).tolist() == [[25, 7], [1, 28]]     # the Note's matrices
assert confusion_matrix(yt, pred["Decision tree"]).tolist() == [[25, 7], [3, 26]]
print({n: confusion_matrix(yt, p).tolist() for n, p in pred.items()})
NAME = {(0, 0): "TN", (0, 1): "FP", (1, 0): "FN", (1, 1): "TP"}
PER = 8                                                         # dots per row inside a cell


def render(figs, name, fps, keys, scale, hold=10):
    tmp = HERE / f".{name}_frames"
    tmp.mkdir(exist_ok=True)
    for k, f in enumerate(figs):
        f.write_image(tmp / f"{k:03d}.png")
    for k in range(len(figs), len(figs) + hold):
        shutil.copy(tmp / f"{len(figs) - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(tmp / "%03d.png"), "-vf",
                    f"scale={scale}:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / f"{name}_frames.png")
    shutil.rmtree(tmp)


def fill_frame(k):
    titles = []
    for n, p in pred.items():
        ok = int((p[:k] == yt[:k]).sum())
        titles.append(f"{n}<br>" + (f"accuracy = {ok} / {N} = {ok / N:.3f}" if k == N else f"{k} of {N} patients placed"))
    f = make_subplots(rows=1, cols=2, horizontal_spacing=0.14, subplot_titles=titles)
    for c, (n, p) in enumerate(pred.items(), 1):
        for (a, b), nm in NAME.items():
            good = a == b
            f.add_shape(type="rect", x0=b, x1=b + 1, y0=1 - a, y1=2 - a, row=1, col=c, layer="below",
                        fillcolor="#E3F1DF" if good else "#FBE3E3", line=dict(color="black", width=2))
            m = (yt[:k] == a) & (p[:k] == b)
            cnt = int(m.sum())
            j = np.arange(cnt)
            f.add_trace(go.Scatter(x=b + 0.1 + (j % PER) * 0.8 / (PER - 1), y=1 - a + 0.62 - (j // PER) * 0.13,
                                   mode="markers", marker=dict(size=11, color=GREEN if good else RED)), 1, c)
            f.add_annotation(x=b + 0.5, y=1 - a + 0.85, text=f"<b>{nm}: {cnt}</b>", showarrow=False, row=1, col=c,
                             font=dict(size=24))
        f.update_xaxes(range=[-0.02, 2.02], tickvals=[0.5, 1.5], ticktext=["predicted 0<br>(no disease)", "predicted 1<br>(disease)"],
                       showline=False, ticks="", row=1, col=c)
        f.update_yaxes(range=[-0.02, 2.02], tickvals=[1.5, 0.5], ticktext=["actual 0", "actual 1"], showline=False,
                       ticks="", row=1, col=c)
    f.update_layout(template="simple_white", width=1200, height=620, font=FONT, showlegend=False,
                    margin=dict(l=100, r=20, t=110, b=90))
    f.update_annotations(selector=dict(yref="paper"), font_size=24)
    return f


def sweep_frame(share):
    n, threats = 100_000, int(round(100_000 * share))
    acc = (n - threats) / n
    f = go.Figure(go.Bar(x=["accuracy", "share of threats caught<br>(recall)"], y=[acc, 0], marker_color=[BLUE, RED],
                         text=[f"{acc * 100:.2f}%", "0%"], textposition="outside", textfont=dict(size=30), cliponaxis=False))
    f.update_layout(template="simple_white", width=800, height=620, font=FONT, showlegend=False,
                    margin=dict(l=70, r=20, t=140, b=90), yaxis=dict(range=[0, 1.12], tickformat=".0%"),
                    title=dict(text=f"threats: {threats:,} of {n:,} passengers ({share * 100:g}%)<br>"
                                    "<span style='font-size:22px'>model: always says \"not a threat\"</span>", x=0.5, y=0.95))
    return f


if __name__ == "__main__":
    ks = list(range(0, N + 1))
    render([fill_frame(k) for k in ks], "matrix_fill", 6, [8, 24, 44, N], 900)
    shares = [0.0001, 0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
    render([sweep_frame(s) for s in shares], "imbalance_sweep", 2, [0, 5, 8, len(shares) - 1], 640, hold=6)
