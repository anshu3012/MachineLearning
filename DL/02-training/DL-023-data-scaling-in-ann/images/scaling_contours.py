"""Loss contours before and after scaling, with the gradient-descent path (Plotly frames).
Model: one sigmoid neuron (logistic regression) on the Note's 320 training users, age and salary -> Purchased,
binary cross-entropy. We draw the loss over the two input weights, with the bias held at its best value.
Left: age in years, salary in thousands of rupees (raw salary in rupees is far worse, see the printed ratio).
Right: both standardized. Both start at w = (0, 0), learning rate 1 / (largest curvature at the minimum),
equal axis scales so the shape of the contours is true.
Run: python scaling_contours.py -> scaling_contours.gif, scaling_contours_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from common import BLUE, RED

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
df = pd.read_csv(HERE.parent / "data" / "Social_Network_Ads.csv")
X, y = df[["Age", "EstimatedSalary"]].values.astype(float), df["Purchased"].values
Xtr, _, ytr, _ = train_test_split(X, y, test_size=0.2, random_state=42)    # the Notebook's split
sig = lambda z: 1 / (1 + np.exp(-z))
N = 90


def setup(A):
    m = LogisticRegression(C=np.inf, max_iter=100000, tol=1e-12).fit(A, ytr)
    w_star, b = m.coef_[0], m.intercept_[0]
    p = sig(A @ w_star + b)
    ev = np.linalg.eigvalsh((A * (p * (1 - p))[:, None]).T @ A / len(A))   # curvatures of the loss at the minimum
    loss = lambda w: -np.mean(ytr * np.log(sig(A @ w + b) + 1e-12) + (1 - ytr) * np.log(1 - sig(A @ w + b) + 1e-12))
    lr, w, path = 1 / ev[-1], np.zeros(2), [np.zeros(2)]
    for _ in range(2000):
        w = w - lr * A.T @ (sig(A @ w + b) - ytr) / len(A)
        path.append(w)
    path = np.array(path)
    near = next((k for k, q in enumerate(path) if loss(q) - loss(w_star) < 1e-3), None)   # steps to get close
    return dict(A=A, b=b, w_star=w_star, ev=ev, loss=loss, path=path, near=near)


thou = setup(Xtr / [1, 1000])
std = setup((Xtr - Xtr.mean(0)) / Xtr.std(0))
R = setup(Xtr)
rupees = R["ev"]
assert np.allclose(thou["path"][-1], thou["w_star"], atol=1e-3) and np.allclose(std["path"][-1], std["w_star"], atol=1e-3)
assert std["near"] < thou["near"]
print("curvature ratio (narrowness): rupees %.0f, thousands %.1f, standardized %.2f" %
      (rupees[1] / rupees[0], thou["ev"][1] / thou["ev"][0], std["ev"][1] / std["ev"][0]))
print("steps to within 0.001 of the minimum loss: rupees", R["near"], "(of 2000) thousands", thou["near"], "standardized", std["near"])

PANELS = [(thou, (-0.02, 0.26), (-0.07, 0.19), "salary in thousands", RED),
          (std, (-0.4, 4.6), (-1.0, 3.2), "both standardized", BLUE)]
for P, xr, yr, *_ in PANELS:                                 # contour grid per panel
    gx, gy = np.linspace(*xr, 160), np.linspace(*yr, 160)
    P["grid"] = (gx, gy, np.log10(np.array([[P["loss"](np.array([a, c])) for a in gx] for c in gy])))


def frame(k):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1, subplot_titles=[
        f"{t}: {P['near']} steps" if k >= P["near"] else t for P, _, _, t, _ in PANELS])
    for i, (P, xr, yr, _, c) in enumerate(PANELS, start=1):
        gx, gy, Z = P["grid"]
        lo = np.log10(P["loss"](P["w_star"]))
        fig.add_trace(go.Contour(x=gx, y=gy, z=Z, colorscale="Greys", reversescale=True, showscale=False, opacity=0.5,
                                 contours=dict(start=lo + 0.003, end=Z.max(), size=(Z.max() - lo) / 14), line=dict(width=0.7)), 1, i)
        Q = P["path"][:k + 1]
        fig.add_trace(go.Scatter(x=Q[:, 0], y=Q[:, 1], mode="lines+markers", line=dict(color=c, width=3),
                                 marker=dict(size=7, color=c)), 1, i)
        fig.add_trace(go.Scatter(x=[P["w_star"][0]], y=[P["w_star"][1]], mode="markers",
                                 marker=dict(symbol="star", size=22, color="black")), 1, i)
        fig.update_xaxes(title="age weight", range=xr, row=1, col=i)
        fig.update_yaxes(title="salary weight", range=yr, scaleanchor=f"x{'' if i == 1 else i}", scaleratio=1,
                         row=1, col=i)
    fig.update_layout(template="simple_white", width=1150, height=600, font=FONT, showlegend=False,
                      title=dict(text=f"step {k}", x=0.5, y=0.97), margin=dict(l=80, r=30, t=110, b=70))
    fig.update_annotations(font_size=24)
    return fig


if __name__ == "__main__":
    from surftilt import tilt_gif                              # the two loss surfaces, tilting down to the maps of the gif
    def pane(P, xr, yr, t, c):
        gx, gy, Zl = P["grid"]
        lo = np.log10(P["loss"](P["w_star"]))
        Q = P["path"][:N + 1:3]
        print(t, "log10 loss at start (0, 0):", round(float(np.log10(P["loss"](np.zeros(2)))), 2), "at minimum:", round(float(lo), 2))
        return dict(x=gx[::2], y=gy[::2], Z=Zl[::2, ::2], xlab="age weight", ylab="salary weight", zlab="log10 loss", cscale="Greys",
                    reverse=True, title=t, contours=dict(start=float(lo + 0.003), end=float(Zl.max()), size=float((Zl.max() - lo) / 14)),
                    zrange=(float(min(np.log10(T["loss"](T["w_star"])) for T, *_ in PANELS)), float(max(T["grid"][2].max() for T, *_ in PANELS))),
                    marks=[dict(x=Q[:, 0], y=Q[:, 1], z=[float(np.log10(P["loss"](q))) for q in Q], color=c, size=3),
                           dict(x=[0], y=[0], z=[float(np.log10(P["loss"](np.zeros(2))))], color="black", size=7, line=False),
                           dict(x=[P["w_star"][0]], y=[P["w_star"][1]], z=[float(lo)], color="black", size=9, symbol="diamond", line=False)])
    tilt_gif("loss_surfaces", HERE, [pane(P, xr, yr, t, c) for P, xr, yr, t, c in PANELS], zasp=0.6, floor=0.3)
    tmp = HERE / ".contour_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(N + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(N + 1, N + 13):                           # hold the last frame
        shutil.copy(tmp / f"{N:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "8", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "scaling_contours.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (1, 5, 30, N)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "scaling_contours_frames.png")
    shutil.rmtree(tmp)
