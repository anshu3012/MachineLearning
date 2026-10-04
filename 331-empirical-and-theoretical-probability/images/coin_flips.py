"""A fair coin tossed up to 100,000 times in three runs (seeds 0, 1, 2 as in the Notebook). Left: the share of heads
after each toss (log x axis) grows run by run; right: run 1's heads and tails shares against the theoretical 0.5.
Idea after Seeing Theory, "Basic Probability: Chance Events" (Kunin et al., Brown University); our own data and code.
Run: python coin_flips.py  -> coin_flips.gif, coin_flips_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots
from PIL import Image

HERE = Path(__file__).parent
COLOURS = ["#4C78A8", "#F58518", "#54A24B"]
N = 100_000
steps = np.arange(1, N + 1)
tosses = [np.random.default_rng(seed).integers(0, 2, N) for seed in (0, 1, 2)]   # 1 = head
running = [t.cumsum() / steps for t in tosses]
keep = np.unique(np.concatenate([np.arange(1, 11), np.logspace(0, 5, 600).astype(int)])) - 1
assert all(abs(r[-1] - 0.5) < 0.01 for r in running)


def frame(n):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.68, 0.32], horizontal_spacing=0.1,
                        subplot_titles=["share of heads so far", "run 1"])
    idx = keep[keep < n]
    for i, (r, c) in enumerate(zip(running, COLOURS)):
        fig.add_scatter(x=steps[idx], y=r[idx], mode="lines+markers" if n <= 10 else "lines",
                        line=dict(color=c, width=3), marker=dict(size=8), name=f"run {i + 1}", row=1, col=1)
    fig.add_hline(y=0.5, line=dict(color="#6B6B6B", dash="dash", width=2), row=1, col=1)
    heads = tosses[0][:n].sum()
    fig.add_bar(x=["heads", "tails"], y=[heads / n, 1 - heads / n], marker_color=[COLOURS[0], "#BDBDBD"],
                text=[f"{heads:,}", f"{n - heads:,}"], textposition="inside", insidetextanchor="start", textfont_color="white", showlegend=False, row=1, col=2)
    fig.add_hline(y=0.5, line=dict(color="#6B6B6B", dash="dash", width=2), row=1, col=2)
    fig.add_annotation(x=5.05, y=0.5, xref="x", yref="y", text="theory 0.5", showarrow=False, yshift=-18,
                       xanchor="right", font_size=22, font_color="#6B6B6B")
    seq = " ".join("H" if t else "T" for t in tosses[0][:n]) if n <= 10 else ""
    title = f"after {n:,} toss{'es' if n > 1 else ''}" + (f":  {seq}" if seq else "")
    fig.update_xaxes(type="log", range=[0, 5.08], tickvals=[1, 10, 100, 1000, 10_000, 100_000],
                     ticktext=["1", "10", "100", "1k", "10k", "100k"], title_text="tosses (log scale)", row=1, col=1)
    fig.update_yaxes(range=[0, 1.08], dtick=0.25, row=1, col=1)
    fig.update_yaxes(range=[0, 1.08], showticklabels=False, row=1, col=2)
    fig.update_layout(template="simple_white", width=1000, height=560, font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text=title, x=0.5, y=0.97), legend=dict(orientation="h", x=0.34, xanchor="center",
                                                                         y=-0.25), margin=dict(l=60, r=20, t=110, b=40))
    fig.update_annotations(font_size=24, selector=dict(xref="paper"))
    return fig


SCHEDULE = [(n, 2) for n in range(1, 11)] + [(n, 1) for n in np.unique(np.logspace(1.1, 5, 26).astype(int))[:-1]] \
    + [(N, 12)]

if __name__ == "__main__":
    tmp = HERE / ".coin_frames"
    tmp.mkdir(exist_ok=True)
    k, keys = 0, {}
    for n, rep in SCHEDULE:
        frame(n).write_image(tmp / f"{k:03d}.png")
        keys[n] = k
        for _ in range(rep - 1):
            shutil.copy(tmp / f"{k:03d}.png", tmp / f"{k + 1:03d}.png")
            k += 1
        k += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "coin_flips.gif")], check=True)
    near = lambda m: keys[min(keys, key=lambda n: abs(n - m))]
    ims = [Image.open(tmp / f"{near(m):03d}.png").convert("RGB") for m in (10, 100, 1000, N)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "coin_flips_frames.png")
    shutil.rmtree(tmp)
