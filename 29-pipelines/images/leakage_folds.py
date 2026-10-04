"""Data leakage in cross-validation, fold by fold, on data with NOTHING to learn (made-up on purpose: with pure noise
the honest accuracy is known to be 50%, so any score above it is leakage).
200 observations, 2,000 random features, random 0/1 target. Two ways to keep the 20 "best" features:
  leaky: SelectKBest fitted on all 200 rows first, then 5-fold cross-validation of the model only;
  pipeline: SelectKBest inside the pipeline, so each fold picks its features from its 4 training parts only.
Bars: one dataset (seed 0), fold by fold. Final frame: the mean over 20 datasets (seeds 0..19).
After scikit-learn User Guide, "Common pitfalls and recommended practices" (data leakage during pre-processing).
Plotly frames -> ffmpeg GIF + _frames.png grid. Run: python leakage_folds.py -> leakage_folds.gif, leakage_folds_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline

HERE = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=24)


def both(seed):
    rng = np.random.default_rng(seed)
    X, y = rng.normal(size=(200, 2000)), rng.integers(0, 2, 200)
    leaky = cross_val_score(LogisticRegression(), SelectKBest(f_classif, k=20).fit_transform(X, y), y, cv=5)
    honest = cross_val_score(make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression()), X, y, cv=5)
    return leaky * 100, honest * 100


leaky, honest = both(0)
means = np.array([[a.mean(), b.mean()] for a, b in map(both, range(20))]).mean(0)
print("seed 0 folds:", leaky.round(1), honest.round(1), "| mean of 20 datasets:", means.round(1))
assert means.round(0).tolist() == [78, 51]


def frame(k):                                                   # k folds shown; k == 6: the 20-dataset means
    fig = go.Figure()
    x = [f"fold {i}" for i in range(1, 6)]
    if k <= 5:
        show = lambda v: [v[i] if i < k else None for i in range(5)]
        fig.add_trace(go.Bar(x=x, y=show(leaky), marker_color=ORANGE, name="select features first, then cross-validate",
                             text=[f"{v:.0f}" for v in leaky], textposition="outside"))
        fig.add_trace(go.Bar(x=x, y=show(honest), marker_color=BLUE, name="selection inside the pipeline",
                             text=[f"{v:.0f}" for v in honest], textposition="outside"))
        title = f"Noise data: accuracy on test fold {k}" if k < 5 else "Noise data: accuracy on all 5 test folds"
    else:
        for name, v, c in (("select features first,<br>then cross-validate", means[0], ORANGE),
                           ("selection inside<br>the pipeline", means[1], BLUE)):
            fig.add_trace(go.Bar(x=[name], y=[v], marker_color=c, text=[f"<b>{v:.0f}%</b>"], textposition="outside",
                                 width=0.5, showlegend=False))
        title = "Mean accuracy over 20 noise datasets"
    fig.add_hline(y=50, line=dict(color=GREY, dash="dash", width=3))
    fig.add_annotation(x=1, xref="paper", y=50, text="guessing: 50%", showarrow=False, xanchor="right", yshift=16,
                       font=dict(color=GREY, size=22))
    fig.update_xaxes(range=[-0.5, 5.6] if k <= 5 else [-0.5, 2.1])
    fig.update_yaxes(title="accuracy (%)", range=[0, 100])
    fig.update_layout(template="simple_white", width=1200, height=620, font=FONT, bargap=0.3,
                      title=dict(text=title, x=0.5, y=0.97), legend=dict(orientation="h", x=0.5, xanchor="center", y=1.12),
                      margin=dict(l=90, r=20, t=130, b=90))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".leak_frames"
    tmp.mkdir(exist_ok=True)
    ks = [1, 2, 3, 4, 5, 5, 6, 6, 6, 6]                         # hold the last fold, then hold the means
    for j, k in enumerate(ks):
        frame(k).write_image(tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "leakage_folds.gif")], check=True)
    keys = [Image.open(tmp / f"{j:03d}.png").convert("RGB") for j in (4, 9)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (w, 2 * h + 16), "white")
    for j, im in enumerate(keys):
        sheet.paste(im, (0, j * (h + 16)))
    sheet.save(HERE / "leakage_folds_frames.png")
    shutil.rmtree(tmp)
