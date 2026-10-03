"""Linear combinations a v + b w. Fixing b and turning a traces a line; turning both reaches every point of the plane.
When w lies on v's line, every combination stays on that one line.
Run: python span_sweep.py  -> span_sweep.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
V, W, W_DEP = np.array([2, 1]), np.array([-1, 1]), np.array([-1, -0.5])


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.9, buff=buff), mob)


def arrow(xy, colour, width=7):
    return Arrow(ORIGIN, [*xy, 0], buff=0, color=colour, stroke_width=width, max_tip_length_to_length_ratio=0.18)


class SpanSweep(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, text):
        return boxed(Text(text, font_size=28, weight=BOLD), 0.12).to_edge(DOWN, buff=0.3)

    def construct(self):
        self.snaps = []
        self.add(NumberPlane(x_range=[-8, 8], y_range=[-5, 5], background_line_style={"stroke_color": "#E3E3E3"},
                             axis_config={"stroke_color": "#BBBBBB"}))
        a, b = ValueTracker(1.0), ValueTracker(1.0)
        w_vec = [W.astype(float)]                                  # list so the updaters see a swap to W_DEP
        tip = lambda: a.get_value() * V + b.get_value() * w_vec[0]
        av = always_redraw(lambda: arrow(a.get_value() * V, BLUE_C, 5))
        bw = always_redraw(lambda: Arrow([*(a.get_value() * V), 0], [*tip(), 0], buff=0, color=ORANGE_C,
                                         stroke_width=5, max_tip_length_to_length_ratio=0.18))
        total = always_redraw(lambda: arrow(tip(), RED_C, 8))
        dot = always_redraw(lambda: Dot([*tip(), 0], color=RED_C, radius=0.09))
        title = boxed(VGroup(MathTex(r"a\,", r"\mathbf{v}", r"+\,b\,", r"\mathbf{w}", font_size=54, color=BLACK),
                             Text("a =", font_size=30), DecimalNumber(1, num_decimal_places=1, include_sign=True, color=BLUE_C),
                             Text("b =", font_size=30), DecimalNumber(1, num_decimal_places=1, include_sign=True, color=ORANGE_C))
                      .arrange(RIGHT, buff=0.25), 0.12).to_corner(UL, buff=0.25)
        title[1][0][1].set_color(BLUE_C)
        title[1][0][3].set_color(ORANGE_C)
        title[1][2].add_updater(lambda m: m.set_value(a.get_value()))
        title[1][4].add_updater(lambda m: m.set_value(b.get_value()))
        v0, w0 = arrow(V, BLUE_C, 9), arrow(W, ORANGE_C, 9)
        names = VGroup(boxed(MathTex(r"\mathbf{v}=[2,1]", color=BLUE_C, font_size=40).move_to([2.9, 0.35, 0])),
                       boxed(MathTex(r"\mathbf{w}=[-1,1]", color=ORANGE_C, font_size=40).move_to([-1.9, 1.5, 0])))
        self.add(v0, w0, names, title)
        self.wait(0.8)
        self.snap()
        self.play(FadeOut(v0, w0, names), FadeIn(av, bw, total, dot))
        # 1. fix b, turn a: the tip runs along a straight line
        trace = TracedPath(lambda: np.array([*tip(), 0.0]), stroke_color=RED_C, stroke_width=4)
        self.add(trace)
        cap = self.caption("b fixed, a changing: the tip draws a straight line")
        self.play(FadeIn(cap))
        self.play(a.animate.set_value(-2.0), run_time=2)
        self.play(a.animate.set_value(2.5), run_time=2.5)
        self.wait(0.4)
        self.snap()
        # 2. turn both: the reachable tips cover the plane
        self.remove(trace)
        cloud = VGroup(*[Dot([*(i * V + j * W), 0], color=RED_C, radius=0.05)
                         for i in np.arange(-3, 3.01, 0.5) for j in np.arange(-4, 4.01, 0.5)
                         if abs((i * V + j * W)[0]) < 7.3 and -3.1 < (i * V + j * W)[1] < 3.6
                         and not ((i * V + j * W)[1] > 2.4 and (i * V + j * W)[0] < -1.5)])
        cap2 = self.caption("a and b both free: the tips fill the whole plane")
        self.play(FadeTransform(cap, cap2), a.animate.set_value(1.5), b.animate.set_value(-2.0), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(d) for d in cloud], lag_ratio=0.01), a.animate.set_value(-1.0),
                  b.animate.set_value(2.0), run_time=3)
        self.bring_to_front(av, bw, total, dot, title, cap2)
        self.wait(0.4)
        self.snap()
        # 3. w on v's line: everything collapses onto one line
        cap3 = self.caption("w = [-1, -0.5] lies on v's line: the span is only that line")
        dep = VGroup(*[Dot([*(i * V + j * W_DEP), 0], color=RED_C, radius=0.05)
                       for i in np.arange(-3, 3.01, 0.5) for j in np.arange(-4, 4.01, 0.5)
                       if abs((i * V + j * W_DEP)[0]) < 7.3])
        line = DashedLine([-7.5, -3.75, 0], [7.5, 3.75, 0], color=RED_C, stroke_width=4)
        self.play(FadeTransform(cap2, cap3), Transform(cloud, dep), run_time=2)
        w_vec[0] = W_DEP.astype(float)
        self.play(Create(line), a.animate.set_value(2.0), b.animate.set_value(1.0), run_time=1.5)
        self.bring_to_front(av, bw, total, dot, title, cap3)
        self.wait(1)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    name = "span_sweep"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = SpanSweep()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
