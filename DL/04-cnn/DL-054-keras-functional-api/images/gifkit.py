"""Helper for the animations (no output when run): Plotly figures -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

from PIL import Image


def save_gif(figs, name, here, keys, fps=1.5, width=760, cols=2, holds=None):
    """Write figs as here/name.gif and the frames listed in keys as here/name_frames.png.
    holds[i] repeats frame i that many times (default 1; the last frame is held 4 times)."""
    tmp = Path(here) / f".{name}_tmp"
    tmp.mkdir(exist_ok=True)
    pngs = []
    for i, f in enumerate(figs):
        p = tmp / f"k{i:03d}.png"
        f.write_image(p)
        pngs.append(p)
    holds = holds or [1] * (len(figs) - 1) + [4]
    j = 0
    for p, h in zip(pngs, holds):
        for _ in range(h):
            shutil.copy(p, tmp / f"{j:03d}.png")
            j += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(tmp / "%03d.png"), "-vf",
                    f"scale={width}:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(Path(here) / f"{name}.gif")], check=True)
    ims = [Image.open(pngs[k]).convert("RGB") for k in keys]
    w, h = ims[0].size
    rows = -(-len(ims) // cols)
    sheet = Image.new("RGB", (cols * w + (cols - 1) * 16, rows * h + (rows - 1) * 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * (w + 16), (i // cols) * (h + 16)))
    sheet.save(Path(here) / f"{name}_frames.png")
    shutil.rmtree(tmp)
