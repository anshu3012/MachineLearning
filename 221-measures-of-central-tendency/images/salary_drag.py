"""The tenth salary of the class is dragged up from 40 to 2,000 thousand rupees a month (the founder of section 3.1).
Top: the ten salaries on a log scale, with the mean, median and 10% trimmed mean as lines.
Bottom: each measure against the tenth salary. The mean climbs with it; the median and trimmed mean stay put.
Run: python salary_drag.py -> salary_drag.gif, salary_drag_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image
from plotly.subplots import make_subplots
from scipy import stats

HERE = Path(__file__).parent
RED, BLUE, GREEN, GREY = "#E45756", "#4C78A8", "#54A24B", "#6B6B6B"
nine = np.array([28, 30, 31, 32, 33, 35, 36, 38, 40])     # thousand rupees a month, as in Figure 2
TENTH = np.unique(np.round(np.geomspace(40, 2000, 30)))
MEASURES = [("mean", np.mean, RED, "solid"), ("median", np.median, BLUE, "dash"),
            ("10% trimmed mean", lambda x: stats.trim_mean(x, 0.1), GREEN, "dot")]
track = {name: np.array([f(np.append(nine, t)) for t in TENTH]) for name, f, *_ in MEASURES}
assert abs(track["mean"][-1] - 230.3) < 0.05 and track["median"][-1] == 34 and track["10% trimmed mean"][-1] == 34.375


def frame(i):
    t = TENTH[i]
    x = np.append(nine, t)
    fig = make_subplots(rows=2, cols=1, row_heights=[0.4, 0.6], vertical_spacing=0.2,
                        subplot_titles=[f"Tenth salary: {t:,.0f} thousand", "Each measure as the tenth salary grows"])
    fig.add_scatter(x=nine, y=np.zeros(9), mode="markers", marker=dict(size=14, color=GREY), row=1, col=1)
    fig.add_scatter(x=[t], y=[0], mode="markers", marker=dict(size=22, color="black", symbol="star"), row=1, col=1)
    for k, (name, f, c, dash) in enumerate(MEASURES):
        v = track[name][i]
        fig.add_shape(type="line", x0=v, x1=v, y0=-0.6, y1=0.6, line=dict(color=c, width=4, dash=dash),
                      opacity=1, row=1, col=1)
        fig.add_scatter(x=TENTH[:i + 1], y=track[name][:i + 1], mode="lines", line=dict(color=c, width=4, dash=dash),
                        row=2, col=1)
        fig.add_annotation(x=0.02, y=0.97 - 0.13 * k, xref="x2 domain", yref="y2 domain", xanchor="left",
                           showarrow=False, text=f"{name}: {v:.1f}", font=dict(size=22, color=c))
    fig.update_xaxes(type="log", range=[np.log10(20), np.log10(3000)], tickvals=[30, 100, 300, 1000, 2000],
                     title_text="salary (thousand rupees a month, log scale)", row=1, col=1)
    fig.update_yaxes(visible=False, range=[-1, 1], row=1, col=1)
    fig.update_xaxes(type="log", range=[np.log10(35), np.log10(2300)], tickvals=[40, 100, 300, 1000, 2000],
                     title_text="tenth salary", row=2, col=1)
    fig.update_yaxes(range=[0, 250], title_text="measure", row=2, col=1)
    fig.update_annotations(selector=dict(xref="paper"), font_size=22)
    fig.update_layout(template="simple_white", width=900, height=760, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=20), margin=dict(l=70, r=30, t=60, b=60))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".drag_frames"
    tmp.mkdir(exist_ok=True)
    for i in range(len(TENTH)):
        frame(i).write_image(tmp / f"{i:03d}.png")
    last = len(TENTH) - 1
    for k in range(last + 1, last + 9):                      # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "salary_drag.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (0, last // 3, 2 * last // 3, last)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "salary_drag_frames.png")
    shutil.rmtree(tmp)
