"""Two tomato fields, a two-sample t statistic built step by step. Left: the standard error of the difference is built
from one variance part per field, 0.5^2/22 = 0.01136 and 0.3^2/24 = 0.00375, then square-rooted: 0.123 m. Right: the
gap 1.3 - 1.6 = -0.3 m divided by 0.123 gives t = -2.44 on the t curve; both tails beyond +-2.44 are the two-tailed
p-value: 0.020 with Welch's df 33.8, 0.024 with the conservative df 21.
Run: python tomato_t.py  -> tomato_t.gif, tomato_t_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
from scipy import stats

HERE = Path(__file__).parent
RED, BLUE, ORANGE, GREEN = "#E45756", "#4C78A8", "#F58518", "#54A24B"
VA, VB = 0.5 ** 2 / 22, 0.3 ** 2 / 24
SE = np.sqrt(VA + VB)
T = (1.3 - 1.6) / SE
DFW = (VA + VB) ** 2 / (VA ** 2 / 21 + VB ** 2 / 23)
assert round(T, 2) == -2.44 and round(2 * stats.t.cdf(T, DFW), 3) == 0.020 and round(2 * stats.t.cdf(T, 21), 3) == 0.024
x = np.linspace(-4, 4, 600)


def frame(step, tval=T):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.38, 0.62], horizontal_spacing=0.08,
                        subplot_titles=("variance of the gap", "t curve, Welch df 33.8"))
    fig.update_annotations(font_size=24)
    fig.add_bar(x=["gap"], y=[VA], marker_color=BLUE, row=1, col=1, width=0.5)
    fig.add_annotation(x="gap", y=VA / 2, text="field A<br>0.5²/22", showarrow=False, font=dict(color="white", size=22),
                       row=1, col=1)
    if step >= 1:
        fig.add_bar(x=["gap"], y=[VB], marker_color=ORANGE, row=1, col=1, width=0.5)
        fig.add_annotation(x="gap", y=VA + VB / 2, text="field B 0.3²/24", showarrow=False,
                           font=dict(color="white", size=18), row=1, col=1)
    if step >= 2:
        fig.add_annotation(x="gap", y=(VA + VB) * 1.17, text=f"SE = √{VA + VB:.4f}<br>= <b>{SE:.3f} m</b>",
                           showarrow=False, font=dict(size=22), row=1, col=1)
    fig.add_scatter(x=x, y=stats.t.pdf(x, DFW), mode="lines", line=dict(color="black", width=3), row=1, col=2)
    if step >= 3:
        for lo, hi in ((-4, -abs(tval)), (abs(tval), 4)):
            s = x[(x >= lo) & (x <= hi)]
            fig.add_scatter(x=s, y=stats.t.pdf(s, DFW), fill="tozeroy", fillcolor="rgba(228,87,86,0.45)",
                            line=dict(width=0), row=1, col=2)
        fig.add_scatter(x=[tval], y=[0], mode="markers", marker=dict(size=20, color=GREEN, line=dict(width=2)),
                        cliponaxis=False, row=1, col=2)
        fig.add_annotation(x=tval, y=0.1, text=f"<b>t = {tval:.2f}</b>".replace("-", "−"), showarrow=False,
                           font=dict(size=24, color=GREEN), row=1, col=2)
        p = 2 * stats.t.cdf(-abs(tval), DFW)
        box = (f"t = −0.3 / {SE:.3f} = −2.44<br>" if tval == T else "") + f"both red tails: p = <b>{p:.3f}</b>"
        if step >= 4:
            box += " (df 21: 0.024)<br><b>p < 0.05: reject H₀</b>"
        fig.add_annotation(x=0.99, y=0.92, xref="paper", yref="paper", xanchor="right", yanchor="top",
                           showarrow=False, align="left", bgcolor="white", text=box, font=dict(size=22))
    fig.update_yaxes(range=[0, (VA + VB) * 1.35], showticklabels=False, row=1, col=1)
    fig.update_yaxes(range=[0, 0.66], showticklabels=False, row=1, col=2)
    fig.update_xaxes(showticklabels=False, row=1, col=1)
    fig.update_xaxes(title_text="t", range=[-4, 4], dtick=1, row=1, col=2)
    fig.update_layout(template="simple_white", width=1000, height=540, showlegend=False, barmode="stack",
                      font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text="Field A: 1.3 m, field B: 1.6 m. Is the gap −0.3 m real?", x=0.5, y=0.97),
                      margin=dict(l=30, r=30, t=100, b=60))
    return fig


PLAN = [(0, T, 5), (1, T, 5), (2, T, 7)] + [(3, t, 1) for t in (-0.5, -1.0, -1.5, -2.0)] + [(3, T, 4), (4, T, 14)]

if __name__ == "__main__":
    tmp = HERE / ".tomato_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, []
    for i, (step, t, hold) in enumerate(PLAN):
        frame(step, t).write_image(tmp / f"{n:03d}.png")
        if i in (1, 2, 4, len(PLAN) - 1):
            keys.append(n)
        for _ in range(hold - 1):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + 1:03d}.png")
            n += 1
        n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=700:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "tomato_t.gif")], check=True)
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "tomato_t_frames.png")
    shutil.rmtree(tmp)
