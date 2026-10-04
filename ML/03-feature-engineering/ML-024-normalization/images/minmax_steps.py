"""Min-max scaling as two moves on a cloud of points: slide the min corner to the origin, then squeeze/stretch
each axis so the cloud fits the unit square exactly.
Run: python minmax_steps.py  -> minmax_steps.mp4, minmax_steps.gif, minmax_steps_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")

# made-up cloud: feature 1 from 2 to 7 (range 5: squeezed), feature 2 from 2.5 to 3.1 (range 0.6: stretched)
rng = np.random.default_rng(3)
RAW = rng.normal(size=(60, 2))
RAW = (RAW - RAW.min(0)) / (RAW.max(0) - RAW.min(0))   # exactly 0..1 on each axis ...
RAW = RAW * [5.0, 0.6] + [2.0, 2.5]                     # ... then min (2, 2.5), max (7, 3.1)
MIN, RANGE = RAW.min(0), RAW.max(0) - RAW.min(0)


class MinMaxSteps(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, title, sub):
        return VGroup(Text(title, font_size=32, weight=BOLD), Text(sub, font_size=24, color=GREY_C)
                      ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)

    def state(self, pts, lo, size):
        """Dots, a red dot at the min corner, and a dashed box from the min corner to the max corner."""
        ax = self.ax
        dots = VGroup(*[Dot(ax.c2p(*p), radius=0.06, color=BLUE_C) for p in pts])
        corner = Dot(ax.c2p(*lo), radius=0.11, color=RED_C)
        box = DashedVMobject(Rectangle(width=size[0] * self.unit, height=size[1] * self.unit,
                                       stroke_color=ORANGE_C, stroke_width=3), num_dashes=40)
        box.move_to(ax.c2p(lo[0] + size[0] / 2, lo[1] + size[1] / 2))
        return VGroup(dots, box, corner)

    def construct(self):
        self.snaps = []
        self.unit = 1.1
        self.ax = Axes(x_range=[-1, 8, 1], y_range=[-1, 4, 1], x_length=9 * self.unit, y_length=5 * self.unit,
                       axis_config={"color": GREY_C, "include_numbers": True, "font_size": 22,
                                    "decimal_number_config": {"num_decimal_places": 0, "color": BLACK}},
                       tips=False).shift(UP * 0.8)
        labels = VGroup(Text("feature 1", font_size=22).next_to(self.ax.x_axis, RIGHT, buff=0.15),
                        Text("feature 2", font_size=22).next_to(self.ax.y_axis, UP, buff=0.1))
        # the target: the unit square from (0, 0) to (1, 1)
        square = Polygon(*[self.ax.c2p(*p) for p in [(0, 0), (1, 0), (1, 1), (0, 1)]],
                         stroke_width=0, fill_color=GREEN_C, fill_opacity=0.3)
        self.add(square, self.ax, labels)

        # Step 0: raw data
        cur = self.state(RAW, MIN, RANGE)
        cap = self.caption("Raw data", "min (2, 2.5)   max (7, 3.1)   red dot = min corner, green = unit square")
        self.play(FadeIn(cur, lag_ratio=0.01), FadeIn(cap))
        self.wait(0.6)
        self.snap()

        # Step 1: subtract the min: the cloud slides until its min corner sits at the origin, shape unchanged
        shifted = RAW - MIN
        self.play(Transform(cur, self.state(shifted, [0, 0], RANGE)),
                  Transform(cap, self.caption("1. Subtract the min", "min corner moves to (0, 0), shape unchanged")),
                  run_time=1.6)
        self.wait(0.6)
        self.snap()

        # Step 2a: divide feature 1 by its range 5: squeezed to width 1
        self.play(Transform(cur, self.state(shifted / [RANGE[0], 1], [0, 0], [1, RANGE[1]])),
                  Transform(cap, self.caption("2. Divide feature 1 by its range (5)", "range above 1: points squeeze in")),
                  run_time=1.6)
        self.wait(0.6)
        self.snap()

        # Step 2b: divide feature 2 by its range 0.6: stretched to height 1; the cloud now fills the unit square
        self.play(Transform(cur, self.state(shifted / RANGE, [0, 0], [1, 1])),
                  Transform(cap, self.caption("3. Divide feature 2 by its range (0.6)",
                                              "range below 1: points spread out; now every value is in 0 to 1")),
                  run_time=1.6)
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "minmax_steps", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = MinMaxSteps()
        scene.render()
    mp4 = HERE / "minmax_steps.mp4"
    shutil.copy(next(media.rglob("minmax_steps.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "minmax_steps.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "minmax_steps_frames.png")
    shutil.rmtree(media)
