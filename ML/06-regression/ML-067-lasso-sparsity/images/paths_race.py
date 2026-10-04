"""Ridge and Lasso coefficient paths on the 10-feature diabetes data, drawn as the penalty λ grows.
Same split as the Lasso Note (test size 0.2, random state 2). The λ axis is the Note's: loss = squared error + penalty,
so scikit-learn's Ridge alpha = λ and Lasso alpha = λ / n (Lasso divides the squared error by 2n).
Ridge shrinks much faster on these scaled features, so its panel uses λ from 0.01 to 1000 and Lasso's from 0.1 to 10000.
Run: python paths_race.py  -> paths_race.gif, paths_race_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
import warnings
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Lasso, Ridge
from sklearn.model_selection import train_test_split

warnings.simplefilter("ignore")
HERE = Path(__file__).parent
d = load_diabetes()
names = d.feature_names
Xtr, _, ytr, _ = train_test_split(d.data, d.target, test_size=0.2, random_state=2)
n = len(ytr)
lams = np.logspace(-1, 4, 61)                                  # Ridge shrinks faster here, so each panel gets its own λ range
rlams = np.logspace(-2, 3, 61)
R = np.array([Ridge(alpha=l).fit(Xtr, ytr).coef_ for l in rlams])
L = np.array([Lasso(alpha=l / n, max_iter=200000).fit(Xtr, ytr).coef_ for l in lams])
zl, zr = (L == 0).sum(1), (R == 0).sum(1)
assert zr.max() == 0 and zl[-1] == 10 and zl[0] == 0          # the lesson: Ridge never 0, Lasso ends all 0
print("lasso zeros per frame:", zl.tolist())

COL = {"bmi": "#54A24B", "s5": "#4C78A8", "bp": "#F58518", "s1": "#E45756", "s2": "#B279A2"}
HOLD = 12


fmt = lambda v: f"{v:,.0f}" if v >= 10 else f"{v:.2g}"


def frame(k):
    small = np.abs(R[k]).min()
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.06, shared_yaxes=True,
                        subplot_titles=(f"Ridge: {zr[k]} of 10 at 0<br>(smallest size {fmt(small)})",
                                        f"Lasso: {zl[k]} of 10 at 0<br> "))
    for c, P, X in ((1, R, rlams), (2, L, lams)):
        fig.add_hline(y=0, line=dict(color="black", width=2), row=1, col=c)
        for j, nm in enumerate(names):
            col = COL.get(nm, "#AAAAAA")
            fig.add_trace(go.Scatter(x=X[:k + 1], y=P[:k + 1, j], mode="lines", line=dict(color=col, width=4),
                                     name=nm if nm in COL else "other 5", legendgroup=nm if nm in COL else "o",
                                     showlegend=c == 1 and (nm in COL or nm == "age")), 1, c)
        for j, nm in sorted(enumerate(names), key=lambda t: t[1] in COL):    # coloured dots on top
            col = COL.get(nm, "#AAAAAA")
            dead = P[k, j] == 0
            fig.add_trace(go.Scatter(x=[X[k]], y=[P[k, j]], mode="markers", showlegend=False,
                                     marker=dict(size=14 if dead else 11, color="white" if dead else col,
                                                 line=dict(color="black" if dead else col, width=2))), 1, c)
        fig.add_vline(x=X[k], line=dict(color=GREY, dash="dot"), row=1, col=c)
        fig.update_xaxes(type="log", range=np.log10([X[0], X[-1]]) + [-0.15, 0.15], title=f"λ = {fmt(X[k])}",
                         dtick=1, exponentformat="power", row=1, col=c)
    fig.update_yaxes(range=[-900, 880])
    fig.update_yaxes(title_text="coefficient", row=1, col=1)
    fig.update_layout(template="simple_white", width=1100, height=620, font=dict(family="Latin Modern Roman", size=22),
                      margin=dict(l=90, r=20, t=100, b=150),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.3, font_size=20))
    fig.update_annotations(font_size=24)
    return fig


GREY = "#6B6B6B"

if __name__ == "__main__":
    tmp = HERE / ".paths_frames"
    tmp.mkdir(exist_ok=True)
    last = len(lams) - 1
    for k in range(last + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(last + 1, last + 1 + HOLD):
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "8", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=880:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "paths_race.gif")], check=True)
    picks = [int(np.argmax(zl >= 1)), int(np.argmax(zl >= 3)), int(np.argmax(zl >= 7)), last]
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in picks]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "paths_race_frames.png")
    shutil.rmtree(tmp)
