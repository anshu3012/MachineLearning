"""The visual test for linearity: lines stay straight and the origin stays fixed. Four warps of the same grid:
a curving warp (lines bend), a slide (origin moves), a warp that keeps the grid lines straight but bends the diagonal,
and a shear, which passes the test.
Run: python linear_test.py  -> linear_test.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")

WARPS = [  # (map on (x, y), caption, passes the test?)
    (lambda x, y: (x + 0.35 * np.sin(0.9 * y), y + 0.35 * np.sin(0.9 * x)), "lines curve: NOT linear", False),
    (lambda x, y: (x + 1.5, y), "lines straight, but the origin moved: NOT linear", False),
    (lambda x, y: (x, y + 0.08 * x * y), "grid lines straight, but the diagonal bends: NOT linear", False),
    (lambda x, y: (x + y, y), "lines straight, origin fixed: linear (a shear)", True),
]


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def lift(f):
    return lambda p: np.array([*f(p[0], p[1]), 0.0])


class LinearTest(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        self.add(NumberPlane(x_range=[-8, 8], y_range=[-5, 5], background_line_style={"stroke_color": "#E3E3E3"},
                             axis_config={"stroke_color": "#BBBBBB"}))
        plane = NumberPlane(x_range=[-10, 10], y_range=[-7, 7], faded_line_ratio=0,
                            background_line_style={"stroke_color": BLUE_C, "stroke_opacity": 0.45},
                            axis_config={"stroke_color": BLUE_C})
        plane.prepare_for_nonlinear_transform()
        diag = Line([-6, -6, 0], [6, 6, 0], color=ORANGE_C, stroke_width=6).insert_n_curves(60)
        origin = Dot(ORIGIN, color=BLACK, radius=0.11)
        moving = VGroup(plane, diag, origin)
        moving.save_state()
        rule = boxed(Text("Linear: lines stay straight, origin stays fixed", font_size=32, weight=BOLD), 0.12)
        rule.to_edge(UP, buff=0.25)
        home = Circle(radius=0.2, color=BLACK, stroke_width=3)            # where the origin started
        self.add(moving, home, rule)
        self.wait(1)
        for f, text, ok in WARPS:
            colour = GREEN_C if ok else RED_C
            cap = boxed(Text(text, font_size=30, weight=BOLD, color=colour), 0.12).to_edge(DOWN, buff=0.3)
            self.play(ApplyPointwiseFunction(lift(f), moving), run_time=1.6)
            self.play(FadeIn(cap), run_time=0.5)
            self.bring_to_front(rule)
            self.wait(0.9)
            self.snap()
            if not ok:
                self.play(Restore(moving), FadeOut(cap), run_time=0.8)
        self.wait(1)


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    # the bilinear warp keeps grid lines straight but sends the diagonal y = x onto a parabola
    f = WARPS[2][0]
    assert np.allclose([f(2.0, t)[0] for t in (-1, 0, 3)], 2.0)                    # vertical line stays vertical
    ys = [f(t, t)[1] for t in (0.0, 1.0, 2.0)]
    assert not np.isclose(ys[1] - ys[0], ys[2] - ys[1])                           # diagonal is not straight
    name = "linear_test"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = LinearTest()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48:stats_mode=diff[p];[b][p]paletteuse=dither=none:diff_mode=rectangle",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
