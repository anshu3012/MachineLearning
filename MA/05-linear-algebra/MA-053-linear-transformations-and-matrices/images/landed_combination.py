"""Section 4's worked example drawn: v = [-1, 2] lands on -1 times where i-hat lands ([1, -2]) plus 2 times where
j-hat lands ([3, 0]) = [5, 2]. Scale the green arrow, scale the red arrow, put them tip to tail, read off the sum.
Run: python landed_combination.py  -> landed_combination.gif, landed_combination_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
ORANGE, GREEN, RED, GREY = "#F58518", "#54A24B", "#E45756", "#6B6B6B"
i_new, j_new, v = np.array([1, -2]), np.array([3, 0]), np.array([-1, 2])
target = v[0] * i_new + v[1] * j_new
A = np.column_stack([i_new, j_new])
assert (target == [5, 2]).all() and (A @ v == target).all()        # the Note's numbers


def arrow(fig, tail, head, color, text, dash=False):
    fig.add_annotation(x=head[0], y=head[1], ax=tail[0], ay=tail[1], xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=5, arrowcolor=color, opacity=0.5 if dash else 1)
    if text:
        mid = (np.array(tail) + np.array(head)) / 2
        fig.add_annotation(x=mid[0], y=mid[1], text=text, showarrow=False, font=dict(size=22, color=color),
                           bgcolor="rgba(255,255,255,0.85)", yshift=22)


def frame(si, sj, shift, done, caption):
    """si, sj: current scale factors on i' and j'; shift in [0, 1] slides the j-arrow to the tip of the i-arrow."""
    fig = go.Figure(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=9, color="black"), showlegend=False))
    a = si * i_new
    b0 = shift * a
    arrow(fig, (0, 0), i_new, GREEN, None, dash=True)
    arrow(fig, (0, 0), j_new, RED, None, dash=True)
    arrow(fig, (0, 0), a, GREEN, f"{si:.1f} × [1, −2]")
    arrow(fig, b0, b0 + sj * j_new, RED, f"{sj:.1f} × [3, 0]")
    if done:
        arrow(fig, (0, 0), target, ORANGE, None)
        fig.add_annotation(x=5, y=2, text="<b>v lands on [5, 2]</b>", showarrow=False, xanchor="left", xshift=12,
                           font=dict(size=24, color=ORANGE))
    fig.add_annotation(x=1, y=-2, text="i lands here", showarrow=False, xanchor="left", xshift=10,
                       font=dict(size=18, color=GREEN))
    fig.add_annotation(x=3, y=0, text="j lands here", showarrow=False, yshift=-22, font=dict(size=18, color=RED))
    fig.update_layout(template="simple_white", width=900, height=640, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"<b>[−1, 2] → −1 × [1, −2] + 2 × [3, 0]</b><br>{caption}", x=0.5, y=0.95),
                      xaxis=dict(range=[-2.5, 8], dtick=1, showgrid=True, zeroline=True, scaleanchor="y"),
                      yaxis=dict(range=[-3, 3.5], dtick=1, showgrid=True, zeroline=True),
                      margin=dict(l=50, r=20, t=110, b=40))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".combo_frames"
    tmp.mkdir(exist_ok=True)
    seq = [(1, 1, 0, False, "where the basis vectors land")] * 4
    seq += [(1 + (v[0] - 1) * t, 1, 0, False, "step 1: scale the green arrow by −1") for t in np.linspace(0, 1, 8)]
    seq += [(v[0], 1 + (v[1] - 1) * t, 0, False, "step 2: scale the red arrow by 2") for t in np.linspace(0, 1, 8)]
    seq += [(v[0], v[1], t, False, "step 3: put the red arrow at the tip of the green one") for t in np.linspace(0, 1, 8)]
    seq += [(v[0], v[1], 1, True, "the sum: v lands on [5, 2]")] * 12
    for k, s in enumerate(seq):
        frame(*s).write_image(tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "landed_combination.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (3, 11, 19, len(seq) - 1)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "landed_combination_frames.png")
    shutil.rmtree(tmp)
