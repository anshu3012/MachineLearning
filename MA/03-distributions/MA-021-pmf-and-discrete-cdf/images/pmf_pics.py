"""Plotly figures for the PMF Note, from the Note's own numbers: the two-dice probabilities stacked to exactly 1
(section 2.1); the one-die PMF as a function of every x (section 3); simulated PMF settling as rolls grow
(section 4, GIF + frame grid, same seed and rolls as Figure 2); the 6 - |x - 7| rule (section 5);
Bernoulli p = 0.3 and binomial n = 4, p = 0.5 (section 6)."""
import shutil
import subprocess
from math import comb
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=20)
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
LAY = dict(template="simple_white", font=FONT)
x2 = np.arange(2, 13)
pairs = 6 - np.abs(x2 - 7)
assert list(pairs) == [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1] and pairs.sum() == 36


def save(fig, name):
    fig.write_image(here / f"{name}.png", scale=2); fig.write_image(here / f"{name}.pdf")


# 2.1: stack the 11 probabilities: they fill exactly one unit
fig = go.Figure()
pal = [BLUE, ORANGE]
for i, (x, k) in enumerate(zip(x2, pairs)):
    fig.add_trace(go.Bar(x=["sum of two dice"], y=[k / 36], marker=dict(color=pal[i % 2], line=dict(
        color="white", width=2)), text=f"P({x}) = {k}/36" if k > 1 else "", textposition="inside", insidetextanchor="middle",
        textfont=dict(color="white", size=17), showlegend=False))
fig.add_trace(go.Bar(x=["one die"], y=[1], marker=dict(color="rgba(0,0,0,0)"), showlegend=False))
for f in range(6):
    fig.add_trace(go.Bar(x=["one die"], y=[1 / 6], marker=dict(color=pal[f % 2], line=dict(color="white", width=2)),
                         text=f"P({f + 1}) = 1/6", textposition="inside", textfont=dict(color="white", size=17),
                         showlegend=False, base=f / 6))
fig.add_hline(y=1, line=dict(color=RED, dash="dash", width=3), layer="above", opacity=1)
for y, t in ((1 / 72, "P(2) = 1/36"), (1 - 1 / 72, "P(12) = 1/36")):
    fig.add_annotation(x=0, y=y, text=t, xanchor="right", xshift=-128, showarrow=False, font=dict(size=17))
fig.add_annotation(x=0.5, y=1.04, text="total = 1 exactly", showarrow=False, font=dict(color=RED, size=22))
fig.update_layout(**LAY, barmode="stack", width=800, height=760, margin=dict(l=70, r=20, t=30, b=50),
                  yaxis=dict(title="probabilities stacked", range=[0, 1.1]), bargap=0.35)
save(fig, "pmf_sums_to_one")

# 3: the one-die PMF is defined for every x, and is 0 away from the faces
fig = go.Figure()
fig.add_trace(go.Scatter(x=[0, 7.5], y=[0, 0], mode="lines", line=dict(color=GREY, width=4), showlegend=False))
for f in range(1, 7):
    fig.add_trace(go.Scatter(x=[f, f], y=[0, 1 / 6], mode="lines", line=dict(color=BLUE, width=6), showlegend=False))
fig.add_trace(go.Scatter(x=np.arange(1, 7), y=[1 / 6] * 6, mode="markers", marker=dict(color=BLUE, size=16),
                         showlegend=False))
for xv, txt in ((1.5, "f(1.5) = 0"), (7, "f(7) = 0")):
    fig.add_trace(go.Scatter(x=[xv], y=[0], mode="markers", marker=dict(color=RED, size=16, symbol="circle-open",
                             line=dict(width=3)), showlegend=False))
    fig.add_annotation(x=xv, y=0, text=txt, ay=-60, ax=0, arrowcolor=RED, font=dict(color=RED))
fig.add_annotation(x=3.5, y=1 / 6, yshift=28, text="f(x) = 1/6 at each face 1 to 6", showarrow=False,
                   font=dict(color=BLUE))
fig.update_layout(**LAY, width=900, height=440, margin=dict(l=70, r=20, t=20, b=60),
                  xaxis=dict(title="x", range=[0, 7.6], dtick=1), yaxis=dict(title="f(x)", range=[-0.02, 0.24]))
save(fig, "die_pmf_function")

# 5: the rule 6 - |x - 7|
fig = go.Figure(go.Bar(x=x2, y=pairs, marker_color=[RED if x == 9 else BLUE for x in x2], text=pairs,
                       textposition="outside", showlegend=False))
