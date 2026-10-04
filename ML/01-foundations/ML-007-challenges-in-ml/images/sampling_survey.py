"""Sampling noise vs sampling bias on real data. Population: the 891 passengers of the Titanic training set
(data/titanic_train.csv); 38.4 percent survived. Each "survey" estimates that share from a sample:
- random: passengers drawn at random from everyone;
- biased: passengers drawn only from first class (as if we only asked people in the first-class lounge).
For each sample size we run 40 surveys of each kind (seed 0). Random surveys scatter widely when small (noise) and
close in on 38.4 percent as they grow; biased surveys close in on 63.0 percent, the wrong answer, however large.
Plotly frames -> ffmpeg GIF, plus the final frame for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
BLUE, RED, GREY = "#4C78A8", "#E45756", "#6B6B6B"
d = pd.read_csv(HERE.parent / "data" / "titanic_train.csv")
TRUE, FIRST = d.Survived.mean(), d[d.Pclass == 1].Survived.values
assert len(d) == 891 and round(100 * TRUE, 1) == 38.4 and round(100 * FIRST.mean(), 1) == 63.0
SIZES = [5, 10, 20, 50, 100, 200]
rng = np.random.default_rng(0)
RAND = {n: [100 * rng.choice(d.Survived.values, n, replace=False).mean() for _ in range(40)] for n in SIZES}
BIAS = {n: [100 * rng.choice(FIRST, n, replace=False).mean() for _ in range(40)] for n in SIZES}
spread = lambda v: np.std(v)
assert spread(RAND[5]) > 3 * spread(RAND[200]) and abs(np.mean(BIAS[200]) - 63.0) < 1.5


def frame(k):
    fig = go.Figure()
    fig.add_hline(y=100 * TRUE, line=dict(color="black", width=2.5, dash="dash"))
    fig.add_annotation(x=-0.45, y=100 * TRUE - 3.5, text="true share: 38.4%", showarrow=False, xanchor="left",
                       font=dict(size=18))
    jit = np.random.default_rng(1).uniform(-0.22, 0.22, 40)
    for i, n in enumerate(SIZES[:k + 1]):
        fig.add_scatter(x=i - 0.1 + 0.4 * jit, y=RAND[n], mode="markers", marker=dict(size=9, color=BLUE, opacity=0.7),
                        name="random sample of everyone", showlegend=i == 0)
        fig.add_scatter(x=i + 0.1 + 0.4 * jit, y=BIAS[n], mode="markers", marker=dict(size=9, color=RED, opacity=0.7,
                        symbol="diamond"), name="first-class passengers only", showlegend=i == 0)
    n = SIZES[k]
    fig.update_layout(template="simple_white", width=1100, height=720, font=FONT,
                      title=dict(text=f"40 surveys of {n} passengers each: random ones span "
                                      f"{min(RAND[n]):.0f}-{max(RAND[n]):.0f}%, biased ones average "
                                      f"{np.mean(BIAS[n]):.0f}%", x=0.5, y=0.95, font=dict(size=21)),
                      xaxis=dict(title="passengers asked in each survey", tickvals=list(range(len(SIZES))),
                                 ticktext=[str(s) for s in SIZES], range=[-0.5, len(SIZES) - 0.5]),
                      yaxis=dict(title="estimated share who survived (%)", range=[-3, 103]),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18),
                      margin=dict(l=90, r=30, t=80, b=140))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".ss_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for k in range(len(SIZES)):
        keys.append(tmp / f"k{k}.png")
        frame(k).write_image(keys[-1])
    seq = [k for k in range(len(SIZES)) for _ in range(3)] + [len(SIZES) - 1] * 5
    for j, k in enumerate(seq):
        shutil.copy(keys[k], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=820:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "sampling_survey.gif")], check=True)
    shutil.copy(keys[-1], HERE / "sampling_survey_frames.png")
    shutil.rmtree(tmp)
    for n in SIZES:
        print(n, round(min(RAND[n])), round(max(RAND[n])), round(np.mean(RAND[n]), 1), round(np.mean(BIAS[n]), 1),
              round(min(BIAS[n])), round(max(BIAS[n])))
