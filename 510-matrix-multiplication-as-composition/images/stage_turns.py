"""A seat at (2, 1) on a concert stage. The stage turns 180 degrees, then 90 degrees clockwise: the seat goes
(2, 1) -> (-2, -1) -> (-1, 2). The product of the two turn matrices is one combined turn (90 degrees
counterclockwise) that sends (2, 1) straight to (-1, 2).
Run: python stage_turns.py  -> stage_turns.mp4, .gif, _frames.png (Manim)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C, PURPLE_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B", "#B279A2"
Text.set_default(color=BLACK, font="Latin Modern Roman")
T1 = np.array([[-1, 0], [0, -1]])        # turn 180 degrees
T2 = np.array([[0, 1], [-1, 0]])         # turn 90 degrees clockwise
SEAT = np.array([2, 1])
U = 0.9                                  # screen units per stage unit
C = np.array([-4.1, -0.3, 0])            # where the stage origin sits on screen


def boxed(mob, buff=0.12):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def mat_tex(M):
    return rf"\begin{{bmatrix}} {M[0, 0]} & {M[0, 1]} \\ {M[1, 0]} & {M[1, 1]} \end{{bmatrix}}"


class StageTurns(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def stage(self):
        plane = NumberPlane(x_range=[-3, 3], y_range=[-3, 3], x_length=6 * U, y_length=6 * U,
                            background_line_style={"stroke_color": BLUE_C, "stroke_opacity": 0.35},
                            axis_config={"stroke_color": BLUE_C}).move_to(C)
        front = Rectangle(width=2 * U, height=0.5 * U, color=PURPLE_C, fill_opacity=0.5).move_to(C + np.array([0, -0.6 * U, 0]))
        word = Text("stage front", font_size=24, color=WHITE).move_to(front)
        seat = Dot(C + U * np.array([*SEAT, 0]), radius=0.13, color=ORANGE_C)
        return VGroup(plane, front, word), seat

    def readout(self, lines):
        g = VGroup(*[boxed(MathTex(t, color=c, font_size=32)) for t, c in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        return g.to_edge(RIGHT, buff=0.35).shift(0.3 * UP)

    def turn(self, group, seat, M, p_to):
        self.play(ApplyMatrix(M, group, about_point=C), seat.animate.move_to(C + U * np.array([*p_to, 0])), run_time=2.2)

    def construct(self):
        self.snaps = []
        ghost = NumberPlane(x_range=[-3, 3], y_range=[-3, 3], x_length=6 * U, y_length=6 * U,
                            background_line_style={"stroke_color": "#E3E3E3"}, axis_config={"stroke_color": "#BBBBBB"}).move_to(C)
        self.add(ghost)
        group, seat = self.stage()
        self.add(group, seat)
        title = boxed(Text("Turn the stage twice", font_size=40)).to_edge(UP, buff=0.25)
        r0 = self.readout([(r"\text{seat } (2, 1)", ORANGE_C)])
        self.play(FadeIn(title), FadeIn(r0))
        self.wait(0.8)
        self.snap()
        p1 = T1 @ SEAT
        self.turn(group, seat, T1, p1)
        r1 = self.readout([(r"\text{seat } (2, 1)", ORANGE_C),
                           (r"\text{turn } 180^\circ: \ " + mat_tex(T1) + r"\begin{bmatrix} 2 \\ 1 \end{bmatrix} = \begin{bmatrix} -2 \\ -1 \end{bmatrix}", BLACK)])
        self.play(Transform(r0, r1))
        self.wait(1)
        self.snap()
        p2 = T2 @ p1
        self.turn(group, seat, T2, p2)
        r2 = self.readout([(r"\text{seat } (2, 1)", ORANGE_C),
                           (r"\text{turn } 180^\circ: \ " + mat_tex(T1) + r"\begin{bmatrix} 2 \\ 1 \end{bmatrix} = \begin{bmatrix} -2 \\ -1 \end{bmatrix}", BLACK),
                           (r"\text{turn } 90^\circ \text{ clockwise}: \ " + mat_tex(T2) + r"\begin{bmatrix} -2 \\ -1 \end{bmatrix} = \begin{bmatrix} -1 \\ 2 \end{bmatrix}", BLACK)])
        self.play(Transform(r0, r2))
        self.wait(1.2)
        self.snap()
        # reset, then one combined turn
        self.play(FadeOut(group), FadeOut(seat), FadeOut(r0), FadeOut(title))
        group, seat = self.stage()
        T = T2 @ T1
        title2 = boxed(Text("One combined turn: the product", font_size=40)).to_edge(UP, buff=0.25)
        r3 = self.readout([(mat_tex(T2) + mat_tex(T1) + "=" + mat_tex(T), PURPLE_C),
                           (mat_tex(T) + r"\begin{bmatrix} 2 \\ 1 \end{bmatrix} = \begin{bmatrix} -1 \\ 2 \end{bmatrix}", ORANGE_C),
                           (r"\text{same seat, one step}", BLACK)])
        self.play(FadeIn(group), FadeIn(seat), FadeIn(title2), FadeIn(r3))
        self.turn(group, seat, T, T @ SEAT)
        self.wait(2)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert (T1 @ SEAT == [-2, -1]).all() and (T2 @ T1 @ SEAT == [-1, 2]).all()
    assert (T2 @ T1 == [[0, -1], [1, 0]]).all()                      # 90 degrees counterclockwise
    name = "stage_turns"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = StageTurns()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
