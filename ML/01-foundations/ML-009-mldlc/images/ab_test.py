"""An A/B test, day by day, on SIMULATED visitors (no real data: the numbers are made up to show the method).
Each day 1,000 new visitors are sent at random to group A (the current model) or group B (the new model).
A visitor of A converts with probability 0.10, of B with probability 0.12. Dots: that day's conversion rate.
Lines: the rate over all days so far. The daily dots jump about; the running lines settle and separate.
Plotly frames -> ffmpeg GIF + _frames.png grid. Run: python ab_test.py -> ab_test.gif, ab_test_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=24)
DAYS, VISITORS, RATE = 14, 1000, {"A": 0.10, "B": 0.12}

rng = np.random.default_rng(0)
in_b = rng.random((DAYS, VISITORS)) < 0.5                       # random split, visitor by visitor
buys = rng.random((DAYS, VISITORS)) < np.where(in_b, RATE["B"], RATE["A"])
n = {"A": (~in_b).sum(1), "B": in_b.sum(1)}
k = {"A": (buys & ~in_b).sum(1), "B": (buys & in_b).sum(1)}
daily = {g: k[g] / n[g] * 100 for g in "AB"}
running = {g: k[g].cumsum() / n[g].cumsum() * 100 for g in "AB"}
days = np.arange(1, DAYS + 1)
print({g: (int(n[g].sum()), int(k[g].sum()), round(running[g][-1], 1)) for g in "AB"},
      "days on which A's daily rate beat B's:", int((daily["A"] > daily["B"]).sum()))
assert [round(running[g][-1], 1) for g in "AB"] == [10.2, 12.0]
COLOUR = {"A": BLUE, "B": ORANGE}
NAME = {"A": "A: current model", "B": "B: new model"}


def frame(d):                                                   # d = days seen so far
    fig = go.Figure()
    for g in "AB":
        fig.add_trace(go.Scatter(x=days[:d], y=daily[g][:d], mode="markers",
                                 marker=dict(color=COLOUR[g], size=11, opacity=0.45)))
        fig.add_trace(go.Scatter(x=days[:d], y=running[g][:d], mode="lines", line=dict(color=COLOUR[g], width=5)))
    order = sorted("AB", key=lambda g: running[g][d - 1])       # keep the two end labels apart
    for g, shift in zip(order, (-14, 14)):
        fig.add_annotation(x=days[d - 1], y=running[g][d - 1], text=f"<b>{NAME[g]}, {running[g][d - 1]:.1f}%</b>",
                           showarrow=False, xanchor="left", xshift=12, yshift=shift, font=dict(color=COLOUR[g], size=23))
    fig.update_xaxes(title="day of the test", range=[0.5, 19.5], tickvals=list(range(1, 15)))
    fig.update_yaxes(title="visitors who buy (%)", range=[6, 16])
    fig.update_layout(template="simple_white", width=1200, height=600, font=FONT, showlegend=False,
                      title=dict(text=f"Day {d}: dots = that day only, lines = all days so far", x=0.5, y=0.96),
                      margin=dict(l=90, r=20, t=80, b=80))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".ab_frames"
    tmp.mkdir(exist_ok=True)
    for d in days:
        frame(d).write_image(tmp / f"{d - 1:03d}.png")
    for j in range(DAYS, DAYS + 6):                             # hold the final frame
        shutil.copy(tmp / f"{DAYS - 1:03d}.png", tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "ab_test.gif")], check=True)
    keys = [Image.open(tmp / f"{j:03d}.png").convert("RGB") for j in (0, 3, 7, 13)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for j, im in enumerate(keys):
        sheet.paste(im, ((j % 2) * (w + 16), (j // 2) * (h + 16)))
    sheet.save(HERE / "ab_test_frames.png")
    shutil.rmtree(tmp)
