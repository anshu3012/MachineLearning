"""Two ways to know the sine function. Geometric: a point turns around the unit circle and sin(t) is its height,
traced out as a curve. Numeric: the polynomial t - t^3/3! + t^5/5! - ..., which is how a calculator evaluates
sine; adding terms makes it hug the same curve over a wider range. Plotly frames -> ffmpeg GIF + key-frame grid.
Run: python sine_two_views.py  -> sine_two_views.gif, sine_two_views_frames.png"""
import shutil
import subprocess
from math import factorial
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
T = np.linspace(0, 2 * np.pi, 400)
CIRCLE = np.linspace(0, 2 * np.pi, 200)


def taylor(t, n):
    """Sum of the first n non-zero terms of the sine series."""
    return sum((-1) ** k * t ** (2 * k + 1) / factorial(2 * k + 1) for k in range(n))


# the series really approaches sine on [0, 2 pi]: the worst error falls with every extra term
NMAX = 9
ERR = [np.abs(taylor(T, n) - np.sin(T)).max() for n in range(1, NMAX + 1)]
assert all(a > b for a, b in zip(ERR[2:], ERR[3:])) and ERR[-1] < 0.02    # from 3 terms on, every term helps


def base(title):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.38, 0.62], horizontal_spacing=0.08,
                        subplot_titles=("sin(t): height of a point on a circle", "solid: sin(t)    dashed: the polynomial"))
    fig.update_layout(template="simple_white", width=1100, height=520, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), title=dict(text=title, x=0.5, y=0.97),
                      margin=dict(l=40, r=20, t=110, b=50))
    fig.update_annotations(font_size=22)
    fig.update_xaxes(range=[-1.3, 1.3], row=1, col=1, scaleanchor="y", scaleratio=1, showticklabels=False)
    fig.update_yaxes(range=[-1.3, 1.3], row=1, col=1, showticklabels=False)
    fig.update_xaxes(range=[0, 2 * np.pi], row=1, col=2, title="t", tickvals=[0, np.pi, 2 * np.pi], ticktext=["0", "π", "2π"])
    fig.update_yaxes(range=[-1.6, 1.6], row=1, col=2, tickvals=[-1, 0, 1])
    fig.add_trace(go.Scatter(x=np.cos(CIRCLE), y=np.sin(CIRCLE), line=dict(color=GREY, width=2)), 1, 1)
    return fig


def circle_frame(t):
    s = 0.0 if abs(np.sin(t)) < 0.005 else np.sin(t)
    fig = base(f"t = {t:.2f}: sin(t) = {s:+.2f}")
    fig.add_trace(go.Scatter(x=[0, np.cos(t)], y=[0, np.sin(t)], line=dict(color=GREY, width=2)), 1, 1)
    fig.add_trace(go.Scatter(x=[np.cos(t), np.cos(t)], y=[0, np.sin(t)], line=dict(color=BLUE, width=6)), 1, 1)
    fig.add_trace(go.Scatter(x=[np.cos(t)], y=[np.sin(t)], mode="markers", marker=dict(color=BLUE, size=16)), 1, 1)
    tt = T[T <= t]
    fig.add_trace(go.Scatter(x=tt, y=np.sin(tt), line=dict(color=BLUE, width=5)), 1, 2)
    fig.add_trace(go.Scatter(x=[t, t], y=[0, np.sin(t)], line=dict(color=BLUE, width=6)), 1, 2)
    return fig


def series_frame(n):
    last = "t" if n == 1 else f"t<sup>{2 * n - 1}</sup>/{2 * n - 1}!"
    text = "t" if n == 1 else ("t − t<sup>3</sup>/3! " if n == 2 else "t − t<sup>3</sup>/3! + … ") + ("" if n == 2 else ("− " if n % 2 == 0 else "+ ") + last)
    fig = base(f"{n} term{'s' if n > 1 else ''}: {text}   (largest gap {ERR[n - 1]:.2f})")
    fig.add_trace(go.Scatter(x=np.cos(CIRCLE), y=np.sin(CIRCLE), line=dict(color=GREY, width=2)), 1, 1)
    fig.add_trace(go.Scatter(x=T, y=np.sin(T), line=dict(color=BLUE, width=5)), 1, 2)
    y = np.clip(taylor(T, n), -5, 5)
    fig.add_trace(go.Scatter(x=T, y=y, line=dict(color=ORANGE, width=4, dash="dash")), 1, 2)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".sine_frames"
    tmp.mkdir(exist_ok=True)
    figs = [circle_frame(t) for t in np.linspace(0.05, 2 * np.pi, 24)]
    figs += [figs[-1]] * 4                                     # hold the traced curve
    first_series = len(figs)
    for n in range(1, NMAX + 1):
        figs += [series_frame(n)] * 3
    figs += [figs[-1]] * 4                                     # hold the last frame
    for k, f in enumerate(figs):
        f.write_image(tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "sine_two_views.gif")], check=True)
    picks = [8, 23, first_series + 3 * 3, first_series + 3 * (NMAX - 1)]  # mid-turn, full turn, 4 terms, 9 terms
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in picks]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "sine_two_views_frames.png")
    shutil.rmtree(tmp)
