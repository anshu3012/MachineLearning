"""A rank-1 matrix squashes the plane onto a line (idea after 3Blue1Brown, "Inverse matrices, column space and null
space | Chapter 7, Essence of linear algebra"; our own code). C = [[2, 1], [4, 2]] moves the grid: everything lands
on the line through (1, 2), the column space, while the whole line through (-1, 2), the null space, lands on the
origin. v1 lands at length 5 = sigma1, v2 lands on 0 = sigma2.
Run: python rank_one_squash.py  -> rank_one_squash.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, PURPLE_C, RED_C, GREEN_C, GREY_C = "#4C78A8", "#F58518", "#B279A2", "#E45756", "#54A24B", "#C8C8C8"
Text.set_default(color=BLACK, font="Latin Modern Roman")
C = np.array([[2.0, 1.0], [4.0, 2.0]])
V1 = np.array([2.0, 1.0]) / np.sqrt(5)
V2 = np.array([-1.0, 2.0]) / np.sqrt(5)
K, ORG = 0.8, np.array([-3.0, -0.6])


def sc(p):
    return np.array([ORG[0] + K * p[0], ORG[1] + K * p[1], 0])


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class Squash(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        t = ValueTracker(0.0)
        M = lambda: (1 - t.get_value()) * np.eye(2) + t.get_value() * C
        phi = np.linspace(0, 2 * np.pi, 120)

        def picture():
            m = M()
            out = VGroup()
            for i in range(-12, 13):
                out.add(Line(sc(m @ [i, -12]), sc(m @ [i, 12]), color=GREY_C, stroke_width=1.5))
                out.add(Line(sc(m @ [-12, i]), sc(m @ [12, i]), color=GREY_C, stroke_width=1.5))
            out.add(Line(sc(m @ (-6 * V2)), sc(m @ (6 * V2)), color=RED_C, stroke_width=6))       # null space line
            circ = np.c_[np.cos(phi), np.sin(phi)] @ m.T
            out.add(VMobject(stroke_color=BLUE_C, stroke_width=5).set_points_as_corners([sc(p) for p in circ]))
            out.add(Arrow(sc([0, 0]), sc(m @ V1), buff=0, color=ORANGE_C, stroke_width=7,
                          max_tip_length_to_length_ratio=0.15))
            if np.linalg.norm(m @ V2) > 0.05:
                out.add(Arrow(sc([0, 0]), sc(m @ V2), buff=0, color=PURPLE_C, stroke_width=7,
                              max_tip_length_to_length_ratio=0.3))
            out.add(Dot(sc([0, 0]), color=BLACK, radius=0.07))
            g = VGroup(Text(f"|C v₁| = {np.linalg.norm(m @ V1):.2f}", font_size=32, color=ORANGE_C),
                       Text(f"|C v₂| = {np.linalg.norm(m @ V2):.2f}", font_size=32, color=PURPLE_C))
            out.add(boxed(g.arrange(DOWN, aligned_edge=LEFT, buff=0.12), 0.1).move_to([4.3, 1.0, 0]))
            return out

        self.add(always_redraw(picture))
        title = boxed(Text("C = [[2, 1], [4, 2]] moves the plane", font_size=34), 0.08).move_to([3.4, 3.3, 0])
        legend = boxed(VGroup(Text("red line: through (−1, 2)", font_size=28, color=RED_C),
                              Text("blue: the unit circle", font_size=28, color=BLUE_C)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1), 0.08).move_to([4.3, -1.0, 0])
        self.add(title, legend)
        self.wait(1.0)
        self.snap()
        self.play(t.animate.set_value(0.5), run_time=2.0, rate_func=linear)
        self.snap()
        self.play(t.animate.set_value(1.0), run_time=2.0, rate_func=linear)
        col = boxed(Text("column space: the line through (1, 2), rank 1", font_size=26, color=BLUE_C), 0.08)
        nul = boxed(Text("null space: the red line, squashed onto 0", font_size=26, color=RED_C), 0.08)
        VGroup(col, nul).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.3, -2.7, 0])
        self.play(FadeOut(legend), FadeIn(col), FadeIn(nul))
        self.wait(2.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (len(frames) * w + (len(frames) - 1) * gap, h), "white")
    for i, fr in enumerate(frames):
        sheet.paste(fr.convert("RGB"), (i * (w + gap), 0))
    sheet.save(out)


if __name__ == "__main__":
    assert abs(np.linalg.norm(C @ V1) - 5) < 1e-12 and np.allclose(C @ V2, 0)    # the Note's sigma1 = 5, sigma2 = 0
    name = "rank_one_squash"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = Squash()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48:stats_mode=diff[p];"
                    "[b][p]paletteuse=dither=none", str(HERE / f"{name}.gif")], check=True)
    key_frames_grid([scene.snaps[0], scene.snaps[2]], HERE / f"{name}_frames.png")
    shutil.rmtree(media)
