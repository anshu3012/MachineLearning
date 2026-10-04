"""Flatten: the 28 rows of a 28 x 28 digit leave the image one by one and line up into one strip of 784 values (Manim).
The digit is the first training image (a 5) from results.json. In the strip every pixel is a thin bar with its grey level.
Run: python flatten.py -> flatten.mp4, .gif, _frames.png"""
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
import manimpango

for f in Path("/usr/share/texmf/fonts/opentype/public/lm").glob("lmroman10-*.otf"):   # pango on topgro misses LM
    manimpango.register_font(str(f))

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
img = np.array(json.loads((HERE / "results.json").read_text())["train_images"][0]) / 255
assert img.shape == (28, 28)
CELL, SW, SH = 0.13, 12.6 / 784, 0.7            # image cell; strip bar width and height
IMG_C, STRIP_Y = np.array([0, 1.0, 0]), -2.4


def grey(v):
    return interpolate_color(ManimColor(WHITE), ManimColor(BLACK), float(v))


class Flatten(Scene):
    def construct(self):
        snaps = []
        title = Text("Flatten: 28 rows of 28 pixels become one row of 784", font_size=34, weight=BOLD).to_edge(UP, buff=0.2)
        rows = [VGroup(*[Rectangle(width=CELL, height=CELL, stroke_width=0, fill_color=grey(img[r, c]), fill_opacity=1)
                         .move_to(IMG_C + np.array([(c - 13.5) * CELL, (13.5 - r) * CELL, 0])) for c in range(28)]) for r in range(28)]
        frame = Square(side_length=28 * CELL, color=GREY_C, stroke_width=2).move_to(IMG_C)
        strip_frame = Rectangle(width=784 * SW, height=SH, color=GREY_C, stroke_width=2).move_to([0, STRIP_Y, 0])
        lab_img = Text("image: 28 × 28", font_size=28).next_to(frame, LEFT, buff=0.4)
        counter = Text("values in the row: 0", font_size=30, color=BLUE_C).next_to(strip_frame, UP, buff=0.25)
        ends = VGroup(Text("pixel 1", font_size=24, color=GREY_C).next_to(strip_frame, DOWN, buff=0.12).align_to(strip_frame, LEFT),
                      Text("pixel 784", font_size=24, color=GREY_C).next_to(strip_frame, DOWN, buff=0.12).align_to(strip_frame, RIGHT))
        self.add(title, *rows, frame, strip_frame, lab_img, counter, ends)
        self.wait(0.8)
        x0 = -784 * SW / 2
        for r, row in enumerate(rows):
            target = VGroup(*[Rectangle(width=SW, height=SH, stroke_width=0, fill_color=grey(img[r, c]), fill_opacity=1)
                              .move_to([x0 + (r * 28 + c + 0.5) * SW, STRIP_Y, 0]) for c in range(28)])
            hl = SurroundingRectangle(row, color=ORANGE_C, buff=0.01, stroke_width=4)
            new = Text(f"values in the row: {28 * (r + 1)}", font_size=30, color=BLUE_C).move_to(counter)
            t = 0.7 if r < 3 else 0.22                       # first rows slowly, then faster
            self.add(hl)
            self.play(Transform(row.copy(), target), row.animate.set_opacity(0.25), run_time=t)
            self.remove(hl, counter)
            counter = new
            self.add(counter)
            if r in (2, 13):
                snaps.append(Image.fromarray(self.renderer.get_frame()))
        done = Text("one input node per value: 784 inputs", font_size=30, color=GREEN_C).next_to(ends, DOWN, buff=0.1).set_x(0)
        self.play(FadeIn(done), run_time=0.4)
        self.wait(2.0)
        snaps.append(Image.fromarray(self.renderer.get_frame()))
        self.snaps = snaps


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "frame_rate": 15, "background_color": WHITE, "media_dir": str(media),
                     "output_file": "flatten", "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = Flatten()
        scene.render()
    mp4 = HERE / "flatten.mp4"
    shutil.copy(next(media.rglob("flatten.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse", str(HERE / "flatten.gif")], check=True)
    w, h = scene.snaps[0].size
    sheet = Image.new("RGB", (w, 3 * h + 32), "white")
    for i, f in enumerate(scene.snaps):
        sheet.paste(f.convert("RGB"), (0, i * (h + 16)))
    sheet.save(HERE / "flatten_frames.png")
    shutil.rmtree(media)
