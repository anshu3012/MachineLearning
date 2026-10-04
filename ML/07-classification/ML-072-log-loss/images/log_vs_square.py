"""The cost of one point under log loss, -log p, and under squared error, (1 - p)^2, against the probability p given to
the true class. A point slides from a good prediction (p = 0.95) to a bad one (p = 0.03); the tangent of each curve is
drawn at the point, and its slope is printed: -1/p for log loss, -2(1 - p) for squared error.
Run: python log_vs_square.py  -> log_vs_square.gif, log_vs_square_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, RED = "#4C78A8", "#E45756"
p = np.linspace(0.01, 1, 400)
ps = np.r_[np.arange(0.95, 0.1, -0.05), 0.1, 0.07, 0.05, 0.03]
assert abs((-np.log(0.1 + 1e-6) + np.log(0.1)) / 1e-6 - (-1 / 0.1)) < 1e-3          # the printed slopes are the derivatives


def frame(q):
    fig = go.Figure()
    for f, df, col, name in ((lambda v: -np.log(v), -1 / q, RED, "log loss  −log p"),
                             (lambda v: (1 - v) ** 2, -2 * (1 - q), BLUE, "squared error  (1 − p)²")):
        fig.add_trace(go.Scatter(x=p, y=f(p), mode="lines", line=dict(color=col, width=5),
                                 name=f"{name}: cost {f(q):.2f}, slope {df:.1f}".replace("-", "−")))
        h = 0.12 / np.hypot(1, df / 4.5) + 0.03                 # tangent segment of similar drawn length
        fig.add_trace(go.Scatter(x=[q - h, q + h], y=[f(q) - h * df, f(q) + h * df], mode="lines",
                                 line=dict(color="black", width=3), showlegend=False))
        fig.add_trace(go.Scatter(x=[q], y=[f(q)], mode="markers", showlegend=False,
                                 marker=dict(size=16, color=col, line=dict(color="black", width=2))))
    fig.update_layout(template="simple_white", width=900, height=640, font=dict(family="Latin Modern Roman", size=22),
                      margin=dict(l=80, r=20, t=140, b=70),
                      title=dict(text=f"probability given to the true class: p = {q:.2f}", x=0.5, y=0.97),
                      legend=dict(x=0.5, xanchor="center", y=1.02, yanchor="bottom", font_size=22),
                      xaxis=dict(title="p (1 = perfect prediction, 0 = worst)", range=[0, 1.02]),
                      yaxis=dict(title="cost of one point", range=[0, 4.5]))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".lvs_frames"
    tmp.mkdir(exist_ok=True)
    N = len(ps)
    for k, q in enumerate(ps):
        frame(q).write_image(tmp / f"{k:03d}.png")
    for k in range(N, N + 8):
        shutil.copy(tmp / f"{N - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "log_vs_square.gif")], check=True)
    pick = [int(np.argmin(abs(ps - v))) for v in (0.9, 0.5, 0.1, 0.03)]
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in pick]
    w_, h_ = keys[0].size
    sheet = Image.new("RGB", (2 * w_ + 16, 2 * h_ + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w_ + 16), (i // 2) * (h_ + 16)))
    sheet.save(HERE / "log_vs_square_frames.png")
    shutil.rmtree(tmp)
