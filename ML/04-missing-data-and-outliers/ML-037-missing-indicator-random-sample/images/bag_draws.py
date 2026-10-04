"""Random sample imputation as draws from a bag: the 148 missing training ages are filled one batch at a time with
ages drawn from the 564 known ones (seed 42, as in the Notebook). Bars: share of each age decade among the known
ages (grey outline) and among the draws so far (orange). The draws settle onto the known shape.
Plotly frames -> ffmpeg GIF + _frames.png grid. Run: python bag_draws.py -> bag_draws.gif, bag_draws_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
ORANGE, GREY, BLUE = "#F58518", "#6B6B6B", "#4C78A8"
FONT = dict(family="Latin Modern Roman", size=22)

df = pd.read_csv(HERE.parent / "data" / "titanic.csv", usecols=["Age", "Fare", "Survived"])
X_train, *_ = train_test_split(df[["Age", "Fare"]], df["Survived"], test_size=0.2, random_state=2)
pool = X_train["Age"].dropna()
n_gaps = int(X_train["Age"].isnull().sum())
draws = pool.sample(n_gaps, random_state=42).to_numpy()      # exactly the Notebook's fill values, in order
edges = np.arange(0, 90, 10)
labels = [f"{a}s" if a else "0-9" for a in edges[:-1]]
known = np.histogram(pool, edges)[0]
assert len(pool) == 564 and n_gaps == 148 and known[2] == 174   # 174 of 564 known ages in their twenties
known_share = known / known.sum() * 100
STEPS = [1, 3, 6, 10, 20, 40, 70, 110, 148]


def frame(n):
    got = np.histogram(draws[:n], edges)[0]
    share = got / n * 100
    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=known_share, marker_color="rgba(0,0,0,0)", marker_line=dict(color=GREY, width=3),
                         width=0.85, name="known ages (the bag): 564"))
    fig.add_trace(go.Bar(x=labels, y=share, marker_color=ORANGE, width=0.55, name=f"drawn so far: {n} of {n_gaps}",
                         text=[str(c) if c else "" for c in got], textposition="outside", textfont=dict(size=20)))
    if n <= 6:                                               # name the first draws, one by one
        fig.add_annotation(x=0.98, y=0.95, xref="paper", yref="paper", xanchor="right", showarrow=False,
                           text="draws: " + ", ".join(f"{a:g}" for a in draws[:n]), font=dict(size=24, color=ORANGE))
    fig.update_layout(barmode="overlay", template="simple_white", width=1000, height=560, font=FONT,
                      title=dict(text=f"{n} of {n_gaps} gaps filled from the bag", x=0.5),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2),
                      margin=dict(l=80, r=20, t=70, b=130))
    fig.update_xaxes(title="")
    fig.update_yaxes(title="share of ages (%)", range=[0, 60])
    return fig, got


if __name__ == "__main__":
    tmp = HERE / ".bag_frames"
    tmp.mkdir(exist_ok=True)
    for i, n in enumerate(STEPS):
        fig, got = frame(n)
        fig.write_image(tmp / f"{i:03d}.png")
    print("twenties among the 148 draws:", got[2], "known share", round(known_share[2], 1))
    last = len(STEPS) - 1
    for i in range(last + 1, last + 6):                       # hold the final frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "bag_draws.gif")], check=True)
    keys = [Image.open(tmp / f"{i:03d}.png").convert("RGB") for i in (1, 4, 6, last)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "bag_draws_frames.png")
    shutil.rmtree(tmp)
