"""The 'lift the paper into a bowl' picture of section 2 (Plotly 3D frames + ffmpeg).
Two rings of points (make_circles): no straight line in (x1, x2) separates them. Adding the squared features lifts
each point to height x1^2 + x2^2, a bowl; there a flat plane separates the rings, and the plane cuts the bowl in a circle.
Run: python lift_bowl.py  -> lift_bowl.gif, lift_bowl_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from sklearn.datasets import make_circles
from sklearn.linear_model import LogisticRegression

HERE = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"
X, y = make_circles(n_samples=200, noise=0.08, factor=0.45, random_state=0)
r2 = (X ** 2).sum(1)
flat = LogisticRegression().fit(X, y).score(X, y)
Xl = np.c_[X, X ** 2, X[:, 0] * X[:, 1]]                         # degree-2 features
lifted = LogisticRegression(C=100, max_iter=10000).fit(Xl, y).score(Xl, y)
cut = (r2[y == 1].max() + r2[y == 0].min()) / 2                   # a flat plane between the two rings' heights
assert flat < 0.7 and lifted > 0.97 and r2[y == 1].max() < r2[y == 0].min()
print(f"straight line: {flat:.2f}, degree-2 features: {lifted:.2f}, plane at height {cut:.2f}")

g = np.linspace(-1.35, 1.35, 40)
GX, GY = np.meshgrid(g, g)
th = np.linspace(0, 2 * np.pi, 120)
LIFT, PLANE, HOLD = 10, 4, 6


def frame(k):
    t = min(k / LIFT, 1.0)
    s = 3 * t ** 2 - 2 * t ** 3                                   # smooth start and stop
    fig = go.Figure()
    fig.add_trace(go.Surface(x=GX, y=GY, z=s * (GX ** 2 + GY ** 2), opacity=0.18, showscale=False,
                             colorscale=[[0, GREY], [1, GREY]], hoverinfo="skip"))
    for cls, c, name in ((1, ORANGE, "inner ring"), (0, BLUE, "outer ring")):
        m = y == cls
        fig.add_trace(go.Scatter3d(x=X[m, 0], y=X[m, 1], z=s * r2[m], mode="markers", name=name,
                                   marker=dict(size=4.5, color=c)))
    if k > LIFT:
        fig.add_trace(go.Surface(x=GX, y=GY, z=np.full_like(GX, cut), opacity=0.35, showscale=False,
                                 colorscale=[[0, "#54A24B"], [1, "#54A24B"]], hoverinfo="skip"))
        rc = np.sqrt(cut)
        fig.add_trace(go.Scatter3d(x=rc * np.cos(th), y=rc * np.sin(th), z=np.full_like(th, cut), mode="lines",
                                   name="plane meets bowl: a circle", line=dict(color="black", width=8)))
    title = ("flat paper: no straight line splits the rings" if k == 0 else
             "add x₁², x₂²: lift each point to height x₁² + x₂²" if k <= LIFT else
             "a flat plane now splits them; it cuts the bowl in a circle")
    eye_z = 2.4 - 1.7 * s
    fig.update_layout(width=900, height=760, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=title, x=0.5, y=0.96), margin=dict(l=0, r=0, t=70, b=0),
                      legend=dict(x=0.02, y=0.9, font_size=20),
                      scene=dict(xaxis=dict(title="x₁", range=[-1.4, 1.4], showticklabels=False),
                                 yaxis=dict(title="x₂", range=[-1.4, 1.4], showticklabels=False),
                                 zaxis=dict(title="height", range=[0, 2.2], showticklabels=False),
                                 aspectmode="manual", aspectratio=dict(x=1, y=1, z=0.75),
                                 camera=dict(eye=dict(x=0.25 + 1.3 * s, y=-0.25 - 1.3 * s, z=eye_z))))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".lift_frames"
    tmp.mkdir(exist_ok=True)
    last = LIFT + PLANE
    for k in range(last + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(last + 1, last + 1 + HOLD):                      # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "lift_bowl.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, last)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, h), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "lift_bowl_frames.png")
    shutil.rmtree(tmp)
