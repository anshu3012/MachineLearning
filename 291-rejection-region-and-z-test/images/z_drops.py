"""The rejection region at work when H0 is true. The chips example of section 7 is repeated 400 times with
packets whose true mean really is 50 g (sigma = 4 g, n = 40): each sample's z drops onto the standard normal curve
and turns red if it lands in the two-tailed rejection region. Then alpha sweeps from 0.30 to 0.01 over the same
400 z values, and finally the watchdog's observed z = -1.58 lands.
Run: python z_drops.py  -> z_drops.gif, z_drops_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE, RED, GREEN, GREY = "#4C78A8", "#E45756", "#54A24B", "#6B6B6B"
MU0, SIGMA, N, REPS, BW = 50, 4, 40, 400, 0.2
rng = np.random.default_rng(42)
zs = (rng.normal(MU0, SIGMA, size=(REPS, N)).mean(1) - MU0) / (SIGMA / np.sqrt(N))
for a in (0.30, 0.05, 0.01):                                 # rejected share stays within 3 binomial SEs of alpha
    assert abs((np.abs(zs) > stats.norm.ppf(1 - a / 2)).mean() - a) < 3 * np.sqrt(a * (1 - a) / REPS), a
Z_OBS = (49 - 50) / (4 / np.sqrt(40))
x = np.linspace(-4, 4, 600)

b = np.floor(zs / BW)                                        # dot pile: each dot has area 1/REPS, so the pile
ys = np.array([(b[:i] == b[i]).sum() + 0.5 for i in range(REPS)]) / (REPS * BW)   # traces the density curve
xs = zs                                                      # true position; only the height is binned


def frame(k, alpha, title, obs=False):
    c = stats.norm.ppf(1 - alpha / 2)
    rej = np.abs(zs[:k]) > c
    fig = go.Figure()
    for side in (x[x <= -c], x[x >= c]):
        fig.add_scatter(x=side, y=stats.norm.pdf(side), fill="tozeroy", fillcolor="rgba(228,87,86,0.25)",
                        line=dict(width=0))
    fig.add_scatter(x=x, y=stats.norm.pdf(x), mode="lines", line=dict(color="black", width=3))
    fig.add_scatter(x=xs[:k], y=ys[:k], mode="markers",
                    marker=dict(size=10, color=np.where(rej, RED, BLUE), line=dict(width=1, color="white")))
    for s in (-1, 1):
        fig.add_vline(x=s * c, line=dict(color=RED, width=3, dash="dash"), opacity=1)
    fig.add_annotation(x=c, y=0.415, text=f"±{c:.2f}", showarrow=False, xanchor="left", xshift=6,
                       font=dict(color=RED))
    if k:
        fig.add_annotation(x=-3.95, y=0.37, xanchor="left", showarrow=False, align="left",
                           text=f"α = {alpha:.2f}<br>rejected: {rej.sum()} of {k}<br>= <b>{100 * rej.mean():.1f}%</b>",
                           font=dict(size=26, color=RED), bgcolor="white")
    if obs:
        fig.add_vline(x=Z_OBS, line=dict(color=GREEN, width=5), opacity=1)
        fig.add_annotation(x=Z_OBS, y=0.2, ax=-120, ay=0, text="observed<br>z = −1.58", arrowcolor=GREEN,
                           arrowwidth=3, font=dict(size=26, color=GREEN), bgcolor="white")
    fig.update_layout(template="simple_white", width=900, height=620, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=24), title=dict(text=title, x=0.5, y=0.96),
                      xaxis=dict(title="z", range=[-4, 4]), yaxis=dict(showticklabels=False, range=[0, 0.44]),
                      margin=dict(l=30, r=30, t=80, b=60))
    return fig


H0 = "H₀ true: 400 samples of 40 packets"
SCHEDULE = [(k, 0.05, H0, False, 2) for k in (1, 2, 3, 4, 5, 6, 8, 10)] \
    + [(k, 0.05, H0, False, 1) for k in (15, 25, 40, 60, 90, 130, 180, 240, 310)] \
    + [(400, 0.05, H0, False, 6)] \
    + [(400, a, "same 400 z values, α changes", False, 4) for a in (0.30, 0.20, 0.10, 0.05, 0.01)] \
    + [(400, 0.05, "the watchdog's sample: fail to reject H₀", True, 12)]

if __name__ == "__main__":
    tmp = HERE / ".z_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, []
    for i, (k, a, title, obs, rep) in enumerate(SCHEDULE):
        frame(k, a, title, obs).write_image(tmp / f"{n:03d}.png")
        if i in (2, 17, 18, len(SCHEDULE) - 1):
            keys.append(n)
        for _ in range(rep - 1):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + 1:03d}.png")
            n += 1
        n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "z_drops.gif")], check=True)
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "z_drops_frames.png")
    shutil.rmtree(tmp)
