"""GELU built point by point as an average over dropout whose keep-probability depends on the input (section 6.3).
An input x is kept with probability Phi(x) (the standard normal CDF) and replaced by 0 otherwise, so its average
output is x * Phi(x) + 0 * (1 - Phi(x)) = x * Phi(x). Left: Phi with the current x marked. Right: the average output,
one dot per x = -2, -1, 0, 1, 2; then the whole GELU curve; then ReLU and SiLU = x * sigmoid(x) for comparison.
Idea after StatQuest, "The GELU, SiLU and SwiGLU activation functions". Plotly frames -> ffmpeg GIF + key frames."""
import shutil
import subprocess
from math import erf, sqrt
from pathlib import Path

import numpy as np
from PIL import Image
from plotly.subplots import make_subplots

from common import BLUE, GREEN, GREY, ORANGE, RED

HERE = Path(__file__).parent
Phi = np.vectorize(lambda t: 0.5 * (1 + erf(t / sqrt(2))))
x = np.linspace(-4, 4, 401)
gelu, silu, relu = x * Phi(x), x / (1 + np.exp(-x)), np.maximum(0, x)
PTS = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
OUT = PTS * Phi(PTS)
assert [round(float(v), 2) for v in OUT] == [-0.05, -0.16, 0.0, 0.84, 1.95], OUT
assert round(float(gelu.min()), 2) == -0.17
N = len(PTS)


def frame(k):
    """k < N: dots up to point k. k = N: the GELU curve. k = N + 1: ReLU and SiLU added."""
    j = min(k, N - 1)
    fig = make_subplots(1, 2, horizontal_spacing=0.13, subplot_titles=("probability of being kept, Φ(x)",
                                                                        "average output, x × Φ(x)"))
    fig.add_scatter(x=x, y=Phi(x), mode="lines", line=dict(color=BLUE, width=4, simplify=False), showlegend=False, row=1, col=1)
    if k < N:
        fig.add_scatter(x=[PTS[j], PTS[j]], y=[0, Phi(PTS[j])], mode="lines", line=dict(color=RED, width=3, dash="dot"),
                        showlegend=False, row=1, col=1)
        fig.add_scatter(x=[PTS[j]], y=[Phi(PTS[j])], mode="markers", marker=dict(size=16, color=RED), showlegend=False,
                        row=1, col=1)
        title = (f"x = {PTS[j]:g}: kept with probability {Phi(PTS[j]):.2f}, so the average output is "
                 f"{PTS[j]:g} × {Phi(PTS[j]):.2f} = {OUT[j]:.2f}").replace("-", "−")
    elif k == N:
        title = "Every x gives one dot: together they trace GELU(x) = x × Φ(x)"
    else:
        title = "GELU and SiLU are smooth versions of ReLU, with a small dip below 0"
    if k > N:
        fig.add_scatter(x=x, y=relu, mode="lines", name="ReLU", line=dict(color=GREY, width=3, dash="dash"), row=1, col=2)
        fig.add_scatter(x=x, y=silu, mode="lines", name="SiLU", line=dict(color=ORANGE, width=3, dash="dot"), row=1, col=2)
    if k >= N:
        fig.add_scatter(x=x, y=gelu, mode="lines", name="GELU", line=dict(color=GREEN, width=5, simplify=False), row=1, col=2)
    fig.add_scatter(x=PTS[:j + 1], y=OUT[:j + 1], mode="markers", marker=dict(size=16, color=GREEN,
                    line=dict(width=1, color="black")), showlegend=False, row=1, col=2)
    fig.add_hline(y=0, line=dict(color=GREY, width=1), row=1, col=2)
    fig.update_xaxes(title_text="input x", range=[-4, 4])
    fig.update_yaxes(range=[-0.05, 1.05], row=1, col=1)
    fig.update_yaxes(range=[-0.6, 3], row=1, col=2)
    fig.update_layout(template="simple_white", width=1250, height=600, font=dict(family="Latin Modern Roman", size=21),
                      title=dict(text=title, x=0.5, y=0.97, font=dict(size=22)), showlegend=k > N,
                      legend=dict(x=0.6, y=0.95, bgcolor="rgba(255,255,255,0.8)"), margin=dict(l=70, r=20, t=110, b=70))
    for a in fig.layout.annotations[:2]:
        a.font.size = 21
    return fig


if __name__ == "__main__":
    tmp = HERE / ".gelu_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for k in range(N + 2):
        keys.append(tmp / f"k{k}.png")
        frame(k).write_image(keys[-1])
    seq = [k for k in range(N + 2) for _ in range(3)] + [N + 1] * 4
    for i, k in enumerate(seq):
        shutil.copy(keys[k], tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1.5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "gelu_build.gif")], check=True)
    ims = [Image.open(keys[k]).convert("RGB") for k in (0, 3, N, N + 1)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "gelu_build_frames.png")
    shutil.rmtree(tmp)
    print("GELU at", PTS, "=", OUT.round(3), "SiLU", (PTS / (1 + np.exp(-PTS))).round(3), "min", gelu.min().round(3))
