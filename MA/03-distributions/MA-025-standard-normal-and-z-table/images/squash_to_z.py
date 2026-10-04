"""Standardizing as motion (Figure 1's example): X ~ N(5, 2.5^2) with the area right of x = 10 shaded.
Subtracting the mean slides the curve left by 5; dividing by 2.5 squeezes it 2.5 times narrower and, to keep the
total area 1, 2.5 times taller. The cut-off rides along to z = 2, and the shaded area stays 0.0228 throughout.
Run: python squash_to_z.py -> squash_to_z.mp4, squash_to_z.gif, squash_to_z_frames.png (Manim + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREY_C = "#4C78A8", "#F58518", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)
MU, SD, CUT = 5.0, 2.5, 10.0
TAIL = stats.norm.sf(CUT, MU, SD)
assert abs(TAIL - stats.norm.sf(2)) < 1e-12 and round(TAIL, 4) == 0.0228


class SquashToZ(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[-8, 14, 1], y_range=[0, 0.45, 0.1], x_length=13, y_length=4.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 32,
                               "decimal_number_config": {"color": BLACK, "num_decimal_places": 0}},
                  x_axis_config={"numbers_to_include": range(-8, 15, 2)},
                  y_axis_config={"numbers_to_include": [0.1, 0.2, 0.3, 0.4],
                                 "decimal_number_config": {"color": BLACK, "num_decimal_places": 1}}
                  ).shift(DOWN * 0.9)
        m, s = ValueTracker(MU), ValueTracker(SD)
        curve = always_redraw(lambda: ax.plot(lambda x: stats.norm.pdf(x, m.get_value(), s.get_value()),
                                              x_range=[-8, 14, 0.02], color=ORANGE_C, stroke_width=5))
        area = always_redraw(lambda: ax.get_area(
            ax.plot(lambda x: stats.norm.pdf(x, m.get_value(), s.get_value()), x_range=[-8, 14, 0.02]),
            x_range=[m.get_value() + 2 * s.get_value(), 14], color=BLUE_C, opacity=0.85))
        cut = always_redraw(lambda: ax.get_vertical_line(ax.c2p(m.get_value() + 2 * s.get_value(), 0.3),
                                                         color=BLUE_C, stroke_width=4))
        cut_lab = always_redraw(lambda: DecimalNumber(m.get_value() + 2 * s.get_value(), num_decimal_places=1,
                                                      color=BLUE_C, font_size=36).next_to(cut, UP, buff=0.1))
        title = Text("X ~ N(5, 2.5²): the shaded area is P(X > 10)", font_size=32).to_edge(UP, buff=0.3)
        tail_lab = MathTex(r"P(X > 10) = 0.0228", font_size=44, color=BLUE_C).to_corner(UR, buff=0.4).shift(DOWN * 0.8)
        self.play(Create(ax), FadeIn(title), run_time=1)
        self.play(Create(curve), run_time=1)
        self.play(FadeIn(area), Create(cut), FadeIn(cut_lab), FadeIn(tail_lab))
        self.wait(0.8)
        self.snap()

        step1 = Text("Step 1: subtract the mean, x − 5", font_size=32).to_edge(UP, buff=0.3)
        self.play(Transform(title, step1))
        self.play(m.animate.set_value(0), run_time=2.5, rate_func=smooth)
        self.wait(0.6)
        self.snap()

        step2 = Text("Step 2: divide by the standard deviation 2.5: narrower, taller", font_size=32).to_edge(UP, buff=0.3)
        self.play(Transform(title, step2))
        self.play(s.animate.set_value(1.6), run_time=1.8, rate_func=smooth)
        self.snap()
        self.play(s.animate.set_value(1), run_time=1.6, rate_func=smooth)
        self.wait(0.6)

        final = Text("Z ~ N(0, 1): the cut-off is now z = (10 − 5) / 2.5 = 2", font_size=32).to_edge(UP, buff=0.3)
        z_lab = MathTex(r"P(Z > 2) = 0.0228", font_size=44, color=BLUE_C).next_to(tail_lab, DOWN, buff=0.3)
        same = Text("same area", font_size=30, color=BLUE_C).next_to(z_lab, DOWN, buff=0.25)
        self.play(Transform(title, final), FadeIn(z_lab), FadeIn(same))
        self.wait(3)
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
                     "output_file": "squash_to_z", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = SquashToZ()
        scene.render()
    mp4 = HERE / "squash_to_z.mp4"
    shutil.copy(next(media.rglob("squash_to_z.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "squash_to_z.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "squash_to_z_frames.png")
    shutil.rmtree(media)
