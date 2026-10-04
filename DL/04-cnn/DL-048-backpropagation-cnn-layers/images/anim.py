"""Sliding-window animation helper: a window moves over a grid of numbers and fills an output grid.
Used for convolution (kernel given) and max pooling (op="max"). Plotly frames -> ffmpeg GIF + a 2x2 key-frame PNG
for the PDF (pattern of MA/06-calculus/MA-064-hessian-and-multivariate-taylor/images/optimizer_race.py). Imported, not run."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from PIL import Image

from common import BLUE, ORANGE, GREEN, GREY, FONT

LIGHT = "#F2F2F2"


def _shade(v, lo, hi, base):
    """Mix white with the base colour by how large v is between lo and hi."""
    t = 0.0 if hi == lo else float(np.clip((v - lo) / (hi - lo), 0, 1))
    b = [int(base[i:i + 2], 16) for i in (1, 3, 5)]
    return "rgb({},{},{})".format(*[int(255 + (c - 255) * 0.75 * t) for c in b])


def _grid(fig, M, x0, y0, fill, fmt, fsize, pad_mask=None):
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M[i, j]
            col = LIGHT if (pad_mask is not None and pad_mask[i, j]) else ("white" if np.isnan(v) else fill(v))
            fig.add_shape(type="rect", x0=x0 + j, x1=x0 + j + 1, y0=y0 - i, y1=y0 - i - 1, line=dict(color=GREY, width=1),
                          fillcolor=col, layer="below")
            if not np.isnan(v):
                fig.add_annotation(x=x0 + j + 0.5, y=y0 - i - 0.5, text=fmt(v), showarrow=False,
                                   font=dict(family=FONT["family"], size=fsize, color="black"))


def _box(fig, x0, y0, r, c, h, w, color, width=7):
    fig.add_shape(type="rect", x0=x0 + c, x1=x0 + c + w, y0=y0 - r, y1=y0 - r - h, line=dict(color=color, width=width), fillcolor="rgba(0,0,0,0)")


def windows(X, f, stride):
    n_r, n_c = (X.shape[0] - f) // stride + 1, (X.shape[1] - f) // stride + 1
    return [(r * stride, c * stride, r, c) for r in range(n_r) for c in range(n_c)], (n_r, n_c)


def animate(name, X, f, *, kernel=None, op="conv", stride=1, pad=0, fmt=lambda v: f"{v:g}", fsize=16,
            keys=(0, 1, None, -1), here=None, hold=6, fps=1.5, width=1100, height=520, labels=None):
    """X: 2D input (before padding). f: window size. kernel: f x f weights for op='conv'. Writes name.gif, name_frames.png."""
    here = Path(here)
    Xp = np.pad(X.astype(float), pad)
    pad_mask = np.pad(np.zeros(X.shape, bool), pad, constant_values=True)
    wins, (n_r, n_c) = windows(Xp, f, stride)
    out = np.full((n_r, n_c), np.nan)
    lo, hi = np.nanmin(Xp), np.nanmax(Xp)
    vals = []
    for r0, c0, r, c in wins:
        patch = Xp[r0:r0 + f, c0:c0 + f]
        vals.append(float((patch * kernel).sum()) if op == "conv" else float(patch.max()))
    olo, ohi = min(vals + [0]), max(vals + [1e-9])
    gap = 1.5
    xk = Xp.shape[1] + gap                                       # kernel panel (conv only)
    xo = xk + (f + gap if op == "conv" else 0)                   # output panel
    labels = labels or ("input" + (" (zero-padded)" if pad else ""), "filter", "feature map" if op == "conv" else "pooled map")

    def frame(k):
        fig = go.Figure()
        cur = out.copy()
        for kk in range(k + 1):
            cur[wins[kk][2], wins[kk][3]] = vals[kk]
        _grid(fig, Xp, 0, 0, lambda v: _shade(v, lo, hi, BLUE), fmt, fsize, pad_mask)
        if op == "conv":
            _grid(fig, kernel.astype(float), xk, 0, lambda v: _shade(abs(v), 0, np.abs(kernel).max(), ORANGE), fmt, fsize)
        _grid(fig, cur, xo, 0, lambda v: _shade(v, olo, ohi, GREEN), fmt, fsize)
        r0, c0, r, c = wins[k]
        _box(fig, 0, 0, r0, c0, f, f, ORANGE)
        _box(fig, xo, 0, r, c, 1, 1, ORANGE)
        for idx, (x, lab) in enumerate(((0, labels[0]), (xk, labels[1]), (xo, labels[2]))):
            if lab is None or (idx == 1 and op != "conv"):
                continue
            fig.add_annotation(x=x, y=0.35, text=lab, showarrow=False, xanchor="left", yanchor="bottom",
                               font=dict(family=FONT["family"], size=19, color=GREY))
        patch = Xp[r0:r0 + f, c0:c0 + f]
        if op == "conv":
            terms = " + ".join(f"({fmt(a)})({fmt(b)})" for a, b in zip(patch.ravel(), kernel.ravel()) if a != 0 and b != 0)
            txt = f"window {k + 1} of {len(wins)}: sum of products = {terms or '0'} = {fmt(vals[k])}"
        else:
            txt = f"window {k + 1} of {len(wins)}: max({', '.join(fmt(a) for a in patch.ravel())}) = {fmt(vals[k])}"
        if len(txt) > 85:
            txt = f"window {k + 1} of {len(wins)}: sum of the {f * f} products = {fmt(vals[k])}"
        W = xo + n_c
        fig.update_layout(template="simple_white", width=width, height=height, font=FONT, showlegend=False,
                          title=dict(text=txt, x=0.5, y=0.97, font=dict(size=18)),
                          xaxis=dict(visible=False, range=[-0.3, W + 0.3], scaleanchor="y"),
                          yaxis=dict(visible=False, range=[-Xp.shape[0] - 0.3, 1.2]), margin=dict(l=10, r=10, t=60, b=10))
        return fig

    tmp = here / f".{name}_frames"
    tmp.mkdir(exist_ok=True)
    pio.write_images([frame(k) for k in range(len(wins))], [tmp / f"{k:03d}.png" for k in range(len(wins))],
                     width=width, height=height)
    last = len(wins) - 1
    for k in range(len(wins), len(wins) + hold):
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse", str(here / f"{name}.gif")],
                   check=True)
    ks = [len(wins) // 2 if k is None else (k % len(wins)) for k in keys]
    imgs = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in ks]
    w, h = imgs[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(imgs):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(here / f"{name}_frames.png")
    shutil.rmtree(tmp)
    return np.array(vals).reshape(n_r, n_c)
