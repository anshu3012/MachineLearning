"""The eigenbasis: draw the grid along the eigenvectors e1 = (1, 0) (eigenvalue 3) and e2 = (-1, 1) (eigenvalue 2)
of A = [[3, 1], [0, 2]]. Applying A only stretches that grid along its own lines, so in eigen-coordinates A is
D = diag(3, 2): v = 1 e1 + 1 e2 = (0, 1) lands on 3 e1 + 2 e2 = (1, 2), and applying A again gives 9 e1 + 4 e2.
Intuition after Sanderson (3Blue1Brown), "Eigenvectors and eigenvalues"; our own code and matrix.
Run: python eigenbasis_grid.py  -> eigenbasis_grid.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C, PURPLE_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B", "#9D5BA8"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)
A = np.array([[3.0, 1.0], [0.0, 2.0]])
E1, E2 = np.array([1.0, 0.0]), np.array([-1.0, 1.0])
SHIFT = np.array([-2.0, -2.2, 0])                      # origin of the plane on screen


def boxed(mob, buff=0.12):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def P(xy):
    return np.array([xy[0], xy[1], 0]) + SHIFT


def arrow(a, b, colour, width=7):
    return Arrow(P(a), P(b), buff=0, color=colour, stroke_width=width, max_tip_length_to_length_ratio=0.18)


def eigen_grid():
    """Lines parallel to e1 (green) through multiples of e2, and lines parallel to e2 (purple) through multiples of e1."""
    g = VGroup()
    for k in range(-8, 9):
        g.add(Line(P(k * E2 - 30 * E1), P(k * E2 + 30 * E1), color=GREEN_C, stroke_width=2, stroke_opacity=0.6))
    for m in range(-14, 15):
        g.add(Line(P(m * E1 - 30 * E2), P(m * E1 + 30 * E2), color=PURPLE_C, stroke_width=2, stroke_opacity=0.6))
    return g


def path(c1, c2):
    """Arrow of c1 e1 then c2 e2, plus the total vector."""
    a = c1 * E1
    return VGroup(arrow([0, 0], a, GREEN_C, 6), arrow(a, a + c2 * E2, PURPLE_C, 6), arrow([0, 0], a + c2 * E2, ORANGE_C, 8))


class EigenbasisGrid(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, text):
        return boxed(Text(text, font_size=34, weight=BOLD)).to_edge(UP, buff=0.3)

    def construct(self):
        self.snaps = []
        ghost = NumberPlane(x_range=[-12, 12], y_range=[-8, 8], background_line_style={"stroke_color": "#E3E3E3"},
                            axis_config={"stroke_color": "#BBBBBB"}).shift(SHIFT)
        grid = eigen_grid()
        self.add(ghost)
        cap = self.caption("A grid drawn along the eigenvectors")
        self.play(Create(grid), FadeIn(cap), run_time=2)
        v = path(1, 1)
        coords = boxed(MathTex(r"\mathbf{v} = 1\,\mathbf{e}_1 + 1\,\mathbf{e}_2", font_size=48)).to_corner(DR, buff=0.4)
        names = VGroup(boxed(MathTex(r"\mathbf{e}_1", font_size=44, color=GREEN_C), 0.05).move_to(P([0.55, -0.45])),
                       boxed(MathTex(r"\mathbf{e}_2", font_size=44, color=PURPLE_C), 0.05).move_to(P([0.95, 0.75])))
        self.play(LaggedStart(*[GrowArrow(a) for a in v], lag_ratio=0.5), FadeIn(coords), FadeIn(names))
        self.wait(1)
        self.snap()

        cap2 = self.caption("Apply A: each grid line only stretches along itself")
        v2 = path(3, 2)
        coords2 = boxed(MathTex(r"A\mathbf{v} = 3\,\mathbf{e}_1 + 2\,\mathbf{e}_2", font_size=48)).to_corner(DR, buff=0.4)
        self.play(FadeOut(names), run_time=0.4)
        self.play(ApplyMatrix(A, grid, about_point=SHIFT), Transform(v, v2), FadeTransform(cap, cap2),
                  FadeTransform(coords, coords2), run_time=3)
        self.bring_to_front(cap2, coords2)
        tags = VGroup(boxed(MathTex(r"\times 3", font_size=50, color=GREEN_C)).move_to(P([2.0, -0.6])),
                      boxed(MathTex(r"\times 2", font_size=50, color=PURPLE_C)).move_to(P([-2.6, 2.0])))
        self.play(FadeIn(tags))
        self.wait(1)
        self.snap()

        D = boxed(MathTex(r"D = \begin{bmatrix} 3 & 0 \\ 0 & 2 \end{bmatrix}:\ "
                          r"\begin{bmatrix} 1 \\ 1 \end{bmatrix} \to \begin{bmatrix} 3 \\ 2 \end{bmatrix}",
                          font_size=46)).to_corner(UL, buff=0.3).shift(DOWN * 1.0)
        cap3 = self.caption("In eigen-coordinates, A is a diagonal matrix")
        self.play(FadeOut(tags), FadeIn(D), FadeTransform(cap2, cap3))
        self.wait(1.2)
        self.snap()

        cap4 = self.caption("Apply A again: 3 and 2 multiply again")
        v3 = path(9, 4)
        coords3 = boxed(MathTex(r"A^2\mathbf{v} = 9\,\mathbf{e}_1 + 4\,\mathbf{e}_2", font_size=48)).to_corner(DR, buff=0.4)
        D2 = boxed(MathTex(r"D^2 = \begin{bmatrix} 3^2 & 0 \\ 0 & 2^2 \end{bmatrix}", font_size=46)).move_to(D)
        self.play(ApplyMatrix(A, grid, about_point=SHIFT), Transform(v, v3), FadeTransform(cap3, cap4),
                  FadeTransform(coords2, coords3), FadeTransform(D, D2), run_time=3)
        self.bring_to_front(cap4, coords3, D2)
        self.wait(2)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert np.allclose(A @ E1, 3 * E1) and np.allclose(A @ E2, 2 * E2)
    v = E1 + E2
    assert np.allclose(A @ v, 3 * E1 + 2 * E2) and np.allclose(A @ A @ v, 9 * E1 + 4 * E2)
    name = "eigenbasis_grid"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = EigenbasisGrid()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48:stats_mode=diff[p];"
                    "[b][p]paletteuse=dither=none:diff_mode=rectangle", str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
