"""Section 4: how one tree of a random forest is built, on 12 patients of the heart disease data (the data of the
tuning and OOB Notes; here the first 6 patients of each class and 5 of the 13 features).
Step 1: a bootstrap sample (12 draws with replacement). Step 2: at EVERY split, 2 of the 5 features are drawn at
random (the "sqrt" default: floor(sqrt(5)) = 2) and the best Gini split among those two is used.
The tree is grown by the small function below, so that the two candidates of every node can be shown.
Run: python build_tree.py  -> build_tree.gif, build_tree_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY, RED = "#4C78A8", "#F58518", "#54A24B", "#9A9A9A", "#E45756"
FONT = dict(family="Latin Modern Roman", size=22)
df = pd.read_csv(HERE.parent / "data" / "heart.csv")                      # the heart disease data of Notes 112 and 113
COLS = ["age", "cp", "trestbps", "chol", "thalach"]
NAMES = ["age", "chest pain", "pressure", "chol.", "heart rate"]
keep = np.sort(np.r_[np.where(df.target == 0)[0][:6], np.where(df.target == 1)[0][:6]])   # first 6 patients of each class
X, y = df.loc[keep, COLS].to_numpy(float), df.target.to_numpy()[keep]
N, P, K = 12, 5, int(np.sqrt(5))                                          # 12 patients, 5 features, 2 per split
rng = np.random.default_rng(0)
draws = rng.integers(0, N, N)                                             # step 1: bootstrap sample
Xb, yb = X[draws], y[draws]


def gini(t):
    p = np.bincount(t, minlength=2) / len(t)
    return 1 - (p ** 2).sum()


def best_split(rows, feats):
    """Best (weighted Gini, feature, threshold) among the given features."""
    best = None
    for f in feats:
        v = np.unique(Xb[rows, f])
        for thr in (v[:-1] + v[1:]) / 2:
            left = rows[Xb[rows, f] <= thr]
            right = rows[Xb[rows, f] > thr]
            g = (len(left) * gini(yb[left]) + len(right) * gini(yb[right])) / len(rows)
            if best is None or g < best[0]:
                best = (g, f, thr)
    return best


# step 2: grow the tree; every impure node draws its own K candidate features
nodes = [dict(rows=np.arange(N), depth=0, parent=None)]
queue = [0]
while queue:
    i = queue.pop(0)
    nd = nodes[i]
    if gini(yb[nd["rows"]]) == 0:
        continue
    while True:                                   # a candidate pair that cannot split (all values equal) is redrawn
        cand = np.sort(rng.choice(P, K, replace=False))
        b = best_split(nd["rows"], cand)
        if b is not None:
            break
    nd.update(cand=cand, feat=b[1], thr=b[2], kids=[])
    for side in (Xb[nd["rows"], b[1]] <= b[2], Xb[nd["rows"], b[1]] > b[2]):
        nodes.append(dict(rows=nd["rows"][side], depth=nd["depth"] + 1, parent=i))
        nd["kids"].append(len(nodes) - 1)
        queue.append(len(nodes) - 1)
splits = [i for i, nd in enumerate(nodes) if "feat" in nd]
used = sorted({nodes[i]["feat"] for i in splits})
cands = [tuple(nodes[i]["cand"]) for i in splits]
oob = sorted(set(range(N)) - set(draws))
counts = np.bincount(draws, minlength=N)
print("draws", draws, "out-of-bag", oob, "splits", [(nodes[i]["cand"] + 1, nodes[i]["feat"] + 1, round(nodes[i]["thr"], 2))
                                                 for i in splits])
# what the animation claims
assert len(oob) >= 1 and counts.max() >= 2            # drawing with replacement: repeats and left-out observations
assert len(set(cands)) > 1                            # the candidate pair changes from split to split
assert all(gini(yb[nd["rows"]]) == 0 for nd in nodes if "feat" not in nd)     # every leaf is pure

# tree layout: leaves spread evenly, a parent sits above the middle of its children
leaves = []


def order(i):
    if "kids" in nodes[i]:
        for k in nodes[i]["kids"]:
            order(k)
        nodes[i]["x"] = np.mean([nodes[k]["x"] for k in nodes[i]["kids"]])
    else:
        leaves.append(i)
        nodes[i]["x"] = 0


def place(i):
    if "kids" in nodes[i]:
        for k in nodes[i]["kids"]:
            place(k)
        nodes[i]["x"] = np.mean([nodes[k]["x"] for k in nodes[i]["kids"]])


order(0)
for j, i in enumerate(leaves):
    nodes[i]["x"] = 40 + (j + 0.5) * 60 / len(leaves)
place(0)
for nd in nodes:
    nd["y"] = 43 - 11 * nd["depth"]


def base(title):
    fig = go.Figure()
    fig.update_xaxes(range=[0, 100], visible=False)
    fig.update_yaxes(range=[0, 62], visible=False)
    fig.update_layout(template="simple_white", width=1000, height=620, font=FONT, showlegend=False,
                      margin=dict(l=5, r=5, t=70, b=5), title=dict(text=title, x=0.5, font_size=24))
    return fig


def box(fig, x, y, w, h, text, line, fill, size=20, colour="black"):
    fig.add_shape(opacity=1, type="rect", x0=x - w / 2, x1=x + w / 2, y0=y - h / 2, y1=y + h / 2,
                  line=dict(color=line, width=3), layer="below", fillcolor=fill)
    fig.add_annotation(x=x, y=y, text=text, showarrow=False, font=dict(size=size, color=colour))


def frame(title, n_draws, show_oob, n_splits, pending):
    """n_draws: bootstrap slots filled; n_splits: split nodes finished; pending: show the next node's 2 candidates."""
    fig = base(title)
    cls_fill = {0: "#DCE6F2", 1: "#FDE5CC"}
    cls_line = {0: BLUE, 1: ORANGE}
    fig.add_annotation(x=7, y=59, text="<b>data</b>", showarrow=False)
    fig.add_annotation(x=23, y=59, text="<b>bootstrap sample</b>", showarrow=False)
    for r in range(N):
        yy = 54 - 4.5 * r
        out = show_oob and r in oob
        box(fig, 7, yy, 12, 3.7, f"patient {r + 1}", GREY if out else cls_line[y[r]], "white" if out else cls_fill[y[r]],
            colour=GREY if out else "black")
        if out:
            fig.add_annotation(x=14.8, y=yy, text="out", showarrow=False, font=dict(size=18, color=RED))
        if r < n_draws:
            d = draws[r]
            again = d in draws[:r]
            box(fig, 23, yy, 12, 3.7, f"patient {d + 1}", RED if again else cls_line[y[d]], cls_fill[y[d]])
            if again:
                fig.add_annotation(x=32, y=yy, text="again", showarrow=False, font=dict(size=18, color=RED))
        else:
            box(fig, 23, yy, 12, 3.7, "", "#DDDDDD", "white")
    fig.add_annotation(x=15, y=0.8, text="blue: no disease, orange: disease", showarrow=False, font=dict(size=18, color="#6B6B6B"))
    # the five feature chips
    cur = splits[n_splits] if (pending and n_splits < len(splits)) else (splits[n_splits - 1] if n_splits else None)
    if n_draws == N and show_oob:
        fig.add_annotation(x=70, y=59, text="<b>features</b> (2 random candidates per split)", showarrow=False)
        for f in range(P):
            is_c = cur is not None and f in nodes[cur]["cand"]
            is_best = cur is not None and not pending and f == nodes[cur]["feat"]
            box(fig, 49 + 10.4 * f, 53, 10, 4.6, NAMES[f], GREEN if is_best else (ORANGE if is_c else "#CCCCCC"),
                "#D9EFD5" if is_best else ("#FDE5CC" if is_c else "white"), 17, "black" if is_c else GREY)
    # the tree so far
    done = set(splits[:n_splits])
    shown = {0} if (n_draws == N and show_oob and (n_splits or pending)) else set()
    for i in done:
        shown |= {i, *nodes[i]["kids"]}
    for i in sorted(shown):
        nd = nodes[i]
        c = np.bincount(yb[nd["rows"]], minlength=2)
        if nd["parent"] is not None:
            par = nodes[nd["parent"]]
            fig.add_shape(opacity=1, type="line", x0=par["x"], y0=par["y"] - 3.6, x1=nd["x"], y1=nd["y"] + 3.6,
                          line=dict(color="#6B6B6B", width=2))
        if i in done:
            box(fig, nd["x"], nd["y"], 16, 7.2, f"{NAMES[nd['feat']]} ≤ {nd['thr']:g}<br>[{c[0]}, {c[1]}]", GREEN, "#D9EFD5", 17)
        elif "feat" in nd:
            hot = pending and i == cur
            box(fig, nd["x"], nd["y"], 16, 7.2, f"split?<br>[{c[0]}, {c[1]}]", ORANGE if hot else GREY, "#FDE5CC" if hot else "white", 17)
        else:
            k = int(c.argmax())
            box(fig, nd["x"], nd["y"], 10.5, 7.2, ("disease" if k else "no disease") + f"<br>[{c[0]}, {c[1]}]", cls_line[k], cls_fill[k], 17)
    if shown:
        fig.add_annotation(x=70, y=0.8, text="[no disease, disease] patients in the node", showarrow=False,
                           font=dict(size=18, color="#6B6B6B"))
    return fig


