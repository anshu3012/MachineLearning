"""The bootstrap confidence interval, step by step, on 12 random Titanic ages (seed 12).
Top: the 12 ages (grey) and one resample of 12 drawn from them with replacement (orange; a value drawn twice
is stacked). Bottom: the means of all resamples so far. At the end the 2.5th and 97.5th percentiles of 10,000
bootstrap means mark the 95% interval, drawn beside the t-interval of the same sample.
Run: python bootstrap_ci.py -> bootstrap_ci.gif, bootstrap_ci_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
ages = pd.read_csv(HERE.parent / "data" / "titanic_train.csv")["Age"].dropna().to_numpy()
x = np.random.default_rng(12).choice(ages, 12, replace=False)
B = 10_000
idx = np.random.default_rng(0).integers(0, 12, size=(B, 12))
boot = x[idx].mean(axis=1)
lo, hi = np.percentile(boot, [2.5, 97.5])
tlo, thi = stats.t.interval(0.95, 11, loc=x.mean(), scale=x.std(ddof=1) / np.sqrt(12))
print(f"ages {x.tolist()} mean {x.mean():.2f} s {x.std(ddof=1):.2f}; bootstrap 95%: {lo:.2f} to {hi:.2f}; "
      f"t-interval {tlo:.2f} to {thi:.2f}; population mean {ages.mean():.2f}")
assert lo < ages.mean() < hi
EDGES = np.arange(10, 50.5, 1)
STEPS = [1, 2, 3, 4, 5, 20, 100, 1000, B]


def frame(k, final=False):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.38, 0.62], vertical_spacing=0.16,
                        subplot_titles=("the 12 ages (grey) and resample number %d (orange)" % k,
                                        "means of %s resample%s" % (f"{k:,}", "s" if k > 1 else "")))
    fig.add_scatter(x=x, y=np.zeros(12), mode="markers", marker=dict(color=GREY, size=13), row=1, col=1,
                    showlegend=False)
    pick = np.sort(x[idx[k - 1]])
    level = np.array([np.sum(pick[:i] == v) for i, v in enumerate(pick)]) + 1      # stack repeated values
    fig.add_scatter(x=pick, y=level, mode="markers", marker=dict(color=ORANGE, size=13), row=1, col=1,
                    showlegend=False)
    m = boot[k - 1]
    fig.add_scatter(x=[m, m], y=[-0.6, 5.1], mode="lines", line=dict(color=ORANGE, width=3, dash="dot"), row=1, col=1,
                    showlegend=False)
    fig.add_annotation(x=m, y=5.6, text=f"mean {m:.1f}", showarrow=False, font=dict(color=ORANGE, size=19), row=1, col=1)
    counts, _ = np.histogram(boot[:k], bins=EDGES)
    fig.add_bar(x=EDGES[:-1] + 0.5, y=counts, width=1, marker=dict(color=BLUE, line=dict(color="white", width=0.5)),
                row=2, col=1, showlegend=False)
    top = max(counts.max(), 1)
    if final:
        for v in (lo, hi):
            fig.add_scatter(x=[v, v], y=[0, top * 1.05], mode="lines", line=dict(color=GREEN, width=4), row=2, col=1,
                            showlegend=False)
        fig.add_scatter(x=[lo, hi], y=[top * 1.2] * 2, mode="lines+markers", line=dict(color=GREEN, width=6),
                        marker=dict(symbol="line-ns-open", size=16, color=GREEN), row=2, col=1, showlegend=False)
        fig.add_annotation(x=hi, y=top * 1.2, xanchor="left", xshift=10, showarrow=False, row=2, col=1,
                           text=f"bootstrap 95%: {lo:.1f} to {hi:.1f}", font=dict(color=GREEN, size=19))
        fig.add_scatter(x=[tlo, thi], y=[top * 1.42] * 2, mode="lines+markers", line=dict(color="black", width=6),
                        marker=dict(symbol="line-ns-open", size=16, color="black"), row=2, col=1, showlegend=False)
        fig.add_annotation(x=thi, y=top * 1.42, xanchor="left", xshift=10, showarrow=False, row=2, col=1,
                           text=f"t-interval: {tlo:.1f} to {thi:.1f}", font=dict(size=19))
    fig.update_yaxes(visible=False, range=[-0.8, 6.2], row=1, col=1)
    fig.update_yaxes(title_text="count", range=[0, top * 1.6], row=2, col=1)
    fig.update_xaxes(range=[8, 62], dtick=5, row=1, col=1)
    fig.update_xaxes(range=[8, 62], dtick=5, title_text="age (years)", row=2, col=1)
    fig.update_layout(template="simple_white", width=1000, height=680, bargap=0,
                      font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text="Bootstrap: resample the sample, keep each mean" if not final else
                                 "The middle 95% of the bootstrap means is the interval", x=0.5),
                      margin=dict(l=70, r=30, t=110, b=55))
    fig.update_annotations(font_size=20)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".boot_frames"
    tmp.mkdir(exist_ok=True)
    keys, f = {}, 0
    for k in STEPS:
        fig = frame(k)
        fig.write_image(tmp / f"{f:03d}.png")
        keys[k] = tmp / f"{f:03d}.png"
        f += 1
        for _ in range(1 if k < 20 else 2):
            shutil.copy(tmp / f"{f - 1:03d}.png", tmp / f"{f:03d}.png")
            f += 1
    frame(B, final=True).write_image(tmp / "final.png")
    for _ in range(8):
        shutil.copy(tmp / "final.png", tmp / f"{f:03d}.png")
        f += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "bootstrap_ci.gif")], check=True)
    grid = [Image.open(p).convert("RGB") for p in (keys[1], keys[2], keys[100], tmp / "final.png")]
    w, h = grid[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(grid):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "bootstrap_ci_frames.png")
    shutil.rmtree(tmp)
