"""Animations for the XGBoost classification Note (lambda = 0, eta = 0.3, depth 1, min_child_weight = 0).
split_search.gif - the threshold visits the four midpoints; each candidate's gain S_left + S_right - S_parent,
                   with S = (sum r)^2 / sum p(1-p), is recorded; CGPA < 7.625 wins (2.22) and the leaves get
                   their log-odds outputs -1.11 and 1.67;
next_trees.gif   - tree after tree: the predicted probability of each student and its residual y - p.
Run: python animations.py  -> split_search.gif/_frames.png, next_trees.gif/_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, PURPLE, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#9A9A9A"
FONT = dict(family="Latin Modern Roman", size=22)
x = np.array([5.70, 6.25, 7.10, 8.15, 9.60])
y = np.array([0, 1, 0, 1, 1])
sig = lambda z: 1 / (1 + np.exp(-z))
z0, ETA = np.log(1.5), 0.3
CANDS = (x[:-1] + x[1:]) / 2


def split_stats(z):
    """Gain of every candidate split for the residuals at log-odds z (lambda = 0)."""
    p = sig(z); r = y - p; h = p * (1 - p)
    S = lambda m: r[m].sum() ** 2 / h[m].sum()
    out = []
    for t in CANDS:
        L = x < t
        out.append((S(L), S(~L), S(L) + S(~L) - S(np.ones(5, bool))))
    return np.array(out)


def tree(z):
    p = sig(z); r = y - p; h = p * (1 - p)
    t = CANDS[split_stats(z)[:, 2].argmax()]
    L = x < t
    return t, r[L].sum() / h[L].sum(), r[~L].sum() / h[~L].sum()


st = split_stats(np.full(5, z0))
assert np.allclose(CANDS, [5.975, 6.675, 7.625, 8.875])
assert np.allclose(st[:, 2], [1.88, 0.14, 2.22, 0.83], atol=0.005)
t1, wl, wr = tree(np.full(5, z0))
assert np.isclose(t1, 7.625) and np.isclose(wl, -1.11, atol=0.005) and np.isclose(wr, 1.67, atol=0.005)
# all trees
zs, trees = [np.full(5, z0)], []
for m in range(15):
    t, a, b = tree(zs[-1]); trees.append((t, a, b))
    zs.append(zs[-1] + ETA * np.where(x < t, a, b))
assert np.allclose(sig(zs[1]), [0.518, 0.518, 0.518, 0.712, 0.712], atol=0.001)
assert np.isclose(trees[1][0], 5.975) and np.isclose(split_stats(zs[1])[:, 2].max(), 1.39, atol=0.005)
print("p after 15 trees:", sig(zs[-1]).round(3))


def write(name, frames, keys, fps=4):
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


def search_frame(title, t, seen, best=None):
    r = y - sig(z0)
    fig = make_subplots(1, 2, column_widths=[0.58, 0.42], horizontal_spacing=0.12,
                        subplot_titles=["residuals y - p (p = 0.6)", "gain of each candidate"])
    col = ["black"] * 5 if t is None else [BLUE if xi < t else ORANGE for xi in x]
    fig.add_trace(go.Bar(x=x, y=r, width=0.12, marker_color=col, showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=x, y=r + np.sign(r) * 0.09, mode="text", text=[f"{v:+.1f}" for v in r],
                             textfont=dict(size=22), showlegend=False), 1, 1)
    fig.add_hline(y=0, line=dict(color="black", width=1), row=1, col=1)
    if t is not None:
        fig.add_vrect(x0=5.3, x1=t, fillcolor=BLUE, opacity=0.12, line_width=0, row=1, col=1)
        fig.add_vrect(x0=t, x1=10, fillcolor=ORANGE, opacity=0.12, line_width=0, row=1, col=1)
        fig.add_vline(x=t, line=dict(color=GREEN if best else "black", width=4, dash=None if best else "dash"),
                      row=1, col=1)
    if best:
        for a, b, v in ((5.3, best, wl), (best, 10, wr)):
            fig.add_annotation(x=(a + b) / 2, y=-0.85, text=f"output {v:+.2f} (log-odds)", showarrow=False,
                               font=dict(size=21, color=GREEN), bgcolor="white", row=1, col=1)
    g = [st[i, 2] if c in seen else 0 for i, c in enumerate(CANDS)]
    fig.add_trace(go.Bar(x=[f"< {c:g}" for c in CANDS], y=g, showlegend=False,
                         text=[f"{v:.2f}" if c in seen else "" for v, c in zip(g, CANDS)], textposition="outside",
                         textfont=dict(size=22), marker_color=[GREEN if c == best else GREY for c in CANDS]), 1, 2)
    fig.update_xaxes(title_text="CGPA", range=[5.3, 10], row=1, col=1)
    fig.update_yaxes(title_text="residual", range=[-1.05, 0.75], row=1, col=1)
    fig.update_yaxes(range=[0, 2.7], row=1, col=2)
    fig.update_xaxes(title_text="split", tickfont=dict(size=18), row=1, col=2)
    fig.update_annotations(font_family="Latin Modern Roman")
    for a in fig.layout.annotations[:2]:
        a.font.size = 24
    fig.update_layout(template="simple_white", width=1200, height=620, font=FONT,
                      title=dict(text=title, x=0.5, y=0.96), margin=dict(l=80, r=20, t=110, b=70))
    return fig


def boost_frame(k):
    p = sig(zs[k])
    grid = np.linspace(5.3, 10, 600)
    zg = np.full_like(grid, z0)
    for t, a, b in trees[:k]:
        zg = zg + ETA * np.where(grid < t, a, b)
    fig = make_subplots(1, 2, column_widths=[0.55, 0.45], horizontal_spacing=0.1,
                        subplot_titles=["probability of placement", "residual y - p of each student"])
    fig.add_trace(go.Scatter(x=grid, y=sig(zg), mode="lines", line=dict(color=RED, width=4, shape="hv"),
                             showlegend=False), 1, 1)
    fig.add_hline(y=0.5, line=dict(color=GREY, width=1.5, dash="dot"), row=1, col=1)
    cols = [ORANGE, BLUE, PURPLE, GREEN, "#222222"]
    for i in range(5):
        fig.add_trace(go.Scatter(x=[x[i]], y=[y[i]], mode="markers", marker=dict(size=16, color=cols[i]),
                                 showlegend=False), 1, 1)
        fig.add_trace(go.Scatter(x=list(range(k + 1)), y=[y[i] - sig(zz[i]) for zz in zs[:k + 1]],
                                 mode="lines+markers", line=dict(color=cols[i], width=7 if i == 3 else 3, dash="dash" if i == 4 else None),
                                 marker=dict(size=8),
                                 name=f"student {i + 1} ({'placed' if y[i] else 'not placed'})"), 1, 2)
    fig.add_hline(y=0, line=dict(color="black", width=1), row=1, col=2)
    wrong = int(((p > 0.5) != y).sum())
    fig.update_xaxes(title_text="CGPA", range=[5.3, 10], row=1, col=1)
    fig.update_yaxes(range=[-0.08, 1.08], dtick=0.25, row=1, col=1)
    fig.update_xaxes(title_text="trees added", range=[-0.4, len(trees) + 0.4], dtick=3, row=1, col=2)
    fig.update_yaxes(range=[-0.7, 0.55], row=1, col=2)
    fig.update_annotations(font_family="Latin Modern Roman")
    for a in fig.layout.annotations[:2]:
        a.font.size = 24
    head = "stage 1: p = 0.6 for everyone" if k == 0 else f"after {k} tree{'s' if k > 1 else ''}"
    fig.update_layout(template="simple_white", width=1200, height=660, font=FONT,
                      title=dict(text=f"{head}: {wrong} of 5 on the wrong side of 0.5", x=0.5, y=0.97),
                      margin=dict(l=80, r=20, t=110, b=130),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.2, font=dict(size=18)))
    return fig


if __name__ == "__main__":
    frames = [(search_frame("residuals of the five students: one leaf", None, []), 6)]
    seen = []
    for i, c in enumerate(CANDS):
        seen.append(c)
        sl, sr, g = st[i]
        frames.append((search_frame(f"CGPA < {c:g}: {sl:.2f} + {sr:.2f} - 0 = {g:.2f}", c, list(seen)), 6))
    frames.append((search_frame("best: CGPA < 7.625, gain 2.22", 7.625, list(seen), best=7.625), 16))
    write("split_search", frames, [3, 5])
    frames = [(boost_frame(k), 8 if k in (0, 1) else 3) for k in range(len(trees))] + [(boost_frame(len(trees)), 14)]
    write("next_trees", frames, [1, len(trees)])
