"""Animation for Note ML-053, Section 5: the gradient of E = (y - X beta)^T (y - X beta) is -2 X^T y + 2 X^T X beta,
one partial derivative per coefficient. On the four students of Section 6.1 we walk beta in a straight line from
(0, 0.3) to the normal-equation answer (-0.81, 0.57). Left: E against beta_0 with beta_1 held; right: E against
beta_1 with beta_0 held. The tangent slopes are the two entries of the gradient; both reach 0 together at the
answer. Run: python gradient_zero.py -> gradient_zero.gif, gradient_zero_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
cgpa = np.array([6.89, 5.12, 7.82, 7.42])
y = np.array([3.26, 1.98, 3.25, 3.67])
X = np.column_stack([np.ones(4), cgpa])
E = lambda b: float((y - X @ b) @ (y - X @ b))
grad = lambda b: -2 * X.T @ y + 2 * X.T @ X @ b                 # the matrix-calculus formula of Section 5
best = np.linalg.solve(X.T @ X, X.T @ y)
assert np.allclose(best.round(2), [-0.81, 0.57]) and np.allclose(grad(best), 0, atol=1e-9)
b, h = np.array([0.2, 0.4]), 1e-6                              # formula = finite differences
assert np.allclose(grad(b), [(E(b + h * d) - E(b - h * d)) / (2 * h) for d in np.eye(2)], rtol=1e-4)
START = np.array([1.0, 0.4])
N = 24


def fmt(v):
    return "0" if abs(v) < 0.005 else f"{v:+.2f}"


def frame(k):
    t = min(1.0, k / (N - 1))
    b = START + t * (best - START)
    g = grad(b)
    fig = make_subplots(1, 2, horizontal_spacing=0.12,
                        subplot_titles=[f"∂E/∂β<sub>{j}</sub> = {fmt(g[j])}" for j in (0, 1)])
    for j, (lo, hi) in enumerate(((-2.5, 1.5), (0.25, 0.85))):
        v = np.linspace(lo, hi, 200)
        curve = []
        for s in v:
            c = b.copy(); c[j] = s; curve.append(E(c))
        fig.add_trace(go.Scatter(x=v, y=curve, mode="lines", line=dict(color=BLUE, width=3)), 1, j + 1)
        w = 0.35 * (hi - lo)                                    # tangent: slope = this entry of the gradient
        fig.add_trace(go.Scatter(x=[b[j] - w, b[j] + w], y=[E(b) - g[j] * w, E(b) + g[j] * w], mode="lines",
                                 line=dict(color=ORANGE, width=4)), 1, j + 1)
        fig.add_trace(go.Scatter(x=[b[j]], y=[E(b)], mode="markers",
                                 marker=dict(color=GREEN if t == 1 else RED, size=16)), 1, j + 1)
        fig.update_xaxes(title=f"β<sub>{j}</sub>  (β<sub>{1 - j}</sub> held at {b[1 - j]:.2f})", range=[lo, hi],
                         row=1, col=j + 1)
        fig.update_yaxes(range=[0, 4], row=1, col=j + 1)
    fig.update_yaxes(title="E (sum of squared errors)", row=1, col=1)
    top = (f"β = ({b[0]:.2f}, {b[1]:.2f}),  E = {E(b):.3f}" if t < 1 else
           f"β = (-0.81, 0.57): both slopes are 0, E = {E(b):.3f} is the minimum")
    fig.update_layout(template="simple_white", width=1100, height=520, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=20), title=dict(text=top, x=0.02, y=0.97),
                      margin=dict(l=90, r=30, t=110, b=80))
    fig.update_annotations(font_size=24)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".grad_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(N):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(N, N + 10):
        shutil.copy(tmp / f"{N - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "gradient_zero.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 8, 16, N - 1)]
    w, hh = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * hh + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (hh + 16)))
    sheet.save(HERE / "gradient_zero_frames.png")
    shutil.rmtree(tmp)
