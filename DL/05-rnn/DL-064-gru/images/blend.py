"""Section 7: the new memory lies between the old memory and the candidate. For each aspect, a segment from the old
value h_{t-1} to the candidate value. The diamond slides along it: z = 0 keeps the old value, z = 1 takes the candidate,
and each aspect's own z (section 8.3) puts the new value a share z of the way along. Sentence 4 of the story.
Run: python blend.py  -> blend.gif, blend_frames.png (Plotly frames + ffmpeg: positions sliding along segments)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

from common import BLUE, GREY, PURPLE, RED

HERE = Path(__file__).parent
ASPECTS = ["power", "conflict", "tragedy", "revenge"]
old, cand, z = np.array([0.6, 0.6, 0.7, 0.1]), np.array([0.7, 0.2, 0.1, 0.2]), np.array([0.1, 0.7, 0.8, 0.2])
new = (1 - z) * old + z * cand
assert np.allclose(np.round(new, 2), [0.61, 0.32, 0.22, 0.12])                # section 8.4


def frame(zz, title, final=False):
    """The chart with the diamonds at share zz (one number per aspect) of the way from old to candidate."""
    pos = (1 - zz) * old + zz * cand
    fig = go.Figure()
    for k, a in enumerate(ASPECTS):
        fig.add_trace(go.Scatter(x=[old[k], cand[k]], y=[a, a], mode="lines", line=dict(color=GREY, width=3),
                                 showlegend=False))
        fig.add_annotation(x=pos[k], y=a, yshift=-30, showarrow=False, font=dict(size=20, color=PURPLE),
                           text=f"z = {zz[k]:g}: {zz[k]:.0%} of the way" if final else f"z = {zz[k]:.2f}")
    fig.add_trace(go.Scatter(x=old, y=ASPECTS, mode="markers", name="old memory h<sub>t−1</sub>",
                             marker=dict(size=20, color=RED)))
    fig.add_trace(go.Scatter(x=cand, y=ASPECTS, mode="markers", name="candidate h̃<sub>t</sub>",
                             marker=dict(size=20, color=BLUE)))
    fig.add_trace(go.Scatter(x=pos, y=ASPECTS, mode="markers+text", name="new memory h<sub>t</sub>",
                             text=[f"{v:.2f}" for v in pos], textposition="top center", textfont=dict(size=20),
                             marker=dict(size=22, color=PURPLE, symbol="diamond")))
    fig.update_yaxes(range=[3.6, -0.5])
    fig.update_layout(template="simple_white", width=1000, height=620, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=title, x=0.5, font=dict(size=28)),
                      xaxis=dict(title="value", range=[0, 0.8]), legend=dict(orientation="h", y=1.1, x=0),
                      margin=dict(l=110, r=30, t=110, b=60))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".blend_frames"
    tmp.mkdir(exist_ok=True)
    one = np.ones(4)
    plan = [(0 * one, "z = 0: keep the old memory", False)] * 8                               # hold
    plan += [(s * one, "z rising: move toward the candidate", False) for s in np.linspace(0.1, 0.9, 9)]
    plan += [(one, "z = 1: take the candidate", False)] * 8
    plan += [((1 - s) * one + s * z, "each entry gets its own z", False) for s in np.linspace(0.1, 0.9, 9)]
    plan += [(z, "each entry gets its own z", True)] * 20
    keys = {}
    for n, (zz, title, final) in enumerate(plan):
        key = (tuple(np.round(zz, 4)), title)
        if key not in keys:
            keys[key] = tmp / f"k{len(keys)}.png"
            frame(zz, title, final).write_image(keys[key])
        shutil.copy(keys[key], tmp / f"{n:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "8", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=800:-2:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "blend.gif")], check=True)
    # the last frame (every aspect at its own z) is the PDF figure
    Image.open(tmp / f"{len(plan) - 1:03d}.png").convert("RGB").save(HERE / "blend_frames.png")
    shutil.rmtree(tmp)
