"""KDE built step by step on the six points of section 5.1 (2, 2.5, 3, 4, 8, 8.5): a Gaussian bump of bandwidth 1
drops onto each point and the running sum (orange) grows; the KDE at x = 3 reads 0.206. Then the bandwidth sweeps
from 0.2 to 3: thin bumps give six spikes, wide bumps merge the two groups into one hill.
Run: python kde_anim.py -> kde_anim.gif, kde_anim_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, RED = "#4C78A8", "#F58518", "#E45756"
PTS = np.array([2, 2.5, 3, 4, 8, 8.5])
X = np.linspace(-1, 11.5, 600)
YMAX = 0.36


def bumps(h):
    return np.array([stats.norm.pdf((X - p) / h) / (len(PTS) * h) for p in PTS])


assert abs(bumps(1.0).sum(axis=0)[np.argmin(abs(X - 3))] - 0.206) < 0.002     # the Note's worked value


def frame(h, landed, drop=None, lift=0.0, probe=False):
    """landed: bumps already in the sum; drop: index of the bump falling, `lift` above its resting place."""
    B = bumps(h)
    fig = go.Figure()
    for i in range(landed):
        fig.add_scatter(x=X, y=B[i], mode="lines", line=dict(color=BLUE, width=2, dash="dot"))
    if drop is not None:
        fig.add_scatter(x=X, y=B[drop] + lift, mode="lines", line=dict(color=BLUE, width=3.5))
    if landed:
        fig.add_scatter(x=X, y=B[:landed].sum(axis=0), mode="lines", line=dict(color=ORANGE, width=5))
    fig.add_scatter(x=PTS, y=np.full(len(PTS), -0.012), mode="markers",
                    marker=dict(symbol="line-ns-open", size=18, color="black", line=dict(width=3)))
    if probe:
        y3 = B.sum(axis=0)[np.argmin(abs(X - 3))]
        fig.add_shape(type="line", x0=3, x1=3, y0=0, y1=y3, line=dict(color=RED, dash="dash", width=3))
        fig.add_annotation(x=3, y=y3, text=f"KDE at 3: {y3:.3f}", ax=90, ay=-40, font=dict(size=24, color=RED),
                           arrowcolor=RED, arrowwidth=2)
    if landed == 0 and drop is None:
        title = "<b>six data points</b>"
    elif drop is not None or landed < len(PTS):
        title = f"<b>bump {min(landed + (drop is not None), 6)} of 6 drops on its point</b>"
    else:
        title = f"<b>bandwidth h = {h:.2f}</b>"
    fig.update_layout(template="simple_white", width=900, height=560, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=24), title=dict(text=title, x=0.5, y=0.95),
                      xaxis=dict(title="x", range=[-1, 11.5], dtick=1), margin=dict(l=90, r=30, t=80, b=70),
                      yaxis=dict(title="density", range=[-0.03, YMAX]))
    if h == 1.0:                                                    # label the sum only while it is built
        fig.add_annotation(x=6, y=0.32, text="<b>KDE = sum of bumps</b>", showarrow=False, xanchor="center",
                           font=dict(size=22, color=ORANGE))
    return fig


def plan():
    out = [dict(h=1.0, landed=0)] * 2
    for i in range(len(PTS)):
        out += [dict(h=1.0, landed=i, drop=i, lift=l) for l in (0.2, 0.12, 0.05, 0.0)]
        out += [dict(h=1.0, landed=i + 1)]
    out += [dict(h=1.0, landed=6, probe=True)] * 10
    sweep = np.concatenate([np.geomspace(1.0, 0.2, 10), np.geomspace(0.2, 3.0, 22), np.geomspace(3.0, 1.0, 10)])
    out += [dict(h=float(h), landed=6) for h in sweep]
    out += [dict(h=1.0, landed=6)] * 8
    return out


if __name__ == "__main__":
    tmp = HERE / ".kde_frames"
    tmp.mkdir(exist_ok=True)
    frames = plan()
    for j, kw in enumerate(frames):
        frame(**kw).write_image(tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "kde_anim.gif")], check=True)
    first_sweep = next(j for j, kw in enumerate(frames) if kw["h"] != 1.0)
    pick = [8, frames.index(dict(h=1.0, landed=6, probe=True)), first_sweep + 8, first_sweep + 30]   # h = 0.2, h = 3
    keys = [Image.open(tmp / f"{j:03d}.png").convert("RGB") for j in pick]
    w, hh = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * hh + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (hh + 16)))
    sheet.save(HERE / "kde_anim_frames.png")
    shutil.rmtree(tmp)
