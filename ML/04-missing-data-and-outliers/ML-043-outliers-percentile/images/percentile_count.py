"""A percentile found by counting, on 14 heights: every 700th person of the Note's data, rounded to whole inches.
Dot plot; the dots below 69 inches light up (7 of 14 = 50th percentile), then the dot at 69 joins (8 of 14 = 57th).
The two counting rules give two answers. Idea (count the dots below, then at or below, on a dot plot) after Khan
Academy, "Calculating percentile"; data and code are ours.
Plotly frames -> ffmpeg GIF + _frames.png grid. Run: python percentile_count.py"""
import shutil
import subprocess
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, RED, GREY = "#4C78A8", "#F58518", "#E45756", "#B0B0B0"
h = pd.read_csv(HERE.parent / "data" / "weight-height.csv")["Height"].iloc[::700][:14].round().astype(int).to_numpy()
h = np.sort(h)
V = 69
below, at_or_below = int((h < V).sum()), int((h <= V).sum())
assert list(h) == [63, 63, 63, 65, 67, 67, 67, 69, 70, 71, 73, 73, 74, 74]
assert (below, at_or_below, len(h)) == (7, 8, 14) and np.quantile(h, 0.5) == 68
seen = Counter()
ys = []
for v in h:                                                   # stack equal heights
    seen[v] += 1
    ys.append(seen[v])
ys = np.array(ys)
TITLES = ["1. the heights of 14 people, one dot each",
          f"2. at which percentile is the person who is {V} inches tall?",
          f"3. count the dots below {V}: {below} of 14 = 50% → 50th percentile",
          f"4. count the dots at or below {V}: {at_or_below} of 14 = 57% → 57th percentile"]


def frame(k):
    colour = [GREY] * len(h)
    for i, v in enumerate(h):
        if k >= 1 and v == V:
            colour[i] = RED
        if k >= 2 and v < V:
            colour[i] = BLUE
        if k == 3 and v == V:
            colour[i] = ORANGE
    fig = go.Figure(go.Scatter(x=h, y=ys, mode="markers",
                               marker=dict(color=colour, size=34, line=dict(color="white", width=2))))
    if k >= 1:
        fig.add_annotation(x=V, y=1.0, ay=-90, ax=0, text=f"{V} inches", font=dict(size=24, color=RED),
                           arrowcolor=RED, arrowwidth=2, standoff=22)
    if k >= 2:
        fig.add_annotation(x=65, y=4.4, text=f"{below} dots below", showarrow=False, font=dict(size=26, color=BLUE))
    if k == 3:
        fig.add_annotation(x=71.5, y=4.4, text="+ 1 dot at 69", showarrow=False, font=dict(size=26, color=ORANGE))
    fig.update_layout(template="simple_white", width=1000, height=520, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), title=dict(text=TITLES[k], x=0.02, y=0.95),
                      margin=dict(l=40, r=40, t=90, b=70))
    fig.update_xaxes(range=[61.5, 75.5], dtick=1, title="height (inches)")
    fig.update_yaxes(visible=False, range=[0.3, 5])
    return fig


if __name__ == "__main__":
    tmp = HERE / ".pct_frames"
    tmp.mkdir(exist_ok=True)
    n = 0
    for k in range(4):
        frame(k).write_image(tmp / f"k{k}.png")
        for _ in range(2 if k < 3 else 4):                    # 2 s per step, hold the last
            shutil.copy(tmp / f"k{k}.png", tmp / f"{n:03d}.png")
            n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "percentile_count.gif")], check=True)
    keys = [Image.open(tmp / f"k{k}.png").convert("RGB") for k in range(4)]
    w, hh = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * hh + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (hh + 16)))
    sheet.save(HERE / "percentile_count_frames.png")
    shutil.rmtree(tmp)
