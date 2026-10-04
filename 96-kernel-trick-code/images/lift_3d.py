"""Section 4: the circles data lifted by z = exp(-x1^2) + exp(-x2^2). The points rise from the flat plane to
their height, then the plane z = 1.75 appears between the classes.
Run: python lift_3d.py  -> lift_3d.gif, lift_3d_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import COLOURS, make_data  # noqa: E402

X, y = make_data("circles")
z = np.exp(-X ** 2).sum(axis=1)
inner, ring = z[y == 1], z[y == 0]
# the Note's numbers: centre 1.89-2.00, ring 1.01-1.56, plane at 1.75 separates them
assert (round(inner.min(), 2), round(inner.max(), 2)) == (1.89, 2.00), (inner.min(), inner.max())
assert (round(ring.min(), 2), round(ring.max(), 2)) == (1.01, 1.56), (ring.min(), ring.max())
assert inner.min() > 1.75 > ring.max()
RISE = 14                                                     # frames for the rise


def frame(k):
    t = min(k / RISE, 1.0)
    fig = go.Figure()
    for cls, name in ((0, "ring (class 0)"), (1, "centre (class 1)")):
        m = y == cls
        fig.add_trace(go.Scatter3d(x=X[m, 0], y=X[m, 1], z=t * z[m], mode="markers", name=name,
                                   marker=dict(size=5, color=COLOURS[cls])))
    if k > RISE:
        g = np.linspace(-1.3, 1.3, 2)
        fig.add_trace(go.Surface(x=g, y=g, z=np.full((2, 2), 1.75), showscale=False, opacity=0.45,
                                 colorscale=[[0, "#54A24B"], [1, "#54A24B"]], name="plane z = 1.75"))
    title = ("flat: no line separates the classes" if k == 0 else
             "the plane z = 1.75 separates them" if k > RISE else f"lifting: height × {t:.2f}")
    ang = 1.7 + 0.5 * t
    fig.update_layout(template="simple_white", width=900, height=720, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=title, x=0.5, y=0.95), margin=dict(l=0, r=0, t=70, b=0),
                      legend=dict(x=0.02, y=0.9),
                      scene=dict(xaxis=dict(title="x₁", range=[-1.3, 1.3], tickfont_size=14, dtick=1), yaxis=dict(title="x₂", range=[-1.3, 1.3], tickfont_size=14, dtick=1),
                                 zaxis=dict(title="z", range=[0, 2.1], tickfont_size=14, dtick=0.5), aspectmode="manual",
                                 aspectratio=dict(x=1, y=1, z=0.8),
                                 camera=dict(eye=dict(x=1.9 * np.cos(ang), y=1.9 * np.sin(ang),
                                                      z=0.6 + 1.4 * (1 - t)))))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".lift_frames"
    tmp.mkdir(exist_ok=True)
    last = RISE + 1
    for k in range(last + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(last + 1, last + 8):                       # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=8,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "lift_3d.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, RISE // 2, RISE, last)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "lift_3d_frames.png")
    shutil.rmtree(tmp)
