"""The first churn network (11-3-1, sigmoid) during its 10 epochs: the predicted probability of leaving for each of
the 2,000 test customers, split by what really happened. From data/prob_epochs.npz (experiments/prob_epochs.py,
the Notebook's seed and steps). Every probability stays below the 0.5 threshold, so the network predicts "stays"
for everyone. Plotly frames -> ffmpeg GIF, plus the final frame for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
D = np.load(HERE.parent / "data" / "prob_epochs.npz")
P, y, LOSS = D["probs"], D["y"], D["loss"]
assert P.shape == (11, 2000) and y.sum() == 415
assert round(float(P[-1].max()), 3) == 0.498 and round(float(LOSS[-1]), 3) == 0.429
jit = np.random.default_rng(0).uniform(-0.32, 0.32, 2000)


def frame(e):
    p = P[e]
    fig = go.Figure()
    for lab, c, name, yy in ((0, "#4C78A8", "stayed (1,585)", 0), (1, "#E45756", "left (415)", 1)):
        m = y == lab
        fig.add_scatter(x=p[m], y=yy + jit[m], mode="markers", name=name, marker=dict(size=5, color=c, opacity=0.5))
    fig.add_vline(x=0.5, line=dict(color="black", width=3, dash="dash"), opacity=1)
    fig.add_annotation(x=0.51, y=1.62, text="threshold 0.5: above it, predict \"leaves\"", showarrow=False,
                       xanchor="left", font=dict(size=17))
    flagged = int((p > 0.5).sum())
    head = "Before training" if e == 0 else f"After epoch {e}: training loss {LOSS[e - 1]:.3f}"
    fig.update_layout(template="simple_white", width=1100, height=560, font=dict(family="Latin Modern Roman", size=21),
                      title=dict(text=f"{head}; highest probability {p.max():.3f}; predicted to leave: <b>{flagged}</b>",
                                 x=0.5, y=0.94, font=dict(size=20)),
                      xaxis=dict(title="predicted probability of leaving", range=[0, 1]),
                      yaxis=dict(tickvals=[0, 1], ticktext=["stayed", "left"], range=[-0.55, 1.8]),
                      showlegend=False, margin=dict(l=90, r=30, t=80, b=70))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".pe_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for e in range(11):
        keys.append(tmp / f"e{e}.png")
        frame(e).write_image(keys[-1])
    seq = [0] * 3 + [e for e in range(1, 11) for _ in range(2)] + [10] * 5
    for j, e in enumerate(seq):
        shutil.copy(keys[e], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=820:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "prob_epochs.gif")], check=True)
    shutil.copy(keys[10], HERE / "prob_epochs_frames.png")
    shutil.rmtree(tmp)
    print([round(float(P[e].max()), 3) for e in range(11)], [round(float(P[e].mean()), 3) for e in range(11)])
