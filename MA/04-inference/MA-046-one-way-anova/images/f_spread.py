"""Section 5: keep the group means at 5, 7, 9 and widen the spread inside each group. SSB stays 24, so MSB stays 12;
SSW = 6 s^2 grows, so F = 12 / s^2 falls from 12 (tight groups, s = 1) to 0.75 (spread-out groups, s = 4), crossing
the 5% critical value 5.14 on the way.
Run: python f_spread.py  -> f_spread.gif, f_spread_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
COLOURS = [BLUE, ORANGE, GREEN]
MEANS = np.array([5, 7, 9])
CRIT = stats.f.ppf(0.95, 2, 6)
groups = lambda s: [list(mu + s * np.array([-1, 0, 1])) for mu in MEANS]
for s, F in [(1, 12), (4, 0.75)]:                                      # the Note's two sets of groups
    assert np.isclose(stats.f_oneway(*groups(s)).statistic, F)
assert groups(4) == [[1, 5, 9], [3, 7, 11], [5, 9, 13]] and np.isclose(CRIT, 5.14, atol=5e-3)


def frame(s):
    g = groups(s)
    ssw = sum(((np.array(v) - np.mean(v)) ** 2).sum() for v in g)
    msb, msw = 24 / 2, ssw / 6
    F = msb / msw
    p = stats.f.sf(F, 2, 6)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45], horizontal_spacing=0.12,
                        subplot_titles=["same means, growing spread", "between vs within"])
    for i, (v, c) in enumerate(zip(g, COLOURS)):
        fig.add_trace(go.Scatter(x=[i] * 3, y=v, mode="markers", marker=dict(size=16, color=c), showlegend=False), 1, 1)
        fig.add_trace(go.Scatter(x=[i - 0.3, i + 0.3], y=[MEANS[i]] * 2, mode="lines", line=dict(color=c, width=4),
                                 showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=[-0.5, 2.5], y=[7, 7], mode="lines", line=dict(color="black", dash="dash", width=2),
                             showlegend=False), 1, 1)
    fig.add_trace(go.Bar(x=["MSB<br>(between)", "MSW<br>(within)"], y=[msb, msw], marker_color=[BLUE, GREY],
                         text=[f"{msb:.0f}", f"{msw:.2f}"], textposition="outside", textfont=dict(size=20),
                         showlegend=False), 1, 2)
    fig.update_xaxes(tickvals=[0, 1, 2], ticktext=["A", "B", "C"], range=[-0.6, 2.6], row=1, col=1)
    fig.update_yaxes(title="marks", range=[0, 14], row=1, col=1)
    fig.update_yaxes(range=[0, 19], row=1, col=2)
    verdict = "reject H0" if F > CRIT else "no evidence of a difference"
    col = RED if F > CRIT else GREY
    fig.update_layout(template="simple_white", width=1000, height=560, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=f"<b>F = {msb:.0f} / {msw:.2f} = {F:.2f}</b>   p = {p:.3f}   "
                                      f"<span style='color:{col}'><b>{verdict}</b></span>"
                                      f"<br><span style='font-size:17px'>5% critical value 5.14</span>", x=0.5, y=0.95),
                      margin=dict(l=70, r=20, t=120, b=50))
    fig.update_annotations(font_size=20)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".fspread_frames"
    tmp.mkdir(exist_ok=True)
    seq = [1.0] * 6 + list(np.linspace(1, 4, 24)) + [4.0] * 12
    for k, s in enumerate(seq):
        frame(s).write_image(tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "f_spread.gif")], check=True)
    near = 6 + int(np.argmin(np.abs(np.linspace(1, 4, 24) - np.sqrt(12 / CRIT))))   # the frame nearest F = 5.14
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (5, near, 20, len(seq) - 1)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "f_spread_frames.png")
    shutil.rmtree(tmp)
