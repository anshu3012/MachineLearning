"""How the out-of-bag (OOB) score is computed (section 4), on the moons training data (375 observations):
25 fully grown trees, each on a bootstrap sample of 375 draws. For one training observation at a time, the
trees whose sample contains it are greyed out; the remaining trees (about a third) vote, and the vote is
checked against the true class. Doing this for all 375 observations gives the OOB score, shown next to the
test accuracy. Idea after StatQuest, "Random Forests Part 1" (run each out-of-bag sample through the trees
built without it); data and code are ours.
Run: python oob_votes.py -> oob_votes.gif, oob_votes_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import COLOURS, X_test, X_train, y_test, y_train  # noqa: E402  same data as the app

T = 25
bag = BaggingClassifier(DecisionTreeClassifier(), n_estimators=T, bootstrap=True, oob_score=True,
                        random_state=42).fit(X_train, y_train)
n = len(y_train)
drew = np.array([np.isin(np.arange(n), s) for s in bag.estimators_samples_])        # tree x observation
votes = np.array([t.predict(X_train) for t in bag.estimators_])                     # tree x observation
oob = ~drew
assert oob.sum(axis=0).min() > 0                                                     # every row has OOB trees
blue = (votes * oob).sum(axis=0) / oob.sum(axis=0)                                   # share of OOB votes for class 1
pred = (blue > 0.5).astype(int)
correct = pred == y_train
assert abs(correct.mean() - bag.oob_score_) < 1e-9, (correct.mean(), bag.oob_score_)
test_acc = bag.score(X_test, y_test)
print("OOB score", round(bag.oob_score_, 3), "test accuracy", round(test_acc, 3),
      "mean share of trees that miss a row", round(oob.mean(), 3))
right = np.flatnonzero(correct)
ROWS = [int(right[0]), int(right[1]), int(np.flatnonzero(~correct)[0])]              # two right, one wrong
NAME = {0: "orange", 1: "blue"}
FONT = dict(family="Latin Modern Roman", size=23, color="black")


def frame(step):
    """step 0..2: one observation each; step 3: the final score over all observations."""
    fig = make_subplots(1, 2, horizontal_spacing=0.06, column_widths=[0.48, 0.52],
                        subplot_titles=["training data", "the 25 trees"])
    fig.update_annotations(font_size=26)
    for cls in (0, 1):
        m = y_train == cls
        fig.add_trace(go.Scatter(x=X_train[m, 0], y=X_train[m, 1], mode="markers", showlegend=False,
                                 marker=dict(color=COLOURS[cls], size=8, opacity=0.55)), 1, 1)
    gx, gy = np.arange(T) % 5, 4 - np.arange(T) // 5
    if step < 3:
        i = ROWS[step]
        fig.add_trace(go.Scatter(x=[X_train[i, 0]], y=[X_train[i, 1]], mode="markers", showlegend=False,
                                 marker=dict(symbol="star", size=30, color=COLOURS[y_train[i]],
                                             line=dict(color="black", width=2.5))), 1, 1)
        col = ["#D9D9D9" if drew[t, i] else COLOURS[votes[t, i]] for t in range(T)]
        txt = ["saw it" if drew[t, i] else f"votes<br>{NAME[votes[t, i]]}" for t in range(T)]
        k, b = int(oob[:, i].sum()), int((votes[:, i] * oob[:, i]).sum())
        mark = "✓ right" if correct[i] else "✗ wrong"
        done = ROWS[:step + 1]
        title = f"Observation {step + 1} (star, true class {NAME[y_train[i]]})"
        foot = (f"{T - k} trees drew it (grey, no vote). {k} trees never saw it: {b} vote blue, {k - b} orange"
                f"<br><b>OOB prediction: {NAME[pred[i]]} {mark}</b> &nbsp;&nbsp; right so far: "
                f"{int(correct[done].sum())} of {len(done)}")
    else:
        col, txt = ["#555555"] * T, [f"tree<br>{t + 1}" for t in range(T)]
        title = "Repeat for all 375 training observations"
        foot = (f"<b>OOB score: {int(correct.sum())} of {n} right = {bag.oob_score_:.3f}</b>"
                f"<br>accuracy on the 125 test observations: {test_acc:.3f}")
    fig.add_trace(go.Scatter(x=gx, y=gy, mode="markers+text", showlegend=False, text=txt,
                             textfont=dict(size=15, color=["black" if c == "#D9D9D9" else "white" for c in col]),
                             marker=dict(symbol="square", size=74, color=col, line=dict(color="white", width=2))), 1, 2)
    fig.update_xaxes(visible=False, range=[-0.6, 4.6], row=1, col=2)
    fig.update_yaxes(visible=False, range=[-0.6, 4.6], row=1, col=2)
    fig.update_xaxes(title="x₁", row=1, col=1)
    fig.update_yaxes(title="x₂", row=1, col=1)
    fig.add_annotation(xref="paper", yref="paper", x=0.5, y=-0.2, yanchor="top", showarrow=False, text=foot,
                       font=dict(size=24))
    fig.update_layout(template="simple_white", width=1250, height=760, font=FONT,
                      title=dict(text=f"<b>{title}</b>", x=0.5, y=0.97, font_size=30),
                      margin=dict(l=70, r=20, t=110, b=190))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".oob_votes"
    tmp.mkdir(exist_ok=True)
    keys, k = [], 0
    for step, hold in zip(range(4), [5, 5, 5, 8]):
        png = tmp / f"{k:03d}.png"
        frame(step).write_image(png)
        keys.append(Image.open(png).convert("RGB"))
        for j in range(1, hold):
            shutil.copy(png, tmp / f"{k + j:03d}.png")
        k += hold
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=5,scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "oob_votes.gif")], check=True)
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, f in enumerate(keys):
        sheet.paste(f, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "oob_votes_frames.png")
    shutil.rmtree(tmp)
