"""SVD as rotate-stretch-rotate: A = U Sigma V^T applied to the unit circle, one factor at a time.
A = [[3, 0], [4, 5]]: V^T turns v1, v2 (at 45 and 135 degrees) onto the axes, Sigma stretches the axes by
sigma1 = 6.71 and sigma2 = 2.24, U turns them onto u1, u2 (at 71.6 degrees). The final ellipse equals A applied directly.
Run: python rotate_stretch_rotate.py  -> rotate_stretch_rotate.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C, PURPLE_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B", "#B279A2"
Text.set_default(color=BLACK, font="Latin Modern Roman")
A = np.array([[3.0, 0.0], [4.0, 5.0]])
S1, S2 = np.sqrt(45), np.sqrt(5)
TH_V, TH_U = np.pi / 4, np.arctan2(3, 1)          # V rotates by 45 degrees, U by 71.57 degrees
K = 0.55                                          # screen units per grid unit
O = np.array([-3.0, 0.0, 0])                     # origin of the plane on screen
V1 = np.array([np.cos(TH_V), np.sin(TH_V)])
V2 = np.array([-np.sin(TH_V), np.cos(TH_V)])


def rot(a):
    return np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class RotateStretchRotate(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        t1, t2, t3 = ValueTracker(0), ValueTracker(0), ValueTracker(0)

        def M():
            R1 = rot(-TH_V * t1.get_value())
            D = np.diag([1 + (S1 - 1) * t2.get_value(), 1 + (S2 - 1) * t2.get_value()])
            R3 = rot(TH_U * t3.get_value())
            return R3 @ D @ R1

        sc = lambda p: O + K * np.array([p[0], p[1], 0])
        plane = NumberPlane(x_range=[-7.5, 7.5], y_range=[-7.5, 7.5], x_length=15 * K, y_length=15 * K,
                            background_line_style={"stroke_color": "#E6E6E6", "stroke_width": 1},
                            axis_config={"stroke_color": "#BBBBBB"}).move_to(O)
        angles = np.linspace(0, 2 * np.pi, 13)[:-1]

        def picture():
            m = M()
            curve = ParametricFunction(lambda t: sc(m @ [np.cos(t), np.sin(t)]), t_range=[0, 2 * np.pi],
                                       color=BLUE_C, stroke_width=5, fill_color=BLUE_C, fill_opacity=0.12)
            dots = VGroup(*[Dot(sc(m @ [np.cos(a), np.sin(a)]), radius=0.06, color=GREY_C) for a in angles])
            a1 = Arrow(sc([0, 0]), sc(m @ V1), buff=0, color=ORANGE_C, stroke_width=7, max_tip_length_to_length_ratio=0.3)
            a2 = Arrow(sc([0, 0]), sc(m @ V2), buff=0, color=GREEN_C, stroke_width=7, max_tip_length_to_length_ratio=0.3)
            return VGroup(curve, dots, a1, a2)

        pic = always_redraw(picture)
        eq = MathTex("A", "=", "U", r"\Sigma", r"V^{\mathsf T}", color=BLACK, font_size=60).move_to([3.9, 3.1, 0])
        mat = MathTex(r"A = \begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix}", color=BLACK, font_size=40).move_to([3.9, 1.9, 0])
        steps = [r"start: unit circle, $\mathbf{v}_1$ and $\mathbf{v}_2$",
                 r"1. $V^{\mathsf T}$: rotate $\mathbf{v}_1, \mathbf{v}_2$ onto the axes",
                 r"2. $\Sigma$: stretch the axes by 6.71 and 2.24",
                 r"3. $U$: rotate the axes onto $\mathbf{u}_1, \mathbf{u}_2$"]
        step_tex = [Tex(s, color=BLACK, font_size=34).move_to([3.9, 0.6, 0]) for s in steps]
        labels = [VGroup(MathTex(r"\mathbf{v}_1", color=ORANGE_C, font_size=40).move_to(sc(1.75 * V1)),
                         MathTex(r"\mathbf{v}_2", color=GREEN_C, font_size=40).move_to(sc(1.75 * V2)))]
        self.add(plane, pic, eq, mat, step_tex[0], labels[0])
        self.wait(0.8)
        self.snap()
        # 1. V^T
        self.play(eq[4].animate.set_color(RED_C), FadeOut(labels[0]), ReplacementTransform(step_tex[0], step_tex[1]))
        self.play(t1.animate.set_value(1), run_time=2)
        lab1 = VGroup(MathTex(r"\mathbf{e}_1", color=ORANGE_C, font_size=40).move_to(sc([1.6, 0.45])),
                      MathTex(r"\mathbf{e}_2", color=GREEN_C, font_size=40).move_to(sc([0.5, 1.6])))
        self.play(FadeIn(lab1))
        self.wait(0.6)
        self.snap()
        # 2. Sigma
        self.play(eq[4].animate.set_color(BLACK), eq[3].animate.set_color(RED_C), FadeOut(lab1),
                  ReplacementTransform(step_tex[1], step_tex[2]))
        self.play(t2.animate.set_value(1), run_time=2.5)
        lab2 = VGroup(boxed(MathTex(r"\sigma_1 \mathbf{e}_1", color=ORANGE_C, font_size=40)).move_to(sc([5.0, 0.7])),
                      boxed(MathTex(r"\sigma_2 \mathbf{e}_2", color=GREEN_C, font_size=40)).move_to(sc([1.0, 3.0])))
        self.play(FadeIn(lab2))
        self.wait(0.6)
        self.snap()
        # 3. U
        self.play(eq[3].animate.set_color(BLACK), eq[2].animate.set_color(RED_C), FadeOut(lab2),
                  ReplacementTransform(step_tex[2], step_tex[3]))
        self.play(t3.animate.set_value(1), run_time=2)
        u1, u2 = rot(TH_U) @ [1, 0], rot(TH_U) @ [0, 1]
        lab3 = VGroup(boxed(MathTex(r"\sigma_1 \mathbf{u}_1", color=ORANGE_C, font_size=40)).move_to(sc(S1 * u1 + [1.3, -0.2])),
                      boxed(MathTex(r"\sigma_2 \mathbf{u}_2", color=GREEN_C, font_size=40)).move_to(sc(S2 * u2 + [-0.6, 0.6])))
        direct = ParametricFunction(lambda t: sc(A @ [np.cos(t), np.sin(t)]), t_range=[0, 2 * np.pi],
                                    color=RED_C, stroke_width=3).set_stroke(opacity=0.9)
        direct = DashedVMobject(direct, num_dashes=40)
        note = Tex(r"dashed red: $A$ applied directly", color=RED_C, font_size=32).move_to([3.9, -0.4, 0])
        self.play(FadeIn(lab3), Create(direct), FadeIn(note))
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    full = rot(TH_U) @ np.diag([S1, S2]) @ rot(-TH_V)
    assert np.allclose(full, A), full
    name = "rotate_stretch_rotate"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = RotateStretchRotate()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
