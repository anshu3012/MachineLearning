"""Solvers and stopping on the breast-cancer data (L2, C = 1), scored by the quantity every solver minimises:
mean log loss + ||w||^2 / (2 n C). Each point is a fresh fit stopped at max_iter = k (tol tiny so k decides).
solvers.png (section 3): five solvers, standardised features: different paths, the same minimum (0.0664).
max_iter.gif (section 4): lbfgs on raw vs standardised features: raw needs about 2,300 iterations, so the default
max_iter = 100 stops it early with a ConvergenceWarning; standardised converges in 19. (Plotly frames + ffmpeg)"""
import shutil
import subprocess
import warnings
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from sklearn.datasets import load_breast_cancer
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

warnings.simplefilter("ignore")
HERE = Path(__file__).parent
X, y = load_breast_cancer(return_X_y=True)
Xs = StandardScaler().fit_transform(X)
FONT = dict(family="Latin Modern Roman", size=22)


def obj(m, A):
    z = A @ m.coef_.ravel() + m.intercept_[0]
    return np.mean(np.logaddexp(0, -np.where(y == 1, z, -z))) + 0.5 * (m.coef_ ** 2).sum() / len(y)


def run(A, solver, ks):
    return [obj(LogisticRegression(solver=solver, max_iter=k, tol=1e-12).fit(A, y), A) for k in ks]


# section 3: solvers
ks = list(range(1, 21)) + list(range(25, 101, 5))
SOLV = {"lbfgs (default)": ("lbfgs", "#4C78A8"), "newton-cg": ("newton-cg", "#54A24B"),
        "liblinear": ("liblinear", "#B279A2"), "sag": ("sag", "#F58518"), "saga": ("saga", "#E45756")}
curves = {k: run(Xs, s, ks) for k, (s, _) in SOLV.items()}
best = min(v[-1] for v in curves.values())
assert round(best, 4) == 0.0664 and all(abs(v[-1] - best) < 1e-3 for v in curves.values())

# section 4: raw vs standardised, default settings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    LogisticRegression().fit(X, y)
assert any(issubclass(x.category, ConvergenceWarning) for x in w)          # raw features: the warning appears
n_raw = LogisticRegression(max_iter=10000).fit(X, y).n_iter_[0]
n_std = LogisticRegression().fit(Xs, y).n_iter_[0]
assert n_std == 19 and 2000 < n_raw < 2600, (n_std, n_raw)
kk = sorted(set(np.unique(np.geomspace(1, 3000, 45).astype(int))) | {100})
gap_raw = np.array(run(X, "lbfgs", kk)) - obj(LogisticRegression(max_iter=10000, tol=1e-12).fit(X, y), X)
gap_std = np.array(run(Xs, "lbfgs", kk)) - best
FLOOR = 1e-6
gap_raw, gap_std = np.maximum(gap_raw, FLOOR), np.maximum(gap_std, FLOOR)
print("iterations to converge: raw", n_raw, "standardised", n_std)


def solvers_png():
    fig = go.Figure()
    for name, (_, c) in SOLV.items():
        fig.add_trace(go.Scatter(x=ks, y=curves[name], mode="lines+markers", name=name, line=dict(color=c, width=3.5),
                                 marker=dict(size=6)))
    fig.add_hline(y=best, line=dict(color="black", dash="dot", width=2))
    fig.add_annotation(x=np.log10(2), y=best, yshift=-16, text=f"same minimum: {best:.4f}", showarrow=False)
    fig.update_layout(template="simple_white", width=1000, height=560, font=FONT,
                      xaxis=dict(title="iterations allowed (max_iter)", type="log", tickvals=[1, 2, 5, 10, 20, 50, 100]),
                      yaxis=dict(title="loss + L2 penalty", range=[0.05, 0.33]),
                      legend=dict(x=0.98, xanchor="right", y=0.98), margin=dict(l=80, r=30, t=30, b=70))
    fig.write_image(HERE / "solvers.png", scale=2)


def frame(j):
    fig = go.Figure()
    for g, name, c in ((gap_raw, f"raw features: converges after {n_raw:,}", "#E45756"),
                       (gap_std, f"standardised: converges after {n_std}", "#4C78A8")):
        fig.add_trace(go.Scatter(x=kk[:j + 1], y=g[:j + 1], mode="lines+markers", name=name,
                                 line=dict(color=c, width=4), marker=dict(size=7)))
    fig.add_vline(x=100, line=dict(color="black", dash="dash", width=2))
    fig.add_annotation(x=np.log10(100), y=-0.25, text="default max_iter = 100", showarrow=False, xanchor="left",
                       xshift=6)
    if kk[j] >= 100:
        i = kk.index(100)
        fig.add_annotation(x=np.log10(100), y=np.log10(gap_raw[i]), text="stopped here:<br>ConvergenceWarning",
                           showarrow=True, ax=-110, ay=110, font=dict(color="#E45756"))
    fig.update_layout(template="simple_white", width=1000, height=660, font=FONT,
                      title=dict(text=f"lbfgs, {kk[j]:,} iterations allowed", x=0.5, y=0.97),
                      xaxis=dict(title="iterations allowed (max_iter)", type="log", range=[0, np.log10(3500)]),
                      yaxis=dict(title="distance from the minimum", type="log", range=[-6.2, 0], exponentformat="power", dtick=1),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2), margin=dict(l=90, r=30, t=70, b=120))
    return fig


if __name__ == "__main__":
    solvers_png()
    tmp = HERE / ".maxiter_frames"
    tmp.mkdir(exist_ok=True)
    last = len(kk) - 1
    for j in range(last + 1):
        frame(j).write_image(tmp / f"{j:03d}.png")
    for j in range(last + 1, last + 13):
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=12,scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "max_iter.gif")], check=True)
    shutil.copy(tmp / f"{last:03d}.png", HERE / "max_iter_frames.png")      # the last frame holds both full curves
    shutil.rmtree(tmp)
