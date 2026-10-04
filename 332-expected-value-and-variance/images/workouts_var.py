"""Section 4.1: variance term by term. X = workouts in a week, values 0..4 with P = 0.1, 0.15, 0.4, 0.25, 0.1,
mean 2.1. One bar at a time, the distance to the mean is drawn and its term (x - 2.1)^2 P(x) is added to a running
total: 0.441 + 0.1815 + 0.004 + 0.2025 + 0.361 = 1.19. Last, the standard deviation 1.09 is marked either side of the
mean (1.01 to 3.19) to check that it looks like a fair measure of spread.
Run: python workouts_var.py  -> workouts_var.gif, workouts_var_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, RED, GREY, PURPLE = "#4C78A8", "#E45756", "#6B6B6B", "#B279A2"
X = np.arange(5)
P = np.array([0.1, 0.15, 0.4, 0.25, 0.1])
MU = (X * P).sum()
TERMS = (X - MU) ** 2 * P
VAR, SD = TERMS.sum(), np.sqrt(TERMS.sum())
assert round(MU, 2) == 2.1 and round(VAR, 2) == 1.19 and round(SD, 2) == 1.09


def frame(k, show_sd=False):
    """k = number of terms added so far (0..5)."""
    colours = [PURPLE if i < k else BLUE for i in X]
    fig = go.Figure(go.Bar(x=X, y=P, marker_color=colours, width=0.6, text=[f"{p:g}" for p in P],
                           textposition="outside"))
    fig.add_vline(x=MU, line=dict(color="black", width=3, dash="dash"), opacity=1)
    fig.add_annotation(x=MU, y=0.66, text="mean 2.1", showarrow=False, xshift=6, xanchor="left")
    if 0 < k <= 5 and not show_sd:
        i = k - 1
        fig.add_annotation(x=X[i], y=P[i] / 2, ax=MU, ay=P[i] / 2, xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=2, arrowwidth=3, arrowcolor=RED, text="")
    lines = ["Var = Σ (x − 2.1)² P(x)", ""]
    for i in range(k):
        style = f"color:{RED}" if (i == k - 1 and not show_sd) else ""
        lines.append(f"<span style='{style}'>x = {X[i]}: ({X[i]} − 2.1)² × {P[i]:g} = {TERMS[i]:.4f}</span>")
    if k == 5:
        lines += ["", f"total: Var = <b>{VAR:.2f}</b>"]
    if show_sd:
        lines += [f"SD = √1.19 = <b>{SD:.2f}</b>"]
        fig.add_annotation(x=MU + SD, y=0.5, ax=MU - SD, ay=0.5, xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=2, arrowside="end+start", arrowwidth=3, arrowcolor=RED, text="")
        fig.add_annotation(x=MU, y=0.5, text=f"{MU - SD:.2f} to {MU + SD:.2f}", showarrow=False, yshift=18,
                           font=dict(color=RED, size=22))
    fig.add_annotation(x=0.64, y=0.95, xref="paper", yref="paper", xanchor="left", yanchor="top", showarrow=False,
                       align="left", text="<br>".join(lines), font=dict(size=22))
    fig.update_layout(template="simple_white", width=1150, height=560, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text="Workouts in a week: the spread around 2.1", x=0.5, y=0.96),
                      xaxis=dict(title="workouts in a week, x", dtick=1, range=[-0.6, 4.6], domain=[0, 0.6]),
                      yaxis=dict(title="P(x)", range=[0, 0.72], dtick=0.1), margin=dict(l=70, r=20, t=70, b=70))
    return fig


PLAN = [(0, False, 5)] + [(k, False, 6) for k in range(1, 6)] + [(5, True, 14)]

if __name__ == "__main__":
    tmp = HERE / ".workout_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, []
    for i, (k, sd, hold) in enumerate(PLAN):
        frame(k, sd).write_image(tmp / f"{n:03d}.png")
        if i in (1, 3, 5, 6):
            keys.append(n)
        for _ in range(hold - 1):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + 1:03d}.png")
            n += 1
        n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "workouts_var.gif")], check=True)
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "workouts_var_frames.png")
    shutil.rmtree(tmp)
