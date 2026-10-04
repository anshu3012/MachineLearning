"""The gradient travelling back through a linear SimpleRNN whose W_h is s times an orthogonal matrix, step by step.
Left: gradient size relative to the last word, by distance, with s^d dashed; right: the current size as bars.
Data: data/linear_scaled_wh.csv (Notebook section 2).
Run: python gradient_travel.py  -> gradient_travel.gif, gradient_travel_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

from common import BLUE, GREY, RED

HERE = Path(__file__).parent
d = pd.read_csv(HERE.parent / "data" / "linear_scaled_wh.csv")
SERIES = []
for s, c, name in ((1.1, RED, "s = 1.1"), (1.0, GREY, "s = 1.0"), (0.9, BLUE, "s = 0.9")):
    g = d[d.scale == s].set_index("distance").grad.sort_index()
    SERIES.append((s, c, name, (g / g[0]).values))
assert abs(SERIES[2][3][50] - 0.0062) < 5e-4 and abs(SERIES[0][3][50] - 141) < 1     # table of section 4.4
DIST = list(range(0, 51, 2)) + list(range(58, 200, 8)) + [199]
KEYS = (10, 50, 106, 199)


def label(v):
    if 1e-3 <= v < 1e4:
        return f"×{v:.2g}" if v < 1 else f"×{v:.3g}"
    m, e = f"{v:.0e}".split("e")
    return f"×{m}·10<sup>{int(e)}</sup>"


def frame(k):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.62, 0.38], horizontal_spacing=0.08)
    x = np.arange(k + 1)
    for s, c, name, r in SERIES:
        fig.add_trace(go.Scatter(x=np.arange(200), y=s ** np.arange(200.0), mode="lines", showlegend=False,
                                 line=dict(color=c, width=2, dash="dot"), opacity=0.45), 1, 1)
        fig.add_trace(go.Scatter(x=x, y=r[:k + 1], mode="lines", name=name, line=dict(color=c, width=5),
                                 showlegend=False), 1, 1)
        fig.add_trace(go.Scatter(x=[k], y=[r[k]], mode="markers", marker=dict(color=c, size=14), showlegend=False), 1, 1)
        fig.add_trace(go.Bar(x=[name], y=[r[k]], marker_color=c, text=[label(r[k])], textposition="outside",
                             textfont=dict(size=22, color=c), cliponaxis=False, showlegend=False), 1, 2)
    fig.update_xaxes(range=[0, 200], title_text="steps back from the last word", row=1, col=1)
    fig.update_yaxes(type="log", range=[-10, 9.5], exponentformat="power", dtick=3,
                     title_text="gradient size, relative to the last word", row=1, col=1)
    fig.update_yaxes(type="log", range=[-10, 9.5], showticklabels=False, row=1, col=2)
    fig.update_layout(template="simple_white", width=1000, height=600, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"the gradient after {k} steps back through W<sub>h</sub>", x=0.5, y=0.97),
                      margin=dict(l=90, r=20, t=110, b=70),
                      annotations=[dict(text="dotted: s<sup>d</sup>", x=0.02, y=1.06, xref="paper", yref="paper",
                                        showarrow=False, font=dict(size=20, color=GREY), xanchor="left")])
    return fig


if __name__ == "__main__":
    tmp = HERE / ".travel_frames"
    tmp.mkdir(exist_ok=True)
    for i, k in enumerate(DIST):
        frame(k).write_image(tmp / f"{i:03d}.png")
    n = len(DIST)
    for i in range(n, n + 16):                                    # hold the last frame
        shutil.copy(tmp / f"{n - 1:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "8", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "gradient_travel.gif")], check=True)
    keys = [Image.open(tmp / f"{DIST.index(k):03d}.png").convert("RGB") for k in KEYS]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "gradient_travel_frames.png")
    shutil.rmtree(tmp)
