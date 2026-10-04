"""Section 7.1: the pull of the context word. The weight w that "bank" puts on "money" slides from 0 to 1, and
y_bank = v_bank + w (v_money - v_bank) slides along the line from v_bank to v_money. The weight the Note's
numbers give, 0.397, is marked. Data: data/vectors.csv.
Run: python weight_slide.py -> weight_slide.gif, weight_slide_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from common import GREEN, PURPLE, GREY, FONT

HERE = Path(__file__).parent
d = pd.read_csv(HERE.parent / "data" / "vectors.csv").query("sentence == 'money bank'")
get = lambda word, kind: d[(d.word == word) & (d.kind == kind)].iloc[0]
v_m, v_b = (np.array([get(w, "v").x, get(w, "v").y]) for w in ("money", "bank"))
W_NOTE = get("bank", "weight_money").x                       # 0.397
assert np.allclose(v_b + W_NOTE * (v_m - v_b), [get("bank", "y").x, get("bank", "y").y], atol=1e-3)


def arrow(fig, b, color, width):
    fig.add_annotation(x=b[0], y=b[1], ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True,
                       arrowhead=2, arrowsize=1.1, arrowwidth=width, arrowcolor=color)


def frame(w):
    y = v_b + w * (v_m - v_b)
    y_note = v_b + W_NOTE * (v_m - v_b)
    fig = go.Figure(go.Scatter(x=[v_b[0], v_m[0]], y=[v_b[1], v_m[1]], mode="lines", showlegend=False,
                               line=dict(color=PURPLE, width=2, dash="dot")))
    fig.add_scatter(x=[y_note[0]], y=[y_note[1]], mode="markers", showlegend=False,
                    marker=dict(size=16, color="white", line=dict(color=PURPLE, width=3)))
    arrow(fig, v_m, GREEN, 3), arrow(fig, v_b, GREEN, 3), arrow(fig, y, PURPLE, 5)
    for p, text, col, xs, ys in ((v_m, "v<sub>money</sub>", GREEN, 0, 18), (v_b, "v<sub>bank</sub>", GREEN, 44, -4),
                                 (y_note, f"the Note's weight, {W_NOTE:.3f}", PURPLE, 118, 14)):
        fig.add_annotation(x=p[0], y=p[1], text=text, showarrow=False, xshift=xs, yshift=ys, font=dict(color=col, size=19))
    fig.add_annotation(x=0.98, y=0.04, xref="paper", yref="paper", showarrow=False, align="left", xanchor="right",
                       yanchor="bottom", font=dict(size=20), bgcolor="white",
                       text=f"weight of bank on money: <b>w = {w:.2f}</b><br>"
                            f"<span style='color:{PURPLE}'>y<sub>bank</sub> = ({y[0]:.2f}, {y[1]:.2f})</span><br>"
                            f"{100 * w:.0f} percent of the way to v<sub>money</sub>")
    fig.update_layout(template="simple_white", width=820, height=700, font=FONT,
                      title=dict(text="More weight on money, a stronger pull towards money", x=0.5),
                      xaxis=dict(range=[-0.6, 9.2], title="dimension 1", zeroline=True),
                      yaxis=dict(range=[-0.8, 7.8], title="dimension 2", zeroline=True, scaleanchor="x"),
                      margin=dict(l=60, r=20, t=60, b=55))
    return fig


up = list(np.linspace(0, 1, 21))
ws = [0.0] * 3 + up + [1.0] * 3 + up[::-1]
ws = ws + list(np.linspace(0, W_NOTE, 6)) + [W_NOTE] * 6          # end on the Note's own weight and hold

if __name__ == "__main__":
    tmp = HERE / ".slide_frames"
    tmp.mkdir(exist_ok=True)
    for i, w in enumerate(ws):
        frame(w).write_image(tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "weight_slide.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, 13, 23, len(ws) - 1)]
    w_, h_ = keys[0].size
    sheet = Image.new("RGB", (2 * w_ + 16, 2 * h_ + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w_ + 16), (i // 2) * (h_ + 16)))
    sheet.save(HERE / "weight_slide_frames.png")
    shutil.rmtree(tmp)
    print(len(ws), "frames")
