"""Shared helper for this Note's animations: render Plotly figures as frames, join them into a GIF with ffmpeg, and
save a grid of key frames for the PDF (no output when run on its own)."""
import shutil
import subprocess
from pathlib import Path

from PIL import Image

FONT = dict(family="Latin Modern Roman", size=22)
BLUE, ORANGE, GREEN, RED, GREY, PURPLE = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B", "#B279A2"


def make_gif(figs, out, fps=6, holds=None, keys=None, cols=2, width=900):
    """figs: list of Plotly figures, one per distinct frame. holds[i]: how many GIF frames figure i stays on screen.
    keys: indexes of figures for the frame grid (default: first, last). Writes out.gif and out_frames.png."""
    out = Path(out)
    tmp = out.parent / f".{out.stem}_tmp"
    tmp.mkdir(exist_ok=True)
    holds = holds or [1] * len(figs)
    pngs = []
    for i, f in enumerate(figs):
        p = tmp / f"f{i:03d}.png"
        f.write_image(p)
        pngs.append(p)
    j = 0
    for p, h in zip(pngs, holds):
        for _ in range(h):
            shutil.copy(p, tmp / f"{j:04d}.png")
            j += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(tmp / "%04d.png"), "-vf",
                    f"scale={width}:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse",
                    str(out.with_suffix(".gif"))], check=True)
    keys = keys if keys is not None else [0, len(figs) - 1]
    ims = [Image.open(pngs[k]).convert("RGB") for k in keys]
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w + (cols - 1) * 16, rows * h + (rows - 1) * 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * (w + 16), (i // cols) * (h + 16)))
    sheet.save(out.parent / f"{out.stem}_frames.png")
    shutil.rmtree(tmp)
    size = out.with_suffix(".gif").stat().st_size / 1e6
    assert size < 3.2, f"{out.name}.gif is {size:.1f} MB"
