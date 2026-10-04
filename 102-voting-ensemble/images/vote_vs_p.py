"""Assumption 2 as a moving picture (Plotly frames + ffmpeg): each of three independent models is right with
probability p; p sweeps from 0.30 to 0.80. Left: the vote's accuracy p^3 + 3p^2(1 - p) against p, with the line
"vote = one model". Right: one model against the vote at the current p.
Run: python vote_vs_p.py -> vote_vs_p.gif, vote_vs_p_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

HERE = Path(__file__).parent
vote = lambda p: p**3 + 3 * p**2 * (1 - p)
assert round(vote(0.7), 3) == 0.784 and round(vote(0.3), 3) == 0.216 and vote(0.5) == 0.5   # section 5 numbers
PS = np.round(np.arange(0.30, 0.801, 0.025), 3)
grid = np.linspace(0.3, 0.8, 200)


def frame(p):
    v = vote(p)
    better = v > p + 1e-12
    c = "#54A24B" if better else ("#6B6B6B" if abs(v - p) < 1e-12 else "#E45756")
    fig = make_subplots(1, 2, column_widths=[0.6, 0.4], horizontal_spacing=0.14)
    fig.add_trace(go.Scatter(x=grid, y=grid, mode="lines", line=dict(color="#6B6B6B", dash="dash", width=2),
                             name="one model"), 1, 1)
    fig.add_trace(go.Scatter(x=grid, y=vote(grid), mode="lines", line=dict(color="#4C78A8", width=4),
                             name="vote of three"), 1, 1)
    fig.add_trace(go.Scatter(x=[p, p], y=[p, v], mode="lines+markers", line=dict(color=c, width=4),
                             marker=dict(size=14, color=c), showlegend=False), 1, 1)
    fig.add_trace(go.Bar(x=["one model", "vote"], y=[p, v], marker_color=["#6B6B6B", c], showlegend=False,
                         text=[f"{p:.2f}", f"{v:.3f}"], textposition="outside"), 1, 2)
    fig.update_xaxes(title="accuracy p of each model", range=[0.28, 0.82], row=1, col=1)
    fig.update_yaxes(title="accuracy", range=[0.1, 0.95], row=1, col=1)
    fig.update_yaxes(range=[0, 1.05], row=1, col=2)
    word = "vote helps" if better else ("no gain" if c == "#6B6B6B" else "vote hurts")
    fig.update_layout(template="simple_white", width=1100, height=560, font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text=f"p = {p:.2f}: {word}", x=0.5, font=dict(color=c, size=30)),
                      legend=dict(x=0.02, y=0.98), margin=dict(l=90, r=20, t=80, b=70))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".vp_frames"
    tmp.mkdir(exist_ok=True)
    j = 0
    keys = {}
    for p in PS:
        frame(p).write_image(tmp / "f.png")
        hold = 6 if p in (0.3, 0.5, 0.7, 0.8) else 1
        for _ in range(hold):
            shutil.copy(tmp / "f.png", tmp / f"{j:03d}.png")
            j += 1
        if p in (0.3, 0.5, 0.7, 0.8):
            keys[p] = Image.open(tmp / "f.png").convert("RGB")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=8,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "vote_vs_p.gif")], check=True)
    ims = list(keys.values())
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for n, im in enumerate(ims):
        sheet.paste(im, ((n % 2) * (w + 16), (n // 2) * (h + 16)))
    sheet.save(HERE / "vote_vs_p_frames.png")
    shutil.rmtree(tmp)
