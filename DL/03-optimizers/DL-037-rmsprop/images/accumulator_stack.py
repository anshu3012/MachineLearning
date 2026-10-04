"""The accumulator v of the bias b as a stack of squared gradients, AdaGrad (left) and RMSProp (right), learning
rate 0.2 on the students data. AdaGrad adds every g^2 and keeps it; RMSProp adds (1 - beta) g^2 and shrinks every
older block by beta at each step, so its stack rises and then melts as the gradients shrink.
Run: python accumulator_stack.py -> accumulator_stack.gif, accumulator_stack_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from common import GREEN, PURPLE, FONT
from shared import ETA, grad, run

HERE = Path(__file__).parent
BETA = 0.9
RUNS = {}
for kind in ("adagrad", "rmsprop"):
    P, V = run(kind)
    RUNS[kind] = (np.array([grad(p)[1] for p in P[:-1]]) ** 2, V[:, 1])   # squared gradients of b, and v of b


def blocks(kind, k):
    """Heights of the blocks that make up v after step k (oldest first)."""
    g2 = RUNS[kind][0][:k]
    return g2.copy() if kind == "adagrad" else (1 - BETA) * BETA ** np.arange(k - 1, -1, -1) * g2


for kind in RUNS:
    assert np.allclose([blocks(kind, k).sum() for k in (1, 10, 300)], RUNS[kind][1][[0, 9, 299]])
assert np.allclose(RUNS["adagrad"][1][[0, 9, 299]], [253.5, 2171.2, 20654.3], atol=0.1)   # numbers in the Note
STEPS = [*range(1, 16), 20, 25, 30, 40, 50, 60, 80, 100, 150, 200, 250, 300]
TOP = {"adagrad": 23000, "rmsprop": 100}


def frame(k):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.18,
                        subplot_titles=("AdaGrad: v = sum of all g²", "RMSProp: v = EWMA of g²"))
    fig.update_annotations(font_size=26, yshift=12)
    for col, (kind, colour) in enumerate((("adagrad", GREEN), ("rmsprop", PURPLE)), start=1):
        h = blocks(kind, k)
        age = np.arange(k - 1, -1, -1)
        fig.add_trace(go.Bar(x=np.zeros(k), y=h, base=np.cumsum(h) - h, width=0.7, showlegend=False,
                             marker=dict(color=colour, opacity=np.where(age == 0, 1.0, 0.45),
                                         line=dict(color="white", width=0.6 if k < 40 else 0))), 1, col)
        v = h.sum()
        fig.add_annotation(x=0, y=TOP[kind] * 0.97, text=f"v = {v:,.0f}" if v >= 10 else f"v = {v:.2f}",
                           showarrow=False, font=dict(size=28, color=colour), row=1, col=col)
        fig.add_annotation(x=0, y=-0.1, yref="y domain" if col == 1 else "y2 domain", yanchor="top",
                           text=f"learning rate η/√v = {ETA / np.sqrt(v):.4f}", showarrow=False,
                           font=dict(size=24), row=1, col=col)
        fig.update_yaxes(range=[0, TOP[kind]], title_text="v of b", row=1, col=col)
        fig.update_xaxes(range=[-0.8, 0.8], showticklabels=False, ticks="", row=1, col=col)
    fig.update_layout(template="simple_white", width=1000, height=640, font=dict(FONT, size=22), barmode="overlay",
                      title=dict(text=f"step {k}: the newest block is dark", x=0.5, y=0.97),
                      margin=dict(l=90, r=30, t=120, b=90))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".stack_frames"
    tmp.mkdir(exist_ok=True)
    for i, k in enumerate(STEPS):
        frame(k).write_image(tmp / f"{i:03d}.png")
    last = len(STEPS) - 1
    for i in range(last + 1, last + 9):                    # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "accumulator_stack.gif")], check=True)
    keys = [Image.open(tmp / f"{STEPS.index(k):03d}.png").convert("RGB") for k in (1, 10, 50, 300)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "accumulator_stack_frames.png")
    shutil.rmtree(tmp)
