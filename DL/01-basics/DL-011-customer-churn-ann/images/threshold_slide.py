"""The threshold as a slider, on the first churn network after its 10 epochs (data/prob_epochs.npz, last row: the
predicted probability of leaving for the 2,000 test customers). The threshold moves from 0.5 down to 0.1; at each
value we count who is predicted to leave and print accuracy, precision and recall. At 0.5 nobody is flagged; a lower
threshold finds leavers at the cost of false alarms. No retraining: only the cut changes.
Plotly frames (a line moving over fixed data) -> ffmpeg GIF, plus one key frame for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

HERE = Path(__file__).parent
D = np.load(HERE.parent / "data" / "prob_epochs.npz")
p, y = D["probs"][-1], D["y"]
assert p.shape == (2000,) and y.sum() == 415 and round(float(p.max()), 3) == 0.498
jit = np.random.default_rng(0).uniform(-0.32, 0.32, 2000)
CUTS = [0.5, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1]


def scores(t):
    pred = p > t
    tp, fp = int((pred & (y == 1)).sum()), int((pred & (y == 0)).sum())
    acc = 100 * (pred == y).mean()
    prec = 100 * tp / (tp + fp) if tp + fp else float("nan")
    return tp, fp, acc, prec, 100 * tp / 415


def frame(t):
    tp, fp, acc, prec, rec = scores(t)
    fig = go.Figure()
    for lab, c, yy in ((0, "#4C78A8", 0), (1, "#E45756", 1)):
        m = y == lab
        fig.add_scatter(x=p[m], y=yy + jit[m], mode="markers", marker=dict(size=5, color=c, opacity=0.5))
    fig.add_vrect(x0=t, x1=0.6, fillcolor="#F58518", opacity=0.12, line_width=0)
    fig.add_vline(x=t, line=dict(color="black", width=3, dash="dash"), opacity=1)
    fig.add_annotation(x=t + 0.005, y=1.62, text="predicted \"leaves\" →", showarrow=False, xanchor="left",
                       font=dict(size=18))
    ptxt = "no one flagged" if tp + fp == 0 else f"precision {prec:.0f}%"
    fig.update_layout(template="simple_white", width=1100, height=600, font=dict(family="Latin Modern Roman", size=21),
                      title=dict(text=f"threshold <b>{t:g}</b>: flags {tp + fp} customers ({tp} really left, {fp} stayed)"
                                      f"<br>accuracy {acc:.1f}%, {ptxt}, recall {rec:.0f}%", x=0.5, y=0.95,
                                 font=dict(size=21)),
                      xaxis=dict(title="predicted probability of leaving", range=[0, 0.6]),
                      yaxis=dict(tickvals=[0, 1], ticktext=["stayed", "left"], range=[-0.55, 1.8]),
                      showlegend=False, margin=dict(l=90, r=30, t=110, b=70))
    return fig


if __name__ == "__main__":
    for t in CUTS:
        print(t, [round(v, 1) if isinstance(v, float) else v for v in scores(t)])
    tmp = HERE / ".ts_frames"
    tmp.mkdir(exist_ok=True)
    keys, n = [], 0
    for t in CUTS:
        keys.append(tmp / f"t{t}.png")
        frame(t).write_image(keys[-1])
        for _ in range(3):
            shutil.copy(keys[-1], tmp / f"{n:03d}.png")
            n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=820:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "threshold_slide.gif")], check=True)
    shutil.copy(keys[CUTS.index(0.25)], HERE / "threshold_slide_frames.png")          # one key frame for the PDF
    shutil.rmtree(tmp)
