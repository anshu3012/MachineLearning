"""Animation for Note 43, Section 3: building the IQR fences on the 1,000 placement exam marks.
Mark Q1 and Q3 (the middle half), measure the IQR, stretch 1.5 IQR out from each side, and colour what lies beyond.
Run: python fences_build.py -> fences_build.gif, fences_build_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, RED, GREY = "#4C78A8", "#F58518", "#E45756", "#6B6B6B"
x = pd.read_csv(HERE.parent / "data" / "placement.csv")["placement_exam_marks"].to_numpy()
q1, q3 = np.quantile(x, [0.25, 0.75])
iqr = q3 - q1
lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
out = (x < lo) | (x > hi)
assert (q1, q3, iqr, lo, hi, out.sum(), (x < lo).sum()) == (17, 44, 27, -23.5, 84.5, 15, 0)
assert ((x >= q1) & (x <= q3)).mean() > 0.5 - 0.03         # about half the students sit in the box
jit = np.random.default_rng(0).uniform(-1, 1, len(x))
N = 30


def frame(k):
    fig = go.Figure()
    grow = min(1, max(0, (k - 12) / 8))                     # arms stretch from 0 to 1.5 IQR over frames 12-20
    done = k >= 22
    for flag, c in ((~out | (not done), BLUE), (out & done, RED)):
        fig.add_trace(go.Scatter(x=x[flag], y=jit[flag], mode="markers",
                                 marker=dict(color=c, size=7 if c == BLUE else 12, opacity=0.35 if c == BLUE else 1)))
    title = "1. the exam marks of 1,000 students (long tail to the right)"
    if k >= 4:
        fig.add_vrect(x0=q1, x1=q3, fillcolor=BLUE, opacity=0.18, line_width=0)
        for v, t in ((q1, f"Q1 = {q1:g}"), (q3, f"Q3 = {q3:g}")):
            fig.add_vline(x=v, line=dict(color=BLUE, width=3))
            fig.add_annotation(x=v, y=1.2, text=t, showarrow=False, font=dict(color=BLUE), yanchor="bottom")
        title = "2. Q1 and Q3 hold the middle half of the students"
    if k >= 8:
        fig.add_annotation(x=q1, y=-1.25, ax=q3, ay=-1.25, axref="x", ayref="y", showarrow=True, arrowside="end+start",
                           arrowcolor=BLUE, arrowwidth=2, text="")
        fig.add_annotation(x=(q1 + q3) / 2, y=-1.3, text=f"IQR = {iqr:g}", showarrow=False, yanchor="top",
                           font=dict(color=BLUE))
        title = f"3. IQR = Q3 - Q1 = {q3:g} - {q1:g} = {iqr:g}"
    if k >= 12:
        arm = grow * 1.5 * iqr
        for a, b in ((q1, q1 - arm), (q3, q3 + arm)):
            fig.add_shape(type="line", x0=a, x1=b, y0=-1.25, y1=-1.25, line=dict(color=ORANGE, width=7), layer="above", opacity=1)
            fig.add_annotation(x=(a + b) / 2, y=-1.3, text="1.5 IQR", showarrow=False, yanchor="top",
                               font=dict(color=ORANGE))
        title = f"4. stretch 1.5 x IQR = {1.5 * iqr:g} out from each side"
    if k >= 21:
        for v, t, s in ((lo, f"lower fence {lo:g}", "left"), (hi, f"upper fence {hi:g}", "right")):
            fig.add_vline(x=v, line=dict(color=GREY, width=3, dash="dash"))
            fig.add_annotation(x=v, y=1.2, text=t, showarrow=False, yanchor="bottom", xanchor=s)
    if done:
        title = "5. beyond the fences: 15 outliers above 84.5, none below -23.5"
    fig.update_layout(template="simple_white", width=1000, height=540, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), title=dict(text=title, x=0.02, y=0.95),
                      margin=dict(l=40, r=40, t=90, b=70))
    fig.update_xaxes(range=[-35, 105], dtick=10, title="placement_exam_marks")
    fig.update_yaxes(visible=False, range=[-1.9, 1.7])
    return fig


if __name__ == "__main__":
    tmp = HERE / ".fences_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(N):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(N, N + 10):
        shutil.copy(tmp / f"{N - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "fences_build.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (5, 9, 16, N - 1)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "fences_build_frames.png")
    shutil.rmtree(tmp)
