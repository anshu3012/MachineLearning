"""A product computed column by column. Apply M1 (columns [1, 1] and [-2, 0]), then M2 (columns [0, 1] and [2, 0]).
i-hat sits at [1, 1] after M1, and M2 [1, 1] = [2, 1] is the first column of M2 M1; j-hat sits at [-2, 0], and
M2 [-2, 0] = [0, -2] is the second column.
Run: python column_by_column.py  -> column_by_column.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
M1, M2 = np.array([[1, -2], [1, 0]]), np.array([[0, 2], [1, 0]])
O = np.array([2.2, -0.2, 0])                              # screen position of the origin
K = 1.2                                                   # screen units per grid unit
P = lambda xy: O + K * np.array([xy[0], xy[1], 0.0])


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def vec(xy, colour):
    return Arrow(O, P(xy), buff=0, color=colour, stroke_width=9, max_tip_length_to_length_ratio=0.25)


def mat(rows):
    out = Matrix(rows, element_to_mobject_config={"color": BLACK}, bracket_config={"color": BLACK}, h_buff=0.9)
    out.get_columns()[0].set_color(GREEN_C)
    out.get_columns()[1].set_color(RED_C)
    return out.scale(0.7)


class ColumnByColumn(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def line(self, tex, colour, y):
        return boxed(MathTex(tex, color=colour, font_size=38), 0.08).move_to([-4.0, y, 0])

    def construct(self):
        self.snaps = []
        ghost = NumberPlane(x_range=[-9, 9], y_range=[-6, 6], background_line_style={"stroke_color": "#E3E3E3"},
                            axis_config={"stroke_color": "#BBBBBB"}).scale(K).shift(O)
        plane = NumberPlane(x_range=[-12, 12], y_range=[-9, 9], faded_line_ratio=0,
                            background_line_style={"stroke_color": BLUE_C, "stroke_opacity": 0.35},
                            axis_config={"stroke_color": BLUE_C}).scale(K).shift(O)
        i_hat, j_hat = vec([1, 0], GREEN_C), vec([0, 1], RED_C)
        eq = VGroup(MathTex("M_2", color=BLACK, font_size=44), mat([[0, 2], [1, 0]]),
                    MathTex("M_1", color=BLACK, font_size=44), mat([[1, -2], [1, 0]]),
                    MathTex("=", color=BLACK, font_size=44), mat([["?", "?"], ["?", "?"]])).arrange(RIGHT, buff=0.15)
        eq[1].set_color(BLACK)
        head = boxed(eq, 0.12).to_corner(UL, buff=0.25)
        self.add(ghost, plane, i_hat, j_hat, head)
        self.wait(0.8)
        self.snap()
        # 1. apply M1: i-hat and j-hat land on M1's columns
        self.play(ApplyMatrix(M1, plane, about_point=O), Transform(i_hat, vec(M1[:, 0], GREEN_C)),
                  Transform(j_hat, vec(M1[:, 1], RED_C)), run_time=2.5)
        l1 = self.line(r"\text{after } M_1:\ \hat\imath \to [1, 1],\ \hat\jmath \to [-2, 0]", BLACK, 1.2)
        self.play(FadeIn(l1))
        self.bring_to_front(head)
        self.wait(0.8)
        self.snap()
        # 2. apply M2 to the whole plane; follow both arrows
        self.play(ApplyMatrix(M2, plane, about_point=O), Transform(i_hat, vec(M2 @ M1[:, 0], GREEN_C)),
                  Transform(j_hat, vec(M2 @ M1[:, 1], RED_C)), run_time=2.5)
        self.bring_to_front(head, l1)
        l2 = self.line(r"M_2\,[1, 1] = [2, 1]", GREEN_C, 0.4)
        prod1 = mat([[2, "?"], [1, "?"]]).move_to(eq[5])
        self.play(FadeIn(l2), Transform(eq[5], prod1))
        self.wait(0.8)
        self.snap()
        l3 = self.line(r"M_2\,[-2, 0] = [0, -2]", RED_C, -0.4)
        prod2 = mat([[2, 0], [1, -2]]).move_to(eq[5])
        self.play(FadeIn(l3), Transform(eq[5], prod2))
        self.wait(0.6)
        cap = boxed(VGroup(Text("columns of the product =", font_size=30, weight=BOLD),
                           Text("where i-hat and j-hat end up", font_size=30, weight=BOLD)).arrange(DOWN, buff=0.1),
                    0.12).move_to([-4.0, -2.2, 0])
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
    assert (M2 @ M1 == np.array([[2, 0], [1, -2]])).all()
    name = "column_by_column"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = ColumnByColumn()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48:stats_mode=diff[p];[b][p]paletteuse=dither=none:diff_mode=rectangle",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
