"""A z-score in three rows: eight made-up ages (chosen so the mean is 30 and the standard deviation exactly 4).
Row 1: the ages in years. Row 2: subtract the mean (years from the mean). Row 3: divide by the standard deviation
(standard deviations from the mean = z-score). The dots never move: only the numbers under them change.
Plotly frames -> ffmpeg GIF + _frames.png grid. Run: python z_score_line.py -> z_score_line.gif, z_score_line_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=24)
AGES = np.array([24, 28, 28, 28, 30, 30, 34, 38])
MEAN, STD = AGES.mean(), AGES.std()
assert (MEAN, STD) == (30, 4)
ROWS = [("age (years)", lambda v: f"{v:g}", "black"),
        ("age - 30 (years from the mean)", lambda v: f"{v - MEAN:+g}".replace("+0", "0"), ORANGE),
        ("(age - 30) / 4 = z-score", lambda v: f"{(v - MEAN) / STD:+g}".replace("+0", "0"), GREEN)]
TITLES = ["Eight ages. Mean 30, standard deviation 4.",
          "Step 1: subtract the mean. The mean becomes 0.",
          "Step 2: divide by the standard deviation, 4.",
          "z-score = how many standard deviations from the mean"]
TICKS = [22, 26, 30, 34, 38]


def frame(k):                                                   # k rows of numbers shown (1..3); 4 = highlight
    fig = go.Figure()
    seen = {}
    xs, ys = [], []
    for a in AGES:                                              # stack equal ages
        seen[a] = seen.get(a, 0) + 1
        xs.append(a)
        ys.append(3.35 + 0.28 * (seen[a] - 1))
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="markers", marker=dict(color=BLUE, size=20)))
    fig.add_shape(type="line", x0=MEAN, x1=MEAN, y0=-0.3, y1=4.3, line=dict(color=RED, width=3, dash="dash"))
    fig.add_annotation(x=MEAN, y=4.5, text="<b>mean</b>", showarrow=False, font=dict(color=RED, size=24))
    for r, (label, fmt, colour) in enumerate(ROWS[:min(k, 3)]):
        y = 2.6 - r * 1.1
        fig.add_shape(type="line", x0=21, x1=39, y0=y + 0.3, y1=y + 0.3, line=dict(color=GREY, width=2))
        for t in TICKS:
            fig.add_shape(type="line", x0=t, x1=t, y0=y + 0.22, y1=y + 0.38, line=dict(color=GREY, width=2))
            bold = k == 4 and r == 2
            fig.add_annotation(x=t, y=y, text=f"<b>{fmt(t)}</b>" if bold else fmt(t), showarrow=False,
                               font=dict(size=26, color=colour))
        fig.add_annotation(x=20.4, y=y + 0.1, text=label, showarrow=False, xanchor="right", font=dict(size=22, color=colour))
    if k == 4:
        fig.add_annotation(x=38, y=3.35, ax=40, ay=-60, text="age 38: 2 standard<br>deviations above", showarrow=True,
                           arrowhead=2, font=dict(size=21, color=GREEN))
        fig.add_annotation(x=24, y=3.35, ax=-40, ay=-60, text="age 24: 1.5 standard<br>deviations below", showarrow=True,
                           arrowhead=2, font=dict(size=21, color=GREEN))
    fig.update_xaxes(range=[9.5, 45.5], visible=False)
    fig.update_yaxes(range=[-0.5, 5.0], visible=False)
    fig.update_layout(template="simple_white", width=1200, height=600, font=FONT, showlegend=False,
                      title=dict(text=TITLES[k - 1], x=0.5, y=0.96), margin=dict(l=20, r=20, t=70, b=10))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".z_frames"
    tmp.mkdir(exist_ok=True)
    n = 0
    for k in (1, 2, 3, 4):
        frame(k).write_image(tmp / f"k{k}.png")
        for _ in range(3 if k < 4 else 6):                      # hold each step; hold the last longer
            shutil.copy(tmp / f"k{k}.png", tmp / f"{n:03d}.png")
            n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "z_score_line.gif")], check=True)
    keys = [Image.open(tmp / f"k{k}.png").convert("RGB") for k in (2, 4)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (w, 2 * h + 16), "white")
    for j, im in enumerate(keys):
        sheet.paste(im, (0, j * (h + 16)))
    sheet.save(HERE / "z_score_line_frames.png")
    shutil.rmtree(tmp)
