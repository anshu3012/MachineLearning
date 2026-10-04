"""Shared helper for this Note's animations: render Plotly figures to a GIF (ffmpeg) plus a grid of key frames
for the PDF (tools/media-swap.lua swaps <name>.gif for <name>_frames.png). Not a figure itself."""
import shutil
import subprocess
from pathlib import Path

import plotly.io as pio
from PIL import Image

FONT = dict(family="Latin Modern Roman", size=22)
BLUE, ORANGE, GREEN, RED, GREY, PURPLE = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#9a9a9a", "#B279A2"


def save_gif(figs, name, here, keys, fps=2, holds=None, width=760, cols=2):
    """figs: list of go.Figure, one per distinct frame. holds: how many GIF frames each figure lasts
    (default 2, last one 6). keys: indices of the figures shown in the PDF frame grid."""
    here = Path(here)
    tmp = here / f".{name}_frames"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir()
    paths = [tmp / f"f{i:03d}.png" for i in range(len(figs))]
    pio.write_images(figs, paths, width=[f.layout.width or 900 for f in figs],
                     height=[f.layout.height or 600 for f in figs])
    holds = holds or [2] * (len(figs) - 1) + [6]
    j = 0
    for p, h in zip(paths, holds):
        for _ in range(h):
            shutil.copy(p, tmp / f"{j:04d}.png")
            j += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(tmp / "%04d.png"), "-vf",
                    f"scale={width}:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(here / f"{name}.gif")], check=True)
    ims = [Image.open(paths[k]).convert("RGB") for k in keys]
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w + 16 * (cols - 1), rows * h + 16 * (rows - 1)), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * (w + 16), (i // cols) * (h + 16)))
    sheet.save(here / f"{name}_frames.png")
    shutil.rmtree(tmp)
