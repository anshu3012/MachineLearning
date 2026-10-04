"""EM fitting a two-component GMM to the 272 Old Faithful eruptions (duration and waiting time, both in minutes),
from a poor start. Left: observations coloured by responsibility and the 1- and 2-standard-deviation ellipses.
Right: the log-likelihood after each iteration; it never goes down.
Run: python em_2d.py -> em_2d.gif, em_2d_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

from em_core import FAITHFUL_START, FONT, GREY, faithful, run_em

HERE = Path(__file__).parent
RGB = np.array([[76, 120, 168], [245, 133, 24]])
X = faithful()
ITERS = 14
hist = run_em(X, *FAITHFUL_START, ITERS)
LL = np.array([h[4] for h in hist])
assert np.all(np.diff(LL) >= -1e-9)
t = np.linspace(0, 2 * np.pi, 120)


def frame(i):
    pi, mu, cov, R, ll = hist[i]
    fig = make_subplots(rows=1, cols=2, column_widths=[0.58, 0.42], horizontal_spacing=0.1,
                        subplot_titles=(f"iteration {i}", "log-likelihood"))
    mix = R @ RGB
    fig.add_trace(go.Scatter(x=X[:, 0], y=X[:, 1], mode="markers", showlegend=False,
                             marker=dict(size=6, color=["rgb(%d,%d,%d)" % tuple(int(v) for v in c) for c in mix])), 1, 1)
    for k in range(2):
        vals, vecs = np.linalg.eigh(cov[k])
        for s in (1, 2):
            e = mu[k] + s * (vecs @ np.diag(np.sqrt(vals)) @ np.vstack([np.cos(t), np.sin(t)])).T
            fig.add_trace(go.Scatter(x=e[:, 0], y=e[:, 1], mode="lines", showlegend=False,
                                     line=dict(color="rgb(%d,%d,%d)" % tuple(RGB[k]), width=3 if s == 1 else 2,
                                               dash="solid" if s == 1 else "dash")), 1, 1)
        fig.add_trace(go.Scatter(x=[mu[k, 0]], y=[mu[k, 1]], mode="markers", showlegend=False,
                                 marker=dict(symbol="x", size=14, color="black")), 1, 1)
    fig.add_trace(go.Scatter(x=np.arange(i + 1), y=LL[:i + 1], mode="lines+markers", line=dict(color=GREY, width=3),
                             showlegend=False), 1, 2)
    fig.update_xaxes(range=[0.5, 6], title_text="eruption duration (minutes)", row=1, col=1)
    fig.update_yaxes(range=[30, 110], title_text="waiting time (minutes)", row=1, col=1)
    fig.update_xaxes(range=[-0.5, ITERS + 0.5], title_text="iteration", row=1, col=2)
    fig.update_yaxes(range=[-2200, -1050], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=560, font=FONT,
                      title=dict(text=f"log-likelihood {ll:.0f}", x=0.5, y=0.98), margin=dict(l=70, r=20, t=90, b=60))
    fig.update_annotations(font_size=21)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".em2d_frames"
    tmp.mkdir(exist_ok=True)
    for i in range(ITERS + 1):
        frame(i).write_image(tmp / f"{i:03d}.png")
    for j in range(ITERS + 1, ITERS + 6):
        shutil.copy(tmp / f"{ITERS:03d}.png", tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "em_2d.gif")], check=True)
    keys = [Image.open(tmp / f"{i:03d}.png").convert("RGB") for i in (0, 1, 5, ITERS)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "em_2d_frames.png")
    shutil.rmtree(tmp)
    print(np.round(LL, 1))
