"""Matrix multiplication as composition: rotate 90 degrees, then shear. Following i-hat and j-hat through both
steps gives the columns of the product: i-hat ends at (1, 1), j-hat at (-1, 0).
Run: python composition.py  -> composition.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
R, S = np.array([[0, -1], [1, 0]]), np.array([[1, 1], [0, 1]])


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def vec(xy, colour):
    return Arrow(ORIGIN, [*xy, 0], buff=0, color=colour, stroke_width=9, max_tip_length_to_length_ratio=0.25)


def mat(m):
    out = Matrix(m, element_to_mobject_config={"color": BLACK}, bracket_config={"color": BLACK}, h_buff=0.9)
    out.get_columns()[0].set_color(GREEN_C)
    out.get_columns()[1].set_color(RED_C)
    return out.scale(0.75)


class Composition(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        self.camera.frame_center = np.array([0, 0, 0])
        ghost = NumberPlane(x_range=[-8, 8], y_range=[-5, 5], background_line_style={"stroke_color": "#E3E3E3"},
                            axis_config={"stroke_color": "#BBBBBB"}).scale(1.5)
        plane = NumberPlane(x_range=[-12, 12], y_range=[-12, 12], faded_line_ratio=0,
                            background_line_style={"stroke_color": BLUE_C, "stroke_opacity": 0.35},
                            axis_config={"stroke_color": BLUE_C}).scale(1.5)
        u = 1.5                                              # one grid unit on screen
        i_hat, j_hat = vec([u, 0], GREEN_C), vec([0, u], RED_C)
        step = boxed(Text("start", font_size=34, weight=BOLD), 0.12).to_corner(UL, buff=0.3)
        self.add(ghost, plane, i_hat, j_hat, step)
        self.wait(0.6)
        self.snap()
        s1 = boxed(Text("1. rotate 90°", font_size=34, weight=BOLD), 0.12).to_corner(UL, buff=0.3)
        self.play(FadeTransform(step, s1))
        self.play(ApplyMatrix(R, plane), Transform(i_hat, vec([0, u], GREEN_C)), Transform(j_hat, vec([-u, 0], RED_C)),
                  run_time=2)
        self.wait(0.6)
        self.snap()
        s2 = boxed(Text("2. then shear", font_size=34, weight=BOLD), 0.12).to_corner(UL, buff=0.3)
        self.play(FadeTransform(s1, s2))
        self.play(ApplyMatrix(S, plane), Transform(i_hat, vec([u, u], GREEN_C)), Transform(j_hat, vec([-u, 0], RED_C)),
                  run_time=2)
        labels = VGroup(boxed(MathTex(r"\hat{\imath} \to [1, 1]", color=GREEN_C, font_size=44).move_to([2.6, 1.9, 0])),
                        boxed(MathTex(r"\hat{\jmath} \to [-1, 0]", color=RED_C, font_size=44).move_to([-2.4, -0.6, 0])))
        self.play(FadeIn(labels))
        self.wait(0.6)
        self.snap()
        eq = boxed(VGroup(mat([[1, 1], [0, 1]]), mat([[0, -1], [1, 0]]), MathTex("=", color=BLACK, font_size=48),
                          mat([[1, -1], [1, 0]])).arrange(RIGHT, buff=0.2), 0.15)
        names = VGroup(Text("shear", font_size=24), Text("rotation", font_size=24), Text("both at once", font_size=24))
        for n, m in zip(names, [eq[1][0], eq[1][1], eq[1][3]]):
            n.next_to(m, DOWN, buff=0.12)
        panel = boxed(VGroup(eq[1], names), 0.15).to_corner(DR, buff=0.3)
        self.play(FadeIn(panel))
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert (S @ R == np.array([[1, -1], [1, 0]])).all()
    name = "composition"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = Composition()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
