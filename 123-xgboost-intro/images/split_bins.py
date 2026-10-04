"""Exact greedy versus approximate split finding on the Titanic fares (891 passengers, target Survived).
For every candidate threshold we compute the first XGBoost tree's gain for log loss, starting from the survival
rate p (g = p - y, h = p(1 - p), lambda = 1, the XGBoost default): S_left + S_right - S_parent, S = G^2 / (H + lambda).
The exact greedy algorithm tries all 247 midpoints between distinct fares. The approximate algorithm tries only
bin edges: quantile edges (as XGBoost places them; every h is equal here, so the weighted quantiles are the
ordinary ones) or, for comparison, equal-width edges. Frames: 4, 8, 16, 32, 64 bins.
Run: python split_bins.py  -> split_bins.gif, split_bins_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY = "#4C78A8", "#F58518", "#54A24B", "#9A9A9A"
df = pd.read_csv(HERE.parent / "data" / "titanic_train.csv")
fare, y = df.Fare.values, df.Survived.values
p = y.mean()
g, h, LAM = p - y, np.full(len(y), p * (1 - p)), 1.0
S = lambda m: g[m].sum() ** 2 / (h[m].sum() + LAM)
gain = lambda t: S(fare < t) + S(fare >= t) - S(np.ones(len(y), bool))
u = np.unique(fare)
exact = (u[:-1] + u[1:]) / 2
ge = np.array([gain(t) for t in exact])
BINS = [4, 8, 16, 32, 64]


def edges(b, kind):
    if kind == "quantile":
        return np.unique(np.quantile(fare, np.linspace(0, 1, b + 1)[1:-1]))
    return np.linspace(fare.min(), fare.max(), b + 1)[1:-1]


best = {(b, k): max(gain(t) for t in edges(b, k)) for b in BINS for k in ("quantile", "equal-width")}
assert len(exact) == 247 and np.isclose(ge.max(), 79.37, atol=0.01)
assert best[(8, "quantile")] / ge.max() > 0.97 and np.isclose(best[(32, "quantile")], ge.max())
assert all(best[(b, "equal-width")] < best[(b, "quantile")] for b in BINS)
print({k: round(v, 2) for k, v in best.items()})


def frame(b):
    fig = go.Figure(go.Scatter(x=exact, y=ge, mode="lines", line=dict(color=GREY, width=2.5),
                               name=f"exact greedy: all {len(exact)} midpoints, best {ge.max():.1f}"))
    for kind, c, sym in (("equal-width", BLUE, "square"), ("quantile", ORANGE, "circle")):
        e = edges(b, kind)
        e = e[e > 1]                                        # the log axis starts at fare 1
        fig.add_trace(go.Scatter(x=e, y=[gain(t) for t in e], mode="markers", marker=dict(color=c, size=13, symbol=sym,
                                 line=dict(color="white", width=1)),
                                 name=f"{kind} bins: {len(edges(b, kind))} edges tried, best {best[(b, kind)]:.1f}"))
    fig.add_trace(go.Scatter(x=fare[fare > 1], y=np.full((fare > 1).sum(), -6), mode="markers", showlegend=False,
                             marker=dict(color="black", size=9, symbol="line-ns-open", opacity=0.25)))
    fig.update_layout(template="simple_white", width=1100, height=640, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"{b} bins per feature", x=0.5, y=0.97, font=dict(size=26)),
                      xaxis=dict(title="fare threshold (log scale); ticks at the bottom = passengers", type="log",
                                 range=[0, np.log10(600)]),
                      yaxis=dict(title="gain of the split", range=[-10, 100]),
                      legend=dict(x=0.99, xanchor="right", y=0.99, bgcolor="rgba(255,255,255,0.9)", font=dict(size=19)),
                      margin=dict(l=80, r=20, t=70, b=70))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".bins_frames"
    tmp.mkdir(exist_ok=True)
    n, shots = 0, {}
    for b in BINS:
        frame(b).write_image(tmp / "src.png")
        for _ in range(14 if b == BINS[-1] else 8):
            shutil.copy(tmp / "src.png", tmp / f"{n:03d}.png"); n += 1
        shots[b] = Image.open(tmp / "src.png").convert("RGB")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "split_bins.gif")], check=True)
    ims = [shots[4], shots[32]]
    w, hh = ims[0].size
    sheet = Image.new("RGB", (w, 2 * hh + 16), "white")      # stacked: readable in the PDF
    for i, im in enumerate(ims):
        sheet.paste(im, (0, i * (hh + 16)))
    sheet.save(HERE / "split_bins_frames.png")
    shutil.rmtree(tmp)
