"""Duality. A linear map to the number line is defined only by where i-hat (1) and j-hat (-2) land: every grid point
x lands on x1 - 2 x2, and [4, 3] lands on -2. Tipping the 1 x 2 matrix [1 -2] upright gives the vector v = [1, -2],
and projecting [4, 3] onto v's line, times the length of v, gives the same -2: the map is the dot product with v.
Run: python duality.py  -> duality.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C, PURPLE_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B", "#B279A2"
Text.set_default(color=BLACK, font="Latin Modern Roman")
L = np.array([1.0, -2.0])                                  # where i-hat and j-hat land
X = np.array([4.0, 3.0])
O = np.array([-4.4, 0.55, 0])                               # screen origin of the plane
K = 0.75                                                   # screen units per unit
P = lambda xy: O + K * np.array([xy[0], xy[1], 0.0])
LINE_Y = -2.6


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def arrow(a, b, colour, width=6):
    return Arrow(a, b, buff=0, color=colour, stroke_width=width, max_tip_length_to_length_ratio=0.2)


class Duality(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        plane = NumberPlane(x_range=[-3.5, 4.5], y_range=[-2.5, 3.5], background_line_style={"stroke_color": "#DDDDDD"},
                            axis_config={"stroke_color": "#AAAAAA"}).scale(K)
        plane.shift(O - plane.c2p(0, 0))
        nl = NumberLine(x_range=[-9, 8, 1], unit_size=K, color=GREY_C, include_numbers=True, font_size=30,
                        numbers_to_include=range(-8, 9, 2), decimal_number_config={"color": BLACK, "num_decimal_places": 0})
        nl.shift([0, LINE_Y, 0] - nl.n2p(0))
        pts = [(x, y) for x in range(-3, 5) for y in range(-2, 4)]
        dots = VGroup(*[Dot(P(p), radius=0.085 if p == (4, 3) else 0.07, color=ORANGE_C if p == (4, 3) else BLUE_C) for p in pts])
        i_hat, j_hat = arrow(P([0, 0]), P([1, 0]), GREEN_C), arrow(P([0, 0]), P([0, 1]), RED_C)
        rule = boxed(VGroup(MathTex(r"\hat\imath \to 1,\quad \hat\jmath \to -2", color=BLACK, font_size=40),
                            MathTex(r"\text{matrix } \begin{bmatrix} 1 & -2 \end{bmatrix}", color=BLACK, font_size=40))
                     .arrange(DOWN, buff=0.15), 0.12).move_to([3.7, 2.9, 0])
        self.add(plane, nl, dots, i_hat, j_hat, rule)
        self.wait(0.8)
        self.snap()
        # 1. squish every grid point onto the number line: x lands on x1 - 2 x2
        copies = dots.copy()
        self.play(*[c.animate.move_to(nl.n2p(float(L @ p))) for c, p in zip(copies, pts)],
                  i_hat.copy().animate.put_start_and_end_on(nl.n2p(0), nl.n2p(1)),
                  j_hat.copy().animate.put_start_and_end_on(nl.n2p(0), nl.n2p(-2)), run_time=2.5)
        res = boxed(MathTex(r"[4, 3] \to 4(1) + 3(-2) = -2", color=ORANGE_C, font_size=40), 0.1)
        res.move_to([3.7, 1.75, 0])
        mark = arrow(nl.n2p(-2) + DOWN * 0.9, nl.n2p(-2) + DOWN * 0.25, ORANGE_C, 5)
        self.play(FadeIn(res), GrowArrow(mark))
        self.wait(1)
        self.snap()
        # 2. tip the matrix upright: the vector v = [1, -2], and project [4, 3] onto its line
        v_line = DashedLine(P(-1.3 * L), P(1.2 * L), color=PURPLE_C, stroke_width=3)
        v = arrow(P([0, 0]), P(L), PURPLE_C, 8)
        v_lab = boxed(MathTex(r"\mathbf v = [1, -2]", color=PURPLE_C, font_size=40), 0.06).next_to(P(L), RIGHT, 0.15)
        shadow_pt = (X @ L) / (L @ L) * L                                # [-0.4, 0.8]
        drop = DashedLine(P(X), P(shadow_pt), color=ORANGE_C, stroke_width=4)
        shadow = Line(P([0, 0]), P(shadow_pt), color=ORANGE_C, stroke_width=10)
        self.play(GrowArrow(v), Create(v_line), FadeIn(v_lab))
        self.play(Create(drop), run_time=1)
        self.play(Create(shadow))
        proj = boxed(VGroup(Text("shadow on v's line: -0.894", font_size=30, weight=BOLD, color=ORANGE_C),
                            Text("times length of v, 2.236:  -2", font_size=30, weight=BOLD, color=ORANGE_C))
                     .arrange(DOWN, buff=0.1), 0.12).move_to([3.7, 0.7, 0])
        self.play(FadeIn(proj))
        self.wait(1)
        self.snap()
        cap = boxed(VGroup(Text("the map is the dot product", font_size=30, weight=BOLD, color=PURPLE_C),
                           MathTex(r"\text{with } \mathbf v:\quad \mathbf x \mapsto \mathbf v \cdot \mathbf x", color=PURPLE_C,
                                   font_size=42)).arrange(DOWN, buff=0.12), 0.12).move_to([3.7, -0.65, 0])
        self.play(FadeIn(cap))
        self.wait(2)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert L @ X == -2
    shadow_len = (X @ L) / np.linalg.norm(L)
    assert np.isclose(shadow_len, -0.894, atol=1e-3) and np.isclose(shadow_len * np.linalg.norm(L), -2)
    name = "duality"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = Duality()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48:stats_mode=diff[p];[b][p]paletteuse=dither=none:diff_mode=rectangle",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
