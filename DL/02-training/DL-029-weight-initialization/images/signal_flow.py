"""Tanh activations of a wide network, layer by layer, for three starting spreads (Plotly frames + ffmpeg).
Same recipe as the Notebook's numpy experiment (1000 rows of 500 standard-normal inputs, 500-node layers, biases 0,
one generator with seed 0), run for 10 layers instead of 3: weights 0.01 x randn shrink the signal to 0,
randn / sqrt(500) (Xavier for 500 in, 500 out) stays in range (std 0.63 to 0.23, as in Note DL-030), 1 x randn pushes every value to -1 or 1.
Run: python signal_flow.py  -> signal_flow.gif, signal_flow_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from common import BLUE, GREEN, RED

HERE = Path(__file__).parent
LAYERS = 10
STARTS = (("0.01 × randn: shrinks to 0", 0.01, BLUE), ("randn / √500 (Xavier): stays in range", 1 / np.sqrt(500), GREEN),
          ("1 × randn: stuck at −1 and 1", 1.0, RED))


def forward(scale, seed=0):
    rng = np.random.default_rng(seed)
    a, out = rng.standard_normal((1000, 500)), []
    for _ in range(LAYERS):
        a = np.tanh(a @ (rng.standard_normal((500, 500)) * scale))
        out.append(a.ravel())
    return out


acts = {s: forward(s) for _, s, _ in STARTS}
small, large = acts[0.01], acts[1.0]
assert np.allclose([o.std() for o in small[:3]], [0.21, 0.048, 0.011], rtol=0.05)   # the Note's section 6.1 numbers
assert abs(np.mean(np.abs(large[2]) > 0.99) - 0.90) < 0.01                           # the Note's section 7 number
EDGES = np.linspace(-1.075, 1.075, 44)                                               # bins of 0.05, one centred on 0
YMAX = {0.01: 1.0, 1 / np.sqrt(500): 0.1, 1.0: 0.6}                                  # one fixed scale per row


def sci(x):
    m, e = f"{x:.0e}".split("e")
    return f"{m}×10" + str(int(e)).translate(str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹"))


def frame(layer):
    fig = make_subplots(rows=3, cols=1, vertical_spacing=0.13, subplot_titles=[t for t, _, _ in STARTS])
    for r, (title, s, c) in enumerate(STARTS, start=1):
        v = acts[s][layer - 1]
        share = np.histogram(v, EDGES)[0] / v.size
        fig.add_trace(go.Bar(x=(EDGES[:-1] + EDGES[1:]) / 2, y=share, width=0.045, marker_color=c, showlegend=False),
                      row=r, col=1)
        sat = np.mean(np.abs(v) > 0.99)
        sd = v.std()
        label = "spread (std) " + (f"{sd:.2g}" if sd >= 1e-3 else sci(sd)) + (f"<br>{sat:.0%} beyond ±0.99" if sat > 0.05 else "")
        fig.add_annotation(x=0 if s == 1.0 else 1.0, y=0.92 * YMAX[s], text=label, xanchor="center" if s == 1.0 else "right", yanchor="top", showarrow=False,
                           align="center" if s == 1.0 else "right", font=dict(size=22, color=c), row=r, col=1)
        fig.update_yaxes(range=[0, YMAX[s]], showticklabels=False, ticks="", row=r, col=1)
        fig.update_xaxes(range=[-1.1, 1.1], tickvals=[-1, -0.5, 0, 0.5, 1], row=r, col=1)
    fig.update_xaxes(title_text="tanh activation", row=3, col=1)
    fig.update_layout(template="simple_white", width=900, height=900, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"hidden layer {layer} of {LAYERS}", x=0.5, y=0.975, font=dict(size=28)),
                      margin=dict(l=40, r=30, t=110, b=70), bargap=0)
    fig.update_annotations(selector=dict(text=STARTS[0][0]), font=dict(size=24, color=BLUE))
    fig.update_annotations(selector=dict(text=STARTS[1][0]), font=dict(size=24, color=GREEN))
    fig.update_annotations(selector=dict(text=STARTS[2][0]), font=dict(size=24, color=RED))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".signal_flow_frames"
    tmp.mkdir(exist_ok=True)
    seq = []
    for layer in range(1, LAYERS + 1):
        p = tmp / f"{layer:02d}.png"
        frame(layer).write_image(p)
        seq.append((p, 9))                                    # 0.9 s per layer
    seq[-1] = (seq[-1][0], 40)                                # hold the last layer
    with open(tmp / "list.txt", "w") as f:
        for p, t in seq:
            f.write(f"file '{p.name}'\nduration {t / 10}\n")
        f.write(f"file '{seq[-1][0].name}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-i", str(tmp / "list.txt"), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "signal_flow.gif")], check=True)
    ims = [Image.open(tmp / f"{k:02d}.png").convert("RGB") for k in (1, 2, 3, LAYERS)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "signal_flow_frames.png")
    shutil.rmtree(tmp)
