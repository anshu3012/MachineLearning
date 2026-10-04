"""Two Plotly-frame animations for the ROC Note.
roc_eight: the first 4 diabetic and first 4 healthy patients of the test set (lr_probs.csv, written by roc.py). The
  threshold drops past one patient per frame; the 2 x 2 counts are small enough to check by hand and each frame adds
  one point of the ROC staircase.
auc_two: the ROC curves of logistic regression and the depth-3 decision tree on the 154 test patients, drawn left to
  right with the area under each curve filling in and its running value shown; the final areas are the two AUCs.
Run: python roc_small.py -> roc_eight.gif/_frames.png, auc_two.gif/_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
BLUE, RED, ORANGE, GREEN, GREY = "#4C78A8", "#E45756", "#F58518", "#54A24B", "#BBBBBB"
FONT = dict(family="Latin Modern Roman", size=22)
d = pd.read_csv(HERE / "lr_probs.csv")


def render(figs, name, fps, keys, scale, hold=8):
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


# ---- 1. eight patients ---------------------------------------------------------------------------------------
e = pd.concat([d[d.y == 1].head(4), d[d.y == 0].head(4)]).sort_values("p", ascending=False).reset_index(drop=True)
print(e.round(2).T.to_string())
pts = [(0.0, 0.0)]
for k in range(1, 9):
    f = e.head(k)
    pts.append(((f.y == 0).sum() / 4, (f.y == 1).sum() / 4))
print(pts)


def eight(k):
    thr = "above 0.92" if k == 0 else f"{e.p[k - 1]:.2f}"
    tp, fp = int((e.y[:k] == 1).sum()), int((e.y[:k] == 0).sum())
    fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45], horizontal_spacing=0.12, subplot_titles=(
        f"TP {tp}, FN {4 - tp}, FP {fp}, TN {4 - fp}", f"TPR = {tp}/4 = {tp / 4:g},  FPR = {fp}/4 = {fp / 4:g}"))
    if k:
        fig.add_shape(type="rect", x0=e.p[k - 1] - 0.012, x1=1.03, y0=-0.5, y1=1.5, fillcolor="#FAD7B5", line_width=0,
                      layer="below", row=1, col=1)
        fig.add_vline(x=e.p[k - 1] - 0.012, line=dict(color=ORANGE, width=4, dash="dot"), row=1, col=1)
    for cls, col in ((1, RED), (0, BLUE)):
        m = e.y == cls
        fig.add_trace(go.Scatter(x=e.p[m], y=[cls] * 4, mode="markers+text", text=[f"{v:.2f}" for v in e.p[m]],
                                 textposition="top center", marker=dict(size=22, color=col)), 1, 1)
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", line=dict(color=GREY, width=2, dash="dash")), 1, 2)
    P = np.array(pts[:k + 1])
    fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="lines+markers", line=dict(color=BLUE, width=4),
                             marker=dict(size=11, color=BLUE)), 1, 2)
    fig.add_trace(go.Scatter(x=[P[-1, 0]], y=[P[-1, 1]], mode="markers", marker=dict(size=20, color=ORANGE)), 1, 2)
    fig.update_xaxes(title="predicted probability of diabetes", range=[-0.06, 1.06], row=1, col=1)
    fig.update_yaxes(range=[-0.5, 1.5], tickvals=[0, 1], ticktext=["healthy", "diabetic"], row=1, col=1)
    fig.update_xaxes(title="false positive rate", range=[-0.05, 1.05], dtick=0.25, row=1, col=2)
    fig.update_yaxes(title="true positive rate", range=[-0.05, 1.08], dtick=0.25, row=1, col=2)
    fig.update_layout(template="simple_white", width=1150, height=560, font=FONT, showlegend=False,
                      margin=dict(l=100, r=20, t=130, b=70),
                      title=dict(text=f"threshold {thr}: flag everyone in the shaded region", x=0.5, y=0.96))
    fig.update_annotations(font_size=24)
    return fig


# ---- 2. two models, area filling in ----------------------------------------------------------------------------
df = pd.read_csv(HERE.parent / "data" / "diabetes.csv")
X, y = df.drop(columns="Outcome"), df["Outcome"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
assert np.allclose(yte.values, d.y.values)
tree = DecisionTreeClassifier(max_depth=3, random_state=0).fit(Xtr, ytr)
curves = {"logistic regression": roc_curve(yte, d.p)[:2], "decision tree (depth 3)": roc_curve(yte, tree.predict_proba(Xte)[:, 1])[:2]}
aucs = {"logistic regression": roc_auc_score(yte, d.p), "decision tree (depth 3)": roc_auc_score(yte, tree.predict_proba(Xte)[:, 1])}
print(aucs)
assert round(aucs["logistic regression"], 3) == 0.823 and round(aucs["decision tree (depth 3)"], 3) == 0.788


def upto(fpr, tpr, x):
    """The curve cut at false positive rate x."""
    keep = fpr <= x
    fx, ty = list(fpr[keep]), list(tpr[keep])
    if fx[-1] < x:
        ty.append(np.interp(x, fpr, tpr)); fx.append(x)
    return np.array(fx), np.array(ty)


def two(x):
    titles, parts = [], []
    for n, (fpr, tpr) in curves.items():
        fx, ty = upto(fpr, tpr, x)
        area = float(np.sum(np.diff(fx) * (ty[1:] + ty[:-1]) / 2))
        parts.append((fx, ty))
        titles.append(f"{n}<br>area so far {area:.3f}" + (" = AUC" if x >= 1 else ""))
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=titles)
    for c, ((fx, ty), col, fill) in enumerate(zip(parts, (BLUE, GREEN), ("rgba(76,120,168,0.25)", "rgba(84,162,75,0.25)")), 1):
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", line=dict(color=GREY, width=2, dash="dash")), 1, c)
        fig.add_trace(go.Scatter(x=fx, y=ty, mode="lines", line=dict(color=col, width=5), fill="tozeroy", fillcolor=fill), 1, c)
        fig.update_xaxes(title="false positive rate", range=[-0.02, 1.02], row=1, col=c)
        fig.update_yaxes(range=[-0.02, 1.05], row=1, col=c)
    fig.update_yaxes(title_text="true positive rate", row=1, col=1)
    fig.update_layout(template="simple_white", width=1150, height=600, font=FONT, showlegend=False,
                      margin=dict(l=80, r=20, t=110, b=70))
    fig.update_annotations(font_size=24)
    return fig


if __name__ == "__main__":
    render([eight(k) for k in range(9)], "roc_eight", 1, [0, 2, 3, 8], 900, hold=4)
    xs = np.round(np.linspace(0, 1, 41), 3)
    render([two(x) for x in xs], "auc_two", 8, [4, 12, 24, 40], 900, hold=14)
