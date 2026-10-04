"""Gradient descent, Newton and BFGS race to the minimum (1, 1) of the curved valley f = (1 - x)^2 + 5(y - x^2)^2,
starting at (-1.2, 1). All three use the same backtracking line search (halve the step until f drops enough).
Newton uses the true Hessian, BFGS builds its stand-in from gradient changes, gradient descent uses neither.
Run: python optimizer_race.py  -> optimizer_race.gif, optimizer_race_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
f = lambda p: (1 - p[0]) ** 2 + 5 * (p[1] - p[0] ** 2) ** 2
grad = lambda p: np.array([-2 * (1 - p[0]) - 20 * p[0] * (p[1] - p[0] ** 2), 10 * (p[1] - p[0] ** 2)])
hess = lambda p: np.array([[2 - 20 * p[1] + 60 * p[0] ** 2, -20 * p[0]], [-20 * p[0], 10]])
START, TOL, MAX = np.array([-1.2, 1.0]), 1e-6, 20000


def line_search(p, d):
    t = 1.0
    while f(p + t * d) > f(p) + 1e-4 * t * grad(p) @ d:      # Armijo: demand a real drop
        t /= 2
    return t


def run(direction, update=None):
    p, B, path = START.copy(), np.eye(2), [START.copy()]
    while np.linalg.norm(grad(p)) > TOL and len(path) <= MAX:
        d = direction(p, B)
        new = p + line_search(p, d) * d
        if update:
            B = update(B, new - p, grad(new) - grad(p))
        p = new
        path.append(p.copy())
    return np.array(path)


def newton_dir(p, B):
    H = hess(p)
    if np.linalg.eigvalsh(H).min() <= 0:                      # not a bowl here: fall back to a nudged Hessian
        H = H + (1e-3 - np.linalg.eigvalsh(H).min()) * np.eye(2)
    return -np.linalg.solve(H, grad(p))


def bfgs_update(B, s, y):                                    # new B satisfies the secant equation B s = y
    Bs = B @ s
    return B - np.outer(Bs, Bs) / (s @ Bs) + np.outer(y, y) / (y @ s)


paths = {"gradient descent": (run(lambda p, B: -grad(p)), BLUE),
         "Newton (true Hessian)": (run(newton_dir), GREEN),
         "BFGS (Hessian built from gradients)": (run(lambda p, B: -np.linalg.solve(B, grad(p)), bfgs_update), ORANGE)}
steps = {k: len(v[0]) - 1 for k, v in paths.items()}
for k, (P, _) in paths.items():
    assert np.allclose(P[-1], [1, 1], atol=1e-4), k
B_check = bfgs_update(np.eye(2), np.array([1.0, 0.5]), np.array([3.0, 2.0]))
assert np.allclose(B_check @ [1.0, 0.5], [3.0, 2.0])
assert steps["Newton (true Hessian)"] < steps["BFGS (Hessian built from gradients)"] < steps["gradient descent"]
print(steps)
# Check of the text's explanation: how far is BFGS's B from the true Hessian along its run?
p, B, B_err = START.copy(), np.eye(2), []
while np.linalg.norm(grad(p)) > TOL:
    B_err.append(np.linalg.norm(B - hess(p)) / np.linalg.norm(hess(p)))
    d = -np.linalg.solve(B, grad(p))
    new = p + line_search(p, d) * d
    B, p = bfgs_update(B, new - p, grad(new) - grad(p)), new
print("relative error of B, steps 0-6:", np.round(B_err[:7], 2), " steps 7+:", np.round(B_err[7:], 2))

gx, gy = np.linspace(-1.6, 1.6, 200), np.linspace(-0.7, 1.9, 200)
X, Y = np.meshgrid(gx, gy)
Z = np.log10(f(np.array([X, Y])) + 1e-3)
SHOW = 30                                                    # frames shown; gradient descent is still crawling


def frame(k):
    fig = go.Figure(go.Contour(x=gx, y=gy, z=Z, colorscale="Greys", reversescale=True, showscale=False,
                               contours=dict(start=-2, end=2.5, size=0.25), line=dict(width=0.6), opacity=0.45))
    for name, (P, c) in paths.items():
        Q = P[:k + 1]
        done = k >= len(P) - 1
        label = f"{name}: {steps[name]} steps" if done else f"{name}: step {min(k, len(P) - 1)}"
        fig.add_trace(go.Scatter(x=Q[:, 0], y=Q[:, 1], mode="lines+markers", name=label,
                                 line=dict(color=c, width=3), marker=dict(size=7, color=c)))
    fig.add_trace(go.Scatter(x=[1], y=[1], mode="markers+text", text=["minimum (1, 1)"], textposition="middle right",
                             marker=dict(symbol="star", size=18, color=RED), showlegend=False))
    fig.add_trace(go.Scatter(x=[START[0]], y=[START[1]], mode="markers+text", text=["start"], textposition="top center",
                             marker=dict(size=11, color="black"), showlegend=False))
    fig.update_layout(template="simple_white", width=900, height=720, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"step {k}", x=0.5, y=0.98), xaxis=dict(title="x", range=[-1.6, 1.6]),
                      yaxis=dict(title="y", range=[-0.7, 1.9]), margin=dict(l=60, r=20, t=150, b=55),
                      legend=dict(x=0, y=1.02, yanchor="bottom"))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".race_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(SHOW + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(SHOW + 1, SHOW + 9):                      # hold the last frame
        shutil.copy(tmp / f"{SHOW:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "optimizer_race.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 3, 10, SHOW)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "optimizer_race_frames.png")
    shutil.rmtree(tmp)
