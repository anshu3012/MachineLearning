"""Section 2: one tree's bootstrap sample, drawn one observation at a time. 20 observations, 20 draws with
replacement (numpy default_rng(0)). Bars count how often each observation has been drawn; observations still at 0
after the last draw (orange) are out-of-bag for this tree.
Run: python bootstrap_draw.py  -> bootstrap_draw.gif, bootstrap_draw_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
N = 20
draws = np.random.default_rng(0).integers(1, N + 1, N)        # observation numbers 1..20
counts = np.bincount(draws, minlength=N + 1)[1:]
n_oob = int((counts == 0).sum())
assert counts.sum() == N and 0 < n_oob < N
print("drawn:", draws.tolist(), " out-of-bag:", n_oob, "of", N, f"({n_oob / N:.0%}; theory about 36%)")
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#BBBBBB"


def frame(k):
    c = np.bincount(draws[:k], minlength=N + 1)[1:]
    done = k == N
    colours = [BLUE if v else (ORANGE if done else GREY) for v in c]
    shown = np.where((c == 0) & done, 0.3, c)                 # out-of-bag: a short orange stub labelled OOB
    fig = go.Figure(go.Bar(x=np.arange(1, N + 1), y=shown, marker_color=colours, textposition="outside",
                           text=[str(v) if v else ("OOB" if done else "") for v in c], textfont_size=18))
    if 0 < k < N:
        fig.add_annotation(x=draws[k - 1], y=c[draws[k - 1] - 1] + 0.75, text="▼ draw", showarrow=False,
                           font=dict(size=20, color="black"))
    title = (f"draw {k} of {N}: observation {draws[k - 1]}" if 0 < k < N else
             f"after {N} draws: {n_oob} of {N} never drawn = out-of-bag (orange)" if done else
             "one tree's bootstrap sample: 20 draws with replacement")
    fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=title, x=0.5), margin=dict(l=70, r=20, t=70, b=70), showlegend=False,
                      xaxis=dict(title="observation", tickvals=list(range(1, N + 1))),
                      yaxis=dict(title="times drawn", range=[0, counts.max() + 1.3], dtick=1))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".draw_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(N + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(N + 1, N + 9):                              # hold the last frame
        shutil.copy(tmp / f"{N:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=6,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "bootstrap_draw.gif")], check=True)
    shutil.copy(tmp / f"{N:03d}.png", HERE / "bootstrap_draw_frames.png")   # PDF: the last frame alone (a grid is too small)
    shutil.rmtree(tmp)
