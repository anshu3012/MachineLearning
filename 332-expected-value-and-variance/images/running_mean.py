"""The expected value as a long-run average: the running mean of 100,000 die rolls (seed 42, as in the Note)
after each roll, on a log axis. Early averages swing widely; they close in on E[X] = 3.5 and end at 3.49982.
Run: python running_mean.py  -> running_mean.gif, running_mean_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE = "#4C78A8", "#F58518"
rng = np.random.default_rng(42)
rolls = rng.integers(1, 7, 100_000)
run = np.cumsum(rolls) / np.arange(1, len(rolls) + 1)
assert round(run[-1], 5) == 3.49982
idx = np.unique(np.geomspace(1, len(rolls), 500).astype(int)) - 1     # log-spaced points keep the line light


def frame(n):
    keep = idx[idx < n]
    fig = go.Figure()
    fig.add_hline(y=3.5, line=dict(color=ORANGE, width=3, dash="dash"), opacity=1)
    fig.add_annotation(x=np.log10(30_000), y=3.5, yshift=-20, xanchor="center", showarrow=False, text="E[X] = 3.5",
                       font=dict(size=24, color=ORANGE))
    fig.add_scatter(x=keep + 1, y=run[keep], mode="lines", line=dict(color=BLUE, width=3))
    fig.add_scatter(x=[n], y=[run[n - 1]], mode="markers", marker=dict(size=14, color=BLUE))
    fig.add_annotation(x=0.98, y=0.04, xref="paper", yref="paper", xanchor="right", yanchor="bottom",
                       showarrow=False, bgcolor="white", font=dict(size=26),
                       text=f"after {n:,} rolls<br>average = <b>{run[n - 1]:.5f}</b>")
    fig.update_layout(template="simple_white", width=900, height=540, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text="running average of die rolls", x=0.5, y=0.96),
                      xaxis=dict(type="log", title="number of rolls", range=[0, 5.05], dtick=1,
                                 exponentformat="none", separatethousands=True),
                      yaxis=dict(title="average so far", range=[1, 6.05]), margin=dict(l=70, r=30, t=70, b=60))
    return fig


SHOW = [1, 2, 3, 5, 8, 12, 20, 30, 50, 80, 130, 200, 350, 600, 1000, 1800, 3000, 5000, 10_000, 20_000, 50_000,
        100_000]
PLAN = [(n, 2 if n < 10 else 1) for n in SHOW[:-1]] + [(SHOW[-1], 14)]

if __name__ == "__main__":
    tmp = HERE / ".run_frames"
    tmp.mkdir(exist_ok=True)
    m, keys = 0, []
    for i, (n, hold) in enumerate(PLAN):
        frame(n).write_image(tmp / f"{m:03d}.png")
        if n in (3, 30, 1000, 100_000):
            keys.append(m)
        for _ in range(hold - 1):
            shutil.copy(tmp / f"{m:03d}.png", tmp / f"{m + 1:03d}.png")
            m += 1
        m += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "running_mean.gif")], check=True)
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "running_mean_frames.png")
    shutil.rmtree(tmp)
