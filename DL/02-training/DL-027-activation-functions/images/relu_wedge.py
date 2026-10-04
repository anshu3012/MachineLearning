"""How two ReLU nodes build a shape that fits data (section 8.1). A 1-2-1 network with ReLU in the hidden layer and
before the output, on a drug-dosage example: dosage 0 and 1 do not work (0), dosage 0.5 works (1). The numbers are
those of StatQuest, "Neural Networks Pt. 3: ReLU In Action!!!": node 1 computes ReLU(1.70 x - 0.85) and is multiplied
by -40.8; node 2's output times 2.70 is the straight line 34.0 x; the two are added, the bias -16 is added, and a
final ReLU clips the negatives. One operation per frame. Plotly frames -> ffmpeg GIF + a grid of the frames (PDF)."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

from common import BLUE, GREEN, GREY, ORANGE

HERE = Path(__file__).parent
x = np.linspace(0, 1, 401)
relu = lambda z: np.maximum(0, z)
bent = relu(1.70 * x - 0.85)          # node 1 after ReLU
blue = -40.8 * bent                   # ... times its output weight
orange = 34.0 * x                     # node 2 after ReLU, times its output weight 2.70
wedge = blue + orange
shifted = wedge - 16
final = relu(shifted)
assert abs(shifted[0] + 16) < 1e-9 and abs(np.interp(0.2, x, shifted) + 9.2) < 0.01   # the two values StatQuest reads
assert round(final.max(), 2) == 1.0 and round(x[final.argmax()], 2) == 0.5, (final.max(), x[final.argmax()])
assert final[0] == 0 and final[-1] == 0
DOSE, EFFECT = [0, 0.5, 1], [0, 1, 0]
FAINT = "#C8C8C8"
# (title, curves drawn [(y, colour, width, name)], y-range)
STEPS = [
    ("1. Node 1: ReLU(1.70 × dosage − 0.85) is 0 up to dosage 0.5, then rises", [(bent, BLUE, 5, "node 1")], [-0.1, 1.2]),
    ("2. Multiply node 1 by −40.8: the bent line flips and stretches", [(blue, BLUE, 5, "node 1 × −40.8")], [-40, 40]),
    ("3. Node 2, times its weight: the straight line 34.0 × dosage",
     [(blue, BLUE, 3, "node 1 × −40.8"), (orange, ORANGE, 5, "node 2 × 2.70")], [-40, 40]),
    ("4. Add the two lines: a wedge with its corner at dosage 0.5",
     [(blue, FAINT, 2, "node 1 × −40.8"), (orange, FAINT, 2, "node 2 × 2.70"), (wedge, GREEN, 5, "sum")], [-40, 40]),
    ("5. Add the bias −16: the wedge moves down; only its tip is above 0",
     [(wedge, FAINT, 2, "sum"), (shifted, GREEN, 5, "sum − 16")], [-40, 40]),
    ("6. Final ReLU: negatives become 0. The peak fits the three points",
     [(final, GREEN, 5, "network output")], [-0.1, 1.2]),
]


def frame(k):
    title, curves, yr = STEPS[k]
    fig = go.Figure()
    fig.add_hline(y=0, line=dict(color=GREY, width=1))
    for y, c, w, name in curves:
        fig.add_scatter(x=x, y=y, mode="lines", name=name, line=dict(color=c, width=w))
    if k == len(STEPS) - 1:
        fig.add_scatter(x=DOSE, y=EFFECT, mode="markers", name="data", marker=dict(size=18, color="black"))
    fig.update_layout(template="simple_white", width=1000, height=600, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=title, x=0.5, font=dict(size=23)), xaxis=dict(title="dosage", range=[-0.03, 1.03]),
                      yaxis=dict(title="value", range=yr), legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.8)"),
                      margin=dict(l=80, r=20, t=70, b=70))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".wedge_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for k in range(len(STEPS)):
        keys.append(tmp / f"k{k}.png")
        frame(k).write_image(keys[-1])
    seq = [k for k in range(len(STEPS)) for _ in range(3)] + [len(STEPS) - 1] * 4
    for j, k in enumerate(seq):
        shutil.copy(keys[k], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=800:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "relu_wedge.gif")], check=True)
    ims = [Image.open(p).convert("RGB") for p in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 3 * h + 32), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "relu_wedge_frames.png")
    shutil.rmtree(tmp)
    print("peak", final.max().round(3), "at", x[final.argmax()], "non-zero from", x[final > 0][[0, -1]].round(3))
