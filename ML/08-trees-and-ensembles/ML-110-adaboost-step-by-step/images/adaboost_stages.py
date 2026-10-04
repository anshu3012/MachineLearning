"""AdaBoost on the Note's 5 observations, stage by stage: dot size = sample weight, the stump's cut and its two
sides, mistakes ringed in red, alpha bars, then the weighted vote of all stumps.
Real stumps (DecisionTreeClassifier, max_depth=1), weights passed as sample_weight (the scikit-learn way),
alpha = 0.5 ln((1 - error) / error), weights times exp(-alpha y h), normalised (Schapire 2013, Algorithm 1).
Run: python adaboost_stages.py  -> adaboost_stages.gif, adaboost_stages_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
BLUE, ORANGE, RED = "#4C78A8", "#F58518", "#E45756"
SHADE = {1: "rgba(76,120,168,0.32)", -1: "rgba(245,133,24,0.32)"}
X = np.array([[3, 7], [2, 9], [1, 9], [9, 8], [7, 4]])
y = np.array([1, 1, -1, -1, -1])
T = 3

stages, w = [], np.full(5, 0.2)
for t in range(T):
    s = DecisionTreeClassifier(max_depth=1).fit(X, y, sample_weight=w)
    p = s.predict(X)
    err = w[p != y].sum()
    a = 0.5 * np.log((1 - err) / err)
    f, thr = s.tree_.feature[0], s.tree_.threshold[0]
    sides = s.predict([[thr - 0.01, 5], [thr + 0.01, 5]] if f == 0 else [[5, thr - 0.01], [5, thr + 0.01]])
    w_new = w * np.exp(-a * y * p)
    stages.append(dict(w=w, p=p, err=err, a=a, f=f, thr=thr, sides=sides, w_next=w_new / w_new.sum()))
    w = stages[-1]["w_next"]
H = np.sign(sum(st["a"] * st["p"] for st in stages))
assert np.isclose(stages[0]["a"], 0.5 * np.log(4)) and (H == y).all()     # 3 stumps fix every observation
for t, st in enumerate(stages):
    print(t + 1, f"x{st['f'] + 1} cut {st['thr']}", "error", round(st["err"], 3), "alpha", round(st["a"], 3))


def base(title, w, labels=True):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.62, 0.38], horizontal_spacing=0.13,
                        subplot_titles=("", "say of each stump (alpha)"))
    for cls, col, name in ((1, BLUE, "y = +1"), (-1, ORANGE, "y = -1")):
        m = y == cls
        fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", name=name,
                                 marker=dict(color=col, size=18 + 110 * w[m], line=dict(color="white", width=1))), 1, 1)
    fig.add_trace(go.Scatter(x=X[:, 0], y=X[:, 1] - 1.1, mode="text", text=[f"{v:.2f}" if labels else "" for v in w], showlegend=False,
                             textfont=dict(size=22)), 1, 1)
    fig.update_xaxes(range=[0, 10], title="x1", dtick=2, row=1, col=1)
    fig.update_yaxes(range=[1.5, 11], title="x2", dtick=2, row=1, col=1)
    fig.update_xaxes(range=[0.4, T + 0.6], tickvals=list(range(1, T + 1)), ticktext=[f"stump {t}" for t in range(1, T + 1)],
                     row=1, col=2)
    fig.update_yaxes(range=[0, 1.0], row=1, col=2)
    fig.update_annotations(font_size=24)
    fig.update_layout(template="simple_white", width=1100, height=620, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=title, x=0.5, y=0.97), margin=dict(l=70, r=20, t=120, b=60),
                      legend=dict(orientation="h", x=0, y=1.02, yanchor="bottom"))
    return fig


def add_stump(fig, st):
    lo, hi = st["sides"]
    if st["f"] == 0:
        fig.add_shape(type="rect", x0=0, x1=st["thr"], y0=1.5, y1=11, fillcolor=SHADE[lo], line_width=0, row=1, col=1)
        fig.add_shape(type="rect", x0=st["thr"], x1=10, y0=1.5, y1=11, fillcolor=SHADE[hi], line_width=0, row=1, col=1)
        fig.add_shape(type="line", x0=st["thr"], x1=st["thr"], y0=1.5, y1=11, line=dict(width=4, color="black"), row=1, col=1)
    else:
        fig.add_shape(type="rect", x0=0, x1=10, y0=1.5, y1=st["thr"], fillcolor=SHADE[lo], line_width=0, row=1, col=1)
        fig.add_shape(type="rect", x0=0, x1=10, y0=st["thr"], y1=11, fillcolor=SHADE[hi], line_width=0, row=1, col=1)
        fig.add_shape(type="line", x0=0, x1=10, y0=st["thr"], y1=st["thr"], line=dict(width=4, color="black"), row=1, col=1)
    bad = st["p"] != y
    fig.add_trace(go.Scatter(x=X[bad, 0], y=X[bad, 1], mode="markers", name="mistake",
                             marker=dict(symbol="circle-open", color=RED, size=26 + 110 * st["w"][bad],
                                         line=dict(width=4))), 1, 1)


def add_alphas(fig, upto):
    a = [st["a"] for st in stages[:upto]]
    fig.add_trace(go.Bar(x=list(range(1, upto + 1)), y=a, marker_color="#54A24B", text=[f"{v:.2f}" for v in a],
                         textposition="outside", textfont=dict(size=22), showlegend=False), 1, 2)


frames = []
for t, st in enumerate(stages):
    n = t + 1
    fig = base(f"stage {n}: dot size = weight", st["w"]); add_alphas(fig, t); frames.append(fig)
    fig = base(f"stump {n}: cut x{st['f'] + 1} = {st['thr']:g}, error {st['err']:.2f}", st["w"])
    add_stump(fig, st); add_alphas(fig, t); frames.append(fig)
    fig = base(f"alpha = ½ ln((1 - {st['err']:.2f}) / {st['err']:.2f}) = {st['a']:.2f}", st["w"])
    add_stump(fig, st); add_alphas(fig, n); frames.append(fig)
    fig = base("mistakes grow, the rest shrink", st["w_next"])
    add_stump(fig, st); add_alphas(fig, n); frames.append(fig)
# final: weighted vote over the plane
gx = np.linspace(0, 10, 201)
gy = np.linspace(1.5, 11, 191)
GX, GY = np.meshgrid(gx, gy)
score = sum(st["a"] * np.where((GX if st["f"] == 0 else GY) <= st["thr"], *st["sides"]) for st in stages)
fig = base("weighted vote of 3 stumps: all 5 correct", np.full(5, 0.2), labels=False)
fig.add_trace(go.Heatmap(x=gx, y=gy, z=np.sign(score), zmin=-1, zmax=1, showscale=False, hoverinfo="skip",
                         colorscale=[[0, "rgba(245,133,24,0.25)"], [1, "rgba(76,120,168,0.25)"]]), 1, 1)
fig.data = fig.data[-1:] + fig.data[:-1]                  # regions under the points
add_alphas(fig, T)
frames.append(fig)

if __name__ == "__main__":
    tmp = HERE / ".ada_frames"
    tmp.mkdir(exist_ok=True)
    k = 0
    for i, f in enumerate(frames):
        f.write_image(tmp / f"{k:03d}.png")
        for _ in range(8 if i == len(frames) - 1 else 2):    # each step held 3 frames, the last longer
            shutil.copy(tmp / f"{k:03d}.png", tmp / f"{k + 1:03d}.png")
            k += 1
        k += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "adaboost_stages.gif")], check=True)
    keys = [Image.open(tmp / f"{3 * i:03d}.png").convert("RGB") for i in (1, 3, 9, len(frames) - 1)]
    w_, h_ = keys[0].size
    sheet = Image.new("RGB", (2 * w_ + 16, 2 * h_ + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w_ + 16), (i // 2) * (h_ + 16)))
    sheet.save(HERE / "adaboost_stages_frames.png")
    shutil.rmtree(tmp)
