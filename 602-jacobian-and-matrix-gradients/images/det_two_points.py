"""One map, two points: areas stretch at one and shrink at the other (idea after Khan Academy, "The Jacobian
Determinant"; our own code). The map g(x, y) = (x + sin y, y + sin x) bends a grid; two insets zoom on a tiny square
at (-2, 1) and at (0, 1) while the map plays. The area readout ends at det J = 1 - cos x cos y: 1.22 and 0.46.
Run: python det_two_points.py  -> det_two_points.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#B279A2", "#9A9A9A"
Text.set_default(color=BLACK, font="Latin Modern Roman")
POINTS = [(np.array([-2.0, 1.0]), ORANGE_C), (np.array([0.0, 1.0]), PURPLE_C)]
D = 0.08                                            # side of the tiny input square
INSETS = [np.array([1.6, -0.2]), np.array([5.2, -0.2])]
MAG = 1.3 / D                                       # the input square is 1.3 screen units wide in the inset


def g(p):
    return np.array([p[0] + np.sin(p[1]), p[1] + np.sin(p[0])])


def det_j(p):
    return 1 - np.cos(p[0]) * np.cos(p[1])


def sc(p):
    return np.array([-3.8 + 1.1 * (p[0] + 0.5), -0.5 + 1.1 * (p[1] - 1.0), 0])


def square(p, d, n=12):
    s = np.linspace(-d / 2, d / 2, n)
    c = np.full(n, d / 2)
    xs = np.r_[s, c, s[::-1], -c] + p[0]
    ys = np.r_[-c, s, c, s[::-1]] + p[1]
    return np.c_[xs, ys]


def area(poly):
    x, y = poly[:, 0], poly[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class TwoPoints(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        w = ValueTracker(0.0)
        warp = lambda p: (1 - w.get_value()) * np.asarray(p) + w.get_value() * g(p)
        u = np.linspace(0, 1, 40)

        def grid():
            out = VGroup()
            for x in np.arange(-3, 1.01, 0.5):
                out.add(VMobject(stroke_color=BLUE_C, stroke_width=2).set_points_smoothly(
                    [sc(warp([x, 2 * a])) for a in u]))
            for y in np.arange(0, 2.01, 0.5):
                out.add(VMobject(stroke_color=BLUE_C, stroke_width=2).set_points_smoothly(
                    [sc(warp([-3 + 4 * a, y])) for a in u]))
            for p, col in POINTS:
                out.add(Dot(sc(warp(p)), color=col, radius=0.09))
            return out

        def inset(k):
            p, col = POINTS[k]
            c = INSETS[k]
            centre = warp(p)
            to = lambda q: np.array([c[0] + MAG * (q[0] - centre[0]), c[1] + MAG * (q[1] - centre[1]), 0])
            out = VGroup()
            for t in np.linspace(-D / 2, D / 2, 5):          # a dense grid inside the tiny square
                out.add(Line(to(warp(p + [t, -D / 2])), to(warp(p + [t, D / 2])), color=BLUE_C, stroke_width=1.5))
                out.add(Line(to(warp(p + [-D / 2, t])), to(warp(p + [D / 2, t])), color=BLUE_C, stroke_width=1.5))
            ref = square(np.zeros(2), D)
            out.add(DashedVMobject(Polygon(*[np.array([c[0] + MAG * a, c[1] + MAG * b, 0]) for a, b in ref],
                                           color=GREY_C, stroke_width=3), num_dashes=24))
            img = np.array([warp(q) for q in square(p, D)])
            out.add(Polygon(*[to(q) for q in img], color=col, stroke_width=4, fill_color=col, fill_opacity=0.35))
            ratio = area(img) / D ** 2
            out.add(boxed(Text(f"area × {ratio:.2f}", font_size=32, color=col), 0.06).move_to([c[0], c[1] - 1.75, 0]))
            return out

        frames = VGroup(*[Square(side_length=3.2, color=GREY_C, stroke_width=2).move_to([*c, 0]) for c in INSETS])
        heads = VGroup(*[boxed(Text(f"zoom at ({p[0]:.0f}, {p[1]:.0f})", font_size=30, color=col), 0.05)
                         .next_to(fr, UP, buff=0.12) for (p, col), fr in zip(POINTS, frames)])
        title = boxed(MathTex(r"g(x, y) = (x + \sin y,\ y + \sin x)", color=BLACK, font_size=42), 0.1)
        title.to_edge(UP, buff=0.15)
        self.add(always_redraw(grid), frames, heads, title, always_redraw(lambda: inset(0)),
                 always_redraw(lambda: inset(1)))
        self.wait(1.0)
        self.snap()                                    # before: both tiny squares have area x 1.00
        self.play(w.animate.set_value(0.5), run_time=2.0, rate_func=linear)
        self.snap()                                    # half way
        self.play(w.animate.set_value(1.0), run_time=2.0, rate_func=linear)
        dets = VGroup(*[boxed(MathTex(rf"\det J = {det_j(p):.2f}", color=col,
                                      font_size=40), 0.06).move_to([c[0], c[1] - 2.45, 0])
                        for (p, col), c in zip(POINTS, INSETS)])
        msg = boxed(Text("stretched at (−2, 1), squashed at (0, 1)", font_size=30), 0.1).move_to([-3.4, -3.45, 0])
        self.play(FadeIn(dets), FadeIn(msg))
        self.wait(2.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (len(frames) * w + (len(frames) - 1) * gap, h), "white")
    for i, fr in enumerate(frames):
        sheet.paste(fr.convert("RGB"), (i * (w + gap), 0))
    sheet.save(out)


if __name__ == "__main__":
    # the Note's numbers: det J at the two points, and the tiny squares' area ratios agree with it
    assert abs(det_j(POINTS[0][0]) - 1.2248) < 1e-3 and abs(det_j(POINTS[1][0]) - 0.4597) < 1e-3
    for p, _ in POINTS:
        assert abs(area(np.array([g(q) for q in square(p, D)])) / D ** 2 - det_j(p)) < 0.01
    name = "det_two_points"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = TwoPoints()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid([scene.snaps[0], scene.snaps[2]], HERE / f"{name}_frames.png")
    shutil.rmtree(media)
