"""What a perceptron does geometrically, in 3D. For the trained perceptron of section 8 (standardized inputs,
z = 5.82 x1 + 1.48 x2 + 1), z is a tilted plane above the input plane. Frame 1: the z plane over the 100 students;
frame 2: where it crosses height 0, the line z = 0; frame 3: the step function flattens z into two terraces,
1 on one side of the line and 0 on the other. Plotly 3D frames -> ffmpeg GIF, plus a grid for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from sklearn.linear_model import Perceptron
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=18)
GREEN, RED, BLUE = "#54A24B", "#E45756", "#4C78A8"
df = pd.read_csv(HERE.parent / "data" / "placement.csv")
X, y = df[["cgpa", "resume_score"]].values, df.placed.values
model = make_pipeline(StandardScaler(), Perceptron(random_state=0)).fit(X, y)
W1, W2, B = model[-1].coef_[0][0], model[-1].coef_[0][1], model[-1].intercept_[0]
assert (round(W1, 2), round(W2, 2), B) == (5.82, 1.48, 1.0)
Z = model[0].transform(X)
g = np.linspace(-2.5, 2.5, 60)
GX, GY = np.meshgrid(g, g)
ZZ = W1 * GX + W2 * GY + B
TITLES = ["z = 5.82·x₁ + 1.48·x₂ + 1 is a tilted plane above the students",
          "Where the plane crosses height 0: the line z = 0 (the decision boundary)",
          "The step function flattens z: 1 on one side of the line, 0 on the other"]


def frame(k):
    fig = go.Figure()
    zs = ZZ if k < 2 else (ZZ >= 0).astype(float) * 6
    fig.add_surface(x=GX, y=GY, z=zs, colorscale=[[0, RED], [0.5, "#F2F2F2"], [1, GREEN]], cmin=-15 if k < 2 else 0,
                    cmax=15 if k < 2 else 6, showscale=False, opacity=0.75)
    lxx = np.linspace(-2.5, 2.5, 400)                    # the line z = 0, clipped to the drawn square
    lyy = -(W1 * lxx + B) / W2
    keep = (lyy >= -2.5) & (lyy <= 2.5)
    if k >= 1:
        fig.add_scatter3d(x=lxx[keep], y=lyy[keep], z=np.zeros(keep.sum()), mode="lines",
                          line=dict(color=BLUE, width=10), name="z = 0")
    for lab, c, name in ((1, GREEN, "placed"), (0, RED, "not placed")):
        s = y == lab
        fig.add_scatter3d(x=Z[s, 0], y=Z[s, 1], z=np.zeros(s.sum()), mode="markers", name=name,
                          marker=dict(size=4, color=c))
    zt = "z" if k < 2 else "output (1 drawn as a raised terrace)"
    fig.update_layout(template="simple_white", width=1000, height=800, font=FONT,
                      title=dict(text=TITLES[k], x=0.5, y=0.95, font=dict(size=21)),
                      scene=dict(xaxis_title="x₁ CGPA", yaxis_title="x₂ resume", zaxis_title=zt,
                                 camera=dict(eye=dict(x=1.15, y=-1.25, z=0.7)), aspectmode="manual",
                                 aspectratio=dict(x=1, y=1, z=0.7)),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=0.02),
                      margin=dict(l=0, r=0, t=70, b=0))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".zp_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for k in range(3):
        keys.append(tmp / f"k{k}.png")
        frame(k).write_image(keys[-1])
    seq = [0] * 4 + [1] * 4 + [2] * 5
    for j, k in enumerate(seq):
        shutil.copy(keys[k], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse",
                    str(HERE / "z_plane.gif")], check=True)
    ims = [Image.open(keys[k]).convert("RGB") for k in (1, 2)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, h), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "z_plane_frames.png")
    shutil.rmtree(tmp)
