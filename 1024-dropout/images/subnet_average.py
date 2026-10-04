"""Dropout as an ensemble, from data/subnet_average.npz (experiments/subnet_average.py): a dropout network trained on
make_moons; thin grey lines are the decision boundaries of single random sub-networks (one dropout mask each), blue
is the boundary of their average, and the dashed black line is the full network with every node (what predict()
uses). Frames add sub-networks: 1, 2, 5, 10, 20, 50. Plotly frames -> ffmpeg GIF, plus the final frame for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
D = np.load(HERE.parent / "data" / "subnet_average.npz")
X, y, g1, g2, full = D["X"], D["y"], D["g1"], D["g2"], D["full"]
subs = D["subs"].astype(np.float32)
K = [1, 2, 5, 10, 20, 50]
same = {k: 100 * ((subs[:k].mean(0) > 0.5) == (full > 0.5)).mean() for k in K}
assert same[1] > 95 and same[50] > same[1] and subs.shape[0] == 50
gx, gy = g1[0], g2[:, 0]


def contour(z, color, width, dash="solid"):
    return go.Contour(x=gx, y=gy, z=z.reshape(g1.shape), showscale=False, contours_coloring="none", hoverinfo="skip",
                      contours=dict(start=0.5, end=0.5, size=1), line=dict(color=color, width=width, dash=dash))


def frame(k):
    fig = go.Figure()
    for i in range(min(k, 20)):
        fig.add_trace(contour(subs[i], "#BBBBBB", 1.5))
    for lab, c in ((0, "#F58518"), (1, "#4C78A8")):
        m = y == lab
        fig.add_scatter(x=X[m, 0], y=X[m, 1], mode="markers", marker=dict(size=7, color=c, opacity=0.7),
                        showlegend=False)
    fig.add_trace(contour(full, "black", 4, "dash"))
    fig.add_trace(contour(subs[:k].mean(0), "#54A24B", 5))
    drawn = "" if k <= 20 else " (20 drawn)"
    fig.update_layout(template="simple_white", width=960, height=760, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"<b>{k}</b> random sub-network{'s' if k > 1 else ''}{drawn}: their average "
                                      f"(green) agrees with the<br>full network (dashed) on {same[k]:.1f}% of the plane",
                                 x=0.5, y=0.95, font=dict(size=21)),
                      xaxis=dict(title="x₁", range=[-2, 3]), yaxis=dict(title="x₂", range=[-1.6, 2.1]),
                      showlegend=False, margin=dict(l=70, r=20, t=100, b=70))
    return fig


if __name__ == "__main__":
    print({k: round(v, 2) for k, v in same.items()})
    tmp = HERE / ".sa_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for k in K:
        keys.append(tmp / f"k{k}.png")
        frame(k).write_image(keys[-1])
    seq = [i for i in range(len(K)) for _ in range(3)] + [len(K) - 1] * 4
    for j, i in enumerate(seq):
        shutil.copy(keys[i], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "subnet_average.gif")], check=True)
    shutil.copy(keys[-1], HERE / "subnet_average_frames.png")
    shutil.rmtree(tmp)
