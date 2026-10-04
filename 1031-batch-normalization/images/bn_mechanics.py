"""The two steps of batch normalisation on the Note's batch of 4 values z = 2, 4, 6, 8 of one node (section 4.3-4.4),
as dots moving on a number line: subtract the batch mean, divide by the batch standard deviation, scale by
gamma = 1.5, shift by beta = 0.5. The bar under the dots is mean +- one standard deviation.
Run: python bn_mechanics.py  -> bn_mechanics.gif, bn_mechanics_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from common import BLUE, GREEN, ORANGE, PURPLE, RED

HERE = Path(__file__).parent
z = np.array([2.0, 4.0, 6.0, 8.0])
mu, var, eps, gamma, beta = z.mean(), z.var(), 0.001, 1.5, 0.5
STAGES = [(z, "the batch: z = 2, 4, 6, 8", BLUE),
          (z - mu, "1. subtract the batch mean 5", ORANGE),
          ((z - mu) / np.sqrt(var + eps), "2. divide by the batch std 2.24", RED),
          (gamma * (z - mu) / np.sqrt(var + eps), "3. scale by γ = 1.5", PURPLE),
          (gamma * (z - mu) / np.sqrt(var + eps) + beta, "4. shift by β = 0.5", GREEN)]
assert np.allclose(STAGES[2][0], [-1.34, -0.45, 0.45, 1.34], atol=0.005)               # section 4.3
assert np.allclose(STAGES[4][0], [-1.51, -0.17, 1.17, 2.51], atol=0.005)               # section 4.4
TWEEN, HOLD = 8, 14                                                                    # frames per move, per pause


def frame(v, title, c):
    m, s = round(v.mean(), 6) + 0.0, v.std()             # + 0.0 turns -0.0 into 0.0
    fig = go.Figure()
    fig.add_shape(type="line", x0=m - s, x1=m + s, y0=-0.45, y1=-0.45, line=dict(color=c, width=6), opacity=1, layer="above")
    fig.add_trace(go.Scatter(x=[m], y=[-0.45], mode="markers", marker=dict(symbol="diamond", size=16, color=c)))
    fig.add_annotation(x=m, y=-0.45, text=f"mean {m:.2f}   std {s:.2f}".replace("-", "−"), yshift=-30, showarrow=False,
                       font=dict(size=24, color=c))
    fig.add_trace(go.Scatter(x=v, y=np.zeros(4), mode="markers+text", text=[f"{x:.2f}".replace("-", "−") for x in v],
                             textposition=["top center", "bottom center"] * 2, textfont=dict(size=24, color=c),
                             marker=dict(size=26, color=c, line=dict(width=1.5, color="white"))))
    fig.add_vline(x=0, line=dict(color="#BBBBBB", width=1.5, dash="dot"))
    fig.update_layout(template="simple_white", width=900, height=430, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), title=dict(text=title, x=0.5, y=0.93,
                      font=dict(size=30, color=c)), margin=dict(l=30, r=30, t=90, b=60),
                      xaxis=dict(range=[-3.6, 9.2], dtick=1, title="value of the node over the batch"),
                      yaxis=dict(range=[-0.9, 0.4], visible=False))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".bn_mechanics_frames"
    tmp.mkdir(exist_ok=True)
    seq, keys, k = [], [], 0
    for i, (v, title, c) in enumerate(STAGES):
        if i:                                                  # slide from the previous stage
            v0 = STAGES[i - 1][0]
            for t in np.linspace(0, 1, TWEEN + 1)[1:-1]:
                t = 3 * t ** 2 - 2 * t ** 3                    # ease in and out
                p = tmp / f"{k:03d}.png"; k += 1
                frame(v0 + t * (v - v0), title, c).write_image(p)
                seq.append((p, 1))
        p = tmp / f"{k:03d}.png"; k += 1
        frame(v, title, c).write_image(p)
        seq.append((p, HOLD))
        keys.append(p)
    seq[-1] = (seq[-1][0], 40)
    with open(tmp / "list.txt", "w") as f:
        for p, t in seq:
            f.write(f"file '{p.name}'\nduration {t / 10}\n")
        f.write(f"file '{seq[-1][0].name}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-i", str(tmp / "list.txt"), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "bn_mechanics.gif")], check=True)
    ims = [Image.open(p).convert("RGB") for p in keys[1:]]   # the four steps
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "bn_mechanics_frames.png")
    shutil.rmtree(tmp)
