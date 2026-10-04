"""The two parameters of the normal curve, one at a time, on the heights N(68, 3^2): first the mean slides (shape
unchanged), then the standard deviation grows (wider and lower, area still 1). The peak height 1/(sigma sqrt(2 pi))
is printed each frame.
Run: python param_sweep.py -> param_sweep.gif, param_sweep_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREY = "#4C78A8", "#F58518", "#6B6B6B"
x = np.linspace(50, 86, 700)
assert round(stats.norm(68, 3).pdf(68), 4) == 0.1330 and round(stats.norm(68, 3).pdf(72), 4) == 0.0547
STEPS = ([(m, 3.0, "μ") for m in np.r_[np.linspace(68, 62, 7), np.linspace(62, 74, 13), np.linspace(74, 68, 7)]]
         + [(68, s, "σ") for s in np.r_[np.linspace(3, 1.5, 7), np.linspace(1.5, 5, 15)]])


def frame(mu, sd, moving):
    d = stats.norm(mu, sd)
    area = np.trapezoid(d.pdf(x), x)
    fig = go.Figure()
    fig.add_scatter(x=x, y=stats.norm(68, 3).pdf(x), mode="lines", name="N(68, 3²), the heights",
                    line=dict(color=GREY, width=2.5, dash="dash"))
    fig.add_scatter(x=x, y=d.pdf(x), mode="lines", fill="tozeroy", fillcolor="rgba(245,133,24,0.25)",
                    name=f"μ = {mu:.1f}, σ = {sd:.2f}", line=dict(color=ORANGE, width=4))
    fig.add_annotation(x=mu, y=d.pdf(mu), text=f"peak {d.pdf(mu):.3f}", showarrow=True, ay=-35,
                       font=dict(size=20, color=ORANGE))
    fig.add_annotation(x=0.98, y=0.95, xref="paper", yref="paper", xanchor="right", showarrow=False,
                       text=f"area = {area:.3f}", font=dict(size=22, color=BLUE))
    head = ("changing μ slides the curve; the shape stays" if moving == "μ"
            else "changing σ: wider and lower, or narrower and taller")
    fig.update_layout(template="simple_white", width=900, height=560, font=dict(family="Latin Modern Roman", size=20),
                      title=dict(text=head, x=0.5), xaxis=dict(title="height (inches)", range=[50, 86], dtick=3),
                      yaxis=dict(title="density", range=[0, 0.31]), legend=dict(x=0.01, y=0.98),
                      margin=dict(l=70, r=20, t=70, b=55))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".param_sweep_frames"
    tmp.mkdir(exist_ok=True)
    for k, (mu, sd, mv) in enumerate(STEPS):
        frame(mu, sd, mv).write_image(tmp / f"{k:03d}.png")
    last = len(STEPS) - 1
    for k in range(last + 1, last + 9):
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "8", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "param_sweep.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (6, 19, 33, last)]   # mu 62, 74; sigma 1.5, 5
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "param_sweep_frames.png")
    shutil.rmtree(tmp)
