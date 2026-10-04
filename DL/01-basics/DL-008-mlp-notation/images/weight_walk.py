"""Reading a weight's name on the 4-3-2-1 network. For five weights in turn, three steps: the layer it enters lights up
(k), then the node it leaves (i), then the node it enters (j), and the name fills in one index per step.
Plotly frames (a fixed drawing whose highlights change) -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
SIZES = [4, 3, 2, 1]
GREY, BLUE, ORANGE, RED = "#C8C8C8", "#4C78A8", "#F58518", "#E45756"
POS = {(l, j): (l * 3.0, (n - 1) / 2 - (j - 1)) for l, n in enumerate(SIZES) for j in range(1, n + 1)}
WEIGHTS = [(1, 1, 1), (1, 4, 2), (1, 1, 3), (2, 2, 2), (3, 1, 1)]          # (k, i, j)
SUB = "⁰¹²³⁴"


def frame(k, i, j, step):
    fig = go.Figure()
    for l in range(1, 4):
        for a in range(1, SIZES[l - 1] + 1):
            for b in range(1, SIZES[l] + 1):
                (x0, y0), (x1, y1) = POS[(l - 1, a)], POS[(l, b)]
                hot = step == 3 and (l, a, b) == (k, i, j)
                fig.add_scatter(x=[x0, x1], y=[y0, y1], mode="lines", hoverinfo="skip",
                                line=dict(color=RED if hot else GREY, width=7 if hot else 1.5))
    for (l, n), (x, y) in POS.items():
        col = "white"
        if l == k and step >= 1:
            col = "#FDE3C8"
        if (l, n) == (k - 1, i) and step >= 2:
            col = BLUE
        if (l, n) == (k, j) and step >= 3:
            col = ORANGE
        fig.add_scatter(x=[x], y=[y], mode="markers+text", text=[str(n)], textfont=dict(size=22),
                        marker=dict(size=52, color=col, line=dict(color="#555", width=2)), hoverinfo="skip")
    for l in range(4):
        fig.add_annotation(x=l * 3.0, y=-2.2, text=f"layer {l}", showarrow=False,
                           font=dict(size=24, color=ORANGE if (l == k and step >= 1) else "#555"))
    kk, ii, jj = (str(k) if step >= 1 else "?"), (str(i) if step >= 2 else "?"), (str(j) if step >= 3 else "?")
    said = ["", f"enters layer <b>{k}</b>", f"leaves node <b>{i}</b> of layer {k - 1}",
            f"enters node <b>{j}</b> of layer {k}"][step]
    name = (f"W<sup><span style='color:{ORANGE}'>{kk}</span></sup>"
            f"<sub><span style='color:{BLUE}'>{ii}</span><span style='color:{ORANGE}'>{jj}</span></sub>")
    fig.update_layout(template="simple_white", width=1000, height=720, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"<span style='font-size:44px'>{name}</span>    {said}", x=0.5, y=0.93,
                                 font=dict(size=28)),
                      xaxis=dict(visible=False, range=[-0.8, 9.8]), yaxis=dict(visible=False, range=[-2.6, 2.1]),
                      margin=dict(l=10, r=10, t=120, b=10))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".ww_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, []
    for (k, i, j) in WEIGHTS:
        for step in (1, 2, 3):
            f = tmp / f"k{k}{i}{j}{step}.png"
            frame(k, i, j, step).write_image(f)
            for _ in range(2 if step < 3 else 4):
                shutil.copy(f, tmp / f"{n:03d}.png")
                n += 1
            if (k, i, j) == (1, 4, 2):
                keys.append(f)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "weight_walk.gif")], check=True)
    ims = [Image.open(f).convert("RGB") for f in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (3 * w + 32, h), "white")
    for a, im in enumerate(ims):
        sheet.paste(im, (a * (w + 16), 0))
    sheet.save(HERE / "weight_walk_frames.png")
    shutil.rmtree(tmp)
