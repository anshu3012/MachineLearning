"""The first iris flower's first three features, [5.1, 3.5, 1.4], reached the way a vector is read: walk 5.1 along x,
then 3.5 along y, then 1.4 along z. Three components, so a point in 3D.
Run: python vector_walk.py  -> vector_walk.gif, vector_walk_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from sklearn.datasets import load_iris

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
v = load_iris().data[0]
assert np.allclose(v, [5.1, 3.5, 1.4, 0.2])            # the Note's first flower
v = v[:3]
NAMES, COLS = ["sepal length", "sepal width", "petal length"], [ORANGE, GREEN, BLUE]
AX = dict(tickfont=dict(size=15), title_font=dict(size=17))
STEPS = 6                                                # frames per axis walk


def frame(axis, t):
    """axis = 0, 1, 2 walking; 3 = arrow drawn. t in [0, 1] = how far along the current axis."""
    p = np.zeros(3)
    pts = [p.copy()]
    for a in range(3):
        if a < axis:
            p[a] = v[a]
        elif a == axis:
            p[a] = t * v[a]
        pts.append(p.copy())
    fig = go.Figure()
    for a in range(3):
        if a <= axis:
            seg = np.array(pts[a:a + 2])
            fig.add_trace(go.Scatter3d(x=seg[:, 0], y=seg[:, 1], z=seg[:, 2], mode="lines", showlegend=False,
                                       line=dict(color=COLS[a], width=9, dash="dash" if axis == 3 else "solid")))
    fig.add_trace(go.Scatter3d(x=[p[0]], y=[p[1]], z=[p[2]], mode="markers", showlegend=False,
                               marker=dict(size=7, color=RED)))
    if axis == 3:
        fig.add_trace(go.Scatter3d(x=[0, v[0]], y=[0, v[1]], z=[0, v[2]], mode="lines", showlegend=False,
                                   line=dict(color=RED, width=10)))
    shown = [f"{v[a]:.1f}" if a < axis else (f"{p[a]:.1f}" if a == axis else "_") for a in range(3)]
    sub = {0: "walk along x: sepal length", 1: "then along y: sepal width", 2: "then along z: petal length",
           3: "3 components, so the vector lives in 3D"}[axis]
    fig.update_layout(template="simple_white", width=820, height=640, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"<b>[{', '.join(shown)}]</b><br><span style='font-size:20px'>{sub}</span>",
                                 x=0.5, y=0.95),
                      scene=dict(xaxis=dict(title="x: sepal length", range=[0, 6], dtick=2, **AX),
                                 yaxis=dict(title="y: sepal width", range=[0, 4], dtick=2, **AX),
                                 zaxis=dict(title="z: petal length", range=[0, 2], dtick=1, **AX),
                                 camera=dict(eye=dict(x=1.5, y=-1.7, z=1.0), center=dict(x=0, y=0, z=-0.15)),
                                 aspectmode="manual", aspectratio=dict(x=1.4, y=1, z=0.75)),
                      margin=dict(l=0, r=0, t=110, b=0))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".walk_frames"
    tmp.mkdir(exist_ok=True)
    seq = [(a, s / STEPS) for a in range(3) for s in range(1, STEPS + 1)] + [(3, 1)] * 10
    for k, (a, t) in enumerate(seq):
        frame(a, t).write_image(tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "vector_walk.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (STEPS - 1, 2 * STEPS - 1, 3 * STEPS - 1, len(seq) - 1)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "vector_walk_frames.png")
    shutil.rmtree(tmp)
