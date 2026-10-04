"""Finding a critical value: slide a cutoff along the standard normal until the tail area beyond it equals alpha.
Right-tailed: the area drops to 0.05 at 1.645 (and to 0.025 at 1.96, too strict for one tail). Two-tailed:
both cutoffs at +-1.645 leave 0.10 (too loose), at +-1.96 they leave 0.05.
Run: python find_critical.py  -> find_critical.gif, find_critical_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
RED = "#E45756"
x = np.linspace(-4, 4, 600)
assert round(stats.norm.sf(1.645), 3) == 0.050 and round(stats.norm.sf(1.96), 3) == 0.025
assert round(2 * stats.norm.sf(1.645), 2) == 0.10 and round(2 * stats.norm.sf(1.96), 3) == 0.050


def frame(c, two, note=""):
    area = (2 if two else 1) * stats.norm.sf(c)
    fig = go.Figure()
    for lo, hi in ([(-4, -c), (c, 4)] if two else [(c, 4)]):
        s = x[(x >= lo) & (x <= hi)]
        fig.add_scatter(x=s, y=stats.norm.pdf(s), fill="tozeroy", fillcolor="rgba(228,87,86,0.4)", line=dict(width=0))
    fig.add_scatter(x=x, y=stats.norm.pdf(x), mode="lines", line=dict(color="black", width=3))
    for s in ((-1, 1) if two else (1,)):
        fig.add_vline(x=s * c, line=dict(color=RED, width=3, dash="dash"), opacity=1)
    hit = abs(area - 0.05) < 0.0005
    fig.add_annotation(x=-3.95, y=0.40, xanchor="left", showarrow=False, align="left", bgcolor="white",
                       text=f"cutoff {'±' if two else ''}{c:.3f}<br>red area = <b>{area:.3f}</b>"
                            + (" = α ✓" if hit else "") + (f"<br>{note}" if note else ""),
                       font=dict(size=26, color=RED if hit else "black"))
    fig.update_layout(template="simple_white", width=900, height=540, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=24),
                      title=dict(text=("two-tailed: α = 0.05 split over both tails" if two
                                       else "right-tailed: all of α = 0.05 in one tail"), x=0.5, y=0.96),
                      xaxis=dict(title="z", range=[-4, 4]), yaxis=dict(showticklabels=False, range=[0, 0.45]),
                      margin=dict(l=30, r=30, t=70, b=60))
    return fig


PLAN = [(c, False, "", 1) for c in (0.0, 0.5, 1.0, 1.3, 1.5)] + [(1.645, False, "", 8)] \
    + [(1.96, False, "1.96 here: too strict", 7)] \
    + [(1.645, True, "1.645 here: too loose", 7)] + [(c, True, "", 1) for c in (1.75, 1.85)] \
    + [(1.96, True, "", 10)]

if __name__ == "__main__":
    tmp = HERE / ".crit_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, []
    for i, (c, two, note, hold) in enumerate(PLAN):
        frame(c, two, note).write_image(tmp / f"{n:03d}.png")
        if i in (5, 6, 7, len(PLAN) - 1):
            keys.append(n)
        for _ in range(hold - 1):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + 1:03d}.png")
            n += 1
        n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "find_critical.gif")], check=True)
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "find_critical_frames.png")
    shutil.rmtree(tmp)
