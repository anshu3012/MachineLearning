"""The two knobs of w^T x + w0 = 0, on iris setosa vs versicolor (petal length x1, petal width x2, cm).
Turning w0 slides the line parallel to itself (w keeps its direction); turning w tilts the line, which stays
perpendicular to w. The shaded side is where w^T x + w0 > 0, the side w points to. With w = [1, 1] and w0 = -3.2,
every versicolor flower is on the positive side and every setosa flower on the negative side.
Run: python hyperplane_knobs.py  -> hyperplane_knobs.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
from sklearn.datasets import load_iris

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C, PURPLE_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B", "#B279A2"
Text.set_default(color=BLACK, font="Latin Modern Roman")
X_ALL, Y_ALL = load_iris(return_X_y=True)
XS, YS = X_ALL[Y_ALL < 2][:, 2:], Y_ALL[Y_ALL < 2]          # setosa (0) and versicolor (1): petal length, width
NORM = np.sqrt(2)                                           # |w| stays sqrt(2), so w = [1, 1] at 45 degrees


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class HyperplaneKnobs(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[0, 6.5, 1], y_range=[0, 3, 1], x_length=6.5 * 1.5, y_length=3 * 1.5, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 30,
                               "decimal_number_config": {"color": BLACK, "num_decimal_places": 0}}).move_to([0.2, -0.45, 0])
        xl = Text("petal length x1 (cm)", font_size=28).next_to(ax.x_axis, DOWN, buff=0.5)
        yl = Text("petal width x2 (cm)", font_size=28).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.45)
        w0, ang = ValueTracker(0.0), ValueTracker(45.0)
        w_vec = lambda: NORM * np.array([np.cos(np.radians(ang.get_value())), np.sin(np.radians(ang.get_value()))])

        def side():                                         # half-plane w^T x + w0 > 0, clipped to the axes box
            w = w_vec()
            box = [(0, 0), (6.5, 0), (6.5, 3), (0, 3)]
            f = lambda p: w @ np.array(p) + w0.get_value()
            pts = []
            for a, b in zip(box, box[1:] + box[:1]):
                if f(a) > 0:
                    pts.append(a)
                if (f(a) > 0) != (f(b) > 0):
                    t = f(a) / (f(a) - f(b))
                    pts.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
            if len(pts) < 3:
                return VGroup()
            return Polygon(*[ax.c2p(*p) for p in pts], stroke_width=0, fill_color=ORANGE_C, fill_opacity=0.15)

        def segment():                                      # the part of the line inside the axes box
            w, c = w_vec(), w0.get_value()
            foot = -c * w / (w @ w)                         # point of the line closest to the origin
            d = np.array([-w[1], w[0]]) / np.linalg.norm(w)
            lo, hi = -50.0, 50.0
            for k, top in ((0, 6.5), (1, 3.0)):
                if abs(d[k]) > 1e-9:
                    t1, t2 = sorted(((0 - foot[k]) / d[k], (top - foot[k]) / d[k]))
                    lo, hi = max(lo, t1), min(hi, t2)
            return foot + lo * d, foot + hi * d, w

        def line():
            a, b, _ = segment()
            return Line(ax.c2p(*a), ax.c2p(*b), color=PURPLE_C, stroke_width=6)

        def normal():                                       # w drawn from the middle of the visible segment
            a, b, w = segment()
            mid = (a + b) / 2
            u, d = w / np.linalg.norm(w), (b - a) / np.linalg.norm(b - a)
            corner = [mid + 0.18 * d, mid + 0.18 * (d + u), mid + 0.18 * u]
            return VGroup(Arrow(ax.c2p(*mid), ax.c2p(*(mid + 0.75 * w)), buff=0, color=PURPLE_C, stroke_width=8,
                                max_tip_length_to_length_ratio=0.3),
                          VMobject(color=PURPLE_C, stroke_width=3).set_points_as_corners([ax.c2p(*q) for q in corner]))

        shade = always_redraw(side)
        hline = always_redraw(line)
        warrow = always_redraw(normal)
        dots = VGroup(*[Dot(ax.c2p(*p), radius=0.07, color=ORANGE_C if c else BLUE_C, fill_opacity=0.85)
                        for p, c in zip(XS, YS)])
        legend = boxed(VGroup(Dot(color=BLUE_C), Text("setosa", font_size=28, color=BLUE_C),
                              Dot(color=ORANGE_C), Text("versicolor", font_size=28, color=ORANGE_C))
                       .arrange(RIGHT, buff=0.15), 0.08).move_to(ax.c2p(5.1, 0.35))
        readout = always_redraw(lambda: boxed(MathTex(
            rf"w = [{w_vec()[0]:.2f},\ {w_vec()[1]:.2f}],\quad w_0 = {w0.get_value():.1f}", color=PURPLE_C,
            font_size=42), 0.1).to_corner(UL, buff=0.25))
        self.add(shade, ax, xl, yl, dots, hline, warrow, legend, readout)
        self.wait(0.8)
        self.snap()
        # 1. turn w0: the line slides, parallel to itself
        cap = boxed(Text("turn w0: the line slides, w keeps its direction", font_size=30, weight=BOLD), 0.1)
        cap.to_corner(UR, buff=0.25).shift(DOWN * 0.8)
        self.play(FadeIn(cap))
        self.play(w0.animate.set_value(-5.5), run_time=3)
        self.play(w0.animate.set_value(-3.2), run_time=1.5)
        self.wait(0.5)
        self.snap()
        # 2. turn w: the line tilts, always perpendicular to w
        cap2 = boxed(Text("turn w: the line tilts, always at 90 degrees to w", font_size=30, weight=BOLD), 0.1)
        cap2.move_to(cap)
        self.play(FadeTransform(cap, cap2))
        self.play(ang.animate.set_value(20.0), run_time=1.5)
        self.play(ang.animate.set_value(65.0), run_time=2)
        self.wait(0.3)
        self.snap()
        self.play(ang.animate.set_value(45.0), run_time=1.2)
        cap3 = boxed(VGroup(MathTex(r"\text{shaded: } w^{\mathsf T}x + w_0 > 0", color=BLACK, font_size=40),
                            Text("every versicolor inside, every setosa outside", font_size=30, weight=BOLD))
                     .arrange(DOWN, buff=0.1), 0.1).to_corner(UR, buff=0.25).shift(DOWN * 0.8)
        self.play(FadeTransform(cap2, cap3))
        self.wait(2)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    score = XS @ np.array([1.0, 1.0]) - 3.2
    assert (score[YS == 1] > 0).all() and (score[YS == 0] < 0).all()   # the final line separates the two species
    name = "hyperplane_knobs"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = HyperplaneKnobs()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48:stats_mode=diff[p];"
                    "[b][p]paletteuse=dither=none:diff_mode=rectangle", str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
