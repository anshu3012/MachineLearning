"""Why cross entropy and not squared error for probabilities. The predicted probability p of the true class falls
from 0.95 to 0.05. Cross entropy -ln p (blue) shoots up; the squared residual (1 - p)^2 (orange) never passes 1.
Red lines: the tangents at the current p; their slopes, -1/p and -2(1 - p), set the size of the gradient step.
At p = 0.05: -20 against -1.9.
Run: python ce_vs_squared.py -> ce_vs_squared.gif, ce_vs_squared_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
PS = np.round(np.arange(0.95, 0.049, -0.05), 2)
pg = np.linspace(0.005, 1, 400)
ce, se = lambda p: -np.log(p), lambda p: (1 - p) ** 2
dce, dse = lambda p: -1 / p, lambda p: -2 * (1 - p)
assert abs(dce(0.05) + 20) < 1e-9 and abs(dse(0.05) + 1.9) < 1e-9


def frame(p):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pg, y=ce(pg), mode="lines", line=dict(color=BLUE, width=4), name="cross entropy −ln p"))
    fig.add_trace(go.Scatter(x=pg, y=se(pg), mode="lines", line=dict(color=ORANGE, width=4), name="squared residual (1 − p)²"))
    for f, d, c in ((ce, dce, BLUE), (se, dse, ORANGE)):
        h = 0.12 / np.sqrt(1 + d(p) ** 2) * 3                  # short tangent segment of similar length
        tt = np.array([p - h, p + h])
        fig.add_trace(go.Scatter(x=tt, y=f(p) + d(p) * (tt - p), mode="lines", line=dict(color=RED, width=3),
                                 showlegend=False))
        fig.add_trace(go.Scatter(x=[p], y=[f(p)], mode="markers", marker=dict(size=14, color=c), showlegend=False))
    fig.update_xaxes(range=[0, 1], title_text="predicted probability p of the true class")
    fig.update_yaxes(range=[0, 3.5], title_text="loss")
    fig.update_layout(template="simple_white", width=900, height=620, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"p = {p:.2f}    slope: cross entropy {dce(p):.1f},  squared {dse(p):.1f}",
                                 x=0.5, y=0.97),
                      legend=dict(x=0.45, y=0.95), margin=dict(l=80, r=30, t=80, b=60))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".ce_frames"
    tmp.mkdir(exist_ok=True)
    for k, p in enumerate(PS):
        frame(p).write_image(tmp / f"{k:03d}.png")
    last = len(PS) - 1
    for k in range(last + 1, last + 7):                        # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "ce_vs_squared.gif")], check=True)
    keys = [Image.open(tmp / f"{list(PS).index(v):03d}.png").convert("RGB") for v in (0.9, 0.55, 0.25, 0.05)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "ce_vs_squared_frames.png")
    shutil.rmtree(tmp)
