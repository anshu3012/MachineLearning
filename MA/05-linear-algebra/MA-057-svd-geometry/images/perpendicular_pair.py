"""Section 2.2: turn a perpendicular pair of unit vectors and watch the angle between their images under
A = [[3, 0], [4, 5]]. Only at 45 degrees (and 135) do the images stay perpendicular: the singular vectors.
Plotly frames -> ffmpeg GIF, plus a key-frame grid for the PDF.  Run: python perpendicular_pair.py"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"
A = np.array([[3.0, 0.0], [4.0, 5.0]])
ANGLES = list(range(0, 91, 5))                                # the pair repeats every 90 degrees


def pair(deg):
    a = np.radians(deg)
    return np.array([np.cos(a), np.sin(a)]), np.array([-np.sin(a), np.cos(a)])


def out_angle(deg):
    x, y = pair(deg)
    ax, ay = A @ x, A @ y
    return np.degrees(np.arccos(ax @ ay / np.linalg.norm(ax) / np.linalg.norm(ay)))


x0, y0 = pair(0)
assert (A @ x0) @ (A @ y0) == 20                              # i-hat, j-hat: dot product 20, not perpendicular
x45, y45 = pair(45)
assert abs((A @ x45) @ (A @ y45)) < 1e-12                     # 45 degrees: perpendicular outputs
assert np.allclose([np.linalg.norm(A @ x45), np.linalg.norm(A @ y45)], [np.sqrt(45), np.sqrt(5)])
assert all(abs(out_angle(d) - 90) > 1 for d in ANGLES if d != 45)   # the only perpendicular pair in the sweep
t = np.linspace(0, 2 * np.pi, 200)
circle = np.array([np.cos(t), np.sin(t)])
ellipse = A @ circle


def arrow(fig, v, color, col):
    fig.add_annotation(x=v[0], y=v[1], ax=0, ay=0, xref=f"x{col}", yref=f"y{col}", axref=f"x{col}", ayref=f"y{col}",
                       showarrow=True, arrowhead=2, arrowwidth=4, arrowcolor=color, text="")


def frame(deg):
    x, y = pair(deg)
    ang = out_angle(deg)
    fig = make_subplots(1, 2, column_widths=[0.35, 0.65], horizontal_spacing=0.08,
                        subplot_titles=("input: perpendicular pair", "output under A"))
    fig.add_trace(go.Scatter(x=circle[0], y=circle[1], mode="lines", line=dict(color=GREY, width=2)), 1, 1)
    fig.add_trace(go.Scatter(x=ellipse[0], y=ellipse[1], mode="lines", line=dict(color=GREY, width=2)), 1, 2)
    for v, c in ((x, BLUE), (y, ORANGE)):
        arrow(fig, v, c, 1)
        arrow(fig, A @ v, c, 2)
    hit = abs(ang - 90) < 1e-6
    fig.update_layout(template="simple_white", width=1000, height=560, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), margin=dict(l=50, r=20, t=110, b=40),
                      title=dict(text=f"pair turned {deg}°: outputs meet at {ang:.0f}°" + ("  ← perpendicular" if hit else ""),
                                 x=0.5, y=0.96, font=dict(color="#E45756" if hit else "black")))
    fig.update_annotations(font_size=22)
    fig.update_xaxes(range=[-1.3, 1.3], row=1, col=1)
    fig.update_yaxes(range=[-1.3, 1.3], scaleanchor="x", row=1, col=1)
    fig.update_xaxes(range=[-7, 7], row=1, col=2)
    fig.update_yaxes(range=[-7, 7], scaleanchor="x2", row=1, col=2)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".pair_frames"
    tmp.mkdir(exist_ok=True)
    seq = ANGLES[:ANGLES.index(45) + 1] + [45] * 6 + ANGLES[ANGLES.index(45) + 1:]   # pause at the answer
    for k, d in enumerate(seq):
        frame(d).write_image(tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "perpendicular_pair.gif")], check=True)
    keys = [Image.open(tmp / f"{seq.index(d):03d}.png").convert("RGB") for d in (0, 20, 45, 70)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "perpendicular_pair_frames.png")
    shutil.rmtree(tmp)
