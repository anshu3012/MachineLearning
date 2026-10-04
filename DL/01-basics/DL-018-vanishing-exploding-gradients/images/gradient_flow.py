"""The gradient of every layer for the 10-layer sigmoid and 10-layer ReLU networks (from the Notebook,
data/gradient_epochs.csv). Part 1: the backward pass at the start, layer 11 (output) down to layer 1 (input);
sigmoid shrinks the gradient at every layer, ReLU does not. Part 2: training, epoch by epoch, with the loss below.
Run: python gradient_flow.py  -> gradient_flow.gif, gradient_flow_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from common import GREEN, RED

HERE = Path(__file__).parent
g = pd.read_csv(HERE.parent / "data" / "gradient_epochs.csv")
NETS = (("10 sigmoid layers", RED, 1), ("10 ReLU layers", GREEN, 2))
LAYERS = np.arange(1, 12)
grad = {n: g[g.network == n].pivot(index="epoch", columns="layer", values="mean_abs_grad") for n, _, _ in NETS}
loss = {n: g[(g.network == n) & (g.layer == 1)].set_index("epoch").loss for n, _, _ in NETS}
s0 = grad["10 sigmoid layers"].loc[0]
assert s0[11] / s0[1] > 1e6 and grad["10 ReLU layers"].loc[0].max() / grad["10 ReLU layers"].loc[0].min() < 10
SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def sci(x):
    m, e = f"{x:.0e}".split("e")
    return f"{m}×10{str(int(e)).translate(SUP)}"


FONT = dict(family="Latin Modern Roman", size=22)


def frame(epoch, shown, title):
    """shown = layers whose bars are drawn (backward pass reveals 11 first)."""
    fig = make_subplots(rows=2, cols=2, row_heights=[0.62, 0.38], vertical_spacing=0.2, horizontal_spacing=0.1,
                        specs=[[{}, {}], [{"colspan": 2}, None]],
                        subplot_titles=("sigmoid: gradient shrinks", "ReLU: gradient stays", ""))
    for name, c, col in NETS:
        v = grad[name].loc[epoch]
        fig.add_trace(go.Bar(x=LAYERS, y=[v[l] if l in shown else None for l in LAYERS], marker_color=c,
                             showlegend=False), row=1, col=col)
        if 1 in shown:
            fig.add_annotation(x=0.6, y=np.log10(max(v[1], 1e-10)), text=sci(v[1]), xanchor="left",
                               yshift=16, showarrow=False, font=dict(size=20, color=c), row=1, col=col)
        fig.update_xaxes(title_text="layer (1 = input side)", tickvals=[1, 6, 11], range=[0.4, 11.6], row=1, col=col)
        fig.update_yaxes(type="log", range=[-10, 0], tickvals=[1e-9, 1e-6, 1e-3, 1], ticktext=["10⁻⁹", "10⁻⁶", "10⁻³", "1"],
                         row=1, col=col)
        L = loss[name].loc[1:epoch]
        fig.add_trace(go.Scatter(x=L.index, y=L.values, mode="lines", line=dict(color=c, width=4), name=name,
                                 showlegend=False), row=2, col=1)
        if epoch:
            fig.add_annotation(x=epoch, y=L.values[-1], text=f"{name.split()[1]} {L.values[-1]:.2f}", xanchor="left", xshift=8, showarrow=False,
                               font=dict(size=20, color=c), row=2, col=1)
    fig.update_yaxes(title_text="mean |∂L/∂W|", row=1, col=1)
    fig.update_xaxes(title_text="epoch", range=[0, 135], tickvals=[0, 25, 50, 75, 100], row=2, col=1)
    fig.update_yaxes(title_text="loss", range=[0, 0.8], tickvals=[0, 0.35, 0.7], row=2, col=1)
    fig.update_layout(template="simple_white", width=900, height=820, font=FONT, margin=dict(l=90, r=30, t=110, b=70),
                      title=dict(text=title, x=0.5, y=0.97, font=dict(size=26)), bargap=0.15)
    fig.update_annotations(selector=dict(text="sigmoid: gradient shrinks"), font=dict(size=24, color=RED))
    fig.update_annotations(selector=dict(text="ReLU: gradient stays"), font=dict(size=24, color=GREEN))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".gradient_flow_frames"
    tmp.mkdir(exist_ok=True)
    seq, keys = [], {}                                         # (image, ticks of 0.1 s)
    for k, layer in enumerate(range(11, 0, -1)):               # part 1: backward pass at epoch 0
        p = tmp / f"a{k:02d}.png"
        frame(0, set(range(layer, 12)), f"Backward pass: layer {layer}").write_image(p)
        seq.append((p, 6))
    seq[-1] = (seq[-1][0], 25)
    keys["mid"], keys["start"] = seq[5][0], seq[-1][0]
    for e in range(2, 101, 2):                                 # part 2: training
        p = tmp / f"b{e:03d}.png"
        frame(e, set(LAYERS), f"Training: epoch {e}").write_image(p)
        seq.append((p, 1))
        if e == 50:
            keys["e50"] = p
    seq[-1] = (seq[-1][0], 40)                                 # hold the last frame
    with open(tmp / "list.txt", "w") as f:
        for p, t in seq:
            f.write(f"file '{p.name}'\nduration {t / 10}\n")
        f.write(f"file '{seq[-1][0].name}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-i", str(tmp / "list.txt"), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "gradient_flow.gif")], check=True)
    ims = [Image.open(keys[k]).convert("RGB") for k in ("mid", "start", "e50")] + [Image.open(seq[-1][0]).convert("RGB")]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "gradient_flow_frames.png")
    shutil.rmtree(tmp)
