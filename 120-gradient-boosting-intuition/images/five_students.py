"""Gradient boosting on the five students (sections 4-9), learning rate 0.1: start at the mean 4.8, then each tree is
trained on the residuals and one tenth of it is added. Left: actual package (outline) and prediction (bar) per
student. Right: the residuals, shrinking stage by stage.
Run: python five_students.py  -> five_students.gif, five_students_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.tree import DecisionTreeRegressor

HERE = Path(__file__).parent
BLUE, RED, GREEN, GREY = "#4C78A8", "#E45756", "#54A24B", "#6B6B6B"
X = np.array([[90, 8], [100, 7], [110, 6], [120, 9], [80, 5]])
y = np.array([3, 4, 8, 6, 3], dtype=float)
LR, M = 0.1, 50
preds = [np.full(5, y.mean())]                      # stage 1: the mean, 4.8
for _ in range(M):
    tree = DecisionTreeRegressor(random_state=0).fit(X, y - preds[-1])   # target: the residuals
    preds.append(preds[-1] + LR * tree.predict(X))
assert np.allclose(preds[1], [4.62, 4.72, 5.12, 4.92, 4.62])           # pred2 in section 9
assert np.allclose(preds[2], [4.458, 4.648, 5.408, 5.028, 4.458])      # pred3
KS = [0, 1, 2, 3, 5, 10, 20, 30, 50]
students = [f"student {i}" for i in range(1, 6)]


def frame(m):
    res = y - preds[m]
    label = "the mean" if m == 0 else f"4.8 + 0.1 × (tree 1 + … + tree {m})" if m > 2 else \
        "4.8 + 0.1 × tree 1" if m == 1 else "4.8 + 0.1 × (tree 1 + tree 2)"
    fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=["package (LPA): actual and predicted",
                                                                      "residual = actual − predicted"])
    fig.add_trace(go.Bar(x=students, y=preds[m], marker_color=BLUE, name="predicted", width=0.6,
                         text=[f"{p:.2f}" for p in preds[m]], textposition="inside", textfont=dict(color="white", size=20)), 1, 1)
    fig.add_trace(go.Bar(x=students, y=y, name="actual", width=0.6, marker=dict(color="rgba(0,0,0,0)",
                                                                                line=dict(color="black", width=3))), 1, 1)
    fig.add_trace(go.Bar(x=students, y=res, marker_color=[RED if r < 0 else GREEN for r in res], width=0.6,
                         text=[f"{r:+.2f}" for r in res], textposition="outside", textfont=dict(size=20),
                         showlegend=False), 1, 2)
    fig.update_yaxes(range=[0, 9], title_text="LPA", row=1, col=1)
    fig.update_yaxes(range=[-2.6, 4], title_text="LPA", zeroline=True, zerolinecolor=GREY, row=1, col=2)
    fig.update_xaxes(tickangle=0, tickfont=dict(size=18))
    fig.update_annotations(font_size=24)
    fig.update_layout(template="simple_white", width=1300, height=640, barmode="overlay",
                      font=dict(family="Latin Modern Roman", size=20), margin=dict(l=70, r=20, t=110, b=60),
                      title=dict(text=f"after {m} tree{'s' * (m != 1)}: prediction = {label}", x=0.5, y=0.96, font_size=28),
                      legend=dict(x=0.01, y=0.98, font_size=20))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".five_frames"
    tmp.mkdir(exist_ok=True)
    for i, m in enumerate(KS):
        frame(m).write_image(tmp / f"{i:03d}.png")
    for i in range(len(KS), len(KS) + 5):                   # hold the last frame
        shutil.copy(tmp / f"{len(KS) - 1:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "five_students.gif")], check=True)
    keys = [Image.open(tmp / f"{KS.index(m):03d}.png").convert("RGB") for m in (0, 1, 2, 50)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "five_students_frames.png")
    shutil.rmtree(tmp)
