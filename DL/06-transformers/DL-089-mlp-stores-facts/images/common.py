"""Shared colours, font and GIF helpers for this Note's figures (no output when run).
Colour rule (after Sanderson 2024, Ch 5): learned weights in blue, data flowing through the model in grey."""
import shutil
import subprocess
from pathlib import Path

from PIL import Image

BLUE, ORANGE, GREEN, RED, PURPLE, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)
DATA = Path(__file__).parent.parent / "data"


def grid(frames, out, gap=16):
    """2 x 2 sheet of four key frames (PIL images) for the PDF."""
    frames = [f.convert("RGB") for f in frames[:4]]
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames):
        sheet.paste(f, ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


def gif(src, out, fps=12, width=720, framerate=None):
    """ffmpeg palette GIF from an mp4 or a %03d.png pattern."""
    inp = ["-framerate", str(framerate), "-i", str(src)] if framerate else ["-i", str(src)]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inp, "-vf",
                    f"fps={fps},scale={width}:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(out)], check=True)


def render_manim(scene_cls, name, here):
    """Render a Manim scene to <name>.gif and <name>_frames.png (scene.snaps holds 4 PIL key frames)."""
    from manim import WHITE, tempconfig
    media = here / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = scene_cls()
        scene.render()
    gif(next(media.rglob(f"{name}.mp4")), here / f"{name}.gif")
    grid(scene.snaps, here / f"{name}_frames.png")
    shutil.rmtree(media)
