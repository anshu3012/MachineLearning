"""Gradient descent (eta 0.3), momentum (eta 0.1, beta 0.9) and AdaGrad (eta 2) on the sparse-feature loss,
from (m, b) = (-4, -4). Gradient descent and momentum first fix b, then crawl along m; AdaGrad heads for the minimum.
Run: python adagrad_race.py -> adagrad_race.gif, adagrad_race_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from PIL import Image
from common import BLUE, ORANGE, GREEN, RED, FONT
from shared import X, y, BEST, run, steps_to

HERE = Path(__file__).parent
SHOW = 45
paths = {"gradient descent, η = 0.3": (run("gd", 0.3), BLUE),
         "momentum, η = 0.1, β = 0.9": (run("momentum", 0.1), ORANGE),
         "AdaGrad, η = 2": (run("adagrad", 2.0), GREEN)}
done = {k: steps_to(P) for k, (P, _) in paths.items()}
m, b = np.linspace(-5, 9, 200), np.linspace(-5, 9, 200)
M, B = np.meshgrid(m, b)
Z = np.log10(((y[None, None, :] - M[..., None] * X[:, 0] - B[..., None]) ** 2).mean(-1))


def frame(k):
    fig = go.Figure(go.Contour(x=m, y=b, z=Z, colorscale="Greys", reversescale=True, showscale=False,
                               contours=dict(start=-0.6, end=2.4, size=0.2), line=dict(width=0.6), opacity=0.5))
    for name, (P, c) in paths.items():
        Q = P[:k + 1]
        label = f"{name}: done in {done[name]} steps" if k >= done[name] else f"{name}: step {k}"
        fig.add_trace(go.Scatter(x=Q[:, 0], y=Q[:, 1], mode="lines+markers", name=label,
                                 line=dict(color=c, width=3), marker=dict(size=6, color=c)))
    fig.add_trace(go.Scatter(x=[BEST[0]], y=[BEST[1]], mode="markers", showlegend=False,
                             marker=dict(symbol="star", size=18, color=RED)))
    fig.update_layout(template="simple_white", width=820, height=820, font=dict(FONT, size=20),
                      title=dict(text=f"step {k}", x=0.5, y=0.98), xaxis=dict(title="m (weight of IIT)", range=[-5, 9]),
                      yaxis=dict(title="b (bias)", range=[-5, 9]), margin=dict(l=70, r=20, t=170, b=55),
                      legend=dict(x=0, y=1.02, yanchor="bottom"))
    return fig


if __name__ == "__main__":
    print(done)
    tmp = HERE / ".race_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(SHOW + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(SHOW + 1, SHOW + 9):
        shutil.copy(tmp / f"{SHOW:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "adagrad_race.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (3, 10, 25, SHOW)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "adagrad_race_frames.png")
    shutil.rmtree(tmp)
