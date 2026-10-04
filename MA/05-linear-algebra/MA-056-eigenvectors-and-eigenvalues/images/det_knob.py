"""Finding eigenvalues: turn a knob lambda and watch A - lambda I act on the unit square.
For A = [[3, 1], [0, 2]], det(A - lambda I) = (3 - lambda)(2 - lambda): the square's area hits 0 (it is squished
flat onto a line) exactly at lambda = 2 and lambda = 3, the eigenvalues.
Run: python det_knob.py  -> det_knob.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
A = np.array([[3.0, 1.0], [0.0, 2.0]])
K = 0.85                                        # screen units per grid unit on the left
ORIGIN_L = np.array([-4.6, -1.2, 0])            # origin of the left plane


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def det(lam):
    return (3 - lam) * (2 - lam)


class DetKnob(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        lam = ValueTracker(0.0)
        grid = NumberPlane(x_range=[-2, 4], y_range=[-2, 3], background_line_style={"stroke_color": "#E3E3E3"},
                           axis_config={"stroke_color": "#BBBBBB"}).scale(K)
        grid.shift(ORIGIN_L - grid.c2p(0, 0))
        to_screen = lambda xy: grid.c2p(xy[0], xy[1])

        def shape():
            M = A - lam.get_value() * np.eye(2)
            c1, c2 = M[:, 0], M[:, 1]
            pts = [to_screen(p) for p in ([0, 0], c1, c1 + c2, c2)]
            flat = abs(det(lam.get_value())) < 0.04
            poly = Polygon(*pts, color=RED_C if flat else BLUE_C, fill_opacity=0.35, stroke_width=4)
            a1 = Arrow(to_screen([0, 0]), to_screen(c1), buff=0, color=GREEN_C, stroke_width=7,
                       max_tip_length_to_length_ratio=0.25)
            a2 = Arrow(to_screen([0, 0]), to_screen(c2), buff=0, color=RED_C, stroke_width=7,
                       max_tip_length_to_length_ratio=0.25)
            return VGroup(poly, a1, a2)

        sq = always_redraw(shape)
        head = boxed(MathTex(r"A - \lambda I = \begin{bmatrix} 3-\lambda & 1 \\ 0 & 2-\lambda \end{bmatrix}",
                             color=BLACK, font_size=40), 0.12).move_to([-3.6, 3.2, 0])
        axes = Axes(x_range=[0, 4.5, 1], y_range=[-1, 6, 1], x_length=5.2, y_length=4.4, tips=False,
                    axis_config={"color": GREY_C, "include_numbers": True, "font_size": 26,
                                 "decimal_number_config": {"color": BLACK, "num_decimal_places": 0}}).move_to([3.4, -0.3, 0])
        curve = axes.plot(det, x_range=[0, 4.3], color=BLUE_C, stroke_width=5)
        xl = MathTex(r"\lambda", color=BLACK, font_size=36).next_to(axes.x_axis, RIGHT, buff=0.15)
        yl = MathTex(r"\det(A - \lambda I) = (3-\lambda)(2-\lambda)", color=BLACK, font_size=32)
        yl.next_to(axes, UP, buff=0.25)
        dot = always_redraw(lambda: Dot(axes.c2p(lam.get_value(), det(lam.get_value())), color=ORANGE_C, radius=0.11))
        readout = always_redraw(lambda: boxed(MathTex(
            rf"\lambda = {lam.get_value():.2f}\quad \det = {(det(lam.get_value()) if abs(det(lam.get_value())) > 0.005 else 0.0):.2f}",
            color=BLACK, font_size=36), 0.1).move_to([-3.6, -3.4, 0]))
        self.add(grid, sq, head, axes, curve, xl, yl, dot, readout)
        self.wait(0.6)
        self.snap()
        self.play(lam.animate.set_value(1.0), run_time=2)
        self.wait(0.4)
        self.snap()
        self.play(lam.animate.set_value(2.0), run_time=2)
        flat2 = boxed(Tex(r"squished flat: $\lambda = 2$ is an eigenvalue", font_size=36, color=RED_C), 0.1)
        flat2.move_to([-3.6, 2.2, 0])
        roots = VGroup(*[Dot(axes.c2p(r, 0), color=RED_C, radius=0.12) for r in (2, 3)])
        self.play(FadeIn(flat2), FadeIn(roots[0]))
        self.wait(0.8)
        self.snap()
        self.play(FadeOut(flat2))
        self.play(lam.animate.set_value(2.5), run_time=1)
        self.play(lam.animate.set_value(3.0), run_time=1)
        flat3 = boxed(Tex(r"flat again: $\lambda = 3$ is an eigenvalue", font_size=36, color=RED_C), 0.1).move_to([-3.6, 2.2, 0])
        self.play(FadeIn(flat3), FadeIn(roots[1]))
        self.wait(1.2)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert sorted(np.linalg.eigvals(A).real) == [2.0, 3.0]
    name = "det_knob"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = DetKnob()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
