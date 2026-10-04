"""Dot product and angle: a stays fixed, b turns around it; a . b = |a||b| cos(theta) goes from positive to 0 to negative.
Run: python angle_dot.py  -> angle_dot.mp4, angle_dot.gif, angle_dot_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
A = np.array([3.0, 1.0])                 # fixed vector a
R = 2.5                                  # length of b
ANG_A = np.arctan2(A[1], A[0])


class AngleDot(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 4, 1], x_length=7.2, y_length=6.3,
                            background_line_style={"stroke_color": "#DDDDDD", "stroke_width": 1},
                            axis_config={"stroke_color": GREY_C}).shift(LEFT * 3.1 + DOWN * 0.3)
        self.add(plane)
        o = plane.c2p(0, 0)
        theta = ValueTracker(np.deg2rad(30))

        def b_vec():
            t = ANG_A + theta.get_value()
            return np.array([R * np.cos(t), R * np.sin(t)])

        va = Arrow(o, plane.c2p(*A), buff=0, color=BLUE_C, stroke_width=7, max_tip_length_to_length_ratio=0.12)
        la = MathTex("a = [3, 1]", font_size=34, color=BLUE_C).next_to(plane.c2p(*A), DOWN + RIGHT * 0.3, buff=0.25)
        vb = always_redraw(lambda: Arrow(o, plane.c2p(*b_vec()), buff=0, color=ORANGE_C, stroke_width=7,
                                         max_tip_length_to_length_ratio=0.12))
        def b_label():
            b = b_vec()
            n = np.array([-b[1], b[0]]) / R                     # unit normal, counter-clockwise side
            return MathTex("b", font_size=40, color=ORANGE_C).move_to(plane.c2p(*(b * 0.6 + n * 0.45)))
        lb = always_redraw(b_label)
        arc = always_redraw(lambda: Arc(radius=0.7, start_angle=ANG_A, angle=theta.get_value(), arc_center=o,
                                        color=GREEN_C, stroke_width=5))

        def panel():
            th = theta.get_value()
            c = np.cos(th)
            dot = float(A @ b_vec())
            col = GREEN_C if dot > 1e-6 else (RED_C if dot < -1e-6 else GREY_C)
            word = r"\text{acute: } a \cdot b > 0" if dot > 1e-6 else (r"\text{obtuse: } a \cdot b < 0" if dot < -1e-6
                                                                     else r"\text{right angle: } a \cdot b = 0")
            rows = VGroup(
                MathTex(rf"\theta = {np.rad2deg(th):.0f}^\circ", font_size=42, color=GREEN_C),
                MathTex(rf"\cos\theta = {c:+.2f}".replace("+0.00", "0.00").replace("-0.00", "0.00"), font_size=42, color=BLACK),
                MathTex(rf"a \cdot b = \lVert a\rVert\,\lVert b\rVert \cos\theta = {dot:+.2f}".replace("+0.00", "0.00").replace("-0.00", "0.00"), font_size=36, color=BLACK),
                MathTex(word, font_size=40, color=col),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
            return rows.to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        info = always_redraw(panel)
        title = Text("The dot product follows the angle", font_size=36, weight=BOLD).to_edge(UP, buff=0.25)
        self.add(title)
        self.play(GrowArrow(va), FadeIn(la), FadeIn(vb), FadeIn(lb), FadeIn(arc), FadeIn(info))
        self.wait(0.6)
        self.snap()
        for deg in [90, 150]:
            self.play(theta.animate.set_value(np.deg2rad(deg)), run_time=2.2)
            self.wait(0.6)
            self.snap()
        self.play(theta.animate.set_value(np.deg2rad(0)), run_time=2.5)
        self.wait(1.2)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "angle_dot", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = AngleDot()
        scene.render()
    mp4 = HERE / "angle_dot.mp4"
    shutil.copy(next(media.rglob("angle_dot.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "angle_dot.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "angle_dot_frames.png")
    shutil.rmtree(media)
