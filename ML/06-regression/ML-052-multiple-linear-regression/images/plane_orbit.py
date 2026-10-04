"""Multiple linear regression with two inputs, seen from all sides: the points, then the fitted plane, then each
point's error as a stick to the plane, while the camera circles once (Plotly frames + ffmpeg ->
plane_orbit.gif, plane_orbit_frames.png). Same data and model as plane.py."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED = "#4C78A8", "#F58518", "#54A24B", "#E45756"
X, y = make_regression(n_samples=100, n_features=2, n_informative=2, noise=50, random_state=7)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3)
lr = LinearRegression().fit(X_train, y_train)
assert np.allclose(lr.coef_.round(1), [58.6, 29.1]) and round(lr.intercept_, 1) == -1.9
yhat = lr.predict(X)
above = y > yhat
g = np.linspace(-3, 3, 20)
G1, G2 = np.meshgrid(g, g)
Z = lr.intercept_ + lr.coef_[0] * G1 + lr.coef_[1] * G2
N, PLANE, STICKS = 48, 8, 18                                   # frames; plane appears at 8, sticks at 18


def sticks(mask, colour):
    sx, sy, sz = [], [], []
    for (a, b), t, p in zip(X[mask], y[mask], yhat[mask]):
        sx += [a, a, None]; sy += [b, b, None]; sz += [t, p, None]
    return go.Scatter3d(x=sx, y=sy, z=sz, mode="lines", line=dict(color=colour, width=4))


def frame(k):
    ang = -2.25 + 2 * np.pi * k / N                            # start at plane.py's view, circle once
    fig = go.Figure()
    if k >= PLANE:
        fig.add_trace(go.Surface(x=G1, y=G2, z=Z, colorscale=[[0, ORANGE], [1, ORANGE]], opacity=0.4, showscale=False))
    if k >= STICKS:
        fig.add_trace(sticks(above, GREEN))
        fig.add_trace(sticks(~above, RED))
    fig.add_trace(go.Scatter3d(x=X[:, 0], y=X[:, 1], z=y, mode="markers",
                               marker=dict(size=4, color=BLUE, line=dict(width=0.5, color="white"))))
    title = ("100 observations, two features" if k < PLANE else "The fitted plane" if k < STICKS
             else "Errors: green above the plane, red below")
    fig.update_layout(template="simple_white", width=800, height=640, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=20), margin=dict(l=0, r=0, t=50, b=0),
                      title=dict(text=title, x=0.5, y=0.97), scene_aspectmode="cube",
                      scene=dict(xaxis=dict(title="feature1", range=[-3.2, 3.2], tickfont=dict(size=15), dtick=2),
                                 yaxis=dict(title="feature2", range=[-3.2, 3.2], tickfont=dict(size=15), dtick=2),
                                 zaxis=dict(title="target", range=[-250, 250], tickfont=dict(size=15), dtick=200),
                                 camera=dict(eye=dict(x=2.05 * np.cos(ang), y=2.05 * np.sin(ang), z=0.6))))
    return fig


if __name__ == "__main__":
    print("points above the plane:", above.sum(), "below:", (~above).sum(), "target range", y.min().round(), y.max().round())
    tmp = HERE / ".orbit_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(N):
        frame(k).write_image(tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "8", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "plane_orbit.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, PLANE + 2, STICKS + 4, 34)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "plane_orbit_frames.png")
    shutil.rmtree(tmp)
