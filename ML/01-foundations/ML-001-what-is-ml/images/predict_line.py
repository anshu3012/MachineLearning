"""A model making predictions: 200 students' CGPA and salary package (data/placement.csv, the dataset of Note ML-049).
Training fits a straight line to the dots; for a new student we go up from the CGPA to the line and across to the
predicted package. Idea after StatQuest, "A Gentle Introduction to Machine Learning" (yam eaten vs running speed).
Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=24)
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#8A8A8A"

d = pd.read_csv(HERE.parent / "data" / "placement.csv")
assert len(d) == 200
m, b = np.polyfit(d.cgpa, d.package, 1)                  # the model: package = m * cgpa + b
assert round(m, 2) == 0.57 and round(b, 2) == -0.99, (m, b)
pred = lambda x: m * x + b
assert round(pred(7.5), 2) == 3.29 and round(pred(8.5), 2) == 3.86 and round(pred(6.0), 2) == 2.43


def frame(stage, x=None):
    """stage 0: training data; 1: + fitted line (the model); 2: + prediction for a new student with CGPA x."""
    fig = go.Figure()
    fig.add_scatter(x=d.cgpa, y=d.package, mode="markers", marker=dict(size=10, color=BLUE, opacity=0.55),
                    showlegend=False)
    title = "<b>Training data:</b> 200 students, CGPA and package"
    if stage >= 1:
        xs = np.array([4.5, 10])
        fig.add_scatter(x=xs, y=pred(xs), mode="lines", line=dict(color="black", width=4), showlegend=False)
        title = f"<b>The model</b> found by training: package = {m:.2f} × CGPA − {-b:.2f}"
    if stage == 2:
        y = pred(x)
        fig.add_scatter(x=[x, x, 4.5], y=[0.8, y, y], mode="lines", line=dict(color=ORANGE, width=4, dash="dash"),
                        showlegend=False)
        fig.add_scatter(x=[x], y=[y], mode="markers", marker=dict(size=22, color=ORANGE,
                                                                   line=dict(color="black", width=2)), showlegend=False)
        title = f"New student, CGPA <b>{x:.1f}</b> → <b>prediction: {y:.2f} LPA</b>"
    fig.update_layout(template="simple_white", width=1000, height=720, font=FONT, title=dict(text=title, x=0.5, y=0.95),
                      xaxis=dict(title="CGPA (input: the feature)", range=[4.5, 10]),
                      yaxis=dict(title="package in LPA (output: the target)", range=[0.8, 5]),
                      margin=dict(l=90, r=30, t=90, b=90))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".pl_frames"
    tmp.mkdir(exist_ok=True)
    shots = [(0, None)] * 4 + [(1, None)] * 4
    for a, z in [(7.5, 8.5), (8.5, 6.0)]:
        shots += [(2, a)] * 4 + [(2, v) for v in np.linspace(a, z, 8)[1:-1]]
    shots += [(2, 6.0)] * 6
    cache = {}
    for j, s in enumerate(shots):
        if s not in cache:
            cache[s] = tmp / f"k{len(cache)}.png"
            frame(*s).write_image(cache[s])
        shutil.copy(cache[s], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "predict_line.gif")], check=True)
    ims = [Image.open(cache[s]).convert("RGB") for s in [(1, None), (2, 7.5)]]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, h), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "predict_line_frames.png")
    shutil.rmtree(tmp)
