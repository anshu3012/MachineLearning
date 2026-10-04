"""Consistency of the MLE (Plotly frames -> GIF). For each sample size n we simulate 20000 datasets of n Poisson counts
with true rate 2, and compute the MLE (the average count) of each. The histogram of the 20000 estimates narrows around
2 as n grows; its spread (standard deviation) halves each time n is multiplied by 4: 0.63, 0.32, 0.16, 0.08 for
n = 5, 20, 80, 320, matching sqrt(2 / n).
Run: python consistency.py -> consistency.gif, consistency_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
rng = np.random.default_rng(0)
NS = [5, 10, 20, 40, 80, 160, 320]
est = {n: rng.poisson(2, size=(20000, n)).mean(axis=1) for n in NS}
for n, s in zip((5, 20, 80, 320), (0.63, 0.32, 0.16, 0.08)):
    assert abs(est[n].std() - s) < 0.01, (n, est[n].std())


def frame(n):
    wid = int(np.ceil(0.025 * n)) / n                    # a whole number of possible averages (steps of 1/n) per bar
    edges = np.arange(-0.5 / n, 4.6, wid)
    counts, _ = np.histogram(est[n], bins=edges)
    sd = est[n].std()
    fig = go.Figure(go.Bar(x=edges[:-1] + wid / 2, y=counts / 20000 / wid, width=wid * 0.9, marker_color=BLUE))
    fig.add_vline(x=2, line=dict(color=RED, width=3, dash="dash"), opacity=1)
    fig.add_annotation(x=2, y=1.0, yref="paper", text="true rate 2", showarrow=False, xshift=62,
                       font=dict(color=RED, size=22))
    fig.add_shape(type="line", x0=2 - sd, x1=2 + sd, y0=-0.25, y1=-0.25, line=dict(color=ORANGE, width=8), opacity=1)
    fig.update_layout(template="simple_white", width=900, height=560, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"n = {n} counts per dataset: spread {sd:.2f}", x=0.5, font=dict(size=28)),
                      xaxis=dict(title="MLE of the rate (average count)", range=[0, 4.5]),
                      yaxis=dict(title="density of the 20000 estimates", range=[-0.5, 5.5]), showlegend=False,
                      margin=dict(l=80, r=20, t=70, b=60))
    fig.add_annotation(x=2 + sd, y=-0.25, text="± 1 spread", showarrow=False, xanchor="left", xshift=8,
                       font=dict(color=ORANGE, size=20))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".consistency_frames"
    tmp.mkdir(exist_ok=True)
    k = 0
    for n in NS:
        frame(n).write_image(tmp / f"{n}.png")
        for _ in range(3 if n != NS[-1] else 8):          # each n held ~1 s, the last one longer
            shutil.copy(tmp / f"{n}.png", tmp / f"{k:03d}.png")
            k += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "consistency.gif")], check=True)
    keys = [Image.open(tmp / f"{n}.png").convert("RGB") for n in (5, 20, 80, 320)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "consistency_frames.png")
    shutil.rmtree(tmp)
