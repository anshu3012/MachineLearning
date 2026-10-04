"""The Jacobian determinant of polar coordinates is det J = r: the same input cell (sides 0.4 by 0.2) slides outward
in r and its image under f(r, theta) = (r cos theta, r sin theta) grows in proportion to r.
Plotly frames -> ffmpeg GIF, plus a key-frame grid for the PDF.  Run: python area_scaling.py"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
ORANGE, GREY = "#F58518", "#BBBBBB"
P = lambda r, t: (r * np.cos(t), r * np.sin(t))
DR, DT, T0 = 0.4, 0.2, np.pi / 6
STARTS = np.round(np.arange(0.2, 2.61, 0.3), 2)               # left edge of the cell in r


def area_out(r0):                                             # exact: integral of r dr dtheta over the cell
    return DT * ((r0 + DR) ** 2 - r0 ** 2) / 2


s = np.linspace(0, 1, 60)
for r0 in STARTS:
    x, y = P(np.r_[r0 + DR * s, np.full(60, r0 + DR), r0 + DR * s[::-1], np.full(60, r0)],
             np.r_[np.full(60, T0), T0 + DT * s, np.full(60, T0 + DT), T0 + DT * s[::-1]])
    shoelace = 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
    assert abs(shoelace - area_out(r0)) < 2e-4                # the drawn outline has the stated area
    assert abs(area_out(r0) - DR * DT * (r0 + DR / 2)) < 1e-12  # = input area x r at the cell's middle
assert abs(area_out(2.0) - 0.176) < 1e-12                     # the Note's Section 5 example


def frame(r0):
    fig = make_subplots(1, 2, horizontal_spacing=0.12, subplot_titles=("input cell: area 0.08", "output cell"))
    for r in np.arange(0.2, 3.01, 0.4):
        fig.add_trace(go.Scatter(x=[r, r], y=[0, 1.2], mode="lines", line=dict(color=GREY, width=1)), 1, 1)
        x, y = P(r, np.linspace(0, 1.2, 60))
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=GREY, width=1)), 1, 2)
    for t in np.arange(0, 1.21, 0.2):
        fig.add_trace(go.Scatter(x=[0, 3], y=[t, t], mode="lines", line=dict(color=GREY, width=1)), 1, 1)
        x, y = P(np.array([0, 3]), t)
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(color=GREY, width=1)), 1, 2)
    cr = np.r_[r0 + DR * s, np.full(60, r0 + DR), r0 + DR * s[::-1], np.full(60, r0)]
    ct = np.r_[np.full(60, T0), T0 + DT * s, np.full(60, T0 + DT), T0 + DT * s[::-1]]
    style = dict(fill="toself", mode="lines", line=dict(color=ORANGE, width=3), fillcolor="rgba(245,133,24,0.45)")
    fig.add_trace(go.Scatter(x=cr, y=ct, **style), 1, 1)
    fig.add_trace(go.Scatter(x=P(cr, ct)[0], y=P(cr, ct)[1], **style), 1, 2)
    fig.update_annotations(font_size=22)
    rm = r0 + DR / 2
    fig.update_layout(template="simple_white", width=1000, height=560, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), margin=dict(l=70, r=20, t=120, b=60),
                      title=dict(text=f"cell at r = {rm:.1f}: area out = {rm:.1f} × 0.08 = {area_out(r0):.3f}",
                                 x=0.5, y=0.96))
    fig.update_xaxes(title="r", range=[0, 3.05], row=1, col=1)
    fig.update_yaxes(title="θ (radians)", range=[0, 1.25], row=1, col=1)
    fig.update_xaxes(title="x", range=[0, 3.05], row=1, col=2)
    fig.update_yaxes(title="y", range=[0, 2.6], scaleanchor="x2", row=1, col=2)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".area_frames"
    tmp.mkdir(exist_ok=True)
    for k, r0 in enumerate(STARTS):
        frame(r0).write_image(tmp / f"{k:03d}.png")
    n = len(STARTS)
    for k in range(n, n + 4):
        shutil.copy(tmp / f"{n - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "area_scaling.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, n - 1)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, h), "white")      # side by side: readable at text width
    for i, im in enumerate(keys):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "area_scaling_frames.png")
    shutil.rmtree(tmp)
