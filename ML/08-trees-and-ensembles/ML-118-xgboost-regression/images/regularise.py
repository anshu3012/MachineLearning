"""Lambda and gamma on the first XGBoost tree of the four students (same splits: CGPA < 8.25, then CGPA < 5.85).
lambda_shrink.gif: lambda grows 0 -> 5; the leaf outputs sum(r)/(n + lambda) shrink towards 0, the one-residual
leaves fastest, and both gains shrink.
gamma_prune.gif: gamma rises 0 -> 22 (lambda = 0); a split whose gain is below gamma is pruned, bottom up, and the
leaves merge.
Run: python regularise.py  -> lambda_shrink.gif/_frames.png, gamma_prune.gif/_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#9A9A9A"
cgpa = np.array([6.7, 9.0, 7.5, 5.0])
r = np.array([4.5, 11, 6, 8]) - 7.375
LEAVES = [(4.6, 5.85, cgpa < 5.85), (5.85, 8.25, (cgpa >= 5.85) & (cgpa < 8.25)), (8.25, 9.4, cgpa >= 8.25)]
S = lambda m, lam: r[m].sum() ** 2 / (m.sum() + lam)
out = lambda m, lam: r[m].sum() / (m.sum() + lam)
ALL, LEFT = np.ones(4, bool), cgpa < 8.25


def gains(lam):
    root = S(LEFT, lam) + S(~LEFT, lam) - S(ALL, lam)
    low = S(LEAVES[0][2], lam) + S(LEAVES[1][2], lam) - S(LEFT, lam)
    return root, low


def pruned_leaves(gamma):
    """Bottom-up pruning with lambda = 0: the lower split goes first, then the root (only if its child went)."""
    root, low = gains(0)
    if low - gamma >= 0:
        return LEAVES
    if root - gamma >= 0:
        return [(4.6, 8.25, LEFT), LEAVES[2]]
    return [(4.6, 9.4, ALL)]


assert np.allclose([out(m, 1) for _, _, m in LEAVES], [0.3125, -1.4167, 1.8125], atol=1e-4)
assert np.allclose(gains(0), [17.52, 5.04], atol=0.01) and np.allclose(gains(1), [9.86, 2.93], atol=0.01)
assert np.isclose(out(pruned_leaves(6)[0][2], 0), -1.2083, atol=1e-4) and len(pruned_leaves(6)) == 2
assert len(pruned_leaves(20)) == 1 and np.isclose(out(ALL, 0), 0)


def base(title, leaves, lam, bar_vals, bar_cols, gamma=None):
    fig = make_subplots(1, 2, column_widths=[0.6, 0.4], horizontal_spacing=0.12,
                        subplot_titles=["residuals and leaf outputs", "gain of each split"])
    fig.add_trace(go.Bar(x=cgpa, y=r, width=0.1, marker_color=GREY, showlegend=False), 1, 1)
    for a, b, m in leaves:
        v = out(m, lam)
        fig.add_trace(go.Scatter(x=[a, b], y=[v, v], mode="lines", line=dict(color=GREEN, width=7), showlegend=False), 1, 1)
        fig.add_annotation(x=(a + b) / 2, y=v + (0.55 if v >= 0 else -0.55), text=f"{v:.3f}".rstrip("0").rstrip(".") + f" (n = {m.sum()})",
                           showarrow=False, font=dict(size=21, color=GREEN), bgcolor="white", row=1, col=1)
    fig.add_hline(y=0, line=dict(color="black", width=1), row=1, col=1)
    fig.add_trace(go.Bar(x=["root: < 8.25", "lower: < 5.85"], y=bar_vals, marker_color=bar_cols, width=0.6,
                         text=[f"{v:.2f}" for v in bar_vals], textposition="outside", textfont=dict(size=22),
                         showlegend=False), 1, 2)
    if gamma:
        fig.add_hline(y=gamma, line=dict(color=RED, width=4, dash="dash"), opacity=1, row=1, col=2)
        fig.add_annotation(x=0.5, y=gamma, text=f"gamma = {gamma:g}", showarrow=False, yshift=16, xanchor="center", bgcolor="white",
                           font=dict(size=22, color=RED), row=1, col=2)
    fig.update_xaxes(title_text="CGPA", range=[4.6, 9.4], row=1, col=1)
    fig.update_yaxes(title_text="residual", range=[-3.6, 4.4], row=1, col=1)
    fig.update_yaxes(range=[0, 24], row=1, col=2)
    fig.update_annotations(font_family="Latin Modern Roman")
    for a in fig.layout.annotations[:2]:
        a.font.size = 24
    fig.update_layout(template="simple_white", width=1200, height=620, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=title, x=0.5, y=0.96), margin=dict(l=80, r=20, t=110, b=70))
    return fig


def lam_frame(lam):
    return base(f"lambda = {lam:.2f}", LEAVES, lam, list(gains(lam)), [GREEN, GREEN])


def gam_frame(gamma):
    leaves = pruned_leaves(gamma)
    kept = {3: [GREEN, GREEN], 2: [GREEN, GREY], 1: [GREY, GREY]}[len(leaves)]
    txt = {3: "both splits kept", 2: "lower split pruned", 1: "both pruned: one leaf, output 0"}[len(leaves)]
    return base(f"gamma = {gamma:g}: {txt}", leaves, 0, list(gains(0)), kept, gamma)


def write(name, frames, keys, fps=5):
    tmp = HERE / f".{name}_frames"
    tmp.mkdir(exist_ok=True)
    n, shots = 0, {}
    for k, (f, hold) in enumerate(frames):
        f.write_image(tmp / "src.png")
        for _ in range(hold):
            shutil.copy(tmp / "src.png", tmp / f"{n:03d}.png"); n += 1
        if k in keys:
            shots[k] = Image.open(tmp / "src.png").convert("RGB")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    ims = [shots[k] for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (w, len(ims) * h + 16 * (len(ims) - 1)), "white")   # stacked: readable in the PDF
    for i, im in enumerate(ims):
        sheet.paste(im, (0, i * (h + 16)))
    sheet.save(HERE / f"{name}_frames.png")
    shutil.rmtree(tmp)


if __name__ == "__main__":
    lams = np.round(np.arange(0, 5.01, 0.25), 2)
    frames = [(lam_frame(l), 10 if l in (0, 1, 5) else 1) for l in lams]
    write("lambda_shrink", frames, [0, 4])
    gams = list(range(0, 23))
    frames = [(gam_frame(g), 10 if g in (0, 6, 20, 22) else 2) for g in gams]
    write("gamma_prune", frames, [6, 18])
