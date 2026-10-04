"""The elbow loop, animated (Plotly frames): for k = 1 to 10, k-means on the 200 students (left, coloured by cluster,
crosses = centroids) and the WCSS (inertia_) of that model added to the elbow curve (right). The bend appears at k = 4.
Same settings as the Note's loop: KMeans(n_clusters=k, random_state=0) on the unscaled data.
Run: python elbow_loop.py  -> elbow_loop.gif, elbow_loop_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.cluster import KMeans

HERE = Path(__file__).parent
PALETTE = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#9D755D", "#72B7B2", "#EECA3B", "#FF9DA6", "#BAB0AC"]
df = pd.read_csv(HERE.parent / "data" / "student_clustering.csv")
X = df.to_numpy()
models = {k: KMeans(n_clusters=k, random_state=0).fit(X) for k in range(1, 11)}
wcss = [models[k].inertia_ for k in range(1, 11)]
assert [round(w) for w in wcss[:5]] == [29958, 4184, 2503, 682, 530]     # the numbers quoted in the Note


def frame(k, done=False):
    fig = make_subplots(1, 2, horizontal_spacing=0.12, subplot_titles=[f"k-means with k = {k}", "WCSS (inertia_) so far"])
    km = models[k]
    for c in range(k):
        pts = X[km.labels_ == c]
        fig.add_trace(go.Scatter(x=pts[:, 0], y=pts[:, 1], mode="markers", marker=dict(color=PALETTE[c], size=9),
                                 showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=km.cluster_centers_[:, 0], y=km.cluster_centers_[:, 1], mode="markers", showlegend=False,
                             marker=dict(color="black", size=16, symbol="x")), 1, 1)
    ks = list(range(1, k + 1))
    fig.add_trace(go.Scatter(x=ks, y=wcss[:k], mode="lines+markers", line=dict(color="#6B6B6B", width=3),
                             marker=dict(size=12, color="#6B6B6B"), showlegend=False), 1, 2)
    fig.add_trace(go.Scatter(x=[k], y=[wcss[k - 1]], mode="markers+text", marker=dict(size=18, color="#E45756"),
                             text=[f"{wcss[k - 1]:,.0f}"], textposition="top right", textfont=dict(size=22),
                             showlegend=False), 1, 2)
    if done:
        fig.add_annotation(x=4, y=wcss[3], text="the elbow: k = 4", ax=70, ay=-110, arrowhead=2, arrowwidth=2,
                           font=dict(size=24, color="#E45756"), row=1, col=2)
    fig.update_xaxes(title_text="CGPA", row=1, col=1)
    fig.update_yaxes(title_text="IQ", row=1, col=1)
    fig.update_xaxes(title_text="number of clusters k", range=[0.5, 12.2], dtick=1, row=1, col=2)
    fig.update_yaxes(title_text="WCSS", range=[0, 33000], row=1, col=2)
    fig.update_annotations(selector=lambda a: "k = 4" not in a.text or "k-means" in a.text, font_size=24)
    fig.update_layout(template="simple_white", width=1300, height=600, font=dict(family="Latin Modern Roman", size=20),
                      margin=dict(l=70, r=30, t=70, b=70))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".elbow_loop_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, []
    for k in range(1, 11):
        frame(k).write_image(tmp / f"{n:03d}.png")
        if k in (1, 2, 4):
            keys.append(Image.open(tmp / f"{n:03d}.png").convert("RGB"))
        for j in range(1, 3):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + j:03d}.png")
        n += 3
    frame(10, done=True).write_image(tmp / f"{n:03d}.png")
    keys.append(Image.open(tmp / f"{n:03d}.png").convert("RGB"))
    for j in range(1, 8):
        shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=860:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "elbow_loop.gif")], check=True)
    w, h = keys[0].size
    grid = Image.new("RGB", (2 * w, 2 * h), "white")
    for i, im in enumerate(keys):
        grid.paste(im, ((i % 2) * w, (i // 2) * h))
    grid.save(HERE / "elbow_loop_frames.png")
    shutil.rmtree(tmp)
