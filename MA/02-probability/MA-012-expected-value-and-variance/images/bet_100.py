"""Section 3.1: a 1-rupee bet made 100 times. With P(lose) = 0.17 and P(win) = 0.83, about 17 of 100 bets lose
(red, -1) and 83 win (green, +1). The total is -17 + 83 = +66 rupees, 0.66 per bet, which is the expected value
(-1)(0.17) + (1)(0.83): the 100s cancel.
Run: python bet_100.py  -> bet_100.gif, bet_100_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
RED, GREEN, GREY = "#E45756", "#54A24B", "#BBBBBB"
assert round(-1 * 0.17 * 100 + 1 * 0.83 * 100) == 66 and round(-0.17 + 0.83, 2) == 0.66
cols, rows = np.meshgrid(np.arange(10), np.arange(10)[::-1])
X, Y = cols.ravel(), rows.ravel()
TEXT = ["100 bets of 1 rupee each",
        "<span style='color:#E45756'>lose 0.17 × 100 = 17 bets: −17</span>",
        "<span style='color:#54A24B'>win 0.83 × 100 = 83 bets: +83</span>",
        "total: −17 + 83 = <b>+66 rupees</b>",
        "per bet: 66 / 100 = <b>0.66</b>",
        "100s cancel:<br>(−1)(0.17) + (1)(0.83)<br>= <b>0.66 = E[X]</b>"]


def frame(step, n_red, n_green):
    colour = np.array([GREY] * 100, dtype=object)
    colour[:n_red] = RED
    colour[17:17 + n_green] = GREEN
    fig = go.Figure(go.Scatter(x=X, y=Y, mode="markers+text", marker=dict(size=34, color=list(colour),
                                                                        line=dict(width=1.5, color="black")),
                               text=["−1" if i < n_red else ("+1" if 17 <= i < 17 + n_green else "")
                                     for i in range(100)],
                               textfont=dict(color="white", size=14)))
    fig.add_annotation(x=11.0, y=4.5, xanchor="left", showarrow=False, align="left", text="<br><br>".join(TEXT[max(1, 0 if step == 0 else 1):step + 1]) if step else TEXT[0],
                       font=dict(size=30))
    fig.update_layout(template="simple_white", width=1100, height=540, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text="Lose 1 rupee with probability 0.17, win 1 rupee with 0.83", x=0.5, y=0.96),
                      xaxis=dict(visible=False, range=[-0.7, 22]), yaxis=dict(visible=False, range=[-0.7, 9.7]),
                      margin=dict(l=20, r=20, t=70, b=20))
    return fig


PLAN = [(0, 0, 0, 4)] + [(1, r, 0, 1) for r in (6, 12, 17)] + [(1, 17, 0, 4)] \
    + [(2, 17, g, 1) for g in (20, 40, 60, 83)] + [(2, 17, 83, 4), (3, 17, 83, 7), (4, 17, 83, 7), (5, 17, 83, 14)]

if __name__ == "__main__":
    tmp = HERE / ".bet_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, {}
    for step, r, g, hold in PLAN:
        frame(step, r, g).write_image(tmp / f"{n:03d}.png")
        keys[step] = n
        for _ in range(hold - 1):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + 1:03d}.png")
            n += 1
        n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "bet_100.gif")], check=True)
    ims = [Image.open(tmp / f"{keys[k]:03d}.png").convert("RGB") for k in (1, 2, 3, 5)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "bet_100_frames.png")
    shutil.rmtree(tmp)
