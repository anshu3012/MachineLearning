"""Section 3.3, n_estimators: the forest grows from 1 to 200 trees on the concentric-circles data.
Left: the decision surface on one split (the app's split). Right: mean test accuracy over the Notebook's 20 random
splits, drawn up to the current number of trees; it rises, then levels off.
Run: python trees_sweep.py  -> trees_sweep.gif, trees_sweep_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import X, fit, traces, xs, y, ys  # noqa: E402  same data, model and surface code as the app

NS = [1, 2, 3, 5, 8, 10, 15, 20, 30, 50, 100, 200]
splits = [train_test_split(X, y, random_state=s) for s in range(20)]          # as in the Notebook


def score(n):
    return float(np.mean([RandomForestClassifier(n_estimators=n, random_state=s, n_jobs=-1).fit(a, c).score(b, d)
                          for s, (a, b, c, d) in enumerate(splits)]))


acc = {n: score(n) for n in NS}
assert [round(acc[n], 3) for n in (1, 5, 10)] == [0.846, 0.868, 0.888]
assert all(abs(acc[n] - 0.887) < 0.002 for n in (50, 100, 200))
print({n: round(a, 3) for n, a in acc.items()})


def frame(k):
    n = NS[k]
    rf, one = fit(n_estimators=n)
    fig = make_subplots(1, 2, column_widths=[0.5, 0.5], horizontal_spacing=0.1,
                        subplot_titles=[f"{n} tree{'s' if n > 1 else ''}: decision surface",
                                        "mean test accuracy, 20 splits"])
    for t in traces(rf, show_legend=False):
        fig.add_trace(t, 1, 1)
    shown = NS[:k + 1]
    fig.add_trace(go.Scatter(x=NS, y=[acc[m] for m in NS], mode="lines", line=dict(color="#DDDDDD", width=3),
                             showlegend=False), 1, 2)
    fig.add_trace(go.Scatter(x=shown, y=[acc[m] for m in shown], mode="lines+markers", showlegend=False,
                             line=dict(color="#4C78A8", width=4), marker=dict(size=10)), 1, 2)
    fig.add_trace(go.Scatter(x=[n], y=[acc[n]], mode="markers+text", text=[f"{acc[n]:.3f}"], showlegend=False,
                             textposition="bottom right" if n < 50 else "bottom left", textfont=dict(size=30, color="#E45756"),
                             marker=dict(size=18, color="#E45756")), 1, 2)
    fig.update_xaxes(range=[xs[0], xs[-1]], showticklabels=False, row=1, col=1)
    fig.update_yaxes(range=[ys[0], ys[-1]], showticklabels=False, row=1, col=1)
    fig.update_xaxes(type="log", title="trees (log scale)", tickvals=[1, 3, 10, 30, 100],
                     row=1, col=2)
    fig.update_yaxes(title="accuracy", range=[0.83, 0.9], row=1, col=2)
    fig.update_annotations(font_size=30)
    fig.update_layout(template="simple_white", width=1200, height=600, font=dict(family="Latin Modern Roman", size=26),
                      margin=dict(l=20, r=30, t=70, b=80))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".sweep_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(len(NS)):
        frame(k).write_image(tmp / f"{k:03d}.png")
    last = len(NS) - 1
    for k in range(len(NS), len(NS) + 5):                     # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "trees_sweep.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 3, 5, last)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "trees_sweep_frames.png")
    shutil.rmtree(tmp)
