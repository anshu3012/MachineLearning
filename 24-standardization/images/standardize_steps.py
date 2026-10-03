"""Standardization as two moves on a cloud of points: shift the mean to 0, then squeeze/stretch each axis to std 1.
Run: python standardize_steps.py  -> standardize_steps.mp4, standardize_steps.gif, standardize_steps_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")

# made-up cloud: feature 1 spread out (std 2: will be squeezed), feature 2 narrow (std 0.6: will be stretched)
rng = np.random.default_rng(3)
RAW = rng.normal(size=(60, 2))
RAW = (RAW - RAW.mean(0)) / RAW.std(0)          # exact mean 0, std 1 ...
RAW = RAW * [2.0, 0.6] + [4.5, 3.0]               # ... then mean (4.5, 3), std (2, 0.6)
MEAN, STD = RAW.mean(0), RAW.std(0)


class StandardizeSteps(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, title, sub):
        return VGroup(Text(title, font_size=32, weight=BOLD), Text(sub, font_size=24, color=GREY_C)
                      ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)

    def state(self, pts, mean, std):
        """Dots, a red cross at the mean, and a dashed box one std either side of the mean."""
        ax = self.ax
        dots = VGroup(*[Dot(ax.c2p(*p), radius=0.06, color=BLUE_C) for p in pts])
        m = ax.c2p(*mean)
        cross = VGroup(Line(m + 0.18 * UL, m + 0.18 * DR), Line(m + 0.18 * DL, m + 0.18 * UR)).set_stroke(RED_C, 5)
        box = DashedVMobject(Rectangle(width=2 * std[0] * self.unit, height=2 * std[1] * self.unit,
                                       stroke_color=ORANGE_C, stroke_width=3).move_to(m), num_dashes=40)
        return VGroup(dots, box, cross)

    def construct(self):
        self.snaps = []
        self.ax = Axes(x_range=[-6, 9, 1], y_range=[-3, 5, 1], x_length=15 * 0.6, y_length=8 * 0.6,
                       axis_config={"color": GREY_C, "include_numbers": True, "font_size": 22,
                                    "decimal_number_config": {"num_decimal_places": 0, "color": BLACK}},
                       tips=False).shift(UP * 0.7)
        self.unit = 0.6
        labels = VGroup(Text("feature 1", font_size=22).next_to(self.ax.x_axis, RIGHT, buff=0.15),
                        Text("feature 2", font_size=22).next_to(self.ax.y_axis, UP, buff=0.1))
        self.add(self.ax, labels)

        # Step 0: raw data
        cur = self.state(RAW, MEAN, STD)
        cap = self.caption("Raw data", "mean (4.5, 3)   std (2, 0.6)   red cross = mean, box = 1 std either side")
        self.play(FadeIn(cur, lag_ratio=0.01), FadeIn(cap))
        self.wait(0.6)
        self.snap()

        # Step 1: subtract the mean: the whole cloud slides to the origin, its shape unchanged
        centred = RAW - MEAN
        nxt = self.state(centred, [0, 0], STD)
        self.play(Transform(cur, nxt), Transform(cap, self.caption("1. Subtract the mean", "mean centring: mean becomes (0, 0), shape unchanged")),
                  run_time=1.6)
        self.wait(0.6)
        self.snap()

        # Step 2a: divide feature 1 by its std 2: squeezed
        half = centred / [STD[0], 1]
        nxt = self.state(half, [0, 0], [1, STD[1]])
        self.play(Transform(cur, nxt), Transform(cap, self.caption("2. Divide feature 1 by its std (2)", "std above 1: points squeeze in")),
                  run_time=1.6)
        self.wait(0.6)
        self.snap()

        # Step 2b: divide feature 2 by its std 0.6: stretched
        nxt = self.state(centred / STD, [0, 0], [1, 1])
        self.play(Transform(cur, nxt), Transform(cap, self.caption("3. Divide feature 2 by its std (0.6)", "std below 1: points spread out; now mean 0, std 1 on both axes")),
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
                     "output_file": "standardize_steps", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = StandardizeSteps()
        scene.render()
    mp4 = HERE / "standardize_steps.mp4"
    shutil.copy(next(media.rglob("standardize_steps.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "standardize_steps.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "standardize_steps_frames.png")
    shutil.rmtree(media)
