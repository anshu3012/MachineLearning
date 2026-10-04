"""The KNN vote as k changes: the Note's 60 example students, one new student (IQ 97.5, CGPA 8.0) near the boundary.
For k = 1, 3, 5 and 11 the circle grows to hold the k nearest students and the vote is counted. With k = 1 the answer
is "not placed" (the single nearest student was not placed); from k = 3 on it is "placed". Distances use scaled
features, so each circle is drawn as an ellipse on the raw axes. Idea after StatQuest, "K-nearest neighbors, Clearly
Explained" (the vote tally for k = 1 and k = 11). Plotly frames -> ffmpeg GIF, plus a grid of frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler

from placement_data import placement_data

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=24)
GREEN, RED, BLUE, GREY = "#54A24B", "#E45756", "#4C78A8", "#6B6B6B"
QUERY, KS = np.array([97.5, 8.0]), [1, 3, 5, 11]

X, y = placement_data()
sc = StandardScaler().fit(X)
dist = np.linalg.norm(sc.transform(X) - sc.transform([QUERY]), axis=1)
order = np.argsort(dist)
VOTES = {k: (int(y[order[:k]].sum()), k - int(y[order[:k]].sum())) for k in KS}      # (placed, not placed)
assert VOTES == {1: (0, 1), 3: (2, 1), 5: (3, 2), 11: (6, 5)}, VOTES


def frame(k):
    near = order[:k]
    yes, no = VOTES[k]
    answer, colour = ("placed", GREEN) if yes > no else ("not placed", RED)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.68, 0.32], horizontal_spacing=0.1)
    for c, name, col in [(1, "placed", GREEN), (0, "not placed", RED)]:
        fig.add_scatter(x=X[y == c, 0], y=X[y == c, 1], mode="markers", marker=dict(size=12, color=col, opacity=0.45),
                        row=1, col=1)
    fig.add_scatter(x=X[near, 0], y=X[near, 1], mode="markers", row=1, col=1,
                    marker=dict(size=16, color=[GREEN if c else RED for c in y[near]], line=dict(color="black", width=2.5)))
    r = (dist[order[k - 1]] + dist[order[k]]) / 2                    # between the k-th and the next student
    t = np.linspace(0, 2 * np.pi, 200)
    fig.add_scatter(x=QUERY[0] + r * sc.scale_[0] * np.cos(t), y=QUERY[1] + r * sc.scale_[1] * np.sin(t), mode="lines",
                    line=dict(color=BLUE, width=3, dash="dash"), row=1, col=1)
    fig.add_scatter(x=[QUERY[0]], y=[QUERY[1]], mode="markers", row=1, col=1,
                    marker=dict(size=20, color=BLUE, symbol="star", line=dict(color="black", width=1.5)))
    fig.add_bar(x=["placed", "not<br>placed"], y=[yes, no], marker_color=[GREEN, RED], text=[f"<b>{yes}</b>", f"<b>{no}</b>"],
                textposition="outside", row=1, col=2)
    fig.update_xaxes(title="IQ", range=[73, 137], row=1, col=1)
    fig.update_yaxes(title="CGPA", range=[4.8, 10], row=1, col=1)
    fig.update_yaxes(title="votes", range=[0, 7.5], dtick=1, row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=720, font=FONT, showlegend=False,
                      title=dict(text=f"<b>k = {k}</b>: {yes} placed, {no} not placed → "
                                      f"<span style='color:{colour}'><b>{answer}</b></span>", x=0.5, y=0.95,
                                 font=dict(size=32)),
                      margin=dict(l=90, r=30, t=100, b=90))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".kv_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for k in KS:
        keys.append(tmp / f"k{k}.png")
        frame(k).write_image(keys[-1])
    for j, i in enumerate([0] * 3 + [1] * 3 + [2] * 3 + [3] * 5):
        shutil.copy(keys[i], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=820:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "knn_votes.gif")], check=True)
    ims = [Image.open(k).convert("RGB") for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i % 2 * (w + 16), i // 2 * (h + 16)))
    sheet.save(HERE / "knn_votes_frames.png")
    shutil.rmtree(tmp)
