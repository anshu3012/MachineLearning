"""Animation helper: Plotly figures -> ffmpeg GIF plus a grid of key frames for the PDF. Imported, not run."""
import shutil
import subprocess
from pathlib import Path

import plotly.io as pio
from PIL import Image


def save(name, figs, seq, keys, here, fps=4, gif_width=760, cols=2):
    """figs: the distinct frames. seq: indices into figs, in play order (repeat an index to hold a frame).
    keys: indices into figs for the PDF grid. Writes <name>.gif and <name>_frames.png next to the script."""
    here = Path(here)
    tmp = here / f".{name}_tmp"
    tmp.mkdir(exist_ok=True)
    w, h = figs[0].layout.width, figs[0].layout.height
    pio.write_images(figs, [tmp / f"f{i:03d}.png" for i in range(len(figs))], width=w, height=h)
    for k, i in enumerate(seq):
        shutil.copy(tmp / f"f{i:03d}.png", tmp / f"s{k:04d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(tmp / "s%04d.png"), "-vf",
                    f"scale={gif_width}:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(here / f"{name}.gif")], check=True)
    imgs = [Image.open(tmp / f"f{i:03d}.png").convert("RGB") for i in keys]
    rows = -(-len(imgs) // cols)
    sheet = Image.new("RGB", (cols * w + (cols - 1) * 16, rows * h + (rows - 1) * 16), "white")
    for i, im in enumerate(imgs):
        sheet.paste(im, ((i % cols) * (w + 16), (i // cols) * (h + 16)))
    sheet.save(here / f"{name}_frames.png")
    shutil.rmtree(tmp)
