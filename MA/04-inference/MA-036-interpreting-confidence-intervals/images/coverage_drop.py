"""Confidence intervals drop in one by one: blue if the interval contains mu = 50, red if it misses. Below, the
running share that contain mu; after the first 100 intervals the same simulation runs on to 100,000 and the share
settles near 95%. Data: the Notebook's intervals(sims=100_000) with seed 42; its first 100 rows are Figure 1's.
Idea after Seeing Theory (Kunin et al.), "Frequentist Inference: Confidence Interval".
Run: python coverage_drop.py -> coverage_drop.gif, coverage_drop_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE, RED, GREY = "#4C78A8", "#E45756", "#6B6B6B"
MU, SIGMA, N, SIMS = 50, 15, 50, 100_000
rng = np.random.default_rng(42)
means = rng.normal(MU, SIGMA, (SIMS, N)).mean(axis=1)
E = stats.norm.ppf(0.975) * SIGMA / np.sqrt(N)
low, high = means - E, means + E
hit = (low <= MU) & (MU <= high)
run = np.cumsum(hit) / np.arange(1, SIMS + 1)
assert hit[:100].sum() == 93 and round(run[999], 4) == 0.945 and round(run[-1], 4) == 0.9494   # the Note's table
SHOW = 100                                                       # intervals drawn in the top panel
YR = [low[:SHOW].min() - 1, high[:SHOW].max() + 1]
KS = list(range(1, 21)) + list(range(25, SHOW + 1, 5)) + [int(k) for k in np.unique(np.geomspace(150, SIMS, 22).round(-1))]


def frame(k):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.58, 0.42], vertical_spacing=0.16)
    m = min(k, SHOW)
    for ok, col, w in ((True, BLUE, 2.5), (False, RED, 5)):
        xs, ys = [], []
        for i in np.flatnonzero(hit[:m] == ok):
            xs += [i + 1, i + 1, None]
            ys += [low[i], high[i], None]
        fig.add_scatter(x=xs, y=ys, mode="lines", line=dict(color=col, width=w), showlegend=False, row=1, col=1)
    fig.add_scatter(x=np.arange(1, m + 1), y=means[:m], mode="markers", marker=dict(color="black", size=5),
                    showlegend=False, row=1, col=1)
    fig.add_hline(y=MU, line=dict(color="black", width=2.5, dash="dash"), opacity=1, row=1, col=1)
    fig.add_annotation(x=SHOW + 1, y=MU, text="μ = 50", xanchor="left", yshift=16, showarrow=False, font_size=22, row=1, col=1)
    # running coverage, log x so 1 to 100,000 fits
    idx = np.unique(np.geomspace(1, k, 400).astype(int))
    fig.add_scatter(x=idx, y=100 * run[idx - 1], mode="lines", line=dict(color=GREY, width=3),
                    showlegend=False, row=2, col=1)
    fig.add_scatter(x=[k], y=[100 * run[k - 1]], mode="markers", marker=dict(color="black", size=11),
                    showlegend=False, row=2, col=1)
    fig.add_hline(y=95, line=dict(color=BLUE, width=2.5, dash="dash"), opacity=1, row=2, col=1)
    fig.add_annotation(x=0, y=95, xref="x2 domain", text="95%", yshift=14, xanchor="left", showarrow=False,
                       font=dict(size=20, color=BLUE), row=2, col=1)
    fig.update_xaxes(range=[0, SHOW + 9], title_text="sample number" + (" (first 100 shown)" if k > SHOW else ""), row=1, col=1)
    fig.update_yaxes(range=YR, title_text="interval", row=1, col=1)
    fig.update_xaxes(type="log", dtick=1, range=[0, np.log10(SIMS) + 0.05], title_text="number of intervals (log scale)",
                     row=2, col=1)
    fig.update_yaxes(range=[85, 101], title_text="% containing μ", row=2, col=1)
    missed = k - hit[:k].sum()
    fig.update_layout(template="simple_white", width=900, height=820, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"<b>{k:,} intervals: {missed:,} miss μ, {100 * run[k - 1]:.2f}% contain it</b>",
                                 x=0.5, y=0.97), margin=dict(l=90, r=30, t=80, b=60))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".cov_frames"
    tmp.mkdir(exist_ok=True)
    for j, k in enumerate(KS):
        frame(k).write_image(tmp / f"{j:03d}.png")
    last = len(KS) - 1
    for j in range(last + 1, last + 13):                        # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "coverage_drop.gif")], check=True)
    keys = [Image.open(tmp / f"{KS.index(k):03d}.png").convert("RGB") for k in (5, 20, 100, KS[-1])]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "coverage_drop_frames.png")
    shutil.rmtree(tmp)
