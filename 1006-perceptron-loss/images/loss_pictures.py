"""Three pictures for the perceptron loss, on the Note's own numbers.
distance_vs_value.png : line 2x + 3y + 4 = 0 and its two mistakes (4, 6) and (-2, -2): 0-1 loss 1 + 1, distances
                        8.32 and 1.66, values |f| = 30 and 6 (Sections 5.1-5.3).
loss_landscape.png    : the average perceptron loss over (w1, w2) for the 100 make_classification points, b fixed at
                        the final value, with the path of the 12 updates of Figure 1 (Section 4).
one_point_steps.gif   : repeated gradient steps (lr 0.1) on the point (-2, -2), y = +1: f = -6, -5.1, ... until the point
                        crosses the line and its loss is 0 (Section 7).  Run: python loss_pictures.py"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from sklearn.datasets import make_classification

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=24)


def seg(w, xr, yr):
    """Two end points of w1 x + w2 y + b = 0 across the box."""
    xs = np.linspace(*xr, 400)
    ys = -(w[0] * xs + w[2]) / w[1]
    ok = (ys >= yr[0]) & (ys <= yr[1])
    return xs[ok], ys[ok]


# 1. Distance against value in the line's equation
w = np.array([2.0, 3.0, 4.0])
pts = np.array([[4.0, 6.0], [-2.0, -2.0]])
f = pts @ w[:2] + w[2]
d = np.abs(f) / np.hypot(*w[:2])
assert np.allclose(f, [30, -6]) and np.allclose(d, [8.32, 1.66], atol=0.005) and np.abs(f).sum() == 36
foot = pts - (f / (w[:2] @ w[:2]))[:, None] * w[:2]          # nearest point on the line
fig = go.Figure()
xr, yr = (-8, 9), (-6, 8)
lx, ly = seg(w, xr, yr)
fig.add_trace(go.Scatter(x=lx, y=ly, mode="lines", line=dict(color=GREY, width=4), name="2x + 3y + 4 = 0"))
for p, q, fi, di, c in zip(pts, foot, f, d, (RED, ORANGE)):
    fig.add_trace(go.Scatter(x=[p[0], q[0]], y=[p[1], q[1]], mode="lines", line=dict(color=c, width=3, dash="dash"),
                             showlegend=False))
    fig.add_trace(go.Scatter(x=[p[0]], y=[p[1]], mode="markers+text", marker=dict(size=16, color=c),
                             text=[f"({p[0]:.0f}, {p[1]:.0f})".replace("-", "−")],
                             textposition="middle left" if p[0] < 0 else "middle right", textfont=dict(color=c, size=24),
                             showlegend=False))
fig.update_layout(template="simple_white", width=1000, height=640, font=FONT, showlegend=False,
                  xaxis=dict(title="x", range=xr, zeroline=True), yaxis=dict(title="y", range=yr, zeroline=True, scaleanchor="x"),
                  margin=dict(l=70, r=20, t=30, b=70))
fig.add_annotation(x=-7.5, y=7.6, xanchor="left", yanchor="top", showarrow=False, font=dict(size=24),
                   align="left", text="0-1 loss: 1 + 1 = 2<br>distance: 8.32 + 1.66 = 9.98<br>value |f|: 30 + 6 = 36")
fig.write_image(HERE / "distance_vs_value.png", scale=2)

# 2. Loss landscape on the Note's 100 points
X, Y01 = make_classification(n_samples=100, n_features=2, n_informative=1, n_redundant=0, n_classes=2,
                             n_clusters_per_class=1, random_state=41, hypercube=False, class_sep=15)
Y = np.where(Y01 == 1, 1, -1)
W0 = np.array([-1.0, 1.0, 0.5])
loss = lambda w: np.maximum(0, -Y * (X @ w[:2] + w[2])).mean()
path = [W0.copy()]
wc = W0.copy()
for i in range(len(Y)):                                        # epoch 1, as in Figure 1
    if Y[i] * (X[i] @ wc[:2] + wc[2]) < 0:
        wc = wc + 0.1 * Y[i] * np.r_[X[i], 1]
        path.append(wc.copy())
path = np.array(path)
assert len(path) - 1 == 12 and loss(path[-1]) == 0 and np.isclose(path[-1, 2], 0.5) and round(loss(W0), 3) == 1.687
assert round(loss(path[1]), 3) == 1.712                        # the first update raises the average loss
g1, g2 = np.linspace(-1.5, 3.5, 160), np.linspace(-1.5, 2.0, 140)
L = np.array([[loss(np.array([a, b, path[-1, 2]])) for a in g1] for b in g2])
fig = go.Figure(go.Contour(x=g1, y=g2, z=L, colorscale="Blues", reversescale=False, contours=dict(start=0, end=L.max(), size=0.25),
                           colorbar=dict(title="loss L"), line=dict(width=0.5)))
fig.add_trace(go.Scatter(x=path[:, 0], y=path[:, 1], mode="lines+markers", line=dict(color=RED, width=3),
                         marker=dict(size=9, color=RED), name="the 12 updates of Figure 1"))
fig.add_trace(go.Scatter(x=[path[0, 0]], y=[path[0, 1]], mode="markers+text", text=["start: L = 1.69"],
                         textposition="top center", marker=dict(size=14, color="black"), textfont=dict(size=24)))
fig.add_trace(go.Scatter(x=[path[-1, 0]], y=[path[-1, 1]], mode="markers+text", text=["end: L = 0"],
                         textposition="top center", marker=dict(size=16, color=GREEN, symbol="star"), textfont=dict(size=24, color=GREEN)))
fig.update_layout(template="simple_white", width=1000, height=700, font=FONT, showlegend=False,
                  xaxis=dict(title="w₁"), yaxis=dict(title="w₂"), margin=dict(l=70, r=20, t=30, b=70))
fig.write_image(HERE / "loss_landscape.png", scale=2)

# 3. Repeated steps on one point
p, y = np.array([-2.0, -2.0]), 1
steps = [w.copy()]
while y * (p @ steps[-1][:2] + steps[-1][2]) < 0:
    steps.append(steps[-1] + 0.1 * y * np.r_[p, 1])
vals = [p @ s[:2] + s[2] for s in steps]
assert np.allclose(steps[1], [1.8, 2.8, 4.1]) and np.isclose(vals[1], -5.1)
assert np.allclose(np.diff(vals), 0.9)                         # each step raises f by lr (x1^2 + x2^2 + 1) = 0.9
xr, yr = (-4, 3), (-4, 3)


def frame(k):
    s = steps[k]
    fig = go.Figure()
    for j in range(k):
        lx, ly = seg(steps[j], xr, yr)
        fig.add_trace(go.Scatter(x=lx, y=ly, mode="lines", line=dict(color="#CCCCCC", width=2)))
    lx, ly = seg(s, xr, yr)
    fig.add_trace(go.Scatter(x=lx, y=ly, mode="lines", line=dict(color=BLUE, width=4)))
    ok = vals[k] >= 0
    fig.add_trace(go.Scatter(x=[p[0]], y=[p[1]], mode="markers", marker=dict(size=18, color=GREEN if ok else RED)))
    fig.update_layout(template="simple_white", width=900, height=760, font=FONT, showlegend=False,
                      title=dict(text=f"step {k}: {s[0]:.1f}x₁ + {s[1]:.1f}x₂ + {s[2]:.1f} = 0<br>"
                                      f"f(−2, −2) = {vals[k]:.1f}, loss of the point {max(0, -vals[k]):.1f}".replace("= -", "= −"), x=0.5),
                      xaxis=dict(title="x₁", range=xr, zeroline=True), yaxis=dict(title="x₂", range=yr, zeroline=True, scaleanchor="x"),
                      margin=dict(l=70, r=20, t=120, b=70))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".step_frames"
    tmp.mkdir(exist_ok=True)
    n = len(steps)
    for k in range(n):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(n, n + 4):
        shutil.copy(tmp / f"{n - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "one_point_steps.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 1, n // 2, n - 1)]
    w_, h_ = keys[0].size
    sheet = Image.new("RGB", (2 * w_ + 16, 2 * h_ + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w_ + 16), (i // 2) * (h_ + 16)))
    sheet.save(HERE / "one_point_steps_frames.png")
    shutil.rmtree(tmp)
    print("steps", n - 1, "values", np.round(vals, 1))
