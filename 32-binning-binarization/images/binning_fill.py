"""Discretization as a histogram that remembers: the 571 training ages drop one by one into 10-year bins.
Each passenger becomes a square in the column of its bin, coloured by its bin number, so the stack heights are
the histogram and every square still knows its bin. Plotly frames -> ffmpeg GIF + _frames.png grid.
Run: python binning_fill.py -> binning_fill.gif, binning_fill_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
GREY = "#6B6B6B"
PALETTE = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#72B7B2", "#9D755D", "#EECA3B"]
FONT = dict(family="Latin Modern Roman", size=24)
PER_ROW = 8                                                   # squares per row inside one bin column

df = pd.read_csv(HERE.parent / "data" / "titanic_train.csv", usecols=["Age", "Fare", "Survived"]).dropna()
X_train, *_ = train_test_split(df[["Age", "Fare"]], df["Survived"], test_size=0.2, random_state=42)
age = X_train["Age"].to_numpy()
edges = np.arange(0, 90, 10)                                  # 0, 10, ..., 80
bins = np.digitize(age, edges[1:-1])                          # bin number 0..7, left edge included
counts = np.bincount(bins, minlength=8)
assert len(age) == 571 and counts.sum() == 571
assert np.array_equal(counts, np.histogram(age, edges)[0])    # the stacks are exactly the histogram

# position of each passenger's square: its bin column, filled row by row in arrival order
slot = np.zeros(len(age), int)
seen = np.zeros(8, int)
for i, b in enumerate(bins):
    slot[i], seen[b] = seen[b], seen[b] + 1
sq_x = edges[bins] + 1.1 + (slot % PER_ROW) * 1.1
sq_y = slot // PER_ROW + 1
TOP = int(np.ceil(counts.max() / PER_ROW)) + 6
STRIP = -3.5                                                  # where the not-yet-binned ages wait
STEPS = [0, 5, 20, 60, 120, 200, 300, 420, 571]
EXAMPLE = 3                                                   # one passenger we follow
ex_age, ex_bin = age[EXAMPLE], bins[EXAMPLE]


def frame(n):
    fig = go.Figure()
    for e in edges:
        fig.add_vline(x=e, line=dict(color="#BBBBBB", width=1.5))
    wait = np.arange(len(age)) >= n
    fig.add_trace(go.Scatter(x=age[wait], y=np.full(wait.sum(), STRIP), mode="markers",
                             marker=dict(symbol="line-ns-open", size=16, color=GREY, line_width=2)))
    done = ~wait
    fig.add_trace(go.Scatter(x=sq_x[done], y=sq_y[done], mode="markers",
                             marker=dict(symbol="square", size=9, color=[PALETTE[b] for b in bins[done]])))
    for b in range(8):
        c = int(np.sum(bins[done] == b))
        if c:
            fig.add_annotation(x=edges[b] + 5, y=np.ceil(c / PER_ROW) + 1.2, text=str(c), showarrow=False,
                               font=dict(size=22, color=PALETTE[b]), yanchor="bottom")
    if n > EXAMPLE:                                           # follow one passenger to its square
        fig.add_annotation(x=sq_x[EXAMPLE], y=sq_y[EXAMPLE], ax=62, ay=TOP - 7, axref="x", ayref="y", arrowhead=2, arrowwidth=2, xanchor="left",
                           text=f"age {ex_age:g} → bin {ex_bin}", font=dict(size=24))
    fig.update_xaxes(range=[-1, 81], tickvals=edges, title="Age (years): bins 0 to 7, each 10 years wide")
    fig.update_yaxes(range=[STRIP - 2, TOP], tickvals=[STRIP], ticktext=["waiting"], title="", showgrid=False)
    fig.update_layout(template="simple_white", width=1000, height=640, font=FONT, showlegend=False,
                      title=dict(text=f"{n} of 571 passengers placed in their bin", x=0.5),
                      margin=dict(l=110, r=20, t=70, b=80))
    for b in range(8):
        fig.add_annotation(x=edges[b] + 5, y=TOP - 0.5, text=f"bin {b}", showarrow=False,
                           font=dict(size=20, color=PALETTE[b]))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".binning_frames"
    tmp.mkdir(exist_ok=True)
    for k, n in enumerate(STEPS):
        frame(n).write_image(tmp / f"{k:03d}.png")
    last = len(STEPS) - 1
    for k in range(last + 1, last + 6):                       # hold the final frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "binning_fill.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (1, 3, 5, last)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "binning_fill_frames.png")
    shutil.rmtree(tmp)
    print("counts per bin:", counts.tolist(), "example:", ex_age, "-> bin", ex_bin)
