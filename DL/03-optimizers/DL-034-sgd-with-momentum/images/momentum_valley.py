"""Plain gradient descent and gradient descent with momentum race along the narrow valley
L = (w1^2 + 100 w2^2)/2 from (-10, 0.4), both with learning rate 0.01; momentum beta = 0.9.
Run: python momentum_valley.py -> momentum_valley.gif, momentum_valley_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from PIL import Image
from surf import beside, quad_surface, VALLEY_LEVELS
from common import BLUE, ORANGE, RED, FONT

HERE = Path(__file__).parent
K, START, ETA, BETA, SHOW = 100, np.array([-10.0, 0.4]), 0.01, 0.9, 60
grad = lambda w: np.array([w[0], K * w[1]])
loss = lambda w: 0.5 * (w[0] ** 2 + K * w[1] ** 2)


def run(beta, steps=600):
    w, v, P = START.copy(), np.zeros(2), [START.copy()]
    for _ in range(steps):
        v = beta * v + ETA * grad(w)               # beta = 0 is plain gradient descent
        w = w - v
        P.append(w.copy())
    return np.array(P)


paths = {"gradient descent": (run(0.0), BLUE), "momentum, β = 0.9": (run(BETA), ORANGE)}
done = {k: int(np.argmax([loss(p) < 0.01 for p in P])) for k, (P, _) in paths.items()}
gx, gy = np.linspace(-11, 4, 220), np.linspace(-0.6, 0.6, 220)
X, Y = np.meshgrid(gx, gy)
Z = np.log10(0.5 * (X ** 2 + K * Y ** 2) + 0.01)
ZMAX = 62                                                   # the corners go higher than drawn
TRACES = quad_surface(np.linspace(-11, 4, 100), np.linspace(-0.6, 0.6, 41), np.zeros(2), np.diag([0.5, 50.0]), 0.0,
                      VALLEY_LEVELS, ZMAX, -2, 2.2, off=0.01)
height = lambda P: 0.5 * (P[:, 0] ** 2 + K * P[:, 1] ** 2)


def frame(k):
    fig = go.Figure(go.Contour(x=gx, y=gy, z=Z, colorscale="Greys", reversescale=True, showscale=False,
                               contours=dict(start=-2, end=2.2, size=0.3), line=dict(width=0.5), opacity=0.4))
    for name, (P, c) in paths.items():
        Q = P[:k + 1]
        label = f"{name}: loss < 0.01 after {done[name]} steps" if k >= done[name] else f"{name}: step {k}"
        fig.add_trace(go.Scatter(x=Q[:, 0], y=Q[:, 1], mode="lines+markers", name=label,
                                 line=dict(color=c, width=3), marker=dict(size=6, color=c)))
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(symbol="star", size=18, color=RED),
                             showlegend=False))
    fig.update_layout(template="simple_white", width=950, height=560, font=dict(FONT, size=20),
                      title=dict(text=f"step {k}", x=0.5, y=0.97), xaxis=dict(title="w₁", range=[-11, 4]),
                      yaxis=dict(title="w₂", range=[-0.6, 0.6]), margin=dict(l=70, r=20, t=130, b=55),
                      legend=dict(x=0, y=1.02, yanchor="bottom"))
    beside(fig, TRACES, [(P[:k + 1], height(P[:k + 1]), c, 5) for P, c in paths.values()], (0, 0, 0),
           ("w₁", "w₂"), (2.2, 1.3, 1.2), ZMAX, xr=[-11, 4], yr=[-0.6, 0.6])
    return fig


if __name__ == "__main__":
    print(done)
    tmp = HERE / ".valley_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(SHOW + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(SHOW + 1, SHOW + 9):                      # hold the last frame
        shutil.copy(tmp / f"{SHOW:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=1100:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "momentum_valley.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (5, 15, 30, SHOW)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "momentum_valley_frames.png")
    shutil.rmtree(tmp)