stages = [("The training data: 12 patients, 5 features", 0, False, 0, False)]
for k in range(1, N + 1):
    d = draws[k - 1]
    stages.append((f"Step 1, draw {k} of {N}: patient {d + 1}" + (" again" if d in draws[:k - 1] else ""), k, False, 0, False))
stages.append((f"Bootstrap sample done; never drawn: {'patients ' + ', '.join(str(r + 1) for r in oob)}", N, True, 0, False))
for j, i in enumerate(splits):
    a, b = (NAMES[f] for f in nodes[i]["cand"])
    stages.append((f"Step 2, split {j + 1}: draw 2 of the 5 features: {a}, {b}", N, True, j, True))
    stages.append((f"Split {j + 1}: the better of the two is {NAMES[nodes[i]['feat']]}", N, True, j + 1, False))
stages.append((f"One tree done: {len(splits)} splits, each with its own 2 candidates", N, True, len(splits), False))

if __name__ == "__main__":
    tmp = HERE / ".build_frames"
    tmp.mkdir(exist_ok=True)
    k = 0
    for i, s in enumerate(stages):
        img = tmp / f"s{i:02d}.png"
        frame(*s).write_image(img)
        hold = 2 if 1 <= i <= N else 5                      # draws go faster; every tree step is held
        for _ in range(hold + (6 if i == len(stages) - 1 else 0)):
            shutil.copy(img, tmp / f"{k:03d}.png")
            k += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=6,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "build_tree.gif")], check=True)
    keys = [N + 1, N + 2, N + 3, len(stages) - 1]            # sample done, first candidates, first split, finished tree
    ims = [Image.open(tmp / f"s{i:02d}.png").convert("RGB") for i in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "build_tree_frames.png")
    shutil.rmtree(tmp)
