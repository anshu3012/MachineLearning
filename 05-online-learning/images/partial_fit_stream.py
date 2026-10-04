"""What partial_fit does, drawn: an SGDRegressor learns a line from a stream of mini-batches of 10 observations, the
same stream as the Notebook's first 500 rows (y = 2x plus noise, seed 0). After each call the line moves a little;
earlier batches are never seen again. Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from sklearn.linear_model import SGDRegressor

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#BBBBBB"

rng = np.random.default_rng(0)                          # the Notebook's data, first 500 rows (before the change)
n, change = 1000, 500
x = rng.uniform(0, 4, n)
y = np.where(np.arange(n) < change, 2 * x, 8 - 2 * x) + rng.normal(0, 0.5, n)
x, y = x[:change], y[:change]

model = SGDRegressor(random_state=0)
states = []
for b in range(0, change, 10):
    model.partial_fit(x[b:b + 10, None], y[b:b + 10])
    states.append((b // 10 + 1, model.coef_[0], model.intercept_[0]))
SHOW = [1, 2, 3, 5, 10, 20, 50]
assert round(states[-1][1], 2) == 1.81 and round(states[-1][2], 2) == 0.51, states[-1]   # near the true y = 2x


def frame(k):
    calls, a, c = states[k - 1]
    seen = 10 * calls
    fig = go.Figure()
    fig.add_scatter(x=x[:seen - 10], y=y[:seen - 10], mode="markers", marker=dict(size=7, color=GREY),
                    name="earlier mini-batches (not stored)")
    fig.add_scatter(x=x[seen - 10:seen], y=y[seen - 10:seen], mode="markers",
                    marker=dict(size=14, color=ORANGE, line=dict(width=1, color="white")), name="this mini-batch")
    xs = np.array([0, 4])
    fig.add_scatter(x=xs, y=a * xs + c, mode="lines", line=dict(color=BLUE, width=5), name="model after this call")
    fig.update_layout(template="simple_white", width=1000, height=700, font=FONT,
                      title=dict(text=f"partial_fit call {calls}: model  y = {a:.2f}·x {'+' if c >= 0 else '−'} "
                                      f"{abs(c):.2f}", x=0.5, y=0.95),
                      xaxis=dict(title="feature x", range=[0, 4]), yaxis=dict(title="target y", range=[-2, 10]),
                      legend=dict(x=0.02, y=0.98, font=dict(size=18)), margin=dict(l=80, r=30, t=80, b=80))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".pf_frames"
    tmp.mkdir(exist_ok=True)
    keys = {}
    for k in SHOW:
        keys[k] = tmp / f"k{k}.png"
        frame(k).write_image(keys[k])
    seq = [k for k in SHOW for _ in range(3)] + [SHOW[-1]] * 4
    for j, k in enumerate(seq):
        shutil.copy(keys[k], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "partial_fit_stream.gif")], check=True)
    ims = [Image.open(keys[k]).convert("RGB") for k in (1, 50)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, h), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "partial_fit_stream_frames.png")
    shutil.rmtree(tmp)
    print([(s[0], round(s[1], 2), round(s[2], 2)) for s in states if s[0] in SHOW])
