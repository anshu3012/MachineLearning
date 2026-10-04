"""A sample drawn from a population, one passenger at a time. Population: the 891 Titanic fares (mean mu = 32.20).
Top: every fare as a grey dot, the sampled ones in orange, with mu and the running sample mean x-bar.
Bottom: x-bar after each draw. x-bar wanders while the sample is small and is still not exactly mu at n = 100.
One random sample (seed 0), drawn without replacement.
Run: python sample_mean_walk.py -> sample_mean_walk.gif, sample_mean_walk_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#B0B0B0"
fare = pd.read_csv(HERE.parent / "data" / "titanic_train.csv")["Fare"].to_numpy()
mu = fare.mean()
rng = np.random.default_rng(0)
order = rng.choice(len(fare), 100, replace=False)
xbar = np.cumsum(fare[order]) / np.arange(1, 101)
jit = rng.uniform(-1, 1, len(fare))
assert abs(mu - 32.20) < 0.01
STEPS = list(range(1, 11)) + list(range(12, 31, 2)) + list(range(35, 101, 5))


def frame(n):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.45, 0.55], vertical_spacing=0.2,
                        subplot_titles=[f"Population: 891 fares · sample: {n} drawn",
                                        "Sample mean after each draw"])
    s = order[:n]
    fig.add_scatter(x=fare, y=jit, mode="markers", marker=dict(size=6, color=GREY, opacity=0.6), row=1, col=1)
    fig.add_scatter(x=fare[s], y=jit[s], mode="markers", marker=dict(size=11, color=ORANGE,
                    line=dict(color="white", width=1)), row=1, col=1)
    fig.add_scatter(x=fare[s[-1:]], y=jit[s[-1:]], mode="markers", marker=dict(size=20, color="rgba(0,0,0,0)",
                    line=dict(color="black", width=2)), row=1, col=1)
    fig.add_vline(x=mu, line=dict(color=BLUE, width=4, dash="dash"), opacity=1, layer="above", row=1, col=1)
    fig.add_vline(x=xbar[n - 1], line=dict(color=ORANGE, width=4), opacity=1, layer="above", row=1, col=1)
    fig.add_scatter(x=np.arange(1, n + 1), y=xbar[:n], mode="lines+markers", line=dict(color=ORANGE, width=3),
                    marker=dict(size=6), row=2, col=1)
    fig.add_hline(y=mu, line=dict(color=BLUE, width=3, dash="dash"), opacity=1, row=2, col=1)
    fig.add_annotation(x=1, y=1.6, xref="x domain", yref="y", xanchor="right", showarrow=False,
                       text=f"<span style='color:{BLUE}'>μ = {mu:.1f}</span>   "
                            f"<span style='color:{ORANGE}'>x̄ = {xbar[n - 1]:.1f}</span>", font=dict(size=24))
    fig.update_xaxes(range=[-5, 525], title_text="fare", row=1, col=1)
    fig.update_yaxes(range=[-1.4, 2.0], visible=False, row=1, col=1)
    fig.update_xaxes(range=[0, 101], title_text="sample size n", row=2, col=1)
    fig.update_yaxes(range=[0, 80], title_text="x̄", row=2, col=1)
    fig.update_annotations(selector=dict(xref="paper"), font_size=22)
    fig.update_layout(template="simple_white", width=900, height=760, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=20), margin=dict(l=70, r=30, t=60, b=60))
    return fig


if __name__ == "__main__":
    print("x-bar at n = 1, 3, 10, 30, 100:", np.round(xbar[[0, 2, 9, 29, 99]], 1), "mu:", round(mu, 2))
    tmp = HERE / ".walk_frames"
    tmp.mkdir(exist_ok=True)
    for i, n in enumerate(STEPS):
        frame(n).write_image(tmp / f"{i:03d}.png")
    last = len(STEPS) - 1
    for k in range(last + 1, last + 9):                      # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "sample_mean_walk.gif")], check=True)
    keys = [Image.open(tmp / f"{STEPS.index(n):03d}.png").convert("RGB") for n in (1, 3, 10, 100)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "sample_mean_walk_frames.png")
    shutil.rmtree(tmp)
