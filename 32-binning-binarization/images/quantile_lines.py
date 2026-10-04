"""Quantiles as cutting lines, on 20 real ages: the first 20 distinct ages of the Titanic training set (distinct, so
that no cutting line falls on a tie). Step 1: the sorted ages as dots. Step 2: the median cuts them into 2 equal
groups. Step 3: the quartiles cut them into 4. Step 4: the 0.2, 0.4, 0.6, 0.8 quantiles cut them into 5 groups of 4:
those four lines are the edges of 5 equal frequency bins. Quantiles from np.quantile (linear interpolation).
Plotly frames -> ffmpeg GIF + _frames.png grid. Run: python quantile_lines.py -> quantile_lines.gif, quantile_lines_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
GREY, RED = "#6B6B6B", "#E45756"
PALETTE = ["#4C78A8", "#F58518", "#54A24B", "#B279A2", "#72B7B2"]
FONT = dict(family="Latin Modern Roman", size=24)

df = pd.read_csv(HERE.parent / "data" / "titanic_train.csv", usecols=["Age", "Fare", "Survived"]).dropna()
X_train, *_ = train_test_split(df[["Age", "Fare"]], df["Survived"], test_size=0.2, random_state=42)
ages = np.sort(pd.unique(X_train["Age"])[:20])
assert len(ages) == 20
STEPS = [("20 ages, sorted from youngest to oldest", []),
         ("The median: 10 ages below, 10 above. It is the 0.5 quantile.", [0.5]),
         ("Three lines, four groups of 5: the 0.25, 0.5 and 0.75 quantiles", [0.25, 0.5, 0.75]),
         ("Four lines, five groups of 4: the edges of 5 equal frequency bins", [0.2, 0.4, 0.6, 0.8])]
for _, ps in STEPS:                                             # every cut leaves equal groups
    cuts = np.quantile(ages, ps) if ps else np.array([])
    sizes = np.bincount(np.digitize(ages, cuts), minlength=len(ps) + 1)
    assert len(set(sizes)) == 1 and not np.isin(cuts, ages).any(), (ps, sizes)
print("quartiles", np.quantile(ages, [0.25, 0.5, 0.75]), "quintiles", np.quantile(ages, [0.2, 0.4, 0.6, 0.8]))


def frame(k):
    title, ps = STEPS[k]
    cuts = np.quantile(ages, ps) if ps else np.array([])
    group = np.digitize(ages, cuts)
    fig = go.Figure()
    colours = [PALETTE[g] for g in group] if ps else [PALETTE[0]] * 20
    fig.add_trace(go.Scatter(x=ages, y=[0] * 20, mode="markers", marker=dict(size=20, color=colours,
                                                                              line=dict(color="white", width=1))))
    for p, c in zip(ps, cuts):
        fig.add_shape(type="line", x0=c, x1=c, y0=-0.55, y1=0.55, line=dict(color=RED, width=4))
        fig.add_annotation(x=c, y=0.8, text=f"<b>{c:g}</b>", showarrow=False, font=dict(color=RED, size=24))
        fig.add_annotation(x=c, y=-0.8, text=f"Q({p:g})", showarrow=False, font=dict(color=RED, size=22))
    if ps:
        bounds = np.concatenate([[ages.min() - 1], cuts, [ages.max() + 1]])
        for g in range(len(ps) + 1):
            fig.add_annotation(x=(bounds[g] + bounds[g + 1]) / 2, y=-1.35, text=f"{(group == g).sum()} ages",
                               showarrow=False, font=dict(color=PALETTE[g], size=22))
    fig.update_xaxes(title="age (years)", range=[3, 52], tickvals=list(range(5, 51, 5)))
    fig.update_yaxes(range=[-1.7, 1.2], visible=False)
    fig.update_layout(template="simple_white", width=1200, height=480, font=FONT, showlegend=False,
                      title=dict(text=title, x=0.5, y=0.95), margin=dict(l=30, r=30, t=80, b=80))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".q_frames"
    tmp.mkdir(exist_ok=True)
    n = 0
    for k in range(4):
        frame(k).write_image(tmp / f"k{k}.png")
        for _ in range(3 if k < 3 else 6):                      # hold each step; hold the last longer
            shutil.copy(tmp / f"k{k}.png", tmp / f"{n:03d}.png")
            n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "quantile_lines.gif")], check=True)
    keys = [Image.open(tmp / f"k{k}.png").convert("RGB") for k in (1, 2, 3)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (w, 3 * h + 32), "white")
    for j, im in enumerate(keys):
        sheet.paste(im, (0, j * (h + 16)))
    sheet.save(HERE / "quantile_lines_frames.png")
    shutil.rmtree(tmp)
