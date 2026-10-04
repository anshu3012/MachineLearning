"""The grouping experiment of section 5 (three near-copies of one signal + three noise features, 200 observations):
the six Elastic Net coefficients while l1_ratio sweeps from 0 (Ridge-like) to 1 (Lasso) at a fixed alpha of 0.1.
Run: python ratio_sweep.py  -> ratio_sweep.gif, ratio_sweep_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
import warnings
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from sklearn.linear_model import ElasticNet

warnings.simplefilter("ignore")
HERE = Path(__file__).parent
rng = np.random.default_rng(0)
n = 200
z = rng.standard_normal(n)
X = np.c_[z + 0.05 * rng.standard_normal(n), z + 0.05 * rng.standard_normal(n), z + 0.05 * rng.standard_normal(n),
          rng.standard_normal((n, 3))]
y = 3 * z + rng.standard_normal(n)
names = ["x1", "x2", "x3", "noise1", "noise2", "noise3"]
ratios = np.round(np.linspace(0, 1, 41), 3)
C = np.array([ElasticNet(alpha=0.1, l1_ratio=r, max_iter=100000).fit(X, y).coef_ for r in ratios])
for r in (0, 0.1, 0.5, 0.9, 1):
    print(r, C[np.argmin(abs(ratios - r))].round(2))
first_noise0 = ratios[np.argmax((C[:, 3:] == 0).all(1))]
first_x1_0 = ratios[np.argmax(C[:, 0] == 0)]
print("all noise exactly 0 from l1_ratio", first_noise0, "; x1 exactly 0 from", first_x1_0)
# the lesson: Ridge end keeps noise, the mix shares the weight and zeroes the noise, the Lasso end drops a copy
assert (C[0, 3:] != 0).all() and C[-1, 0] == 0 and (C[20, 3:] == 0).all() and np.ptp(C[20, :3]) < 0.2


def frame(k):
    c, r = C[k], ratios[k]
    if (c[3:] != 0).any():
        note = "noise features kept (small, not 0)"
    elif c[0] > 0.8 * c[2]:
        note = "noise features exactly 0, weight shared by x1, x2, x3"
    elif c[0] != 0:
        note = "noise features exactly 0, x1 is losing its share"
    else:
        note = "noise features exactly 0, but x1 is dropped too"
    fig = go.Figure(go.Bar(x=names, y=c, marker_color=["#4C78A8"] * 3 + ["#BBBBBB"] * 3,
                           text=[("0" if v == 0 else f"{v:.2f}").replace("-", "−") for v in c], textposition="outside",
                           textfont=dict(size=24), cliponaxis=False))
    fig.add_hline(y=0, line=dict(color="black", width=1))
    fig.update_layout(template="simple_white", width=900, height=600, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=24), margin=dict(l=90, r=20, t=130, b=60),
                      title=dict(text=f"l1_ratio = {r:.2f} (alpha 0.1)<br><span style='font-size:22px'>{note}</span>",
                                 x=0.5, y=0.95),
                      yaxis=dict(title="coefficient", range=[-0.15, 2.0]))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".sweep_frames"
    tmp.mkdir(exist_ok=True)
    last = len(ratios) - 1
    for k in range(last + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(last + 1, last + 11):
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "ratio_sweep.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 20, 36, last)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "ratio_sweep_frames.png")
    shutil.rmtree(tmp)
