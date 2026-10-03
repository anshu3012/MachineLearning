"""Projecting the plane onto a tilted copy of the number line is linear: evenly spaced dots land evenly spaced.
i-hat lands on u_x = 0.6 and j-hat on u_y = 0.8, so the 1 x 2 matrix of the projection is [0.6 0.8]:
projecting = taking the dot product with u = [0.6, 0.8].
Run: python projection_line.py  -> projection_line.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
U = np.array([0.6, 0.8])
K = 1.6                                                   # screen units per data unit
P = lambda xy: np.array([K * xy[0], K * xy[1], 0.0])     # data point -> screen point


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class ProjectionLine(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        self.add(NumberPlane(x_range=[-5, 5], y_range=[-3, 3], background_line_style={"stroke_color": "#E3E3E3"},
                             axis_config={"stroke_color": "#BBBBBB"}).scale(K))
        line = Line(P(-2.6 * U), P(2.6 * U), color=GREY_C, stroke_width=4)
        ticks = VGroup(*[VGroup(Line(P(t * U) + 0.12 * P([-U[1], U[0]]) / K, P(t * U) - 0.12 * P([-U[1], U[0]]) / K,
                                     color=GREY_C, stroke_width=3),
                                MathTex(str(t), color=GREY_C, font_size=30).move_to(P(t * U) + 0.38 * np.array([U[1], -U[0], 0])))
                         for t in range(-2, 3)])
        u_hat = Arrow(ORIGIN, P(U), buff=0, color=ORANGE_C, stroke_width=8, max_tip_length_to_length_ratio=0.25)
        u_lab = boxed(MathTex(r"\hat{u} = [0.6, 0.8]", color=ORANGE_C, font_size=38)).move_to([2.9, 1.5, 0])
        title = boxed(Text("Project every point onto a tilted number line", font_size=30, weight=BOLD), 0.12)
        title.to_edge(UP, buff=0.2)
        self.add(line, ticks, u_hat, u_lab, title)
        pts = [np.array([x, -1.5]) for x in np.arange(-2.0, 2.01, 0.8)]
        dots = VGroup(*[Dot(P(p), color=BLUE_C, radius=0.09) for p in pts])
        cap = boxed(Text("evenly spaced dots ...", font_size=28, color=BLUE_C), 0.1).move_to([3.4, -3.1, 0])
        self.play(FadeIn(dots), FadeIn(cap))
        self.wait(0.6)
        self.snap()
        proj = [float(U @ p) for p in pts]
        drops = VGroup(*[DashedLine(P(p), P(t * U), color=BLUE_C, stroke_width=2) for p, t in zip(pts, proj)])
        cap2 = boxed(Text("... land evenly spaced: the projection is linear", font_size=28, color=BLUE_C), 0.1)
        cap2.move_to([2.6, -3.1, 0])
        self.play(Create(drops), FadeTransform(cap, cap2))
        self.play(*[d.animate.move_to(P(t * U)) for d, t in zip(dots, proj)], run_time=2)
        self.wait(0.6)
        self.snap()
        self.play(FadeOut(drops), FadeOut(dots), FadeOut(cap2))
        i_hat = Arrow(ORIGIN, P([1, 0]), buff=0, color=GREEN_C, stroke_width=8, max_tip_length_to_length_ratio=0.25)
        j_hat = Arrow(ORIGIN, P([0, 1]), buff=0, color=RED_C, stroke_width=8, max_tip_length_to_length_ratio=0.25)
        i_drop = DashedLine(P([1, 0]), P(0.6 * U), color=GREEN_C, stroke_width=3)
        j_drop = DashedLine(P([0, 1]), P(0.8 * U), color=RED_C, stroke_width=3)
        i_dot, j_dot = Dot(P(0.6 * U), color=GREEN_C, radius=0.1), Dot(P(0.8 * U), color=RED_C, radius=0.1)
        labs = VGroup(boxed(MathTex(r"\hat{\imath} \to 0.6 = u_x", color=GREEN_C, font_size=38)).move_to([3.3, 0.2, 0]),
                      boxed(MathTex(r"\hat{\jmath} \to 0.8 = u_y", color=RED_C, font_size=38)).move_to([-2.0, 1.75, 0]))
        self.play(GrowArrow(i_hat), GrowArrow(j_hat))
        self.play(Create(i_drop), Create(j_drop), FadeIn(i_dot, j_dot), FadeIn(labs))
        self.wait(0.6)
        self.snap()
        eq = boxed(MathTex(r"\begin{bmatrix} 0.6 & 0.8 \end{bmatrix}\begin{bmatrix} x \\ y \end{bmatrix} = 0.6x + 0.8y = \hat{u}\cdot\mathbf{x}",
                           color=BLACK, font_size=40), 0.15).to_edge(DOWN, buff=0.3)
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
    name = "projection_line"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = ProjectionLine()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
