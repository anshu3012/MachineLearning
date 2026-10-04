"""The photo of Figure 1 rebuilt layer by layer: left, the sum of the first k rank-1 layers; right, the layers just
added (blue positive, red negative); below, the singular values with the kept ones filled and the error
sigma_(k+1)/sigma_1 in the title. k = 1, 2, ..., 10, then in bigger steps to 100.
Run: python rank_rebuild.py -> rank_rebuild.gif, rank_rebuild_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from sklearn.datasets import load_sample_image

HERE = Path(__file__).parent
BLUE, GREY = "#4C78A8", "#6B6B6B"
img = load_sample_image("china.jpg").astype(float) @ [0.299, 0.587, 0.114] / 255   # same matrix as figures.py
m, n = img.shape
U, s, Vt = np.linalg.svd(img, full_matrices=False)
assert round(s[0], 1) == 326.7 and round(s[20] / s[0], 3) == 0.023            # the Note's numbers
KS = list(range(1, 11)) + [12, 15, 20, 25, 30, 40, 50, 70, 100]


def part(a, b):
    return (U[:, a:b] * s[a:b]) @ Vt[a:b]


def frame(j):
    k, prev = KS[j], (KS[j - 1] if j else 0)
    added = part(prev, k)
    fig = make_subplots(rows=2, cols=2, specs=[[{}, {}], [{"colspan": 2}, None]], row_heights=[0.6, 0.4],
                        horizontal_spacing=0.03, vertical_spacing=0.14,
                        subplot_titles=[f"sum of the first {k} layer{'s' * (k > 1)}",
                                        f"layer {k} added" if k - prev == 1 else f"layers {prev + 1}–{k} added", ""])
    fig.add_trace(go.Heatmap(z=part(0, k), colorscale="gray", zmin=0, zmax=1, showscale=False), 1, 1)
    lim = np.abs(added).max()                                   # each frame on its own scale
    fig.add_trace(go.Heatmap(z=added, colorscale="RdBu", zmid=0, zmin=-lim, zmax=lim, showscale=False), 1, 2)
    for c in (1, 2):
        fig.update_xaxes(visible=False, row=1, col=c)
        fig.update_yaxes(visible=False, autorange="reversed", scaleanchor="x" if c == 1 else "x2", row=1, col=c)
    i = np.arange(1, len(s) + 1)
    fig.add_trace(go.Scatter(x=i, y=s, mode="lines", line=dict(color=GREY, width=2.5)), 2, 1)
    fig.add_trace(go.Scatter(x=i[:k], y=s[:k], mode="lines", fill="tozeroy", line=dict(color=BLUE, width=4),
                             fillcolor="rgba(76,120,168,0.35)"), 2, 1)
    fig.add_trace(go.Scatter(x=[k + 1], y=[s[k]], mode="markers", marker=dict(color="#E45756", size=13)), 2, 1)
    fig.update_xaxes(type="log", dtick=1, title_text="i (log scale)", range=[0, np.log10(len(s))], row=2, col=1)
    fig.update_yaxes(type="log", title_text="σ<sub>i</sub>", dtick=1, row=2, col=1)
    fig.update_layout(template="simple_white", width=960, height=760, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), margin=dict(l=80, r=20, t=90, b=60),
                      title=dict(text=f"<b>k = {k}: {k * (m + n + 1) / (m * n):.1%} stored, "
                                      f"error σ<sub>{k + 1}</sub>/σ<sub>1</sub> = {s[k] / s[0]:.1%}</b>", x=0.5, y=0.97))
    fig.update_annotations(font_size=24)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".rank_frames"
    tmp.mkdir(exist_ok=True)
    for j in range(len(KS)):
        frame(j).write_image(tmp / f"{j:03d}.png")
    last = len(KS) - 1
    for j in range(last + 1, last + 4):                           # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "rank_rebuild.gif")], check=True)
    keys = [Image.open(tmp / f"{KS.index(k):03d}.png").convert("RGB") for k in (1, 5, 20, 100)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "rank_rebuild_frames.png")
    shutil.rmtree(tmp)
