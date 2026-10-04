"""Why the spread of the weights must depend on the fan-in (section 3). For fan-in n from 2 to 1000, one node adds
n products w_i x_i with standard normal inputs x_i. 4000 such weighted sums z are drawn for three ways of scaling the
weights: 0.01 x randn (fixed, small), 1 x randn (fixed, large) and randn x sqrt(1/n) (depends on n). One frame per n:
the first histogram stays a needle at 0, the second flattens out as n grows, the third keeps the same width.
Numpy, seed 0. Plotly frames -> ffmpeg GIF + a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image
from plotly.subplots import make_subplots

from common import BLUE, GREEN, RED

HERE = Path(__file__).parent
NS = [2, 5, 10, 25, 50, 100, 250, 500, 1000]
M = 4000
rng = np.random.default_rng(0)
SCALES = [("0.01 × randn", lambda n: 0.01, BLUE), ("1 × randn", lambda n: 1.0, RED),
          ("randn × √(1/n)", lambda n: np.sqrt(1 / n), GREEN)]
Z = {}
for n in NS:
    X, W = rng.standard_normal((M, n)), rng.standard_normal((M, n))
    for name, s, _ in SCALES:
        Z[n, name] = (s(n) * W * X).sum(1)
SD = {key: z.std() for key, z in Z.items()}
for n in NS:                                            # the variance rule Var(z) = n Var(w) Var(x), within 10 percent
    for name, s, _ in SCALES:
        assert abs(SD[n, name] / (s(n) * np.sqrt(n)) - 1) < 0.1, (n, name, SD[n, name])
BINS = dict(start=-10, end=10, size=0.25)


def frame(n):
    fig = make_subplots(3, 1, shared_xaxes=True, vertical_spacing=0.09, subplot_titles=[
        f"weights {name}:  standard deviation of z = {SD[n, name]:.2f}" for name, _, _ in SCALES])
    for r, (name, _, c) in enumerate(SCALES, start=1):
        fig.add_histogram(x=np.clip(Z[n, name], -9.99, 9.99), xbins=BINS, histnorm="probability", marker_color=c,
                          showlegend=False, row=r, col=1)
        fig.update_yaxes(range=[0, 1.05 if r == 1 else 0.14], showticklabels=False, row=r, col=1)
    fig.update_xaxes(range=[-10, 10])
    fig.update_xaxes(title_text="weighted sum z (values beyond ±10 are piled on the edges)", row=3, col=1)
    fig.update_layout(template="simple_white", width=1000, height=820, font=dict(family="Latin Modern Roman", size=21),
                      title=dict(text=f"fan-in n = {n}: each node adds {n} products", x=0.5, font=dict(size=25)),
                      bargap=0, margin=dict(l=40, r=20, t=110, b=70))
    for a in fig.layout.annotations[:3]:
        a.font.size = 21
    return fig


if __name__ == "__main__":
    tmp = HERE / ".fan_frames"
    tmp.mkdir(exist_ok=True)
    keys = {}
    for n in NS:
        keys[n] = tmp / f"n{n}.png"
        frame(n).write_image(keys[n])
    seq = [n for n in NS for _ in range(2)] + [NS[-1]] * 4
    for i, n in enumerate(seq):
        shutil.copy(keys[n], tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "fan_in_sweep.gif")], check=True)
    ims = [Image.open(keys[n]).convert("RGB") for n in (2, 25, 250, 1000)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "fan_in_sweep_frames.png")
    shutil.rmtree(tmp)
    for n in (2, 250, 1000):
        print(n, {name: round(float(SD[n, name]), 3) for name, _, _ in SCALES})
