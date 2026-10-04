"""The chord test, animated: a chord between two points of the graph slides and stretches.
Left: softplus ln(1 + e^z), convex: every chord stays on or above the graph (green).
Right: q(w) = w^2 (w - 1)^2, not convex: some chords dip below the graph (red gap), e.g. from w = 0.17 to 0.83.
Run: python chord_test.py  -> chord_test.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")


def softplus(z):
    return np.log1p(np.exp(z))


def q(w):
    return w ** 2 * (w - 1) ** 2


PANELS = [  # function, axis range, chord/plot range (graph stays inside the box), y range, axis steps, title
    (softplus, (-3.0, 3.0), (-3.0, 3.0), (0, 3.2), (1, 1), r"\ln(1 + e^z)"),
    (q, (-0.4, 1.4), (-0.33, 1.33), (0, 0.2), (0.5, 0.05), r"w^2 (w - 1)^2"),
]


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def gap(fn, a, b, n=200):
    """Largest amount by which the graph rises above the chord from a to b."""
    x = np.linspace(a, b, n)
    chord = fn(a) + (fn(b) - fn(a)) * (x - a) / (b - a)
    return np.max(fn(x) - chord)


class ChordTest(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        ua, ub = ValueTracker(0.15), ValueTracker(0.45)
        parts = []
        for i, (fn, xr, dom, yr, st, name) in enumerate(PANELS):
            dec = 0 if st[1] >= 1 else 2
            ax = Axes(x_range=[xr[0], xr[1], st[0]], y_range=[yr[0], yr[1], st[1]], x_length=5.8, y_length=4.6,
                      tips=False, axis_config={"color": GREY_C, "font_size": 24},
                      x_axis_config={"include_numbers": True, "decimal_number_config": {"color": BLACK, "num_decimal_places": 1 if i else 0}},
                      y_axis_config={"include_numbers": True, "decimal_number_config": {"color": BLACK, "num_decimal_places": dec}})
            ax.move_to([-3.45 + 6.9 * i, -0.6, 0])
            curve = ax.plot(fn, x_range=[dom[0], dom[1]], color=BLUE_C, stroke_width=5)
            lab = MathTex(name, color=BLUE_C, font_size=40).next_to(ax, UP, buff=0.15)

            def chord(fn=fn, dom=dom, ax=ax):
                a = dom[0] + ua.get_value() * (dom[1] - dom[0])
                b = dom[0] + ub.get_value() * (dom[1] - dom[0])
                bad = gap(fn, a, b) > 1e-6 * (1 + abs(fn(a)))
                col = RED_C if bad else GREEN_C
                x = np.linspace(a, b, 80)
                ch = fn(a) + (fn(b) - fn(a)) * (x - a) / (b - a)
                g = VGroup()
                if bad:   # shade where the graph is above the chord
                    top = np.maximum(fn(x), ch)
                    g.add(Polygon(*[ax.c2p(u, v) for u, v in zip(x, top)], *[ax.c2p(u, v) for u, v in zip(x[::-1], ch[::-1])],
                                  stroke_width=0, fill_color=RED_C, fill_opacity=0.45))
                g.add(Line(ax.c2p(a, fn(a)), ax.c2p(b, fn(b)), color=col, stroke_width=6))
                g.add(Dot(ax.c2p(a, fn(a)), color=col, radius=0.08), Dot(ax.c2p(b, fn(b)), color=col, radius=0.08))
                return g

            parts += [ax, curve, lab, always_redraw(chord)]
        verdict = [boxed(Text("convex", font_size=34, color=GREEN_C), 0.08).move_to([-3.45, 3.45, 0]),
                   boxed(Text("not convex", font_size=34, color=RED_C), 0.08).move_to([3.45, 3.45, 0])]
        rule = boxed(Text("chord on or above the graph: green;  below: red", font_size=28, color=BLACK), 0.08)
        rule.to_edge(DOWN, buff=0.15)
        self.add(*parts, rule)
        self.wait(1.0)
        self.snap()                                    # first chords
        self.play(ua.animate.set_value(0.02), ub.animate.set_value(0.98), run_time=2.5)
        self.wait(0.8)
        self.snap()                                    # wide chord: both pass
        self.play(ua.animate.set_value(0.3), ub.animate.set_value(0.7), run_time=2.5)
        self.wait(0.8)
        self.snap()                                    # w from 0.14 to 0.86: q fails
        self.play(ua.animate.set_value(0.05), ub.animate.set_value(0.5), run_time=2)
        self.play(ua.animate.set_value(0.3), ub.animate.set_value(0.7), run_time=2)
        self.play(FadeIn(verdict[0]), FadeIn(verdict[1]))
        self.wait(2.0)
        self.snap()


def key_frames_grid(frames, out, gap_px=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap_px, 2 * h + gap_px), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap_px), (i // 2) * (h + gap_px)))
    sheet.save(out)


if __name__ == "__main__":
    rng = np.random.default_rng(0)                    # softplus passes every chord; q fails the shown one
    for a, b in np.sort(rng.uniform(-3, 3, (200, 2)), axis=1):
        if b - a > 1e-3:
            assert gap(softplus, a, b) < 1e-9
    assert gap(q, 0.168, 0.832) > 0.04
    name = "chord_test"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = ChordTest()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)
