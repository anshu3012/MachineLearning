"""A bad and a good random start side by side, animated (Plotly frames): the from-scratch KMeans class on the 200
students, k = 4, seeds 0 (bad) and 3 (good), one assign-and-move round per frame. Both runs stop within a few rounds;
the bad run then stays at WCSS 2,280 however many rounds are allowed, so a larger max_iter is not the fix.
Run: python start_race.py  -> start_race.gif, start_race_frames.png"""
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from kmeans import KMeans  # noqa: E402

COLS = ["#4C78A8", "#F58518", "#54A24B", "#E45756"]
X = pd.read_csv(HERE.parent / "data" / "student_clustering.csv").to_numpy()
ROUNDS = 8


def history(seed):
    """Centroids, labels and WCSS after 0, 1, ... ROUNDS rounds, and the round in which the class's loop breaks."""
    km = KMeans(n_clusters=4, random_state=seed)
    rng = np.random.default_rng(seed)
    km.centroids = X[rng.choice(X.shape[0], size=4, replace=False)].astype(float)
    out, stop = [], None
    for i in range(ROUNDS + 1):
        lab = km.assign_clusters(X)
        out.append((km.centroids.copy(), lab, ((X - km.centroids[lab]) ** 2).sum()))
        new = km.move_centroids(X, lab)
        if stop is None and np.allclose(new, km.centroids):
            stop = i + 1                                   # the round whose move changes nothing: the loop breaks
        km.centroids = new
    ref = KMeans(n_clusters=4, max_iter=500, random_state=seed)
    ref.fit_predict(X)
    assert ref.n_iter_ == stop and np.isclose(ref.inertia_, out[-1][2])
    return out, stop


runs = [history(0), history(3)]
assert round(runs[0][0][-1][2]) == 2280 and round(runs[1][0][-1][2]) == 682   # the Note's numbers


def frame(i):
    titles = []
    for name, (hist, stop) in zip(("bad start", "good start"), runs):
        state = f"stopped in round {stop}" if i >= stop else "running"
        titles.append(f"{name}: {state}, WCSS {hist[i][2]:,.0f}")
    fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=titles)
    for c, (hist, stop) in enumerate(runs, start=1):
        cen, lab, _ = hist[i]
        for k in range(4):
            pts = X[lab == k]
            fig.add_trace(go.Scatter(x=pts[:, 0], y=pts[:, 1], mode="markers", marker=dict(color=COLS[k], size=9),
                                     showlegend=False), 1, c)
        fig.add_trace(go.Scatter(x=cen[:, 0], y=cen[:, 1], mode="markers", showlegend=False,
                                 marker=dict(color="black", size=18, symbol="x")), 1, c)
    fig.update_xaxes(title_text="CGPA")
    fig.update_yaxes(title_text="IQ")
    fig.update_annotations(font_size=23)
    fig.update_layout(template="simple_white", width=1300, height=620, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"round {i}" if i else "the random start", x=0.5, y=0.97, font_size=28),
                      margin=dict(l=70, r=30, t=120, b=70))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".start_race_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, []
    for i in range(ROUNDS + 1):
        rep = 4 if i == 0 else 8 if i == ROUNDS else 3
        frame(i).write_image(tmp / f"{n:03d}.png")
        if i in (0, 1, 3, ROUNDS):
            keys.append(Image.open(tmp / f"{n:03d}.png").convert("RGB"))
        for j in range(1, rep):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + j:03d}.png")
        n += rep
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=860:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "start_race.gif")], check=True)
    w, h = keys[0].size
    grid = Image.new("RGB", (2 * w, 2 * h), "white")
    for i, im in enumerate(keys):
        grid.paste(im, ((i % 2) * w, (i // 2) * h))
    grid.save(HERE / "start_race_frames.png")
    shutil.rmtree(tmp)
