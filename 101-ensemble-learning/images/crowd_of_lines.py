"""Wisdom of the crowd for regression: the 60 points of why_it_works.py (b) (true trend y = 2 + 0.8x, noise 2.2).
Lines are added one per frame, each fitted to 10 random points (the first four are the figure's four lines).
Left: the lines (faint), their mean (black), the true trend (dashed). Right: how far the mean line is from the
true trend (root mean squared gap over x in [0, 10]) as the crowd grows, averaged over 500 crowds drawn the same way,
against the average gap of one line.
Run: python crowd_of_lines.py  -> crowd_of_lines.gif, crowd_of_lines_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

HERE = Path(__file__).parent
GREY, RED = "#6B6B6B", "#E45756"
rng = np.random.default_rng(7)
x = rng.uniform(0, 10, 60)
yv = 2 + 0.8 * x + rng.normal(0, 2.2, 60)
N = 25
g = np.linspace(0, 10, 101)
true = 2 + 0.8 * g
def crowd_of(rng):
    out = []
    for _ in range(N):
        idx = rng.choice(60, 10, replace=False)
        out.append(np.polyval(np.polyfit(x[idx], yv[idx], 1), g))
    return np.array(out)


gap = lambda line: np.sqrt(((line - true) ** 2).mean())
lines = crowd_of(rng)                                          # the crowd we draw
many = [crowd_of(np.random.default_rng(1000 + s)) for s in range(500)]
crowd = [np.mean([gap(c[:n].mean(0)) for c in many]) for n in range(1, N + 1)]
single = crowd[0]
assert crowd[-1] < 0.6 * single and all(np.diff(crowd[:10]) < 0)   # the mean of more lines is closer, on average
print("typical single line", round(single, 2), "crowd", np.round(crowd, 2))


def frame(n):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45], horizontal_spacing=0.12,
                        subplot_titles=(f"{n} lines and their mean" if n > 1 else "1 line", "gap from the true trend<br>(average of 500 crowds)"))
    fig.add_trace(go.Scatter(x=x, y=yv, mode="markers", marker=dict(color="#BBBBBB", size=7)), 1, 1)
    for l in lines[:n]:
        fig.add_trace(go.Scatter(x=g, y=l, mode="lines", line=dict(color="#4C78A8", width=2), opacity=0.45), 1, 1)
    fig.add_trace(go.Scatter(x=g, y=true, mode="lines", line=dict(color=RED, width=3, dash="dash")), 1, 1)
    fig.add_trace(go.Scatter(x=g, y=lines[:n].mean(0), mode="lines", line=dict(color="black", width=5)), 1, 1)
    fig.add_trace(go.Scatter(x=np.arange(1, n + 1), y=crowd[:n], mode="lines+markers", line=dict(color="black", width=4),
                             marker=dict(size=9)), 1, 2)
    fig.add_hline(y=single, line=dict(color=GREY, dash="dot", width=3), row=1, col=2)
    fig.add_annotation(x=N, y=single, text=f"one line: {single:.2f}", xanchor="right", yanchor="bottom", showarrow=False,
                       font=dict(color=GREY), row=1, col=2)
    fig.add_annotation(x=n, y=crowd[n - 1], text=f"mean of {n}: {crowd[n - 1]:.2f}", xanchor="left" if n < 15 else "right", yanchor="top",
                       showarrow=False, xshift=6 if n < 15 else 0, yshift=-8, row=1, col=2)
    fig.update_xaxes(title="input", range=[0, 10], row=1, col=1)
    fig.update_yaxes(title="output", range=[-2, 16], row=1, col=1)
    fig.update_xaxes(title="number of lines", range=[0, N + 4], row=1, col=2)
    fig.update_yaxes(range=[0, 1.2], row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=560, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), margin=dict(l=70, r=20, t=100, b=70))
    fig.update_annotations(font_size=22)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".crowd_frames"
    tmp.mkdir(exist_ok=True)
    for n in range(1, N + 1):
        frame(n).write_image(tmp / f"{n - 1:03d}.png")
    for k in range(N, N + 8):
        shutil.copy(tmp / f"{N - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=9,scale=880:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "crowd_of_lines.gif")], check=True)
    keys = [Image.open(tmp / f"{n - 1:03d}.png").convert("RGB") for n in (1, 4, 10, N)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "crowd_of_lines_frames.png")
    shutil.rmtree(tmp)
