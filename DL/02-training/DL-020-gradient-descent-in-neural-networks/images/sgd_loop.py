"""Stochastic gradient descent's inner loop on 50 observations: shuffle, then one update per observation.
The grid shows the shuffled order of one epoch (numbers = observation IDs); the counter totals the updates,
reaching 50 x 10 = 500 after 10 epochs (Plotly frames + ffmpeg).
Run: python sgd_loop.py -> sgd_loop.gif, sgd_loop_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from common import BLUE, RED, GREY

HERE = Path(__file__).parent
N, EPOCHS, COLS = 50, 10, 10
rng = np.random.default_rng(0)
orders = [rng.permutation(N) + 1 for _ in range(EPOCHS)]
assert N * EPOCHS == 500                                       # the Note's count: 50 observations, 10 epochs
assert not np.array_equal(orders[0], orders[1])                 # a fresh shuffle each epoch


def frame(epoch, k):
    """k observations of this epoch done; the (k)th is being used now (k >= 1)."""
    order = orders[epoch]
    xs, ys, colours, texts = [], [], [], []
    for i, obs in enumerate(order):
        xs.append(i % COLS)
        ys.append(-(i // COLS))
        colours.append(RED if i == k - 1 else (GREY if i < k - 1 else "#DDDDDD"))
        texts.append(str(obs))
    total = epoch * N + k
    fig = go.Figure(go.Scatter(x=xs, y=ys, mode="markers+text", text=texts, textfont=dict(size=18, color=["white" if c != "#DDDDDD" else "#444444" for c in colours]),
                               marker=dict(symbol="square", size=58, color=colours), showlegend=False))
    fig.add_annotation(x=4.5, y=1.25, showarrow=False, font=dict(size=26),
                       text=f"epoch {epoch + 1}: observation {k} of {N} (shuffled order)")
    fig.add_annotation(x=4.5, y=-5.2, showarrow=False, font=dict(size=30, color=BLUE),
                       text=f"<b>updates so far: {total}</b>")
    fig.update_layout(template="simple_white", width=900, height=640, font=dict(family="Latin Modern Roman"),
                      xaxis=dict(visible=False, range=[-0.7, 9.7]), yaxis=dict(visible=False, range=[-5.8, 1.7]),
                      margin=dict(l=10, r=10, t=10, b=10))
    return fig


if __name__ == "__main__":
    plan = [(0, k) for k in range(1, N + 1, 2)] + [(0, N)] + [(1, k) for k in range(1, N + 1, 7)] + [(1, N)]
    plan += [(EPOCHS - 1, N)]
    assert plan[-1][0] * N + plan[-1][1] == 500
    tmp = HERE / ".sgd_frames"
    tmp.mkdir(exist_ok=True)
    for j, (e, k) in enumerate(plan):
        frame(e, k).write_image(tmp / f"{j:03d}.png")
    last = len(plan) - 1
    for j in range(last + 1, last + 15):                        # hold the final count
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "sgd_loop.gif")], check=True)
    keys = [Image.open(tmp / f"{j:03d}.png").convert("RGB") for j in (0, 13, 26, last)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "sgd_loop_frames.png")
    shutil.rmtree(tmp)
