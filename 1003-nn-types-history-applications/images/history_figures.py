"""Three figures for the history and applications (Plotly):
imagenet_errors.png     : best ImageNet top-5 error by year as given in the Note (about 28 percent in 2010, 26 in 2011),
                          and 2012: AlexNet 15.3 against the second-best entry 26.2 (Krizhevsky et al. 2012).
go_vs_chess.png         : sequences of moves after n turns with about 35 choices (chess) or 250 (Go) per turn.
universal_approx.gif    : one hidden layer of n sigmoid neurons (steep, evenly placed) with least-squares output
                          weights, approximating a continuous function; the worst error falls as n grows.
Run: python history_figures.py"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=24)

# 1. ImageNet
years = ["2010<br>best entry", "2011<br>best entry", "2012<br>second best", "2012<br>AlexNet"]
err = [28, 26, 26.2, 15.3]
assert err[3] / err[2] < 0.6                                   # "almost half"
fig = go.Figure(go.Bar(x=years, y=err, marker_color=[GREY, GREY, GREY, RED], text=[f"{e:g}%" for e in err],
                       textposition="outside", textfont=dict(size=26)))
fig.update_layout(template="simple_white", width=1000, height=560, font=FONT, margin=dict(l=80, r=20, t=30, b=90),
                  yaxis=dict(title="top-5 error (percent)", range=[0, 33]))
fig.write_image(HERE / "imagenet_errors.png", scale=2)

# 2. Go against chess
n = np.arange(0, 41)
chess, gov = n * np.log10(35), n * np.log10(250)
assert np.isclose(gov[10] - chess[10], 10 * np.log10(250 / 35))   # the gap widens by 0.85 orders per turn
fig = go.Figure()
fig.add_trace(go.Scatter(x=n, y=chess, mode="lines", line=dict(color=BLUE, width=4), name="chess: about 35 moves per turn"))
fig.add_trace(go.Scatter(x=n, y=gov, mode="lines", line=dict(color=RED, width=4), name="Go: about 250 moves per turn"))
fig.update_layout(template="simple_white", width=1000, height=560, font=FONT, margin=dict(l=80, r=20, t=30, b=70),
                  xaxis=dict(title="turns played"), yaxis=dict(title="possible move sequences", tickvals=list(range(0, 101, 20)),
                                                               ticktext=[f"10<sup>{k}</sup>" for k in range(0, 101, 20)]),
                  legend=dict(x=0.02, y=0.98))
fig.add_annotation(x=40, y=gov[40], text=f"10<sup>{gov[40]:.0f}</sup>", showarrow=False, xanchor="right", yshift=22,
                   font=dict(color=RED, size=24))
fig.add_annotation(x=40, y=chess[40], text=f"10<sup>{chess[40]:.0f}</sup>", showarrow=False, xanchor="right", yshift=22,
                   font=dict(color=BLUE, size=24))
fig.write_image(HERE / "go_vs_chess.png", scale=2)

# 3. Universal approximation
x = np.linspace(0, 1, 800)
target = np.sin(2 * np.pi * x) + 0.5 * np.sin(6 * np.pi * x) + x   # any continuous function on [0, 1]
NS = [1, 2, 4, 8, 16, 32]


def fit(k):
    centres = (np.arange(k) + 0.5) / k
    H = 1 / (1 + np.exp(-8 * k * (x[:, None] - centres)))           # k hidden sigmoid neurons, steeper when more
    H = np.c_[np.ones_like(x), H]                                 # plus the output bias
    v, *_ = np.linalg.lstsq(H, target, rcond=None)
    return H @ v


errs = {k: np.abs(fit(k) - target).max() for k in NS}
assert all(errs[a] > errs[b] for a, b in zip(NS, NS[1:]))         # worst error keeps falling
assert errs[32] < 0.1


def frame(k):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=target, mode="lines", line=dict(color=GREY, width=6), name="target function"))
    fig.add_trace(go.Scatter(x=x, y=fit(k), mode="lines", line=dict(color=RED, width=3),
                             name=f"network, {k} hidden neuron{'s' if k > 1 else ''}"))
    fig.update_layout(template="simple_white", width=900, height=560, font=FONT,
                      title=dict(text=f"{k} hidden neuron{'s' if k > 1 else ''}: worst error {errs[k]:.2f}", x=0.5),
                      xaxis=dict(title="input x"), yaxis=dict(title="output", range=[-1.3, 2.2]),
                      legend=dict(x=0.01, y=0.02, yanchor="bottom"), margin=dict(l=70, r=20, t=70, b=70))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".ua_frames"
    tmp.mkdir(exist_ok=True)
    for i, k in enumerate(NS):
        frame(k).write_image(tmp / f"{i:03d}.png")
    for i in range(len(NS), len(NS) + 3):
        shutil.copy(tmp / f"{len(NS) - 1:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "universal_approx.gif")], check=True)
    keys = [Image.open(tmp / f"{NS.index(k):03d}.png").convert("RGB") for k in (1, 4, 8, 32)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "universal_approx_frames.png")
    shutil.rmtree(tmp)
    print({k: round(e, 3) for k, e in errs.items()})
