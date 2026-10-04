"""One 64 x 64 crop of the Note's photo convolved with four kernels, one per frame: a 3 x 3 box blur, a 5 x 5
Gaussian blur, the vertical-edge kernel and the horizontal-edge kernel. Each frame draws the kernel beside its result.
Blur kernels sum to 1 (an average); edge kernels sum to 0 (a flat patch gives 0).
Plotly frames because the same picture changes with the kernel. Our own code and photo; the sequence of kernels
(box blur, Gaussian blur, vertical edges, horizontal edges) follows 3Blue1Brown, "But what is a convolution?" (08:30-12:30).
Run: python kernel_gallery.py -> kernel_gallery.gif, kernel_gallery_frames.png"""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from anim import save_gif
from common import GREY, FONT

HERE = Path(__file__).parent
photo = np.array(Image.open(HERE.parent / "data" / "photo.png"), dtype=float)
R0, C0, N = 70, 0, 64
crop = photo[R0:R0 + N, C0:C0 + N]
b = np.array([1, 4, 6, 4, 1])
KERNELS = [
    ("box blur: nine weights of 1/9", np.full((3, 3), 1 / 9), lambda v: "1/9", "the weights add up to 1: each pixel becomes the average of its 3 × 3 neighbours"),
    ("Gaussian blur: 25 weights, largest in the centre", np.outer(b, b) / 256, lambda v: f"{round(v * 256)}", "weights shown × 256; they add up to 1: an average that favours the centre"),
    ("vertical-edge kernel", np.array([[-1, 0, 1]] * 3, float), lambda v: f"{v:g}", "the weights add up to 0: a flat patch gives 0, a left-to-right change gives a large value"),
    ("horizontal-edge kernel", np.array([[-1, 0, 1]] * 3, float).T, lambda v: f"{v:g}", "the weights add up to 0: a flat patch gives 0, a top-to-bottom change gives a large value"),
]


def conv(X, K):
    f = K.shape[0]
    return np.array([[(X[i:i + f, j:j + f] * K).sum() for j in range(X.shape[1] - f + 1)] for i in range(X.shape[0] - f + 1)])


flat = np.full((7, 7), 180.0)                                # a flat patch: blur keeps it, edge kernels give 0
for _, K, _, _ in KERNELS:
    s = K.sum()
    assert np.isclose(s, 1) or np.isclose(s, 0)
    assert np.allclose(conv(flat, K), 180.0 * s)
p = crop[10:13, 10:13]
print("3 x 3 patch at rows 10-12, columns 10-12 of the crop:", p.astype(int).tolist(), "mean", p.mean().round(1))


def frame(k):
    title, K, fmt, note = KERNELS[k]
    Z = conv(crop, K)
    edge = np.isclose(K.sum(), 0)
    fig = make_subplots(1, 3, column_widths=[0.38, 0.24, 0.38], horizontal_spacing=0.04,
                        subplot_titles=("photo (64 × 64 pixels)", "kernel", "result"))
    fig.update_annotations(font_size=24)
    fig.add_trace(go.Heatmap(z=crop, colorscale="gray", zmin=0, zmax=255, showscale=False), 1, 1)
    top = np.abs(K).max()
    fig.add_trace(go.Heatmap(z=K, colorscale="RdBu_r" if edge else "Oranges", zmin=-2 * top if edge else 0, zmax=2 * top,
                             showscale=False, xgap=2, ygap=2, text=[[fmt(v) for v in r] for r in K],
                             texttemplate="%{text}", textfont=dict(size=24 if K.shape[0] == 3 else 19, color="black")), 1, 2)
    if edge:
        m = np.percentile(np.abs(Z), 99)
        fig.add_trace(go.Heatmap(z=Z, colorscale="RdBu_r", zmin=-m, zmax=m, showscale=False), 1, 3)
    else:
        fig.add_trace(go.Heatmap(z=Z, colorscale="gray", zmin=0, zmax=255, showscale=False), 1, 3)
    fig.update_xaxes(visible=False)
    for c in (1, 2, 3):
        fig.update_yaxes(visible=False, autorange="reversed", scaleanchor="x" if c == 1 else f"x{c}", row=1, col=c)
    fig.update_layout(template="simple_white", width=1100, height=560, font=dict(FONT, size=20),
                      title=dict(text=f"{k + 1} of 4: {title}", x=0.5, y=0.97, font=dict(size=26)),
                      margin=dict(l=10, r=10, t=110, b=70))
    fig.add_annotation(text=note + (" (red positive, blue negative)" if edge else ""), xref="paper", yref="paper", x=0.5, y=-0.1,
                       showarrow=False, font=dict(size=20, color=GREY))
    return fig


if __name__ == "__main__":
    figs = [frame(k) for k in range(4) for _ in range(3)]          # hold each kernel for 3 frames
    save_gif(figs, "kernel_gallery", HERE, fps=1, hold=2, keys=(0, 3, 6, 9), height=560)
