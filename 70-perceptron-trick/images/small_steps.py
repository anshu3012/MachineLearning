"""The perceptron trick in small steps (learning rate 0.1) on the Note's own line 2x + 3y + 5 = 0.
Case 1: the negative point (5, 2) sits on the positive side; each step subtracts 0.1 (5, 2, 1) and the line swings
towards it until it crosses (step 8). Case 2: the positive point (-3, -2) sits on the negative side; each step adds
0.1 (-3, -2, 1) until it crosses (step 6).
Run: python small_steps.py -> small_steps.gif, small_steps_frames.png"""
import shutil
import subprocess
from pathlib import Path

import manimpango
import numpy as np
from manim import *
from PIL import Image

for f in Path("/usr/share/texmf/fonts/opentype/public/lm").glob("lmroman10-*.otf"):   # pango on topgro misses LM
    manimpango.register_font(str(f))

HERE = Path(__file__).parent
BLUE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)
W0, LR, LIM = np.array([2.0, 3.0, 5.0]), 0.1, 6
CASES = [  # point, class, sign of the update, steps until it crosses
    (np.array([5.0, 2.0]), "negative", -1, 8),
    (np.array([-3.0, -2.0]), "positive", +1, 6),
]


def halfplane(w, sign):
    """Corners of the box [-LIM, LIM]^2 where sign * (w . (x, y, 1)) >= 0 (one clip of the square)."""
    box = [(-LIM, -LIM), (LIM, -LIM), (LIM, LIM), (-LIM, LIM)]
    f = lambda p: sign * (w[0] * p[0] + w[1] * p[1] + w[2])
    out = []
    for a, b in zip(box, box[1:] + box[:1]):
        fa, fb = f(a), f(b)
        if fa >= 0:
            out.append(a)
        if fa * fb < 0:
            t = fa / (fa - fb)
            out.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
    return out


def fmt(v):
    return f"{v:.1f}".replace("-", "−") if abs(v) >= 0.05 else "0"


class SmallSteps(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[-LIM, LIM, 2], y_range=[-LIM, LIM, 2], x_length=6.4, y_length=6.4, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 28,
                               "decimal_number_config": {"color": GREY_C, "num_decimal_places": 0}}).to_edge(LEFT, buff=0.35)
        ax.shift(DOWN * 0.15)
        self.add(ax)
        for case, (pt, cls, sgn, n) in enumerate(CASES):
            k = ValueTracker(0)
            w_of = lambda: W0 + sgn * LR * k.get_value() * np.array([pt[0], pt[1], 1.0])

            def region(sign, colour):
                def make():
                    corners = halfplane(w_of(), sign)
                    return Polygon(*[ax.c2p(*c) for c in corners], stroke_width=0, fill_color=colour,
                                   fill_opacity=0.18).set_z_index(-2)
                return always_redraw(make)

            def line_mob():
                c = [q for q in halfplane(w_of(), +1) if abs(w_of() @ (q[0], q[1], 1)) < 1e-9]
                return Line(ax.c2p(*c[0]), ax.c2p(*c[-1]), color=BLACK, stroke_width=6)

            pos, neg = region(+1, GREEN_C), region(-1, BLUE_C)
            line = always_redraw(line_mob)
            ghost = DashedLine(*[ax.c2p(*q) for q in halfplane(W0, +1) if abs(W0 @ (q[0], q[1], 1)) < 1e-9],
                               color=GREY_C, stroke_width=4)
            colour = BLUE_C if cls == "negative" else GREEN_C
            dot = Dot(ax.c2p(*pt), radius=0.16, color=colour, stroke_color=BLACK, stroke_width=2).set_z_index(3)
            ring = Circle(radius=0.3, color=RED_C, stroke_width=5).move_to(dot).set_z_index(3)
            word = "subtract" if sgn < 0 else "add"
            title = VGroup(Text(f"{cls} point ({pt[0]:.0f}, {pt[1]:.0f}), wrong side".replace("-", "−"),
                                font_size=32),
                           Text(f"each step: {word} 0.1 × ({pt[0]:.0f}, {pt[1]:.0f}, 1)".replace("-", "−"), font_size=30,
                                color=RED_C)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([3.55, 3.2, 0])
            legend = VGroup(Text("green: positive side", font_size=26, color=GREEN_C),
                            Text("blue: negative side", font_size=26, color=BLUE_C),
                            Text("dashed: start line", font_size=26, color=GREY_C)
                            ).arrange(DOWN, buff=0.1, aligned_edge=LEFT).to_corner(DR, buff=0.45)

            def panel():
                kk = int(round(k.get_value()))
                w = W0 + sgn * LR * kk * np.array([pt[0], pt[1], 1.0])
                v = w @ np.array([pt[0], pt[1], 1.0])
                vcol = GREEN_C if v > 1e-9 else (BLUE_C if v < -1e-9 else GREY_C)
                g = VGroup(Text(f"step {kk}", font_size=34),
                           Text(f"{fmt(w[0])}x + {fmt(w[1])}y + {fmt(w[2])} = 0".replace("+ −", "− "),
                                font_size=36),
                           Text(f"value at the point: {fmt(v)}", font_size=34, color=vcol)
                           ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
                return g.next_to(title, DOWN, buff=0.55).set_x(3.55)

            info = always_redraw(panel)
            self.play(FadeIn(pos), FadeIn(neg), FadeIn(ghost), Create(line), FadeIn(dot), FadeIn(title),
                      FadeIn(info), FadeIn(legend), run_time=0.8)
            self.play(Create(ring), run_time=0.5)
            self.wait(0.8)
            if case == 0:
                self.snap()
            for s in range(1, n + 1):
                self.play(k.animate.set_value(s), run_time=0.55)
                self.wait(0.25)
                if case == 0 and s == 4:
                    self.snap()
            done = Text("crossed: now on its own side", font_size=32, color=RED_C).next_to(info, DOWN, buff=0.4,
                                                                                          aligned_edge=LEFT)
            self.play(FadeIn(done), FadeOut(ring), run_time=0.5)
            self.wait(1.8)
            self.snap()
            info.clear_updaters(); pos.clear_updaters(); neg.clear_updaters(); line.clear_updaters()
            self.play(*[FadeOut(m) for m in (pos, neg, line, ghost, dot, title, info, legend, done)], run_time=0.5)


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    for pt, _, sgn, n in CASES:   # the step counts in the Note: last step crosses, the one before does not
        x = np.array([pt[0], pt[1], 1.0])
        v = lambda s: round((W0 + sgn * LR * s * x) @ x, 9)
        assert np.sign(v(n)) == sgn and np.sign(v(n - 1)) != sgn, (pt, v(n - 1), v(n))
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "small_steps", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = SmallSteps()
        scene.render()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(next(media.rglob("small_steps.mp4"))), "-vf",
                    "fps=10,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "small_steps.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "small_steps_frames.png")
    shutil.rmtree(media)
