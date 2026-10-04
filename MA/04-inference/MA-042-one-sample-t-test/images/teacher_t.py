"""Teachers' experience, a one-sample t-test step by step: H0 mu = 5, H1 mu < 5, n = 25, mean 4, s = 2.
The t value walks from 0 to (4 - 5)/(2/5) = -2.5 on the t curve with 24 degrees of freedom while the left-tail
area (the p-value) shrinks to 0.0098; then the 5% cutoff -1.711 appears: t is beyond it, reject H0.
Run: python teacher_t.py  -> teacher_t.gif, teacher_t_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
RED, GREEN, GREY = "#E45756", "#54A24B", "#888888"
DF, T = 24, (4 - 5) / (2 / np.sqrt(25))
CUT = stats.t.ppf(0.05, DF)
assert np.isclose(T, -2.5) and round(stats.t.cdf(T, DF), 4) == 0.0098 and round(CUT, 3) == -1.711
x = np.linspace(-4, 4, 700)


def frame(t, cutoff=False):
    fig = go.Figure()
    s = x[x <= t]
    fig.add_scatter(x=s, y=stats.t.pdf(s, DF), fill="tozeroy", fillcolor="rgba(228,87,86,0.45)", line=dict(width=0))
    fig.add_scatter(x=x, y=stats.norm.pdf(x), mode="lines", line=dict(color=GREY, width=2, dash="dash"))
    fig.add_scatter(x=x, y=stats.t.pdf(x, DF), mode="lines", line=dict(color="black", width=3))
    fig.add_scatter(x=[t], y=[0], mode="markers", marker=dict(size=22, color=GREEN, line=dict(width=2, color="black")),
                    cliponaxis=False)
    fig.add_annotation(x=t, y=0.09, text=f"<b>t = {t:.2f}</b>".replace("-", "−"), showarrow=False, font=dict(size=26, color=GREEN))
    p = stats.t.cdf(t, DF)
    text = f"area left of t<br>= <b>{p:.4f}</b>"
    if cutoff:
        fig.add_vline(x=CUT, line=dict(color=RED, width=3, dash="dash"), opacity=1)
        fig.add_annotation(x=CUT, y=0.36, text="5% cutoff<br>−1.711", showarrow=False, xanchor="left", xshift=8,
                           font=dict(size=22, color=RED))
        text = f"p = <b>{p:.4f}</b> < 0.05<br><b>reject H₀</b>"
    fig.add_annotation(x=0.99, y=0.97, xref="paper", yref="paper", xanchor="right", yanchor="top", showarrow=False,
                       align="left", bgcolor="white", text=text, font=dict(size=26))
    fig.add_annotation(x=0.01, y=0.97, xref="paper", yref="paper", xanchor="left", yanchor="top", showarrow=False,
                       align="left", text="black: t, 24 df<br><span style='color:#888888'>dashed: normal</span>",
                       font=dict(size=20))
    fig.update_layout(template="simple_white", width=900, height=540, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text="t = (4 − 5) / (2 / √25)", x=0.5, y=0.96),
                      xaxis=dict(title="t", range=[-4, 4], dtick=1), yaxis=dict(showticklabels=False, range=[0, 0.45]),
                      margin=dict(l=30, r=30, t=70, b=60))
    return fig


PLAN = [(0.0, False, 5)] + [(t, False, 1) for t in (-0.5, -1.0, -1.5, -2.0)] + [(T, False, 8), (T, True, 14)]

if __name__ == "__main__":
    tmp = HERE / ".teacher_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, []
    for i, (t, cut, hold) in enumerate(PLAN):
        frame(t, cut).write_image(tmp / f"{n:03d}.png")
        if i in (0, 3, 5, 6):
            keys.append(n)
        for _ in range(hold - 1):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + 1:03d}.png")
            n += 1
        n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "teacher_t.gif")], check=True)
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "teacher_t_frames.png")
    shutil.rmtree(tmp)
