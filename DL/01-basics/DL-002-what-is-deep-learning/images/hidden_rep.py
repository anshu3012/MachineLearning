"""Representation learning on MNIST, from data/hidden_rep.npz (made by experiments/hidden_rep.py): 1,500 test digits
(the 432 threes, fives and eights among them) seen as raw pixels and as the 32 numbers of an MLP's last hidden layer after 0, 1, 2, 5 and 10 epochs of training,
each squeezed to 2D by PCA. The title gives the share of digits whose nearest neighbour in the 2D picture is the
same digit. Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from sklearn.neighbors import NearestNeighbors

HERE = Path(__file__).parent
D = np.load(HERE.parent / "data" / "hidden_rep.npz")
y = D["labels"]
PAL = {3: "#4C78A8", 5: "#F58518", 8: "#54A24B"}
VIEWS = [("p_pixels", "Raw pixels (784 numbers per digit)", None)] + \
        [(f"p{e}", f"Hidden layer after {e} epoch{'s' if e != 1 else ''} (32 numbers)", float(D[f"a{e}"]))
         for e in D["epochs"]]


def agree2d(P):
    _, nb = NearestNeighbors(n_neighbors=2).fit(P).kneighbors(P)
    return 100 * (y[nb[:, 1]] == y).mean()


SCORES = [agree2d(D[k]) for k, _, _ in VIEWS]
assert [round(v, 1) for v in SCORES] == [55.8, 47.9, 64.4, 69.4, 77.5, 87.3], SCORES
assert round(float(D["a10"]), 3) == 0.969


def frame(i):
    key, label, acc = VIEWS[i]
    P = D[key]
    P = (P - P.mean(0)) / P.std(0)
    fig = go.Figure()
    for c in (3, 5, 8):
        m = y == c
        fig.add_scatter(x=P[m, 0], y=P[m, 1], mode="markers", name=str(c),
                        marker=dict(size=9, color=PAL[c], opacity=0.75))
        fig.add_annotation(x=np.median(P[m, 0]), y=np.median(P[m, 1]), text=f"<b>{c}</b>", showarrow=False,
                           font=dict(size=34, color="black"), bgcolor="rgba(255,255,255,0.7)")
    sub = f"test accuracy {100 * acc:.1f}%, " if acc is not None else ""
    fig.update_layout(template="simple_white", width=900, height=820, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"<b>{label}</b><br>{sub}{SCORES[i]:.0f}% of the 3s, 5s and 8s sit next to the same digit",
                                 x=0.5, y=0.96, font=dict(size=22)),
                      xaxis=dict(visible=False, range=[-3.2, 3.2]), yaxis=dict(visible=False, range=[-3.2, 3.2]),
                      showlegend=False, margin=dict(l=10, r=10, t=100, b=10))
    return fig


if __name__ == "__main__":
    print([round(s, 1) for s in SCORES])
    tmp = HERE / ".hr_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for i in range(len(VIEWS)):
        keys.append(tmp / f"k{i}.png")
        frame(i).write_image(keys[-1])
    seq = [0] * 4 + [i for i in range(1, len(VIEWS)) for _ in range(3)] + [len(VIEWS) - 1] * 4
    for j, i in enumerate(seq):
        shutil.copy(keys[i], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse",
                    str(HERE / "hidden_rep.gif")], check=True)
    ims = [Image.open(keys[i]).convert("RGB") for i in (0, len(VIEWS) - 1)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, h), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "hidden_rep_frames.png")
    shutil.rmtree(tmp)
