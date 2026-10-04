"""AdaBoost from scratch, step by step on the 10-row toy data (same steps and seed as the Notebook and figs.py):
weights, stump and mistakes, update, normalise, ranges, ten random draws, next dataset; three stages.
Top left: the data and the stump (marker size = copies in the current dataset). Top right: total weight of each
original row. Bottom: each row of the current dataset owns a stretch of 0 to 1; the darts are the random draws.
Run: python weights_stages.py  -> weights_stages.gif, weights_stages_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
COLOURS = {0: "#F58518", 1: "#4C78A8"}
LIGHT = {0: "#FDE5CC", 1: "#DCE6F2"}
REGION = [[0, LIGHT[0]], [1, LIGHT[1]]]
RED, GREY = "#E45756", "#6B6B6B"
X = np.c_[[1, 2, 3, 4, 5, 6, 6, 7, 9, 9], [5, 3, 6, 8, 1, 9, 5, 8, 9, 2]].astype(float)
Y = np.array([1, 1, 0, 1, 0, 1, 0, 1, 0, 0])
rng = np.random.default_rng(0)

stages, rows = [], np.arange(10)          # rows: original row of every position in the current dataset
for k in range(3):
    stump = DecisionTreeClassifier(max_depth=1, random_state=0).fit(X[rows], Y[rows])
    wrong = stump.predict(X[rows]) != Y[rows]
    w = np.full(10, 0.1)
    err = w[wrong].sum()
    alpha = 0.5 * np.log((1 - err) / err)
    updated = np.where(wrong, w * np.exp(alpha), w * np.exp(-alpha))
    norm = updated / updated.sum()
    upper = np.cumsum(norm)
    darts = [rng.random() for _ in range(10)]
    picks = [int(np.argmax(upper > a)) for a in darts]
    f, t = stump.tree_.feature[0], stump.tree_.threshold[0]
    stages.append(dict(rows=rows, stump=stump, wrong=wrong, err=err, alpha=alpha, updated=updated, norm=norm,
                       upper=upper, darts=darts, picks=picks, rule=f"X{f + 1} ≤ {t:g}"))
    rows = rows[picks]
assert list(stages[1]["rows"]) == [6, 2, 0, 0, 8, 8, 6, 7, 6, 9]          # the draw in the Note, section 6
assert list(stages[2]["rows"]) == [7, 6, 7, 6, 7, 0, 7, 7, 8, 7]          # section 8
assert np.allclose([s["alpha"] for s in stages], [0.4236, 1.0986, 0.6931], atol=1e-4)
print([(s["rule"], round(s["err"], 2), round(s["alpha"], 4)) for s in stages])

xs = np.linspace(0, 10, 200)
XX, YY = np.meshgrid(xs, xs)
grid = np.c_[XX.ravel(), YY.ravel()]


def per_row(values, s):
    """Total of a per-position quantity for each original row (a row drawn 3 times counts 3 times)."""
    return np.bincount(s["rows"], weights=values, minlength=10)


def frame(k, step, n_darts=0):
    """step: data, stump, update, normalise, ranges (with n_darts darts)."""
    s = stages[k]
    a = s["alpha"]
    show_stump = step != "data"
    weights = {"data": np.full(10, 0.1), "stump": np.full(10, 0.1), "update": s["updated"]}.get(step, s["norm"])
    titles = {"data": f"stage {k + 1}: every row of the dataset weighs 0.1",
              "stump": f"stage {k + 1}: stump {s['rule']}, error {s['err']:.1f}, alpha {a:.2f}",
              "update": f"mistakes × e<sup>{a:.2f}</sup> = × {np.exp(a):.2f}; correct × e<sup>−{a:.2f}</sup> = × {np.exp(-a):.2f}",
              "normalise": f"normalise: divide by the total, {s['updated'].sum():.4f}",
              "ranges": f"draw 10 random numbers: {n_darts} of 10"}
    fig = make_subplots(2, 2, specs=[[{}, {}], [{"colspan": 2}, None]], row_heights=[0.74, 0.26],
                        vertical_spacing=0.16, horizontal_spacing=0.1,
                        subplot_titles=["data and stump", "total weight of each original row", "each row owns a stretch of 0 to 1"])
    copies = np.bincount(s["rows"], minlength=10)
    wrong_rows = set(s["rows"][s["wrong"]]) if show_stump else set()
    if show_stump:
        fig.add_trace(go.Heatmap(x=xs, y=xs, z=s["stump"].predict(grid).reshape(XX.shape), zmin=0, zmax=1,
                                 colorscale=REGION, showscale=False), 1, 1)
    shown = copies > 0
    fig.add_trace(go.Scatter(x=X[shown, 0], y=X[shown, 1], mode="markers+text", text=[str(i) for i in np.where(shown)[0]],
                             textposition="middle center", textfont=dict(color="white", size=17),
                             marker=dict(color=[COLOURS[c] for c in Y[shown]], size=18 + 7 * copies[shown],
                                         line=dict(color="white", width=1))), 1, 1)
    bad = sorted(wrong_rows)
    fig.add_trace(go.Scatter(x=X[bad, 0], y=X[bad, 1], mode="markers", marker=dict(
        color="rgba(0,0,0,0)", size=[30 + 7 * copies[b] for b in bad], line=dict(color=RED, width=4))), 1, 1)
    fig.add_trace(go.Scatter(x=X[~shown, 0], y=X[~shown, 1], mode="markers",
                             marker=dict(symbol="x-thin", size=14, line=dict(color=GREY, width=2))), 1, 1)
    tot = per_row(weights, s)
    fig.add_trace(go.Bar(x=list(range(10)), y=tot, marker=dict(color=[COLOURS[c] for c in Y],
                                                               line=dict(color=[RED if i in wrong_rows else "white" for i in range(10)], width=3)),
                         text=[f"{v:.3f}".lstrip("0") if v else "" for v in tot], textposition="outside",
                         textfont=dict(size=19)), 1, 2)
    if step in ("normalise", "ranges"):
        lo = s["upper"] - s["norm"]
        for p in range(10):
            r = s["rows"][p]
            fig.add_trace(go.Bar(x=[s["norm"][p]], base=[lo[p]], y=[0], orientation="h", width=0.7,
                                 marker=dict(color=LIGHT[Y[r]], line=dict(color=RED if s["wrong"][p] else GREY, width=2)),
                                 text=str(r) if s["norm"][p] > 0.04 else "", textposition="inside", insidetextanchor="middle", constraintext="none",
                                 textfont=dict(size=22, color="black")), 2, 1)
        d = s["darts"][:n_darts]
        fig.add_trace(go.Scatter(x=d, y=[0.62] * len(d), mode="markers+text", text=[str(s["rows"][p]) for p in s["picks"][:n_darts]],
                                 textposition="top center", textfont=dict(size=22, color=RED),
                                 marker=dict(symbol="triangle-down", size=16, color=RED)), 2, 1)
    fig.update_xaxes(range=[0, 10], dtick=2, title_text="X1", row=1, col=1)
    fig.update_yaxes(range=[0, 10], dtick=2, title_text="X2", row=1, col=1)
    fig.update_xaxes(dtick=1, title_text="original row", row=1, col=2)
    fig.update_yaxes(range=[0, 0.7], title_text="weight", row=1, col=2)
    fig.update_xaxes(range=[0, 1], dtick=0.1, row=2, col=1)
    fig.update_yaxes(range=[-0.5, 1.3], visible=False, row=2, col=1)
    fig.update_annotations(font_size=24)
    fig.update_layout(template="simple_white", width=1200, height=900, showlegend=False, barmode="overlay",
                      font=dict(family="Latin Modern Roman", size=21), margin=dict(l=60, r=20, t=110, b=40),
                      title=dict(text=titles[step], x=0.5, y=0.97, font_size=27))
    return fig


SEQ = []
for k in range(3):
    SEQ += [(k, "data"), (k, "stump")]
    if k < 2:
        SEQ += [(k, "update"), (k, "normalise"), (k, "ranges", 0), (k, "ranges", 3), (k, "ranges", 6), (k, "ranges", 10)]

if __name__ == "__main__":
    tmp = HERE / ".weights_frames"
    tmp.mkdir(exist_ok=True)
    for i, args in enumerate(SEQ):
        frame(*args).write_image(tmp / f"{i:03d}.png")
    for i in range(len(SEQ), len(SEQ) + 4):                   # hold the last frame
        shutil.copy(tmp / f"{len(SEQ) - 1:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "0.8", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "weights_stages.gif")], check=True)
    keys = [Image.open(tmp / f"{SEQ.index(a):03d}.png").convert("RGB")
            for a in [(0, "stump"), (0, "normalise"), (0, "ranges", 10), (1, "stump")]]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "weights_stages_frames.png")
    shutil.rmtree(tmp)
