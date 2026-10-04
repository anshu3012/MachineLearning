"""Habit 3 in action: the t distribution next to the standard normal while the degrees of freedom rise.
The heavy tails shrink and the two curves merge. Plotly frames -> ffmpeg GIF, plus a key-frame grid for the PDF.
Run: python t_vs_normal.py  -> t_vs_normal.gif, t_vs_normal_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE = "#4C78A8", "#F58518"
x = np.linspace(-5, 5, 401)
DFS = [1, 2, 3, 4, 5, 7, 10, 15, 20, 30]
gap = {d: np.abs(stats.t.pdf(x, d) - stats.norm.pdf(x)).max() for d in DFS}
assert all(gap[a] > gap[b] for a, b in zip(DFS, DFS[1:]))       # the gap only shrinks as df rises
assert gap[1] > 0.09 and gap[30] < 0.005                          # far apart at df 1, nearly one curve at df 30


def frame(d):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=stats.norm.pdf(x), name="standard normal", line=dict(color=BLUE, width=4)))
    fig.add_trace(go.Scatter(x=x, y=stats.t.pdf(x, d), name=f"t, df = {d}", line=dict(color=ORANGE, width=4, dash="dash")))
    fig.update_layout(template="simple_white", width=900, height=560, font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text=f"df = {d}: largest gap {gap[d]:.3f}", x=0.5),
                      xaxis=dict(title="x", range=[-5, 5]), yaxis=dict(title="density", range=[0, 0.42]),
                      legend=dict(x=0.02, y=0.98), margin=dict(l=70, r=20, t=70, b=60))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".t_frames"
    tmp.mkdir(exist_ok=True)
    for k, d in enumerate(DFS):
        frame(d).write_image(tmp / f"{k:03d}.png")
    for k in range(len(DFS), len(DFS) + 4):                         # hold the last frame
        shutil.copy(tmp / f"{len(DFS) - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "t_vs_normal.gif")], check=True)
    keys = [Image.open(tmp / f"{DFS.index(d):03d}.png").convert("RGB") for d in (1, 3, 10, 30)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "t_vs_normal_frames.png")
    shutil.rmtree(tmp)
