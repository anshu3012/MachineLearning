"""Section 3: projecting w onto v and projecting v onto w give the same number. With v = [3, 1] and w = [1, 2]
(Section 2's example), both views give 5; stretching v to 2v doubles the length in one view and the shadow in the
other, so both views give 10.
Run: python order_symmetry.py  -> order_symmetry.gif, order_symmetry_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, PURPLE, GREY = "#4C78A8", "#F58518", "#B279A2", "#6B6B6B"
V, W = np.array([3.0, 1.0]), np.array([1.0, 2.0])
proj = lambda a, onto: (a @ onto) / (onto @ onto) * onto              # shadow of a on the line of onto
sl = lambda a, onto: (a @ onto) / np.linalg.norm(onto)               # its signed length
assert np.isclose(V @ W, 5) and np.allclose(proj(W, V), [1.5, 0.5])   # Section 2's numbers
for s in (1, 2):
    v = s * V
    assert np.isclose(sl(W, v) * np.linalg.norm(v), sl(v, W) * np.linalg.norm(W)) and np.isclose(v @ W, 5 * s)


def panel(fig, c, a, onto, a_col, onto_col, a_name, onto_name):
    sh = proj(a, onto)
    far = onto / np.linalg.norm(onto) * 8
    fig.add_trace(go.Scatter(x=[-far[0] * 0.1, far[0]], y=[-far[1] * 0.1, far[1]], mode="lines",
                             line=dict(color=GREY, dash="dash", width=1.5), showlegend=False), row=1, col=c)
    fig.add_trace(go.Scatter(x=[0, sh[0]], y=[0, sh[1]], mode="lines", line=dict(color=PURPLE, width=14),
                             opacity=0.7, showlegend=False), row=1, col=c)
    fig.add_trace(go.Scatter(x=[a[0], sh[0]], y=[a[1], sh[1]], mode="lines", line=dict(color=GREY, dash="dot", width=2),
                             showlegend=False), row=1, col=c)
    for vec, col, name in [(onto, onto_col, onto_name), (a, a_col, a_name)]:
        fig.add_annotation(x=vec[0], y=vec[1], ax=0, ay=0, xref=f"x{c}", yref=f"y{c}", axref=f"x{c}", ayref=f"y{c}",
                           showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=4, arrowcolor=col)
        fig.add_annotation(x=vec[0], y=vec[1], xref=f"x{c}", yref=f"y{c}", text=f"<b>{name}</b>", showarrow=False,
                           font=dict(size=22, color=col), xshift=18, yshift=12)
    fig.update_xaxes(range=[-0.8, 7.0], dtick=1, showgrid=True, zeroline=True, row=1, col=c)
    fig.update_yaxes(range=[-0.6, 4.6], dtick=1, showgrid=True, zeroline=True, row=1, col=c,
                     scaleanchor=f"x{c}" if c > 1 else "x")


def frame(s, note):
    v = s * V
    lv = "v" if s == 1 else f"{s:.1f} v"
    left = (f"<b>project w onto {lv}</b><br>shadow {sl(W, v):.2f} × length of {lv} {np.linalg.norm(v):.2f}"
            f" = <b>{sl(W, v) * np.linalg.norm(v):.1f}</b>")
    right = (f"<b>project {lv} onto w</b><br>shadow {sl(v, W):.2f} × length of w {np.linalg.norm(W):.2f}"
             f" = <b>{sl(v, W) * np.linalg.norm(W):.1f}</b>")
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.06, subplot_titles=[left, right])
    panel(fig, 1, W, v, ORANGE, BLUE, "w", lv)
    panel(fig, 2, v, W, BLUE, ORANGE, lv, "w")
    fig.update_layout(template="simple_white", width=1200, height=640, font=dict(family="Latin Modern Roman", size=18),
                      title=dict(text=f"<b>{note}</b>", x=0.5, y=0.97), margin=dict(l=40, r=20, t=150, b=40))
    fig.update_annotations(selector=dict(xref="paper"), font_size=19)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".order_frames"
    tmp.mkdir(exist_ok=True)
    seq = [(1.0, "two different shadows, the same product: 5")] * 10
    seq += [(s, "stretch v: one view's length grows, the other's shadow grows") for s in np.linspace(1, 2, 12)]
    seq += [(2.0, "still the same product: 2 × 5 = 10")] * 12
    for k, s in enumerate(seq):
        frame(*s).write_image(tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "order_symmetry.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (9, len(seq) - 1)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (w, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, (0, i * (h + 16)))
    sheet.save(HERE / "order_symmetry_frames.png")
    shutil.rmtree(tmp)
