"""Softmax saturation as the vector length d grows. One random query and 10 random keys (standard normal numbers,
seed 0); at length d we use their first d numbers. Left: weights from the raw dot products; right: from the dot
products divided by sqrt(d). Under each panel: the averages over 2,000 random draws from the Notebook
(data/saturation.csv). Run: python saturation_anim.py -> saturation_anim.gif, saturation_anim_frames.png
(Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from common import BLUE, ORANGE, GREY, FONT

HERE = Path(__file__).parent
sat = pd.read_csv(HERE.parent / "data" / "saturation.csv")
rng = np.random.default_rng(0)
q, K = rng.normal(size=1024), rng.normal(size=(10, 1024))
DS = [d for d in sorted(sat.d.unique()) if d >= 1]


def softmax(s):
    e = np.exp(s - s.max())
    return e / e.sum()


def frame(d):
    s = K[:, :d] @ q[:d]
    w_un, w_sc = softmax(s), softmax(s / np.sqrt(d))
    m = sat[sat.d == d].set_index("version")
    fig = make_subplots(1, 2, horizontal_spacing=0.1,
                        subplot_titles=("without scaling: softmax(q·k)", "scaled: softmax(q·k / √d)"))
    keys = [f"k{j + 1}" for j in range(10)]
    for c, (w, col) in enumerate(((w_un, ORANGE), (w_sc, BLUE)), 1):
        fig.add_trace(go.Bar(x=keys, y=w, marker_color=col, text=[f"{v:.2f}" for v in w], textposition="outside",
                             textfont=dict(size=13)), 1, c)
        fig.update_yaxes(range=[0, 1.1], title="weight" if c == 1 else None, row=1, col=c)
    for c, v in ((1, "unscaled"), (2, "scaled")):
        fig.add_annotation(xref=f"x{'' if c == 1 else 2} domain", yref="paper", x=0.5, y=-0.2, showarrow=False,
                           text=f"average over 2,000 draws: largest weight {m.loc[v, 'max_weight']:.2f}, "
                                f"gradient size {m.loc[v, 'jacobian_norm']:.2f}", font=dict(size=15, color=GREY))
    fig.update_layout(template="simple_white", width=1150, height=520, font=dict(FONT, size=17), showlegend=False,
                      title=dict(text=f"vector length d = {d}", x=0.5, font=dict(size=24)),
                      margin=dict(l=70, r=20, t=110, b=110))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".sat_frames"
    tmp.mkdir(exist_ok=True)
    for k, d in enumerate(DS):
        frame(d).write_image(tmp / f"{k:03d}.png")
    n = len(DS)
    for k in range(n, n + 3):
        shutil.copy(tmp / f"{n - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "saturation_anim.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (DS.index(4), n - 1)]
    w_, h_ = keys[0].size
    sheet = Image.new("RGB", (w_, 2 * h_ + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, (0, i * (h_ + 16)))
    sheet.save(HERE / "saturation_anim_frames.png")
    shutil.rmtree(tmp)
    print(DS)
