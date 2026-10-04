"""The 256 first-layer weights during training, without regularisation (blue) and with L2(0.03) (orange), same
start: one histogram per snapshot epoch. Data: data/weight_snapshots.csv from the Notebook.
Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from common import BLUE, ORANGE

HERE = Path(__file__).parent
s = pd.read_csv(HERE.parent / "data" / "weight_snapshots.csv")
FONT = dict(family="Latin Modern Roman", size=22)
EPOCHS = sorted(s.epoch.unique())
RUNS = (("none", BLUE, "no regularisation"), ("L2", ORANGE, "L2, λ = 0.03"))
BINS = dict(start=-3, end=3, size=0.1)
TOP = max(np.histogram(s[(s.run == r) & (s.epoch == e)].w, bins=np.arange(-3, 3.01, 0.1))[0].max()
          for r, _, _ in RUNS for e in EPOCHS)


def frame(ep):
    fig = go.Figure()
    for i, (r, c, label) in enumerate(RUNS):
        w = s[(s.run == r) & (s.epoch == ep)].w
        fig.add_trace(go.Histogram(x=w, xbins=BINS, name=f"{label}: largest |w| {w.abs().max():.2f}",
                                   marker_color=c, opacity=0.6))
    fig.update_layout(barmode="overlay", template="simple_white", width=1000, height=580, font=FONT,
                      title=dict(text=f"first-layer weights, epoch {ep:,}", x=0.5),
                      xaxis=dict(title="weight", range=[-3, 3]),
                      yaxis=dict(title="number of weights", range=[0, 1.05 * TOP]),
                      legend=dict(x=0.02, y=0.98), margin=dict(l=80, r=20, t=70, b=60))
    return fig


SEQ = [EPOCHS[0]] * 4 + [e for e in EPOCHS for _ in range(2)] + [EPOCHS[-1]] * 8
KEYS = [0, 20, 200, EPOCHS[-1]]

if __name__ == "__main__":
    assert set(KEYS) <= set(EPOCHS)
    tmp = HERE / ".wd_frames"
    tmp.mkdir(exist_ok=True)
    made = {}
    for k, ep in enumerate(SEQ):
        out = tmp / f"{k:03d}.png"
        if ep in made:
            shutil.copy(made[ep], out)
        else:
            frame(ep).write_image(out)
            made[ep] = out
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "weight_decay_anim.gif")], check=True)
    keys = [Image.open(made[k]).convert("RGB") for k in KEYS]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "weight_decay_anim_frames.png")
    shutil.rmtree(tmp)
