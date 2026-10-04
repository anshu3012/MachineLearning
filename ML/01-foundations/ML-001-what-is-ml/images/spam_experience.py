"""Mitchell's definition on real data: a spam filter's performance P (share of test messages sorted correctly) improves
with its experience E (number of labelled messages it has learned from). Data: the UCI SMS Spam Collection
(data/sms_spam.tsv.gz, Almeida et al. 2011), 5,574 text messages labelled spam or not spam. A fixed test set of
1,000 messages; for each training size, the mean accuracy of a Naive Bayes filter over 20 random training sets.
Plotly frames -> ffmpeg GIF, plus the final frame for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#8A8A8A"
SIZES = [10, 20, 50, 100, 200, 500, 1000, 2000, 4574]

d = pd.read_csv(HERE.parent / "data" / "sms_spam.tsv.gz", sep="\t", header=None, names=["label", "text"], quoting=3)
y = (d.label == "spam").astype(int).values
assert len(d) == 5574 and y.sum() == 747
Xtr, Xte, ytr, yte = train_test_split(d.text.to_numpy(dtype=object), y, test_size=1000, stratify=y, random_state=0)
BASE = 1 - yte.mean()                                   # a filter that calls every message "not spam"


def accuracy(n):
    accs = []
    for s in range(20):
        idx = np.random.default_rng(s).permutation(len(Xtr))[:n]
        if ytr[idx].min() == ytr[idx].max():            # no spam seen yet: it can only say "not spam"
            accs.append(BASE)
            continue
        v = CountVectorizer()
        m = MultinomialNB().fit(v.fit_transform(Xtr[idx]), ytr[idx])
        accs.append((m.predict(v.transform(Xte)) == yte).mean())
    return 100 * np.mean(accs)


ACC = [accuracy(n) for n in SIZES]
assert round(ACC[0], 1) == 86.9 and round(ACC[3], 1) == 93.8 and round(ACC[-1], 1) == 98.1, ACC


def frame(k):
    fig = go.Figure()
    fig.add_hline(y=100 * BASE, line=dict(color=GREY, dash="dash", width=2.5), layer="above")
    fig.add_annotation(x=np.log10(2500), y=100 * BASE - 0.6, text='always says "not spam": 86.6%', showarrow=False,
                       font=dict(size=18, color=GREY))
    fig.add_scatter(x=SIZES[:k + 1], y=ACC[:k + 1], mode="lines+markers", line=dict(color=BLUE, width=4),
                    marker=dict(size=14, color=BLUE), showlegend=False)
    fig.add_scatter(x=[SIZES[k]], y=[ACC[k]], mode="markers+text", marker=dict(size=22, color=ORANGE),
                    text=[f"<b>{ACC[k]:.1f}%</b>"], textposition="top left", textfont=dict(size=22, color=ORANGE),
                    showlegend=False)
    fig.update_layout(template="simple_white", width=1000, height=700, font=FONT,
                      title=dict(text=f"Experience E: <b>{SIZES[k]:,}</b> labelled messages<br>"
                                      f"Performance P: <b>{ACC[k]:.1f}%</b> of test messages sorted correctly",
                                 x=0.5, y=0.95),
                      xaxis=dict(type="log", title="E: labelled messages learned from (log scale)",
                                 tickvals=SIZES, ticktext=[f"{s:,}" for s in SIZES], range=[0.85, 3.8]),
                      yaxis=dict(title="P: test messages sorted correctly (%)", range=[85, 100]),
                      margin=dict(l=90, r=30, t=120, b=90))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".se_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for k in range(len(SIZES)):
        keys.append(tmp / f"k{k}.png")
        frame(k).write_image(keys[-1])
    seq = [k for k in range(len(SIZES)) for _ in range(2)] + [len(SIZES) - 1] * 6
    for j, k in enumerate(seq):
        shutil.copy(keys[k], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "spam_experience.gif")], check=True)
    shutil.copy(keys[-1], HERE / "spam_experience_frames.png")
    shutil.rmtree(tmp)
