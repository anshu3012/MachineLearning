"""Two ways to draw the same 100,000 CGPAs as bins narrow. Left: bar AREA = share of students (height = density);
the heights stay put and settle onto a curve. Right: bar HEIGHT = share of students (probability);
every bar sinks towards 0 and the shape is lost.
Run: python heights_vs_areas.py -> heights_vs_areas.gif, heights_vs_areas_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE, ORANGE, RED, GREY = "#4C78A8", "#F58518", "#E45756", "#6B6B6B"
CGPA = stats.beta(7, 3, scale=10)
SAMPLE = CGPA.rvs(100_000, random_state=np.random.default_rng(42))
WIDTHS = [2, 1, 0.5, 0.25, 0.1, 0.05]
peaks = {}


def frame(w):
    edges = np.arange(0, 10 + w / 2, w)
    share, _ = np.histogram(SAMPLE, bins=edges)
    share = share / len(SAMPLE)                                  # probability of each bin
    dens = share / w                                             # height that makes area = share
    assert abs((dens * w).sum() - 1) < 1e-9
    peaks[w] = (dens.max(), share.max())
    mids = edges[:-1] + w / 2
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                        subplot_titles=("height = share / width (area = share)", "height = share"))
    fig.add_bar(x=mids, y=dens, width=w, marker=dict(color=BLUE, line=dict(color="white", width=0.5 if w > 0.2 else 0)),
                row=1, col=1, showlegend=False)
    fig.add_bar(x=mids, y=share, width=w, marker=dict(color=RED, line=dict(color="white", width=0.5 if w > 0.2 else 0)),
                row=1, col=2, showlegend=False)
    if w == WIDTHS[-1]:
        xs = np.linspace(0, 10, 400)
        fig.add_scatter(x=xs, y=CGPA.pdf(xs), mode="lines", line=dict(color=ORANGE, width=4), row=1, col=1,
                        showlegend=False)
    fig.update_xaxes(title="CGPA", range=[0, 10], dtick=2)
    fig.update_yaxes(range=[0, 0.55], dtick=0.1, title="density", row=1, col=1)
    fig.update_yaxes(range=[0, 0.55], dtick=0.1, title="probability", row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=560, bargap=0,
                      font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=f"bin width {w}: tallest bar {dens.max():.2f} (left), {share.max():.3f} (right)",
                                 x=0.5, y=0.97), margin=dict(l=70, r=20, t=120, b=60))
    fig.update_annotations(font_size=22)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".hva_frames"
    tmp.mkdir(exist_ok=True)
    k = 0
    for w in WIDTHS:
        frame(w).write_image(tmp / f"key_{w}.png")
        for _ in range(4 if w != WIDTHS[-1] else 10):           # hold each width; hold the last longer
            shutil.copy(tmp / f"key_{w}.png", tmp / f"{k:03d}.png")
            k += 1
    print({w: (round(a, 3), round(b, 4)) for w, (a, b) in peaks.items()})
    assert peaks[WIDTHS[-1]][1] < 0.02 and abs(peaks[WIDTHS[-1]][0] - peaks[WIDTHS[2]][0]) < 0.05
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "heights_vs_areas.gif")], check=True)
    keys = [Image.open(tmp / f"key_{w}.png").convert("RGB") for w in (2, 0.5, 0.1, 0.05)]
    w_, h_ = keys[0].size
    sheet = Image.new("RGB", (2 * w_ + 16, 2 * h_ + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w_ + 16), (i // 2) * (h_ + 16)))
    sheet.save(HERE / "heights_vs_areas_frames.png")
    shutil.rmtree(tmp)
