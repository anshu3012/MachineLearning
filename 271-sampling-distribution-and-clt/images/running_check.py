"""Section 6 check, watched as it runs: 10,000 samples of size 50 from gamma(shape 2, scale 1) (mu = 2,
sigma^2 = 2), seed 7 as in the Notebook. As samples accumulate, the mean of the sample means settles on 2 and their
variance on sigma^2/n = 0.04.
Run: python running_check.py -> running_check.gif, running_check_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"
means = np.random.default_rng(7).gamma(2, 1, size=(10_000, 50)).mean(axis=1)
assert round(means.mean(), 4) == 1.9974 and round(means.var(), 4) == 0.0405 and round(means.std(), 4) == 0.2012
k = np.arange(1, len(means) + 1)
run_mean = np.cumsum(means) / k
run_var = np.cumsum(means ** 2) / k - run_mean ** 2                 # population-style variance, as means.var()
assert np.isclose(run_var[-1], means.var())
STOPS = np.unique(np.round(np.logspace(np.log10(2), 4, 34)).astype(int))


def frame(m):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.14,
                        subplot_titles=[f"mean of the sample means: {run_mean[m - 1]:.4f}  (CLT: 2)",
                                        f"variance of the sample means: {run_var[m - 1]:.4f}  (CLT: 2/50 = 0.04)"])
    for row, y, target, colour in [(1, run_mean, 2, BLUE), (2, run_var, 0.04, ORANGE)]:
        fig.add_scatter(x=k[1:m], y=y[1:m], mode="lines", line=dict(color=colour, width=3.5), showlegend=False,
                        row=row, col=1)
        fig.add_scatter(x=[k[m - 1]], y=[y[m - 1]], mode="markers", marker=dict(color=colour, size=12),
                        showlegend=False, row=row, col=1)
        fig.add_hline(y=target, line=dict(color="black", width=2, dash="dash"), row=row, col=1)
    fig.update_xaxes(type="log", range=[0.25, 4.05], row=1, col=1)
    fig.update_xaxes(type="log", range=[0.25, 4.05], title_text="number of samples drawn (log scale)", row=2, col=1)
    fig.update_yaxes(range=[1.6, 2.4], row=1, col=1)
    fig.update_yaxes(range=[0, 0.09], row=2, col=1)
    fig.update_annotations(font_size=22)
    fig.update_layout(template="simple_white", width=900, height=640, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"{m:,} samples of 50", x=0.5, y=0.985), margin=dict(l=70, r=20, t=100, b=60))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".running_frames"
    tmp.mkdir(exist_ok=True)
    for i, m in enumerate(STOPS):
        frame(m).write_image(tmp / f"{i:03d}.png")
    last = len(STOPS) - 1
    for i in range(last + 1, last + 9):
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "running_check.gif")], check=True)
    shutil.copy(tmp / f"{last:03d}.png", HERE / "running_check_frames.png")   # PDF: the final frame alone, readable at page width
    shutil.rmtree(tmp)
