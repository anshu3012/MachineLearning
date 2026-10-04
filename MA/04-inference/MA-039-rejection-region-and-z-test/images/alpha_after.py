"""Why alpha must be fixed before the test: the chips example (z = -1.58, two-tailed). As alpha grows, the red
rejection tails grow inward; once alpha passes 2 P(Z > 1.58) = 0.114 they swallow the observed z, and the same
data would "reject" H0.
Run: python alpha_after.py  -> alpha_after.gif, alpha_after_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
RED, GREEN = "#E45756", "#54A24B"
Z_OBS = (49 - 50) / (4 / np.sqrt(40))
A_FLIP = 2 * stats.norm.sf(abs(Z_OBS))
assert round(Z_OBS, 2) == -1.58 and round(A_FLIP, 3) == 0.114
x = np.linspace(-4, 4, 600)


def frame(alpha):
    c = stats.norm.ppf(1 - alpha / 2)
    reject = abs(Z_OBS) > c
    fig = go.Figure()
    for side in (x[x <= -c], x[x >= c]):
        fig.add_scatter(x=side, y=stats.norm.pdf(side), fill="tozeroy", fillcolor="rgba(228,87,86,0.35)",
                        line=dict(width=0))
    fig.add_scatter(x=x, y=stats.norm.pdf(x), mode="lines", line=dict(color="black", width=3))
    for s in (-1, 1):
        fig.add_vline(x=s * c, line=dict(color=RED, width=3, dash="dash"), opacity=1)
    fig.add_vline(x=Z_OBS, line=dict(color=GREEN, width=5), opacity=1)
    fig.add_annotation(x=Z_OBS, y=0.30, ax=-110, ay=0, text="z = −1.58", arrowcolor=GREEN, arrowwidth=3,
                       font=dict(size=26, color=GREEN), bgcolor="white")
    verdict = "<b>reject H₀</b>" if reject else "fail to reject H₀"
    fig.add_annotation(x=3.95, y=0.40, xanchor="right", showarrow=False, align="right",
                       text=f"α = {alpha:.3f}<br>critical ±{c:.2f}<br>{verdict}",
                       font=dict(size=26, color=RED if reject else "black"), bgcolor="white")
    fig.update_layout(template="simple_white", width=900, height=560, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text="same data, growing α", x=0.5, y=0.96),
                      xaxis=dict(title="z", range=[-4, 4]), yaxis=dict(showticklabels=False, range=[0, 0.45]),
                      margin=dict(l=30, r=30, t=70, b=60))
    return fig


# (alpha, frames to hold): sweep up from 0.01, pause at the usual 0.05 and at the flip point 0.114
PLAN = [(0.01, 4), (0.02, 1), (0.03, 1), (0.04, 1), (0.05, 6), (0.07, 1), (0.09, 1), (0.10, 1), (0.11, 1),
        (A_FLIP - 0.001, 4), (A_FLIP + 0.002, 6), (0.15, 2), (0.20, 8)]
assert abs(Z_OBS) < stats.norm.ppf(1 - 0.05 / 2) and abs(Z_OBS) > stats.norm.ppf(1 - 0.20 / 2)

if __name__ == "__main__":
    tmp = HERE / ".alpha_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, []
    for i, (a, hold) in enumerate(PLAN):
        frame(a).write_image(tmp / f"{n:03d}.png")
        if i in (0, 4, 9, 10):
            keys.append(n)
        for _ in range(hold - 1):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + 1:03d}.png")
            n += 1
        n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "alpha_after.gif")], check=True)
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "alpha_after_frames.png")
    shutil.rmtree(tmp)
