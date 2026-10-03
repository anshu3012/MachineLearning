"""Gradient descent on the intercept b only (slope fixed at m = 78.35), on the 4-point example.
The loss L(b) is a parabola; each step moves b by learning rate x slope. Real numbers: 100 -> 40.93 -> 29.11 -> 26.75.
Run: python descent_b.py  -> descent_b.mp4, descent_b.gif, descent_b_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
from sklearn.datasets import make_regression

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
X, y = make_regression(n_samples=4, n_features=1, n_informative=1, n_targets=1, noise=80, random_state=13)
x = X.ravel()
M, LR = 78.35, 0.1
loss = lambda b: float(np.sum((y - M * x - b) ** 2))
slope = lambda b: float(-2 * np.sum(y - M * x - b))
bs = [100.0]
for _ in range(3):
    bs.append(bs[-1] - LR * slope(bs[-1]))


class DescentB(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        axes = Axes(x_range=[0, 110, 20], y_range=[0, 40000, 10000], x_length=7.2, y_length=4.8, tips=False,
                    axis_config={"color": GREY_C, "include_numbers": True, "font_size": 22,
                                 "decimal_number_config": {"num_decimal_places": 0, "color": GREY_C}}
                    ).to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        xl = Text("b (intercept)", font_size=22, color=GREY_C).next_to(axes.x_axis, DOWN, buff=0.45)
        yl = Text("loss L(b)", font_size=22, color=GREY_C).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.55)
        curve = axes.plot(loss, x_range=[0, 108], color=BLUE_C, stroke_width=5)
        title = Text("Gradient descent on b (slope fixed at 78.35)", font_size=28, weight=BOLD).to_edge(UP, buff=0.3)
        rule = MathTex(r"b_{\text{new}} = b_{\text{old}} - \eta \cdot \text{slope}", font_size=36,
                       color=BLACK).move_to([3.7, 2.3, 0])
        eta = Text("learning rate = 0.1", font_size=22, color=GREY_C).next_to(rule, DOWN, buff=0.2)
        self.play(Create(axes), FadeIn(xl, yl, title), Create(curve))
        self.play(FadeIn(rule, eta))
        dot = Dot(axes.c2p(bs[0], loss(bs[0])), radius=0.11, color=ORANGE_C)
        self.play(FadeIn(dot))
        info = None
        for i in range(3):
            b, s = bs[i], slope(bs[i])
            # tangent line: its steepness is the slope at b
            span = 9
            tangent = Line(axes.c2p(b - span, loss(b) - s * span), axes.c2p(b + span, loss(b) + s * span),
                           color=RED_C, stroke_width=4)
            new_info = VGroup(Text(f"step {i + 1}", font_size=24, weight=BOLD),
                              Text(f"b = {b:.2f}", font_size=24),
                              Text(f"slope = {s:.1f}", font_size=24, color=RED_C),
                              Text(f"step = 0.1 × {s:.1f} = {LR * s:.2f}", font_size=24),
                              Text(f"new b = {bs[i + 1]:.2f}", font_size=24, color=ORANGE_C, weight=BOLD)
                              ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.7, -0.6, 0])
            if info is None:
                self.play(Create(tangent), FadeIn(new_info))
            else:
                self.play(Create(tangent), FadeTransform(info, new_info))
            info = new_info
            self.wait(0.6)
            self.snap()
            trail = Dot(axes.c2p(b, loss(b)), radius=0.07, color=ORANGE_C, fill_opacity=0.4)
            self.add(trail)
            self.play(dot.animate.move_to(axes.c2p(bs[i + 1], loss(bs[i + 1]))), FadeOut(tangent), run_time=1.2)
        end = VGroup(Text("The slope shrinks near the bottom,", font_size=22),
                     Text("so the steps shrink too.", font_size=22),
                     Text("Best b (OLS): 26.16", font_size=24, color=GREEN_C, weight=BOLD)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.7, -0.6, 0])
        best = DashedLine(axes.c2p(26.16, 0), axes.c2p(26.16, 8000), color=GREEN_C, stroke_width=3)
        self.play(FadeTransform(info, end), Create(best))
        self.wait(1.2)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    for i, b in enumerate(bs):
        print(i, round(b, 3), round(loss(b), 1), round(slope(b), 3))
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "descent_b", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = DescentB()
        scene.render()
    mp4 = HERE / "descent_b.mp4"
    shutil.copy(next(media.rglob("descent_b.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "descent_b.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "descent_b_frames.png")
    shutil.rmtree(media)
