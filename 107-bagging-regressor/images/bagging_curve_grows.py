"""The bagging regressor of section 3 (50 trees, 25 rows each drawn with replacement), built one tree at a time on the
two-bumps data. Grey: every tree so far; green: the newest tree and its drawn points; blue: their mean.
Run: python bagging_curve_grows.py  -> bagging_curve_grows.gif, bagging_curve_grows_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from sklearn.metrics import r2_score

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import X_line, X_test, X_train, fit, y_test, y_train  # noqa: E402  same data and models as the app

(single, r_single), (bag, r_bag) = fit("decision tree", n_estimators=50, max_samples=25, bootstrap=True)
curves = np.array([t.predict(X_line) for t in bag.estimators_])
tests = np.array([t.predict(X_test) for t in bag.estimators_])
r2 = {k: r2_score(y_test, tests[:k].mean(0)) for k in range(1, 51)}
assert np.allclose(curves.mean(0), bag.predict(X_line))      # the mean of the trees is the bagging prediction
assert abs(r2[50] - r_bag) < 1e-12
print("single tree R2", round(r_single, 3), {k: round(r2[k], 3) for k in (1, 2, 5, 10, 50)})
KS = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 40, 50]
x = X_line.ravel()


def frame(k):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X_train.ravel(), y=y_train, mode="markers", name="training points",
                             marker=dict(color="#FFD24C", size=7, opacity=0.5, line=dict(color="black", width=0.5))))
    for c in curves[:k - 1]:
        fig.add_trace(go.Scatter(x=x, y=c, mode="lines", showlegend=False, line=dict(color="#B8B8B8", width=1)))
    drawn = bag.estimators_samples_[k - 1]
    fig.add_trace(go.Scatter(x=X_train[drawn, 0], y=y_train[drawn], mode="markers", name="drawn by the newest tree",
                             marker=dict(color="#54A24B", size=11, line=dict(color="black", width=1))))
    fig.add_trace(go.Scatter(x=x, y=curves[k - 1], mode="lines", name=f"tree {k}", line=dict(color="#54A24B", width=2)))
    fig.add_trace(go.Scatter(x=x, y=curves[:k].mean(0), mode="lines", name=f"mean of {k} tree{'s' * (k > 1)}",
                             line=dict(color="#4C78A8", width=5)))
    fig.update_layout(template="simple_white", width=1100, height=650, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"{k} tree{'s' * (k > 1)}: test R² {r2[k]:.2f}", x=0.5, font_size=28),
                      xaxis=dict(title="x", range=[-5, 5]), yaxis=dict(title="y", range=[-0.5, 2.1]),
                      legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.8)"), margin=dict(l=70, r=20, t=70, b=60))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".bagging_curve_frames"
    tmp.mkdir(exist_ok=True)
    for i, k in enumerate(KS):
        frame(k).write_image(tmp / f"{i:03d}.png")
    for i in range(len(KS), len(KS) + 6):                   # hold the last frame
        shutil.copy(tmp / f"{len(KS) - 1:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "bagging_curve_grows.gif")], check=True)
    keys = [Image.open(tmp / f"{KS.index(k):03d}.png").convert("RGB") for k in (1, 3, 10, 50)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "bagging_curve_grows_frames.png")
    shutil.rmtree(tmp)
