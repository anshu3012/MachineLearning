"""Section 4.4: feature importance built up split by split on the 15-observation tree of the Notebook.
Each split's weighted impurity decrease (delta) is added to its feature's bar; the bars are then divided by the total
(0.498), giving 0.417 and 0.583 = tree.feature_importances_.
Run: python importance_build.py  -> importance_build.gif, importance_build_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY = "#4C78A8", "#F58518", "#54A24B", "#9A9A9A"
FCOL = {0: BLUE, 1: ORANGE}                                     # one colour per feature
X, y = make_classification(n_samples=15, n_classes=2, n_features=2, n_informative=2, n_redundant=0, random_state=0)
tree = DecisionTreeClassifier(random_state=0).fit(X, y)
t = tree.tree_
N = t.n_node_samples[0]
splits = [i for i in range(t.node_count) if t.children_left[i] != -1]
delta = {}
for i in splits:
    l, r = t.children_left[i], t.children_right[i]
    delta[i] = (t.n_node_samples[i] * t.impurity[i] - t.n_node_samples[l] * t.impurity[l]
                - t.n_node_samples[r] * t.impurity[r]) / N
total = sum(delta.values())
imp = [sum(d for i, d in delta.items() if t.feature[i] == f) / total for f in (0, 1)]
assert np.allclose(imp, tree.feature_importances_) and np.round(imp, 3).tolist() == [0.417, 0.583]
assert [round(delta[i], 3) for i in splits] == [0.290, 0.119, 0.089]          # the Note's table
print({i: (int(t.feature[i]), round(delta[i], 3)) for i in splits}, round(total, 3), np.round(imp, 3))

# layout: leaves spread evenly, parents above the middle of their children
pos, leaves = {}, []


def walk(i, depth):
    if t.children_left[i] == -1:
        leaves.append(i)
        pos[i] = [0, depth]
    else:
        walk(t.children_left[i], depth + 1)
        walk(t.children_right[i], depth + 1)
        pos[i] = [None, depth]


walk(0, 0)
for j, i in enumerate(leaves):
    pos[i][0] = 3 + (j + 0.5) * 56 / len(leaves)
for i in sorted(splits, reverse=True):
    pos[i][0] = (pos[t.children_left[i]][0] + pos[t.children_right[i]][0]) / 2
YY = lambda d: 50 - 13 * d                                       # noqa: E731


def frame(title, n_done, normalised):
    fig = go.Figure()
    for i in range(t.node_count):
        x, d = pos[i]
        if i:
            par = next(p for p in splits if i in (t.children_left[p], t.children_right[p]))
            fig.add_shape(opacity=1, type="line", x0=pos[par][0], y0=YY(pos[par][1]) - 4, x1=x, y1=YY(d) + 4,
                          line=dict(color="#6B6B6B", width=2), layer="below")
        c = t.value[i][0] * t.n_node_samples[i]
        if i in splits:
            k = splits.index(i)
            f = int(t.feature[i])
            on, now = k < n_done, k == n_done - 1 and not normalised
            fig.add_shape(opacity=1, type="rect", x0=x - 9, x1=x + 9, y0=YY(d) - 4, y1=YY(d) + 4,
                          line=dict(color=FCOL[f] if on else GREY, width=5 if now else 2.5),
                          fillcolor={0: "#DCE6F2", 1: "#FDE5CC"}[f] if on else "white")
            fig.add_annotation(x=x, y=YY(d), showarrow=False, font_size=18,
                               text=f"feature {f} split<br>{t.n_node_samples[i]} obs, Gini {t.impurity[i]:.3f}")
            if on:
                fig.add_annotation(x=x, y=YY(d) + 6, showarrow=False, font=dict(size=20, color=FCOL[f]),
                                   text=f"<b>Δ = {delta[i]:.3f}</b>")
        else:
            fig.add_shape(opacity=1, type="rect", x0=x - 4.3, x1=x + 4.3, y0=YY(d) - 3, y1=YY(d) + 3,
                          line=dict(color=GREY, width=2), fillcolor="#F2F2F2")
            fig.add_annotation(x=x, y=YY(d), text=f"[{c[0]:.0f}, {c[1]:.0f}]", showarrow=False, font_size=18)
    # the two bars
    scale = 60 if not normalised else 60 * 0.5        # bar height units per unit of delta / of importance
    for f, bx in ((0, 76), (1, 91)):
        y0 = 8
        parts = [delta[i] for i in splits[:n_done] if t.feature[i] == f]
        if normalised:
            parts = [imp[f]]
        for p in parts:
            fig.add_shape(opacity=1, type="rect", x0=bx - 5, x1=bx + 5, y0=y0, y1=y0 + p * scale, fillcolor=FCOL[f],
                          line=dict(color="white", width=2))
            if not normalised and len(parts) > 1:
                fig.add_annotation(x=bx, y=y0 + p * scale / 2, text=f"{p:.3f}", showarrow=False, font=dict(size=17, color="white"))
            y0 += p * scale
        tot = sum(parts) if normalised else sum(round(p, 3) for p in parts)     # rounded parts, as in the Note
        if parts:
            fig.add_annotation(x=bx, y=y0 + 2.5, text=f"<b>{tot:.3f}</b>", showarrow=False, font=dict(size=22, color=FCOL[f]))
        fig.add_annotation(x=bx, y=5, text=f"feature {f}", showarrow=False, font_size=20)
    fig.add_shape(opacity=1, type="line", x0=68, x1=99, y0=8, y1=8, line=dict(color="black", width=1.5))
    fig.add_annotation(x=83.5, y=57, showarrow=False, font_size=20,
                       text="<b>importance</b> (sums to 1)" if normalised else "<b>total Δ per feature</b>")
    fig.add_annotation(x=31, y=1.5, text="[class 0, class 1] observations in a leaf", showarrow=False,
                       font=dict(size=17, color="#6B6B6B"))
    fig.update_xaxes(range=[0, 100], visible=False)
    fig.update_yaxes(range=[0, 62], visible=False)
    fig.update_layout(template="simple_white", width=1000, height=620, font=dict(family="Latin Modern Roman", size=22),
                      margin=dict(l=5, r=5, t=70, b=5), showlegend=False, title=dict(text=title, x=0.5, font_size=24))
    return fig


names = ["the root", "the second split", "the third split"]
stages = [("A tree on 15 observations: three splits", 0, False)]
for k, i in enumerate(splits):
    stages.append((f"{names[k].capitalize()} is on feature {t.feature[i]}: add its Δ = {delta[i]:.3f}", k + 1, False))
stages.append((f"Divide each total by the sum, {total:.3f}", 3, True))

if __name__ == "__main__":
    tmp = HERE / ".imp_frames"
    tmp.mkdir(exist_ok=True)
    n = 0
    for i, s in enumerate(stages):
        img = tmp / f"s{i:02d}.png"
        frame(*s).write_image(img)
        for _ in range(6 + (6 if i == len(stages) - 1 else 0)):
            shutil.copy(img, tmp / f"{n:03d}.png")
            n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=6,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "importance_build.gif")], check=True)
    ims = [Image.open(tmp / f"s{i:02d}.png").convert("RGB") for i in (1, 2, 3, 4)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "importance_build_frames.png")
    shutil.rmtree(tmp)
