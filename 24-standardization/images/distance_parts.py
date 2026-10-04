"""Why scaling matters for a distance: the squared Euclidean distance from the first training user (age 26, salary
15,000) to the next five training users, split into its age part and its salary part.
Raw data: the salary part is the whole distance. After standardization: both parts count, and the nearest user changes.
Data: Social Network Ads, the Note's own training set (random_state=0). Bars are drawn relative to the longest bar.
Plotly frames -> ffmpeg GIF + _frames.png grid. Run: python distance_parts.py -> distance_parts.gif, distance_parts_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=22)

df = pd.read_csv(HERE.parent / "data" / "Social_Network_Ads.csv").iloc[:, 2:]
X_train, *_ = train_test_split(df.drop(columns="Purchased"), df["Purchased"], test_size=0.3, random_state=0)
X_train = X_train.rename(columns={"EstimatedSalary": "Salary"})
me, others = X_train.iloc[0], X_train.iloc[1:6]
assert (me.Age, me.Salary) == (26, 15000)
std = X_train.std(ddof=0)                                       # what StandardScaler divides by
raw = (others - me) ** 2                                        # squared parts, raw units
zed = ((others - me) / std) ** 2                                # squared parts, in standard deviations
names = [f"age {int(r.Age)}, salary {int(r.Salary):,}" for r in others.itertuples()]
near_raw, near_z = int(raw.sum(axis=1).values.argmin()), int(zed.sum(axis=1).values.argmin())
print(others.assign(d_raw=np.sqrt(raw.sum(axis=1)).round(0), d_z=np.sqrt(zed.sum(axis=1)).round(2),
                    age_share_z=(zed.Age / zed.sum(axis=1)).round(2)))
assert (near_raw, near_z) == (3, 4) and raw.Age.max() / raw.sum(axis=1).min() < 1e-6
rel_raw, rel_z = raw / raw.sum(axis=1).max(), zed / zed.sum(axis=1).max()


def frame(t):                                                   # t = 0 raw ... 1 standardized
    rel = rel_raw * (1 - t) + rel_z * t
    fig = go.Figure()
    y = names[::-1]
    fig.add_trace(go.Bar(y=y, x=rel.Age.values[::-1], orientation="h", marker_color=BLUE, name="age part"))
    fig.add_trace(go.Bar(y=y, x=rel.Salary.values[::-1], orientation="h", marker_color=ORANGE, name="salary part"))
    if t in (0, 1):
        parts, near = (raw, near_raw) if t == 0 else (zed, near_z)
        for i, name in enumerate(names):
            a, s = parts.Age.iloc[i], parts.Salary.iloc[i]
            text = (f"age part {a:,.0f} + salary part {s:,.0f}" if t == 0 else f"age part {a:.2f} + salary part {s:.2f}")
            if i == near:
                text += "  <b>nearest</b>"
            fig.add_annotation(x=rel.sum(axis=1).iloc[i], y=name, text=text, showarrow=False, xanchor="left", xshift=8,
                               font=dict(size=20, color=GREEN if i == near else "black"))
    title = ("Raw data: the salary part is the whole distance" if t == 0 else
             "Standardized: age and salary both count" if t == 1 else "Standardizing ...")
    fig.update_xaxes(title="squared distance to the user aged 26 with salary 15,000 (longest bar = 1)",
                     range=[0, 1.75], tickvals=[0, 0.5, 1])
    fig.update_layout(template="simple_white", barmode="stack", width=1200, height=600, font=FONT,
                      title=dict(text=title, x=0.5, y=0.96), legend=dict(orientation="h", x=0.5, xanchor="center", y=1.16, traceorder="normal"),
                      margin=dict(l=250, r=20, t=130, b=80))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".dist_frames"
    tmp.mkdir(exist_ok=True)
    ts = [0] * 8 + list(np.linspace(0, 1, 9)[1:-1]) + [1] * 12  # hold raw, morph, hold standardized
    for j, t in enumerate(ts):
        frame(t).write_image(tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "distance_parts.gif")], check=True)
    keys = [Image.open(tmp / f"{j:03d}.png").convert("RGB") for j in (0, len(ts) - 1)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (w, 2 * h + 16), "white")
    for j, im in enumerate(keys):
        sheet.paste(im, (0, j * (h + 16)))
    sheet.save(HERE / "distance_parts_frames.png")
    shutil.rmtree(tmp)
