"""The Hubel and Wiesel experiment, replayed with the Note's model simple cell (the Notebook's 7 x 7 vertical-bar
filter at the centre of a 41 x 41 screen, then ReLU). A bar of light rotates from horizontal (0 degrees) through
vertical (90) and back (180); the cell's response is traced as it turns. The responses are recomputed here and
checked against data/tuning.csv. Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

from common import BLUE

HERE = Path(__file__).parent
N = 41
yy, xx = np.mgrid[0:N, 0:N]


def bar(angle_deg, width=1.5, length=14):
    a = np.deg2rad(angle_deg)
    dx, dy = xx - 20, yy - 20
    along, across = dx * np.cos(a) - dy * np.sin(a), dx * np.sin(a) + dy * np.cos(a)
    return ((np.abs(across) <= width) & (np.abs(along) <= length)).astype(float)


K = np.zeros((7, 7))
K[:, 2:5], K[:, :2], K[:, 5:] = 1.0, -0.75, -0.75
simple = lambda img: max(0.0, float((img[17:24, 17:24] * K).sum()))
T = pd.read_csv(HERE.parent / "data" / "tuning.csv")
R = np.array([simple(bar(a)) for a in T.angle])
assert np.allclose(R / R.max(), T.simple)
ANG = T.angle.values
SHOW = list(range(0, len(ANG), 3)) + [len(ANG) - 1] if (len(ANG) - 1) % 3 else list(range(0, len(ANG), 3))


def frame(i):
    a = ANG[i]
    fig = make_subplots(rows=1, cols=2, column_widths=[0.4, 0.6], horizontal_spacing=0.1,
                        subplot_titles=(f"Screen: bar at {a}°", "The cell's response as the bar turns"))
    fig.add_trace(go.Heatmap(z=bar(a), colorscale="gray", showscale=False, hoverinfo="skip"), 1, 1)
    fig.add_shape(type="rect", x0=16.5, x1=23.5, y0=16.5, y1=23.5, line=dict(color="#F58518", width=3), fillcolor="rgba(0,0,0,0)", row=1, col=1)
    fig.add_scatter(x=ANG[:i + 1], y=T.simple[:i + 1], mode="lines+markers", line=dict(color=BLUE, width=4),
                    marker=dict(size=8), showlegend=False, row=1, col=2)
    fig.add_scatter(x=[a], y=[T.simple[i]], mode="markers", marker=dict(size=20, color="#F58518"), showlegend=False,
                    row=1, col=2)
    fig.update_xaxes(visible=False, row=1, col=1)
    fig.update_yaxes(visible=False, autorange="reversed", scaleanchor="x", row=1, col=1)
    fig.update_xaxes(title_text="angle of the bar (degrees; 90 = vertical)", range=[-5, 185],
                     tickvals=[0, 45, 90, 135, 180], row=1, col=2)
    fig.update_yaxes(title_text="response (1 = largest)", range=[-0.05, 1.1], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=560, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"Response of the model simple cell: <b>{T.simple[i]:.2f}</b>  "
                                      "(orange square: its receptive field)", x=0.5, y=0.96, font=dict(size=21)),
                      margin=dict(l=40, r=30, t=100, b=70))
    for t in fig.layout.annotations:
        t.font.size = 19
    return fig


if __name__ == "__main__":
    tmp = HERE / ".hw_frames"
    tmp.mkdir(exist_ok=True)
    keys = {}
    for i in SHOW:
        keys[i] = tmp / f"k{i}.png"
        frame(i).write_image(keys[i])
    seq = [SHOW[0]] * 2 + SHOW + [SHOW[-1]] * 4
    for j, i in enumerate(seq):
        shutil.copy(keys[i], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=880:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "hubel_wiesel.gif")], check=True)
    mid = min(SHOW, key=lambda i: abs(ANG[i] - 90))
    shutil.copy(keys[mid], HERE / "hubel_wiesel_frames.png")
    shutil.rmtree(tmp)
    print(len(ANG), SHOW[:5], ANG[mid])
