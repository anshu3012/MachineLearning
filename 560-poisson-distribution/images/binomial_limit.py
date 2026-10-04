"""Where the Poisson distribution comes from (section 7): a day is cut into n moments, and in each one a question
arrives with probability p = 4/n. Top: one simulated day, its moments (grid) and the questions that arrived (dots).
Bottom: the binomial PMF B(n, 4/n) (bars) settling onto the Poisson PMF with lambda = 4 (dots) as n grows.
Run: python binomial_limit.py  -> binomial_limit.gif, binomial_limit_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#BDBDBD"
LAM, NS = 4, [5, 6, 8, 10, 15, 20, 40, 100, 1000]
y = np.arange(0, 13)
gap = lambda n: np.abs(stats.binom.pmf(np.arange(n + 1), n, LAM / n) - stats.poisson.pmf(np.arange(n + 1), LAM)).max()
assert [round(gap(10), 3), round(gap(40), 3), round(gap(1000), 4)] == [0.055, 0.011, 0.0004]   # section 7 table
rng = np.random.default_rng(42)
days = {n: np.flatnonzero(rng.random(n) < LAM / n) for n in NS}   # moments in which a question arrived


def frame(n):
    fig = make_subplots(rows=2, cols=1, row_heights=[0.22, 0.78], vertical_spacing=0.16,
                        subplot_titles=[f"one day = {n} moments, p = 4/{n} = {LAM / n:.3g} each: "
                                        f"{len(days[n])} questions", "number of questions in a day"])
    fig.add_scatter(x=(days[n] + 0.5) / n * 24, y=np.full(len(days[n]), 0.5), mode="markers",
                    marker=dict(color=ORANGE, size=18, line=dict(width=1, color="white")), showlegend=False, row=1, col=1)
    for k in range(n if n <= 40 else 1):                     # moments as boxes; beyond 40 too thin: one outline
        w = 24 / n if n <= 40 else 24
        fig.add_shape(type="rect", x0=k * w, x1=(k + 1) * w, y0=0.15, y1=0.85, xref="x", yref="y",
                      fillcolor="white", line=dict(color=GREY, width=1.5), layer="below")
    fig.add_bar(x=y, y=stats.binom.pmf(y, n, LAM / n), marker_color=BLUE, opacity=0.7, name=f"binomial B({n}, 4/{n})",
                row=2, col=1)
    fig.add_scatter(x=y, y=stats.poisson.pmf(y, LAM), mode="markers", marker=dict(color="black", size=14),
                    name="Poisson, λ = 4", row=2, col=1)
    fig.add_annotation(x=11, y=0.3, xref="x2", yref="y2", text=f"largest gap<br><b>{gap(n):.4f}</b>",
                       showarrow=False, font=dict(size=26))
    fig.update_xaxes(range=[0, 24], showticklabels=False, ticks="", row=1, col=1)
    fig.update_yaxes(range=[0, 1], visible=False, row=1, col=1)
    fig.update_xaxes(tickvals=list(range(0, 13, 2)), range=[-0.6, 12.6], row=2, col=1)
    fig.update_yaxes(title_text="probability", range=[0, 0.42], row=2, col=1)
    fig.update_layout(template="simple_white", width=900, height=700, bargap=0.15,
                      font=dict(family="Latin Modern Roman", size=24),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.1),
                      margin=dict(l=90, r=30, t=60, b=40))
    fig.update_annotations(font_size=24, selector=dict(xref="paper"))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".binlim_frames"
    tmp.mkdir(exist_ok=True)
    k, keys = 0, {}
    for i, n in enumerate(NS):
        frame(n).write_image(tmp / f"{k:03d}.png")
        keys[n] = k
        for _ in range(11 if i == len(NS) - 1 else 3):
            shutil.copy(tmp / f"{k:03d}.png", tmp / f"{k + 1:03d}.png")
            k += 1
        k += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "binomial_limit.gif")], check=True)
    ims = [Image.open(tmp / f"{keys[n]:03d}.png").convert("RGB") for n in (5, 10, 40, 1000)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "binomial_limit_frames.png")
    shutil.rmtree(tmp)
