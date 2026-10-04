"""Two balls roll down L(w) = (w^2 - 4)^2/8 - 0.6 w from w = -3, learning rate 0.05. Plain gradient descent stops
in the local minimum near w = -1.83; momentum (beta = 0.9) rolls over the bump, overshoots the global minimum
near w = 2.14 and swings back and forth before settling.
Run: python momentum_ball.py -> momentum_ball.gif, momentum_ball_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from PIL import Image
from common import BLUE, ORANGE, GREY, FONT

HERE = Path(__file__).parent
f = lambda w: (w ** 2 - 4) ** 2 / 8 - 0.6 * w
df = lambda w: w * (w ** 2 - 4) / 2 - 0.6
START, ETA, SHOW = -3.0, 0.05, 90


def run(beta, steps=SHOW):
    w, v, P = START, 0.0, [START]
    for _ in range(steps):
        v = beta * v + ETA * df(w)
        w = w - v
        P.append(w)
    return np.array(P)


balls = {"gradient descent": (run(0.0), BLUE), "momentum, β = 0.9": (run(0.9), ORANGE)}
ws = np.linspace(-3.2, 3.2, 400)


def frame(k):
    fig = go.Figure(go.Scatter(x=ws, y=f(ws), mode="lines", line=dict(color=GREY, width=3), showlegend=False))
    for name, (P, c) in balls.items():
        trail = P[max(0, k - 6):k + 1]
        fig.add_trace(go.Scatter(x=trail, y=f(trail) + 0.12, mode="markers", showlegend=False,
                                 marker=dict(size=8, color=c, opacity=0.35)))
        fig.add_trace(go.Scatter(x=[P[k]], y=[f(P[k]) + 0.12], mode="markers", name=name,
                                 marker=dict(size=22, color=c, line=dict(color="white", width=2))))
    fig.add_annotation(x=-1.83, y=f(-1.83) - 0.35, text="local minimum", showarrow=False, font=dict(color=GREY))
    fig.add_annotation(x=2.14, y=f(2.14) - 0.35, text="global minimum", showarrow=False, font=dict(color=GREY))
    fig.update_layout(template="simple_white", width=950, height=540, font=dict(FONT, size=20),
                      title=dict(text=f"step {k}", x=0.5, y=0.97), xaxis=dict(title="w", range=[-3.3, 3.3]),
                      yaxis=dict(title="loss L(w)", range=[-1.8, 3.6]), margin=dict(l=70, r=20, t=110, b=55),
                      legend=dict(x=0, y=1.02, yanchor="bottom", orientation="h"))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".ball_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(SHOW + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(SHOW + 1, SHOW + 9):
        shutil.copy(tmp / f"{SHOW:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "8", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "momentum_ball.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (4, 12, 20, SHOW)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "momentum_ball_frames.png")
    shutil.rmtree(tmp)
