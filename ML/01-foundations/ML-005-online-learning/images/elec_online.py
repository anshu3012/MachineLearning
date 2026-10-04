"""Online vs batch learning on a problem that keeps changing. Data: the Electricity dataset (ELEC2, Harries 1999;
OpenML 151), 45,312 half-hour records of the New South Wales market, 1996 to 1998; target: price UP or DOWN
relative to the last 24 hours. Both models start from the first 4 weeks.
- frozen batch: logistic regression trained once, never retrained;
- batch, retrained every 4 weeks from scratch on all data so far;
- online: scikit-learn's SGDClassifier (log loss, default settings). Each day it first predicts that day, then
  learns from it with partial_fit.
Outputs: elec_online.gif (+ _frames.png), the frozen and online models week by week (Plotly frames -> ffmpeg), and
elec_cost.png, accuracy against training work for the three models (Plotly)."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LogisticRegression, SGDClassifier

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
ORANGE, BLUE, GREEN, GREY = "#F58518", "#4C78A8", "#54A24B", "#8A8A8A"
FEAT = ["period", "nswprice", "nswdemand", "vicprice", "vicdemand", "transfer"]

df = pd.read_csv(HERE.parent / "data" / "elec2.csv.gz")
assert len(df) == 45312
X, y = df[FEAT].values, df.up.values
day, week = np.arange(len(df)) // 48, np.arange(len(df)) // 336
FIRST, LAST = 4, 133
first = week < FIRST


def batch(every):
    acc, work = [], 0
    for w in range(FIRST, LAST + 1):
        if w == FIRST or (every and (w - FIRST) % every == 0):
            m = LogisticRegression(max_iter=1000).fit(X[week < w], y[week < w])
            work += int((week < w).sum())               # every retrain reads all the data so far
        acc.append((m.predict(X[week == w]) == y[week == w]).mean())
    return 100 * np.array(acc), work


def online():
    m = SGDClassifier(loss="log_loss", random_state=0)
    m.partial_fit(X[first], y[first], classes=[0, 1])
    for _ in range(20):                                  # 21 passes over the first 4 weeks
        m.partial_fit(X[first], y[first])
    work, acc = 21 * int(first.sum()), []
    for w in range(FIRST, LAST + 1):
        right = 0
        for d in range(7 * w, 7 * w + 7):
            s = day == d
            right += (m.predict(X[s]) == y[s]).sum()    # predict the day first ...
            m.partial_fit(X[s], y[s])                    # ... then learn from it
            work += int(s.sum())
        acc.append(right / (week == w).sum())
    return 100 * np.array(acc), work


(frozen, w_frozen), (every4, w_every4), (onl, w_onl) = batch(None), batch(4), online()
M = dict(frozen=frozen.mean(), every4=every4.mean(), online=onl.mean())
assert round(M["frozen"], 1) == 68.0 and round(M["every4"], 1) == 73.3 and round(M["online"], 1) == 71.7, M
assert (w_frozen, w_every4, w_onl) == (1344, 753984, 71904), (w_frozen, w_every4, w_onl)
weeks = np.arange(FIRST, LAST + 1)
smooth = lambda a: pd.Series(a).rolling(8, min_periods=1).mean().values
S_F, S_O = smooth(frozen), smooth(onl)
CUTS = [8, 26, 52, 78, 104, len(weeks)]


def frame(k):
    n = CUTS[k]
    fig = go.Figure()
    fig.add_scatter(x=weeks[:n], y=S_O[:n], mode="lines", line=dict(color=GREEN, width=4),
                    name="online: learns from every day")
    fig.add_scatter(x=weeks[:n], y=S_F[:n], mode="lines", line=dict(color=ORANGE, width=4),
                    name="batch: trained once, never retrained")
    gap = (onl[:n] - frozen[:n]).mean()
    fig.add_vrect(x0=0, x1=FIRST, fillcolor=GREY, opacity=0.15, line_width=0)
    fig.add_annotation(x=FIRST + 1, y=88, text="grey: first training (weeks 0 to 3)", showarrow=False,
                       xanchor="left", font=dict(size=16, color=GREY))
    fig.update_layout(template="simple_white", width=1100, height=680, font=FONT,
                      title=dict(text=f"Week {weeks[n - 1]}: the online model is ahead by <b>{gap:.1f}</b> points"
                                      " on average", x=0.5, y=0.95),
                      xaxis=dict(title="week since the data begins (May 1996)", range=[0, 136]),
                      yaxis=dict(title="accuracy on that week (%), 8-week average", range=[50, 90]),
                      legend=dict(x=0.06, y=0.04, bgcolor="rgba(255,255,255,0.8)"),
                      margin=dict(l=90, r=30, t=80, b=80))
    return fig


def cost_figure():
    names = ["batch, never<br>retrained", "batch, retrained<br>every 4 weeks", "online,<br>every day"]
    accs, works = [M["frozen"], M["every4"], M["online"]], [w_frozen, w_every4, w_onl]
    cols = [ORANGE, BLUE, GREEN]
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.16,
                        subplot_titles=("Average weekly accuracy (%)", "Records fed to training (thousands)"))
    fig.add_bar(x=names, y=accs, marker_color=cols, text=[f"{a:.1f}" for a in accs], textposition="outside",
                showlegend=False, row=1, col=1)
    fig.add_bar(x=names, y=[w / 1e3 for w in works], marker_color=cols, text=[f"{w / 1e3:,.0f}" for w in works],
                textposition="outside", showlegend=False, row=1, col=2)
    fig.update_yaxes(range=[50, 80], row=1, col=1)
    fig.update_yaxes(range=[0, 1.15 * w_every4 / 1e3], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=600, font=dict(family="Latin Modern Roman", size=19),
                      margin=dict(l=60, r=30, t=70, b=100))
    for a in fig.layout.annotations:
        a.font.size = 22
    return fig


if __name__ == "__main__":
    print({k: round(v, 1) for k, v in M.items()}, w_frozen, w_every4, w_onl)
    cost_figure().write_image(HERE / "elec_cost.png", scale=2)
    tmp = HERE / ".eo_frames"
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
                    str(HERE / "elec_online.gif")], check=True)
    shutil.copy(keys[-1], HERE / "elec_online_frames.png")
    shutil.rmtree(tmp)
