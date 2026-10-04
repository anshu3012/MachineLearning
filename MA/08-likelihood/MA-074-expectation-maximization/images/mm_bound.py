"""EM as minorize-maximize, in one parameter. Mixture 0.5 N(mu1, 1.5^2) + 0.5 N(4, 1.5^2) on the seven points
-3, -2.5, -1, 0, 2, 4, 5; only mu1 is fitted, starting at 3. Black: the log-likelihood l(mu1). Orange: the lower
bound B(mu1) that the E-step builds at the current mu1 (it lies below l and touches it there). The M-step jumps to
the top of B; l goes up by at least as much as B did.
Run: python mm_bound.py -> mm_bound.gif, mm_bound_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from scipy import stats

from em_core import FONT, GREEN, GREY, ORANGE, RED

HERE = Path(__file__).parent
X = np.array([-3, -2.5, -1, 0, 2, 4, 5.0])
MU2, S = 4.0, 1.5
wd = lambda m: np.column_stack([0.5 * stats.norm(m, S).pdf(X), 0.5 * stats.norm(MU2, S).pdf(X)])
ll = lambda m: np.log(wd(m).sum(axis=1)).sum()


def bound(m, m_t):
    """B(m; m_t) = sum_n sum_k r_nk log(pi_k N_k(x_n) / r_nk), with r from m_t."""
    R = wd(m_t) / wd(m_t).sum(axis=1, keepdims=True)
    W = wd(m)
    with np.errstate(divide="ignore", invalid="ignore"):
        terms = np.where(R > 0, R * (np.log(W) - np.log(R)), 0.0)
    return terms.sum()


steps = [3.0]
for _ in range(4):
    R = wd(steps[-1]) / wd(steps[-1]).sum(axis=1, keepdims=True)
    steps.append((R[:, 0] @ X) / R[:, 0].sum())             # M-step for mu1: weighted mean
g = np.linspace(-4, 5, 500)
L = np.array([ll(v) for v in g])
for a, b in zip(steps, steps[1:]):                           # checks: bound below, touching, ascent
    B = np.array([bound(v, a) for v in g])
    assert np.all(B <= L + 1e-9) and abs(bound(a, a) - ll(a)) < 1e-9 and ll(b) >= ll(a)
    assert abs(g[B.argmax()] - b) < 0.02


def frame(t, phase):
    """phase 0: bound built at steps[t] (E-step); phase 1: jump to its top (M-step)."""
    fig = go.Figure(go.Scatter(x=g, y=L, mode="lines", line=dict(color="black", width=4), name="log-likelihood ℓ(μ₁)"))
    m_t = steps[t]
    fig.add_trace(go.Scatter(x=g, y=[bound(v, m_t) for v in g], mode="lines", line=dict(color=ORANGE, width=4),
                             name="lower bound B built at the current μ₁"))
    fig.add_trace(go.Scatter(x=steps[:t + 1], y=[ll(v) for v in steps[:t + 1]], mode="markers",
                             marker=dict(size=13, color=GREY), showlegend=False))
    fig.add_trace(go.Scatter(x=[m_t], y=[ll(m_t)], mode="markers", marker=dict(size=16, color=RED),
                             name="current μ₁ (bound touches ℓ here)"))
    label = f"step {t + 1}, E-step: build B at μ₁ = {m_t:.2f}"
    if phase == 1:
        nxt = steps[t + 1]
        fig.add_trace(go.Scatter(x=[nxt, nxt], y=[bound(nxt, m_t), ll(nxt)], mode="lines+markers",
                                 line=dict(color=GREEN, width=4), marker=dict(size=14, color=GREEN),
                                 name="M-step: top of B, then up to ℓ"))
        label = f"step {t + 1}, M-step: μ₁ = {nxt:.2f}, ℓ from {ll(m_t):.2f} to {ll(nxt):.2f}"
    fig.update_layout(template="simple_white", width=900, height=620, font=FONT,
                      title=dict(text=label, x=0.5, y=0.97), xaxis=dict(title="μ₁", range=[-4, 5]),
                      yaxis=dict(title="value", range=[-45, -14]), legend=dict(x=0.01, y=0.02, yanchor="bottom"),
                      margin=dict(l=70, r=20, t=70, b=60))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".mm_frames"
    tmp.mkdir(exist_ok=True)
    k = 0
    for t in range(4):
        for phase in (0, 0, 1, 1):
            frame(t, phase).write_image(tmp / f"{k:03d}.png")
            k += 1
    for j in range(k, k + 4):
        shutil.copy(tmp / f"{k - 1:03d}.png", tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "mm_bound.gif")], check=True)
    keys = [Image.open(tmp / f"{i:03d}.png").convert("RGB") for i in (0, 2, 4, 6)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "mm_bound_frames.png")
    shutil.rmtree(tmp)
    print([round(v, 3) for v in steps], [round(ll(v), 2) for v in steps])
