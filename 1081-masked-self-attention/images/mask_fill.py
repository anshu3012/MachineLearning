"""Masked self-attention, one row per frame: the word being computed may take only from itself and the words before it.
Run: python mask_fill.py -> mask_fill.gif, mask_fill_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
a = pd.read_csv(HERE.parent / "data" / "weights_masked.csv", index_col=0)
toks, W = list(a.columns), a.values
n = len(toks)


def frame(k):
    """Rows 0..k-1 filled; row k-1 is the one being computed now."""
    z = np.full((n, n), np.nan)
    z[:k] = W[:k]
    z[np.triu_indices(n, 1)] = np.nan                       # future cells: drawn grey underneath
    text = [[("0" if j > i else f"{W[i, j]:.2f}") if i < k else "" for j in range(n)] for i in range(n)]
    fig = go.Figure(go.Heatmap(z=z, x=list(range(n)), y=list(range(n)), zmin=0, zmax=1, colorscale="Blues", showscale=False,
                               text=text, texttemplate="%{text}", textfont=dict(size=20), xgap=2, ygap=2))
    for i in range(n):                                      # grey cells: the future, blocked by the mask
        for j in range(i + 1, n):
            fig.add_shape(type="rect", x0=j - 0.5, x1=j + 0.5, y0=i - 0.5, y1=i + 0.5, fillcolor="#DDDDDD",
                          line=dict(width=0), layer="below")
    if k:
        fig.add_shape(type="rect", x0=-0.5, x1=n - 0.5, y0=k - 1.5, y1=k - 0.5, line=dict(color="#E45756", width=4),
                      fillcolor="rgba(0,0,0,0)")
        title = f"computing '{toks[k - 1]}': it may take from " + ", ".join(f"'{t}'" for t in toks[:k])
    else:
        title = "grey: future words, blocked by the mask (weight 0)"
    fig.update_layout(template="simple_white", width=820, height=700, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=title, x=0.5, font=dict(size=20)),
                      xaxis=dict(tickmode="array", tickvals=list(range(n)), ticktext=toks, title="word taken from (key)"),
                      yaxis=dict(tickmode="array", tickvals=list(range(n)), ticktext=toks, autorange="reversed",
                                 title="word being computed (query)"),
                      margin=dict(l=120, r=30, t=80, b=70), plot_bgcolor="white")
    return fig


if __name__ == "__main__":
    tmp = HERE / ".mask_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(n + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(n + 1, n + 4):                            # hold the last frame
        shutil.copy(tmp / f"{n:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "mask_fill.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (1, 2, 3, n)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "mask_fill_frames.png")
    shutil.rmtree(tmp)
