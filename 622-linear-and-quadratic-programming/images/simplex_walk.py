"""The workshop linear program, built and solved step by step (Manim). First the feasible region is cut out one
constraint at a time (oven, flour, demand). Then a dot walks from corner to corner, each time to a neighbour with a
higher profit: (0, 0) profit 0 -> (3, 0) profit 9 -> (3, 1) profit 11. The next neighbour (1.5, 2.5) earns 9.5, less,
so the walk stops: this is the main idea of the simplex algorithm.
Idea after StatQuest, "Optimization with Linear Programming (and the Simplex Algorithm), Main Ideas!!!"; our own problem.
Run: python simplex_walk.py -> simplex_walk.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
Tex.set_default(color=BLACK)
C = np.array([3.0, 2.0])                                           # profit per batch
BOX = [([-1, 0], 0), ([0, -1], 0), ([1, 0], 5.3), ([0, 1], 4.3)]   # x1, x2 >= 0 and the edge of the plot
CUTS = [([1, 1], 4, r"oven: $x_1 + x_2 \le 4$"), ([1, 3], 9, r"flour: $x_1 + 3x_2 \le 9$"), ([1, 0], 3, r"demand: $x_1 \le 3$")]
WALK = [(0, 0), (3, 0), (3, 1)]
REJECT = (1.5, 2.5)


def clip(rows):
    """Polygon left after clipping a big square with each half-plane a x <= b (Sutherland-Hodgman)."""
    pts = [np.array(p, float) for p in ((-10, -10), (10, -10), (10, 10), (-10, 10))]
    for a, b in rows:
        a, out = np.array(a, float), []
        for i in range(len(pts)):
            p, q = pts[i], pts[(i + 1) % len(pts)]
            fp, fq = a @ p - b, a @ q - b
            if fp <= 0:
                out.append(p)
            if fp * fq < 0:
                out.append(p + (q - p) * fp / (fp - fq))
        pts = out
    return pts


def boxed(mob, buff=0.1):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class SimplexWalk(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[-0.3, 5.3, 1], y_range=[-0.3, 4.3, 1], x_length=6.72, y_length=5.52, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 26,
                               "decimal_number_config": {"color": BLACK, "num_decimal_places": 0}})
        ax.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        xl = Tex("$x_1$ (A)", color=BLACK, font_size=32).next_to(ax.x_axis, DOWN, buff=0.35).align_to(ax.x_axis, RIGHT)
        yl = Tex("$x_2$ (B)", color=BLACK, font_size=32).next_to(ax.y_axis, UP, buff=0.1)
        poly = lambda rows: Polygon(*[ax.c2p(*q) for q in clip(rows)], color=BLUE_C, stroke_width=3,
                                    fill_color=BLUE_C, fill_opacity=0.22)
        rows = [(a, b) for a, b in BOX]
        region = poly(rows)
        head = Tex(r"Step 1: cut out the feasible region", font_size=36).move_to([3.9, 3.2, 0])
        self.add(ax, xl, yl, region, head)
        self.wait(0.6)
        labels = VGroup()
        for k, (a, b, name) in enumerate(CUTS):
            rows.append((a, b))
            xs = np.clip([(b - a[1] * 4.3) / a[0], (b + a[1] * 0.3) / a[0]], -0.3, 5.3)     # stay inside the plot
            p, q = [(x, (b - a[0] * x) / a[1]) if a[1] else (x, y) for x, y in zip(xs, (4.3, -0.3))]
            line = DashedLine(ax.c2p(*p), ax.c2p(*q), color=GREY_C, stroke_width=3)
            lab = Tex(name, font_size=34, color=BLUE_C).move_to([3.9, 2.3 - 0.6 * k, 0])
            labels.add(lab)
            self.play(Create(line), FadeIn(lab), run_time=0.7)
            self.play(Transform(region, poly(rows)), run_time=0.9)
            self.wait(0.3)
        self.wait(0.6)
        self.snap()                                   # the finished region
        head2 = Tex(r"Step 2: walk to a better corner", font_size=36).move_to([3.9, 3.2, 0])
        profit = Tex(r"profit $= 3x_1 + 2x_2$", font_size=34, color=ORANGE_C).move_to([3.9, 0.3, 0])
        self.play(FadeOut(head), FadeIn(head2), FadeIn(profit))
        dot = Dot(ax.c2p(0, 0), color=GREEN_C, radius=0.15)

        def tag(pt, colour, shift):
            return boxed(MathTex(f"{C @ np.array(pt):g}", font_size=40, color=colour), 0.06).move_to(ax.c2p(*pt) + shift)

        shifts = {(0, 0): UP * 0.45 + RIGHT * 0.45, (3, 0): UP * 0.4 + LEFT * 0.4, (3, 1): RIGHT * 0.55, REJECT: UP * 0.45 + RIGHT * 0.3}
        self.play(FadeIn(dot), FadeIn(tag((0, 0), GREEN_C, shifts[(0, 0)])))
        self.wait(0.6)
        notes = [r"A earns 3 a batch, B earns 2:\\ go along $x_1$ first", r"up the edge: profit rises again"]
        note = None
        for (a, b), text, k in zip(zip(WALK[:-1], WALK[1:]), notes, range(2)):
            new = Tex(text, font_size=32).move_to([3.9, -0.8, 0])
            self.play(*([FadeOut(note)] if note else []), FadeIn(new), run_time=0.5)
            note = new
            path = Line(ax.c2p(*a), ax.c2p(*b), color=GREEN_C, stroke_width=9)
            self.play(Create(path), dot.animate.move_to(ax.c2p(*b)), run_time=1.4)
            self.play(FadeIn(tag(b, GREEN_C, shifts[b])), run_time=0.4)
            self.wait(0.7)
            self.snap()                               # at (3, 0), then at (3, 1)
        probe = DashedLine(ax.c2p(*WALK[-1]), ax.c2p(*REJECT), color=RED_C, stroke_width=6)
        bad = Dot(ax.c2p(*REJECT), color=RED_C, radius=0.12)
        end = Tex(r"next corner earns 9.5: worse.\\ Stop at $(3, 1)$, profit 11.", font_size=32, color=RED_C).move_to([3.9, -0.8, 0])
        self.play(FadeOut(note), Create(probe), FadeIn(bad), FadeIn(tag(REJECT, RED_C, shifts[REJECT])), FadeIn(end), run_time=1.2)
        self.play(Indicate(bad, color=RED_C, scale_factor=1.6), run_time=0.8)
        self.wait(2.2)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    corners = clip(BOX[:2] + [(a, b) for a, b, _ in CUTS])
    profits = sorted(round(float(C @ p), 2) for p in corners)
    assert profits == [0, 6, 9, 9.5, 11]                                      # the five corners of the Note's table
    assert [float(C @ np.array(p)) for p in WALK] == [0, 9, 11] and float(C @ np.array(REJECT)) == 9.5
    name = "simplex_walk"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = SimplexWalk()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
