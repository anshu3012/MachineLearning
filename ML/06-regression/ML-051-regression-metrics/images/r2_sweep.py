"""R2 as the share of squared error removed: the flat average line turns into the regression line, the squared
errors shrink, and the R2 bar fills (Plotly frames + ffmpeg -> r2_sweep.gif, r2_sweep_frames.png). Test set of 40.
Idea of drawing the errors as squares: Starmer, J. (StatQuest), "R-squared, Clearly Explained"."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from common import x, y, pred, lr, BLUE, ORANGE, RED, GREY

HERE = Path(__file__).parent
ybar = y.mean()
sst = float(((y - ybar) ** 2).sum())
T = np.r_[np.zeros(4), np.linspace(0, 1, 17), np.ones(8)]          # hold start, turn the line, hold end
ss = lambda t: float(((y - ((1 - t) * ybar + t * pred)) ** 2).sum())
assert abs(1 - ss(1) / sst - 0.781) < 0.001                          # matches the Note's R2
XR, YR = [4.2, 9.6], [0.9, 4.9]


def frame(t):
    yhat = (1 - t) * ybar + t * pred
    s = ss(t)
    fig = make_subplots(2, 2, column_widths=[0.66, 0.34], specs=[[{"rowspan": 2}, {}], [None, {}]],
                        horizontal_spacing=0.1, vertical_spacing=0.3,
                        subplot_titles=("", "Squared errors", "R² = 1 − orange / red"))
    for a, b, c in zip(x, y, yhat):                                  # one square per student, side = its error
        d = abs(b - c)
        side = 1 if b < c else -1                                    # square sits away from the line's far side
        fig.add_trace(go.Scatter(x=[a, a + side * d, a + side * d, a, a], y=[c, c, b, b, c], fill="toself",
                                 mode="lines", line=dict(width=0.5, color=ORANGE), fillcolor="rgba(245,133,24,0.18)"),
                      1, 1)
    fig.add_trace(go.Scatter(x=XR, y=[ybar, ybar], mode="lines", line=dict(color=RED, width=2, dash="dot")), 1, 1)
    fig.add_trace(go.Scatter(x=XR, y=(1 - t) * ybar + t * (lr.coef_[0] * np.array(XR) + lr.intercept_), mode="lines",
                             line=dict(color=ORANGE, width=4)), 1, 1)
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=dict(size=8, color=BLUE)), 1, 1)
    fig.add_trace(go.Bar(x=["average", "this line"], y=[sst, s], marker_color=[RED, ORANGE], width=0.6,
                         text=[f"{sst:.1f}", f"{s:.1f}"], textposition="outside", textfont=dict(size=22)), 1, 2)
    r2 = 1 - s / sst
    fig.add_trace(go.Bar(x=[r2], y=[""], orientation="h", marker_color=BLUE, width=0.6, text=[f"{r2:.2f}"],
                         textposition="outside", textfont=dict(size=24)), 2, 2)
    fig.update_xaxes(title="CGPA", range=XR, row=1, col=1)
    fig.update_yaxes(title="Package (LPA)", range=YR, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_yaxes(range=[0, 27], showticklabels=False, ticks="", row=1, col=2)
    fig.update_xaxes(range=[0, 1.25], tickvals=[0, 0.5, 1], row=2, col=2)
    fig.update_yaxes(showticklabels=False, ticks="", row=2, col=2)
    head = "Guess the average for everyone" if t == 0 else ("The regression line" if t == 1 else "Turning the line")
    fig.update_layout(template="simple_white", width=1100, height=560, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=20), margin=dict(l=70, r=30, t=80, b=60),
                      title=dict(text=head, x=0.33, xanchor="center", y=0.97))
    fig.update_annotations(font_size=21)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".r2_frames"
    tmp.mkdir(exist_ok=True)
    for k, t in enumerate(T):
        frame(t).write_image(tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=880:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "r2_sweep.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 8, 14, len(T) - 1)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "r2_sweep_frames.png")
    shutil.rmtree(tmp)
    print("SST", round(sst, 2), "SSR", round(ss(1), 2), "min over t", round(min(ss(t) for t in np.linspace(0, 1.2, 61)), 2))
