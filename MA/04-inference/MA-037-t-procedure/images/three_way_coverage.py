"""Three 95% intervals from the same samples of n = 10 from N(50, 15^2) (seed 42, as z_vs_t_coverage.py):
z with the true sigma, z with the sample's s (the tempting shortcut), and t with s. Intervals arrive in batches;
each panel title keeps a running count of how many contain mu. Coverage over 100,000 samples is in the last frame.
Run: python three_way_coverage.py -> three_way_coverage.gif, three_way_coverage_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, RED = "#4C78A8", "#F58518", "#E45756"
MU, SIGMA, N = 50, 15, 10
Z, T = stats.norm.ppf(0.975), stats.t.ppf(0.975, N - 1)


def intervals(sims, seed=42):
    x = np.random.default_rng(seed).normal(MU, SIGMA, (sims, N))
    m, s = x.mean(axis=1), x.std(axis=1, ddof=1)
    return {"z with σ": (m - Z * SIGMA / np.sqrt(N), m + Z * SIGMA / np.sqrt(N)),
            "z with s": (m - Z * s / np.sqrt(N), m + Z * s / np.sqrt(N)),
            "t with s": (m - T * s / np.sqrt(N), m + T * s / np.sqrt(N))}


big = {k: np.mean((lo <= MU) & (MU <= hi)) for k, (lo, hi) in intervals(100_000).items()}
print({k: round(v, 4) for k, v in big.items()})
assert big["z with s"] < 0.93 < 0.94 < big["t with s"] and big["z with σ"] > 0.94
SHOW = intervals(100)
STEPS = [5, 10, 20, 35, 50, 70, 100]


def frame(k, final=False):
    titles = []
    for name, (lo, hi) in SHOW.items():
        hit = (lo[:k] <= MU) & (MU <= hi[:k])
        titles.append(f"{name}: {hit.sum()} of {k} contain μ" if not final else
                      f"{name}: {big[name]:.1%} of 100,000")
    fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.04, shared_yaxes=True, subplot_titles=titles)
    for col, (name, (lo, hi)) in enumerate(SHOW.items(), start=1):
        hit = (lo <= MU) & (MU <= hi)
        for ok, colour in [(True, BLUE), (False, ORANGE)]:
            xs, ys = [], []
            for i in np.flatnonzero(hit[:k] == ok):
                xs += [i + 1, i + 1, None]
                ys += [lo[i], hi[i], None]
            fig.add_scatter(x=xs, y=ys, mode="lines", line=dict(color=colour, width=2.5 if ok else 4), row=1, col=col,
                            showlegend=False)
        fig.add_hline(y=MU, line=dict(color=RED, width=3), opacity=1, layer="above", row=1, col=col)
        fig.update_xaxes(title_text="sample number", range=[0, 101], row=1, col=col)
    fig.update_yaxes(title_text="95% interval", row=1, col=1)
    fig.update_yaxes(range=[20, 80])
    fig.update_layout(template="simple_white", width=1200, height=520, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text="the same samples of n = 10, three ways to build a 95% interval"
                                      + ("<br><sup>orange: misses μ = 50</sup>"), x=0.5),
                      margin=dict(l=70, r=20, t=120, b=55))
    fig.update_annotations(font_size=21)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".tw_frames"
    tmp.mkdir(exist_ok=True)
    f, keys = 0, []
    for k in STEPS:
        frame(k).write_image(tmp / f"{f:03d}.png")
        keys.append(tmp / f"{f:03d}.png")
        f += 1
        shutil.copy(tmp / f"{f - 1:03d}.png", tmp / f"{f:03d}.png")
        f += 1
    frame(100, final=True).write_image(tmp / "final.png")
    for _ in range(8):
        shutil.copy(tmp / "final.png", tmp / f"{f:03d}.png")
        f += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=840:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "three_way_coverage.gif")], check=True)
    grid = [Image.open(p).convert("RGB") for p in (keys[1], keys[4], keys[-1], tmp / "final.png")]
    w, h = grid[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(grid):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "three_way_coverage_frames.png")
    shutil.rmtree(tmp)
