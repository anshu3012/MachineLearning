"""The 68-95-99.7 rule read off the Note's own data: the CGPA histogram of the 1,000 students with a bell curve; the
bands mean +- 1, 2, 3 standard deviations shade in turn, each with the count of students inside it next to the rule's
share; last, the two tails and the 5 outliers in red. Idea (shade band by band, then read the two tails) after Khan
Academy, "ck12.org normal distribution problems: Empirical rule"; data and code are ours.
Plotly frames -> ffmpeg GIF + _frames.png grid. Run: python rule_bands.py"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from scipy.stats import norm

HERE = Path(__file__).parent
BLUE, RED, GREY, GREEN = "#4C78A8", "#E45756", "#6B6B6B", "#54A24B"
BAND = ["rgba(76,120,168,0.45)", "rgba(76,120,168,0.28)", "rgba(76,120,168,0.14)"]
x = pd.read_csv(HERE.parent / "data" / "placement.csv")["cgpa"].to_numpy()
mean, std = x.mean(), x.std(ddof=1)
inside = [int(((x >= mean - k * std) & (x <= mean + k * std)).sum()) for k in (1, 2, 3)]
low, high = int((x < mean - 3 * std).sum()), int((x > mean + 3 * std).sum())
assert inside == [679, 957, 995] and (low, high) == (3, 2)
assert (int((x < mean - std).sum()), int((x > mean + std).sum())) == (163, 158)   # the one-std tails of Section 3.1
RULE = ["68%", "95%", "99.7%"]
BIN = 0.1
grid = np.linspace(4.4, 9.6, 400)
TITLES = ["The CGPA of 1,000 students: mean 6.96, std 0.62",
          f"within 1 std: {inside[0]} students = {inside[0] / 10:.1f}%  (rule: 68%)",
          f"within 2 std: {inside[1]} students = {inside[1] / 10:.1f}%  (rule: 95%)",
          f"within 3 std: {inside[2]} students = {inside[2] / 10:.1f}%  (rule: 99.7%)",
          f"left over: {low} below 5.11 and {high} above 8.81 = 0.5%: the outliers"]


def frame(k):
    fig = go.Figure()
    for j in range(min(k, 3) - 1, -1, -1):                   # widest band first, so the inner ones sit on top
        fig.add_vrect(x0=mean - (j + 1) * std, x1=mean + (j + 1) * std, fillcolor=BAND[j], line_width=0, layer="below")
    fig.add_trace(go.Histogram(x=x, xbins=dict(start=4.4, end=9.6, size=BIN), marker_color=GREY, opacity=0.55))
    fig.add_trace(go.Scatter(x=grid, y=norm.pdf(grid, mean, std) * len(x) * BIN, mode="lines",
                             line=dict(color="black", width=3)))
    for j in range(min(k, 3)):
        for s in (-1, 1):
            v = mean + s * (j + 1) * std
            fig.add_vline(x=v, line=dict(color=BLUE, width=2, dash="dash"))
            fig.add_annotation(x=v, y=74, text=f"{v:.2f}", showarrow=False, font=dict(size=19, color=BLUE),
                               textangle=-90, xshift=-12 if s < 0 else 12)
    if k == 4:
        out = x[(x < mean - 3 * std) | (x > mean + 3 * std)]
        fig.add_trace(go.Scatter(x=out, y=np.full(len(out), 3), mode="markers",
                                 marker=dict(color=RED, size=16, line=dict(color="white", width=1))))
        for xa, n in ((4.75, low), (9.15, high)):
            fig.add_annotation(x=xa, y=14, text=f"{n} students", showarrow=False, font=dict(size=22, color=RED))
    fig.update_layout(template="simple_white", width=1000, height=560, showlegend=False, bargap=0.05,
                      font=dict(family="Latin Modern Roman", size=22), title=dict(text=TITLES[k], x=0.5),
                      margin=dict(l=80, r=20, t=70, b=70))
    fig.update_xaxes(title="CGPA", range=[4.4, 9.6], dtick=0.5)
    fig.update_yaxes(title="students", range=[0, 82])
    return fig


if __name__ == "__main__":
    tmp = HERE / ".band_frames"
    tmp.mkdir(exist_ok=True)
    n = 0
    for k in range(5):
        frame(k).write_image(tmp / f"k{k}.png")
        for _ in range(2 if k < 4 else 4):                    # 2 s per stage, hold the last
            shutil.copy(tmp / f"k{k}.png", tmp / f"{n:03d}.png")
            n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "rule_bands.gif")], check=True)
    keys = [Image.open(tmp / f"k{k}.png").convert("RGB") for k in (1, 2, 3, 4)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "rule_bands_frames.png")
    shutil.rmtree(tmp)
