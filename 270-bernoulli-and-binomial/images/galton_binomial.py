"""Bernoulli trials add up to a binomial count, as a Galton board: each run of 10 fair-coin tosses is a ball that
steps right on a head and left on a tail, and lands in the bin of its head count. The bins fill with the 1000 runs
of section 7 (seed 42, so heads[:10] = 6 5 7 6 3 8 6 6 3 5 and 5 heads appear 244 times); at the end the exact
binomial PMF (dots) is laid over the shares. rng.binomial gives only the count, so each ball's order of heads and
tails is a random arrangement of that count (all arrangements are equally likely given the count).
Galton-board picture after Sanderson (3Blue1Brown), "But what is the Central Limit Theorem?".
Run: python galton_binomial.py -> galton_binomial.gif, galton_binomial_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
N, RUNS = 10, 1000
heads = np.random.default_rng(42).binomial(N, 0.5, RUNS)            # the Notebook's simulation
assert list(heads[:10]) == [6, 5, 7, 6, 3, 8, 6, 6, 3, 5] and (heads == 5).sum() == 244
order = np.random.default_rng(0)
tosses = np.array([order.permutation([1] * h + [0] * (N - h)) for h in heads])   # 1 = head
assert (tosses.sum(axis=1) == heads).all()
paths = np.hstack([np.zeros((RUNS, 1)), np.cumsum(2 * tosses - 1, axis=1)])      # x after t tosses: heads - tails
PMF = stats.binom.pmf(np.arange(N + 1), N, 0.5)
X_BIN = 2 * np.arange(N + 1) - N                                    # bin of h heads sits at x = 2h - 10
PEG_X = [x for t in range(N) for x in range(-t, t + 1, 2)]
PEG_Y = [-t for t in range(N) for _ in range(-t, t + 1, 2)]


def frame(done, ball=None, step=0, show_pmf=False):
    """done: runs already in the bins; ball: index of the run being dropped, shown up to `step` tosses."""
    fig = make_subplots(rows=2, cols=1, row_heights=[0.55, 0.45], vertical_spacing=0.04, shared_xaxes=True)
    fig.add_scatter(x=PEG_X, y=PEG_Y, mode="markers", marker=dict(color=GREY, size=7), row=1, col=1)
    title = f"<b>{done:,} runs in the bins</b>"
    if ball is not None:
        p = paths[ball][:step + 1]
        fig.add_scatter(x=p, y=-np.arange(step + 1), mode="lines+markers", line=dict(color=ORANGE, width=4),
                        marker=dict(size=8, color=ORANGE), row=1, col=1)
        fig.add_scatter(x=[p[-1]], y=[-step], mode="markers", marker=dict(size=22, color=ORANGE,
                        line=dict(color="black", width=1.5)), row=1, col=1)
        seq = " ".join("H" if t else "T" for t in tosses[ball][:step])
        title = f"<b>run {ball + 1}: {seq}</b>" + (f"<b> → {heads[ball]} heads</b>" if step == N else "")
    share = np.bincount(heads[:done], minlength=N + 1) / max(done, 1)
    fig.add_bar(x=X_BIN, y=share, marker_color=BLUE, opacity=0.75, width=1.6, row=2, col=1)
    if done and done < 60:                                          # few runs: show the raw counts
        cnt = np.bincount(heads[:done], minlength=N + 1)
        fig.add_scatter(x=X_BIN, y=share, mode="text", text=[str(c) if c else "" for c in cnt],
                        textposition="top center", textfont=dict(size=20), row=2, col=1)
    if show_pmf:
        fig.add_scatter(x=X_BIN, y=PMF, mode="markers", marker=dict(color="black", size=13), row=2, col=1)
        fig.add_annotation(x=X_BIN[8], y=0.32, text="● exact binomial PMF", showarrow=False, font_size=22,
                           xref="x2", yref="y2")
    fig.update_xaxes(showticklabels=False, showline=False, ticks="", row=1, col=1)
    fig.update_yaxes(visible=False, range=[-N - 0.4, 0.6], row=1, col=1)
    fig.update_xaxes(tickvals=X_BIN, ticktext=[str(h) for h in range(N + 1)], range=[-N - 1.2, N + 1.2],
                     title_text="number of heads in 10 tosses", row=2, col=1)
    fig.update_yaxes(range=[0, max(0.36, 1.2 * share.max()) if done < 60 else 0.36], title_text="share of runs", row=2, col=1)
    fig.update_layout(template="simple_white", width=900, height=860, showlegend=False, bargap=0,
                      font=dict(family="Latin Modern Roman", size=22), title=dict(text=title, x=0.5, y=0.975),
                      margin=dict(l=90, r=30, t=70, b=70))
    return fig


def plan():
    """(kwargs, label) for every frame: three balls toss by toss, 17 whole drops, then the bins fill to 1000."""
    out = []
    for b in range(3):
        out += [dict(done=b, ball=b, step=s) for s in range(N + 1)] + [dict(done=b + 1, ball=b, step=N)]
    out += [dict(done=b + 1, ball=b, step=N) for b in range(3, 20)]
    out += [dict(done=d) for d in (20, 40, 70, 100, 150, 200, 300, 400, 550, 700, 850, 1000)]
    out += [dict(done=RUNS, show_pmf=True)] * 12                    # hold with the exact PMF
    return out


if __name__ == "__main__":
    tmp = HERE / ".galton_frames"
    tmp.mkdir(exist_ok=True)
    frames = plan()
    for j, kw in enumerate(frames):
        frame(**kw).write_image(tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=600:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "galton_binomial.gif")], check=True)
    pick = [6, 11, frames.index(dict(done=100)), len(frames) - 1]      # mid-drop, one landed, 100 runs, 1000 + PMF
    keys = [Image.open(tmp / f"{j:03d}.png").convert("RGB") for j in pick]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "galton_binomial_frames.png")
    shutil.rmtree(tmp)
