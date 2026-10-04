"""Mode imputation, gap by gap: the 547 FireplaceQu gaps of the training set are filled with the mode Gd in steps.
Left: category shares among the rows that have a value. Right: Gd's share as the number of filled gaps grows.
The more gaps get the mode, the more the mode grows and every other category shrinks.
Plotly frames -> ffmpeg GIF + _frames.png grid. Run: python mode_fill.py -> mode_fill.gif, mode_fill_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=22)
ORDER = ["Gd", "TA", "Fa", "Ex", "Po"]

df = pd.read_csv(HERE.parent / "data" / "house_prices.csv")
X_train, *_ = train_test_split(df[["GarageQual", "FireplaceQu"]], df["SalePrice"], test_size=0.2, random_state=42)
known = X_train["FireplaceQu"].value_counts().reindex(ORDER)
gaps = int(X_train["FireplaceQu"].isnull().sum())
mode = known.idxmax()
assert mode == "Gd" and gaps == 547 and known["Gd"] == 305 and len(X_train) == 1168


def shares(k):                                                # k gaps filled with the mode
    c = known.copy()
    c[mode] += k
    return c / c.sum() * 100


ks = np.arange(0, gaps + 1)
gd_curve = np.array([shares(k)[mode] for k in ks])
assert round(gd_curve[0], 1) == 49.1 and round(gd_curve[-1], 1) == 72.9
assert round(shares(gaps)["TA"], 1) == 21.6
STEPS = [0, 50, 100, 150, 200, 300, 400, 547]


def frame(k):
    fig = make_subplots(1, 2, column_widths=[0.5, 0.5], horizontal_spacing=0.12,
                        subplot_titles=["FireplaceQu: share of each category", "Gd's share as gaps are filled"])
    s = shares(k)
    fig.add_trace(go.Bar(x=ORDER, y=shares(0), marker_color="rgba(0,0,0,0)", marker_line=dict(color=GREY, width=2),
                         width=0.8, name="before"), 1, 1)
    fig.add_trace(go.Bar(x=ORDER, y=s, marker_color=[GREEN if c == mode else BLUE for c in ORDER], width=0.55,
                         text=[f"{v:.1f}" for v in s], textposition="outside", textfont=dict(size=22)), 1, 1)
    fig.add_trace(go.Scatter(x=ks[:k + 1], y=gd_curve[:k + 1], mode="lines", line=dict(color=GREEN, width=4)), 1, 2)
    fig.add_trace(go.Scatter(x=[k], y=[gd_curve[k]], mode="markers+text", marker=dict(color=GREEN, size=14),
                             text=[f"{gd_curve[k]:.1f}%"], textposition="top left", textfont=dict(size=24)), 1, 2)
    fig.update_layout(barmode="overlay")
    fig.update_yaxes(title="share of rows (%)", range=[0, 85], row=1, col=1)
    fig.update_yaxes(title="Gd share (%)", range=[45, 80], row=1, col=2)
    fig.update_xaxes(title="category (grey outline: before)", row=1, col=1)
    fig.update_xaxes(title="gaps filled with Gd", range=[0, 560], row=1, col=2)
    fig.update_annotations(font_size=23)
    fig.update_layout(template="simple_white", width=1200, height=560, font=FONT, showlegend=False,
                      title=dict(text=f"{k} of {gaps} gaps filled with the mode, Gd", x=0.5, y=0.97),
                      margin=dict(l=80, r=30, t=110, b=70))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".mode_frames"
    tmp.mkdir(exist_ok=True)
    for i, k in enumerate(STEPS):
        frame(k).write_image(tmp / f"{i:03d}.png")
    last = len(STEPS) - 1
    for i in range(last + 1, last + 6):                       # hold the final frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "mode_fill.gif")], check=True)
    keys = [Image.open(tmp / f"{i:03d}.png").convert("RGB") for i in (0, 2, 5, last)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "mode_fill_frames.png")
    shutil.rmtree(tmp)
