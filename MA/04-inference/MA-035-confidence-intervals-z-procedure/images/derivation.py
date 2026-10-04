"""Section 8 in motion: why x_bar +- 2.94 works. The Notebook's population has mu = 28, sigma = 15, n = 100, so
x_bar follows N(28, 1.5^2) and lands within 2.94 of mu 95% of the time (blue band). The same distance read from the
other end: when x_bar is within 2.94 of mu, the interval x_bar +- 2.94 reaches mu. Two sample means from the
Notebook's simulation (seed 42): the first one, and the first one that falls outside the band.
Run: python derivation.py -> derivation.gif, derivation_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from scipy import stats

HERE = Path(__file__).parent
BLUE, GREEN, RED, GREY = "#4C78A8", "#54A24B", "#E45756", "#6B6B6B"
MU, SE = 28, 1.5
E = stats.norm.ppf(0.975) * SE
assert round(E, 2) == 2.94
means = np.random.default_rng(42).normal(28, 15, size=(100_000, 100)).mean(axis=1)
inside = np.abs(means - MU) <= E
assert round(inside.mean(), 2) == 0.95
picks = [means[0], means[np.argmax(~inside)]]
assert abs(picks[0] - MU) <= E < abs(picks[1] - MU)
x = np.linspace(21, 35, 600)
pdf = stats.norm(MU, SE).pdf(x)


def frame(stage, k=None, t=1.0):
    """stage 0: bell; 1: band; 2/3: sample k drops (t) then grows its interval (t)."""
    fig = go.Figure()
    fig.add_scatter(x=x, y=pdf, mode="lines", line=dict(color="black", width=3), showlegend=False)
    head = "x̄ follows N(μ, 1.5²) around μ = 28"
    if stage >= 1:
        xs = x[np.abs(x - MU) <= E]
        fig.add_scatter(x=xs, y=stats.norm(MU, SE).pdf(xs), fill="tozeroy", fillcolor="rgba(76,120,168,0.35)",
                        mode="lines", line=dict(width=0), showlegend=False)
        head = "95% of sample means land within 2.94 of μ: 25.06 to 30.94"
    fig.add_vline(x=MU, line=dict(color=GREY, width=2.5, dash="dash"))
    fig.add_annotation(x=MU, y=0.3, text="μ = 28", showarrow=False, xanchor="left", xshift=6, font=dict(size=20))
    for j, xb in enumerate(picks):
        if k is None or j > k:
            continue
        ok = abs(xb - MU) <= E
        c = GREEN if ok else RED
        row = -0.06 - 0.07 * j
        drop = 1.0 if (j < k or stage == 3) else t
        if j < k or stage == 3:
            grow = 1.0 if j < k else t
            fig.add_scatter(x=[xb - E * grow, xb + E * grow], y=[row, row], mode="lines", line=dict(color=c, width=8),
                            showlegend=False)
            if grow == 1.0:
                fig.add_annotation(x=xb + E + 0.1, y=row, xanchor="left", showarrow=False, font=dict(size=18, color=c),
                                   text=f"{xb - E:.2f} to {xb + E:.2f}: {'reaches' if ok else 'misses'} μ")
        fig.add_scatter(x=[xb], y=[0.30 * (1 - drop) + row * drop], mode="markers",
                        marker=dict(color=c, size=16, line=dict(color="black", width=1.5)), showlegend=False)
        if j == k:
            head = (f"x̄ = {xb:.2f} is {abs(xb - MU):.2f} from μ: {'inside' if ok else 'outside'} the band"
                    if stage == 2 else f"so x̄ ± 2.94 {'reaches' if ok else 'misses'} μ: the same distance, read from x̄")
    fig.update_layout(template="simple_white", width=960, height=560, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=head, x=0.5, font=dict(size=22)),
                      xaxis=dict(title="mean age of a sample of 100 (years)", range=[21, 35], dtick=1),
                      yaxis=dict(range=[-0.22, 0.32], visible=False), margin=dict(l=30, r=20, t=70, b=60))
    return fig


SEQ = [(0, None, 1)] * 4 + [(1, None, 1)] * 6
for k in (0, 1):
    SEQ += [(2, k, t) for t in np.linspace(0.1, 1, 6)] + [(2, k, 1)] * 6
    SEQ += [(3, k, t) for t in np.linspace(0.1, 1, 6)] + [(3, k, 1)] * 8

if __name__ == "__main__":
    tmp = HERE / ".derivation_frames"
    tmp.mkdir(exist_ok=True)
    for i, (st, k, t) in enumerate(SEQ):
        frame(st, k, t).write_image(tmp / f"{i:03d}.png")
    last = len(SEQ) - 1
    for i in range(last + 1, last + 10):
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "derivation.gif")], check=True)
    shutil.copy(tmp / f"{last:03d}.png", HERE / "derivation_frames.png")   # PDF: the final frame alone, readable at page width
    shutil.rmtree(tmp)
