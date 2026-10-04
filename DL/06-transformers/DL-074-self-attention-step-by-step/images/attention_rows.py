"""The learned attention weights of a real IMDB review forming one query word at a time.
Run: python attention_rows.py -> attention_rows.gif, attention_rows_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from common import BLUE, RED, FONT

HERE = Path(__file__).parent
w = pd.read_csv(HERE.parent / "data" / "weights_review.csv", index_col=[0, 1]).loc["learned"]
words = list(w.index)
W = w.values
n = len(words)
pos = list(range(n))


def frame(k):
    Z = np.full_like(W, np.nan)
    Z[:k + 1] = W[:k + 1]
    fig = make_subplots(1, 2, column_widths=[0.55, 0.45], horizontal_spacing=0.2,
                        subplot_titles=["weights so far (one row per query word)", f"row of '{words[k]}': weights sum to 1"])
    fig.add_trace(go.Heatmap(z=Z, x=pos, y=pos, colorscale="Blues", zmin=0, zmax=1, showscale=False,
                             text=np.where(np.isnan(Z), "", np.round(Z, 2).astype(str)), texttemplate="%{text}",
                             textfont=dict(size=11)), 1, 1)
    fig.add_shape(type="rect", x0=-0.5, x1=n - 0.5, y0=k - 0.5, y1=k + 0.5, line=dict(color=RED, width=4), fillcolor="rgba(0,0,0,0)", row=1, col=1)
    fig.add_trace(go.Bar(x=W[k], y=pos, orientation="h", marker_color=[RED if j == W[k].argmax() else BLUE for j in pos],
                         text=np.round(W[k], 2), textposition="outside"), 1, 2)
    fig.update_yaxes(autorange="reversed", tickvals=pos, ticktext=words, row=1, col=1)
    fig.update_xaxes(tickvals=pos, ticktext=words, tickangle=-45, row=1, col=1)
    fig.update_yaxes(autorange="reversed", tickvals=pos, ticktext=words, row=1, col=2)
    fig.update_xaxes(range=[0, 1.05], title="attention weight", row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=560, font=FONT, showlegend=False,
                      title=dict(text=f"query word {k + 1} of {n}: '{words[k]}'", x=0.5, y=0.98),
                      margin=dict(l=110, r=30, t=90, b=110))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".rows_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(n):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(n, n + 4):                                # hold the last frame
        shutil.copy(tmp / f"{n - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=880:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "attention_rows.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 3, 7, n - 1)]
    wd, ht = keys[0].size
    sheet = Image.new("RGB", (2 * wd + 16, 2 * ht + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (wd + 16), (i // 2) * (ht + 16)))
    sheet.save(HERE / "attention_rows_frames.png")
    shutil.rmtree(tmp)
