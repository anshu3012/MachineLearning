"""A linear transformation moves the whole grid; it is fixed by where i-hat and j-hat land.
Matrix [[1, 3], [-2, 0]]: i-hat -> (1, -2), j-hat -> (3, 0), so v = (-1, 2) = -1 i-hat + 2 j-hat -> (5, 2).
Run: python basis_landing.py  -> basis_landing.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
A = [[1, 3], [-2, 0]]


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def vec(xy, colour):
    return Arrow(ORIGIN, [*xy, 0], buff=0, color=colour, stroke_width=8, max_tip_length_to_length_ratio=0.2)


class BasisLanding(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def tex(self, s, colour, pos, size=40):
        return boxed(MathTex(s, color=colour, font_size=size).move_to(pos))

    def construct(self):
        self.snaps = []
        ghost = NumberPlane(x_range=[-8, 8], y_range=[-5, 5], background_line_style={"stroke_color": "#E3E3E3"},
                            axis_config={"stroke_color": "#BBBBBB"})
        plane = NumberPlane(x_range=[-12, 12], y_range=[-12, 12], faded_line_ratio=0,
                            background_line_style={"stroke_color": BLUE_C, "stroke_opacity": 0.35},
                            axis_config={"stroke_color": BLUE_C})
        i_hat, j_hat, v = vec([1, 0], GREEN_C), vec([0, 1], RED_C), vec([-1, 2], ORANGE_C)
        self.add(ghost, plane, i_hat, j_hat, v)
        before = VGroup(self.tex(r"\hat{\imath}", GREEN_C, [0.6, -0.4, 0]), self.tex(r"\hat{\jmath}", RED_C, [0.4, 1.05, 0]),
                        self.tex(r"\mathbf{v} = -1\,\hat{\imath} + 2\,\hat{\jmath}", ORANGE_C, [-2.6, 2.4, 0]))
        self.play(FadeIn(before))
        self.wait(0.8)
        self.snap()
        self.play(FadeOut(before))
        self.play(ApplyMatrix(A, plane), Transform(i_hat, vec([1, -2], GREEN_C)), Transform(j_hat, vec([3, 0], RED_C)),
                  Transform(v, vec([5, 2], ORANGE_C)), run_time=3)
        landed = VGroup(self.tex(r"\hat{\imath} \to [1, -2]", GREEN_C, [2.2, -2.2, 0]),
                        self.tex(r"\hat{\jmath} \to [3, 0]", RED_C, [3.3, -0.55, 0]))
        self.play(FadeIn(landed))
        self.wait(0.8)
        self.snap()
        rule = self.tex(r"\mathbf{v} \to -1\,[1, -2] + 2\,[3, 0] = [5, 2]", ORANGE_C, [-3.0, 3.3, 0], 42)
        self.play(FadeIn(rule))
        self.wait(1)
        self.snap()
        m = Matrix([[1, 3], [-2, 0]], element_to_mobject_config={"color": BLACK}, bracket_config={"color": BLACK}, h_buff=0.9).scale(0.8)
        m.get_columns()[0].set_color(GREEN_C)
        m.get_columns()[1].set_color(RED_C)
        eq = boxed(VGroup(m, MathTex(r"\begin{bmatrix} -1 \\ 2 \end{bmatrix} = \begin{bmatrix} 5 \\ 2 \end{bmatrix}",
                                     color=BLACK, font_size=40)).arrange(RIGHT, buff=0.15), 0.15)
        eq.to_corner(DL, buff=0.4)
        self.play(FadeIn(eq))
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert np.allclose(np.array(A) @ [-1, 2], [5, 2])
    name = "basis_landing"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = BasisLanding()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
