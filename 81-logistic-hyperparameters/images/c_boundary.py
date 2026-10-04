"""C on a two-feature dataset (the playground's binary dataset: make_classification, 300 points, class_sep 0.8, random
state 1; all 300 points used). C falls from 100 to 0.001 with the default L2 penalty. Left: the decision boundary
(p = 0.5) and the band where the model is unsure (0.1 < p < 0.9). Right: the two coefficients.
As C falls the coefficients shrink towards 0 and the unsure band widens.
Run: python c_boundary.py  -> c_boundary.gif, c_boundary_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression

HERE = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"
X, y = make_classification(n_samples=300, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1,
                           class_sep=0.8, random_state=1)
Cs = np.logspace(2, -3, 26)
M = [LogisticRegression(C=c, max_iter=10000).fit(X, y) for c in Cs]
coef = np.array([m.coef_[0] for m in M])
acc = [m.score(X, y) for m in M]
size = np.abs(coef).max(1)
for c in (100, 1, 0.01, 0.001):
    k = int(np.argmin(abs(Cs - c)))
    print(f"C {Cs[k]:g}: coef {coef[k].round(3)}, training accuracy {acc[k]:.3f}")
assert all(a > b for a, b in zip(size, size[1:]))            # the lesson: smaller C, smaller coefficients
xr, yr = [X[:, 0].min() - 0.5, X[:, 0].max() + 0.5], [X[:, 1].min() - 0.5, X[:, 1].max() + 0.5]
gx, gy = np.linspace(*xr, 160), np.linspace(*yr, 160)
GX, GY = np.meshgrid(gx, gy)
top = float(np.abs(coef).max()) * 1.2


def frame(k):
    m = M[k]
    P = m.predict_proba(np.c_[GX.ravel(), GY.ravel()])[:, 1].reshape(GX.shape)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.62, 0.38], horizontal_spacing=0.12,
                        subplot_titles=("pale band: unsure (0.1 < p < 0.9)", "coefficients"))
    fig.add_trace(go.Contour(x=gx, y=gy, z=P, zmin=0, zmax=1, showscale=False, line=dict(width=0),
                             contours=dict(start=0.1, end=0.9, size=0.4),
                             colorscale=[[0, "#C9DAEC"], [0.5, "#FFFFFF"], [1, "#FDDDB8"]], opacity=0.9), 1, 1)
    fig.add_trace(go.Contour(x=gx, y=gy, z=P, showscale=False, contours=dict(start=0.5, end=0.5, size=1, coloring="lines"),
                             line=dict(width=5), colorscale=[[0, "black"], [1, "black"]]), 1, 1)
    for cls, col in ((0, BLUE), (1, ORANGE)):
        fig.add_trace(go.Scatter(x=X[y == cls, 0], y=X[y == cls, 1], mode="markers",
                                 marker=dict(color=col, size=8, line=dict(color="white", width=1))), 1, 1)
    fig.add_trace(go.Bar(x=["w₁", "w₂"], y=m.coef_[0], marker_color=GREY,
                         text=[f"{v:.2f}".replace("-", "−") for v in m.coef_[0]], textposition="outside",
                         textfont=dict(size=24), cliponaxis=False), 1, 2)
    fig.update_xaxes(title="x₁", range=xr, row=1, col=1)
    fig.update_yaxes(title="x₂", range=yr, row=1, col=1)
    fig.update_yaxes(range=[-top, top], zeroline=True, zerolinecolor="black", row=1, col=2)
    fig.update_layout(template="simple_white", width=1150, height=600, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), margin=dict(l=80, r=20, t=130, b=70),
                      title=dict(text=f"C = {Cs[k]:.3g}   ·   training accuracy {acc[k]:.2f}", x=0.5, y=0.96))
    fig.update_annotations(font_size=24)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".cb_frames"
    tmp.mkdir(exist_ok=True)
    N = len(Cs)
    for k in range(N):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(N, N + 8):
        shutil.copy(tmp / f"{N - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "c_boundary.gif")], check=True)
    keys = [Image.open(tmp / f"{int(np.argmin(abs(Cs - c))):03d}.png").convert("RGB") for c in (100, 1, 0.01, 0.001)]
    w_, h_ = keys[0].size
    sheet = Image.new("RGB", (2 * w_ + 16, 2 * h_ + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w_ + 16), (i // 2) * (h_ + 16)))
    sheet.save(HERE / "c_boundary_frames.png")
    shutil.rmtree(tmp)
