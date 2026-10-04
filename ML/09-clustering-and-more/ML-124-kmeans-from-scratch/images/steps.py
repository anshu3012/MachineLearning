"""Steps of the from-scratch class drawn with Plotly: the random start (section 4), the five-row centroid example
(section 6) and the assign/move loop on the students until the centroids stop (section 7, GIF + frame grid). The start is seed 3, the good start of the four-datasets and bad-start figures."""
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

here = Path(__file__).parent
sys.path.insert(0, str(here.parent))
from kmeans import KMeans

FONT = dict(family="Latin Modern Roman", size=20)
COLS = ["#4C78A8", "#F58518", "#54A24B", "#E45756"]
X = pd.read_csv(here.parent / "data" / "student_clustering.csv").values.astype(float)
SEED = 3                                              # the good start of Figure 2 / Figure 3 (right)
LAYOUT = dict(template="simple_white", font=FONT, xaxis=dict(title="CGPA"), yaxis=dict(title="IQ"))

# replay fit_predict round by round with the class's own methods
km = KMeans(n_clusters=4, random_state=SEED)
rng = np.random.default_rng(SEED)
idx = rng.choice(X.shape[0], size=4, replace=False)
km.centroids = X[idx].astype(float)
hist = [(km.centroids.copy(), None)]
while True:
    lab = km.assign_clusters(X)
    new = km.move_centroids(X, lab)
    hist.append((new, lab))
    done = np.allclose(km.centroids, new)
    km.centroids = new
    if done:
        break
ref = KMeans(n_clusters=4, random_state=SEED)
ref_lab = ref.fit_predict(X)
assert np.array_equal(ref_lab, hist[-1][1]) and ref.n_iter_ == len(hist) - 1 == 4   # "4 rounds" in Figure 2
print("start rows", idx, "rounds", ref.n_iter_)


def points(fig, lab):
    if lab is None:
        fig.add_trace(go.Scatter(x=X[:, 0], y=X[:, 1], mode="markers", marker=dict(color="#BBBBBB", size=8),
                                 showlegend=False))
    else:
        for k in range(4):
            m = lab == k
            fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode="markers", marker=dict(color=COLS[k], size=8),
                                     showlegend=False))


def cross(fig, C, text=None):
    fig.add_trace(go.Scatter(x=C[:, 0], y=C[:, 1], mode="markers+text" if text else "markers", text=text,
                             textposition="top center", textfont=dict(size=18),
                             marker=dict(color="black", size=18, symbol="x"), showlegend=False))


# Section 4: the random start
fig = go.Figure()
points(fig, None)
cross(fig, hist[0][0], [f"row {i}" for i in idx])
fig.update_layout(**LAYOUT, width=900, height=560, margin=dict(l=70, r=20, t=60, b=60),
                  title=dict(text="Step 2: four random rows become the first centroids", x=0.5))
fig.write_image(here / "start_centroids.png", scale=2); fig.write_image(here / "start_centroids.pdf")

# Section 6: the five-row example
P = np.array([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)], float)
g = np.array([0, 1, 0, 0, 1])
toy = KMeans(n_clusters=2); toy.centroids = np.zeros((2, 2))
C = toy.move_centroids(P, g)
assert np.allclose(C.round(2), [(2.67, 3.67), (3.5, 4.5)])
from plotly.subplots import make_subplots
calc = ["(1 + 3 + 4)/3 = 2.67<br>(2 + 4 + 5)/3 = 3.67", "(2 + 5)/2 = 3.5<br>(3 + 6)/2 = 4.5"]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                    subplot_titles=["cluster 0: rows 0, 2, 3", "cluster 1: rows 1, 4"])
for k in range(2):
    fig.add_trace(go.Scatter(x=P[g != k, 0], y=P[g != k, 1], mode="markers", showlegend=False,
                             marker=dict(color="#DDDDDD", size=16)), 1, k + 1)
    fig.add_trace(go.Scatter(x=P[g == k, 0], y=P[g == k, 1], mode="markers+text", showlegend=False,
                             text=[f"row {i}" for i in np.where(g == k)[0]], textposition="middle left",
                             marker=dict(color=COLS[k], size=16)), 1, k + 1)
    fig.add_trace(go.Scatter(x=[C[k, 0]], y=[C[k, 1]], mode="markers", showlegend=False,
                             marker=dict(color=COLS[k], size=24, symbol="x", line=dict(width=2, color="black"))),
                  1, k + 1)
    fig.add_annotation(x=C[k, 0] + 0.25, y=C[k, 1] - 0.15, text=f"new centroid ({C[k, 0]:.2f}, {C[k, 1]:.2f})".replace(
        "3.50", "3.5").replace("4.50", "4.5") + "<br>" + calc[k], showarrow=False, xanchor="left", yanchor="top",
        align="left", row=1, col=k + 1, font=dict(size=18))
fig.update_xaxes(title="feature 1", range=[0, 6.5]); fig.update_yaxes(title="feature 2", range=[1, 7])
fig.update_layout(template="simple_white", font=FONT, width=1100, height=520, margin=dict(l=60, r=20, t=60, b=60))
fig.update_annotations(font_family="Latin Modern Roman")
fig.write_image(here / "move_example.png", scale=2); fig.write_image(here / "move_example.pdf")


# Section 7: the loop, one frame per half-step
def frame(r, half):
    """r = round number; half 'assign' shows new colours at old centroids, 'move' shows the centroids moved."""
    C_old, _ = hist[r - 1] if r else hist[0]
    C_new, lab = hist[r] if r else hist[0]
    fig = go.Figure()
    points(fig, lab if r else None)
    if half == "move" and r:
        shift = np.linalg.norm(C_new - C_old, axis=1).max()
        for a, b in zip(C_old, C_new):
            fig.add_trace(go.Scatter(x=[a[0], b[0]], y=[a[1], b[1]], mode="lines", showlegend=False,
                                     line=dict(color="black", width=3)))
        cross(fig, C_new)
        title = (f"round {r}, step 4: centroids move (largest move {shift:.2f})" if shift > 1e-9
                 else f"round {r}: centroids did not move, so stop")
    else:
        cross(fig, C_old)
        title = "start: 4 random rows" if r == 0 else f"round {r}, step 3: each student joins its nearest centroid"
    fig.update_layout(**LAYOUT, width=900, height=600, margin=dict(l=70, r=20, t=70, b=60),
                      title=dict(text=title, x=0.5, font=dict(size=22)))
    return fig


if __name__ == "__main__":
    tmp = here / ".rounds"
    tmp.mkdir(exist_ok=True)
    seq = [(0, "start")] + [(r, h) for r in range(1, len(hist)) for h in ("assign", "move")]
    n = 0
    for r, h in seq:
        frame(r, h).write_image(tmp / f"{n:03d}.png")
        for _ in range(2 if h != "start" else 1):     # 2 copies: each half-step stays up about 1.3 s at 1.5 fps
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + 1:03d}.png"); n += 1
        n += 1
    for _ in range(5):                                # hold the final frame
        shutil.copy(tmp / f"{n - 1:03d}.png", tmp / f"{n:03d}.png"); n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(here / "kmeans_rounds.gif")], check=True)
    keys = [frame(*s) for s in (seq[0], seq[1], seq[2], seq[-1])]
    ims = []
    for i, f in enumerate(keys):
        f.write_image(tmp / f"k{i}.png"); ims.append(Image.open(tmp / f"k{i}.png").convert("RGB"))
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(here / "kmeans_rounds_frames.png")
    shutil.rmtree(tmp)
