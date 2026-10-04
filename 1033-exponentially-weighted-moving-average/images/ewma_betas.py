"""EWMA of Delhi's 2013 temperatures as beta grows from 0.1 to 0.98: the curve goes from spiky to smooth.
Run: python ewma_betas.py -> ewma_betas.gif, ewma_betas_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from common import BLUE, GREY, FONT

HERE = Path(__file__).parent
d = pd.read_csv(HERE.parent / "data" / "delhi_climate.csv", parse_dates=["date"])
d = d[d.date.dt.year == 2013]
theta = d.meantemp.to_numpy()
BETAS = [0.1, 0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 0.98]
KEYS = [0.1, 0.5, 0.9, 0.98]                   # the four values in the PDF grid


def ewma(beta):
    v, out = theta[0], []                       # V_0 = theta_1
    for t in theta:
        v = beta * v + (1 - beta) * t
        out.append(v)
    return out


def frame(beta):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d.date, y=theta, mode="markers", name="daily temperature",
                             marker=dict(color=GREY, size=5, opacity=0.5)))
    fig.add_trace(go.Scatter(x=d.date, y=ewma(beta), name="EWMA", line=dict(color=BLUE, width=4)))
    fig.update_layout(template="simple_white", width=900, height=520, font=dict(FONT, size=20),
                      title=dict(text=f"β = {beta}   (averages about 1/(1 − β) ≈ {1 / (1 - beta):.3g} days)",
                                 x=0.5, y=0.96),
                      yaxis=dict(title="temperature (°C)", range=[4, 40]), xaxis=dict(title="2013"),
                      showlegend=False, margin=dict(l=75, r=20, t=70, b=60))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".ewma_frames"
    tmp.mkdir(exist_ok=True)
    order = BETAS + BETAS[-2:0:-1]              # up, then back down, so the GIF loops smoothly
    for k, b in enumerate(order):
        frame(b).write_image(tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "ewma_betas.gif")], check=True)
    keys = [Image.open(tmp / f"{BETAS.index(b):03d}.png").convert("RGB") for b in KEYS]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "ewma_betas_frames.png")
    shutil.rmtree(tmp)
