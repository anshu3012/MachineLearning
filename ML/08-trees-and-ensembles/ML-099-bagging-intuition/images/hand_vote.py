"""Bagging by hand, drawn: the Notebook's 10 training flowers, three bootstrap samples of 8 (random_state 0, 1, 2),
three fully grown trees, each a single cut on petal length, and their vote on the new flower (sepal width 2.2,
petal length 5.0). Plotly frames -> ffmpeg GIF, plus the final frame for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
ORANGE, GREEN, GREY = "#F58518", "#54A24B", "#BBBBBB"
TREE_COL = ["#4C78A8", "#B279A2", "#E45756"]

iris = load_iris(as_frame=True).frame.rename(columns={"target": "species"})
df = iris[iris["species"] != 0][["sepal width (cm)", "petal length (cm)", "species"]]
df = df.sample(100, random_state=2)
df_train = df.iloc[:60].sample(10, random_state=2)       # exactly the Notebook's steps
bags = [df_train.sample(8, replace=True, random_state=b) for b in range(3)]
trees = [DecisionTreeClassifier(random_state=0).fit(b.iloc[:, 0:2], b.iloc[:, -1]) for b in bags]
cuts = [t.tree_.threshold[0] for t in trees]
assert [round(c, 2) for c in cuts] == [5.2, 4.9, 4.95] and all(t.tree_.feature[0] == 1 for t in trees)
point = np.array([[2.2, 5.0]])
import pandas as pd  # noqa: E402
votes = [int(t.predict(pd.DataFrame(point, columns=df.columns[:2]))[0]) for t in trees]
assert votes == [1, 2, 2]


def frame(k):
    """k = 0, 1, 2: tree k with its sample; k = 3: all three cuts and the vote."""
    fig = go.Figure()
    sw, pl, sp = df_train.iloc[:, 0].values, df_train.iloc[:, 1].values, df_train.iloc[:, 2].values
    if k < 3:
        cnt = bags[k].index.value_counts().reindex(df_train.index, fill_value=0).values
    else:
        cnt = np.ones(len(df_train), int)
    for lab, c, name in ((1, ORANGE, "versicolor (1)"), (2, GREEN, "virginica (2)")):
        m = sp == lab
        fig.add_scatter(x=pl[m & (cnt == 0)], y=sw[m & (cnt == 0)], mode="markers", showlegend=False,
                        marker=dict(size=14, color="white", line=dict(width=2, color=c)))
        fig.add_scatter(x=pl[m & (cnt > 0)], y=sw[m & (cnt > 0)], mode="markers+text", name=name,
                        marker=dict(size=12 + 8 * cnt[m & (cnt > 0)], color=c, line=dict(width=1, color="white")),
                        text=[f"×{n}" if n > 1 else "" for n in cnt[m & (cnt > 0)]], textposition="top center",
                        textfont=dict(size=18))
    show = range(3) if k == 3 else [k]
    for i in show:
        fig.add_vline(x=cuts[i], line=dict(color=TREE_COL[i], width=4, dash="dash"), opacity=1, layer="above")
        fig.add_annotation(x=cuts[i], y=3.62 - 0.1 * i if k == 3 else 3.62, text=f"tree {i + 1}: {cuts[i]:.2f}",
                           showarrow=False, xanchor="left", xshift=4, font=dict(size=17, color=TREE_COL[i]))
    fig.add_scatter(x=[5.0], y=[2.2], mode="markers", name="new flower",
                    marker=dict(size=28, symbol="star", color="black"))
    if k < 3:
        title = (f"Tree {k + 1}: cut at petal length {cuts[k]:.2f}; new flower (5.0) is "
                 f"{'below' if 5.0 <= cuts[k] else 'above'}, so tree {k + 1} votes <b>{votes[k]}</b>")
    else:
        title = "Votes 1, 2, 2: the majority says <b>2</b> (virginica), which is right"
    fig.update_layout(template="simple_white", width=1100, height=660, font=FONT,
                      title=dict(text=title, x=0.5, y=0.95, font=dict(size=21)),
                      xaxis=dict(title="petal length (cm)", range=[3.6, 6.9]),
                      yaxis=dict(title="sepal width (cm)", range=[2.0, 3.7]),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.17),
                      margin=dict(l=80, r=30, t=80, b=130))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".hv_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for k in range(4):
        keys.append(tmp / f"k{k}.png")
        frame(k).write_image(keys[-1])
    seq = [0] * 4 + [1] * 4 + [2] * 4 + [3] * 6
    for j, k in enumerate(seq):
        shutil.copy(keys[k], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=820:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "hand_vote.gif")], check=True)
    shutil.copy(keys[3], HERE / "hand_vote_frames.png")
    shutil.rmtree(tmp)
