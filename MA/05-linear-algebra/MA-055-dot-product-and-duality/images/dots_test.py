"""The visual test for a linear map from the plane to the number line. Six evenly spaced dots on the line y = 0.5
(x = 0, 0.4, ..., 2) are sent to numbers two ways. Linear map x - 2y (i-hat -> 1, j-hat -> -2): they land
-1, -0.6, ..., 1, evenly spaced. Non-linear map 2^x - 2y: they land 0, 0.32, 0.74, 1.30, 2.03, 3, gaps growing.
Run: python dots_test.py  -> dots_test.mp4, .gif, _frames.png (Manim)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
XS = np.arange(6) * 0.4
Y = 0.5
LIN = XS - 2 * Y
NON = 2 ** XS - 2 * Y


def boxed(mob, buff=0.1):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class DotsTest(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        plane = NumberPlane(x_range=[-1, 3], y_range=[-0.5, 1.5], x_length=4.8, y_length=2.4,
                            background_line_style={"stroke_color": "#E3E3E3"}, axis_config={"stroke_color": "#BBBBBB"})
        plane.move_to([-3.6, 2.2, 0])
        ptitle = boxed(Text("evenly spaced dots in the plane", font_size=30)).next_to(plane, RIGHT, buff=0.4)
        dots = VGroup(*[Dot(plane.c2p(x, Y), radius=0.09, color=BLUE_C) for x in XS])
        kw = dict(x_range=[-1.5, 3.5, 0.5], length=11, include_numbers=True, color=GREY_C,
                  numbers_to_include=[-1, 0, 1, 2, 3], font_size=30, decimal_number_config={"color": GREY_C, "num_decimal_places": 0})
        nl1 = NumberLine(**kw).move_to([0.3, -0.4, 0])
        nl2 = NumberLine(**kw).move_to([0.3, -2.5, 0])
        l1 = boxed(MathTex(r"x - 2y \ \ (\hat{\imath} \to 1, \ \hat{\jmath} \to -2)", color=GREEN_C, font_size=34)).next_to(nl1, UP, buff=0.25).align_to(nl1, LEFT)
        l2 = boxed(MathTex(r"2^x - 2y", color=RED_C, font_size=34)).next_to(nl2, UP, buff=0.25).align_to(nl2, LEFT)
        self.add(plane, dots, ptitle, nl1, nl2, l1, l2)
        self.wait(0.8)
        self.snap()
        d1 = dots.copy()
        self.play(*[d.animate.move_to(nl1.n2p(v)).set_color(GREEN_C) for d, v in zip(d1, LIN)], run_time=2)
        ok = boxed(Text("still evenly spaced: linear", font_size=30, color=GREEN_C)).next_to(nl1, UP, buff=0.25).align_to(nl1, RIGHT)
        self.play(FadeIn(ok))
        self.wait(1)
        self.snap()
        d2 = dots.copy()
        self.play(*[d.animate.move_to(nl2.n2p(v)).set_color(RED_C) for d, v in zip(d2, NON)], run_time=2)
        bad = boxed(Text("gaps grow: not linear", font_size=30, color=RED_C)).next_to(nl2, UP, buff=0.25).align_to(nl2, RIGHT)
        self.play(FadeIn(bad))
        self.wait(1)
        self.snap()
        gaps = VGroup(*[Brace(Line(nl2.n2p(a), nl2.n2p(b)), DOWN, buff=0.05, color=RED_C) for a, b in zip(NON[:-1], NON[1:])])
        self.play(FadeIn(gaps))
        self.wait(2)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert np.allclose(np.diff(LIN), 0.4) and np.all(np.diff(np.diff(NON)) > 0)
    name = "dots_test"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = DotsTest()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
