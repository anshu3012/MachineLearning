"""One student of a placement table, [CGPA, IQ] = [8, 80], read as a vector: walk 8 along the CGPA axis, then 80 up
the IQ axis; the arrow from the origin to that point is the vector, written as a column. Swapping the order gives
[80, 8], a CGPA of 80 that cannot exist: the order of a list matters.
Run: python student_vector.py  -> student_vector.mp4, .gif, _frames.png (Manim)"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
CGPA, IQ = 8, 80


def boxed(mob, buff=0.1):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class StudentVector(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 150, 25], x_length=6.6, y_length=5.2, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 30,
                               "decimal_number_config": {"color": GREY_C, "num_decimal_places": 0}})
        ax.to_edge(LEFT, buff=1.0).shift(0.3 * UP)
        xl = Text("CGPA", font_size=32, color=GREY_C).next_to(ax.x_axis, DOWN, buff=0.5)
        yl = Text("IQ", font_size=32, color=GREY_C).next_to(ax.y_axis, UP, buff=0.2)
        self.add(ax, xl, yl)
        p = ax.c2p(CGPA, IQ)
        dot = Dot(p, radius=0.11, color=BLUE_C)
        row = boxed(Text("one student:  CGPA 8,  IQ 80", font_size=34)).to_corner(UR, buff=0.4)
        self.play(FadeIn(dot), FadeIn(row))
        self.wait(0.8)
        self.snap()
        walk_x = DashedLine(ax.c2p(0, 0), ax.c2p(CGPA, 0), color=ORANGE_C, stroke_width=7)
        walk_y = DashedLine(ax.c2p(CGPA, 0), p, color=GREEN_C, stroke_width=7)
        tx = boxed(Text("1. walk 8 along CGPA", font_size=32, color=ORANGE_C)).next_to(row, DOWN, buff=0.35, aligned_edge=RIGHT)
        ty = boxed(Text("2. then 80 up along IQ", font_size=32, color=GREEN_C)).next_to(tx, DOWN, buff=0.2, aligned_edge=RIGHT)
        self.play(Create(walk_x), FadeIn(tx), run_time=1.5)
        self.play(Create(walk_y), FadeIn(ty), run_time=1.5)
        self.wait(0.8)
        self.snap()
        arrow = Arrow(ax.c2p(0, 0), p, buff=0, color=BLUE_C, stroke_width=9, max_tip_length_to_length_ratio=0.08)
        col = boxed(MathTex(r"\mathbf{x} = \begin{bmatrix} 8 \\ 80 \end{bmatrix}", color=BLUE_C, font_size=52))
        col.next_to(ty, DOWN, buff=0.45, aligned_edge=RIGHT)
        tail = boxed(Text("tail at the origin, tip at the point", font_size=28, color=GREY_C)).next_to(col, DOWN, buff=0.25, aligned_edge=RIGHT)
        self.play(GrowArrow(arrow), FadeIn(col), FadeIn(tail), run_time=1.5)
        self.wait(1)
        self.snap()
        swap = boxed(MathTex(r"\begin{bmatrix} 80 \\ 8 \end{bmatrix}", r"\text{: a CGPA of 80?}",
                             color=RED_C, font_size=44)).move_to(tx, aligned_edge=RIGHT).shift(0.1 * UP)
        self.play(FadeOut(tx), FadeOut(ty), FadeIn(swap), run_time=1.2)
        order = boxed(Text("swapped order: no such student", font_size=30, color=RED_C)).next_to(swap, DOWN, buff=0.2, aligned_edge=RIGHT)
        self.play(FadeIn(order))
        self.wait(2)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    name = "student_vector"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = StudentVector()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
