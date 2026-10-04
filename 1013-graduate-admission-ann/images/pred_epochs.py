"""The second admission network (7-7-7-1) learning: predicted against actual chance of admission for the 100 test
students after 0, 1, 2, 3, 5, 10, 20, 50 and 100 epochs, with the test R² of each. From data/pred_epochs.npz
(experiments/pred_epochs.py: the Notebook's seed and steps; the final R² equals the Note's 0.80).
Plotly frames -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from sklearn.metrics import r2_score

HERE = Path(__file__).parent
D = np.load(HERE.parent / "data" / "pred_epochs.npz")
E, y, P = D["epochs"], D["y"], D["preds"]
R2 = [r2_score(y, p) for p in P]
assert round(R2[-1], 2) == 0.80 and R2[0] < -5 and round(R2[E.tolist().index(10)], 2) == -0.34


def frame(i):
    fig = go.Figure()
    fig.add_scatter(x=[0.3, 1.05], y=[0.3, 1.05], mode="lines", line=dict(color="#8A8A8A", dash="dash", width=2),
                    showlegend=False)
    fig.add_hline(y=y.mean(), line=dict(color="#F58518", width=2, dash="dot"), opacity=1)
    fig.add_annotation(x=0.32, y=y.mean() + 0.025, text=f"always the average ({y.mean():.3f}): R² = 0",
                       showarrow=False, xanchor="left", font=dict(size=16, color="#F58518"))
    fig.add_scatter(x=y, y=np.clip(P[i], -0.5, 1.6), mode="markers", showlegend=False,
                    marker=dict(size=11, color="#4C78A8", opacity=0.8, line=dict(width=1, color="white")))
    fig.update_layout(template="simple_white", width=820, height=800, font=dict(family="Latin Modern Roman", size=21),
                      title=dict(text=f"After {E[i]} epoch{'s' if E[i] != 1 else ''}: test R² = <b>{R2[i]:.2f}</b>",
                                 x=0.5, y=0.96, font=dict(size=24)),
                      xaxis=dict(title="actual chance of admission", range=[0.3, 1.05]),
                      yaxis=dict(title="predicted chance", range=[-0.1, 1.15]),
                      margin=dict(l=80, r=30, t=80, b=70))
    return fig


if __name__ == "__main__":
    print([(int(e), round(r, 3)) for e, r in zip(E, R2)])
    tmp = HERE / ".pe_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for i in range(len(E)):
        keys.append(tmp / f"k{i}.png")
        frame(i).write_image(keys[-1])
    seq = [i for i in range(len(E)) for _ in range(2)] + [len(E) - 1] * 5
    for j, i in enumerate(seq):
        shutil.copy(keys[i], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=680:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "pred_epochs.gif")], check=True)
    ims = [Image.open(keys[E.tolist().index(e)]).convert("RGB") for e in (5, 20, 100)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (3 * w + 32, h), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "pred_epochs_frames.png")
    shutil.rmtree(tmp)
