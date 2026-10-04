"""Where bootstrapping comes from: resample a small dataset to see how much its mean could vary. Example data: 8
responses to a drug (5 positive, 3 negative, mean 0.5), our own numbers. Left: the 8 original values (top row) and
the bootstrap sample being drawn from them with replacement (bottom row; a value drawn again is stacked). Right: the
histogram of bootstrap means, first one mean at a time, then 10, 100, 1,000 and 10,000 samples (seed 0).
Idea after StatQuest, "Bootstrapping Main Ideas!!!". Plotly frames -> ffmpeg GIF, plus a grid of frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=24)
BLUE, ORANGE, GREEN, GREY = "#4C78A8", "#F58518", "#54A24B", "#8A8A8A"

DATA = np.array([1.8, 1.4, 1.1, 0.9, 0.6, -0.3, -0.6, -0.9])
assert DATA.mean() == 0.5
rng = np.random.default_rng(0)
IDX = rng.integers(0, 8, size=(10_000, 8))               # 10,000 bootstrap samples of 8 draws
MEANS = DATA[IDX].mean(axis=1)
SE = MEANS.std()
LOW, HIGH = np.percentile(MEANS, [2.5, 97.5])
assert sorted(DATA[IDX[0]].tolist()) == [-0.6, -0.3, 0.6, 1.1, 1.1, 1.8, 1.8, 1.8] and round(MEANS[0], 2) == 0.91
assert (f"{SE:.2f}", f"{LOW:.2f}", f"{HIGH:.2f}") == ("0.32", "-0.15", "1.12"), (SE, LOW, HIGH)
BINS = dict(start=-1.0, end=2.0, size=0.1)


def frame(sample, drawn, n_means, final=False):
    """sample: index of the bootstrap sample shown on the left; drawn: how many of its 8 values are drawn so far;
    n_means: how many bootstrap means are in the histogram."""
    fig = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5], horizontal_spacing=0.12)
    fig.add_scatter(x=DATA, y=[1] * 8, mode="markers", marker=dict(size=22, color=BLUE), row=1, col=1)
    vals = DATA[IDX[sample, :drawn]]
    height = [0.0 + 0.12 * int((vals[:i] == v).sum()) for i, v in enumerate(vals)]     # stack repeats
    colour = [ORANGE if (vals[:i] == v).any() else GREEN for i, v in enumerate(vals)]
    fig.add_scatter(x=vals, y=height, mode="markers", marker=dict(size=22, color=colour), row=1, col=1)
    if drawn == 8:
        fig.add_scatter(x=[vals.mean()] * 2, y=[-0.08, 0.5], mode="lines", line=dict(color="black", width=3, dash="dash"),
                        row=1, col=1)
        fig.add_annotation(x=vals.mean(), y=0.6, text=f"<b>mean {vals.mean():.2f}</b>", showarrow=False, row=1, col=1)
    fig.add_annotation(x=-1.2, y=1.2, xanchor="left", text="the 8 measured values (mean 0.50)", showarrow=False,
                       font=dict(color=BLUE), row=1, col=1)
    fig.add_annotation(x=-1.2, y=-0.22, xanchor="left", showarrow=False, row=1, col=1,
                       text=f"bootstrap sample: {drawn} of 8 drawn (<span style='color:{ORANGE}'>orange = repeat</span>)")
    fig.add_histogram(x=MEANS[:n_means], xbins=BINS, marker_color=GREY, row=1, col=2)
    if final:
        fig.add_vrect(x0=LOW, x1=HIGH, fillcolor=GREEN, opacity=0.15, line_width=0, row=1, col=2)
        fig.add_vline(x=0, line=dict(color="black", width=2, dash="dot"), row=1, col=2)
        fig.add_annotation(x=0.5, y=1.07, xref="x2 domain", yref="y2 domain", showarrow=False, font=dict(color=GREEN),
                           text=f"95% of the means: {LOW:.2f} to {HIGH:.2f}")
    fig.update_xaxes(title="response to the drug", range=[-1.3, 2.2], row=1, col=1)
    fig.update_yaxes(visible=False, range=[-0.4, 1.4], row=1, col=1)
    fig.update_xaxes(title="mean of a bootstrap sample", range=[-1.0, 2.0], row=1, col=2)
    top = max(5, 1.12 * np.histogram(MEANS[:n_means], bins=np.arange(-1.0, 2.01, 0.1))[0].max()) if n_means else 5
    fig.update_yaxes(title="number of samples", range=[0, top], row=1, col=2)
    title = (f"<b>{n_means:,} bootstrap samples:</b> their means spread from about {LOW:.2f} to {HIGH:.2f}" if final else
             f"<b>Bootstrap sample {sample + 1}</b>, means recorded: {n_means:,}")
    fig.update_layout(template="simple_white", width=1400, height=680, font=FONT, showlegend=False, bargap=0.05,
                      title=dict(text=title, x=0.5, y=0.96, font=dict(size=30)), margin=dict(l=40, r=30, t=110, b=90))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".bm_frames"
    tmp.mkdir(exist_ok=True)
    shots = [(0, d, 0, False) for d in range(1, 9)] + [(0, 8, 1, False)] * 2
    shots += [(1, 4, 1, False), (1, 8, 2, False), (2, 4, 2, False), (2, 8, 3, False)]
    shots += [(n - 1, 8, n, False) for n in (10, 100, 1000)] + [(9999, 8, 10_000, True)]
    paths = []
    for j, s in enumerate(shots):
        paths.append(tmp / f"s{j:02d}.png")
        frame(*s).write_image(paths[-1])
    seq = list(range(len(shots))) + [len(shots) - 1] * 6
    for j, k in enumerate(seq):
        shutil.copy(paths[k], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "bootstrap_means.gif")], check=True)
    ims = [Image.open(paths[k]).convert("RGB") for k in (8, len(shots) - 1)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (w, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (0, i * (h + 16)))
    sheet.save(HERE / "bootstrap_means_frames.png")
    shutil.rmtree(tmp)
