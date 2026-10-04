"""Superimpose, then smooth, one step per frame, with the two perceptrons of prob_maps.py (our own weights):
p1 = s(3x1 + 3x2), p2 = s(3x1 - 3x2). Frames: p1; p2; the plain sum p1 + p2 (0 to 2, not a probability);
the weighted sum 8 p1 + 8 p2 - 12; its sigmoid, with the curved 0.5 boundary.
Plotly frames (a map changing) -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
s = lambda z: 1 / (1 + np.exp(-z))
xs = np.linspace(-3, 3, 241)
X1, X2 = np.meshgrid(xs, xs)
P1, P2 = s(3 * (X1 + X2)), s(3 * (X1 - X2))
ZW = 8 * P1 + 8 * P2 - 12
CS = [[0, "#E45756"], [0.5, "#FFFFFF"], [1, "#54A24B"]]
# (title, values, colour range, level drawn in black, its label)
STEPS = [
    ("Perceptron 1: p₁ = σ(3x₁ + 3x₂)", P1, (0, 1), 0.5, "p₁ = 0.5"),
    ("Perceptron 2: p₂ = σ(3x₁ − 3x₂)", P2, (0, 1), 0.5, "p₂ = 0.5"),
    ("Superimpose: p₁ + p₂ runs from 0 to 2, so it is not a probability", P1 + P2, (0, 2), None, ""),
    ("Weights and bias: z = 8·p₁ + 8·p₂ − 12 is positive only where both are high", ZW, (-12, 12), 0, "z = 0"),
    ("Smooth: σ(z) is a probability again, and its 0.5 boundary is curved", s(ZW), (0, 1), 0.5, "0.5"),
]


def frame(k):
    title, Z, (lo, hi), level, lab = STEPS[k]
    fig = go.Figure()
    fig.add_contour(x=xs, y=xs, z=Z, colorscale=CS, zmin=lo, zmax=hi, opacity=0.75,
                    contours=dict(start=lo, end=hi, size=(hi - lo) / 10), line=dict(width=0.5, color="#999"),
                    colorbar=dict(thickness=18, len=0.8, tickfont=dict(size=18)))
    if level is not None:
        fig.add_contour(x=xs, y=xs, z=Z, showscale=False, contours_coloring="none",
                        contours=dict(start=level, end=level, size=1), line=dict(width=5, color="black"))
    fig.update_layout(template="simple_white", width=860, height=820, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"<b>Step {k + 1} of {len(STEPS)}.</b> {title}"
                                      + (f"<br>black line: {lab}" if lab else "<br> "), x=0.5, y=0.96,
                                 font=dict(size=20)),
                      xaxis=dict(title="x₁", range=[-3, 3]), yaxis=dict(title="x₂", range=[-3, 3], scaleanchor="x"),
                      margin=dict(l=70, r=20, t=110, b=70))
    return fig


if __name__ == "__main__":
    print("values at (1, 0):", round(float(s(3)), 3), round(float(2 * s(3)), 3), round(float(16 * s(3) - 12), 2))
    tmp = HERE / ".si_frames"
    tmp.mkdir(exist_ok=True)
    keys, n = [], 0
    for k in range(len(STEPS)):
        keys.append(tmp / f"k{k}.png")
        frame(k).write_image(keys[-1])
        for _ in range(3 if k < len(STEPS) - 1 else 6):
            shutil.copy(keys[-1], tmp / f"{n:03d}.png")
            n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=700:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse",
                    str(HERE / "superimpose.gif")], check=True)
    ims = [Image.open(keys[i]).convert("RGB") for i in (2, 3, 4)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (3 * w + 32, h), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "superimpose_frames.png")
    shutil.rmtree(tmp)
