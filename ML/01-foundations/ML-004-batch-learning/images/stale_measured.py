"""A batch model going stale, measured. Data: the Electricity dataset (ELEC2, Harries 1999; OpenML 151), 45,312
half-hour records of the New South Wales electricity market, 1996 to 1998. Target: does the price go UP or DOWN
relative to the last 24 hours. Features: time of day, NSW price and demand, Victoria price and demand, transfer.
A logistic regression is trained on the first 4 weeks. One copy is never retrained; the other is retrained from
scratch on all data so far, every 4 weeks. Each is scored on every following week (accuracy).
Plotly frames -> ffmpeg GIF, plus the final frame for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LogisticRegression

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
ORANGE, BLUE, GREY = "#F58518", "#4C78A8", "#8A8A8A"
FEAT = ["period", "nswprice", "nswdemand", "vicprice", "vicdemand", "transfer"]

df = pd.read_csv(HERE.parent / "data" / "elec2.csv.gz")
assert len(df) == 45312
X, y = df[FEAT].values, df.up.values
week = np.arange(len(df)) // (48 * 7)
FIRST, LAST = 4, 133                                    # train on weeks 0-3; score weeks 4-133 (the full weeks)


def run(every):
    """Accuracy on each week from FIRST on. every=None: trained once, never retrained."""
    acc = []
    for w in range(FIRST, LAST + 1):
        if w == FIRST or (every and (w - FIRST) % every == 0):
            m = LogisticRegression(max_iter=1000).fit(X[week < w], y[week < w])
        acc.append((m.predict(X[week == w]) == y[week == w]).mean())
    return 100 * np.array(acc)


never, every4 = run(None), run(4)
MEANS = {"never": never.mean(), 13: run(13).mean(), 4: every4.mean(), 1: run(1).mean()}
assert MEANS["never"] < MEANS[13] < MEANS[4] < MEANS[1], MEANS
weeks = np.arange(FIRST, LAST + 1)
smooth = lambda a: pd.Series(a).rolling(8, min_periods=1).mean().values   # 8-week moving average
S_NEVER, S_EVERY = smooth(never), smooth(every4)
CUTS = [8, 26, 52, 78, 104, len(weeks)]


def frame(k):
    n = CUTS[k]
    fig = go.Figure()
    fig.add_scatter(x=weeks[:n], y=S_EVERY[:n], mode="lines", line=dict(color=BLUE, width=4),
                    name="retrained every 4 weeks")
    fig.add_scatter(x=weeks[:n], y=S_NEVER[:n], mode="lines", line=dict(color=ORANGE, width=4),
                    name="trained once, never retrained")
    gap = (every4[:n] - never[:n]).mean()
    fig.update_layout(template="simple_white", width=1100, height=680, font=FONT,
                      title=dict(text=f"Week {weeks[n - 1]}: the retrained model is ahead by "
                                      f"<b>{gap:.1f}</b> points on average", x=0.5, y=0.95),
                      xaxis=dict(title="week since the data begins (May 1996)", range=[0, 136]),
                      yaxis=dict(title="accuracy on that week (%), 8-week average", range=[50, 90]),
                      legend=dict(x=0.06, y=0.04, bgcolor="rgba(255,255,255,0.8)"),
                      margin=dict(l=90, r=30, t=80, b=80))
    fig.add_vrect(x0=0, x1=FIRST, fillcolor=GREY, opacity=0.15, line_width=0)
    fig.add_annotation(x=FIRST + 1, y=88, text="grey: first training (weeks 0 to 3)", showarrow=False, xanchor="left", font=dict(size=16, color=GREY))
    return fig


if __name__ == "__main__":
    print({k: round(v, 1) for k, v in MEANS.items()})
    tmp = HERE / ".sm_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for k in range(len(CUTS)):
        keys.append(tmp / f"k{k}.png")
        frame(k).write_image(keys[-1])
    seq = [k for k in range(len(CUTS)) for _ in range(2)] + [len(CUTS) - 1] * 5
    for j, k in enumerate(seq):
        shutil.copy(keys[k], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=820:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "stale_measured.gif")], check=True)
    shutil.copy(keys[-1], HERE / "stale_measured_frames.png")
    shutil.rmtree(tmp)
