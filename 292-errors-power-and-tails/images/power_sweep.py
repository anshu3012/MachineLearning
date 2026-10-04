"""What moves the power of the training-program z-test (H0: mu = 50, H1: mu > 50, sigma = 5), one knob at a time:
1. alpha from 0.10 down to 0.01 (n = 30, true mean 52): the critical line moves right, beta grows;
2. n from 10 up to 100 (alpha = 0.05, true mean 52): the H1 curve moves away, power climbs to 0.99;
3. the true mean from 50 to 54 (alpha = 0.05, n = 30): a bigger effect is easier to detect.
Left: z under H0 (blue) and under the true mean (black dashed), red = alpha, orange = beta, green = power.
Right: the three probabilities as bars.
Run: python power_sweep.py -> power_sweep.gif, power_sweep_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from plotly.subplots import make_subplots
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED = "#4C78A8", "#F58518", "#54A24B", "#E45756"
MU0, SIGMA = 50, 5
Z = np.linspace(-3.5, 8, 1000)


def probs(alpha, n, mu):
    c = stats.norm.ppf(1 - alpha)
    d = (mu - MU0) / (SIGMA / np.sqrt(n))
    beta = stats.norm.cdf(c - d)
    return c, d, beta


# the Note's numbers (section 3, 4 and its Extra)
assert round(1 - probs(0.05, 30, 52)[2], 2) == 0.71 and round(1 - probs(0.01, 30, 52)[2], 2) == 0.45
assert [round(1 - probs(0.05, n, 52)[2], 2) for n in (60, 100)] == [0.93, 0.99]


def frame(alpha, n, mu, act):
    c, d, beta = probs(alpha, n, mu)
    h0, h1 = stats.norm.pdf(Z), stats.norm.pdf(Z, loc=d)
    L, R = Z <= c, Z >= c
    fig = make_subplots(rows=1, cols=2, column_widths=[0.72, 0.28], horizontal_spacing=0.09)
    fig.add_scatter(x=Z[R], y=h1[R], fill="tozeroy", fillcolor="rgba(84,162,75,0.4)", line_width=0, row=1, col=1)
    fig.add_scatter(x=Z[L], y=h1[L], fill="tozeroy", fillcolor="rgba(245,133,24,0.5)", line_width=0, row=1, col=1)
    fig.add_scatter(x=Z[R], y=h0[R], fill="tozeroy", fillcolor="rgba(228,87,86,0.8)", line_width=0, row=1, col=1)
    fig.add_scatter(x=Z, y=h0, mode="lines", line=dict(color=BLUE, width=3), row=1, col=1)
    fig.add_scatter(x=Z, y=h1, mode="lines", line=dict(color="black", width=3, dash="dash"), row=1, col=1)
    fig.add_vline(x=c, line=dict(color="black", width=2.5), opacity=1, row=1, col=1)
    fig.add_annotation(x=0, y=0.43, text="H₀: μ = 50", showarrow=False, font=dict(size=22, color=BLUE), bgcolor="white", row=1, col=1)
    fig.add_annotation(x=d, y=0.47, text=f"true μ = {mu:.1f}", showarrow=False, font=dict(size=22), bgcolor="white", row=1, col=1)
    fig.add_bar(x=["α", "β", "power"], y=[alpha, beta, 1 - beta], marker_color=[RED, ORANGE, GREEN],
                text=[f"{v:.2f}" for v in (alpha, beta, 1 - beta)], textposition="outside", textfont_size=24,
                row=1, col=2)
    knob = {1: f"<b>1. Lower α</b> (n = 30, true μ = 52): α = {alpha:.3f}",
            2: f"<b>2. Bigger sample</b> (α = 0.05, true μ = 52): n = {n:.0f}",
            3: f"<b>3. Bigger effect</b> (α = 0.05, n = 30): true μ = {mu:.1f}"}[act]
    fig.update_xaxes(title_text="z", range=[-3.5, 8], dtick=2, row=1, col=1)
    fig.update_yaxes(showticklabels=False, ticks="", range=[0, 0.52], row=1, col=1)
    fig.update_yaxes(range=[0, 1.18], dtick=0.25, title_text="probability", row=1, col=2)
    fig.update_layout(template="simple_white", width=1000, height=520, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), title=dict(text=knob, x=0.03, y=0.95),
                      margin=dict(l=20, r=20, t=80, b=60))
    return fig


def plan():
    out = [(float(a), 30, 52, 1) for a in np.geomspace(0.10, 0.01, 24)] + [(0.01, 30, 52, 1)] * 6
    out += [(0.05, float(n), 52, 2) for n in np.geomspace(10, 100, 24)] + [(0.05, 100, 52, 2)] * 6
    out += [(0.05, 30, float(m), 3) for m in np.linspace(50, 54, 24)] + [(0.05, 30, 54, 3)] * 10
    return out


if __name__ == "__main__":
    tmp = HERE / ".power_frames"
    tmp.mkdir(exist_ok=True)
    frames = plan()
    for j, args in enumerate(frames):
        frame(*args).write_image(tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "8", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "power_sweep.gif")], check=True)
    pick = [0, 23, 53, 83]                        # alpha 0.10, alpha 0.01, n = 100, true mean 54
    keys = [Image.open(tmp / f"{j:03d}.png").convert("RGB") for j in pick]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "power_sweep_frames.png")
    shutil.rmtree(tmp)
