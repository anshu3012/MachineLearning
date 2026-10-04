"""Steepest ascent, watched. At the point (1, 1) of f(x1, x2) = x1^2 + x1 x2 + 2 x2^2 a unit direction u turns full
circle. The slope of f along u is the dot product grad f . u = sqrt(34) cos(angle between u and grad f), traced on
the right: 3 along the x1-axis, a peak of sqrt(34) = 5.83 when u lines up with grad f = [3, 5], 0 along the contour
line, and -5.83 straight downhill.
Intuition after Sanderson (Khan Academy), "Why the gradient is the direction of steepest ascent"; our own code.
Run: python direction_sweep.py  -> direction_sweep.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)
H = np.array([[1.0, 0.5], [0.5, 2.0]])              # f(x) = x^T H x
P0 = np.array([1.0, 1.0])
GRAD = 2 * H @ P0                                     # [3, 5]
PHI = np.degrees(np.arctan2(GRAD[1], GRAD[0]))        # 59.04 degrees


def f(x):
    return x @ H @ x


def slope(deg):
    t = np.radians(deg)
    return GRAD @ np.array([np.cos(t), np.sin(t)])


def boxed(mob, buff=0.1):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class DirectionSweep(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, text, colour=BLACK):
        return boxed(Text(text, font_size=32, color=colour, weight=BOLD)).to_edge(UP, buff=0.2)

    def construct(self):
        self.snaps = []
        # Left: contour map around (1, 1)
        plane = Axes(x_range=[-1.5, 3, 1], y_range=[-1.5, 3, 1], x_length=5.4, y_length=5.4, tips=False,
                     axis_config={"color": GREY_C, "include_numbers": True, "font_size": 30,
                                  "decimal_number_config": {"color": GREY_C, "num_decimal_places": 0}})
        plane.move_to([-3.75, -0.45, 0])
        w, V = np.linalg.eigh(H)
        th = np.linspace(0, 2 * np.pi, 400)
        lo, hi = -1.5, 3.0

        def contour(c, colour="#BBBBBB", width=2):
            pts = (np.c_[np.cos(th), np.sin(th)] * np.sqrt(c / w)) @ V.T
            g, run = VGroup(), []
            for p in pts:
                if lo <= p[0] <= hi and lo <= p[1] <= hi:
                    run.append(plane.c2p(*p))
                    continue
                if len(run) > 1:
                    g.add(VMobject(color=colour, stroke_width=width).set_points_as_corners(run))
                run = []
            if len(run) > 1:
                g.add(VMobject(color=colour, stroke_width=width).set_points_as_corners(run))
            return g

        contours = VGroup(*[contour(c) for c in (0.5, 1.5, 7, 10)], contour(f(P0), GREEN_C, 4))
        x1 = MathTex("x_1", font_size=34, color=GREY_C).next_to(plane.x_axis, RIGHT, buff=0.1)
        x2 = MathTex("x_2", font_size=34, color=GREY_C).next_to(plane.y_axis, UP, buff=0.1)
        dot = Dot(plane.c2p(*P0), color=BLACK, radius=0.08)
        scale = plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0]
        g_end = plane.c2p(*P0) + 1.45 * scale * np.array([*GRAD / np.linalg.norm(GRAD), 0])
        grad_arrow = Arrow(plane.c2p(*P0), g_end, buff=0, color=ORANGE_C, stroke_width=8,
                           max_tip_length_to_length_ratio=0.25)
        grad_tag = boxed(MathTex(r"\nabla f = [3,\ 5]", font_size=36, color=ORANGE_C), 0.05)
        grad_tag.next_to(g_end, UP, buff=0.05)

        # Right: slope against the angle of u
        ax = Axes(x_range=[0, 360, 90], y_range=[-6, 6, 3], x_length=5.6, y_length=4.4, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 30,
                               "decimal_number_config": {"color": GREY_C, "num_decimal_places": 0}})
        ax.move_to([3.55, -0.45, 0])
        ax_x = Text("angle of u (degrees)", font_size=24, color=GREY_C).next_to(ax, DOWN, buff=0.12)
        ax_y = MathTex(r"\nabla f \cdot \mathbf{u}", font_size=34, color=BLUE_C).next_to(ax, UP, buff=0.1)
        peak = VGroup(DashedLine(ax.c2p(0, np.sqrt(34)), ax.c2p(360, np.sqrt(34)), color=ORANGE_C, stroke_width=3),
                      MathTex(r"|\nabla f| = 5.83", font_size=32, color=ORANGE_C).next_to(ax.c2p(360, np.sqrt(34)), UP + LEFT,
                                                                                    buff=0.08))

        ang = ValueTracker(0.0)
        u_arrow = always_redraw(lambda: Arrow(
            plane.c2p(*P0), plane.c2p(*P0) + 1.1 * scale * np.array([np.cos(np.radians(ang.get_value())),
                                                                        np.sin(np.radians(ang.get_value())), 0]),
            buff=0, color=BLUE_C, stroke_width=8, max_tip_length_to_length_ratio=0.3))
        tracer = always_redraw(lambda: Dot(ax.c2p(ang.get_value(), slope(ang.get_value())), color=BLUE_C, radius=0.09))
        trace = always_redraw(lambda: ax.plot(slope, x_range=[0, max(ang.get_value(), 0.5)], color=BLUE_C,
                                              stroke_width=5))
        readout = always_redraw(lambda: boxed(MathTex(
            rf"\theta = {ang.get_value():.0f}^\circ \quad \nabla f \cdot \mathbf{{u}} = {slope(ang.get_value()):.2f}",
            font_size=38), 0.08).move_to([3.55, -3.55, 0]))

        cap = self.caption("At (1, 1), turn a unit direction u and read the slope")
        self.add(contours, plane, x1, x2, dot, ax, ax_x, ax_y, trace, tracer, u_arrow, readout, cap)
        self.wait(1.2)
        self.snap()

        cap2 = self.caption("Slope peaks when u lines up with the gradient", ORANGE_C)
        self.play(ang.animate.set_value(PHI), run_time=3, rate_func=linear)
        self.play(GrowArrow(grad_arrow), FadeIn(grad_tag), Create(peak), FadeTransform(cap, cap2))
        self.bring_to_front(u_arrow)
        self.wait(1.5)
        self.snap()

        cap3 = self.caption("At right angles: slope 0, we walk along the contour", GREEN_C)
        self.play(ang.animate.set_value(PHI + 90), FadeTransform(cap2, cap3), run_time=2.5, rate_func=linear)
        self.wait(1.5)
        self.snap()

        cap4 = self.caption("Opposite the gradient: steepest downhill, -5.83", RED_C)
        self.play(ang.animate.set_value(PHI + 180), FadeTransform(cap3, cap4), run_time=2.5, rate_func=linear)
        self.wait(1.2)
        self.snap()
        self.play(ang.animate.set_value(360), run_time=2.5, rate_func=linear)
        self.wait(2)


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, fr in enumerate(frames[:4]):
        sheet.paste(fr.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert np.allclose(GRAD, [3, 5]) and abs(slope(0) - 3) < 1e-9
    degs = np.linspace(0, 360, 36001)
    assert abs(degs[np.argmax(slope(degs))] - PHI) < 0.02 and abs(slope(PHI) - np.sqrt(34)) < 1e-9
    assert abs(slope(PHI + 90)) < 1e-9 and abs(slope(PHI + 180) + np.sqrt(34)) < 1e-9
    name = "direction_sweep"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = DirectionSweep()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48:stats_mode=diff[p];"
                    "[b][p]paletteuse=dither=none:diff_mode=rectangle", str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
