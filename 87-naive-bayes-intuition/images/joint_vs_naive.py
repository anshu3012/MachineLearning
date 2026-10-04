"""Why Naive Bayes splits the likelihood (Plotly), on the 8-match table.
joint_filter.gif: keep only matches that agree with the new match on toss, then venue, then outlook, per class.
  No winning match survives, so the exact joint likelihood P(lost, Mumbai, sunny | win) is 0.
naive_split.png: the naive way counts each feature on its own over all matches of the class: 1/5, 2/5, 4/5 and 2/3, 2/3, 1/3."""
import shutil
import subprocess
from fractions import Fraction as F
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
df = pd.read_csv(HERE.parent / "data" / "matches.csv")
df.index = range(1, len(df) + 1)
q = dict(toss="lost", venue="Mumbai", outlook="sunny")
feats = list(q)
GREEN, RED, LIGHT_G, LIGHT_R, GREY, HILITE = "#54A24B", "#E45756", "#DDEFD9", "#F9DCDC", "#F2F2F2", "#F58518"
CLS = {"win": (GREEN, LIGHT_G), "loss": (RED, LIGHT_R)}

# joint filter: survivors after each condition
survivors = {}
for cls in CLS:
    sub, steps = df[df.result == cls], []
    steps.append(sub)
    for f in feats:
        sub = sub[sub[f] == q[f]]
        steps.append(sub)
    survivors[cls] = steps
assert [len(s) for s in survivors["win"]] == [5, 1, 0, 0]
assert [len(s) for s in survivors["loss"]] == [3, 2, 1, 1]
# naive factors (the Note's section 7)
naive = {c: [F(int((df[df.result == c][f] == q[f]).sum()), int((df.result == c).sum())) for f in feats] for c in CLS}
assert naive["win"] == [F(1, 5), F(2, 5), F(4, 5)] and naive["loss"] == [F(2, 3), F(2, 3), F(1, 3)]

FONT = dict(family="Latin Modern Roman", size=22)
cond_text = ["", "step 1: keep toss = lost", "step 2: also venue = Mumbai", ""]


def table(cls, k):
    """Table of one class's matches; rows that fail the first k conditions greyed, matching cells orange."""
    sub = df[df.result == cls]
    alive = set(survivors[cls][k].index)
    fills, fonts = [], []
    for col in ["match"] + feats:
        fc, tc = [], []
        for i, row in sub.iterrows():
            live = i in alive
            j = feats.index(col) if col in feats else -1
            if live and 0 <= j < k and row[col] == q[col]:
                fc.append(HILITE); tc.append("white")
            else:
                fc.append(CLS[cls][1] if live else GREY); tc.append("black" if live else "#BBBBBB")
        fills.append(fc); fonts.append(tc)
    cells = [list(sub.index)] + [list(sub[f]) for f in feats]
    return go.Table(columnwidth=[0.6, 1, 1.2, 1.2],
                    header=dict(values=["match"] + feats, fill_color=CLS[cls][0], font=dict(color="white", **FONT),
                                height=44),
                    cells=dict(values=cells, fill_color=fills, font=dict(color=fonts, **FONT), height=42))


def frame(k):
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "table"}, {"type": "table"}]], horizontal_spacing=0.05,
                        subplot_titles=[f"{c}: {len(survivors[c][k])} of {len(survivors[c][0])} left"
                                        for c in CLS])
    for j, cls in enumerate(CLS):
        fig.add_trace(table(cls, k), 1, j + 1)
    title = cond_text[k] if k else "New match: lost, Mumbai, sunny. Which past matches agree?"
    if k == 3:
        title = "step 3: also outlook = sunny. Win: 0 of 5 agree"
    fig.update_layout(width=1200, height=470, font=FONT, title=dict(text=title, x=0.5, y=0.95, font_size=28),
                      margin=dict(l=20, r=20, t=120, b=0))
    fig.update_annotations(font_size=26)
    return fig


def naive_fig():
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "table"}, {"type": "table"}]], horizontal_spacing=0.05,
                        subplot_titles=[" × ".join(f"{v.numerator}/{v.denominator}" for v in naive[c]) +
                                        f"  (×{(df.result == c).sum()}/8 prior)" for c in CLS])
    for j, cls in enumerate(CLS):
        sub = df[df.result == cls]
        cells = [list(sub.index) + ["count"]] + [list(sub[f]) + [f"{naive[cls][i].numerator}/{len(sub)}"]
                                                 for i, f in enumerate(feats)]
        fills = [[CLS[cls][1]] * len(sub) + ["white"]] + \
                [[HILITE if v == q[f] else CLS[cls][1] for v in sub[f]] + ["white"] for f in feats]
        fonts = [["black"] * (len(sub) + 1)] + [["white" if v == q[f] else "black" for v in sub[f]] + ["black"]
                                                 for f in feats]
        fig.add_trace(go.Table(columnwidth=[0.6, 1, 1.2, 1.2],
                               header=dict(values=["match"] + [f"{f} = {q[f]}?" for f in feats],
                                           fill_color=CLS[cls][0], font=dict(color="white", **FONT), height=44),
                               cells=dict(values=cells, fill_color=fills, font=dict(color=fonts, **FONT), height=42)),
                      1, j + 1)
    fig.update_layout(width=1300, height=520, font=FONT, margin=dict(l=20, r=20, t=140, b=10),
                      title=dict(text="Naive: count each feature on its own, over every match of the class",
                                 x=0.5, y=0.95, font_size=28))
    fig.update_annotations(font_size=26)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".joint_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(4):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(4, 7):                                      # hold the last frame
        shutil.copy(tmp / "003.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "0.8", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=10,scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "joint_filter.gif")], check=True)
    shutil.copy(tmp / "003.png", HERE / "joint_filter_frames.png")   # last frame alone: a 2x2 grid is unreadable in the PDF
    shutil.rmtree(tmp)
    naive_fig().write_image(HERE / "naive_split.png", scale=2)
