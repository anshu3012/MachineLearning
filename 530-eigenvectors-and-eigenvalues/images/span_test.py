"""Eigenvectors stay on their span. Eight vectors, each with its span drawn as a dashed line, go through
A = [[3, 1], [0, 2]] together with the grid. Six are knocked off their line (red); only the ones along
(1, 0) and (-1, 1) stay on it (green), stretched by 3 and by 2.
Intuition after Sanderson (3Blue1Brown), "Eigenvectors and eigenvalues"; our own code and matrix.
Run: python span_test.py  -> span_test.mp4, .gif, _frames.png"""
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
ANGLES = np.arange(8) * np.pi / 8                      # 0, 22.5, ..., 157.5 degrees
VECS = [1.4 * np.array([np.cos(a), np.sin(a)]) for a in ANGLES]


def on_span(v):
    w = A @ v
    return abs(v[0] * w[1] - v[1] * w[0]) < 1e-9       # 2D cross product 0: same line


def boxed(mob, buff=0.1):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def arrow(xy, colour):
    return Arrow(ORIGIN, [*xy, 0], buff=0, color=colour, stroke_width=7, max_tip_length_to_length_ratio=0.2)


def span_line(v, colour=GREY_C, width=2.5):
    d = v / np.linalg.norm(v) * 9
    return DashedLine([-d[0], -d[1], 0], [d[0], d[1], 0], color=colour, stroke_width=width, dash_length=0.12)


class SpanTest(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, text, colour=BLACK):
        return boxed(Text(text, font_size=34, color=colour, weight=BOLD)).to_edge(UP, buff=0.3)

    def construct(self):
        self.snaps = []
        ghost = NumberPlane(x_range=[-8, 8], y_range=[-5, 5], background_line_style={"stroke_color": "#E3E3E3"},
                            axis_config={"stroke_color": "#BBBBBB"})
        plane = NumberPlane(x_range=[-10, 10], y_range=[-6, 6], faded_line_ratio=0,
                            background_line_style={"stroke_color": BLUE_C, "stroke_opacity": 0.5},
                            axis_config={"stroke_color": BLUE_C})
        self.add(ghost, plane)

        # Step 1: one vector, its span, and where it lands
        v = np.array([1.0, 1.0])
        line, vec = span_line(v), arrow(v, ORANGE_C)
        cap = self.caption("A vector and its span (dashed line)")
        self.play(Create(line), GrowArrow(vec), FadeIn(cap))
        self.wait(0.6)
        self.snap()
        new_cap = self.caption("After the matrix: knocked off its span", RED_C)
        self.play(ApplyMatrix(A, plane), Transform(vec, arrow(A @ v, RED_C)), FadeTransform(cap, new_cap),
                  run_time=2.5)
        self.bring_to_front(line, vec, new_cap)
        self.wait(1)
        self.snap()

        # Step 2: eight vectors, their spans, all transformed at once
        self.play(FadeOut(vec), FadeOut(line), FadeOut(new_cap), ApplyMatrix(np.linalg.inv(A), plane), run_time=1.5)
        lines = VGroup(*[span_line(u) for u in VECS])
        vecs = VGroup(*[arrow(u, ORANGE_C) for u in VECS])
        cap = self.caption("Eight vectors, eight spans")
        self.play(Create(lines), LaggedStart(*[GrowArrow(a) for a in vecs], lag_ratio=0.1), FadeIn(cap))
        self.wait(0.6)
        cap2 = self.caption("Which ones stay on their own line?")
        self.play(ApplyMatrix(A, plane),
                  *[Transform(a, arrow(A @ u, GREEN_C if on_span(u) else RED_C)) for a, u in zip(vecs, VECS)],
                  FadeTransform(cap, cap2), run_time=3)
        self.bring_to_front(lines, vecs, cap2)
        self.wait(0.8)
        self.snap()

        # Step 3: the two eigenvector lines
        keep = [i for i, u in enumerate(VECS) if on_span(u)]
        eig_lines = VGroup(*[span_line(VECS[i], GREEN_C, 6) for i in keep])
        cap3 = self.caption("Only 2 of 8 stay on their span: the eigenvectors", GREEN_C)
        self.play(FadeOut(VGroup(*[vecs[i] for i in range(8) if i not in keep])), lines.animate.set_opacity(0.25),
                  Create(eig_lines), FadeTransform(cap2, cap3))
        self.bring_to_front(*[vecs[i] for i in keep])
        tags = VGroup(boxed(MathTex(r"\times 3", font_size=54, color=GREEN_C)).move_to([5.3, -0.55, 0]),
                      boxed(MathTex(r"\times 2", font_size=54, color=GREEN_C)).move_to([-3.4, 2.45, 0]))
        self.play(FadeIn(tags))
        self.wait(1)
        formula = boxed(MathTex(r"A\mathbf{v} = \lambda \mathbf{v}", font_size=64, color=BLACK), 0.15)
        formula.to_corner(DR, buff=0.5)
        self.play(FadeIn(formula))
        self.wait(2)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert [i for i, u in enumerate(VECS) if on_span(u)] == [0, 6]      # 0 and 135 degrees: (1, 0) and (-1, 1)
    assert np.allclose(A @ VECS[0], 3 * VECS[0]) and np.allclose(A @ VECS[6], 2 * VECS[6])
    name = "span_test"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = SpanTest()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48:stats_mode=diff[p];"
                    "[b][p]paletteuse=dither=none:diff_mode=rectangle",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
