"""The decision surface as stumps are added, learning_rate 1.0 against 0.1, on the Note's circles split (Plotly frames).
Each panel is one model of 1,500 stumps; staged_predict gives its prediction after every stage.
Run: python grow.py  -> grow.gif, grow_frames.png"""
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.ensemble import AdaBoostClassifier

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import COLOURS, REGION, X_test, X_train, fit, y_test, y_train  # noqa: E402

N = 1500
STEPS = [1, 2, 3, 5, 8, 12, 20, 30, 50, 80, 150, 250, 500, 800, 1500]
xs = np.linspace(X_train[:, 0].min() - 0.2, X_train[:, 0].max() + 0.2, 160)
ys = np.linspace(X_train[:, 1].min() - 0.2, X_train[:, 1].max() + 0.2, 160)
XX, YY = np.meshgrid(xs, ys)
grid = np.c_[XX.ravel(), YY.ravel()]
runs = {}
for lr in (1.0, 0.1):
    m = AdaBoostClassifier(n_estimators=N, learning_rate=lr, random_state=42).fit(X_train, y_train)
    keep = set(STEPS)
    surf = {k + 1: z.reshape(XX.shape) for k, z in enumerate(m.staged_predict(grid)) if k + 1 in keep}
    tr = {k + 1: a for k, a in enumerate(m.staged_score(X_train, y_train)) if k + 1 in keep}
    te = {k + 1: a for k, a in enumerate(m.staged_score(X_test, y_test)) if k + 1 in keep}
    runs[lr] = surf, tr, te
    for n in (1, 50, 150, 500, 1500):                       # same model as Figure 1 (app.fit)
        _, title = fit(n, lr)
        if n in surf and (lr == 1.0 or n == 1500):
            assert title == f"train {tr[n]:.2f}, test {te[n]:.2f}", (lr, n, title)
assert f"{runs[0.1][2][1500]:.2f}" == "0.85"                 # the Note, section 4.3


def frame(n):
    fig = make_subplots(1, 2, horizontal_spacing=0.03, subplot_titles=[
        f"learning_rate {lr}<br>train {runs[lr][1][n]:.2f}, test {runs[lr][2][n]:.2f}" for lr in runs])
    for c, lr in enumerate(runs, start=1):
        fig.add_trace(go.Heatmap(x=xs, y=ys, z=runs[lr][0][n], zmin=0, zmax=1, colorscale=REGION, showscale=False), 1, c)
        for cls in (0, 1):
            k = y_train == cls
            fig.add_trace(go.Scatter(x=X_train[k, 0], y=X_train[k, 1], mode="markers", showlegend=False,
                                     marker=dict(color=COLOURS[cls], size=6, line=dict(color="white", width=0.5))), 1, c)
    fig.update_xaxes(range=[xs[0], xs[-1]], showticklabels=False)
    fig.update_yaxes(range=[ys[0], ys[-1]], showticklabels=False)
    fig.update_annotations(font_size=24)
    fig.update_layout(template="simple_white", width=1100, height=640, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"<b>{n} stump{'s' if n > 1 else ''}</b>", x=0.5, y=0.97, font_size=30),
                      margin=dict(l=10, r=10, t=130, b=10))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".grow_frames"
    tmp.mkdir(exist_ok=True)
    for i, n in enumerate(STEPS):
        frame(n).write_image(tmp / f"{i:03d}.png")
    last = len(STEPS) - 1
    for i in range(last + 1, last + 6):                     # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "grow.gif")], check=True)
    keys = [Image.open(tmp / f"{STEPS.index(n):03d}.png").convert("RGB") for n in (1, 50, 500, 1500)]
    keys[-1].save(HERE / "grow_frames.png")                # the PDF shows the last frame: a 2x2 grid was too small
    shutil.rmtree(tmp)
