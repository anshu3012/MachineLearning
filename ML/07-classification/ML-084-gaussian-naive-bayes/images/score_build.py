"""Gaussian Naive Bayes score for the new person (185 cm, 170 lb), built one factor at a time (Plotly frames + ffmpeg):
prior, times the height density, times the weight density, then normalised into probabilities. Log-scale bars.
Run: python score_build.py -> score_build.gif, score_build_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
df = pd.read_csv(HERE.parent / "data" / "people.csv")
Q = {"height_cm": 185, "weight_lb": 170}
COL = {"male": "#4C78A8", "female": "#E45756"}


def pdf(x, mu, sd):
    return np.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))


steps = {g: [] for g in COL}
for g in COL:
    d = df[df.gender == g]
    s = len(d) / len(df)
    steps[g].append(s)
    for c in Q:
        s *= pdf(Q[c], d[c].mean(), d[c].std())
        steps[g].append(s)
m, f = steps["male"][-1], steps["female"][-1]
assert round(m * 1e4, 1) == 5.5 and round(f * 1e5, 1) == 1.1 and round(m / (m + f), 2) == 0.98   # the Note's table
LABELS = ["prior P(class)", "× density of height 185", "× density of weight 170"]


def frame(k):
    fig = go.Figure()
    if k < 3:
        for g in COL:
            v = steps[g][k]
            fig.add_trace(go.Bar(x=[g], y=[v], marker_color=COL[g], text=[f"{v:.2g}"], textposition="outside",
                                 showlegend=False))
        fig.update_yaxes(type="log", range=[-5.6, 0.4], dtick=1, exponentformat="power", title="score (log scale)")
        title = "step " + str(k + 1) + ": " + LABELS[k]
    else:
        for g, v in (("male", m), ("female", f)):
            p = v / (m + f)
            fig.add_trace(go.Bar(x=[g], y=[p], marker_color=COL[g], text=[f"{p:.0%}"], textposition="outside",
                                 showlegend=False))
        fig.update_yaxes(range=[0, 1.15], title="probability")
        title = f"step 4: divide by the total → predict male"
    fig.update_layout(template="simple_white", width=900, height=620, font=dict(family="Latin Modern Roman", size=26),
                      title=dict(text=title, x=0.5), margin=dict(l=110, r=30, t=80, b=60), bargap=0.45)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".score_frames"
    tmp.mkdir(exist_ok=True)
    j = 0
    for k, hold in ((0, 4), (1, 5), (2, 6), (3, 10)):
        frame(k).write_image(tmp / f"key_{k}.png")
        for _ in range(hold):
            shutil.copy(tmp / f"key_{k}.png", tmp / f"{j:03d}.png")
            j += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=6,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "score_build.gif")], check=True)
    keys = [Image.open(tmp / f"key_{k}.png").convert("RGB") for k in range(4)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for n, im in enumerate(keys):
        sheet.paste(im, ((n % 2) * (w + 16), (n // 2) * (h + 16)))
    sheet.save(HERE / "score_build_frames.png")
    shutil.rmtree(tmp)
