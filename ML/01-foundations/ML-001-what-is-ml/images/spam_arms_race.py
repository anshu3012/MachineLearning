"""Rules that keep changing, measured: a hand-written rule ("contains the word call -> spam") against a learned filter,
before and after spammers swap "call" for "ring". Data: the UCI SMS Spam Collection (data/sms_spam.tsv.gz), the same
1,000-message test set as spam_experience.py (134 of them spam); the swap is applied by us to every spam message.
Left: share of the test spam each filter catches. Right: the weight the learned filter gives the two words
(log of P(word | spam) / P(word | not spam) from Naive Bayes). Plotly frames -> ffmpeg GIF, plus a grid for the PDF."""
import re
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=28)
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#8A8A8A"
OLD, NEW = "call", "ring"

d = pd.read_csv(HERE.parent / "data" / "sms_spam.tsv.gz", sep="\t", header=None, names=["label", "text"], quoting=3)
y = (d.label == "spam").astype(int).values
Xtr, Xte, ytr, yte = train_test_split(d.text.to_numpy(dtype=object), y, test_size=1000, stratify=y, random_state=0)
assert yte.sum() == 134


def swap(X, labels):                                     # spammers replace the word in every spam message
    return np.array([re.sub(rf"\b{OLD}\b", NEW, t, flags=re.I) if l else t for t, l in zip(X, labels)], dtype=object)


def rule_catch(X):                                       # the hand-written rule
    return 100 * np.mean([bool(re.search(rf"\b{OLD}\b", t.lower())) for t in X[yte == 1]])


def fit(X):
    v = CountVectorizer()
    return v, MultinomialNB().fit(v.fit_transform(X), ytr)


def ml_catch(vm, X):
    return 100 * vm[1].predict(vm[0].transform(X))[yte == 1].mean()


def weight(vm, word):
    i = vm[0].vocabulary_[word]
    return vm[1].feature_log_prob_[1, i] - vm[1].feature_log_prob_[0, i]


Xte2, Xtr2 = swap(Xte, yte), swap(Xtr, ytr)
old, new = fit(Xtr), fit(Xtr2)
STAGES = [  # title, rule catch, ML catch, weight of OLD, weight of NEW
    ('1. Today: spam often says "call"', rule_catch(Xte), ml_catch(old, Xte), weight(old, OLD), weight(old, NEW)),
    ('2. Spammers write "ring" instead', rule_catch(Xte2), ml_catch(old, Xte2), weight(old, OLD), weight(old, NEW)),
    ("3. The filter retrains on new labelled messages", rule_catch(Xte2), ml_catch(new, Xte2), weight(new, OLD),
     weight(new, NEW)),
]
assert [round(s[1], 1) for s in STAGES] == [42.5, 0.0, 0.0], STAGES
assert [round(s[2], 1) for s in STAGES] == [88.1, 87.3, 91.0], STAGES
assert [round(s[3], 1) for s in STAGES] == [1.4, 1.4, -4.3] and [round(s[4], 1) for s in STAGES] == [-0.3, -0.3, 4.1]


def frame(k):
    title, rc, mc, wo, wn = STAGES[k]
    fig = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5], horizontal_spacing=0.16,
                        subplot_titles=["Spam caught (%)", "Learned weight of the word"])
    fig.add_bar(x=['hand rule:<br>"call" → spam', "learned<br>filter"], y=[rc, mc], marker_color=[GREY, BLUE],
                text=[f"<b>{rc:.1f}</b>", f"<b>{mc:.1f}</b>"], textposition="outside", row=1, col=1)
    fig.add_bar(x=['"call"', '"ring"'], y=[wo, wn], marker_color=[ORANGE if v > 0 else GREY for v in (wo, wn)],
                text=[f"<b>{wo:+.1f}</b>", f"<b>{wn:+.1f}</b>"], textposition="outside", row=1, col=2)
    fig.add_hline(y=0, line=dict(color="black", width=1.5), row=1, col=2)
    fig.add_annotation(x=0.5, y=6.6, xref="x2", yref="y2", text="above 0: a sign of spam", showarrow=False,
                       font=dict(size=24, color=ORANGE))
    fig.update_yaxes(range=[0, 112], row=1, col=1)
    fig.update_yaxes(range=[-6, 7.2], row=1, col=2)
    fig.update_annotations(font=dict(family="Latin Modern Roman", size=28))
    fig.update_layout(template="simple_white", width=1100, height=760, font=FONT, showlegend=False,
                      title=dict(text=f"<b>{title}</b>", x=0.5, y=0.96, font=dict(size=34)),
                      margin=dict(l=70, r=30, t=130, b=90))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".ar_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for k in range(3):
        keys.append(tmp / f"k{k}.png")
        frame(k).write_image(keys[-1])
    for j, k in enumerate([0] * 3 + [1] * 3 + [2] * 5):
        shutil.copy(keys[k], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=820:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "spam_arms_race.gif")], check=True)
    ims = [Image.open(k).convert("RGB") for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")          # 2 x 2 grid: readable at page width
    for i, im in enumerate(ims):
        sheet.paste(im, (i % 2 * (w + 16), i // 2 * (h + 16)))
    sheet.save(HERE / "spam_arms_race_frames.png")
    shutil.rmtree(tmp)