fig.add_shape(type="line", x0=7, x1=9, y0=6.6, y1=6.6, line=dict(color=RED, width=3), opacity=1)
fig.add_annotation(x=8, y=6.6, yshift=18, text="distance 2 from 7", showarrow=False, font=dict(color=RED))
fig.add_annotation(x=10.6, y=5.6, text="6 - 2 = 4 pairs<br>f(9) = 4/36", showarrow=False,
                   xanchor="left", align="left", font=dict(color=RED))
assert pairs[x2 == 9][0] == 4 and round(4 / 36, 3) == 0.111
fig.update_layout(**LAY, width=900, height=480, margin=dict(l=70, r=20, t=20, b=60),
                  xaxis=dict(title="sum x", dtick=1), yaxis=dict(title="pairs giving x (out of 36)", range=[0, 7.6]))
save(fig, "tent_rule")

# 6: Bernoulli and binomial
binom = np.array([comb(4, k) * 0.5 ** 4 for k in range(5)])
assert binom[2] == 0.375 and abs(binom.sum() - 1) < 1e-12
fig = make_subplots(rows=1, cols=2, column_widths=[0.38, 0.62], horizontal_spacing=0.12,
                    subplot_titles=["Bernoulli, p = 0.3", "binomial, n = 4, p = 0.5: heads in 4 tosses"])
fig.add_trace(go.Bar(x=[0, 1], y=[0.7, 0.3], marker_color=[GREY, GREEN], text=["0.7", "0.3"],
                     textposition="outside", showlegend=False), 1, 1)
fig.add_trace(go.Bar(x=list(range(5)), y=binom, marker_color=[RED if k == 2 else BLUE for k in range(5)],
                     text=[f"{v:.4g}" for v in binom], textposition="outside", showlegend=False), 1, 2)
fig.update_xaxes(title="k (1 = success)", tickvals=[0, 1], row=1, col=1)
fig.update_xaxes(title="k heads", dtick=1, row=1, col=2)
fig.update_yaxes(title="P(X = k)", range=[0, 0.85], row=1, col=1); fig.update_yaxes(range=[0, 0.85], row=1, col=2)
fig.update_layout(**LAY, width=1000, height=460, margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font=dict(family="Latin Modern Roman", size=21))
save(fig, "bernoulli_binomial")

# 4: simulated PMF as the number of rolls grows (prefixes of the Note's 10,000 rolls, seed 42)
rolls = np.random.default_rng(42).integers(1, 7, 10_000)
assert (rolls == 1).sum() == 1681
far10 = np.abs(np.bincount(rolls[:10], minlength=7)[1:] / 10 - 1 / 6).max()
assert round(far10, 3) == 0.133   # "0.133 away after 10 rolls" in the text
NS = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10_000]


def frame(n):
    share = np.bincount(rolls[:n], minlength=7)[1:] / n
    worst = np.abs(share - 1 / 6).max()
    fig = go.Figure(go.Bar(x=np.arange(1, 7), y=share, marker_color=BLUE, text=[f"{s:.3f}" for s in share],
                           textposition="outside", showlegend=False))
    fig.add_hline(y=1 / 6, line=dict(color=RED, dash="dash", width=3), layer="above", opacity=1)
    fig.add_annotation(x=6.45, y=1 / 6, text="1/6", xanchor="left", showarrow=False, font=dict(color=RED, size=22))
    fig.update_layout(**LAY, width=900, height=560, margin=dict(l=80, r=60, t=80, b=60),
                      title=dict(text=f"{n:,} rolls: farthest face is {worst:.3f} from 1/6", x=0.5),
                      xaxis=dict(title="face", dtick=1), yaxis=dict(title="share of rolls", range=[0, 0.45]))
    return fig


if __name__ == "__main__":
    tmp = here / ".lln"
    tmp.mkdir(exist_ok=True)
    n = 0
    for N in NS:
        frame(N).write_image(tmp / f"{n:03d}.png")
        for _ in range(2):                         # 3 copies: each sample size stays up 1.5 s at 2 fps
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + 1:03d}.png"); n += 1
        n += 1
    for _ in range(6):
        shutil.copy(tmp / f"{n - 1:03d}.png", tmp / f"{n:03d}.png"); n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(here / "pmf_settles.gif")], check=True)
    ims = []
    for i, N in enumerate((10, 100, 1000, 10_000)):
        frame(N).write_image(tmp / f"k{i}.png"); ims.append(Image.open(tmp / f"k{i}.png").convert("RGB"))
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(here / "pmf_settles_frames.png")
    shutil.rmtree(tmp)
