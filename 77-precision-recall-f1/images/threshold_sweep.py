"""Precision and recall pull against each other: the decision threshold of the Note's logistic regression slides
across the heart-disease test set (61 patients). Each dot is a patient at its predicted probability, in the lane
of its true class; dots right of the threshold are flagged. Right: precision, recall and F1 at that threshold.
Run: python threshold_sweep.py  -> threshold_sweep.gif, threshold_sweep_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).parent
GREEN, RED, ORANGE, GREY, BLUE = "#54A24B", "#E45756", "#F58518", "#BBBBBB", "#4C78A8"
df = pd.read_csv(HERE.parent / "data" / "heart.csv")
X_train, X_test, y_train, y_test = train_test_split(df.iloc[:, :-1], df.iloc[:, -1], test_size=0.2, random_state=2)
model = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_train, y_train)
p, y = model.predict_proba(X_test)[:, 1], y_test.to_numpy()
assert np.isclose(precision_score(y, p >= 0.5), 0.800, atol=5e-4) and np.isclose(recall_score(y, p >= 0.5), 0.966, atol=5e-4)
jit = np.random.default_rng(0).uniform(-0.28, 0.28, len(y))          # spread dots inside each lane
THRESH = np.round(np.r_[np.linspace(0.5, 0.05, 10), np.linspace(0.1, 0.95, 18), np.linspace(0.9, 0.5, 9)], 3)


def scores(t):
    pred = p >= t
    P = precision_score(y, pred, zero_division=0)
    return P, recall_score(y, pred), f1_score(y, pred, zero_division=0), pred


lo, hi = scores(0.1), scores(0.9)
assert lo[1] > hi[1] and lo[0] < hi[0]                                # the trade-off the Note states
print("t=0.1: P %.2f R %.2f | t=0.5: P %.2f R %.2f | t=0.9: P %.2f R %.2f" % (lo[0], lo[1], *scores(0.5)[:2], hi[0], hi[1]))


def frame(t):
    P, R, F, pred = scores(t)
    kind = np.where(pred & (y == 1), "TP", np.where(pred & (y == 0), "FP", np.where(~pred & (y == 1), "FN", "TN")))
    fig = make_subplots(rows=1, cols=2, column_widths=[0.64, 0.36], horizontal_spacing=0.1)
    fig.add_vrect(x0=t, x1=1.02, fillcolor=BLUE, opacity=0.08, line_width=0, row=1, col=1, exclude_empty_subplots=False)
    for k, col, name in (("TP", GREEN, "caught (TP)"), ("FN", ORANGE, "missed (FN)"), ("FP", RED, "false alarm (FP)"),
                         ("TN", GREY, "correctly cleared (TN)")):
        m = kind == k
        fig.add_trace(go.Scatter(x=p[m] if m.any() else [None], y=y[m] + jit[m] if m.any() else [None], mode="markers", name=f"{name}: {m.sum()}",
                                 marker=dict(color=col, size=15, line=dict(color="white", width=1))), 1, 1)
    fig.add_vline(x=t, line=dict(color="black", width=4), row=1, col=1)
    fig.add_annotation(x=min(max(t, 0.12), 0.88), y=1.5, text=f"threshold {t:.2f}", showarrow=False, yanchor="bottom",
                       font=dict(size=24), row=1, col=1)
    fig.add_trace(go.Bar(x=["precision", "recall", "F1"], y=[P, R, F], marker_color=[BLUE, ORANGE, "#6B6B6B"],
                         text=[f"{v:.2f}" for v in (P, R, F)], textposition="outside", textfont=dict(size=26),
                         showlegend=False), 1, 2)
    fig.update_xaxes(range=[-0.02, 1.02], title="predicted probability of disease", row=1, col=1)
    fig.update_yaxes(range=[-0.45, 1.75], tickvals=[0, 1], ticktext=["healthy", "disease"], row=1, col=1)
    fig.update_yaxes(range=[0, 1.15], showticklabels=False, row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=640, font=dict(family="Latin Modern Roman", size=22),
                      margin=dict(l=110, r=20, t=110, b=70),
                      legend=dict(orientation="h", x=0, y=1.02, yanchor="bottom", font=dict(size=21)))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".sweep_frames"
    tmp.mkdir(exist_ok=True)
    seq = [THRESH[0]] * 6 + list(THRESH) + [THRESH[-1]] * 8
    done = {}
    for k, t in enumerate(seq):
        if t in done:
            shutil.copy(tmp / f"{done[t]:03d}.png", tmp / f"{k:03d}.png")
        else:
            frame(t).write_image(tmp / f"{k:03d}.png")
            done[t] = k
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "threshold_sweep.gif")], check=True)
    ims = [Image.open(tmp / f"{done[t]:03d}.png").convert("RGB") for t in (0.5, 0.05, 0.7, 0.95)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "threshold_sweep_frames.png")
    shutil.rmtree(tmp)
